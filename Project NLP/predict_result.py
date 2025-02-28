import joblib
import pickle
import pandas as pd
from language4 import normalize_gaming_terms, mask_offensive_words, load_data_from_excel

# File paths
test_matrix_file = "data/test_data.pkl"  # Đảm bảo rằng file này tồn tại
test_label_file = "data/test_labels.pkl"
model_file = "models/logistic_regression.pkl"
vectorizer_file = "models/tfidf_vectorizer.pkl"
output_file = "output/predicted_results.xlsx"

# Load model and vectorizer
print("Loading model and vectorizer...")
model = joblib.load(model_file)
vectorizer = joblib.load(vectorizer_file)

# Load test data
print("Loading test data...")
with open(test_matrix_file, 'rb') as f:
    test_data = pickle.load(f)
    X_test = test_data['matrix']  # Truy cập vào ma trận TF-IDF

with open(test_label_file, 'rb') as f:
    y_test = pickle.load(f)

# Convert test data back to original text format
original_comments = vectorizer.inverse_transform(X_test)
comments_list = [" ".join(comment) for comment in original_comments]

# Load gamer terms and bad words for detection
gamer_terms, bad_words = load_data_from_excel("data/terms_and_words.xlsx")

# Predict sentiment
print("Predicting sentiment...")
predicted_probs = model.predict_proba(X_test)
predicted_labels = model.predict(X_test)

# Process and rewrite comments
print("Rewriting comments...")
rewritten_comments = []
detected_terms_list = []  # List to store detected gamer terms for each comment
for comment in comments_list:
    normalized_text, detected_terms = normalize_gaming_terms(comment, gamer_terms)
    masked_text, _ = mask_offensive_words(normalized_text, bad_words)
    rewritten_comments.append(masked_text)
    detected_terms_list.append(", ".join(detected_terms))  # Join detected terms into a string

# Prepare results for export
print("Preparing results for export...")
df_results = pd.DataFrame({
    "True Label": y_test,
    "Predicted Label": predicted_labels,
    "Positive Probability": predicted_probs[:, 1],
    "Negative Probability": predicted_probs[:, 0],
    "Rewritten Comment": rewritten_comments,
    "Detected Gamer Terms": detected_terms_list  # Add detected terms to the DataFrame
})

# Save to Excel
print(f"Saving results to {output_file}...")
df_results.to_excel(output_file, index=False)
print("Results saved successfully.")