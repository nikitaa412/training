import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score
import pickle
import os

# Load data
df = pd.read_csv('data/generate_data.csv')

# Encode location
le = LabelEncoder()
df['location'] = le.fit_transform(df['location'])

with open('model/feature_names.pkl', 'wb') as f:
    pickle.dump(X.columns.tolist(), f)

# Save encoder
with open('model/location_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)

# Features and target
X = df[['location', 'sqft', 'beds', 'baths', 'year_built']]
y = df['price']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)

# Save model and R2 score
with open('model/house_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('model/r2_score.txt', 'w') as f:
    f.write(f"R^2 Score: {r2:.4f}")
