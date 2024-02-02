import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from new_stock_attempt import dfs

## this is not courrently being used at all for our model, but was a first attempt at tensorflow.
## Can be ignored
df_all = pd.concat(dfs, ignore_index=True)

X = df_all[['RSI', 'Change', '10_change', 'percentage_diff']]


y = df_all['next_day_change']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(X_train, y_train, epochs=1, batch_size=32, validation_split=0.2, verbose=2)


y_pred = model.predict(X_test)


average_y_test = sum(y_test) / len(y_test)
y_pred_average = [average_y_test] * len(y_test)
# evaluate based on mse
mse_average = mean_squared_error(y_test, y_pred_average)
print(mse_average)

mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error with TensorFlow model: {mse}")
