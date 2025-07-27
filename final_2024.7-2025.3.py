import pandas as pd
import time # 引入time模块来获取当前时间

# --- 1. 配置与加载 ---
# 定义输入和输出文件名
excel_file_name = '数据/data/结果2024_7_3to2025_3_15.xlsx'
output_csv_name = 'final_2024.7-2025.3_combined.csv'
# 继续使用同一个日志文件进行追加记录
log_file_name = 'processing_log.txt'

print(f"步骤 1/8: 开始处理文件 '{excel_file_name}'...")

# 读取Excel文件。由于文件自带列名，我们不需要设置 header=None。
# Pandas会自动将第一行作为列名。
try:
    df = pd.read_excel(excel_file_name)
    # 确认需要的列是否存在
    required_columns = ['title', 'date', 'text']
    if not all(col in df.columns for col in required_columns):
        print(f"错误：文件中缺少必要的列。需要 {required_columns}，但只找到了 {list(df.columns)}")
        exit()
    print("文件加载成功，已识别列名。")
except FileNotFoundError:
    print(f"错误：找不到文件 '{excel_file_name}'。请确认文件名和路径是否正确。")
    exit()
except Exception as e:
    print(f"读取文件时发生错误: {e}")
    exit()


# --- 2. 去重并统计 ---
# 记录去重前的原始行数
initial_rows = len(df)
print(f"\n步骤 2/8: 开始去重... 初始记录总数: {initial_rows}")

# 根据“日期”和“文本内容”两列来识别和删除重复行
# 使用您文件中的列名 'date' 和 'text'
df.drop_duplicates(subset=['date', 'text'], keep='first', inplace=True)

# 记录去重后的行数
deduplicated_rows = len(df)
# 计算并报告被删除的重复记录数量
duplicate_count = initial_rows - deduplicated_rows
print(f"去重完成！共找到并删除了 {duplicate_count} 条重复记录。")
print(f"当前剩余记录条数: {deduplicated_rows}")


# --- 3. 处理日期格式 ---
# 【保留您的核心逻辑】使用您指定的中文日期格式进行解析
print("\n步骤 3/8: 正在解析中文日期格式...")
df['date'] = pd.to_datetime(df['date'], format='%Y 年 %m 月 %d 日', errors='coerce')
print("日期格式解析完成。")


# --- 4. 清理无效日期 ---
print("\n步骤 4/8: 正在移除无法解析的无效日期行...")
# 删除那些日期解析后为空值 (NaT) 的行
rows_before_dropna = len(df)
df.dropna(subset=['date'], inplace=True)
rows_after_dropna = len(df)
print(f"移除了 {rows_before_dropna - rows_after_dropna} 条无效日期行。")


# --- 5. 合并标题和内容 ---
print("\n步骤 5/8: 正在将 'title' 合并到 'text' 前方...")
# 使用 astype(str) 确保类型安全
df['text'] = df['title'].astype(str) + '\n' + df['text'].astype(str)
print("标题与内容合并完成。")


# --- 6. 定义文本合并函数 ---
def join_text(texts):
    """将一个Series中的所有文本元素用 '\n\n' 连接成一个字符串"""
    return '\n\n'.join(texts.astype(str))

print("\n步骤 6/8: 准备按日期分组...")

# --- 7. 按日期分组并合并内容 ---
# print("\n步骤 7/8: 正在按日期合并所有文本内容...")
# 按 'date' 列的日期部分分组，并对 'text' 列应用合并函数
# grouped_content = df.groupby(df['date'].dt.date)['text'].apply(join_text)
# result_df = grouped_content.reset_index()

# 为了与之前的输出文件保持一致，重命名列
# result_df.columns = ['DATE', 'CONTENT']
# print("所有记录已按日期合并完毕。")


# --- 8. 保存结果并追加日志 ---
print(f"\n步骤 8/8: 正在保存结果并更新日志文件...")

# 将最终处理好的DataFrame保存为CSV文件
# 直接使用 df 保存结果，并调整列名
df = df.rename(columns={'date': 'DATE', 'text': 'CONTENT'})
df.to_csv(output_csv_name, index=False, encoding='utf-8-sig')
print(f"处理完成！结果已成功保存到文件：{output_csv_name}")

# --- 将本次统计信息追加到日志文件 ---
# 获取当前时间
current_time = time.strftime("%Y-%m-%d %H:%M:%S")

# 准备日志内容
log_content = f"""

==================================================
文件处理日志
==================================================
处理时间: {current_time}
输入文件: {excel_file_name}
输出文件: {output_csv_name}

------------------ 统计摘要 ------------------
原始记录总条数: {initial_rows}
识别并删除的重复条数: {duplicate_count}
处理后剩余记录条数: {deduplicated_rows}
----------------------------------------------
"""

# 使用 'a' (append) 模式将新日志追加到文件末尾
try:
    with open(log_file_name, 'a', encoding='utf-8') as f:
        f.write(log_content)
    print(f"统计信息已成功追加到文件：{log_file_name}")
except Exception as e:
    print(f"错误：无法写入日志文件。原因: {e}")