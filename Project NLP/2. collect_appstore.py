import time
from app_store_scraper import AppStore
import pandas as pd

def collect_appstore_reviews(app_id, country='vn', count=5000, output_file='appstore_reviews.csv'):
    app_store = AppStore(country=country, app_name=app_id)
    reviews = []
    fetched = 0
    batch_size = 20  # Adjust the batch size for fewer requests per call
    
    while fetched < count:
        try:
            app_store.review(how_many=batch_size)
            new_reviews = app_store.reviews
            reviews.extend(new_reviews)
            fetched += len(new_reviews)
            print(f"Fetched {fetched}/{count} reviews so far.")
            
            if len(new_reviews) < batch_size:
                # Exit if fewer reviews are returned, meaning no more reviews are available
                break
            
            # Add a delay to avoid hitting the server too frequently
            time.sleep(10)  # 10-second delay
        except Exception as e:
            print(f"Error occurred: {e}. Retrying in 30 seconds...")
            time.sleep(30)  # Retry after 30 seconds if an error occurs
    
    # Save reviews to CSV
    df = pd.DataFrame(reviews)
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Saved {len(df)} reviews to {output_file}")

if __name__ == "__main__":
    collect_appstore_reviews(
        app_id="garena-liên-quân-mobile",  # App ID for Liên Quân Mobile
        count=5000,
        output_file='data/lienquan_appstore_reviews.csv'
    )
