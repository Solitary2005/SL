# flow_core.py
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.distributions as D
import math

def create_sinusoidal_pos_embedding(time, dimension, min_period=4e-3, max_period=4.0):
    """
    Computes sine-cosine positional embedding vectors for scalar positions.
    将标量时间time映射到高维向量空间
    time: (B, )
    频率周期的范围为[min_period, max_period]
    return (B, dim)
    """
    half_dim = dimension // 2
    device = time.device
    # 基于 pi0 实现的逻辑
    # Step0: 频率计算
    # 线性插值
    fraction = torch.linspace(0.0, 1.0, half_dim, dtype=torch.float32, device=device)
    # 对数插值
    period = min_period * (max_period / min_period) ** fraction
    scaling_factor = 1.0 / period * 2 * math.pi # f = 1/period * 2pi 角频率 (half_dim, )
    # Step1: 计算输入pos (B, hald_dim)
    sin_input = scaling_factor[None, :] * time[:, None]
    # print(f"DEBUG: {sin_input.shape}")
    return torch.cat([torch.sin(sin_input), torch.cos(sin_input)], dim=-1)

def sample_beta(alpha, beta, bsize, device):
    torch.manual_seed(0) 
    alpha_t = torch.as_tensor(alpha, dtype=torch.float32, device=device)
    beta_t = torch.as_tensor(beta, dtype=torch.float32, device=device)
    dist = torch.distributions.Beta(alpha_t, beta_t)
    return dist.sample((bsize,))

class Pi0ActionExpert(nn.Module):
    def __init__(self, action_dim=20, horizon=16, cond_dim=128, hidden_dim=256):
        super().__init__()
        self.action_dim = action_dim
        self.horizon = horizon
        self.time_dim = hidden_dim
        
        # 动作投影
        self.action_in_proj = nn.Linear(action_dim, hidden_dim)
        self.action_out_proj = nn.Linear(hidden_dim, action_dim)
        
        # 时间 MLP
        self.time_mlp = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )
        
        # 简化的 Transformer 或 MLP 骨架，用于处理 [B, H, hidden_dim]
        self.net = nn.Sequential(
            nn.Linear(hidden_dim*2 + cond_dim, hidden_dim * 2),
            nn.SiLU(),
            nn.Linear(hidden_dim * 2, hidden_dim)
        )

    def forward(self, x_t, cond, t):
        """
        x_t: [B, H, action_dim]
        cond: [B, cond_dim]
        t: [B]
        """
        B, H, _ = x_t.shape
        
        # 1. 时间嵌入
        t_raw_emb = create_sinusoidal_pos_embedding(t, self.time_dim)
        t_emb = self.time_mlp(t_raw_emb) # [B, hidden_dim]
        
        # 2. 动作映射到隐空间
        act_emb = self.action_in_proj(x_t) # [B, H, hidden_dim]
        
        # 3. 融合条件特征
        # 将 cond 和 t_emb 广播并拼接到序列的每一帧
        # print(f"t: {t_emb.shape}")
        # print(f"cond: {cond.shape}")
        cond_t = torch.cat([cond, t_emb], dim=-1) # [B, cond_dim + hidden_dim]
        cond_t_expanded = cond_t.unsqueeze(1).expand(-1, H, -1)
        
        feat = torch.cat([act_emb, cond_t_expanded], dim=-1) # [B, H, hidden_dim*2 + cond_dim]
        
        # 4. 预测向量场 v_t
        h = self.net(feat)
        return self.action_out_proj(h) # [B, H, action_dim]

# ================= 学生实操部分 =================

def sample_time(bsize, device):
    """
    TODO: 实现重要性采样。
    Beta(1.5, 1.0) 的形状：α=1.5，β=1.0：
    由于 α>β，分布的概率密度在 x 接近 0 时较高，呈现右偏的形状。
    要求：使用 Beta(1.5, 1.0) 采样，并缩放到 [0.001, 1.0] 之间。
    """
    # ================================================================ #
    # YOUR CODE HERE
    time = None 

    beta = sample_beta(1.5, 1.0, bsize, device) # 范围在[0,1]
    time = beta * 0.999 + 0.001
    # ================================================================ #
    return time.to(dtype=torch.float32, device=device)

def sample_noise(shape, device):
    """
    TODO: 采样噪声 eps ~ N(0, 1), 形状与 actions 一致
    """
    # ================================================================ #
    # YOUR CODE HERE
    noise = None 
    torch.manual_seed(0) 
    noise = torch.normal(
        mean=0.0,
        std=1.0,
        size=shape,
        device=device,
        dtype=torch.float32
    )
    # ================================================================ #
    return noise

def compute_flow_matching_loss(model:Pi0ActionExpert, actions, cond):
    """
    actions: [B, H, action_dim]
    cond: [B, cond_dim]
    """
    B, H, D_act = actions.shape
    device = actions.device
    
    # ================================================================ #
    # TODO 1: 采样噪声 eps ~ N(0, 1), 形状与 actions 一致
    # TODO 2: 使用 sample_time 采样时间步 t [B]
    # TODO 3: 实现 pi0 的插值策略 (Optimal Transport)
    # 提示：x_t = t * eps + (1 - t) * actions
    # 注意维度广播：t 需要变为 [B, 1, 1]
    # TODO 4: 计算回归目标 u_t (即导数 dx_t/dt)
    # TODO 5: 前向计算模型预测 v_t
    # TODO 6: 计算 MSE Loss
    # ================================================================ #
    loss = None

    noise = sample_noise((B, H, D_act), device)
    time_step = sample_time(B, device)
    t_expend = time_step.unsqueeze(1).unsqueeze(1)
    x_t = t_expend * noise + (1 - t_expend) * actions
    u_t = noise - actions
    v_t = model(x_t, cond, time_step)
    loss_fc = nn.MSELoss()
    loss = loss_fc(u_t, v_t)
    
    # ================================================================ #
    return loss

@torch.no_grad()
def sample_actions(model, cond, action_dim, horizon, num_steps=10):
    device = cond.device
    bsize = cond.shape[0]
    
    # ================================================================ #
    # TODO 7: 初始化 x_t 为纯噪声 (t=1.0)
    # TODO 8: 设置步长 dt = -1.0 / num_steps (从 1.0 迭代到 0.0)
    # TODO 9: 实现 Euler 步进
    # while time >= -dt / 2:
    #   v_t = model(x_t, cond, t)
    #   x_t = x_t + dt * v_t
    # ================================================================ #
    x_t = None

    x_t = sample_noise((bsize, horizon, action_dim), device)
    dt = -1.0 / num_steps
    t = torch.ones((bsize,))
    time = 1.0
    while time >= -dt / 2:
        v_t = model(x_t, cond, t)
        x_t = x_t + dt * v_t
        time += dt
        t += dt
    # ================================================================ #
    return x_t