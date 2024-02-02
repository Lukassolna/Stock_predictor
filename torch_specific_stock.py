import torch
import torch.nn as nn
import os  # Import os module to handle file paths
from torch_RNNmodel import RNNModel  # Assuming this is your custom module
from new_stock_attempt import dfs
from global_var import omx
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def predict_change_for_specific_stock(stock):
    combined_data = []
    index = omx.index(stock)
    df = dfs[index]
    combined_data.extend(zip(df['Change'].tolist(), df['RSI'].tolist(), df['10_change'].tolist()))
    
    def create_sequences(data, sequence_length):
        sequences = []
        targets = []
        for i in range(len(data) - sequence_length):
            seq = data[i:i+sequence_length]
            target = data[i+sequence_length][0]  # The target is the 'Change' value
            sequences.append([item for item in seq])
            targets.append(target)
        return torch.tensor(sequences, dtype=torch.float32), torch.tensor(targets, dtype=torch.float32)

    train_data = combined_data
    test_data = combined_data[int(len(combined_data) * 0.98):]
    sequence_length = 4

    train_sequences, train_targets = create_sequences(train_data, sequence_length)
    test_sequences, test_targets = create_sequences(test_data, sequence_length)

    # Generate a stock-specific model path
    model_path = f'saved_models/model_{stock}.pth'

    # Check if a model for the specific stock already exists
    if os.path.exists(model_path):
        # Load the model
        model = RNNModel(input_size=3, hidden_size=1000, num_layers=3, output_size=1)
        model.load_state_dict(torch.load(model_path))
        model.eval()  # Make sure to set the model to evaluation mode
        print(f"Model for {stock} loaded.")
    else:
        # If the model doesn't exist, proceed with training a new one
        model = RNNModel(input_size=3, hidden_size=1000, num_layers=3, output_size=1)
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

        num_epochs = 20
        for epoch in range(num_epochs):
            model.train()
            optimizer.zero_grad()
            outputs = model(train_sequences)
            loss = criterion(outputs, train_targets.unsqueeze(-1).view(-1, 1))
            loss.backward()
            optimizer.step()
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')
        
        # Save the trained model
        torch.save(model.state_dict(), model_path)
        print(f"Model for {stock} trained and saved.")

    def predict_next_change(model, df, sequence_length):
        data = list(zip(df['Change'].tolist(), df['RSI'].tolist(), df['10_change'].tolist()))
        last_sequence = data[-sequence_length:]
        last_sequence_tensor = torch.tensor([last_sequence], dtype=torch.float32)
        model.eval()
        with torch.no_grad():
            predicted_change = model(last_sequence_tensor).item()
        return predicted_change

    predicted_change = predict_next_change(model, df, sequence_length)
    return predicted_change
