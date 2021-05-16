import argparse
import numpy as np
from machine import WIDTH, train_model

parser = argparse.ArgumentParser(description='Main file')
parser.add_argument("--data", type=str)
parser.add_argument("--model")

args = parser.parse_args()


if args.model is not None:
    new_model = neuronal_network_model(WIDTH)
    new_model.load(args.model)
    model = new_model

elif args.data is not None:
    training_data = np.load(args.data, allow_pickle=True)
    training_data = training_data.tolist()
    print(training_data)
    model = train_model(training_data)




