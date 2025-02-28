import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, ConfusionMatrixDisplay

def plot_classification_report(y_true, y_pred, labels, title="Classification Report"):
    try:
        report = pd.DataFrame(classification_report(y_true, y_pred, target_names=labels, output_dict=True)).transpose()
        metrics = ['precision', 'recall', 'f1-score']
        report_df = report_df.loc[labels, metrics]
        
        plt.figure(figsize=(10, 6))
        report_df.plot(kind='bar', figsize=(10, 6), legend=True, colormap="viridis")
        plt.title(title)
        plt.xlabel('Classes')
        plt.ylabel('Scores')
        plt.ylim(0, 1)
        plt.xticks(rotation=45)
        plt.legend(loc='lower right')
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Lỗi khi vẽ báo cáo: {str(e)}")

def load_data(train_matrix_file, val_matrix_file, test_matrix_file, 
              train_label_file, val_label_file, test_label_file):
    print("Đang tải dữ liệu...")
    
    matrices = {}
    for name, file in [('train', train_matrix_file), ('val', val_matrix_file), ('test', test_matrix_file)]:
        with open(file, 'rb') as f:
            matrices[f'X_{name}'] = pickle.load(f)['matrix']  # Truy cập vào 'matrix'
            
    labels = {}
    for name, file in [('train', train_label_file), ('val', val_label_file), ('test', test_label_file)]:
        with open(file, 'rb') as f:
            labels[f'y_{name}'] = pickle.load(f)
            
    return (matrices['X_train'], matrices['X_val'], matrices['X_test'],
            labels['y_train'], labels['y_val'], labels['y_test'])

def evaluate_model(model, X, y, labels, dataset_name=""):
    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)
    
    print(f"\nKết quả đánh giá trên tập {dataset_name}:")
    print(f"Độ chính xác: {accuracy:.4f}")
    print("\nBáo cáo phân loại:")
    print(classification_report(y, y_pred))
    
    plt.figure(figsize=(8, 6))
    ConfusionMatrixDisplay.from_predictions(y, y_pred, display_labels=labels)
    plt.title(f"Confusion Matrix - {dataset_name}")
    plt.show()
    
    return accuracy, y_pred

def train_model(train_matrix_file, val_matrix_file, test_matrix_file,
                train_label_file, val_label_file, test_label_file, 
                model_file):
    try:
        # Load data
        X_train, X_val, X_test, y_train, y_val, y_test = load_data(
            train_matrix_file, val_matrix_file, test_matrix_file,
            train_label_file, val_label_file, test_label_file
        )
        
        print("\nKích thước dữ liệu:")
        print(f"Train: {X_train.shape[0]} mẫu")
        print(f"Validation: {X_val.shape[0]} mẫu")
        print(f"Test: {X_test.shape[0]} mẫu")
        
        labels = sorted(set(y_train))
        
        # Train model
        print("\nĐang huấn luyện Logistic Regression...")
        model = LogisticRegression(max_iter=1000, random_state=42, 
                                 class_weight='balanced',
                                 multi_class='multinomial')
        model.fit(X_train, y_train)
        
        # Evaluate
        train_accuracy, _ = evaluate_model(model, X_train, y_train, labels, "Train")
        val_accuracy, _ = evaluate_model(model, X_val, y_val, labels, "Validation") 
        test_accuracy, _ = evaluate_model(model, X_test, y_test, labels, "Test")
        
        # Save model
        with open(model_file, 'wb') as f:
            pickle.dump(model, f)
        print("\nĐã lưu mô hình thành công!")
        
        return model, (train_accuracy, val_accuracy, test_accuracy)
        
    except Exception as e:
        print(f"Lỗi: {str(e)}")
        raise

if __name__ == "__main__":
    data_dir = "data"
    model_dir = "models"
    
    train_matrix_file = f"{data_dir}/train_data.pkl"
    val_matrix_file = f"{data_dir}/val_data.pkl"
    test_matrix_file = f"{data_dir}/test_data.pkl"
    train_label_file = f"{data_dir}/train_labels.pkl"
    val_label_file = f"{data_dir}/val_labels.pkl"
    test_label_file = f"{data_dir}/test_labels.pkl"
    model_file = f"{model_dir}/logistic_regression.pkl"
    
    model, accuracies = train_model(
        train_matrix_file, val_matrix_file, test_matrix_file,
        train_label_file, val_label_file, test_label_file,
        model_file
    )