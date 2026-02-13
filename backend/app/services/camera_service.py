import cv2
import threading
import numpy as np
from typing import Optional
from app.core.config import settings

class CameraService:
    """Service for managing camera access and frame streaming."""
    
    def __init__(self):
        self.camera: Optional[cv2.VideoCapture] = None
        self.current_frame: Optional[np.ndarray] = None
        self.lock = threading.Lock()
        self.camera_index = settings.CAMERA_INDEX
        self.is_running = False
    
    def start_camera(self, camera_index: Optional[int] = None) -> bool:
        """Start camera capture."""
        if self.is_running and self.camera is not None:
            return True
        
        index = camera_index if camera_index is not None else self.camera_index
        
        try:
            cap = cv2.VideoCapture(index)
            if not cap.isOpened():
                return False
            
            # Test if we can read a frame
            ret, frame = cap.read()
            if not ret:
                cap.release()
                return False
            
            with self.lock:
                self.camera = cap
                self.current_frame = frame
                self.is_running = True
                self.camera_index = index
            
            return True
        except Exception as e:
            print(f"[Camera] Error starting camera: {e}")
            return False
    
    def stop_camera(self):
        """Stop camera capture."""
        with self.lock:
            if self.camera is not None:
                self.camera.release()
                self.camera = None
            self.current_frame = None
            self.is_running = False
    
    def update_frame(self, frame: np.ndarray):
        """Update the current frame (called by AI monitor)."""
        with self.lock:
            self.current_frame = frame.copy() if frame is not None else None
    
    def get_latest_frame(self) -> Optional[np.ndarray]:
        """Get the latest frame."""
        with self.lock:
            if self.current_frame is not None:
                return self.current_frame.copy()
            elif self.camera is not None and self.camera.isOpened():
                ret, frame = self.camera.read()
                if ret:
                    self.current_frame = frame
                    return frame.copy()
        return None
    
    def read_frame(self) -> Optional[np.ndarray]:
        """Read a new frame from camera."""
        with self.lock:
            if self.camera is not None and self.camera.isOpened():
                ret, frame = self.camera.read()
                if ret:
                    self.current_frame = frame
                    return frame
        return None
    
    def is_available(self) -> bool:
        """Check if camera is available."""
        return self.is_running and self.camera is not None and self.camera.isOpened()

# Global camera service instance
camera_service = CameraService()
