import pandas as pd
from langdetect import detect #Thư viện phát hiện ngôn ngữ của văn bản

# Hàm kiểm tra một đoạn văn bản có phải tiếng Việt hay không, trả về True nếu là tiếng Việt.
def is_vietnamese(text):
    try:
        return detect(text) == 'vi'
    except:
        return False

def merge_and_filter(chplay_file, appstore_file, output_file):
    # Đọc dữ liệu từ CSV
    chplay_df = pd.read_csv(chplay_file)
    appstore_df = pd.read_csv(appstore_file)

    # Hợp nhất dữ liệu
    merged_df = pd.concat([chplay_df, appstore_df], ignore_index=True)

    # Lọc đánh giá tiếng Việt
    merged_df['is_vietnamese'] = merged_df['content'].apply(is_vietnamese)
    filtered_df = merged_df[merged_df['is_vietnamese']]

    # Lưu dữ liệu sau khi lọc
    filtered_df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Đã lưu {len(filtered_df)} đánh giá tiếng Việt vào {output_file}")

# Gọi hàm
if __name__ == "__main__":
    merge_and_filter(
        chplay_file='data/lienquan_reviews_chplay.csv',
        appstore_file='data/lienquan_appstore_reviews.csv',
        output_file='data/lienquan_reviews_filtered.csv'
    )
# Hợp nhất dữ liệu từ hai nguồn.
# Lọc và giữ lại các đánh giá viết bằng tiếng Việt.
# Lưu dữ liệu đã lọc vào file mới.