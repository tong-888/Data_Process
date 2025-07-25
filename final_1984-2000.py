import pandas as pd
import time # 引入time模块来获取当前时间

# --- 1. 配置与加载 ---
# 定义输入和输出文件名
excel_file_name = '数据/data/1984-2000.xlsx'
output_csv_name = 'final_1984-2000_combined.csv'
# 新增：定义日志文件名
log_file_name = 'processing_log.txt'

print(f"步骤 1/7: 开始处理文件 '{excel_file_name}'...")

# 读取Excel文件
df = pd.read_excel(excel_file_name, header=None, usecols=[0, 1, 2])
df.columns = ['DATE', 'TITLE', 'CONTENT']
print("文件加载成功，已指定列名为：DATE, TITLE, CONTENT")

# --- 2. 去重并统计 ---
# 记录去重前的原始行数
initial_rows = len(df)
print(f"\n步骤 2/7: 开始去重... 初始新闻条数: {initial_rows}")

# 根据“日期”和“新闻内容”两列来识别和删除重复行
df.drop_duplicates(subset=['DATE', 'CONTENT'], keep='first', inplace=True)

# 记录去重后的行数
deduplicated_rows = len(df)
# 计算并报告被删除的重复新闻数量
duplicate_count = initial_rows - deduplicated_rows
print(f"去重完成！共找到并删除了 {duplicate_count} 条重复的新闻。")
print(f"当前剩余新闻条数: {deduplicated_rows}")

# --- 3. 处理日期格式 ---
print("\n步骤 3/7: 正在转换日期格式...")
df['DATE'] = pd.to_datetime(df['DATE'], format='%Y/%m/%d', errors='coerce')
df.dropna(subset=['DATE'], inplace=True)
print("日期格式转换完成，并已移除无效日期行。")

# --- 4. 合并标题和内容 ---
print("\n步骤 4/7: 正在将新闻标题合并到内容前方...")
df['CONTENT'] = df['TITLE'].astype(str) + '\n' + df['CONTENT'].astype(str)
print("标题与内容合并完成。")

# --- 5. 定义文本合并函数 ---
def join_text(texts):
    """将一个Series中的所有文本元素用 '\n\n' 连接成一个字符串"""
    return '\n\n'.join(texts.astype(str))

print("\n步骤 5/7: 准备按日期分组...")

# --- 6. 按日期分组并合并内容 ---
print("\n步骤 6/7: 正在按日期合并所有新闻内容...")
grouped_content = df.groupby(df['DATE'].dt.date)['CONTENT'].apply(join_text)
result_df = grouped_content.reset_index()
print("所有新闻已按日期合并完毕。")

# --- 7. 保存结果 ---
print(f"\n步骤 7/7: 正在将结果保存到文件 '{output_csv_name}'...")
result_df.to_csv(output_csv_name, index=False, encoding='utf-8-sig')
print("-" * 50)
print(f"处理完成！结果已成功保存到文件：{output_csv_name}")


# --- 新增步骤 8: 记录统计信息到日志文件 ---
print(f"\n新增步骤: 正在将统计信息写入日志文件 '{log_file_name}'...")

# 获取当前时间，用于记录
current_time = time.strftime("%Y-%m-%d %H:%M:%S")

# 准备要写入文件的文本内容
log_content = f"""
==================================================
文件处理日志
==================================================
处理时间: {current_time}
输入文件: {excel_file_name}
输出文件: {output_csv_name}

------------------ 统计摘要 ------------------
原始新闻总条数: {initial_rows}
识别并删除的重复条数: {duplicate_count}
处理后剩余新闻条数: {deduplicated_rows}
----------------------------------------------
"""

# 使用 'w' 模式写入文件。如果文件已存在，会覆盖旧内容。
# 如果希望每次运行都追加记录而不是覆盖，可以将 'w' 改为 'a'。
# 这里我们使用 'w'，假设每次运行都是一次全新的处理。
try:
    with open(log_file_name, 'w', encoding='utf-8') as f:
        f.write(log_content)
    print(f"统计信息已成功保存到文件：{log_file_name}")
except Exception as e:
    print(f"错误：无法写入日志文件。原因: {e}")