import pandas as pd
import numpy as np
df = pd.read_csv('crawl_data3.csv')
headers = ['author','name','lyric','audio_path','crawl_date']
i_0 = df['audio_path'].convert_dtypes()[0]
a = np.array(i_0)
print(a[0])