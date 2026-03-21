# core/noise_scheduler.py
import torch
import numpy as np

class DDPMScheduler:
    def __init__(self, num_train_timesteps=100, beta_start=0.0001, beta_end=0.02):
        self.num_train_timesteps = num_train_timesteps
        
        # 线性噪声调度 (Linear Variance Schedule)
        self.betas = torch.linspace(beta_start, beta_end, num_train_timesteps)
        self.alphas = 1.0 - self.betas
        self.alphas_cumprod = torch.cumprod(self.alphas, dim=0)
        
    def add_noise(self, original_samples, noise, timesteps):
        """
        前向加噪过程：根据 timestep t 给原始动作序列加噪。
        
        输入:
            original_samples: shape (B, T_obs, Action_Dim) - 例如 (B, 16, 20) 20指代多指手的自由度
            noise: 与 original_samples shape 相同的纯高斯噪声
            timesteps: shape (B,) - 批次中每个样本对应的 t
        
        返回:
            noisy_samples: 加噪后的样本
        """
        # 提取当前 t 对应的累乘 alpha
        alphas_cumprod_t = self.alphas_cumprod.to(original_samples.device)[timesteps]
        
        # 将 alphas_cumprod_t 调整为与 original_samples 相同的维度以进行广播
        while len(alphas_cumprod_t.shape) < len(original_samples.shape):
            alphas_cumprod_t = alphas_cumprod_t.unsqueeze(-1)
            
        ###########################################################################
        # TODO: 实现 DDPM 前向过程公式:                                           #
        # x_t = sqrt(alpha_bar_t) * x_0 + sqrt(1 - alpha_bar_t) * epsilon         #
        ###########################################################################
        noisy_samples = None 
        # ======== 你的代码 ========
        
        # ==========================
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return noisy_samples

    def step(self, model_output, timestep, sample):
        """
        反向去噪过程（单步）：根据模型预测的噪声，从 x_t 推导 x_{t-1}。
        为简化起见，这里实现最基础的 DDPM step。
        """
        t = timestep
        alpha_t = self.alphas[t].to(sample.device)
        alpha_cumprod_t = self.alphas_cumprod[t].to(sample.device)
        beta_t = self.betas[t].to(sample.device)
        
        ###########################################################################
        # TODO: 实现 DDPM 反向推导公式计算均值 mu:                                #
        # mu = (1 / sqrt(alpha_t)) * (x_t - (beta_t / sqrt(1 - alpha_bar_t)) * epsilon_theta)
        ###########################################################################
        mu = None
        # ======== 你的代码 ========
        
        # ==========================
        ###########################################################################
        
        if t > 0:
            noise = torch.randn_like(sample)
            variance = torch.sqrt(beta_t) * noise
        else:
            variance = 0.0
            
        prev_sample = mu + variance
        return prev_sample