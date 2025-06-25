import gradio as gr
import pandas as pd
from transformers import pipeline
import matplotlib.pyplot as plt
import tempfile

# Load zero-shot classifier once
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
CATEGORIES = ["Academics", "Facilities", "Administration", "Others"]

def classify_feedback(file):
    df = pd.read_csv(file.name)
    if "Feedback" not in df.columns:
        return "Error: No 'Feedback' column found in CSV", None, None

    predictions = []
    for feedback in df["Feedback"]:
        result = classifier(feedback, CATEGORIES)
        predictions.append(result["labels"][0])

    df["Predicted Category"] = predictions

    # Plot distribution
    category_counts = df["Predicted Category"].value_counts()
    plt.figure(figsize=(6, 4))
    category_counts.plot(kind="bar")
    plt.xlabel("Category")
    plt.ylabel("Number of Feedbacks")
    plt.title("Feedback Category Distribution")

    # Save to temp image file
    temp_img = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    plt.savefig(temp_img.name)
    plt.close()

    # Save output CSV
    temp_csv = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    df.to_csv(temp_csv.name, index=False)

    return "Classification complete ✅", temp_img.name, temp_csv.name

# Gradio UI
demo = gr.Interface(
    fn=classify_feedback,
    inputs=gr.File(label="Upload feedback.csv"),
    outputs=[
        gr.Textbox(label="Status"),
        gr.Image(label="Category Distribution"),
        gr.File(label="Download classified CSV")
    ],
    title="College Feedback Classifier (GenAI)",
    description="Upload a CSV with a 'Feedback' column. The model will classify each entry and visualize the distribution."
)

demo.launch()
