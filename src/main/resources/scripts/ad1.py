import os
import random
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from PIL import Image
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 1. 경로 설정
train_dir = r"src/main/resources/static/data/ad_data/train"
test_dir = r"src/main/resources/static/data/ad_data/test"

# 2. 전처리 정의
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

# 3. 데이터셋 및 데이터로더
train_data = datasets.ImageFolder(train_dir, transform=transform)
test_data = datasets.ImageFolder(test_dir, transform=transform)

train_loader = DataLoader(train_data, batch_size=16, shuffle=True)
test_loader = DataLoader(test_data, batch_size=16, shuffle=False)

print("클래스:", train_data.classes)

# 4. 모델 불러오기 (ResNet18)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, 2)
model = model.to(device)

# 5. 손실 함수 & 옵티마이저
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 6. 학습 루프
num_epochs = 10
train_losses = []
train_accuracies = []

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    correct, total = 0, 0

    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, preds = torch.max(outputs, 1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

    epoch_loss = running_loss / len(train_loader)
    epoch_acc = correct / total
    train_losses.append(epoch_loss)
    train_accuracies.append(epoch_acc)

    print(f"Epoch {epoch+1}, Loss: {epoch_loss:.4f}, Accuracy: {100*epoch_acc:.2f}%")

# 7. 테스트 정확도
model.eval()
correct, total = 0, 0
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, preds = torch.max(outputs, 1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

test_acc = correct / total
print(f"테스트 정확도: {100*test_acc:.2f}%")

# 8. 손실률/정확도 그래프 저장
plt.figure(figsize=(12,5))
plt.rcParams['font.family'] ='Malgun Gothic'
plt.subplot(1,2,1)
plt.plot(range(1, num_epochs+1), train_losses, marker='o', color='red')
plt.title('손실률 변화 ')
plt.xlabel('반복횟수')
plt.ylabel('손실률')

plt.subplot(1,2,2)
plt.plot(range(1, num_epochs+1), [acc*100 for acc in train_accuracies], marker='o', color='blue')
plt.title('정확도 변화')
plt.xlabel('반복횟수')
plt.ylabel('정확도(%)')
graph_path = "data/ad_training_graph.png"
plt.savefig(graph_path)

# 9. 새 이미지 예측 함수
def predict_image(image_path, model):
    model.eval()
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)
    output = model(image)
    _, pred = torch.max(output, 1)
    classes = train_data.classes
    return classes[pred.item()]

test_img = r"src/main/resources/static/data/ad_data/test/normal/normal_test_1.jpg"
print("예측 결과:", predict_image(test_img, model))


# === 여기서부터 샘플 이미지 시각화 및 PDF 생성 ===

# 폴더 경로
normal_dir = test_dir+'/normal'
dementia_dir = test_dir+'/ad'

# 이미지 목록 수집
normal_imgs = [(os.path.join(normal_dir, f), '정상인') for f in os.listdir(normal_dir) if f.endswith(('.jpg', '.png'))]
dementia_imgs = [(os.path.join(dementia_dir, f), '치매 환자') for f in os.listdir(dementia_dir) if f.endswith(('.jpg', '.png'))]

all_imgs = normal_imgs + dementia_imgs
random.shuffle(all_imgs)
sample_imgs = all_imgs[:9]

# 시각화 및 예측 (실제 모델 예측으로 변경)
plt.figure(figsize=(12, 15))
plt.rcParams['font.family'] = 'Malgun Gothic'

for idx, (img_path, label) in enumerate(sample_imgs):
    img = Image.open(img_path).convert("RGB")
    image_tensor = transform(img).unsqueeze(0).to(device)
    output = model(image_tensor)
    prob = torch.softmax(output, dim=1)[0]
    conf_val, pred_idx = torch.max(prob, 0)
    pred_label = train_data.classes[pred_idx.item()]
    confidence = f"{conf_val.item()*100:.2f}%"

    pred_label = "치매 환자" if pred_label == 'ad' else "정상인"

    plt.subplot(3, 3, idx + 1)
    plt.imshow(img)
    plt.title(f"예측: {pred_label}\n정답: {label}\n정확도: {confidence}", fontsize=16)
    plt.axis('off')

plt.tight_layout()
sample_graph_path = "data/sample_predictions.png"
plt.savefig(sample_graph_path)
plt.close()
print(f"샘플 예측 이미지 저장 완료: {sample_graph_path}")

# 9-2. PDF 생성 함수
pdf_path = "data/training_report.pdf"
pdfmetrics.registerFont(TTFont('KoreanFont', 'C:/Windows/Fonts/malgun.ttf'))

def create_pdf_report(pdf_path, losses, accuracies, graph_path, sample_graph_path):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    c.setFont("KoreanFont", 20)
    c.drawString(72, height - 72, "Training Report")

    c.setFont("KoreanFont", 12)
    y = height - 120
    c.drawString(72, y, "Epoch별 손실률 및 정확도:")
    y -= 20
    for epoch, (loss, acc) in enumerate(zip(losses, accuracies), 1):
        text = f"Epoch {epoch}: 손실률 = {loss:.4f}, 정확도 = {acc*100:.2f}%"
        c.drawString(80, y, text)
        y -= 18
        if y < 100:
            c.showPage()
            y = height - 72

    # 손실률/정확도 그래프
    c.showPage()
    c.setFont("KoreanFont", 16)
    c.drawString(72, height - 72, "손실률 및 정확도 그래프")
    graph_img = ImageReader(graph_path)
    c.drawImage(graph_img, 36, height - 450, width=width-72, height=350, preserveAspectRatio=True)

    # 샘플 예측 그래프
    c.showPage()
    c.setFont("KoreanFont", 16)
    c.drawString(72, height - 72, "샘플 예측 결과 시각화")
    sample_img = ImageReader(sample_graph_path)

    # 직접 이미지 사이즈 얻기
    from PIL import Image
    pil_img = Image.open(sample_graph_path)
    img_width, img_height = pil_img.size
    aspect = img_height / img_width

    # 최대 폭 설정 (좌우 여백 36pt 정도만)
    max_width = width - 72  # 거의 전체 너비
    scaled_height = max_width * aspect  # 비율 맞춰 세로 계산

    # 최대 높이가 페이지보다 크면 다시 조정
    max_height = height - 120
    if scaled_height > max_height:
        scaled_height = max_height
        max_width = scaled_height / aspect

    x = (width - max_width) / 2
    y = (height - 72) - scaled_height - 20  # top 여백 포함

    c.drawImage(sample_img, x, y, width=max_width, height=scaled_height)

    c.save()

create_pdf_report(pdf_path, train_losses, train_accuracies, graph_path, sample_graph_path)
print(f"PDF 보고서 저장 완료: {pdf_path}")
