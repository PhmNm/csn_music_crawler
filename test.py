import pandas as pd
table_file_dir = 'crawl_data.csv'
def check_exist_data(table_file_dir, name):
    df = pd.read_csv(table_file_dir)
    df = df[df['name'] == name]
    if df.shape[0] == 0:
        return False
    return True

print(check_exist_data(table_file_dir, 'từ bỏ'))