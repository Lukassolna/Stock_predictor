# Project Title: AI-Powered Stock Predictor

## Table of Contents
- [Description](#description)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [Disclaimer](#disclaimer)
## Description
This project is an AI-powered stock prediction web application. It uses machine learning models to forecast stock prices, utilizing Python for data analysis and machine learning, SQL for data storage, and JavaScript, Flask, HTML, and CSS to create a simple lightweight web interface.

## Technologies Used
- **Python**: For AI model development and backend logic. Some of the main libraries used are:
  - **sklearn, Pytorch**: Machine learning and optimization.
  - **psycopg2**: For interaction with our PostgreSQL database.
  - **pandas, numpy**: Standard data processing and data manipulation.
 
- **Yahoo finance API**: To retrieve stock data.
- **SQL**: To store stock data in a secure way with fast access to be used for training our model (Mostly just to familiarize with SQL and transactions).
- **JavaScript**: To add interactivity to the web pages.
- **Flask**: A lightweight web framework for Python.
- **HTML & CSS**: For structuring and styling the web pages.

Each stock is evaluated based on a model developed with a recurrent neural network which utilizes past performance to predict next day performance.

## Setup and Installation
Follow these steps to set up the AI-Powered Stock Predictor application on your local machine:

1. **Clone the Repository**
   git clone https://github.com/Lukassolna/PROJECT
   cd PROJECT
3. 2. **Set Up a Virtual Environment**
- For Windows:
  ```
  python -m venv venv
  .\venv\Scripts\activate
  ```
- For macOS and Linux:
  ```
  python3 -m venv venv
  source venv/bin/activate
  ```
  

3. **Install Dependencies**
     ```
     pip install -r requirements.txt
     ```

## Running the Application
   ```
      python app.py
   ```

3. **Access the Web Interface**
- Open a web browser and navigate to
   ```
  http://127.0.0.1:5000/
    ```


## Disclaimer
This is solely a for-fun project, and stocks were chosen mainly to have access to large datasets for our training data. The information provided in this application is for educational and informational purposes only and should not be construed as financial advice.
