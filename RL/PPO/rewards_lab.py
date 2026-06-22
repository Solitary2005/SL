import torch

# =========================================================================
# 探究实验一：为什么简单的欧氏距离惩罚（-dist）在 RL 中往往效果很差？
# =========================================================================
def compute_reaching_reward(tcp_pos: torch.Tensor, cube_pos: torch.Tensor) -> torch.Tensor:
    """
    平滑版 Reaching：移除悬崖，让 Critic 轻松拟合
    """
    # 建议先去掉 z 轴的 offset，直接让机械臂对准方块中心。
    # 这样可以避免夹爪外壳直接撞击方块顶部导致无法闭合。
    pre_grasp_pos = cube_pos 
    
    dist = torch.norm(tcp_pos - pre_grasp_pos, dim=1)
    
    # 使用 tanh 保持平滑映射，0 距离时 reward 为 1
    alpha = 4.0
    reaching_reward = 1.0 - torch.tanh(alpha * dist)
    
    # ❌ 删除了 dropped_mask 暴力置零的逻辑
    # 我们将“掉落”的判断交接给环境的 done 信号
    
    return reaching_reward


# =========================================================================
# 探究实验二：局部最优陷阱 —— “贴贴”而不“抓取”
# =========================================================================
def compute_grasping_bonus(is_grasped: torch.Tensor, is_touching: torch.Tensor) -> torch.Tensor:
    """
    微小引导版 Grasping：给 Policy 一点甜头，但不至于让 Critic 崩溃
    """
    bonus = torch.zeros_like(is_grasped, dtype=torch.float32)
    
    bonus[is_touching] += 0.1
    bonus[is_grasped] += 0.5
    
    return bonus


# =========================================================================
# 探究实验三：维持状态的代价与“遗忘灾难”
# =========================================================================
def compute_lifting_reward(cube_pos: torch.Tensor, goal_pos: torch.Tensor, is_grasped: torch.Tensor) -> torch.Tensor:
    """
    [思考引导 3]：
    现象：加上前两步后，机械臂成功抓住了方块！但当它试图向目标点（上方）移动时，往往刚提起来
         一点点，夹爪就松开了，方块掉落。
    原因：向上举起方块时，由于重力和关节阻力，Actor 需要持续输出克服重力的 action_torque。
         如果“靠近目标”带来的奖励增量，抵消不了“持续发力”带来的动作惩罚（Action Penalty）
         或不确定性，Policy 就会选择松手。
    问题：如何设计奖励，使得“带着方块移动”的收益，呈指数级大于“空手移动”？
    
    TODO：设计一个组合条件。只有在 `is_grasped` 为 True 时，才计算方块与目标点的距离奖励。
    """
    dist_to_goal = torch.norm(cube_pos - goal_pos, dim=1)
    lift_reward = torch.zeros_like(dist_to_goal)
   
    # --- YOUR CODE HERE ---
    # 提示：只在 is_grasped 的 mask 下，计算类似 1 - tanh(dist) 的收益，并给予较大的乘数权重
    alpha = 1.0
    lift_reward = (1.0 - torch.tanh(alpha * dist_to_goal)) * is_grasped
    
    # --- END OF YOUR CODE ---
    return lift_reward

def compute_table_penalty(tcp_pos: torch.Tensor) -> torch.Tensor:
    """
    [Sim2Real 安全协议]：桌面防撞护盾
    桌面高度位于 z = 0。方块的中心在 z = 0.02。
    如果机械臂末端（TCP）的 z 坐标低于 0.015，说明它正在用极大的力量按压桌面。
    """
    z_height = tcp_pos[:, 2]  # 提取所有并行环境的 TCP 高度
    safe_margin = 0.01       # 危险红线设定在 1 厘米
    
    # 计算侵入深度：只有当 z_height < safe_margin 时，差值才大于 0
    # 使用 torch.clamp 截断，保证在安全高度以上时惩罚为 0
    violation_depth = torch.clamp(safe_margin - z_height, min=0.0)
    
    # 侵入越深，惩罚呈现指数级爆炸 (防止它宁愿扣分也要往下钻)
    # 返回负数作为惩罚
    penalty = - (violation_depth * 100.0) ** 2 
    
    return penalty

# def compute_action_penalty(actions: torch.Tensor) -> torch.Tensor:
#     """
#     [Sim2Real 安全协议]：动作能量消耗惩罚 (柔顺控制)
#     惩罚 Policy 输出的过大动作幅度，隐式防止自碰撞与高频抽搐。
#     """
#     # 计算动作向量的 L2 范数（模长）
#     action_magnitude = torch.norm(actions, dim=1)
    
#     # 返回负数，动作越猛，扣分越狠
#     return -action_magnitude

