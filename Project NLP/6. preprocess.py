import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from language4 import normalize_gaming_terms, mask_offensive_words, load_data_from_excel

nltk.download('punkt')

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"[^a-zA-Z0-9\sáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴĐ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

if __name__ == "__main__":
    input_file = "data/final_labeled_reviews_by_score.xlsx"
    output_file = "data/lienquan_reviews_preprocessed.xlsx"
    terms_file = "data/terms_and_words.xlsx"

    print("Đang đọc dữ liệu...")
    df = pd.read_excel(input_file)
    df['content'] = df['content'].fillna("")

    print("Đang tải từ lóng và từ tục tĩu từ file Excel...")
    GAMER_TERMS = load_data_from_excel(terms_file)

    print("Đang làm sạch và xử lý dữ liệu...")
    df['gamer_terms_detected'] = df['content'].apply(
        lambda x: normalize_gaming_terms(str(x), GAMER_TERMS)
    )
        
    print(f"Đang lưu dữ liệu vào {output_file}...")
    df.to_excel(output_file, index=False)
    print("Hoàn thành!")
