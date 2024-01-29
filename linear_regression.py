import pandas as pd
from sklearn.linear_model import LinearRegression
from main import dfs
# Concatenate all dataframes in the list
df_all = pd.concat(dfs, ignore_index=True)
# Independent variables
X = df_all[['RSI', 'Change', '10_change', 'percentage_diff']]

# Dependent variable
y = df_all['next_day_change']

# Create a linear regression model
model = LinearRegression()

# Fit the model
model.fit(X, y)

# Get the coefficients
coefficients = model.coef_

# Print the coefficients
for i, col in enumerate(X.columns):
    print(f"Coefficient for {col}: {coefficients[i]}")
