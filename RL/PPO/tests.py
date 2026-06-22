# tests.py
import torch

def rel_error(x, y, eps=1e-8):
    """CS231n 风格的 Tensor 相对误差计算器"""
    x = x.to(torch.float32)
    y = y.to(torch.float32)
    return torch.max(torch.abs(x - y) / (torch.maximum(torch.abs(x) + torch.abs(y), torch.tensor(eps)))).item()

def check_gae():
    print("--- Testing GAE Implementation ---")
    # 模拟一个 seq_len=3, num_envs=1 的环境轨迹
    rewards = torch.tensor([[1.0], [0.5], [2.0]])
    values = torch.tensor([[0.5], [0.8], [1.2], [0.0]]) # len = seq_len + 1 (包含了 bootstrap value)
    dones = torch.tensor([[0.0], [0.0], [1.0]])
    
    # 真实闭式解推导值 (gamma=0.9, lam=0.8)
    expected_adv = torch.tensor([[2.19632], [1.35600], [0.80000]])
    expected_ret = expected_adv + values[:-1]
    
    from ppo_core import compute_gae_advantages
    adv, ret = compute_gae_advantages(rewards, values, dones, gamma=0.9, lam=0.8)
    
    err_adv = rel_error(adv, expected_adv)
    err_ret = rel_error(ret, expected_ret)
    
    if err_adv < 1e-4 and err_ret < 1e-4:
        print(f"✅ [PASSED] GAE Advantages & Returns (Max rel_error: {max(err_adv, err_ret):.4e})")
    else:
        print(f"❌ [FAILED] GAE Computation.")
        print(f"  Your Adv:\n{adv}\n  Expected Adv:\n{expected_adv}")

def check_ppo_loss():
    print("\n--- Testing PPO Clipped Loss ---")
    # 模拟重要性采样
    adv = torch.tensor([1.0, -1.0, 2.0])
    old_logp = torch.tensor([-1.0, -1.0, -1.0])
    new_logp = old_logp + torch.log(torch.tensor([1.5, 0.7, 0.9])) # 这使得 ratio 等于 [1.5, 0.7, 0.9]
    
    # 预期 loss: 当 clip_coef=0.2 时，第三个样本不被 clip，第一个样本触发 clip。推导结果应为 -0.7333333
    expected_loss = torch.tensor(-0.7333333)
    
    from ppo_core import compute_ppo_clip_loss
    loss = compute_ppo_clip_loss(new_logp, old_logp, adv, clip_coef=0.2)
    err = rel_error(loss, expected_loss)
    
    if err < 1e-4:
        print(f"✅ [PASSED] PPO Clipped Loss (rel_error: {err:.4e})")
    else:
        print(f"❌ [FAILED] PPO Loss. Got {loss.item():.5f}, Expected {expected_loss.item():.5f}")