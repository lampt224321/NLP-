import pandas as pd
from imblearn.over_sampling import RandomOverSampler
from language4 import load_data_from_excel

def process_text_with_terms(text, gamer_terms):
    """
    Giữ nguyên văn bản và phát hiện từ lóng.
    """
    words = str(text).split()
    detected_terms = [word for word in words if word.lower() in gamer_terms]
    return text, ', '.join(detected_terms) if detected_terms else ''

def oversample_data(input_file, output_file, text_column='processed_content', label_column='label'):
    try:
        print("Đang đọc dữ liệu...")
        df = pd.read_excel(input_file, engine='openpyxl')
        
        if text_column not in df.columns or label_column not in df.columns:
            print("Các cột hiện tại trong dữ liệu:", df.columns)
            raise ValueError(f"Cột '{text_column}' hoặc '{label_column}' không tồn tại trong dữ liệu!")

        df = df.dropna(subset=[text_column, label_column])
        print(f"Dữ liệu sau khi loại bỏ giá trị rỗng: {df.shape[0]} dòng.")

        print("Đang tải từ lóng từ file Excel...")
        gamer_terms, _ = load_data_from_excel("data/terms_and_words.xlsx")

        print("Đang xử lý từ lóng trong dữ liệu...")
        df['content'], df['detected_terms'] = zip(*df[text_column].apply(lambda x: process_text_with_terms(x, gamer_terms)))

        X = df[text_column].values.reshape(-1, 1)
        y = df[label_column]

        print("Đang thực hiện oversampling...")
        ros = RandomOverSampler(random_state=42)
        X_resampled, y_resampled = ros.fit_resample(X, y)

        print("Đang chuyển đổi dữ liệu oversampled thành DataFrame...")
        df_resampled = pd.DataFrame({
            text_column: X_resampled.flatten(),
            label_column: y_resampled
        })
        
        # Xử lý lại từ lóng cho dữ liệu đã oversample
        df_resampled['content'], df_resampled['detected_terms'] = zip(*df_resampled[text_column].apply(
            lambda x: process_text_with_terms(x, gamer_terms)))

        print(f"Đang lưu dữ liệu cân bằng vào file Excel {output_file}...")
        df_resampled.to_excel(output_file, index=False, engine='openpyxl')
        print("Hoàn thành!")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    input_file = "data/lienquan_reviews_preprocessed.xlsx"
    output_file = "data/balance_training_data.xlsx"
    oversample_data(input_file, output_file, text_column='content', label_column='label')