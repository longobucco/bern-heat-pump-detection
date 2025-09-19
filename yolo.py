from ultralytics import YOLO

# Carica un modello pre-addestrato o nuovo
model = YOLO('yolov8n.pt')  # o .yaml

# Avvia il training
epochs = 5
for epoch in range(epochs):
    results = model.train(data='/Users/lucavisconti/Bern/bern-solar-panel-detection/data.yaml', epochs=5, imgsz=256, verbose=False)  # 1 epoca per volta
    print(f"Epoca {epoch + 1} completata")