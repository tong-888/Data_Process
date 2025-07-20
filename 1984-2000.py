import pandas as pd
excel_file_name = '1984-2000.xlsx'
df = pd.read_excel(excel_file_name, header=None, usecols=[0, 2])
df.columns = ['DATE', 'CONTENT']

df['DATE'] = pd.to_datetime(df['DATE'], format='%Y/%m/%d', errors='coerce')

def join_text(texts):
    return '\n\n'.join(texts.astype(str))

grouped_content = df.groupby(df['DATE'].dt.date)['CONTENT'].apply(join_text)
result_df = grouped_content.reset_index()
output_file_name = '1984-2000_combined.csv'
result_df.to_csv(output_file_name, index=False)
print(f"结果已保存到文件：{output_file_name}")