import pandas as pd
import time # 引入time模块来获取当前时间

# --- 1. 配置与加载 ---
# 定义输入和输出文件名
csv_file_name = '数据/data/2018-2024.6.csv'
output_csv_name = 'final_2018-2024.6_combined.csv'
# 同样，使用相同的日志文件名来追加记录
log_file_name = 'processing_log.txt'

print(f"步骤 1/7: 开始处理文件 '{csv_file_name}'...")

# 读取CSV文件。根据您的描述（无列名，三列），我们设置 header=None。
# 保留您指定的 'latin-1' 编码，这对于正确读取特定文件至关重要。
try:
    df = pd.read_csv(csv_file_name, header=None, encoding='latin-1')
    # 为三列数据手动指定列名
    df.columns = ['DATE', 'TITLE', 'CONTENT']
    print("文件加载成功，已指定列名为：DATE, TITLE, CONTENT")
except FileNotFoundError:
    print(f"错误：找不到文件 '{csv_file_name}'。请确认文件名和路径是否正确。")
    exit()
except Exception as e:
    print(f"读取文件时发生错误: {e}")
    exit()


# --- 2. 去重并统计 ---
# 记录去重前的原始行数
initial_rows = len(df)
print(f"\n步骤 2/7: 开始去重... 初始新闻条数: {initial_rows}")

# 根据“日期”和“新闻内容”两列来识别和删除重复行
# 注意：此时的'DATE'列还是字符串，但不影响基于字符串的精确匹配去重
df.drop_duplicates(subset=['DATE', 'CONTENT'], keep='first', inplace=True)

# 记录去重后的行数
deduplicated_rows = len(df)
# 计算并报告被删除的重复新闻数量
duplicate_count = initial_rows - deduplicated_rows
print(f"去重完成！共找到并删除了 {duplicate_count} 条重复的新闻。")
print(f"当前剩余新闻条数: {deduplicated_rows}")


# --- 3. 定义并应用自定义日期解析函数 ---
# 【保留您的核心逻辑】这个函数用于处理混合的日期格式
def parse_mixed_dates(date_str):
    """尝试以两种不同格式 ('日/月/年' 或 '年/月/日') 解析日期字符串"""
    if not isinstance(date_str, str):
        # 如果日期不是字符串，直接返回空值，增加代码稳健性
        return pd.NaT
    try:
        # 尝试 '日/月/年' 格式, e.g., '25/12/2023'
        return pd.to_datetime(date_str, format='%d/%m/%Y', errors='raise')
    except ValueError:
        # 如果失败，尝试 '年/月/日' 格式, e.g., '2023/12/25'
        try:
            return pd.to_datetime(date_str, format='%Y/%m/%d', errors='raise')
        except ValueError:
            # 如果两种格式都失败，返回 NaT (Not a Time)，表示无法解析
            return pd.NaT

print("\n步骤 3/7: 正在使用自定义函数解析混合日期格式...")
df['DATE'] = df['DATE'].apply(parse_mixed_dates)
print("日期格式解析完成。")


# --- 4. 清理无效日期 ---
print("\n步骤 4/7: 正在移除无法解析的无效日期行...")
# 删除那些日期解析后为空值 (NaT) 的行，确保后续操作不会出错
rows_before_dropna = len(df)
df.dropna(subset=['DATE'], inplace=True)
rows_after_dropna = len(df)
print(f"移除了 {rows_before_dropna - rows_after_dropna} 条无效日期行。")


# --- 5. 合并标题和内容 ---
print("\n步骤 5/7: 正在将新闻标题合并到内容前方...")
df['CONTENT'] = df['TITLE'].astype(str) + '\n' + df['CONTENT'].astype(str)
print("标题与内容合并完成。")


# --- 6. 定义文本合并函数 ---
def join_text(texts):
    """将一个Series中的所有文本元素用 '\n\n' 连接成一个字符串"""
    return '\n\n'.join(texts.astype(str))

print("\n步骤 6/7: 跳过按日期分组合并内容步骤...")
# --- 7. 按日期分组并合并内容 ---
# print("\n步骤 7/8: 正在按日期合并所有新闻内容...")
# grouped_content = df.groupby(df['DATE'].dt.date)['CONTENT'].apply(join_text)
# result_df = grouped_content.reset_index()
# print("所有新闻已按日期合并完毕。")


# --- 8. 保存结果并追加日志 ---
print(f"\n步骤 7/7: 正在保存结果并更新日志文件...")

# 将最终处理好的DataFrame保存为CSV文件
# 直接使用 df 保存结果
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
输入文件: {csv_file_name}
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