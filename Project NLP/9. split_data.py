import pickle
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import os

def align_data(tfidf_dict, labels_df):
    """
    Đảm bảo tfidf_matrix và labels có cùng số lượng mẫu và đúng thứ tự.
    
    Args:
        tfidf_dict (dict): Dictionary chứa ma trận TF-IDF và feature names
        labels_df (pd.DataFrame): DataFrame chứa nhãn
    """
    # Lấy ma trận TF-IDF từ dictionary
    tfidf_matrix = tfidf_dict['matrix']
    feature_names = tfidf_dict['feature_names']
    
    print("\nĐang căn chỉnh dữ liệu...")
    print(f"Kích thước ban đầu của TF-IDF matrix: {tfidf_matrix.shape}")
    print(f"Số lượng features: {len(feature_names)}")
    print(f"Số lượng nhãn ban đầu: {len(labels_df)}")
    
    # Lấy chỉ số của các mẫu có trong cả hai tập dữ liệu
    common_indices = np.arange(min(tfidf_matrix.shape[0], len(labels_df)))
    
    # Cắt ma trận TF-IDF và labels theo common_indices
    aligned_tfidf = tfidf_matrix[common_indices]
    aligned_labels = labels_df.iloc[common_indices]['label'].values
    
    print(f"Kích thước sau khi căn chỉnh:")
    print(f"TF-IDF matrix: {aligned_tfidf.shape}")
    print(f"Labels: {len(aligned_labels)}")
    
    return aligned_tfidf, aligned_labels, feature_names

def create_balanced_splits(tfidf_matrix, labels, train_size=0.7, val_size=0.15, test_size=0.15):
    """
    Tạo các split cân bằng cho train, validation và test.
    """
    # Chuyển labels thành numpy array nếu chưa phải
    labels = np.array(labels)
    
    # Đếm số lượng mẫu cho mỗi nhãn
    unique_labels, counts = np.unique(labels, return_counts=True)
    min_count = min(counts)
    
    print("\nPhân bố nhãn ban đầu:")
    for label, count in zip(unique_labels, counts):
        print(f"{label}: {count} mẫu")
    
    print(f"\nCân bằng về {min_count} mẫu cho mỗi nhãn")
    
    # Tạo indices cho mỗi nhãn
    balanced_indices = []
    for label in unique_labels:
        label_indices = np.where(labels == label)[0]
        # Lấy ngẫu nhiên số lượng mẫu bằng với min_count
        np.random.seed(42)  # Đảm bảo tính tái lập
        np.random.shuffle(label_indices)
        balanced_indices.extend(label_indices[:min_count])
    
    # Shuffle toàn bộ indices
    balanced_indices = np.array(balanced_indices)
    np.random.shuffle(balanced_indices)
    
    # Lấy dữ liệu đã cân bằng
    balanced_tfidf = tfidf_matrix[balanced_indices]
    balanced_labels = labels[balanced_indices]
    
    # Tính số lượng mẫu cho mỗi split
    total_samples = len(balanced_labels)
    n_train = int(total_samples * train_size)
    n_val = int(total_samples * val_size)
    
    # Chia thành train, validation và test
    X_train = balanced_tfidf[:n_train]
    y_train = balanced_labels[:n_train]
    
    X_val = balanced_tfidf[n_train:n_train+n_val]
    y_val = balanced_labels[n_train:n_train+n_val]
    
    X_test = balanced_tfidf[n_train+n_val:]
    y_test = balanced_labels[n_train+n_val:]
    
    return X_train, X_val, X_test, y_train, y_val, y_test

def split_and_save_data(tfidf_dict, labels_df, output_dir="data"):
    """
    Chia và lưu dữ liệu thành các tập train, validation và test.
    """
    # Tạo thư mục output nếu chưa tồn tại
    os.makedirs(output_dir, exist_ok=True)
    
    # Căn chỉnh dữ liệu
    aligned_tfidf, aligned_labels, feature_names = align_data(tfidf_dict, labels_df)
    
    # Chia dữ liệu thành các tập cân bằng
    X_train, X_val, X_test, y_train, y_val, y_test = create_balanced_splits(
        aligned_tfidf, aligned_labels, train_size=0.7, val_size=0.15, test_size=0.15
    )
    
    # In thống kê về các split
    print("\nThống kê về các split:")
    for name, y in [("Train", y_train), ("Validation", y_val), ("Test", y_test)]:
        unique, counts = np.unique(y, return_counts=True)
        print(f"\n{name} set:")
        print(f"Tổng số mẫu: {len(y)}")
        print("Phân bố nhãn:", dict(zip(unique, counts)))
    
    # Lưu các split và feature names
    files_to_save = {
        'train_data.pkl': {'matrix': X_train, 'feature_names': feature_names},
        'val_data.pkl': {'matrix': X_val, 'feature_names': feature_names},
        'test_data.pkl': {'matrix': X_test, 'feature_names': feature_names},
        'train_labels.pkl': y_train,
        'val_labels.pkl': y_val,
        'test_labels.pkl': y_test
    }
    
    for filename, data in files_to_save.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        print(f"Đã lưu {filepath}")

if __name__ == "__main__":
    # Đường dẫn file
    input_matrix_file = "data/tfidf_matrix.pkl"
    input_label_file = "data/balance_training_data.xlsx"
    
    # Tải dữ liệu
    print("Đang tải ma trận TF-IDF...")
    with open(input_matrix_file, 'rb') as f:
        tfidf_dict = pickle.load(f)
    
    print("Đang tải nhãn từ file Excel...")
    labels_df = pd.read_excel(input_label_file)
    
    # Chia và lưu dữ liệu
    split_and_save_data(tfidf_dict, labels_df)