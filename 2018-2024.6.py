import pandas as pd
csv_file_name = '2018-2024.6.csv'
df = pd.read_csv(csv_file_name, encoding='latin-1')

def parse_mixed_dates(date_str):
    try:
        # '日/月/年' 格式
        return pd.to_datetime(date_str, format='%d/%m/%Y')
    except ValueError:
        # 如果失败了
        try:
            # '年/月/日' 格式
            return pd.to_datetime(date_str, format='%Y/%m/%d')
        except ValueError:
            # 如果都失败了，说明这个日期有问题，返回空值
            return pd.NaT

df['DATE'] = df['DATE'].apply(parse_mixed_dates)

def join_text(texts):
    return '\n\n'.join(texts.astype(str))

grouped_content = df.groupby(df['DATE'].dt.date)['CONTENT'].apply(join_text)
result_df = grouped_content.reset_index()
output_file_name = '2018-2024.6_combined.csv'
result_df.to_csv(output_file_name, index=False)
print(f"结果已保存到文件：{output_file_name}")