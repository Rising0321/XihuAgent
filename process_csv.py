import pandas as pd
import os

def process_csv(file_path):
    try:
        # 读取CSV文件
        df = pd.read_csv(file_path)
        
        # 打印列名
        print(f"\n{file_path} 的列名:")
        print(df.columns.tolist())
        
        # 检查是否存在Time列（大小写都检查）
        time_column = None
        if 'Time' in df.columns:
            time_column = 'Time'
        elif 'time' in df.columns:
            time_column = 'time'
        else:
            print(f"警告: {file_path} 中没有找到Time列，跳过处理")
            return
        
        # 按Time列从大到小排序
        df = df.sort_values(by=time_column, ascending=False)
        
        # 保存回原文件
        df.to_csv(file_path, index=False)
        print(f"处理完成: {file_path}")
    except Exception as e:
        print(f"处理 {file_path} 时出错: {str(e)}")

# 获取datas目录下的所有CSV文件
datas_dir = 'datas'
csv_files = [os.path.join(datas_dir, f) for f in os.listdir(datas_dir) if f.endswith('.csv')]

# 处理所有文件
for file in csv_files:
    print(f"\n正在处理: {file}")
    process_csv(file) 