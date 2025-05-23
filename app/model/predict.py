from ultralytics import YOLO

# Load a model
model = YOLO("best.pt")

labels = sorted([
    'apple', 'banana', 'beetroot', 'bell pepper', 'cabbage', 'capsicum', 'carrot',
    'cauliflower', 'chilli pepper', 'corn', 'cucumber', 'eggplant', 'garlic',
    'ginger', 'grapes', 'jalepeno', 'kiwi', 'lemon', 'lettuce', 'mango',
    'onion', 'orange', 'paprika', 'pear', 'peas', 'pineapple', 'pomegranate',
    'potato', 'raddish', 'soy beans', 'spinach', 'sweetcorn', 'sweetpotato',
    'tomato', 'turnip', 'watermelon'
])

def make_json(image_path: str, label: str):
    """
    Create a JSON object with image path and predicted label.

    Args:
        image_path (str): Path to the image file.
        label (str): Predicted class label.

    Returns:
        dict: JSON object with image path and predicted label.
    """
    return {
        "image_path": image_path,
        "predicted_label": label
    }

def predict(image_path: str):
    """
    Predict the class of an image using a YOLOv8 model.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Predicted class label.
    """
    results = model.predict(image_path, verbose=False)[0]

    idx_max = results.probs.data.cpu().argmax()
    
    result = labels[idx_max] if 0 <= idx_max < len(labels) else 'unknown'

    return make_json(image_path, result)