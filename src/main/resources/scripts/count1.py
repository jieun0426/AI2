import cv2
from ultralytics import YOLO
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
model_path = r"C:\심화AI\robotest\yolov5\runs\detect\debris_yolov814\weights\best.pt"
video_path = os.path.join(project_root, "src/main/resources/static/video/car1.mp4")
# 저장 경로
input_path = os.path.join(project_root, "data", "video/output_count.mp4")
output_path = os.path.join(project_root, "data", "video/output_cnt_converted.mp4")

model = YOLO(model_path)

cap = cv2.VideoCapture(video_path)

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

    # 객체 추적
    results = model.track(source=frame, persist=True, conf=0.3, show=False, verbose=False)

    # 프레임 복사해서 그리기용
    annotated_frame = frame.copy()

    if results and results[0].boxes.id is not None:
        boxes = results[0].boxes

        for box in boxes:
            # ID 및 클래스
            track_id = int(box.id[0])
            cls_id = int(box.cls[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # 원하는 라벨 형식: #1, #2, ...
            label_text = f"car {track_id}"

            # 박스 그리기
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

            # 라벨 텍스트 배경
            ((text_width, text_height), _) = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
            cv2.rectangle(annotated_frame, (x1, y1 - text_height - 10), (x1 + text_width, y1), (255, 0, 0), -1)

            # 라벨 텍스트
            cv2.putText(annotated_frame, label_text, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # 프레임 출력
    #cv2.imshow("test", annotated_frame)

    #if cv2.waitKey(1) & 0xFF == ord("q"):
    #    break
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

