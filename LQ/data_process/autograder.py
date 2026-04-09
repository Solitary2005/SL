# autograder.py
import numpy as np
import pandas as pd

def check_missing_and_duplicates(df_clean):
    if df_clean.isnull().sum().sum() == 0 and df_clean.duplicated().sum() == 0:
        print("✅ 缺失值与重复值处理通过！")
    else:
        print("❌ 检查未通过，数据中仍包含缺失值或重复值。")

def check_outliers(df_original, df_cleaned):
    if len(df_cleaned) < len(df_original):
        print(f"✅ 异常值过滤通过！原数据量: {len(df_original)}, 清洗后数据量: {len(df_cleaned)}")
    else:
        print("❌ 检查未通过，未发现被剔除的异常值（或者剔除逻辑有误）。")

def check_scaling(scaled_data, method='zscore'):
    if method == 'zscore':
        mean_err = np.max(np.abs(np.mean(scaled_data, axis=0)))
        std_err = np.max(np.abs(np.std(scaled_data, axis=0) - 1.0))
        if mean_err < 1e-7 and std_err < 1e-7:
            print("✅ Z-Score 标准化结果正确！")
        else:
            print(f"❌ Z-Score 失败: 均值误差 {mean_err:.4f}, 标准差误差 {std_err:.4f}")
    elif method == 'minmax':
        min_val = np.min(scaled_data, axis=0)
        max_val = np.max(scaled_data, axis=0)
        if np.allclose(min_val, 0) and np.allclose(max_val, 1):
            print("✅ Min-Max 归一化结果正确！")
        else:
            print("❌ Min-Max 失败，特征范围未严格缩放至 [0, 1]。")

def check_pca(pca_data, expected_dim):
    if pca_data.shape[1] == expected_dim:
        print(f"✅ PCA 降维通过！数据已降至 {expected_dim} 维。")
    else:
        print(f"❌ PCA 失败，期望维度 {expected_dim}，实际维度 {pca_data.shape[1]}")

def check_text_pipeline(tfidf_matrix, vocab):
    if tfidf_matrix.shape[0] == 2 and len(vocab) > 0:
        print(f"✅ 文本清理、分词与 TF-IDF 提取通过！共提取到 {len(vocab)} 个特征词。")
        print("特征词表示例:", list(vocab.keys())[:5])
    else:
        print("❌ 文本处理管线失败，请检查去噪、分词或 TF-IDF 向量化步骤。")

def check_image_pipeline(img):
    if img is not None and img.shape == (224, 224, 3):
        print("✅ 图像尺寸统一及颜色空间转换处理通过！(Shape: 224x224x3)")
    else:
        shape = img.shape if img is not None else "None"
        print(f"❌ 图像处理失败，期望 shape: (224, 224, 3)，实际 shape: {shape}")