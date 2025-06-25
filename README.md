# College Feedback Classifier

This project classifies college feedback into categories using Hugging Face's zero-shot classification pipeline.

## Features
- Reads feedback from `feedback.csv` (column: `Feedback`).
- Classifies each entry into: Academics, Facilities, Administration, Others (default).
- Saves results to `classified_feedback.csv`.
- Plots category distribution as `category_distribution.png`.
- Supports custom categories via command-line argument.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Place your `feedback.csv` in the project directory.

## Usage
```bash
python classify_feedback.py
```

To specify custom categories:
```bash
python classify_feedback.py --categories "Academics,Facilities,Administration,Others,Hostel"
```

## Output
- `classified_feedback.csv`: CSV with predicted categories.
- `category_distribution.png`: Bar chart of feedback counts per category.

## Notes
- Requires Python 3.7+.
- Uses `facebook/bart-large-mnli` for zero-shot classification. 