import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os
from typing import Dict, Any
import re

def clean_text(text: str) -> str:

    if pd.isna(text):
        return ""
    
    # Chuyển về chữ thường
    text = str(text).lower()
    
    # Loại bỏ ký tự đặc biệt, giữ lại chữ và số
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Chuẩn hóa khoảng trắng
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def create_tfidf_matrix(
    input_file: str,
    output_file: str,
    model_file: str,
    text_column: str = 'content',
    label_column: str = 'label',
    max_features: int = 10000,
    min_df: int = 2,
    max_df: float = 0.95
) -> Dict[str, Any]:

    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    os.makedirs(os.path.dirname(model_file), exist_ok=True)
    
    print("Đang đọc dữ liệu từ file Excel...")
    df = pd.read_excel(input_file)
    
    print(f"\nThống kê ban đầu:")
    print(f"Số lượng mẫu: {len(df)}")
    label_counts = df[label_column].value_counts()
    print("\nPhân bố nhãn:")
    for label, count in label_counts.items():
        print(f"{label}: {count} mẫu")
    
    print("\nĐang tiền xử lý văn bản...")
    texts = df[text_column].apply(clean_text).values
    
    print("Đang tạo ma trận TF-IDF...")
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        min_df=min_df,
        max_df=max_df,
        ngram_range=(1, 2)  # Unigrams và bigrams
    )
    
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    
    print(f"\nThông tin ma trận TF-IDF:")
    print(f"Kích thước: {tfidf_matrix.shape}")
    print(f"Số lượng features: {len(feature_names)}")
    
    # Lưu ma trận TF-IDF và feature names
    tfidf_dict = {
        'matrix': tfidf_matrix,
        'feature_names': feature_names
    }
    
    print(f"\nĐang lưu ma trận TF-IDF vào {output_file}")
    with open(output_file, 'wb') as f:
        pickle.dump(tfidf_dict, f)
    
    print(f"Đang lưu model vectorizer vào {model_file}")
    with open(model_file, 'wb') as f:
        pickle.dump(vectorizer, f)
    
    return tfidf_dict

if __name__ == "__main__":
    # Đường dẫn file
    input_file = "data/balance_training_data.xlsx"  # File Excel đầu vào
    output_file = "data/tfidf_matrix.pkl"           # File ma trận TF-IDF
    model_file = "models/tfidf_vectorizer.pkl"      # File model TF-IDF
    
    # Tạo ma trận TF-IDF
    tfidf_dict = create_tfidf_matrix(
        input_file=input_file,
        output_file=output_file,
        model_file=model_file,
        text_column='content',          # Tên cột văn bản
        label_column='label',           # Tên cột nhãn
        max_features=10000,             # Số lượng features tối đa
        min_df=2,                       # Từ phải xuất hiện ít nhất 2 lần
        max_df=0.95                     # Từ xuất hiện trong tối đa 95% văn bản
    )