import pandas as pd
from sklearn.linear_model import LinearRegression
from new_stock_attempt import dfs

dfs_train=dfs
# Concatenate all dataframes in the list
df_all = pd.concat(dfs_train, ignore_index=True)

X = df_all[['RSI', 'Change', '10_change', 'percentage_diff']]


y = df_all['next_day_change']


model = LinearRegression()


model.fit(X, y)


coefficients = model.coef_

with open('coefficients.txt', 'w') as txt_file:
    for coefficient in coefficients:
        txt_file.write(f"{coefficient}\n")

def testing_mse():


    df_test = dfs[0]
   
    X_test = df_test[['RSI', 'Change', '10_change', 'percentage_diff']]

   
    y_test = df_test['next_day_change']

    y_pred = model.predict(X_test)

    # Evaluate the model
  
    from sklearn.metrics import mean_squared_error
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")