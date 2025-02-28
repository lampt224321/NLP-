import pickle
import pandas as pd
from sklearn.linear_model import LogisticRegression
from language4 import load_data_from_excel, normalize_gaming_terms, mask_offensive_words

def load_model(model_file):
    with open(model_file, 'rb') as f:
        model = pickle.load(f)
    return model

def preprocess_input(input_text, gamer_terms, bad_words):
    normalized_text, detected_terms = normalize_gaming_terms(input_text, gamer_terms)
    masked_text, detected_bad_words = mask_offensive_words(normalized_text, bad_words)
    return masked_text, detected_terms, detected_bad_words

def predict_label(model, input_text, vectorizer):
    input_text_vectorized = vectorizer.transform([input_text])  # Chuyển đổi văn bản thành vector
    prediction = model.predict(input_text_vectorized)
    return prediction[0]

if __name__ == "__main__":
    model_file = "models/logistic_regression.pkl"
    vectorizer_file = "models/tfidf_vectorizer.pkl"
    excel_file = "data/terms_and_words.xlsx"
    
    model = load_model(model_file)
    with open(vectorizer_file, 'rb') as f:
        vectorizer = pickle.load(f)
    
    gamer_terms, bad_words = load_data_from_excel(excel_file)
    
    input_text = input("Nhập comment: ")
    
    # Tiền xử lý và phát hiện từ lóng
    masked_text, detected_terms, detected_bad_words = preprocess_input(input_text, gamer_terms, bad_words)
    print("Văn bản sau khi che từ tục:", masked_text)
    print("Từ lóng phát hiện được:", detected_terms)
    print("Từ tục phát hiện được:", detected_bad_words)
    
    # Dự đoán nhãn
    predicted_label = predict_label(model, masked_text, vectorizer)  # Truyền đúng tham số
    print("Nhãn dự đoán:", predicted_label)