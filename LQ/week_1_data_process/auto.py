import unittest
import pandas as pd
import numpy as np

# 导入你写的模块
from data_process_utils import *

class TestDataCleaning(unittest.TestCase):

    def setUp(self):
        # 每次测试前生成一个标准测试数据
        self.df = pd.DataFrame({
            'A': [1, 2, np.nan, 4, 1],
            'B': [np.nan, 2.5, 3.5, np.nan, np.nan], # 缺失率 60%
            'C': ['apple', 'banana', 'apple', 'orange', 'apple'], # 'apple'重复
            'D': [10, 20, 30, 40, 10]
        })

    def test_drop_missing_rows(self):
        # 测试返回新对象
        df_out = drop_missing_rows(self.df, subset=['A'])
        self.assertEqual(len(df_out), 4)
        self.assertFalse(self.df['A'].isnull().sum() == 0) # 原对象不变

        # 测试 inplace
        df_copy = self.df.copy()
        res = drop_missing_rows(df_copy, subset=['A'], inplace=True)
        self.assertIsNone(res)
        self.assertEqual(len(df_copy), 4)

    def test_drop_missing_columns(self):
        df_out = drop_missing_columns(self.df, threshold=0.5)
        self.assertNotIn('B', df_out.columns)
        self.assertIn('A', df_out.columns)

    def test_fill_missing_with_stat(self):
        # 测试均值
        df_out = fill_missing_with_stat(self.df, strategy='mean', columns=['A'])
        self.assertEqual(df_out['A'].iloc[2], 2.0) # (1+2+4+1)/4 = 2.0

        # 测试常量
        df_out2 = fill_missing_with_stat(self.df, strategy='constant', columns=['B'], constant=99)
        self.assertEqual(df_out2['B'].iloc[0], 99)

    def test_fill_missing_ffill_bfill(self):
        # Ffill
        df_f = fill_missing_ffill(self.df, columns=['A'])
        self.assertEqual(df_f['A'].iloc[2], 2.0) # 前一个是2

        # Bfill
        df_b = fill_missing_bfill(self.df, columns=['B'])
        self.assertEqual(df_b['B'].iloc[0], 2.5) # 后一个是2.5

    def test_add_missing_indicator(self):
        df_out = add_missing_indicator(self.df, columns=['A'])
        self.assertIn('A_missing', df_out.columns)
        self.assertEqual(df_out['A_missing'].iloc[2], 1)
        self.assertEqual(df_out['A_missing'].iloc[0], 0)

    def test_drop_duplicates_exact(self):
        df_out = drop_duplicates_exact(self.df, subset=['A', 'C'], keep='first')
        self.assertEqual(len(df_out), 4) # 第1行和第5行在A和C上完全相同

    @unittest.skipIf(not DIFLIB_AVAILABLE, "difflib not available")
    def test_deduplicate_fuzzy(self):
        df_fuzzy = pd.DataFrame({'text': ['apple', 'appl', 'banana', 'bananna', 'cat']})
        # apple 和 appl 相似度 0.88，banana 和 bananna 相似度 0.92
        df_out = deduplicate_fuzzy(df_fuzzy, column='text', threshold=0.8, keep='first')
        self.assertEqual(len(df_out), 3)
        self.assertIn('apple', df_out['text'].values)
        self.assertNotIn('appl', df_out['text'].values)

    @unittest.skipIf(not SKLEARN_AVAILABLE, "sklearn not available")
    def test_fill_missing_with_model(self):
        df_model = pd.DataFrame({
            'feat': [1, 2, 3, 4, 5],
            'target': [2, 4, np.nan, 8, 10]
        })
        df_out = fill_missing_with_model(df_model, target_col='target', feature_cols=['feat'])
        # 简单线性关系，RF预测可能不是完美6，但应该不为空
        self.assertFalse(np.isnan(df_out['target'].iloc[2]))

    def test_aggregate_duplicates(self):
        df_agg = pd.DataFrame({
            'id': [1, 1, 2],
            'val': [10, 20, 30]
        })
        df_out = aggregate_duplicates(df_agg, group_by=['id'], agg_dict={'val': 'mean'})
        self.assertEqual(len(df_out), 2)
        self.assertEqual(df_out.loc[df_out['id']==1, 'val'].values[0], 15)

if __name__ == '__main__':
    unittest.main(verbosity=2)