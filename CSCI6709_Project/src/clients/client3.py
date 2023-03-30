# -*- coding: utf-8 -*-
"""CSCI6709_LocalModel_client1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nEHbpSGR5KnuMqQ7PoF0GCbJ7LA3oAxk
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, ConfusionMatrixDisplay
from sklearn.utils import Bunch
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from datetime import datetime
import os

# Print python version
import sys
print("Python version")
print (sys.version)
print("Version info.")
print (sys.version_info)

# Function to read the csv file, return a pandas dataframe
def read_csv_files(path_name):
    df_ori = pd.read_csv(path_name)
    return df_ori

# # Achieve list of name for all csv files
# g = os.walk("/content/drive/MyDrive/dataset/N-BaIoT/ProcessedDataset")
# file_path_list = []
# df_processed_list = []
# for path,dir_list,file_list in g:
#     file_list.sort()
#     for j in range(len(file_list)):
#         print(file_list[j])
#         df_processed = read_csv_files("/content/drive/MyDrive/dataset/N-BaIoT/ProcessedDataset/" + file_list[j])
#         df_processed_list.append(df_processed)

# df_processed_list[0]

df_processed = read_csv_files("../../dataset/Processed_Dataset/client3_processed.csv")
df_processed

# Split the dataframe to train and test for each client the ratio is 80% for training and 20% for testing

df_client_train_ori, df_client_test_ori = train_test_split(df_processed, train_size=0.8, random_state=42, stratify=df_processed['target'])

df_client_test = df_client_test_ori.reset_index(drop=True)

df_client_train_ori

# For traning dataset drop the data belong the the specific target to simulate unknown attack
# (Traning does not no the target but testing we will test it)

df_client_train = df_client_train_ori[df_client_train_ori['target'] != 0].reset_index(drop=True)
df_client_train

plt.subplot(2, 2, 1)
plt.title("Train label distribution client1", fontsize=10)
df_client_train.groupby('target').size().plot(kind='pie', autopct='%.2f', figsize=(10,10))
plt.subplots_adjust(left=0.1, right=1.0, top=0.9, bottom=0.1)

plt.subplot(2, 2, 2)
plt.title("Test label distribution client1", fontsize=10)
df_client_test.groupby('target').size().plot(kind='pie', autopct='%.2f', figsize=(5,5))

# Class to create own customelized dataset
import torch
class build_torch_dataset:
    def __init__(self, data, targets):
        self.data = data
        self.targets = targets

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        current_sample = self.data[idx, :]
        current_target = self.targets[idx]
        return (torch.tensor(current_sample, dtype=torch.float), torch.tensor(current_target, dtype=torch.long))

# Convert dataframe to the torch dataset
def covert_df_to_torch_dataset(df):

    # Extra the features and the targets
    df_data = df.iloc[:, 0: len(df.columns) - 1]
    df_target= df.iloc[:, len(df.columns) - 1: len(df.columns)]

    # Covert the dataframe to numpy array first
    ds_torch_data = df_data.to_numpy()
    ds_torch_target = df_target.to_numpy()
    
    # Covert labels from 2D to 1D
    ds_torch_target_list = ds_torch_target.tolist()
    ds_torch_target_1D = []
    for i in range(len(ds_torch_target_list)):
        ds_torch_target_1D = np.append(ds_torch_target_1D, ds_torch_target_list[i][0])

    ds_torch = build_torch_dataset(ds_torch_data, ds_torch_target_1D)
    return ds_torch

ds_torch_train_client = covert_df_to_torch_dataset(df=df_client_train)
ds_torch_test_client = covert_df_to_torch_dataset(df=df_client_test)

ds_torch_test_client

train_loader_client = torch.utils.data.DataLoader(ds_torch_train_client, batch_size = 12, drop_last=True)
test_loader_client = torch.utils.data.DataLoader(ds_torch_test_client, batch_size = 12, drop_last=True)

train_loader_client

import torch.nn as nn
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(115, 100),
            nn.ReLU(),
            nn.Linear(100, 100),
            nn.ReLU(),
            nn.Linear(100, 100),
            nn.ReLU(),
            nn.Linear(100, 100),
            nn.ReLU(),
            nn.Linear(100, 100),
            nn.ReLU(),
            nn.Linear(100, 5),
            nn.Softmax(dim=1)
        )
    def forward(self, features):
        x = self.flatten(features)
        logits = self.linear_relu_stack(x)
        return logits

print(NeuralNetwork().to('cpu'))

# Function to perform the evluation of each model based on the confuse matrix
def evaluation(confmat_glb):

    # Display the confuse matrix
    print(confmat_glb)

    # Achieve the TP, FN, FP for benign
    tp_benign = confmat_glb[0, 0].item()
    fn_benign = confmat_glb[0, 1].item() + confmat_glb[0, 2].item() + confmat_glb[0, 3].item() + confmat_glb[0, 4].item()
    fp_benign = confmat_glb[1, 0].item() + confmat_glb[2, 0].item() + confmat_glb[3, 0].item() + confmat_glb[4, 0].item()

    # Achieve the TP, FN, FP for ACK
    tp_ack = confmat_glb[1, 1].item()
    fn_ack = confmat_glb[1, 0].item() + confmat_glb[1, 2].item() + confmat_glb[1, 3].item() + confmat_glb[1, 4].item()
    fp_ack = confmat_glb[0, 1].item() + confmat_glb[2, 1].item() + confmat_glb[3, 1].item() + confmat_glb[4, 1].item()

    # Achieve the TP, FN, FP for Scan
    tp_scan = confmat_glb[2, 2].item()
    fn_scan = confmat_glb[2, 0].item() + confmat_glb[2, 1].item() + confmat_glb[2, 3].item() + confmat_glb[2, 4].item()
    fp_scan = confmat_glb[0, 2].item() + confmat_glb[1, 2].item() + confmat_glb[3, 2].item() + confmat_glb[4, 2].item()

    # Achieve the TP, FN, FP for SYN
    tp_syn = confmat_glb[3, 3].item()
    fn_syn= confmat_glb[3, 0].item() + confmat_glb[3, 1].item() + confmat_glb[3, 2].item() + confmat_glb[3, 4].item()
    fp_syn = confmat_glb[0, 3].item() + confmat_glb[1, 3].item() + confmat_glb[2, 3].item() + confmat_glb[4, 3].item()

    # Achieve the TP, FN, FP for UDDP
    tp_udp = confmat_glb[4, 4].item()
    fn_udp= confmat_glb[4, 0].item() + confmat_glb[4, 1].item() + confmat_glb[4, 2].item() + confmat_glb[4, 3].item()
    fp_udp = confmat_glb[0, 4].item() + confmat_glb[1, 4].item() + confmat_glb[2, 4].item() + confmat_glb[3, 4].item()

    # calcualte recall, precision and f1 score for each label respective
    recall_benign, precision_benign, f1_score_benign = evaluation_helper(tp_benign, fn_benign, fp_benign)
    recall_ack, precision_ack, f1_score_ack = evaluation_helper(tp_ack, fn_ack, fp_ack)
    recall_scan, precision_scan, f1_score_scan = evaluation_helper(tp_scan, fn_scan, fp_scan)
    recall_syn, precision_syn, f1_score_syn = evaluation_helper(tp_syn, fn_syn, fp_syn)
    recall_udp, precision_udp, f1_score_udp = evaluation_helper(tp_udp, fn_udp, fp_udp)

    # Add them to a 2D list
    return [[recall_benign, precision_benign, f1_score_benign], [ recall_ack, precision_ack, f1_score_ack],
            [recall_scan, precision_scan, f1_score_scan], [recall_syn, precision_syn, f1_score_syn], [recall_udp, precision_udp, f1_score_udp]]

# Helper function to calculate recall precision and f1 score
def evaluation_helper(tp, fn, fp):
    if tp == 0:
        recall = 0
        precision = 0
        f1_score = 0
    else:
        recall = round((tp)/(tp + fn), 4)
        precision = round((tp)/(tp + fp), 4)
        f1_score = round(2 * ((precision * recall)/(precision + recall)), 4)


    return recall, precision, f1_score

def display_evaluation(eval_list):
    print()
    print("The display will followed by format: Type: [Recall, precision, f1_score]")
    for i in range(len(eval_list)):
        if i == 0:
            print('benign:', end = ' ')
        if i == 1:
            print('ack:', end = ' ')
        if i == 2:
            print('scan:', end = ' ')
        if i == 3:
            print('syn:', end = ' ')
        if i == 4:
            print('udp:', end = ' ')
        
        print(eval_list[i])

# Function to train the model
# Citation:
def train(dataloader, model, loss_fn, optimizer, epoch):
    for i in range(epoch):
        model.train()
        for tup in dataloader:

            X = tup[0]
            y = tup[1]

            pred = model(X)
            loss = loss_fn(pred, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()


# Function to test the model
# Citations: 
from torchmetrics import Recall, ConfusionMatrix
def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    model.eval()
    test_loss, total = 0, 0
    recall_glb = 0.0
    recall_model = Recall(task="multiclass", average='macro', num_classes=5)
    confmat_glb = torch.zeros(5, 5, dtype=torch.int64)
    with torch.no_grad():
        for tup in dataloader:
            X = tup[0]
            y = tup[1]

            # calculate y_pred
            pred = model(X)

            test_loss += loss_fn(pred, y).item()

            # Find the specific target
            pred_int = pred.argmax(1)
            recall_local = recall_model(pred_int, y)

            recall_glb += recall_local

            total += y.size(0)

            # Generaate the confusion matrix
            confmat = ConfusionMatrix(task="multiclass", num_classes=5)

            # 
            confmat_local = confmat(pred_int, y)
            confmat_glb += confmat_local


    recall_glb /= size
    recall_glb = recall_glb * 12
    test_loss /= size

    eval_list = evaluation(confmat_glb)
    display_evaluation(eval_list)
    
    return test_loss, recall_glb

def train_test_itr(epochs, train_loader, test_loader):
    loss_fn = nn.CrossEntropyLoss()
    model_dnn = NeuralNetwork()
    optimizer = torch.optim.SGD(model_dnn.parameters(), lr=1e-3)
    for t in range(epochs):
        print(f"Epoch {t + 1}\n----------------------------------------------")
        train(train_loader, model_dnn, loss_fn, optimizer, epoch=5)
        test(test_loader, model_dnn, loss_fn)

# import datetime
# def LDL_rst(e):
#     print()
#     train_test_itr(epochs=e, train_loader=train_loader_client, test_loader=test_loader_client)

# starttime_LDL = datetime.datetime.now()

# LDL_rst(e = 5)

# endtime_LDL = datetime.datetime.now()

# time_LDL = (endtime_LDL - starttime_LDL).seconds

# time_LDL


from collections import OrderedDict

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision.datasets import CIFAR10

import flwr as fl


import flwr as fl
# Citation: 
def get_parameters(net):
    return [val.cpu().numpy() for _, val in net.state_dict().items()]

def set_parameters(net, parameters):
    params_dict = zip(net.state_dict().keys(), parameters)
    state_dict = OrderedDict({k: torch.Tensor(v) for k, v in params_dict})
    net.load_state_dict(state_dict, strict=True)


# Citation:
class FlowerClient(fl.client.NumPyClient):
    def __init__(self, net, trainloader, valloader, loss_func, optimizer, epoch):
        self.net = net
        self.trainloader = trainloader
        self.valloader = valloader
        self.loss_func = loss_func
        self.optimizer = optimizer
        self.epoch = epoch

    def get_parameters(self, config):
        return get_parameters(self.net)

    def fit(self, parameters, config):
        set_parameters(self.net, parameters)
        train(self.trainloader, self.net, self.loss_func, self.optimizer, self.epoch)
        return get_parameters(self.net), len(self.trainloader), {}

    def evaluate(self, parameters, config):
        set_parameters(self.net, parameters)
        loss, accuracy = test(self.valloader, self.net, self.loss_func)
        return float(loss), len(self.valloader), {"accuracy": float(accuracy)}


from torch.optim import optimizer


trainloader = train_loader_client
valloader = test_loader_client
loss_fun = nn.CrossEntropyLoss()
model_dnn = NeuralNetwork()
optimizer = torch.optim.SGD(model_dnn.parameters(), lr=1e-3)

client1 = FlowerClient(model_dnn, trainloader, valloader, loss_fun, optimizer, epoch=1)


fl.client.start_numpy_client(
    server_address = "10.0.0.2:8080",
    client=client1,
)
