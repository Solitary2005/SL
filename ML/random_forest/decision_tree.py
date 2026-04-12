import numpy as np
from collections import Counter

class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, *, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value
        
    def is_leaf_node(self):
        return self.value is not None

class DecisionTree:
    def __init__(self, min_samples_split=2, max_depth=100, n_features=None):
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        self.n_features = n_features
        self.root = None

    def fit(self, X, y):
        self.n_features = int(np.sqrt(X.shape[1])) if not self.n_features else min(int(np.sqrt(X.shape[1])), self.n_features)
        self.root = self._grow_tree(X, y)

    def _grow_tree(self, X, y, depth=0):
        n_samples, n_feats = X.shape
        n_labels = len(np.unique(y))

        # 停止条件 (剪枝与叶子节点)
        if (depth >= self.max_depth or n_labels == 1 or n_samples < self.min_samples_split):
            leaf_value = self._most_common_label(y)
            return Node(value=leaf_value)
        
        # 不看所有特征，而是随机挑选 n_features 个特征（通常是总特征数的平方根）
        feat_idxs = np.random.choice(n_feats, self.n_features, replace=False)

        # 寻找最佳分裂点
        best_feature, best_thresh = self._best_split(X, y, feat_idxs)
        
        # 如果找不到有效分裂
        if best_feature is None:
            return Node(value=self._most_common_label(y))

        # 分裂并递归生长
        left_idxs, right_idxs = self._split(X[:, best_feature], best_thresh)

        # 检查分裂是否有效
        if len(left_idxs) == 0 or len(right_idxs) == 0:
            return Node(value=self._most_common_label(y))

        left = self._grow_tree(X[left_idxs, :], y[left_idxs], depth + 1)
        right = self._grow_tree(X[right_idxs, :], y[right_idxs], depth + 1)
        return Node(best_feature, best_thresh, left, right)

    def _best_split(self, X, y, feat_idxs):
        best_gain = -1
        split_idx, split_threshold = None, None

        for feat_idx in feat_idxs:
            X_column = X[:, feat_idx]
            thresholds = np.unique(X_column)

            for thr in thresholds:
                # ================================================================ #
                # TODO: 计算信息增益 (基于基尼系数)                                  #
                # 1. 尝试使用 thr 分裂 X_column                                     #
                # 2. 计算分裂前后的基尼系数增益                                      #
                # 3. 更新 best_gain, split_idx, split_threshold                    #
                # ================================================================ #
                left_idxs = np.argwhere(X_column <= thr).flatten()
                right_idxs = np.argwhere(X_column > thr).flatten()
                y_left, y_right = y[left_idxs], y[right_idxs]
                origin_gini = self._gini(y)

                n = len(y)
                n_l, n_r = len(y_left), len(y_right)
                if n_l == 0 or n_r == 0:
                    # 说明还是原先的划分，没啥区别
                    gain = 0
                else:
                    child_gini = (n_l / n) * self._gini(y_left) + (n_r / n) * self._gini(y_right)
                    # 因为gini是越小越好，所以如果原先的更大(gain>0)，那么应该进行划分
                    # gini相比原先的减小越多越好
                    gain = origin_gini - child_gini

                if gain > best_gain:
                    best_gain = gain
                    split_idx, split_threshold = feat_idx, thr

                # ================================================================ #
                # END OF YOUR CODE                                                 #
                # ================================================================ #

        return split_idx, split_threshold

    def _gini(self, y):
        """计算基尼系数"""
        # ================================================================ #
        # TODO: 实现基尼系数的计算公式
        # Gini = 1 - sum(p_i^2)
        # 基尼指数是CART决策树中用于分类任务的重要评估指标，
        # 它通过衡量数据集的 不纯度 来帮助算法选择最优的特征和切分点进行数据集的分割
        # 当该子树集合只有一种类别的时候，不纯度为0
        # 所以 gini越小 说明 分类越准确
        # ================================================================ #

        # 这个先把每种label出现多少次快速统计出来
        # 然后除以一共有多少个样本
        # 就得到了每个label在样本集中的出现频率
        counts = np.unique(y, return_counts=True)[1]
        prob = counts / len(y)
        return 1 - np.sum(prob ** 2)
    
        # ================================================================ #
        # END OF YOUR CODE                                                 #
        # ================================================================ #

    def _split(self, X_column, split_thresh):
        left_idxs = np.argwhere(X_column <= split_thresh).flatten()
        right_idxs = np.argwhere(X_column > split_thresh).flatten()
        return left_idxs, right_idxs

    def _most_common_label(self, y):
        counter = Counter(y)
        value = counter.most_common(1)[0][0]
        return value

    def predict(self, X):
        return np.array([self._traverse_tree(x, self.root) for x in X])

    def _traverse_tree(self, x, node):
        if node.is_leaf_node():
            return node.value
        if x[node.feature] <= node.threshold:
            return self._traverse_tree(x, node.left)
        return self._traverse_tree(x, node.right)