# ppo_trainer.py
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions.normal import Normal
from torch.utils.tensorboard import SummaryWriter
import ppo_core

class PPOAgent(nn.Module):
    def __init__(self, obs_dim, act_dim):
        super().__init__()
        self.critic = nn.Sequential(nn.Linear(obs_dim, 256), nn.Tanh(), nn.Linear(256, 256), nn.Tanh(), nn.Linear(256, 1))
        self.actor_mean = nn.Sequential(nn.Linear(obs_dim, 256), nn.Tanh(), nn.Linear(256, 256), nn.Tanh(), nn.Linear(256, act_dim))
        self.actor_logstd = nn.Parameter(torch.full((1, act_dim), -0.5))

    def get_value(self, x): 
        return self.critic(x)
        
    def get_action_and_value(self, x, action=None):
        action_mean = self.actor_mean(x)
        action_std = self.actor_logstd.exp().expand_as(action_mean)
        probs = Normal(action_mean, action_std)
        if action is None: action = probs.sample()
        return action, probs.log_prob(action).sum(1), probs.entropy().sum(1), self.critic(x)

def train_ppo(env, agent, optimizer, num_updates=50, num_steps=50, gamma=0.99, lam=0.95, clip_coef=0.2, writer=None, eval_freq=0, eval_callback=None):
    num_envs = env.num_envs
    device = next(agent.parameters()).device
    obs_dim = env.observation_space.shape[1] if len(env.observation_space.shape) > 1 else env.observation_space.shape[0]
    act_dim = env.action_space.shape[1] if len(env.action_space.shape) > 1 else env.action_space.shape[0]

    # 铁律：在整个 2000 轮的生命周期里，env.reset() 只能在这里执行这唯独的一次！
    obs, _ = env.reset() 

    for update in range(1, num_updates + 1):
        obs_buf = torch.zeros((num_steps, num_envs, obs_dim), device=device)
        act_buf = torch.zeros((num_steps, num_envs, act_dim), device=device)
        logprobs_buf, rewards_buf, dones_buf, values_buf = [torch.zeros((num_steps, num_envs), device=device) for _ in range(4)]
        

        ep_reach, ep_grasp, ep_lift, ep_table_pen, ep_action_pen, ep_track = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

        for step in range(num_steps):
            obs_buf[step] = obs
            with torch.no_grad():
                action, logprob, _, value = agent.get_action_and_value(obs)
            values_buf[step] = value.flatten()
            act_buf[step] = action
            logprobs_buf[step] = logprob
            
            obs, reward, terminated, truncated, info = env.step(action)
            rewards_buf[step] = reward
            dones_buf[step] = terminated | truncated
            

            # if "r_reach" in info: ep_reach += info["r_reach"].mean().item()
            # if "r_grasp" in info: ep_grasp += info["r_grasp"].mean().item()
            # if "r_lift"  in info: ep_lift  += info["r_lift"].mean().item()
            # if "r_table_pen" in info: ep_table_pen += info["r_table_pen"].mean().item()
            if "r_action_pen" in info: ep_action_pen += info["r_action_pen"].mean().item()
            if "r_track" in info: ep_track += info["r_track"].mean().item()
            if "r_grasp" in info: ep_grasp += info["r_grasp"].mean().item()

            
            

        with torch.no_grad():
            next_value = agent.get_value(obs).flatten()
        
        values_for_gae = torch.cat([values_buf, next_value.unsqueeze(0)])
        advantages, returns = ppo_core.compute_gae_advantages(rewards_buf, values_for_gae, dones_buf, gamma, lam)
        

        b_obs = obs_buf.reshape(-1, obs_dim)
        b_logprobs = logprobs_buf.reshape(-1)
        b_actions = act_buf.reshape(-1, act_dim)
        b_advantages = advantages.reshape(-1)
        b_returns = returns.reshape(-1)

        # ------------------------------------------------------------------
        # 💉 工业级 PPO 灵魂升级包：K-Epochs 与 Mini-batch 榨干机制
        # ------------------------------------------------------------------
        update_epochs = 4                 # 核心：把这12800条数据在内存里反复回传 4 轮！
        num_minibatches = 4               # 把数据切成 4 个小批次 (每批3200条)
        batch_size = num_steps * num_envs
        minibatch_size = batch_size // num_minibatches

        # 全局 Advantage 归一化（严格铁律：只在最外层做一次，绝对不能在小批次里做！）
        b_advantages = (b_advantages - b_advantages.mean()) / (b_advantages.std() + 1e-8)

        inds = torch.arange(batch_size, device=device)

        for epoch in range(update_epochs):
            # 每轮开始前，把12800个样本的顺位随机打乱
            inds = inds[torch.randperm(batch_size, device=device)]
            
            for start in range(0, batch_size, minibatch_size):
                end = start + minibatch_size
                mb_inds = inds[start:end] # 抽出来的3200个随机索引

                _, newlogprob, entropy, newvalue = agent.get_action_and_value(
                    b_obs[mb_inds], 
                    b_actions[mb_inds]
                )

                mb_advantages = b_advantages[mb_inds]
                mb_logprobs = b_logprobs[mb_inds]
                mb_returns = b_returns[mb_inds]

                # 1. 算 Actor Loss
                actor_loss = ppo_core.compute_ppo_clip_loss(newlogprob, mb_logprobs, mb_advantages, clip_coef)
                
                # 2. 算 Critic Loss
                critic_loss = nn.functional.mse_loss(newvalue.flatten(), mb_returns)
                
                # 3. 算 Entropy 探索熵
                entropy_loss = entropy.mean()

                loss = actor_loss + 0.5 * critic_loss - 0.01 * entropy_loss

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
        # ------------------------------------------------------------------
        
        if writer is not None:
            # real_update = update + update_offset
            # global_step = real_update * num_steps * num_envs
            global_step = update * num_steps * num_envs
            # global_step = update * num_steps * num_envs
            writer.add_scalar("Loss/Actor", actor_loss.item(), global_step)
            writer.add_scalar("Loss/Critic(Value)", critic_loss.item(), global_step)
            writer.add_scalar("Policy/Entropy", entropy_loss.item(), global_step)
            writer.add_scalar("Reward/Total_Avg", rewards_buf.mean().item(), global_step)
            # writer.add_scalar("Reward_Breakdown/Reaching", ep_reach / num_steps, global_step)
            # writer.add_scalar("Reward_Breakdown/Grasping", ep_grasp / num_steps, global_step)
            # writer.add_scalar("Reward_Breakdown/Lifting", ep_lift / num_steps, global_step)
            # writer.add_scalar("Reward_Breakdown/Table_Penalty", ep_table_pen / num_steps, global_step)
            writer.add_scalar("Reward_Breakdown/Action_Penalty", ep_action_pen / num_steps, global_step)
            writer.add_scalar("Reward_Breakdown/Tracking", ep_track / num_steps, global_step)
            writer.add_scalar("Reward_Breakdown/Grasping", ep_grasp / num_steps, global_step)

            writer.add_scalar("Debug/adv_mean", b_advantages.mean().item(), global_step)
            writer.add_scalar("Debug/action_mag", b_actions.norm(dim=1).mean().item(), global_step)

        if update % 10 == 0:
            print(f"Update {update:03d}/{num_updates} | R_Total: {rewards_buf.mean().item():.4f} | R_Track: {ep_track/num_steps:.4f} | R_grasp: {ep_grasp/num_steps:.4f} | Ent: {entropy_loss.item():.4f}")
        
        if eval_freq > 0 and (update % eval_freq == 0) and (eval_callback is not None):
            eval_callback(update)