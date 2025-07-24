# main.py
# To run this server:
# 1. Make sure you have the required libraries:
#    pip install "fastapi[all]" uvicorn python-multipart ultralytics Pillow
#
# 2. Place your 'best.pt' model file in the same directory as this script.
#
# 3. Run the server from your terminal:
#    uvicorn main:app --host 0.0.0.0 --port 8000
#
# 4. Once running, you can access the interactive API documentation at:
#    http://127.0.0.1:8000/docs

import io
from PIL import Image
from ultralytics import YOLO
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# --- FastAPI App Initialization ---
# Create an instance of the FastAPI class. This will be our main API object.
# We've added a title and version for the API documentation.
app = FastAPI(
    title="Fruit & Vegetable Classifier API",
    description="An API that uses a YOLOv11 model to classify images of fruits and vegetables.",
    version="1.0.0",
)

# --- CORS (Cross-Origin Resource Sharing) Middleware ---
# This middleware allows the API to be called from web pages hosted on different domains.
# The settings below are permissive, allowing all origins, methods, and headers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# --- Model and Labels Configuration ---
# Define the path to your trained YOLO model file.
# IMPORTANT: This script assumes 'best.pt' is in the same directory.
MODEL_PATH = "./best.pt"

# Define the labels for the classes, sorted alphabetically to match the model's output.
LABELS = sorted([
    'apple', 'banana', 'beetroot', 'bell pepper', 'cabbage', 'capsicum', 'carrot',
    'cauliflower', 'chilli pepper', 'corn', 'cucumber', 'eggplant', 'garlic',
    'ginger', 'grapes', 'jalepeno', 'kiwi', 'lemon', 'lettuce', 'mango',
    'onion', 'orange', 'paprika', 'pear', 'peas', 'pineapple', 'pomegranate',
    'potato', 'raddish', 'soy beans', 'spinach', 'sweetcorn', 'sweetpotato',
    'tomato', 'turnip', 'watermelon'
])

# --- Model Loading ---
# Load the YOLO model from the specified path.
# This is done once when the application starts.
try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    # If the model file is not found or there's an error, the server can't function.
    # We print an error and set the model to None.
    print(f"FATAL: Error loading the YOLO model: {e}")
    print("Please make sure the 'best.pt' file is in the correct directory.")
    model = None

# --- Core Prediction Function ---
def predict_image_class(image: Image.Image):
    """
    Predict the class of an image using the loaded YOLO model.

    Args:
        image (PIL.Image.Image): The image to process.

    Returns:
        str: Predicted class label or 'unknown' if prediction fails.
    """
    # The model.predict method can take a PIL image directly
    results = model.predict(image, verbose=False)[0]

    # Check if probabilities are available in the results
    if results.probs is not None:
        # Get the index of the class with the highest probability
        idx_max = results.probs.data.cpu().argmax()
        # Ensure the index is within the bounds of the labels list
        if 0 <= idx_max < len(LABELS):
            return LABELS[idx_max]
    
    # Return 'unknown' if no prediction could be made
    return 'unknown'

# --- API Endpoint Definition ---
@app.post("/predict/")
async def create_prediction(file: UploadFile = File(...)):
    """
    Receives an image file, performs prediction, and returns the result.

    - **file**: An image file to be classified (JPG, PNG, etc.).

    Returns a JSON object with the original filename and the predicted label.
    """
    # First, check if the model was loaded successfully on startup.
    if not model:
        raise HTTPException(status_code=503, detail="Model is not available or failed to load.")

    # Verify that the uploaded file is an image.
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail=f"File '{file.filename}' is not an image.")

    try:
        # Read the contents of the uploaded file into memory.
        contents = await file.read()
        # Open the image from the in-memory bytes.
        image = Image.open(io.BytesIO(contents))
    except Exception:
        # If the file cannot be opened as an image, it's invalid.
        raise HTTPException(status_code=400, detail="Could not process the uploaded image file.")

    # Perform the prediction using our core function.
    predicted_label = predict_image_class(image)

    # Return the result in a JSON format.
    return {
        "image_name": file.filename,
        "predicted_label": predicted_label
    }

@app.get("/", include_in_schema=False)
async def root():
    """
    A simple root endpoint to confirm the server is running.
    Redirects to the API documentation.
    """
    return {"message": "API is running. Go to /docs for interactive documentation."}


# --- Server Execution ---
# This block allows the script to be run directly using 'python main.py'.
# However, for production, it's recommended to use Uvicorn as shown in the top comments.
if __name__ == "__main__":
    print("--- Starting FastAPI Server for YOLOv11 Classification ---")
    print("To access the interactive API docs, open: http://127.0.0.1:8000/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
