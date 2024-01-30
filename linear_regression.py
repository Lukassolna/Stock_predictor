import pandas as pd
from sklearn.linear_model import LinearRegression
from new_stock_attempt import dfs

dfs_train=dfs
# Concatenate all dataframes in the list
df_all = pd.concat(dfs_train, ignore_index=True)
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


df_test = dfs[0]

# Independent variables for the test set
X_test = df_test[['RSI', 'Change', '10_change', 'percentage_diff']]

# Dependent variable for the test set
y_test = df_test['next_day_change']

# Use the model to make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model (optional)
# You can use metrics like mean squared error, mean absolute error, etc.
from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")