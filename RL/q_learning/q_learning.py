import numpy as np

class QLearningAgent:
    def __init__(self, n_states, n_actions, learning_rate=0.1, discount_factor=0.99, epsilon=0.1):
        """
        初始化 Q-Learning 智能体
        """
        self.n_states = n_states
        self.n_actions = n_actions
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        
        # 初始化 Q-Table 为全 0，形状为 (状态数, 动作数)
        self.q_table = np.zeros((n_states, n_actions))

    def choose_action(self, state):
        """
        使用 Epsilon-Greedy 策略选择动作
        """
        action = 0
        #######################################################################
        # TODO:                                                               #
        # 实现 Epsilon-Greedy 策略。                                          #
        # 以 epsilon 的概率随机选择一个动作 (探索)                            #
        # 以 1 - epsilon 的概率选择当前状态下 Q 值最大的动作 (利用)           #
        # 提示: np.random.uniform(0, 1) 可以生成 0 到 1 之间的随机数          #
        #       self.n_actions 是总动作数                                     #
        #######################################################################
        pass # 请删除 pass 并在此处编写你的代码
        #######################################################################
        #                         END OF YOUR CODE                            #
        #######################################################################
        return action

    def update(self, state, action, reward, next_state):
        """
        更新 Q-Table 中的 Q 值
        """
        #######################################################################
        # TODO:                                                               #
        # 根据 Q-Learning 更新公式更新 self.q_table[state, action]            #
        # 公式: Q(s,a) <- Q(s,a) + lr * [R + gamma * max Q(s',a') - Q(s,a)]   #
        # 注意: 如果 next_state 是终止状态，Q 值如何处理？(通常不需要特殊处     #
        # 理，只要保证环境在 done 时重置即可，但请理解公式中的 max Q(s',a'))  #
        #######################################################################
        pass # 请删除 pass 并在此处编写你的代码
        #######################################################################
        #                         END OF YOUR CODE                            #
        #######################################################################