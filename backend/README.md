# Image Anonymization API

This is the backend component of the Image Anonymization application. It provides a FastAPI server that handles image segmentation and anonymization using the SAM 2.1 (Segment Anything Model).

## API Documentation

### Endpoints

#### `POST /segment`

Processes an image by segmenting and blurring a region based on the provided point.

**Request Body:**
```json
{
  "image": "base64-encoded-image-string",
  "point": {
    "x": 100,
    "y": 200
  }
}
```

**Response:**
- Content-Type: image/jpeg or image/png (depends on input format)
- Body: The processed image with the selected region blurred

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Setup Instructions

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the SAM 2.1 model:
   ```bash
   mkdir -p backend/sam_model
   # Download the model file and place it in the above directory
   # For SAM 2.1, the file should be named 'sam2_b.pt'
   ```

   Note: You can download the model from the official repository or use the download script if provided.

4. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at http://localhost:8000

## Development Notes

- The current implementation uses a mock segmentation function when the SAM model is not available.
- For production use, ensure you have properly configured CORS settings in the `main.py` file.
- The API is designed to be stateless. No images are stored on the server.

## Error Handling

The API returns appropriate HTTP status codes:
- 400 - Bad Request (invalid input)
- 500 - Internal Server Error (processing failures)

Each error response includes a detail message explaining the issue.