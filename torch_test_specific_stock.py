import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from torch_RNNmodel import RNNModel  # Assuming this is your custom module
from new_stock_attempt import dfs
from global_var import omx
from sklearn.preprocessing import MinMaxScaler
import numpy as np



combined_data = []
index = omx.index('HM-B.ST')
df=dfs[index]
combined_data.extend(zip(df['Change'].tolist(), df['RSI'].tolist(),df['10_change'].tolist()))
scaler = MinMaxScaler()
#combined_data = scaler.fit_transform(combined_data)
def create_sequences(data, sequence_length):
    sequences = []
    targets = []
    for i in range(len(data) - sequence_length):
        seq = data[i:i+sequence_length]
        target = data[i+sequence_length][0]  # The target is the 'Change' value
        sequences.append([item for item in seq])
        targets.append(target)
    return torch.tensor(sequences, dtype=torch.float32), torch.tensor(targets, dtype=torch.float32)



train_data = combined_data[:int(len(combined_data) * 0.7)]
test_data = combined_data[-30:]

sequence_length = 4  



train_sequences, train_targets = create_sequences(train_data, sequence_length)
test_sequences, test_targets = create_sequences(test_data, sequence_length)


model = RNNModel(input_size=3, hidden_size=1000, num_layers=3, output_size=1)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 20  
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()
    outputs = model(train_sequences)
    loss = criterion(outputs, train_targets.unsqueeze(-1).view(-1, 1))  # Reshape targets to match output
    loss.backward()
    optimizer.step()
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')


def predict_next_change(model, df, sequence_length):
    
    data = list(zip(df['Change'].tolist(), df['RSI'].tolist(), df['10_change'].tolist()))
    # Get the last elements
    last_sequence = data[-sequence_length:]
    # Convert to tensor
    last_sequence_tensor = torch.tensor([last_sequence], dtype=torch.float32)
    # Predict
    model.eval()
    with torch.no_grad():
        predicted_change = model(last_sequence_tensor).item()

    return predicted_change
# Testing 
predicted_change = predict_next_change(model, df, sequence_length)
print(f"Predicted Change for the next day: {predicted_change}") 
def test():
    model.eval()
    test_losses = []
    actuals = []
    predictions = []

    with torch.no_grad():
        for i in range(len(test_sequences)):
            input_seq = test_sequences[i].unsqueeze(0)  # No need for unsqueeze(-1)
            target = test_targets[i]
            output = model(input_seq)
            loss = criterion(output, target.view(-1, 1))  # Reshape target to match output
            test_losses.append(loss.item())
            actuals.append(target.item())
            predictions.append(output.item())

   

    average_test_loss = sum(test_losses) / len(test_losses)
    print(f'Average Test Loss: {average_test_loss:.4f}')
    print(actuals)
    print(predictions)
    # Plot function to visualize results vs predictions
    def plot():
        plt.ion()  
        plt.figure(figsize=(12, 6))
        plt.plot(actuals, label='Actual')
        plt.plot(predictions, label='Predicted')
        plt.title('Test Actual vs Test Predicted')
        plt.xlabel('Sample')
        plt.ylabel('Value')
        plt.legend()
        plt.show(block=True) 

    plot()
test()