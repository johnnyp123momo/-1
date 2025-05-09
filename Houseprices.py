import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# 讀取資料
file_path = "Taipei_house.csv"
df = pd.read_csv(file_path)

# 過濾不合理資料
df = df[df["建物總面積"] > 0]

# 加入新特色欄位：每坪單價
df["每坪單價"] = df["總價"] / df["建物總面積"]

# 特徵欄位與目標欄位
features = [
    "行政區", "土地面積", "建物總面積", "屋齡", "樓層", "總樓層",
    "房數", "廳數", "衛數", "電梯", "車位類別", "經度", "緯度", "每坪單價"
]
target = "總價"

X = df[features]
y = df[target]

# 前處理：類別欄位獨熱編碼
categorical_features = ["行政區", "車位類別"]
numeric_features = list(set(features) - set(categorical_features))

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ],
    remainder="passthrough"
)

# 建立模型管線
model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

# 切分資料集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 訓練模型
model.fit(X_train, y_train)

# 預測與評估
y_pred = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))

# 儲存模型
joblib.dump(model, "taipei_house_price_model.pkl")
print("模型已儲存為 taipei_house_price_model.pkl")
