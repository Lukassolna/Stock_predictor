import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from new_stock_attempt import dfs

import numpy as np


coefficients_list = []
mse_list = []

train_df=dfs[:-1]
for df in train_df:
    X = df[['RSI', 'Change', '10_change', 'percentage_diff']]
    y = df['next_day_change']
    
    # model setup wwith parameters
    model = LinearRegression()
    model.fit(X, y)
    
    
    coefficients_list.append(model.coef_)
    
   
    y_pred = model.predict(X)
    mse = mean_squared_error(y, y_pred)
    mse_list.append(mse)


average_coefficients = sum(coefficients_list) / len(coefficients_list)

# Calculating average coefficients
average_coefficients = np.mean(coefficients_list, axis=0)




#test begins here

test_data=dfs[-1]
X_test = test_data[['RSI', 'Change', '10_change', 'percentage_diff']]
y_test = test_data['next_day_change']


y_pred_manual = np.dot(X_test, average_coefficients) 

mse_manual = mean_squared_error(y_test, y_pred_manual)
print(f"MSE for model with average coefficients: {mse_manual}")


y_mean = np.mean(y_test)
y_baseline_pred = np.full_like(y_test, y_mean)

mse_baseline = mean_squared_error(y_test, y_baseline_pred)
print(f"MSE for baseline model: {mse_baseline}")
