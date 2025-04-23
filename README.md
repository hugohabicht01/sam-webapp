# Image Anonymization Application

A fullstack web application for image anonymization using Vue 3 with TypeScript and Python FastAPI. The application leverages the Segment Anything Model (SAM 2.1) to intelligently identify and blur selected regions in images.

## Features

- Drag & drop or file picker image upload
- Interactive point-based selection for anonymization
- Intelligent segmentation using SAM 2.1
- Full history tracking with undo/redo functionality
- Modern, responsive user interface built with Vue 3 and Tailwind CSS
- Stateless API with no data storage for privacy

## Project Structure

This project consists of two main components:

1. **Frontend**: Vue 3 with TypeScript and Tailwind CSS
2. **Backend**: Python FastAPI server with SAM 2.1 integration

## Getting Started

### Prerequisites

- Node.js 16+ 
- Python 3.8+
- npm or yarn

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/image-anonymization-app.git
   cd image-anonymization-app
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Download the SAM 2.1 model:
   ```bash
   mkdir -p sam_model
   # Download the model file and place it in the sam_model directory
   # For SAM 2.1, the file should be named 'sam2_b.pt'
   ```

### Running the Application

1. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. In a separate terminal, start the frontend development server:
   ```bash
   npm run dev
   ```

3. Open your browser and navigate to: http://localhost:5173

## Usage

1. Upload an image using drag & drop or the file picker
2. Click on any area of the image you want to anonymize
3. The application will automatically segment and blur the selected region
4. Use the undo/redo buttons to navigate through changes
5. Download your anonymized image when finished

## Environment Variables

### Frontend

Create a `.env` file in the root directory:

```
VITE_API_URL=http://localhost:8000
```

### Backend

No environment variables are required for basic operation.

## API Documentation

The backend API exposes the following endpoint:

- `POST /segment`: Processes an image by segmenting and blurring a region based on the provided point.

For detailed API documentation, run the backend server and navigate to http://localhost:8000/docs

## Security and Privacy

- All processing is done on-demand
- No images are stored on the server
- The application is stateless by design

## License

[MIT License](LICENSE)