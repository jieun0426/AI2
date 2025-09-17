import cv2
from ultralytics import YOLO
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
model_path = r"C:\심화AI\robotest\yolov5\runs\pose\debris_yolov8_pose4\weights\best.pt"
video_path = os.path.join(project_root, "src/main/resources/static/video/ski.mp4")
# 저장 경로
input_path = os.path.join(project_root, "data", "video/output_pose.mp4")
output_path = os.path.join(project_root, "data", "video/output_pose_converted.mp4")

# 모델 로드
model = YOLO(model_path)

# 비디오 열기
cap = cv2.VideoCapture(video_path)

# 프레임 사이즈 정보 얻기
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# 비디오 저장 객체 설정 (코덱: mp4v)
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter(input_path, fourcc, fps, (width, height))


# 스켈레톤 연결 정의 (인덱스 기준)
skeleton = [
    (0, 1),     # 어깨 연결
    (0, 4), (4, 5),  # 왼팔
    (1, 6), (6, 7),  # 오른팔
    (0, 3),         # 왼쪽 몸통
    (1, 2),         # 오른쪽 몸통
    (3, 2),         # 골반 중심 연결
    (3, 8), (8, 9),  # 왼다리
    (2, 10), (10, 11)  # 오른다리
]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 포즈 예측
    results = model.predict(source=frame, show=False, conf=0.2)

    annotated_frame = frame.copy()

    for result in results:
        keypoints_list = result.keypoints.xy  # [n, k, 2]

        for keypoints in keypoints_list:
            # keypoints = Tensor → numpy 변환
            keypoints = keypoints.cpu().numpy()

            # 점 그리기
            for x, y in keypoints:
                if x > 0 and y > 0:
                    cv2.circle(annotated_frame, (int(x), int(y)), 4, (0, 255, 0), -1)

            # 스켈레톤 선 그리기
            for i, j in skeleton:
                x1, y1 = keypoints[i]
                x2, y2 = keypoints[j]
                if x1 > 0 and y1 > 0 and x2 > 0 and y2 > 0:
                    cv2.line(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)

    # 시각화
    #cv2.imshow('Pose with Skeleton', annotated_frame)

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
