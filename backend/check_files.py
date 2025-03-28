import pandas as pd

files = [
    '../datas/3-water_level.csv',
    '../datas/xihu_city_delay_index_2.csv',
    '../datas/xihu_road_delay_index_2.csv'
]

for file in files:
    print(f"\n查看文件: {file}")
    df = pd.read_csv(file)
    print("列名:", df.columns.tolist())
    print("前几行数据:")
    print(df.head()) 