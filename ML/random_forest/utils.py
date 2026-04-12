import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def load_data(filepath):
    """加载并标准化数据"""
    df = pd.read_csv(filepath)
    X = df[['Age', 'EstimatedSalary']].values
    y = df['Purchased'].values
    
    # 简单的标准化 (Z-score)，加速收敛和统一尺度
    X = (X - X.mean(axis=0)) / X.std(axis=0)
    return X, y

def rel_error(x, y):
    """返回相对误差，用于标答比对"""
    return np.max(np.abs(x - y) / (np.maximum(1e-8, np.abs(x) + np.abs(y))))

def plot_decision_boundary(X, y, model, title="Decision Boundary"):
    """绘制分类决策边界"""
    h = .02  # 网格步长
    cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA'])
    cmap_bold = ListedColormap(['#FF0000', '#00FF00'])

    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, cmap=cmap_light, alpha=0.8)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold, edgecolor='k', s=20)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.title(title)
    plt.xlabel("Age (Standardized)")
    plt.ylabel("Estimated Salary (Standardized)")
    plt.show()