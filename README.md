# Customer Lifetime Value (CLV) Prediction Using Multimodal Machine Learning

## 📌 Overview
This repository presents a complete machine learning pipeline for predicting **Customer Lifetime Value (CLV)** using a hybrid approach combining **regression, classification, and clustering** techniques. The project is designed to provide granular value prediction, customer segmentation, and high/low-value classification to support business decision-making, marketing strategies, and customer retention initiatives.

## 📁 Repository Structure
```
customerLifeTimeValue/
├── CLV.ipynb                  # Jupyter notebook containing model development and experiments
├── CLV.py                     # Python script version of the notebook
├── ProjectProposalReport.pdf  # Initial project proposal with architecture & methodology
├── finalPresentation.pdf      # Final presentation slide deck
├── README.md                  # Project documentation
```

## 🎯 Project Goals
- Predict customer lifetime value accurately using regression models
- Segment customers into groups using unsupervised learning
- Classify customers as high or low value based on predicted CLV

## 🧠 Methodology
### Data Collection
- Source: UCI Online Retail Dataset
- Data includes transactional, demographic, and behavioral information

### Preprocessing & Feature Engineering
- Cleaned nulls and duplicates
- Engineered Recency, Frequency, Monetary (RFM) scores
- Derived customer age, country, and encoded categorical features
- Normalized features with MinMaxScaler

### Modeling Stages
1. **Baseline Model:** Linear Regression to establish a basic benchmark
2. **Advanced Regression:** XGBoost Regressor with hyperparameter tuning
3. **Classification:** Random Forest Classifier for high/low value tagging
4. **Clustering:** KMeans to identify behavioral customer segments
5. **Ensemble:** Combined all outputs into a unified prediction pipeline

## ⚙️ Tools and Technologies
- **Languages:** Python
- **Libraries:** pandas, scikit-learn, XGBoost, NumPy, seaborn, matplotlib
- **Environment:** Google Colab, VSCode

## 📊 Evaluation Metrics
| Task            | Metric(s)                |
|----------------|--------------------------|
| Regression      | RMSE, MAE, R² Score        |
| Classification  | Accuracy, F1, ROC-AUC     |
| Clustering      | Silhouette Score          |

## 🧪 Results
- **XGBoost** outperformed baseline with higher R² and lower RMSE
- **Random Forest** achieved high precision in classification
- **KMeans** effectively segmented customers into 3 key clusters

## 🚀 Future Work
- Deploy the pipeline as a REST API for real-time prediction
- Integrate NLP-based features from customer reviews
- Explore deep learning (e.g., LSTM) for sequential behavior modeling

## 👨‍💻 Team Members
- Harshith Reddy Gundra - 700780724  
- Sainath Konda - 700757121  
- Nikhila Potla - 700754837  
- Sai Bhavani Prasad - 700754838  

## 📎 Links
- GitHub Repository: [customerLifeTimeValue](https://github.com/HarshithReddyG/customerLifeTimeValue)
- Dataset: [UCI Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail)

---
