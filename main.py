# ==============================
# IMPORT LIBRARIES
# ==============================
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os
import time

# ==============================
# USER INPUT
# ==============================
file_name = input("Enter dataset file name (example: retail_data.csv): ")

if not os.path.exists(file_name):
    print("❌ Dataset file not found.")
    exit()

print("\n✅ ML system started. Monitoring dataset for changes...\n")

last_modified = -1

# ==============================
# CONTINUOUS ML MONITORING
# ==============================
while True:
    current_modified = os.path.getmtime(file_name)

    if current_modified != last_modified:
        print("🔄 Dataset changed. Re-training ML models...\n")
        last_modified = current_modified

        # ==============================
        # LOAD DATA
        # ==============================
        df = pd.read_csv(file_name)

        # ==============================
        # DATE PROCESSING (ML NUMERIC FORM)
        # ==============================
        df['Expiry_Date'] = pd.to_datetime(df['Expiry_Date'], errors='coerce')
        current_time = pd.Timestamp.now()
        df['Days_To_Expiry'] = (df['Expiry_Date'] - current_time).dt.days

        # ==============================
        # DROP NON-ML COLUMNS
        # ==============================
        df_ml = df.drop(['Product', 'Expiry_Date'], axis=1)

        # ==============================
        # ENCODE CATEGORICAL FEATURES
        # ==============================
        le = LabelEncoder()
        for col in df_ml.select_dtypes(include='object').columns:
            df_ml[col] = le.fit_transform(df_ml[col].astype(str))

        df_ml.fillna(0, inplace=True)

        # ==============================
        # RANDOM FOREST REGRESSION
        # ==============================
        X_reg = df_ml.drop('Daily_Sales', axis=1)
        y_reg = df_ml['Daily_Sales']

        rf_reg = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )
        rf_reg.fit(X_reg, y_reg)

        df['Predicted_Sales'] = rf_reg.predict(X_reg).round(2)

        # ==============================
        # RANDOM FOREST CLASSIFICATION
        # ==============================
        median_sales = df['Daily_Sales'].median()
        df['Demand_Label'] = (df['Daily_Sales'] > median_sales).astype(int)

        X_clf = df_ml.drop('Daily_Sales', axis=1)
        y_clf = df['Demand_Label']

        rf_clf = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
        rf_clf.fit(X_clf, y_clf)

        df['Predicted_Demand'] = rf_clf.predict(X_clf)

        # ==============================
        # LOW STOCK FLAG (ML-DERIVED)
        # ==============================
        df['Low_Stock_Flag'] = (df['Predicted_Sales'] > df['Stock']).astype(int)

        # ==============================
        # FINAL PURE ML OUTPUT
        # ==============================
        ml_output = df[
            ['ID',
             'Predicted_Sales',
             'Predicted_Demand',
             'Low_Stock_Flag',
             'Days_To_Expiry']
        ]

        print("✅ ML OUTPUT (Pure Predictions):\n")
        print(ml_output)

        ml_output.to_csv("ml_output.csv", index=False)
        print("\n📁 ML output saved as ml_output.csv\n")

    time.sleep(5)