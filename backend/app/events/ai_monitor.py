import cv2
from ultralytics import YOLO
from app.events.event_manager import event_manager
from app.core.config import settings
from app.services.camera_service import camera_service

# Class mapping (MUST match training)
CLASS_MAP = {
    0: "finished",
    1: "failure_1",
    2: "failure_2"
}

# Lazy-loaded model (None until first use)
_model = None


def get_model():
    """Lazy load model on first use."""
    global _model
    if _model is None:
        model_path = settings.get_model_path()
        if not settings.model_exists():
            raise FileNotFoundError(
                f"Model file not found at {model_path}. "
                f"Please ensure the model file exists or set MODEL_PATH environment variable."
            )
        try:
            _model = YOLO(str(model_path))
            print(f"[AI] Model loaded from {model_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to load YOLO model: {str(e)}")
    return _model


def analyze_frame(frame):
    """Analyze a frame using YOLO model."""
    try:
        model = get_model()
        results = model(frame, verbose=False)
        detections = []

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])

                if conf >= settings.CONFIDENCE_THRESHOLD:
                    if cls_id in CLASS_MAP:
                        # Get bounding box coordinates
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        detections.append({
                            "class_id": cls_id,
                            "class_name": CLASS_MAP[cls_id],
                            "confidence": conf,
                            "bbox": [int(x1), int(y1), int(x2), int(y2)]
                        })
                    else:
                        print(f"[AI] Warning: Unknown class ID {cls_id} detected")

        return detections
    except Exception as e:
        print(f"[AI] Error analyzing frame: {str(e)}")
        return []


def draw_detections(frame, detections):
    """Draw detection boxes and labels on frame."""
    for det in detections:
        bbox = det.get("bbox")
        if bbox:
            x1, y1, x2, y2 = bbox
            
            # Choose color based on detection type
            if det["class_name"] == "finished":
                color = (0, 255, 0)  # Green
            elif det["class_name"] in ["failure_1", "failure_2"]:
                color = (0, 0, 255)  # Red
            else:
                color = (255, 255, 0)  # Cyan
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Draw label with confidence
            label = f"{det['class_name']}: {det['confidence']:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame, (x1, y1 - label_size[1] - 10), 
                         (x1 + label_size[0], y1), color, -1)
            cv2.putText(frame, label, (x1, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    return frame


def check_camera_available(camera_index: int) -> bool:
    """Check if camera is available."""
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        cap.release()
        return False
    
    # Try to read a frame to ensure camera works
    ret, _ = cap.read()
    cap.release()
    return ret


def monitor_printer(job):
    """Monitor printer using AI vision. Handles errors gracefully."""
    camera_index = settings.CAMERA_INDEX
    
    # Start camera service
    if not camera_service.start_camera(camera_index):
        error_msg = f"Camera {camera_index} is not available"
        print(f"[AI] ERROR: {error_msg}")
        event_manager.emit("job_monitoring_failed", job=job, error=error_msg)
        return
    
    # Check model availability
    try:
        get_model()
    except (FileNotFoundError, RuntimeError) as e:
        error_msg = str(e)
        print(f"[AI] ERROR: {error_msg}")
        camera_service.stop_camera()
        event_manager.emit("job_monitoring_failed", job=job, error=error_msg)
        return
    
    print(f"[AI] Monitoring job {job['id']} with camera {camera_index}")
    
    frame_count = 0
    consecutive_failures = 0
    max_consecutive_failures = 10

    try:
        while True:
            frame = camera_service.read_frame()
            if frame is None:
                consecutive_failures += 1
                if consecutive_failures >= max_consecutive_failures:
                    error_msg = f"Failed to read from camera {consecutive_failures} times in a row"
                    print(f"[AI] ERROR: {error_msg}")
                    event_manager.emit("job_monitoring_failed", job=job, error=error_msg)
                    break
                continue
            
            consecutive_failures = 0
            frame_count += 1
            
            # Analyze frame
            detections = analyze_frame(frame)
            
            # Draw detections on frame for streaming
            frame_with_detections = draw_detections(frame.copy(), detections)
            
            # Update camera service with annotated frame
            camera_service.update_frame(frame_with_detections)
            
            # Process detections
            for d in detections:
                if d["class_name"] == "finished":
                    print(f"[AI] Print finished detected (confidence: {d['confidence']:.2f})")
                    event_manager.emit("job_finished", job=job)
                    camera_service.stop_camera()
                    return

                if d["class_name"] in ["failure_1", "failure_2"]:
                    print(f"[AI] Failure detected: {d['class_name']} (confidence: {d['confidence']:.2f})")
                    event_manager.emit("job_failed", job=job)
                    camera_service.stop_camera()
                    return
            
            # Log progress every 100 frames
            if frame_count % 100 == 0:
                print(f"[AI] Processed {frame_count} frames for job {job['id']}")
    
    except KeyboardInterrupt:
        print(f"[AI] Monitoring interrupted for job {job['id']}")
    except Exception as e:
        error_msg = f"Unexpected error during monitoring: {str(e)}"
        print(f"[AI] ERROR: {error_msg}")
        event_manager.emit("job_monitoring_failed", job=job, error=error_msg)
    finally:
        camera_service.stop_camera()
        print(f"[AI] Camera released for job {job['id']}")
