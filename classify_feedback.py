import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import pipeline
from tqdm import tqdm
import argparse
import sys

# Default categories
DEFAULT_CATEGORIES = ["Academics", "Facilities", "Administration", "Others"]


def main():
    parser = argparse.ArgumentParser(description="Classify college feedback using zero-shot classification.")
    parser.add_argument('--categories', type=str, help='Comma-separated list of categories to classify feedback into.')
    parser.add_argument('--input', type=str, default='feedback.csv', help='Input CSV file (default: feedback.csv)')
    parser.add_argument('--output', type=str, default='classified_feedback.csv', help='Output CSV file (default: classified_feedback.csv)')
    parser.add_argument('--plot', type=str, default='category_distribution.png', help='Output plot file (default: category_distribution.png)')
    args = parser.parse_args()

    # Parse categories
    if args.categories:
        categories = [cat.strip() for cat in args.categories.split(',') if cat.strip()]
        if not categories:
            print("No valid categories provided. Using default categories.")
            categories = DEFAULT_CATEGORIES
    else:
        categories = DEFAULT_CATEGORIES

    print(f"Using categories: {categories}")

    # Load feedback data
    try:
        print(f"Loading feedback from {args.input} ...")
        df = pd.read_csv(args.input)
    except FileNotFoundError:
        print(f"Error: File '{args.input}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        sys.exit(1)

    if 'Feedback' not in df.columns:
        print("Error: 'Feedback' column not found in the input CSV.")
        sys.exit(1)

    # Load zero-shot classifier
    try:
        print("Loading zero-shot classification model (facebook/bart-large-mnli)... This may take a while the first time.")
        classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)

    # Classify feedback
    predictions = []
    print("Classifying feedback entries...")
    for feedback in tqdm(df['Feedback'], desc="Classifying"):
        try:
            result = classifier(feedback, categories)
            top_label = result['labels'][0] if result['labels'] else 'Unknown'
        except Exception as e:
            print(f"Warning: Could not classify feedback: {feedback}\nError: {e}")
            top_label = 'Unknown'
        predictions.append(top_label)

    df['Predicted_Category'] = predictions

    # Save results
    try:
        df.to_csv(args.output, index=False)
        print(f"Classified feedback saved to {args.output}")
    except Exception as e:
        print(f"Error saving output CSV: {e}")

    # Plot category distribution
    try:
        plt.figure(figsize=(8, 6))
        sns.countplot(x='Predicted_Category', data=df, order=pd.Series(predictions).value_counts().index)
        plt.title('Feedback Category Distribution')
        plt.xlabel('Category')
        plt.ylabel('Number of Feedbacks')
        plt.tight_layout()
        plt.savefig(args.plot)
        print(f"Category distribution plot saved to {args.plot}")
    except Exception as e:
        print(f"Error generating plot: {e}")

if __name__ == "__main__":
    main() 