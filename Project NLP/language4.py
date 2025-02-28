import re
import pandas as pd

def normalize_gaming_terms(text, gamer_terms):
    """
    Chuẩn hóa văn bản với từ lóng game thủ nhưng vẫn giữ nguyên cấu trúc câu
    
    Args:
        text (str): Văn bản đầu vào
        gamer_terms (dict): Từ điển mapping từ lóng -> nghĩa chuẩn
    
    Returns:
        tuple: (văn bản đã chuẩn hóa, danh sách từ lóng phát hiện được)
    """
    words = text.split()
    detected_terms = []
    normalized_words = []
    
    for word in words:
        lower_word = word.lower()
        if lower_word in gamer_terms:
            # Thay thế từ lóng bằng nghĩa chuẩn
            normalized_words.append(gamer_terms[lower_word])
            detected_terms.append(lower_word)
        else:
            # Giữ nguyên từ không phải từ lóng
            normalized_words.append(word)
            
    return ' '.join(normalized_words), detected_terms

def mask_offensive_words(text, bad_words):
    """
    Phát hiện và che từ tục tĩu trong văn bản
    
    Args:
        text (str): Văn bản đầu vào
        bad_words (list): Danh sách từ tục cần che
    
    Returns:
        tuple: (văn bản đã che từ tục, danh sách từ tục phát hiện được)
    """
    words = text.split()
    detected_bad_words = []
    masked_words = []
    
    for word in words:
        lower_word = word.lower()
        if lower_word in bad_words:
            # Thay thế từ tục bằng dấu *
            masked_words.append('*' * len(word))
            detected_bad_words.append(lower_word)
        else:
            masked_words.append(word)
            
    return ' '.join(masked_words), detected_bad_words

def load_data_from_excel(file_path):
    """
    Đọc dữ liệu từ file Excel
    
    Args:
        file_path (str): Đường dẫn đến file Excel
        
    Returns:
        tuple: (từ điển gaming terms, danh sách từ tục)
    """
    gamer_terms_df = pd.read_excel(file_path, sheet_name="GAMER_TERMS")
    gamer_terms = dict(zip(gamer_terms_df["Key"], gamer_terms_df["Value"]))

    bad_words_df = pd.read_excel(file_path, sheet_name="BAD_WORDS") 
    bad_words = bad_words_df["Word"].tolist()

    return gamer_terms, bad_words

# Ví dụ sử dụng
if __name__ == "__main__":
    excel_file = "data/terms_and_words.xlsx"
    GAMER_TERMS, BAD_WORDS = load_data_from_excel(excel_file)
    
    input_text = "ks ad afk feed mày ngu quá địt dm ulti"
    
    # Xử lý từ lóng game thủ
    normalized_text, detected_terms = normalize_gaming_terms(input_text, GAMER_TERMS)
    print("Văn bản sau khi chuẩn hóa:", normalized_text)
    print("Từ lóng phát hiện được:", detected_terms)
    
    # Xử lý từ tục tĩu
    masked_text, detected_bad_words = mask_offensive_words(input_text, BAD_WORDS)
    print("Văn bản sau khi che từ tục:", masked_text)
    print("Từ tục phát hiện được:", detected_bad_words)