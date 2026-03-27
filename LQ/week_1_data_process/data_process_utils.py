import pandas as pd
import numpy as np
from typing import Union, List, Dict, Optional, Any

# 可选依赖
try:
    from sklearn.ensemble import RandomForestRegressor
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    from difflib import SequenceMatcher
    DIFLIB_AVAILABLE = True
except ImportError:
    DIFLIB_AVAILABLE = False


def drop_missing_rows(
    df: pd.DataFrame,
    thresh: Optional[int] = None,
    subset: Optional[Union[List[str], str]] = None,
    inplace: bool = False,
) -> Optional[pd.DataFrame]:
    """
    保留的行，在 subset 指定的列中，非空值的数量必须 ≥ thresh, 否则被drop
    """
    if inplace == False:
        df_cleaned = df.copy()
        df_cleaned = df_cleaned.dropna(thresh=thresh, subset=subset)
        return df_cleaned
    else:
        df = df.dropna(thresh=thresh, subset=subset)
        return None


def drop_missing_columns(
    df: pd.DataFrame,
    threshold: float = 0.5,
    inplace: bool = False,
) -> Optional[pd.DataFrame]:
    """
    删除缺失率 >= threshold 的列
    """
    na = df.isnull().mean()
    na = na[na >= threshold].index.tolist()
    if inplace == False:
        return df.drop(columns=na, inplace=inplace)
    else:
        df = df.drop(columns=na, inplace=inplace)
        return None



def fill_missing_with_stat(
    df: pd.DataFrame,
    strategy: str = "median",
    columns: Optional[Union[List[str], str]] = None,
    constant: Any = "Missing",
    inplace: bool = False,
) -> Optional[pd.DataFrame]:
    """
    [引导]
    1. 确定需要处理的列（如果是 None，则是所有列）。
    2. 遍历列，根据 strategy ("mean", "median", "mode", "constant") 计算填充值。
       注意："mode" 可能会返回多个值，取第一个即可，若为空则设为 np.nan。
    3. 使用 fillna 进行填充。
    """
    if columns == None:
        columns = df.columns
    for col in columns:
        if strategy == "mean":
            fill_val = df[col].mean()
        elif strategy == "median":
            fill_val = df[col].median()
        elif strategy == "mode":
            fill_val = df[col].mode()
        elif strategy == "constant":
            fill_val = constant
        if inplace:
            df.fillna(fill_val, inplace=inplace)
            return None
        else:
            df.fillna(fill_val, inplace=inplace)
        


def fill_missing_ffill(
    df: pd.DataFrame,
    columns: Optional[Union[List[str], str]] = None,
    inplace: bool = False,
) -> Optional[pd.DataFrame]:
    """
    [引导] 使用 ffill (forward fill) 填充。
    提示：df[cols].ffill() 或者 fillna(method="ffill")。
    """
    # TODO: 在此补充实现
    raise NotImplementedError("等待实现")


def fill_missing_bfill(
    df: pd.DataFrame,
    columns: Optional[Union[List[str], str]] = None,
    inplace: bool = False,
) -> Optional[pd.DataFrame]:
    """
    [引导] 使用 bfill (backward fill) 填充。
    """
    # TODO: 在此补充实现
    raise NotImplementedError("等待实现")


def interpolate_missing(
    df: pd.DataFrame,
    method: str = "linear",
    columns: Optional[Union[List[str], str]] = None,
    inplace: bool = False,
) -> Optional[pd.DataFrame]:
    """
    [引导] 使用 df.interpolate() 方法进行插值。
    """
    # TODO: 在此补充实现
    raise NotImplementedError("等待实现")


def fill_missing_with_model(
    df: pd.DataFrame,
    target_col: str,
    feature_cols: Union[List[str], str],
    model=None,
    test_size: float = 0.2, # 此参数在实际全量填充时可以忽略或用于评估
    random_state: int = 42,
    inplace: bool = False,
) -> Optional[pd.DataFrame]:
    """
    [引导] 
    1. 检查特征列是否有缺失值，有则抛出 ValueError。
    2. 把 target_col 非空的行作为训练集 (X_train, y_train)。
    3. 把 target_col 为空的行作为预测集 (X_test)。
    4. 如果没有提供 model，默认初始化一个 RandomForestRegressor。
    5. 用模型训练并预测，将结果填回 df。
    """
    # TODO: 在此补充实现
    raise NotImplementedError("等待实现")


def add_missing_indicator(
    df: pd.DataFrame,
    columns: Optional[Union[List[str], str]] = None,
    suffix: str = "_missing",
    inplace: bool = False,
) -> Optional[pd.DataFrame]:
    """
    [引导] 
    1. 遍历指定的列。
    2. 创建新列（原列名+suffix），如果原列此处是空值，新列为 1，否则为 0。
    """
    # TODO: 在此补充实现
    raise NotImplementedError("等待实现")


def drop_duplicates_exact(
    df: pd.DataFrame,
    subset: Optional[Union[List[str], str]] = None,
    keep: str = "first",
    inplace: bool = False,
) -> Optional[pd.DataFrame]:
    """
    [引导] 直接调用 pandas 的 drop_duplicates。
    """
    # TODO: 在此补充实现
    raise NotImplementedError("等待实现")


def deduplicate_fuzzy(
    df: pd.DataFrame,
    column: str,
    threshold: float = 0.8,
    method: str = "levenshtein",
    keep: str = "first",
    inplace: bool = False,
) -> Optional[pd.DataFrame]:
    """
    [引导-进阶挑战] 
    1. 提取指定列的文本列表。
    2. 双重循环对比字符串相似度 (SequenceMatcher(None, a, b).ratio())。
    3. 记录需要删除的索引。注意根据 keep ('first'/'last'/False) 逻辑判断到底删哪个。
    4. 使用 df.drop(index=...) 删除行。
    """
    # TODO: 在此补充实现
    raise NotImplementedError("等待实现")


def aggregate_duplicates(
    df: pd.DataFrame,
    group_by: Union[List[str], str],
    agg_dict: Dict[str, Union[str, List[str]]],
    inplace: bool = False,
) -> Optional[pd.DataFrame]:
    """
    [引导] 
    1. 使用 groupby + agg。
    2. 难点在于 inplace=True 时如何修改原 DataFrame。
       (提示：可以在清空原 df 后把聚合结果赋给它，或者更新它)。
    """
    # TODO: 在此补充实现
    raise NotImplementedError("等待实现")