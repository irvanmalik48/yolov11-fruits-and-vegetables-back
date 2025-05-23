import os
import numpy as np
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import ultralytics
from ultralytics import YOLO

ultralytics.checks()

model = YOLO("yolo11n-cls.pt")

results = model.train(data="../dataset/fav-stretched-cleaned", optimizer="Adam", epochs=20, patience=15, imgsz=640, batch=16, nbs=64, lr0=0.001, lrf=0.01)

def calculate_and_print_summary_metrics(y_true, y_pred, class_labels):
    """
    Calculates and prints macro, micro, and weighted averages for precision, recall, and F1-score.
    Args:
        y_true (list): List of true labels.
        y_pred (list): List of predicted labels.
        class_labels (list): List of all possible class names, used for averaging.
    """
    print("\n--- Summary Classification Metrics ---")
    
    report_labels = sorted(list(set(y_true + y_pred)))

    precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
        y_true, y_pred, average='macro', labels=report_labels, zero_division=0
    )
    precision_micro, recall_micro, f1_micro, _ = precision_recall_fscore_support(
        y_true, y_pred, average='micro', labels=report_labels, zero_division=0
    )
    precision_weighted, recall_weighted, f1_weighted, _ = precision_recall_fscore_support(
        y_true, y_pred, average='weighted', labels=report_labels, zero_division=0
    )

    print(f"\nMacro Average:")
    print(f"  Precision: {precision_macro:.4f}")
    print(f"  Recall:    {recall_macro:.4f}")
    print(f"  F1-score:  {f1_macro:.4f}")

    print(f"\nMicro Average (Overall Accuracy for P, R, F1):")
    print(f"  Precision: {precision_micro:.4f}")
    print(f"  Recall:    {recall_micro:.4f}")
    print(f"  F1-score:  {f1_micro:.4f}")
    
    print(f"\nWeighted Average:")
    print(f"  Precision: {precision_weighted:.4f}")
    print(f"  Recall:    {recall_weighted:.4f}")
    print(f"  F1-score:  {f1_weighted:.4f}")

def print_classification_report_details(y_true, y_pred, class_labels):
    """
    Prints a detailed classification report (precision, recall, F1 per class).
    Args:
        y_true (list): List of true labels.
        y_pred (list): List of predicted labels.
        class_labels (list): List of all possible class names, defining the report structure.
    """
    print("\n--- Detailed Classification Report ---")
    
    try:
        report = classification_report(y_true, y_pred, labels=class_labels, target_names=class_labels, zero_division=0)
        print(report)
    except ValueError as e:
        print(f"Could not generate classification report: {e}")
        print("Ensure 'class_labels' for the report are consistent with data.")
        print("Unique labels in actual data:", sorted(list(set(y_true))))
        print("Unique labels in predicted data:", sorted(list(set(y_pred))))


def calculate_and_plot_confusion_matrix(y_true, y_pred, class_labels, plot_filename="confusion_matrix.png"):
    """
    Calculates, prints, and plots the confusion matrix.
    Args:
        y_true (list): List of true labels.
        y_pred (list): List of predicted labels.
        class_labels (list): List of all possible class names for matrix ordering.
        plot_filename (str): Filename to save the plot.
    """
    print("\n--- Confusion Matrix ---")
    cm = confusion_matrix(y_true, y_pred, labels=class_labels)
    print("Raw Confusion Matrix (rows: actual, cols: predicted):")
    print(cm)

    if not class_labels:
        print("Skipping confusion matrix plot as no class_labels were provided.")
        return

    plt.figure(figsize=(max(10, len(class_labels)*0.5), max(8, len(class_labels)*0.4))) # Dynamic sizing
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_labels, yticklabels=class_labels, annot_kws={"size": 8})
    plt.title('Confusion Matrix', fontsize=16)
    plt.ylabel('Actual Label', fontsize=14)
    plt.xlabel('Predicted Label', fontsize=14)
    plt.xticks(rotation=90, ha='right', fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    plt.tight_layout()
    
    try:
        plt.savefig(plot_filename)
        print(f"\nConfusion matrix plot saved as {plot_filename}")
    except Exception as e:
        print(f"Error saving/showing confusion matrix plot: {e}")
    plt.close()

labels = sorted([
    'apple', 'banana', 'beetroot', 'bell pepper', 'cabbage', 'capsicum', 'carrot',
    'cauliflower', 'chilli pepper', 'corn', 'cucumber', 'eggplant', 'garlic',
    'ginger', 'grapes', 'jalepeno', 'kiwi', 'lemon', 'lettuce', 'mango',
    'onion', 'orange', 'paprika', 'pear', 'peas', 'pineapple', 'pomegranate',
    'potato', 'raddish', 'soy beans', 'spinach', 'sweetcorn', 'sweetpotato',
    'tomato', 'turnip', 'watermelon'
])

actual = []
predicted = []

model_favc = YOLO("runs/classify/train/weights/best.pt")

dir_main = "../input/fav-stretched-cleaned/test"

for path in os.listdir(dir_main):
    dir_path = os.path.join(dir_main, path)
    if os.path.isdir(dir_path):
        for image_file in os.listdir(dir_path):
            img_path = os.path.join(dir_path, image_file)
            results = model_favc.predict(img_path, verbose=False)[0]

            actual.append(path)

            idx_max = results.probs.data.cpu().argmax()

            if 0 <= idx_max < len(labels):
                predicted.append(labels[idx_max])
            else:
                predicted.append('unknown')

if not actual or not predicted:
    print("\nError: 'actual' or 'predicted' list is empty. Cannot calculate metrics.")
    print("Please ensure your model runs and populates these lists, or that dummy data is generated.")
else:
    calculate_and_print_summary_metrics(actual, predicted, labels)
    print_classification_report_details(actual, predicted, labels)
    calculate_and_plot_confusion_matrix(actual, predicted, labels)