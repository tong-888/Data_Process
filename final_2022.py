import pandas as pd
import time # 引入time模块来获取当前时间

# --- 1. 配置与加载 ---
# 定义输入和输出文件名
excel_file_name = '数据/data/2022.xlsx'
output_csv_name = 'final_2022_combined.csv'
# 同样，使用相同的日志文件名来追加记录
log_file_name = 'processing_log.txt'

print(f"步骤 1/7: 开始处理文件 '{excel_file_name}'...")

# 读取Excel文件。由于文件自带列名，我们不需要设置 header=None。
# Pandas会自动将第一行作为列名。
try:
    df = pd.read_excel(excel_file_name)
    print("文件加载成功，已自动识别列名。")
    # 我们可以加一个检查，确保必需的列都存在
    required_columns = {'DATE', 'TITLE', 'CONTENT'}
    if not required_columns.issubset(df.columns):
        print(f"错误：文件中缺少必要的列。需要 {required_columns}，但只找到 {set(df.columns)}")
        exit()
except FileNotFoundError:
    print(f"错误：找不到文件 '{excel_file_name}'。请确认文件名和路径是否正确。")
    exit()
except Exception as e:
    print(f"读取文件时发生错误: {e}")
    exit()


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
# 【保留您的核心逻辑】使用 to_datetime 处理日期
# dayfirst=True 会优先尝试将 '10/12/2023' 解析为 12月10日, 而不是 10月12日
# errors='coerce' 会将任何无法解析的日期变为 NaT (Not a Time)
print("\n步骤 3/7: 正在转换日期格式 (优先解析'日/月/年')...")
df['DATE'] = pd.to_datetime(df['DATE'], dayfirst=True, errors='coerce')

# 清理那些日期格式不正确（被转换为NaT）的行
rows_before_dropna = len(df)
df.dropna(subset=['DATE'], inplace=True)
rows_after_dropna = len(df)
print("日期格式转换完成。")
if rows_before_dropna > rows_after_dropna:
    print(f"移除了 {rows_before_dropna - rows_after_dropna} 条无效日期行。")


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


# --- 7. 保存结果并追加日志 ---
print(f"\n步骤 7/7: 正在保存结果并更新日志文件...")

# 将最终处理好的DataFrame保存为CSV文件
result_df.to_csv(output_csv_name, index=False, encoding='utf-8-sig')
print(f"处理完成！结果已成功保存到文件：{output_csv_name}")

# --- 将本次统计信息追加到日志文件 ---
current_time = time.strftime("%Y-%m-%d %H:%M:%S")
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

# 使用 'a' (append) 模式将新日志追加到文件末尾
try:
    with open(log_file_name, 'a', encoding='utf-8') as f:
        f.write(log_content)
    print(f"统计信息已成功追加到文件：{log_file_name}")
except Exception as e:
    print(f"错误：无法写入日志文件。原因: {e}")