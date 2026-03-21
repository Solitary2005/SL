# core/policy.py
import torch
import torch.nn as nn

class DiffusionPolicy(nn.Module):
    def __init__(self, network, noise_scheduler):
        super().__init__()
        self.network = network  # 你的噪声预测网络 (U-Net, 1D CNN 或 Transformer)
        self.noise_scheduler = noise_scheduler
        
    def compute_loss(self, clean_actions, obs_cond):
        """
        计算训练 Loss。
        输入:
            clean_actions: (B, Pred_Horizon, Action_Dim) 真实动作块
            obs_cond: (B, Obs_Horizon, Obs_Dim) 视觉/本体感觉的条件特征
        """
        B = clean_actions.shape[0]
        device = clean_actions.device
        
        # 1. 为每个样本随机采样 timestep t
        timesteps = torch.randint(
            0, self.noise_scheduler.num_train_timesteps, 
            (B,), device=device
        ).long()
        
        # 2. 生成高斯噪声
        noise = torch.randn_like(clean_actions)
        
        # 3. 将噪声添加到真实动作中 (前向过程)
        noisy_actions = self.noise_scheduler.add_noise(clean_actions, noise, timesteps)
        
        ###########################################################################
        # TODO: 将带噪动作和条件输入网络，预测噪声，并计算 MSE Loss。             #
        # 提示: 你的 self.network 需要接收 (noisy_actions, timesteps, obs_cond)   #
        ###########################################################################
        loss = None
        # ======== 你的代码 ========
        
        # ==========================
        ###########################################################################
        return loss

    @torch.no_grad()
    def conditional_sample(self, obs_cond, pred_horizon, action_dim):
        """
        推理过程：基于观测条件，从纯噪声生成动作序列。
        """
        B = obs_cond.shape[0]
        device = obs_cond.device
        
        # 1. 初始化纯噪声序列 x_T
        action_shape = (B, pred_horizon, action_dim)
        sample = torch.randn(action_shape, device=device)
        
        # 2. 迭代去噪 T -> 0
        self.noise_scheduler.alphas_cumprod = self.noise_scheduler.alphas_cumprod.to(device)
        
        ###########################################################################
        # TODO: 实现反向采样主循环。                                              #
        # 提示: 遍历从 num_train_timesteps-1 到 0 的时间步。                      #
        # 在每一步中: 1. 预测当前噪声; 2. 调用 scheduler.step 更新 sample         #
        ###########################################################################
        # ======== 你的代码 ========
        
        # ==========================
        ###########################################################################
        
        return sample # 返回 x_0