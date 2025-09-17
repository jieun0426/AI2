from transformers import pipeline
import oracledb
import sys
sys.stdout.reconfigure(encoding='utf-8')

def get_context_from_db(keyword):
    oracledb.init_oracle_client(lib_dir="C:\\AIHub\\instantclient_11_2")

    conn = oracledb.connect(user='mbc', password='1234', dsn='localhost')
    cursor = conn.cursor()

    sql = "SELECT content FROM hubdata WHERE content LIKE :keyword AND ROWNUM = 1"
    cursor.execute(sql, keyword=f"%{keyword}%")
    row = cursor.fetchone()

    if row:
        question_value = row[0]
        if hasattr(question_value, 'read'):
            question_value = question_value.read()  # 커서, 연결 닫기 전에 읽기
    else:
        question_value = ""

    cursor.close()
    conn.close()

    return question_value

qa_pipeline = pipeline("question-answering", model="monologg/koelectra-base-v3-finetuned-korquad")

user_question = sys.argv[1]

context = get_context_from_db(user_question)

if not context:
    print("관련 자료가 없습니다.")
else:
    question=user_question+" 증상을 보이는 환자의 치료 방법은 무엇입니까?"
    result = qa_pipeline(question=question, context=context)
    print(result['answer'])
