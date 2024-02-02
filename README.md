# Project Title: AI-Powered Stock Predictor

## Description
This project is an AI-powered stock prediction web application. It uses machine learning models to forecast stock prices, employing Python for data analysis and machine learning, SQL for data storage, and JavaScript, Flask, HTML, and CSS to create a simple lightweight web interface.

## Technologies Used
- **Python**: For AI model development and backend logic. Some of the main libraries used are:
  - **psycopg2**: For interaction with our PostgreSQL database.
  - **pandas, numpy**: Standard data processing and data manipulation.
  - **sklearn, Pytorch**: Machine learning and optimization.
- **Yahoo finance API**: To retrieve stock data.
- **SQL**: To store stock data in a secure way with fast access to be used for training our model (Mostly just to familiarize with SQL and transactions).
- **JavaScript**: To add interactivity to the web pages.
- **Flask**: A lightweight web framework for Python.
- **HTML & CSS**: For structuring and styling the web pages.

Each stock is evaluated based on a model developed with a recurrent neural network which utilizes past performance to predict next day performance.

## Disclaimer
This is solely a for-fun project, and stocks were chosen mainly to have access to large datasets for our training data. The information provided in this application is for educational and informational purposes only and should not be construed as financial advice.
