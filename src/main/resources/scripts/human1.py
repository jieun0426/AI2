import cv2
from ultralytics import YOLO
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))

model_path1 = r"C:\심화AI\robotest\yolov5\runs\segment\debris_yolov8_seg3\weights\best.pt"
model_path2 = os.path.join(project_root, "src/main/resources/static/video/saram.mp4")
# 원본 영상 경로
input_path = os.path.join(project_root, "data", "video/output_segment.mp4")
# 변환 후 저장할 경로
output_path = os.path.join(project_root, "data", "video/output_seg_converted.mp4")

model = YOLO(model_path1)

cap=cv2.VideoCapture(model_path2)

# 프레임 사이즈 정보 얻기
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# 비디오 저장 객체 설정 (코덱: mp4v)
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter(input_path, fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model.predict(source=frame, show=False, conf=0.02, task='segment')
    annotated_frame = results[0].plot(masks=True, boxes=False)
    out.write(annotated_frame)

cap.release()
out.release()
cv2.destroyAllWindows()


import subprocess

# ffmpeg 명령어 구성
command = [
    r"C:\ffmpeg\bin\ffmpeg.exe",
    "-y",
    "-i", input_path,
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "23",
    "-c:a", "aac",
    "-movflags", "+faststart",
    output_path
]

# ffmpeg 실행
try:
    subprocess.run(command, check=True)
    print("Video converted successfully!")
except subprocess.CalledProcessError as e:
    print("Error during conversion:", e)


