import pandas as pd
import os
import shutil
from datetime import datetime

def is_time_column(column_name, sample_data):
    # 转换列名为小写以进行不区分大小写的比较
    column_lower = str(column_name).lower()
    
    # 排除包含这些关键词的列
    exclude_keywords = ['平均', '指数', '速度', 'index', 'speed', 'average']
    if any(keyword in column_lower for keyword in exclude_keywords):
        return False
    
    # 时间相关的关键词
    time_keywords = ['time', 'date', 'timestamp', '时间']
    if not any(keyword in column_lower for keyword in time_keywords):
        return False
    
    # 检查数据样本是否符合时间格式
    if not isinstance(sample_data, (pd.Series, list)):
        return False
    
    # 获取前5个非空值作为样本
    sample_values = [str(x) for x in sample_data if pd.notna(x)][:5]
    if not sample_values:
        return False
    
    # 检查样本值是否包含数字和分隔符
    return all(any(c.isdigit() for c in value) and any(c in value for c in ':-/') for value in sample_values)

def format_time(time_str):
    try:
        # 处理不同的输入格式
        for fmt in ['%Y/%m/%d %H:%M', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%Y-%m-%d %H:%M']:
            try:
                dt = datetime.strptime(str(time_str), fmt)
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                continue
        return time_str
    except Exception:
        return time_str

def process_file(file_path):
    try:
        # 跳过备份文件和已格式化的文件
        filename = os.path.basename(file_path)
        if filename.startswith(('backup_', 'formatted_')):
            print(f"跳过处理备份或已格式化的文件: {file_path}")
            return

        # 读取CSV文件
        df = pd.read_csv(file_path)
        
        # 查找时间列
        time_columns = []
        for column in df.columns:
            if is_time_column(column, df[column]):
                time_columns.append(column)
                print(f"发现时间列: {column}")
        
        if not time_columns:
            print(f"在文件 {file_path} 中没有找到时间列")
            return
        
        # 只处理第一个找到的时间列
        time_column = time_columns[0]
        modified = False
        
        # 重命名时间列（如果需要）
        if time_column != 'Time':
            print(f"将列 {time_column} 重命名为 Time")
            df = df.rename(columns={time_column: 'Time'})
            modified = True
        
        # 格式化时间列
        df['Time'] = df['Time'].apply(format_time)
        modified = True
        
        if modified:
            # 生成输出文件名
            output_path = os.path.join(os.path.dirname(file_path), 'formatted_' + os.path.basename(file_path))
            backup_path = os.path.join(os.path.dirname(file_path), 'backup_' + os.path.basename(file_path))
            
            # 保存修改后的文件
            df.to_csv(output_path, index=False)
            print(f"已保存修改后的文件: {output_path}")
            
            try:
                # 创建原文件的备份
                shutil.copy2(file_path, backup_path)
                print(f"已备份原文件: {backup_path}")
                
                # 用格式化后的文件替换原文件
                shutil.copy2(output_path, file_path)
                
                # 删除临时的格式化文件
                os.remove(output_path)
            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {str(e)}")
                
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")

def main():
    # 指定数据目录
    data_dir = '../datas'
    
    # 获取所有CSV文件
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    print(f"找到 {len(csv_files)} 个CSV文件\n")
    
    # 处理每个文件
    for file_name in csv_files:
        file_path = os.path.join(data_dir, file_name)
        print(f"\n处理文件: {file_path}")
        process_file(file_path)

if __name__ == '__main__':
    main() 