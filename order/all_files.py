import pandas as pd

# --- 1. 配置区 ---

# 把你的5个CSV文件名都放在这个列表里
# 请确保文件名的顺序大致是按时间顺序的，这样有助于提高效率，但不是必须的
input_csv_files = [
    '1984-2000_combined.csv',
    '2001-2017_combined.csv',
    '2018-2024.6_combined.csv',
    '2022_combined.csv',
    '2024.7-2025.3_combined.csv'
]

# 定义最终输出的合并文件名
output_csv_file = 'all_news.csv'

# --- 2. 逐个读取、跳过表头并合并 ---

# 创建一个空列表，用来存放从每个CSV文件中读取出来的数据
all_data_frames = []


# 遍历你在上面配置的每一个文件名
for file in input_csv_files:
    df_single = pd.read_csv(file, skiprows=1, header=None, encoding='latin-1')
    all_data_frames.append(df_single)


# 将列表里所有的数据（DataFrame）合并成一个大的数据表
full_df = pd.concat(all_data_frames, ignore_index=True)

# 手动为合并后的大表设置正确的列名
full_df.columns = ['DATE', 'CONTENT']

# --- 3. 数据清理和排序 ---

# 清理那些可能是空行的数据
full_df.dropna(inplace=True)


# 核心步骤：按照 'DATE' 列对整个数据表进行升序排序
full_df.sort_values(by='DATE', inplace=True)

# --- 4. 保存最终结果 ---
# 使用 encoding='utf-8-sig' 来确保CSV文件能被Excel正确打开，不会乱码
full_df.to_csv(output_csv_file, index=False, encoding='utf-8-sig')

print(f"\n结果已成功保存到文件：{output_csv_file}")