from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import Response
import base64
import io
import cv2
import numpy as np
import torch
from PIL import Image
import os
import logging
from typing import Dict, Any, Optional, Tuple
from sam2.sam2_image_predictor import SAM2ImagePredictor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Image Anonymization API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request models
class Point(BaseModel):
    x: int
    y: int

class SegmentRequest(BaseModel):
    image: str  # Base64 encoded image
    point: Point

class ImageAnonymizer:
    def __init__(self):
        self.predictor = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.init_sam()

    def init_sam(self):
        if self.predictor is not None:
            return

        self.predictor = SAM2ImagePredictor.from_pretrained(
            "facebook/sam2.1-hiera-small",
            device=self.device,
        )
        logger.info(f"SAM initialized on {self.device}")

    def get_segmentation_mask(self, image: np.ndarray, point: tuple[int, int]) -> Tuple[np.ndarray, float]:
        """Generate segmentation mask from a point."""
        init_sam()

        # Calculate bounding box around the point
        height, width = image.shape[:2]
        box_size = min(width, height) // 4
        x, y = point
        
        x_min = max(0, x - box_size)
        y_min = max(0, y - box_size)
        x_max = min(width, x + box_size)
        y_max = min(height, y + box_size)
        
        bbox = (x_min, y_min, x_max, y_max)

        with torch.inference_mode(), torch.autocast(self.device, dtype=torch.bfloat16):
            self.predictor.set_image(image)
            masks, scores, _ = self.predictor.predict(
                box=np.array(bbox),
                point_coords=np.array([[x, y]]),
                point_labels=np.array([1]),
                multimask_output=True,
            )

            # Get best mask
            best_idx = np.argmax(scores)
            return self._smoothen_mask(masks[best_idx]), scores[best_idx]

    @staticmethod
    def _smoothen_mask(mask: np.ndarray) -> np.ndarray:
        """Smooth the mask edges."""
        kernel = np.ones((20, 20), np.uint8)
        return cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_CLOSE, kernel)

    @staticmethod
    def _apply_blur(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """Apply blur to masked region."""
        if mask.ndim == 2:
            mask = np.stack((mask,) * 3, axis=-1)
        
        blurred = cv2.GaussianBlur(image, (35, 35), 50)
        return np.where(mask, blurred, image)

# Initialize the anonymizer
anonymizer = ImageAnonymizer()

def decode_base64_image(base64_string: str) -> Tuple[np.ndarray, str]:
    """Decode base64 image to numpy array."""
    try:
        if ',' in base64_string:
            header, base64_string = base64_string.split(',', 1)
            image_format = header.split(';')[0].split('/')[1]
        else:
            image_format = 'jpeg'
        
        image_bytes = base64.b64decode(base64_string)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return image, image_format
    except Exception as e:
        logger.error(f"Error decoding base64 image: {e}")
        raise HTTPException(status_code=400, detail="Invalid image data")

@app.get("/")
async def root():
    return {"message": "Image Anonymization API"}

@app.post("/segment")
async def segment_image(request: SegmentRequest):
    try:
        # Decode the image
        image, image_format = decode_base64_image(request.image)
        
        # Get segmentation mask
        point = (request.point.x, request.point.y)
        mask, score = anonymizer.get_segmentation_mask(image, point)
        
        # Apply blur
        result = anonymizer._apply_blur(image, mask)
        
        # Encode result
        success, buffer = cv2.imencode(f'.{image_format}', result)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to encode image")
        
        return Response(
            content=buffer.tobytes(),
            media_type=f"image/{image_format}"
        )
        
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)