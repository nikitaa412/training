import pandas as pd
import numpy as np
import os

# Set seed for reproducibility
np.random.seed(42)

# Create synthetic dataset
n_samples = 100
sqft = np.random.randint(500, 5000, n_samples)
beds = np.random.randint(1, 7, n_samples)
baths = np.random.randint(1, 6, n_samples)
year_built = np.random.randint(1950, 2024, n_samples)

# Add location choices
locations = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
location = np.random.choice(locations, n_samples)

# Generate prices
base_price = sqft * 200 + beds * 10000 + baths * 15000
age_penalty = (2025 - year_built) * 500
noise = np.random.normal(0, 20000, n_samples)
price = base_price - age_penalty + noise

# Create DataFrame
df = pd.DataFrame({
    'location': location,
    'sqft': sqft,
    'beds': beds,
    'baths': baths,
    'year_built': year_built,
    'price': price.astype(int)
})

# Save to CSV
os.makedirs("data", exist_ok=True)
df.to_csv("data/generate_data.csv", index=False)
print("✅ Dataset saved as 'data/generate_data.csv'")