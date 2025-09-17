import pandas as pd
import numpy as np
import json
from pathlib import Path
import oracledb


def read_json(folder_path):
    data_list = [] # 읽어들일 json 자료가 저장될 곳
    folder = Path(folder_path)
    for file in folder.glob('*.json'):
        try:
            with file.open(encoding='utf-8-sig') as f:
            # utf-8-sig: 헤드나 머릿말, 꼬릿말 등을 무시
                data=json.load(f)
                data_list.append(data)
        except Exception as e:
            print('파일 오류')
            
    return data_list


# 폴더 위치 지정
folder_path = r"C:\data\09.필수의료 의학지식 데이터\3.개방데이터\1.데이터\Training\01.원천데이터\TS_국문_의학 교과서"
data = read_json(folder_path)
print(data)


df = pd.DataFrame(data)

print(df.columns)

# 자료를 오라클에 저장(클라이언트 드라이버 설치)
oracledb.init_oracle_client(lib_dir="C:\AIHub\instantclient_11_2")
connect = oracledb.connect(user="mbc", password="1234", dsn="localhost")
c = connect.cursor()

for i in range(len(df)):    
    # 이미 존재하는지 확인
    c.execute("SELECT COUNT(*) FROM hubdata WHERE c_id = :1", (df["c_id"][i],))
    exists = c.fetchone()[0]
    
    if exists:
        continue
    
    c.execute("insert into hubdata values(:1,:2,:3,:4,:5,:6, hubdata_seq.nextval)", (
        df["c_id"][i],
        int(df["domain"][i]),
        int(df["source"][i]),
        df["source_spec"][i],
        df["creation_year"][i],
        df["content"][i]
        ))

    connect.commit()
