import pandas as pd

def label_by_score(score):
    """
    Gắn nhãn cảm xúc dựa trên điểm số.
    - Điểm thấp (<= 2): negative
    - Điểm trung bình (3): neutral
    - Điểm cao (>= 4): positive
    """
    if score <= 2:
        return 'negative'
    elif score == 3:
        return 'neutral'
    elif score >= 4:
        return 'positive'
    else:
        return 'neutral'  # Trường hợp bất thường (nếu có)

def label_data_by_score(input_file, output_file):
    """
    Đọc dữ liệu, gắn nhãn cảm xúc theo score và lưu kết quả.
    """
    # Đọc dữ liệu
    print("Đang đọc dữ liệu...")
    df = pd.read_csv(input_file)

    # Kiểm tra sự tồn tại của cột 'score'
    if 'score' not in df.columns:
        raise ValueError("Cột 'score' không tồn tại trong dữ liệu!")

    print("Đang gắn nhãn cảm xúc dựa trên score...")
    # Áp dụng hàm gắn nhãn theo điểm số
    df['label'] = df['score'].apply(label_by_score)

    # Giữ lại chỉ cột 'content' và 'label' (hoặc 'review' nếu cột chứa bình luận có tên khác)
    if 'content' in df.columns:
        df_result = df[['content', 'label']]
    elif 'review' in df.columns:
        df_result = df[['review', 'label']]
    else:
        raise ValueError("Cột chứa bình luận ('content' hoặc 'review') không tồn tại trong dữ liệu!")

    print(f"Đang lưu dữ liệu đã gắn nhãn vào {output_file}...")
    # Lưu dữ liệu vào file Excel
    df_result.to_excel(output_file, index=False)
    print(f"Gắn nhãn thành công và lưu vào {output_file}!")

if __name__ == "__main__":
    # Đường dẫn file
    input_file = "data/lienquan_reviews_filtered.csv"  # File đầu vào
    output_file = "data/final_labeled_reviews_by_score.xlsx"  # File đầu ra

    # Gắn nhãn theo score
    label_data_by_score(input_file, output_file)
