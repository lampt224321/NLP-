import pandas as pd

# Đọc tập dữ liệu huấn luyện
train_file = "data/balance_training_data.xlsx"  # Kiểm tra kỹ tên file
df = pd.read_excel(train_file, engine='openpyxl')  # Sử dụng engine openpyxl nếu cần

# Kiểm tra tỷ lệ phân phối nhãn
print("Tỷ lệ phân phối nhãn:")
print(df['label'].value_counts(normalize=True))
