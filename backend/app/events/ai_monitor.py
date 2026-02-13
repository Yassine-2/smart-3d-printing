import cv2
from ultralytics import YOLO
from app.events.event_manager import event_manager

# Path to your trained YOLOv8 model
MODEL_PATH = "app/ai/models/my_model.pt"

# Load model
model = YOLO(MODEL_PATH)

# Class mapping (MUST match training)
CLASS_MAP = {
    0: "finished",
    1: "failure_1",
    2: "failure_2"
}

CONF_THRESHOLD = 0.6


def analyze_frame(frame):
    results = model(frame, verbose=False)
    detections = []

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])

            if conf >= CONF_THRESHOLD:
                detections.append({
                    "class_id": cls_id,
                    "class_name": CLASS_MAP[cls_id],
                    "confidence": conf
                })

    return detections


def monitor_printer(job):
    cap = cv2.VideoCapture(0)  # camera index
    print(f"[AI] Monitoring job {job['id']}")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        detections = analyze_frame(frame)

        for d in detections:
            if d["class_name"] == "finished":
                print("[AI] Print finished detected")
                event_manager.emit("job_finished", job=job)
                cap.release()
                return

            if d["class_name"] in ["failure_1", "failure_2"]:
                print(f"[AI] Failure detected: {d['class_name']}")
                event_manager.emit("job_failed", job=job)
                cap.release()
                return
