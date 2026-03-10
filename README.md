# 🔍 Online Banking Fraud Detection System

A machine learning pipeline that detects fraudulent banking transactions
in real time. Built with Python, Scikit-learn, and Flask REST API.

## ⚡ Why I Built It This Way
I compared 3 classification models on an imbalanced fraud dataset.
Random Forest won (95% accuracy, 83% F1) because ensemble voting
handles class imbalance better than a single Decision Tree.
Logistic Regression scored 91% — good, but missed edge-case fraud
patterns that tree-based models capture through feature interaction.

## 🏗️ Architecture

  Transaction Input (JSON)
         ↓
  Flask REST API  (/predict endpoint)
         ↓
  Preprocessing Pipeline (StandardScaler + feature encoding)
         ↓
  Random Forest Model (fraud_detection_model.pkl)
         ↓
  Response: { 'prediction': 'Fraud' | 'Legitimate', 'confidence': 0.94 }

## 📊 Model Comparison
| Model               | Accuracy | F1-Score | Why Not Chosen         |
|---------------------|----------|----------|------------------------|
| Logistic Regression | 91%      | 76%      | Misses complex patterns|
| Decision Tree       | 89%      | 79%      | Overfits to train data |
| **Random Forest**   | **95%**  | **83%**  | ✅ Best generalization  |

## 🛠️ Tech Stack
- Python, Flask, Scikit-learn, Pandas, NumPy
- Jupyter Notebook for EDA and model training
- REST API for real-time predictions

## 🚀 Run Locally
```bash
git clone https://github.com/sakthipriyadhanaraj/online-banking-fraud-detection
cd online-banking-fraud-detection
pip install flask scikit-learn pandas numpy
python app.py
```

## 📬 Sample API Request
```json
POST /predict
{
  "amount": 15000,
  "transaction_type": "TRANSFER",
  "oldbalanceOrg": 15000,
  "newbalanceOrig": 0
}
```
