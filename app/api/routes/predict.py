from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi import Annotated
from app.model.predict import predict

router = APIRouter()

@router.post("/predict")

async def predict_image(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")]
):
    """
    Predict the class of an image using a YOLOv11 model.
    Args:
        file (UploadFile): The image file to be predicted.
    Returns:
        dict: JSON object with image path and predicted label.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    if not file.filename.endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .png, .jpg, and .jpeg are allowed.")
    
    if file.file._file.tell() > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds the limit of 5MB.")

    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        content = await file.read()
        temp_file.write(content)
    
    result = predict(temp_file_path)
    
    os.remove(temp_file_path)
    
    return result