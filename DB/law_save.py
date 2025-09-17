import pandas as pd
import numpy as np
import oracledb
import json

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from pathlib import Path

def read_json(folder_path):
    data_list=[]
    folder = Path(folder_path)
    for file in folder.glob('*.json'):
        try:
            with file.open(encoding='utf-8-sig') as f:
                data=json.load(f)
                data_list.append(data)
        except Exception as e:
                print('파일 읽기 실패')
    return data_list
        


folder_path=r'C:\data\01.민사법 LLM 사전학습 및 Instruction Tuning 데이터\3.개방데이터\1.데이터\Training\01.원천데이터\TS_01. 민사법_002. 법령'
data=read_json(folder_path)

df = pd.DataFrame(data)

print(df.head())

oracledb.init_oracle_client(lib_dir='C:\AIHub\instantclient_11_2')
connect = oracledb.connect(user='mbc', password='1234', dsn='localhost')
c=connect.cursor()

for i in range(len(df)):
    c.execute('insert into data3 values(data3_seq.nextval,:1,:2,:3,:4,:5,:6,:7,:8)',
              (df['statute_name'][i],
               df['effective_date'][i],
               df['proclamation_date'][i],
               df['statute_type'][i],
               df['statute_abbrv'][i],
               df['statute_category'][i],
               str(df['sentences'][i]),
               int(df['data_class'][i])
               ))

connect.commit()





    
