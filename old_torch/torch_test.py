from torch_RNNmodel import RNNModel
from torch_changeDataset import ChangeDataset
import torch.nn as nn
import torch
from new_stock_attempt import dfs
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

# Initialize dataset and dataloader

def collate_fn(batch):
    return torch.nn.utils.rnn.pad_sequence(batch, batch_first=True, padding_value=0)

# Assuming `dfs` contains 30 stocks
train_dfs = dfs[1:10]  # Use the first 28 stocks for training
test_dfs = dfs[1:10]   # Use the last 2 stocks for testing

train_dataset = ChangeDataset(train_dfs)
train_dataloader = DataLoader(train_dataset, batch_size=10, shuffle=True, collate_fn=collate_fn)
# Print first few samples from ChangeDataset
print("Sample data from ChangeDataset:")
for i in range(min(5, len(train_dataset))):  # Print first 5 samples
    sample = train_dataset[i]
    print(f"Sample {i}: {sample}")
# Print first few batches from DataLoader
print("Sample batches from DataLoader:")
for i, batch in enumerate(train_dataloader):
    if i >= 2:  # Print only first 2 batches
        break
    print(f"Batch {i}: {batch}")

test_dataset = ChangeDataset(test_dfs)
test_dataloader = DataLoader(test_dataset, batch_size=10, shuffle=False, collate_fn=collate_fn)

model = RNNModel(input_size=1, hidden_size=100, num_layers=2, output_size=1)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 10
for epoch in range(num_epochs):
    model.train()  # Set the model to training mode
    for batch in train_dataloader:
        # Assuming batch is of shape (batch_size, sequence_length)
        # and you want to predict the next value in the sequence
       # For one-step prediction
        inputs = batch[:, :-1]  # All but the last element as input
        targets = batch[:, -1].unsqueeze(-1)  # Only the last element as target
        # Forward pass
        inputs = inputs.unsqueeze(-1)  # Add an extra dimension

        outputs = model(inputs)
        loss = criterion(outputs, targets)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Optionally print the loss
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

model.eval()  # Set the model to evaluation mode
test_losses = []
actuals = []
predictions = []

with torch.no_grad():
    for i,batch in enumerate(test_dataloader):
        inputs = batch[:, :-1]  # All but the last element as input
        targets = batch[:, -1].unsqueeze(-1)  # Only the last element as target
        inputs = inputs.unsqueeze(-1)  # Add an extra dimension

        outputs = model(inputs)
        loss = criterion(outputs, targets)
        test_losses.append(loss.item())
        if i < 3:  # print first three samples
            print(f'Inputs: {inputs}')
            print(f'Predicted: {outputs}')
            print(f'Actual: {targets}')
            print('---')

        # Store actual and predicted values for plotting
        actuals.extend(targets.squeeze(-1).tolist())
        predictions.extend(outputs.squeeze(-1).tolist())

average_test_loss = sum(test_losses) / len(test_losses)
print(f'Average Test Loss: {average_test_loss:.4f}')

# Plotting test actual vs test predicted
plt.figure(figsize=(12, 6))
plt.plot(actuals, label='Actual')
plt.plot(predictions, label='Predicted')
plt.title('Test Actual vs Test Predicted')
plt.xlabel('Sample')
plt.ylabel('Value')
plt.legend()
plt.show()