
from google_play_scraper import Sort, reviews
import pandas as pd
# Thư viện pandas được sử dụng để xử lý dữ liệu và lưu vào file csv
def collect_chplay_reviews(app_id, lang='vi', country='vn', count=5000, output_file='chplay_reviews.csv'):
    # Lấy đánh giá từ CH Play
    result, _ = reviews(
        app_id,
        lang=lang,         # Ngôn ngữ (vi: tiếng Việt)
        country=country,   # Quốc gia (vn: Việt Nam)
        sort=Sort.NEWEST,  # Lấy đánh giá mới nhất
        count=count        # Số lượng đánh giá muốn thu thập
    )

    df = pd.DataFrame(result)

    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Đã lưu {len(df)} đánh giá vào {output_file}")

# Gọi hàm
if __name__ == "__main__":
    collect_chplay_reviews(
        app_id='com.garena.game.kgvn',  # ID app Liên Quân Mobile
        count=5000,  # Số lượng đánh giá
        output_file='data/lienquan_reviews_chplay.csv'
    )
