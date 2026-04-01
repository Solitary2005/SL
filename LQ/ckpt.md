补充到 unkown
快速搭建一个k-折交叉验证
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
pipeline = make_pipeline(
    TfidfVectorizer(max_features=5000, ngram_range=(1,2), max_df=0.8, min_df=3),
    LinearSVC(C=0.0000001, class_weight='balanced')
)
scores = cross_val_score(pipeline, train_text, label, cv=5)
print("CV accuracy: {:.4f}".format(scores.mean()))

关于常用的分类模型
LinearSVC：适用于较大规模，高维稀疏特征的数据（比如文本分类）
对于类别不平衡的数据可设置class_weight='balanced'