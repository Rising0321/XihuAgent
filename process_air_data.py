import pandas as pd

# 读取CSV文件
df = pd.read_csv('datas/air_condition.csv')

# 删除第一列（索引列）
df = df.iloc[:, 1:]

# 将date和hour合并为Time列
df['Time'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['hour'].astype(str).str.zfill(2) + ':00:00')

# 删除原来的date和hour列
df = df.drop(['date', 'hour'], axis=1)

# 重新排列列顺序，将Time放在最前面
cols = ['Time'] + [col for col in df.columns if col != 'Time']
df = df[cols]

# 保存处理后的数据
df.to_csv('datas/air_condition_processed.csv', index=False) 