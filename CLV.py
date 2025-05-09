# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1caf02QI04MeQW8XXpCfUWsCgaIhbVVcr
"""

pip install pandas openpyxl

import pandas as pd

# Load the dataset
file_path = 'dataset.xlsx'  # Replace with the actual path if needed
data = pd.read_excel(file_path)

# Display the first 5 rows
print(data.head())

# Display the column names and data types
print("\nColumn Names and Data Types:")
print(data.info())

# Check for missing values
missing_values = data.isnull().sum()
print("Missing Values:\n", missing_values)

# Drop rows with missing 'Description'
data = data.dropna(subset=['Description'])

# Fill missing 'CustomerID' with a placeholder (-1)
data['CustomerID'] = data['CustomerID'].fillna(-1)

# Verify that there are no missing values left
missing_values_after = data.isnull().sum()
print("Missing Values After Handling:\n", missing_values_after)

# Check the number of rows remaining
print("Number of Rows After Handling Missing Values:", len(data))

# Check for missing values again
print("Missing Values After Handling:\n", data.isnull().sum())

# Summary statistics for numeric columns
numeric_columns = ['Quantity', 'UnitPrice']
summary_stats = data[numeric_columns].describe()
print("Summary Statistics:\n", summary_stats)

import matplotlib.pyplot as plt
import seaborn as sns

# Set up the figure and axes
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot histograms
sns.histplot(data['Quantity'], bins=50, ax=axes[0], kde=True, color='blue')
axes[0].set_title('Distribution of Quantity')
axes[0].set_xlabel('Quantity')
axes[0].set_ylabel('Frequency')

sns.histplot(data['UnitPrice'], bins=50, ax=axes[1], kde=True, color='green')
axes[1].set_title('Distribution of UnitPrice')
axes[1].set_xlabel('UnitPrice')
axes[1].set_ylabel('Frequency')

plt.tight_layout()
plt.show()

# Set up the figure and axes
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot boxplots
sns.boxplot(data['Quantity'], ax=axes[0], color='blue')
axes[0].set_title('Boxplot of Quantity')
axes[0].set_xlabel('Quantity')

sns.boxplot(data['UnitPrice'], ax=axes[1], color='green')
axes[1].set_title('Boxplot of UnitPrice')
axes[1].set_xlabel('UnitPrice')

plt.tight_layout()
plt.show()

# Remove rows with invalid Quantity and UnitPrice
data = data[(data['Quantity'] > 0) & (data['UnitPrice'] > 0)]

# Cap Quantity and UnitPrice at the 99th percentile
quantity_99th = data['Quantity'].quantile(0.99)
unitprice_99th = data['UnitPrice'].quantile(0.99)

data['Quantity'] = data['Quantity'].clip(upper=quantity_99th)
data['UnitPrice'] = data['UnitPrice'].clip(upper=unitprice_99th)

# Summary statistics after handling outliers
summary_stats_cleaned = data[numeric_columns].describe()
print("Summary Statistics After Cleaning:\n", summary_stats_cleaned)

# Visualize cleaned distributions
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

sns.histplot(data['Quantity'], bins=50, ax=axes[0], kde=True, color='blue')
axes[0].set_title('Distribution of Quantity (Cleaned)')
axes[0].set_xlabel('Quantity')
axes[0].set_ylabel('Frequency')

sns.histplot(data['UnitPrice'], bins=50, ax=axes[1], kde=True, color='green')
axes[1].set_title('Distribution of UnitPrice (Cleaned)')
axes[1].set_xlabel('UnitPrice')
axes[1].set_ylabel('Frequency')

plt.tight_layout()
plt.show()

# Create TotalAmount feature
data['TotalAmount'] = data['Quantity'] * data['UnitPrice']

# Verify the new feature
print(data[['Quantity', 'UnitPrice', 'TotalAmount']].head())

# Extract features from InvoiceDate
data['DayOfWeek'] = data['InvoiceDate'].dt.day_name()  # Day of the week
data['Month'] = data['InvoiceDate'].dt.month           # Month (1-12)
data['Hour'] = data['InvoiceDate'].dt.hour             # Hour (0-23)
data['DayOfMonth'] = data['InvoiceDate'].dt.day        # Day of the month (1-31)

# Verify the new features
print(data[['InvoiceDate', 'DayOfWeek', 'Month', 'Hour', 'DayOfMonth']].head())

import matplotlib.pyplot as plt
import seaborn as sns

# Group by month and calculate total sales
monthly_sales = data.groupby('Month')['TotalAmount'].sum().reset_index()

# Plot monthly sales
plt.figure(figsize=(10, 6))
sns.lineplot(x='Month', y='TotalAmount', data=monthly_sales, marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.xticks(range(1, 13))  # Ensure all months are shown
plt.grid()
plt.show()

# Group by CustomerID and calculate metrics
customer_behavior = data.groupby('CustomerID').agg(
    TotalPurchases=('InvoiceNo', 'nunique'),  # Number of unique invoices
    TotalAmount=('TotalAmount', 'sum'),       # Total spending
    AvgOrderValue=('TotalAmount', 'mean')     # Average order value
).reset_index()

# Display top customers by total spending
print("Top Customers by Total Spending:\n", customer_behavior.sort_values(by='TotalAmount', ascending=False).head())

# Plot distribution of total purchases
plt.figure(figsize=(10, 6))
sns.histplot(customer_behavior['TotalPurchases'], bins=50, kde=True, color='blue')
plt.title('Distribution of Total Purchases per Customer')
plt.xlabel('Total Purchases')
plt.ylabel('Frequency')
plt.show()

# Group by Country and calculate total sales
sales_by_country = data.groupby('Country')['TotalAmount'].sum().reset_index()

# Sort by total sales
sales_by_country = sales_by_country.sort_values(by='TotalAmount', ascending=False)

# Plot sales by country
plt.figure(figsize=(12, 6))
sns.barplot(x='TotalAmount', y='Country', data=sales_by_country, palette='viridis')
plt.title('Total Sales by Country')
plt.xlabel('Total Sales')
plt.ylabel('Country')
plt.show()

# Group by Description (product name) and calculate total sales
sales_by_product = data.groupby('Description')['TotalAmount'].sum().reset_index()

# Sort by total sales
sales_by_product = sales_by_product.sort_values(by='TotalAmount', ascending=False)

# Display top 10 products by sales
print("Top 10 Products by Sales:\n", sales_by_product.head(10))

# Plot top 10 products
plt.figure(figsize=(12, 6))
sns.barplot(x='TotalAmount', y='Description', data=sales_by_product.head(10), palette='magma')
plt.title('Top 10 Products by Sales')
plt.xlabel('Total Sales')
plt.ylabel('Product Description')
plt.show()

# Filter data for UK customers
data_uk = data[data['Country'] == 'United Kingdom']

# Drop rows with missing CustomerID
data_uk = data_uk[data_uk['CustomerID'].notna()]

# Remove cancelled transactions
data_uk = data_uk[(data_uk['Quantity'] > 0) & (data_uk['UnitPrice'] > 0)]

from datetime import datetime

# Calculate Recency (days since last purchase)
data_uk['InvoiceDate'] = pd.to_datetime(data_uk['InvoiceDate'])
snapshot_date = data_uk['InvoiceDate'].max() + pd.Timedelta(days=1)  # Latest date in the dataset + 1 day

# Aggregate data at customer level
customer_data = data_uk.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,  # Recency
    'InvoiceNo': 'nunique',  # Frequency
    'TotalAmount': 'sum',    # Monetary Value
    'Quantity': 'sum',       # Total Quantity
}).reset_index()

# Rename columns
customer_data.rename(columns={
    'InvoiceDate': 'Recency',
    'InvoiceNo': 'Frequency',
    'TotalAmount': 'MonetaryValue',
    'Quantity': 'TotalQuantity'
}, inplace=True)

# Calculate Average Order Value (AOV)
customer_data['AOV'] = customer_data['MonetaryValue'] / customer_data['Frequency']

# Cap outliers for MonetaryValue and Frequency
monetary_cap = customer_data['MonetaryValue'].quantile(0.95)
frequency_cap = customer_data['Frequency'].quantile(0.95)

customer_data['MonetaryValue'] = customer_data['MonetaryValue'].clip(upper=monetary_cap)
customer_data['Frequency'] = customer_data['Frequency'].clip(upper=frequency_cap)

# Calculate Customer Tenure
customer_tenure = data_uk.groupby('CustomerID')['InvoiceDate'].agg(['min', 'max']).reset_index()
customer_tenure['Tenure'] = (customer_tenure['max'] - customer_tenure['min']).dt.days

# Merge Tenure with customer_data
customer_data = customer_data.merge(customer_tenure[['CustomerID', 'Tenure']], on='CustomerID', how='left')

# Calculate Purchase Frequency (average time between purchases)
customer_data['PurchaseFrequency'] = customer_data['Tenure'] / customer_data['Frequency']

customer_data['CLV'] = customer_data['AOV'] * customer_data['Frequency'] * customer_data['Tenure']

print(customer_data.describe())

import matplotlib.pyplot as plt
import seaborn as sns

# Plot distributions
plt.figure(figsize=(15, 10))

plt.subplot(2, 2, 1)
sns.histplot(customer_data['Recency'], bins=50, kde=True, color='blue')
plt.title('Distribution of Recency')

plt.subplot(2, 2, 2)
sns.histplot(customer_data['Frequency'], bins=50, kde=True, color='green')
plt.title('Distribution of Frequency')

plt.subplot(2, 2, 3)
sns.histplot(customer_data['MonetaryValue'], bins=50, kde=True, color='orange')
plt.title('Distribution of MonetaryValue')

plt.subplot(2, 2, 4)
sns.histplot(customer_data['CLV'], bins=50, kde=True, color='red')
plt.title('Distribution of CLV')

plt.tight_layout()
plt.show()

# Boxplots to check for outliers
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
sns.boxplot(customer_data['Recency'], color='blue')
plt.title('Boxplot of Recency')

plt.subplot(1, 3, 2)
sns.boxplot(customer_data['Frequency'], color='green')
plt.title('Boxplot of Frequency')

plt.subplot(1, 3, 3)
sns.boxplot(customer_data['MonetaryValue'], color='orange')
plt.title('Boxplot of MonetaryValue')

plt.tight_layout()
plt.show()

# Correlation matrix
corr_matrix = customer_data.corr()

# Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
plt.show()

# Summary statistics for CLV
print("CLV Summary:\n", customer_data['CLV'].describe())

# Plot CLV distribution
plt.figure(figsize=(8, 6))
sns.histplot(customer_data['CLV'], bins=50, kde=True, color='red')
plt.title('Distribution of CLV')
plt.xlabel('CLV')
plt.ylabel('Frequency')
plt.show()

# Display first few rows
print(customer_data.head())

from sklearn.model_selection import train_test_split

# Select features and target variable
X = customer_data[['Recency', 'Frequency', 'MonetaryValue', 'Tenure']]
y = customer_data['CLV']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.linear_model import LinearRegression

# Initialize and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, root_mean_squared_error

# Calculate evaluation metrics
mae = mean_absolute_error(y_test, y_pred)
rmse = root_mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Absolute Error (MAE):", mae)
print("Root Mean Squared Error (RMSE):", rmse)
print("R-squared (R²):", r2)

# Cap CLV at the 95th percentile
clv_cap = customer_data['CLV'].quantile(0.95)
customer_data['CLV'] = customer_data['CLV'].clip(upper=clv_cap)

# Verify the changes
print("CLV Summary After Capping:\n", customer_data['CLV'].describe())

from sklearn.preprocessing import MinMaxScaler

# Select features to scale
features_to_scale = ['Recency', 'Frequency', 'MonetaryValue', 'Tenure', 'PurchaseFrequency']

# Initialize the scaler
scaler = MinMaxScaler()

# Scale the features
customer_data[features_to_scale] = scaler.fit_transform(customer_data[features_to_scale])

# Verify the scaled features
print(customer_data[features_to_scale].head())

from sklearn.model_selection import train_test_split

# Select features and target variable
X = customer_data[['Recency', 'Frequency', 'MonetaryValue', 'Tenure', 'PurchaseFrequency']]
y = customer_data['CLV']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Verify the splits
print("Training set shape:", X_train.shape, y_train.shape)
print("Testing set shape:", X_test.shape, y_test.shape)

from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor

# Initialize the XGBoost model
xgb_model = XGBRegressor(random_state=42)

# Define the parameter grid
param_grid = {
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.2],
    'n_estimators': [100, 200, 300]
}

# Initialize Grid Search
grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid, scoring='r2', cv=3, verbose=1)

# Fit Grid Search
grid_search.fit(X_train, y_train)

# Best parameters
print("Best Parameters:", grid_search.best_params_)

# Initialize the XGBoost model with best parameters (if tuning was performed)
xgb_model = XGBRegressor(
    max_depth=grid_search.best_params_['max_depth'],
    learning_rate=grid_search.best_params_['learning_rate'],
    n_estimators=grid_search.best_params_['n_estimators'],
    random_state=42
)

# Train the model
xgb_model.fit(X_train, y_train)

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Make predictions
y_pred_xgb = xgb_model.predict(X_test)

# Calculate evaluation metrics
mae_xgb = mean_absolute_error(y_test, y_pred_xgb)
rmse_xgb = root_mean_squared_error(y_test, y_pred_xgb)
r2_xgb = r2_score(y_test, y_pred_xgb)

print("XGBoost MAE:", mae_xgb)
print("XGBoost RMSE:", rmse_xgb)
print("XGBoost R²:", r2_xgb)

from sklearn.model_selection import cross_val_score

# Perform cross-validation
cv_scores = cross_val_score(xgb_model, X, y, scoring='r2', cv=5)
print("Cross-Validation R² Scores:", cv_scores)
print("Mean Cross-Validation R²:", cv_scores.mean())

import shap

# Initialize SHAP explainer
explainer = shap.TreeExplainer(xgb_model)
shap_values = explainer.shap_values(X)

# Plot SHAP summary
shap.summary_plot(shap_values, X)

import matplotlib.pyplot as plt
import seaborn as sns

# Create a DataFrame for visualization
results_df = pd.DataFrame({
    'MonetaryValue': X_test['MonetaryValue'],  # Use the original (unscaled) values if needed
    'Actual_CLV': y_test,
    'Predicted_CLV': y_pred
})

plt.figure(figsize=(12, 6))
sns.scatterplot(x='MonetaryValue', y='Actual_CLV', data=results_df, color='blue', label='Actual CLV', alpha=0.6)
sns.scatterplot(x='MonetaryValue', y='Predicted_CLV', data=results_df, color='red', label='Predicted CLV', alpha=0.6)
plt.xlabel('MonetaryValue')
plt.ylabel('CLV')
plt.title('MonetaryValue vs. Actual & Predicted CLV')
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
sns.regplot(x='MonetaryValue', y='Actual_CLV', data=results_df, color='blue', label='Actual CLV', scatter_kws={'alpha':0.3})
sns.regplot(x='MonetaryValue', y='Predicted_CLV', data=results_df, color='red', label='Predicted CLV', scatter_kws={'alpha':0.3})
plt.xlabel('MonetaryValue')
plt.ylabel('CLV')
plt.title('Regression: MonetaryValue vs. CLV')
plt.legend()
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Actual CLV
sns.scatterplot(x='MonetaryValue', y='Actual_CLV', data=results_df, ax=axes[0], color='blue', alpha=0.6)
axes[0].set_title('MonetaryValue vs. Actual CLV')

# Predicted CLV
sns.scatterplot(x='MonetaryValue', y='Predicted_CLV', data=results_df, ax=axes[1], color='red', alpha=0.6)
axes[1].set_title('MonetaryValue vs. Predicted CLV')

plt.show()

# Add predicted CLV to the dataset
customer_data['CLV_Predicted'] = xgb_model.predict(X)

# Define the threshold (e.g., 75th percentile)
clv_threshold = customer_data['CLV_Predicted'].quantile(0.75)

# Create the binary target variable
customer_data['HighValue'] = (customer_data['CLV_Predicted'] > clv_threshold).astype(int)

# Display the distribution of high-value vs. low-value customers
print("High-Value Customers:", customer_data['HighValue'].sum())
print("Low-Value Customers:", len(customer_data) - customer_data['HighValue'].sum())

from sklearn.model_selection import train_test_split

# Select features and target variable
X_class = customer_data[['Recency', 'Frequency', 'MonetaryValue', 'Tenure', 'PurchaseFrequency']]
y_class = customer_data['HighValue']

# Split the data
X_train_class, X_test_class, y_train_class, y_test_class = train_test_split(X_class, y_class, test_size=0.2, random_state=42)

# Verify the splits
print("Training set shape:", X_train_class.shape, y_train_class.shape)
print("Testing set shape:", X_test_class.shape, y_test_class.shape)

from sklearn.ensemble import RandomForestClassifier

# Initialize the Random Forest model
rf_model = RandomForestClassifier(random_state=42)

# Train the model
rf_model.fit(X_train_class, y_train_class)

from sklearn.metrics import classification_report, confusion_matrix

# Make predictions
y_pred_class = rf_model.predict(X_test_class)

# Generate classification report
print("Classification Report:\n", classification_report(y_test_class, y_pred_class))

# Generate confusion matrix
conf_matrix = confusion_matrix(y_test_class, y_pred_class)
print("Confusion Matrix:\n", conf_matrix)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create a DataFrame for plotting
plot_data = pd.DataFrame({
    'MonetaryValue': X_test_class['MonetaryValue'],
    'Actual_HighValue': y_test_class,
    'Predicted_HighValue': y_pred_class
})

# Get predicted probabilities instead of binary predictions
y_proba = rf_model.predict_proba(X_test_class)[:, 1]
plot_data['Predicted_Probability'] = y_proba

# Plot probability curve
plt.figure(figsize=(12, 6))
sns.regplot(x='MonetaryValue', y='Actual_HighValue', data=plot_data,
            logistic=True, scatter_kws={'alpha':0.3})
sns.regplot(x='MonetaryValue', y='Predicted_Probability', data=plot_data,
            logistic=True, scatter_kws={'alpha':0.3})
plt.xlabel('MonetaryValue')
plt.ylabel('Predicted Probability of HighValue')
plt.title('Probability Curve by MonetaryValue')
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. First verify your data
print("Data sample:")
print(plot_data[['MonetaryValue', 'Actual_HighValue', 'Predicted_Probability']].head())

# 2. Create a clean figure with proper sizing
plt.figure(figsize=(12, 6), dpi=100)  # Clear any existing figures

# 3. Plot actual binary values with jitter
y_jitter = plot_data['Actual_HighValue'] + np.random.normal(0, 0.05, size=len(plot_data))
plt.scatter(plot_data['MonetaryValue'], y_jitter,
            c='black', alpha=0.5, s=30, label='Actual (Binary)')

# 4. Plot predicted probabilities
sns.regplot(x='MonetaryValue', y='Predicted_Probability', data=plot_data,
            logistic=True, scatter_kws={'alpha':0.3, 'color':'red'},
            line_kws={'color':'red', 'lw':2}, label='Predicted Probability')

# 5. Add proper labels and formatting
plt.xlabel('MonetaryValue', fontsize=12)
plt.ylabel('HighValue Probability', fontsize=12)
plt.title('Random Forest Classification: Actual vs Predicted', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

# 6. Ensure proper display
plt.tight_layout()
plt.show()

# Add predicted high/low value labels to the dataset
customer_data['Predicted_HighValue'] = rf_model.predict(X_class)

# Segment customers
high_value_customers = customer_data[customer_data['Predicted_HighValue'] == 1]
low_value_customers = customer_data[customer_data['Predicted_HighValue'] == 0]

# Display segment sizes
print("High-Value Customers:", len(high_value_customers))
print("Low-Value Customers:", len(low_value_customers))

import seaborn as sns
import matplotlib.pyplot as plt

# Create a heatmap of the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Predicted Low', 'Predicted High'],
            yticklabels=['Actual Low', 'Actual High'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix Heatmap')
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. Prepare the plot
plt.figure(figsize=(12, 6))

# 2. Add actual binary values with jitter
jitter_amount = 0.05
y_jittered = y_test_class + np.random.uniform(-jitter_amount, jitter_amount, size=len(y_test_class))
plt.scatter(X_test_class['MonetaryValue'], y_jittered,
            alpha=0.5, color='blue', label='Actual (Binary)')

# 3. Add predicted probabilities
y_proba = rf_model.predict_proba(X_test_class)[:, 1]
sns.regplot(x=X_test_class['MonetaryValue'], y=y_proba,
            logistic=True, scatter=False,
            line_kws={'color':'red', 'lw':2},
            label='Predicted Probability')

# 4. Add formatting
plt.xlabel('MonetaryValue', fontsize=12)
plt.ylabel('HighValue Probability', fontsize=12)
plt.title('Random Forest Classification: Actual vs Predicted', fontsize=14)
plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
plt.grid(True, alpha=0.3)
plt.legend(loc='best')

# 5. Show plot
plt.tight_layout()
plt.show()

# Select features for clustering
X_cluster = customer_data[['Recency', 'Frequency', 'MonetaryValue', 'Tenure', 'PurchaseFrequency']]

# Scale the features (KNN is sensitive to feature scales)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_cluster_scaled = scaler.fit_transform(X_cluster)

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Calculate the Within-Cluster-Sum-of-Squares (WCSS) for different values of k
wcss = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_cluster_scaled)
    wcss.append(kmeans.inertia_)

# Plot the Elbow Method
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), wcss, marker='o', linestyle='--')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('WCSS')
plt.title('Elbow Method for Optimal k')
plt.show()

from sklearn.neighbors import NearestNeighbors

# Initialize KNN
knn = NearestNeighbors(n_neighbors=5)  # Adjust n_neighbors as needed

# Fit the model
knn.fit(X_cluster_scaled)

# Find the nearest neighbors for each customer
distances, indices = knn.kneighbors(X_cluster_scaled)

# Add cluster labels to the dataset
customer_data['Cluster'] = knn.kneighbors(X_cluster_scaled, return_distance=False)[:, 0]  # Example: Use the first neighbor as the cluster label

cluster_summary = customer_data.groupby('Cluster').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'MonetaryValue': 'mean',
    'Tenure': 'mean',
    'PurchaseFrequency': 'mean',
    'CLV_Predicted': 'mean'
}).round(2)

print(cluster_summary)

import seaborn as sns
import matplotlib.pyplot as plt

# Select 3 most important features for clarity
features = ['MonetaryValue', 'Frequency', 'Recency']
sns.pairplot(customer_data,
             vars=features,
             hue='Cluster',
             palette='viridis',
             plot_kws={'s': 30, 'alpha': 0.7, 'edgecolor': 'k'},
             height=3)
plt.suptitle('Customer Cluster Relationships', y=1.02)
plt.show()

from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

scatter = ax.scatter(customer_data['MonetaryValue'],
                    customer_data['Frequency'],
                    customer_data['Recency'],
                    c=customer_data['Cluster'],
                    cmap='viridis',
                    s=50,
                    alpha=0.7,
                    edgecolor='k')

ax.set_xlabel('MonetaryValue')
ax.set_ylabel('Frequency')
ax.set_zlabel('Recency')
plt.title('3D View of Customer Clusters', pad=20)
fig.colorbar(scatter, ax=ax, label='Cluster')
plt.tight_layout()
plt.show()