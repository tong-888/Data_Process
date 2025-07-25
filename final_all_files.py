import pandas as pd
import os  # 引入os模块，用于检查文件是否存在

# --- 1. 配置区 ---
print("步骤 1/5: 初始化配置...")

input_csv_files = [
    'final_1984-2000_combined.csv',
    'final_2001-2017_combined.csv',
    'final_2018-2024.6_combined.csv',
    'final_2022_combined.csv',
    'final_2024.7-2025.3_combined.csv'
]


# 定义最终合并后的文件名
output_csv_file = 'final_all_news_combined.csv'

print(f"配置完成。准备合并 {len(input_csv_files)} 个文件到 '{output_csv_file}'。")

# --- 2. 逐个读取并合并数据 ---
# 创建一个空列表，用于存放从每个CSV文件中读取的DataFrame对象
all_data_frames = []

print("\n步骤 2/5: 开始逐个读取CSV文件...")

# 遍历您在上面配置的每一个文件名
for file in input_csv_files:
    # 检查文件是否存在，如果不存在则跳过并给出提示
    if not os.path.exists(file):
        print(f"  -> 警告：文件 '{file}' 不存在，已跳过。")
        continue  # 继续下一个循环

    try:
        # 优化点：直接读取CSV。
        # Pandas会自动将第一行作为列名(header)，无需skiprows和手动设置列名。
        # 使用 'utf-8-sig' 编码，与我们之前保存文件时使用的编码保持一致。
        print(f"  -> 正在读取文件: '{file}'...")
        df_single = pd.read_csv(file, encoding='utf-8-sig')

        # 将读取到的数据添加到列表中
        all_data_frames.append(df_single)

    except Exception as e:
        # 如果读取过程中发生其他错误，打印错误信息并跳过
        print(f"  -> 错误：读取文件 '{file}' 时发生问题，已跳过。原因: {e}")

# --- 3. 合并所有数据 ---
# 检查是否成功读取了任何数据
if not all_data_frames:
    print("\n错误：未能成功读取任何文件，程序即将退出。请检查文件列表和文件内容。")
else:
    print("\n步骤 3/5: 正在将所有数据合并到一个表中...")
    # 使用 concat 将列表中的所有DataFrame垂直合并成一个
    # ignore_index=True 会重新生成一套从0开始的连续索引
    full_df = pd.concat(all_data_frames, ignore_index=True)
    print(f"合并完成！共包含 {len(full_df)} 条记录。")

    # --- 4. 数据清理和排序 ---
    print("\n步骤 4/5: 正在清理数据并按日期排序...")

    # 清理那些可能是空行的数据（尽管在此流程中不太可能出现，但这是个好习惯）
    rows_before_cleaning = len(full_df)
    full_df.dropna(subset=['DATE', 'CONTENT'], inplace=True)
    rows_after_cleaning = len(full_df)
    print(f"  -> 清理了 {rows_before_cleaning - rows_after_cleaning} 条空值行。")

    # 核心步骤：按照 'DATE' 列对整个数据表进行升序排序
    # 这能确保最终文件中的新闻是按时间顺序排列的
    full_df.sort_values(by='DATE', inplace=True)
    print("  -> 所有记录已按日期排序。")

    # --- 5. 保存最终结果 ---
    print(f"\n步骤 5/5: 正在将最终结果保存到文件 '{output_csv_file}'...")
    # 再次使用 'utf-8-sig' 编码，确保最终的合并文件在Excel中打开时不会乱码
    full_df.to_csv(output_csv_file, index=False, encoding='utf-8-sig')

    print("-" * 50)
    print("全部处理完成！")
    print(f"结果已成功保存到文件：{output_csv_file}")