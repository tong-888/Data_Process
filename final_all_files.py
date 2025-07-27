import pandas as pd

# 定义输入和输出文件路径
input_csv_files = [
    'final_1984-2000_combined.csv',
    'final_2001-2017_combined.csv',
    'final_2018-2024.6_combined.csv',
    'final_2022_combined.csv',
    'final_2024.7-2025.3_combined.csv'
]
output_csv_file = 'final_all_news_combined.csv'

# 初始化一个空的 DataFrame 用于存储合并后的数据
combined_df = pd.DataFrame()

# 遍历每个输入 CSV 文件
for index, file in enumerate(input_csv_files, start=1):
    print(f"正在处理第 {index}/{len(input_csv_files)} 个文件: {file}")
    try:
        # 读取 CSV 文件
        df = pd.read_csv(file)
        # 选择需要的列
        selected_df = df[['DATE', 'CONTENT']]
        # 合并数据
        combined_df = pd.concat([combined_df, selected_df], ignore_index=True)
        print(f"文件 {file} 处理完成，已合并到总数据中。")
    except FileNotFoundError:
        print(f"错误：文件 {file} 未找到，请检查文件路径。")
    except KeyError:
        print(f"错误：文件 {file} 中缺少 'DATE' 或 'CONTENT' 列，请检查文件内容。")

if not combined_df.empty:
    print("所有文件处理完成，正在对合并后的数据按日期排序...")
    # 将 DATE 列转换为日期时间类型
    combined_df['DATE'] = pd.to_datetime(combined_df['DATE'])
    # 按日期排序
    combined_df = combined_df.sort_values(by='DATE')
    print("数据排序完成。")

    print(f"正在将合并并排序后的数据保存到 {output_csv_file}...")
    # 保存合并并排序后的数据到 CSV 文件
    combined_df.to_csv(output_csv_file, index=False, encoding='utf-8-sig')
    print(f"数据已成功保存到 {output_csv_file}。")
else:
    print("没有有效的数据可以合并，请检查输入文件。")
