# -*- coding: utf-8 -*-

import os
from gtts import gTTS
import sys

text = sys.argv[1]
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
save_path = os.path.join(project_root, "data", "tts_output.mp3")


print("저장 경로:", save_path)  # 디버그용

try:
    tts = gTTS(text=text, lang='ko')
    tts.save(save_path)
    print("TTS 저장 완료")
except Exception as e:
    print("TTS 저장 실패:", e)
