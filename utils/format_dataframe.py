import pandas as pd
from tabulate import tabulate


def convert_float_to_int(df):
    # 遍历DataFrame中的每一列
    for column in df.columns:
        # 检查列的数据类型是否为浮点数
        if pd.api.types.is_float_dtype(df[column]):
            df[column] = df[column].fillna(0.0)
            # 检查该列中的所有值是否都是整数（小数位为0）
            if (df[column] == df[column].astype(int)).all():
                # 将该列转换为整数类型
                df[column] = df[column].astype(int)
    return df

def df_format(df, max_row=5, max_column=4):

    if isinstance(df, pd.DataFrame):  
        df = convert_float_to_int(df)
        if df.shape[0] > max_row:
            if df.shape[1] > max_column:
                return tabulate(df.iloc[:max_row, :max_column], headers="keys", tablefmt='github',  showindex=False, floatfmt=".3f") + f"\n结果超过{max_row}行，{max_column}列，暂不展示"
            else:
                return tabulate(df.iloc[:max_row, :], headers="keys", tablefmt='github', showindex=False, floatfmt=".3f") + f"\n结果超过{max_row}行，暂不展示"
        else:
            if df.shape[1] > max_column:
                return tabulate(df.iloc[:, :max_column], headers="keys", tablefmt='github', showindex=False, floatfmt=".3f") + f"\n结果超过{max_column}列，暂不展示"
            else:
                return tabulate(df, headers="keys", tablefmt='github', showindex=False, floatfmt=".3f")    
    else:
        raise Exception("var `df` is not a  pd.DataFrame")