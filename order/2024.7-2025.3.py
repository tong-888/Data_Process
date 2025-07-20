import pandas as pd
excel_file_name = '结果2024_7_3to2025_3_15.xlsx'
df = pd.read_excel(excel_file_name)
df['date'] = pd.to_datetime(df['date'], format='%Y 年 %m 月 %d 日', errors='coerce')

def join_text(texts):
    return '\n\n'.join(texts.astype(str))

grouped_content = df.groupby(df['date'].dt.date)['text'].apply(join_text)
result_df = grouped_content.reset_index()
output_file_name = '2024.7-2025.3_combined.csv'
result_df.to_csv(output_file_name, index=False)
print(f"结果已保存到文件：{output_file_name}")