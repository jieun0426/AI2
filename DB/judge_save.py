import numpy as np
import pandas as pd
import json
from pathlib import Path
import oracledb
import pickle

def read_json(folder_path): #folder_path에 지정된 경로 속 json 파일을 읽어온다.
    data_list=[] #json파일에서 읽어온 데이터를 저장할 빈 리스트
    folder=Path(folder_path) # 폴더 경로를 path객체로 변환해 folder변수로 재명

    for file in folder.glob("*.json"): # *.json파일을 하나 씩 반복해서 읽어온다
        try:
            with file.open(encoding="utf-8-sig") as f:
                data=json.load(f)
                data_list.append(data)
        except Exception as e:
            print("파일 오류")
    return data_list

folder_path=r"C:\data\01.민사법 LLM 사전학습 및 Instruction Tuning 데이터\3.개방데이터\1.데이터\Training\01.원천데이터\TS_01. 민사법_001. 판결문"
data=read_json(folder_path) # 위에서 정의한 함수를 호출해 JSON 데이터를 가져옵니다.
df=pd.DataFrame(data) # Pandas 데이터프레임으로 변환
print(df.columns)
#25
oracledb.init_oracle_client(lib_dir="C:\AIHub\instantclient_11_2") # 오라클 클라이언트 라이브러리의 경로를 지정

connect=oracledb.connect(user='mbc', password='1234', dsn='localhost') # 데이터베이스에 연결하는 Connection 객체를 생성
c=connect.cursor() #SQL 명령을

a=df["doc_class"]
b=df["doc_id"].str.split("-").str[1]
cc=df["casenames"]
d=df["normalized_court"]
e=df["casetype"]
f=df["sentences"]
g=df["announce_date"].str[:10]

for i in range(len(df)):
    print(i)

    c.execute("insert into hubdata0828 values(:1,:2,:3,:4,:5,:6,:7)",(
        a[i],b[i],cc[i],d[i],e[i], g[i], str(f[i])))
    
    connect.commit()
        
print("자료 저장 완료")
