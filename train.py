from net import Net
import numpy as np
import argparse
import torch
import torch.nn as nn

# Loss and optimizier 
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from create_data import initial_population

class DatasetValue(Dataset):
    def __init__(self, data):
        print(type(data))
        self.X = data["arr_0"]
        print(self.X)
        self.Y = data["arr_1"]

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):
        return (self.X[idx], self.Y[idx])


def train(dataset=[]):
    EPOCHS = 5
    BATCH_SIZE = 256

    model = Net()
    if device == "cuda":
        model.cuda()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters())

    if len(dataset) == 0:
        print("creating data")
        trainset = initial_population()
    else:
        trainset = dataset

    trainsetXY = DatasetValue(trainset)
    train_loader = DataLoader(trainsetXY, batch_size=256, shuffle=True, drop_last=True)
    model.train()

    for epoch in range(EPOCHS):
        running_loss = 0.0
        print(f"{epoch + 1} / {EPOCHS}")
        for i, (data, target) in enumerate(train_loader, 0):
            target = target.unsqueeze(-1)
            if device == "cuda":
                data, target = data.to(device), target.to(device)
            data, target = data.to(torch.float32), target.to(torch.float32)

            optimizer.zero_grad()
            data = data.reshape([256, 1, 8, 8])
            outputs = model(data)
            outputs = outputs.reshape([256, 64, 1])

            loss = criterion(outputs, target)
            loss.backward()
            optimizer.step()

            # running_loss += loss.time()

            # if i % 2000 == 1999:
                # print('[%d, %5d] loss: %.3f' %
                      # (epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0
    torch.save(model.state_dict(), "models/value.pth")
    print("Finished training")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", help="display a square of a given number", type=str)
    args = parser.parse_args()
    device = "cuda"



    if args.data is not None:
        data = np.load(args.data, allow_pickle=True)
        train(data)
    else:
        train()


