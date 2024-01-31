import torch
from torch.utils.data import Dataset, DataLoader
from new_stock_attempt import dfs
class ChangeDataset(Dataset):
    def __init__(self, dataframes):
        self.data = [df['Change'].values for df in dataframes]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return torch.tensor(self.data[idx], dtype=torch.float32)

def collate_fn(batch):
    # Custom collate function to handle variable-length sequences
    return torch.nn.utils.rnn.pad_sequence(batch, batch_first=True, padding_value=0)

