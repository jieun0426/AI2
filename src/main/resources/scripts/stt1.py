import whisper
import os
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
input_path = os.path.join(project_root, "data", "temp_audio_file.wav")  # 이미 wav라면

# Whisper 모델 로드 (작은 모델, 필요에 따라 base, small, medium, large 선택 가능)
model = whisper.load_model("base")

# 음성 인식 (한국어 명시)
result = model.transcribe(input_path, language="ko")

print(result["text"])