def compute_joint_limit_penalty(qpos: torch.Tensor, q_mid: torch.Tensor, q_range: torch.Tensor, danger_margin: float = 0.9) -> torch.Tensor:
    """
    [Sim2Real 安全协议]：关节角度软超限力场 (Soft Joint Limit Shield)
    
    参数:
        qpos: [num_envs, 7] 当前并行的所有机械臂前7个关节角度
        q_mid: [7] 每个关节的物理中点
        q_range: [7] 每个关节由中点向外的单侧最大活动半径
    """
    # 1. 归一化到 [-1.0, 1.0] 区间（0代表该关节正处在最舒服的中间位姿）
    norm_q = (qpos - q_mid) / q_range
    
    # 2. 计算侵入危险区（外侧10%红线）的深度
    # 取绝对值后，只有超过 danger_margin (如0.9) 的部分减去 0.9 才会大于 0
    violation = torch.clamp(torch.abs(norm_q) - danger_margin, min=0.0)
    
    # 3. 溢出量二次方爆炸求和，作为惩罚返回（前面带负号）
    # 越逼近 1.0 的死锁点，往回弹的惩罚梯度越陡峭
    penalty = - torch.sum(violation ** 2, dim=1)
    
    return penalty


# =========================================================================
# 组装线：根据训练日志的反馈，随时在这里调节权重 (Weights Ablation)
# =========================================================================


def compute_carrot_tracking_reward(tcp_pos: torch.Tensor, cube_pos: torch.Tensor, goal_pos: torch.Tensor, 
                                   is_grasped: torch.Tensor, is_touching: torch.Tensor) -> torch.Tensor:
    """
    动态胡萝卜追踪器 (The Drifting Carrot Engine)
    """
    # 1. 设定悬停预备点 (方块正上方 2cm)
    hover_pos = cube_pos + torch.tensor([0.0, 0.0, 0.04], device=tcp_pos.device)
    
    # 2. 游标逻辑分流（核心语句，全 GPU 张量操作）
    # 默认目标是 2cm 悬停点
    target_pos = hover_pos 
    
    should_aim_center = (torch.norm(tcp_pos - hover_pos, dim=1) < 0.005) | is_touching
    target_pos = torch.where(should_aim_center.unsqueeze(1), cube_pos, target_pos)
    
    # 条件B：如果夹爪合拢抓紧了 -> 胡萝卜瞬间瞬移到头顶的目标点！
    target_pos = torch.where(is_grasped.unsqueeze(1), goal_pos, target_pos)

    # 3. 终极计算：全网只算 TCP 距离 target_pos 有多远
    dist_to_carrot = torch.norm(tcp_pos - target_pos, dim=1)
    
    alpha = 4.0
    tracking_reward = 1.0 - torch.tanh(alpha * dist_to_carrot)
    
    return tracking_reward

def get_total_reward(tcp_pos, cube_pos, goal_pos, is_grasped, is_touching, qpos, q_mid, q_range):
    
    w_tracking = 3.0  
    w_grasp_bonus = 1.0 
    
    # 给予超限惩罚极高的权重！因为在90%安全区内它输出的是0，一旦触发说明快折断了，必须一票否决
    w_joint_limit = 2.0 

    r_track = compute_carrot_tracking_reward(tcp_pos, cube_pos, goal_pos, is_grasped, is_touching)
    r_grasp = compute_grasping_bonus(is_grasped, is_touching) 
    
    # 调用新函数
    r_joint_pen = compute_joint_limit_penalty(qpos, q_mid, q_range)
    
    total_reward = (w_tracking * r_track) + (w_grasp_bonus * r_grasp) + (w_joint_limit * r_joint_pen)

    reward_info = {
        "r_track": r_track,
        "r_grasp": r_grasp,
        "r_action_pen": r_joint_pen  # 日志名字顺便改掉
    }

    return total_reward, reward_info

# def get_total_reward(tcp_pos, cube_pos, goal_pos, is_grasped, is_touching, actions):
#     # 权重设计原则：阶段越靠后，天花板越高
#     w_reach = 1.0   # 阶段一：最高拿到 1.0
#     w_grasp = 1.0   # 阶段二：最高拿到 0.15 (来自 bonus 内部)
#     w_lift = 3.0    # 阶段三：一旦抓紧并抬起，最高能拿到 3.0，形成巨大诱惑
    
#     # 安全协议暂时全部关闭，直到你能稳定抓起方块
#     w_table_collision = 0.0  # 🛑 核心雷区，先关闭！ 
#     w_action_penalty = 0.0  # 保留极微小的动作惩罚，防止疯狂抽搐即可
    
#     r_reach = compute_reaching_reward(tcp_pos, cube_pos)
#     r_grasp = compute_grasping_bonus(is_grasped, is_touching)
#     r_lift = compute_lifting_reward(cube_pos, goal_pos, is_grasped)
#     r_table_pen = compute_table_penalty(tcp_pos)
#     r_action_pen = compute_action_penalty(actions)
    
#     total_reward = (w_reach * r_reach + 
#                     w_grasp * r_grasp + 
#                     w_lift * r_lift + 
#                     w_table_collision * r_table_pen + 
#                     w_action_penalty * r_action_pen)
    
#     reward_info = {
#         "r_reach": r_reach,
#         "r_grasp": r_grasp,
#         "r_lift": r_lift,
#         "r_table_pen": r_table_pen,    # 加入追踪
#         "r_action_pen": r_action_pen   # 加入追踪
#     }

#     return total_reward, reward_info