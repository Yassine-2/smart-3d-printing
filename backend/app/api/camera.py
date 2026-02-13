import cv2
import io
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.camera_service import camera_service

router = APIRouter()


def generate_frames():
    """Generator function to yield camera frames as JPEG."""
    while True:
        frame = camera_service.get_latest_frame()
        if frame is None:
            # Try to read a new frame
            frame = camera_service.read_frame()
        
        if frame is not None:
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if ret:
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        else:
            # If no frame available, yield a placeholder or wait
            import time
            time.sleep(0.1)


@router.get("/stream")
def stream_camera():
    """MJPEG stream endpoint for live camera feed."""
    # Ensure camera is started
    if not camera_service.is_available():
        camera_service.start_camera()
    
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@router.get("/frame")
def get_single_frame():
    """Get a single frame as JPEG (fallback endpoint)."""
    frame = camera_service.get_latest_frame()
    if frame is None:
        frame = camera_service.read_frame()
    
    if frame is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="Camera not available")
    
    ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
    if not ret:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail="Failed to encode frame")
    
    from fastapi.responses import Response
    return Response(content=buffer.tobytes(), media_type="image/jpeg")
