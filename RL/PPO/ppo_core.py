# ppo_core.py
import torch

def compute_gae_advantages(rewards: torch.Tensor, values: torch.Tensor, dones: torch.Tensor, gamma: float = 0.99, lam: float = 0.95):
    """
    计算广义优势估计 (GAE - Generalized Advantage Estimation)
    
    参数:
        rewards: shape (num_steps, num_envs)
        values: shape (num_steps + 1, num_envs)  <- 包含了最后一个状态的 V(s_{T})
        dones: shape (num_steps, num_envs)       <- 1.0 表示当前步终止，0.0 表示未终止
    """
    advantages = torch.zeros_like(rewards)
    lastgaelam = 0
    num_steps = rewards.shape[0]

    # TODO: 逆序遍历 0 到 num_steps-1，利用 GAE 迭代公式计算优势函数
    # 提示1: 第 t 步的 next_non_terminal = 1.0 - dones[t]
    # 提示2: TD-error(delta_t) = rewards[t] + gamma * values[t+1] * next_non_terminal - values[t]
    # 提示3: advantages[t] = delta_t + gamma * lam * next_non_terminal * lastgaelam
    # 提示4: 计算完后，记得将当前的 advantages[t] 赋值给 lastgaelam 用于下一步循环
    
    # --- YOUR CODE HERE ---
    for t in range(num_steps-1, -1, -1):
        
        # if dones[t]:
        #     # 已经完成了没有下一个状态了，TD-error直接是实际奖励-预估的
        #     advantages[t] = rewards[t] - values[t]
        # else:
        #     # TD-error是当前实际的reward+下一步的估计值 - 当前估计值
        #     delta_t = rewards[t] + gamma * values[t+1] - values[t]
        #     # GAE的动态规划
        #     advantages[t] = delta_t + gamma * lam * lastgaelam
        
        # lastgaelam = advantages[t]
        next_non_terminal = 1.0 - dones[t]
        delta_t = rewards[t] + gamma * values[t+1] * next_non_terminal - values[t]
        advantages[t] = delta_t + gamma * lam * next_non_terminal * lastgaelam
        lastgaelam = advantages[t]



    # --- END OF YOUR CODE ---

    # Value Target (用于训练 Critic 拟合的基准)
    returns = advantages + values[:-1]
    return advantages, returns


def compute_ppo_clip_loss(log_probs: torch.Tensor, old_log_probs: torch.Tensor, advantages: torch.Tensor, clip_coef: float = 0.2):
    """
    计算 Actor 的截断代理损失函数 (PPO-Clip Loss)
    
    参数:
        log_probs: shape (batch_size,), 新策略的 log \pi(a|s)
        old_log_probs: shape (batch_size,), 旧策略(采样时)的 log \pi_{old}(a|s)
        advantages: shape (batch_size,), 优势函数估计值
    """
    # TODO: 实现 PPO 目标函数
    # 提示1: 重要性采样比率 ratio = exp(log_probs - old_log_probs)
    # 提示2: 未截断的目标 unclipped_surrogate = ratio * advantages
    # 提示3: 截断的目标 clipped_surrogate = torch.clamp(...) * advantages
    # 提示4: 最终代理目标是取两者中的最小值。但因为 PyTorch 优化器默认做**梯度下降**，
    #        而我们要**最大化**代理目标，所以 final_loss 应该是取平均值后再加负号！

    # --- YOUR CODE HERE ---
    ratio = torch.exp(log_probs - old_log_probs)
    unclipped_surrogate = ratio * advantages
    clipped_surrogate = torch.clamp(ratio, 1-clip_coef, 1+clip_coef) * advantages
    loss = torch.min(unclipped_surrogate, clipped_surrogate)
    loss = -loss.mean()
    # --- END OF YOUR CODE ---
    
    return loss