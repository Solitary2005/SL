import numpy as np
from decision_tree import DecisionTree
from collections import Counter

class RandomForest:
    def __init__(self, n_estimators=10, max_depth=10, min_samples_split=2, n_features=None):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.n_features = n_features
        self.trees = []

    def fit(self, X, y):
        self.trees = []
        for _ in range(self.n_estimators):
            # ================================================================ #
            # TODO: 实现森林的构建过程                                           #
            # 1. 对传入的数据进行有放回抽样 (Bootstrap)                           #
            # 2. 实例化一棵 DecisionTree，传入参数                               #
            # 3. 使用抽样后的数据 fit 决策树，并将其添加到 self.trees 列表中       #
            # ================================================================ #
            X_i, y_i = self._bootstrap_samples(X, y)
            tree = DecisionTree(self.min_samples_split, self.max_depth, self.n_features)
            tree.fit(X_i, y_i)
            self.trees.append(tree)
            # ================================================================ #
            # END OF YOUR CODE                                                 #
            # ================================================================ #

    def _bootstrap_samples(self, X, y):
        # ================================================================ #
        # TODO: 实现 Bootstrap 采样逻辑                                     #
        # 提示：使用 np.random.choice                                       #
        # ================================================================ #
        # bootstrap 采样：从原始数据中有放回地随机抽取样本，生成新的训练集
        # 这里我们抽取与原始数据集大小相同的样本数量，但可以有重复的样本
        num_samples = X.shape[0]
        choices = np.random.choice(num_samples, size=num_samples, replace=True)
        X_i = X[choices]
        y_i = y[choices]
        return X_i, y_i
        # ================================================================ #
        # END OF YOUR CODE                                                 #
        # ================================================================ #

    def predict(self, X):
        # 收集森林中所有树的预测结果
        tree_preds = np.array([tree.predict(X) for tree in self.trees])
        
        # 维度变换：[n_trees, n_samples] -> [n_samples, n_trees]
        tree_preds = np.swapaxes(tree_preds, 0, 1)
        
        # ================================================================ #
        # TODO: 实现多数投票机制 (Majority Voting)                          #
        # 对每一个样本的所有树预测结果，找出出现次数最多的类别作为最终预测      #
        # ================================================================ #
        n_samples, n_trees = tree_preds.shape
        select_idxs = []
        for i in range(n_samples):
            sample = {j:tree_preds[i][j] for j in range(n_trees)}
            voting_num = Counter(sample)
            select_idx = voting_num.most_common(1)[0][1]
            select_idxs.append(select_idx)
        return np.array(select_idxs)
        # ================================================================ #
        # END OF YOUR CODE                                                 #
        # ================================================================ #