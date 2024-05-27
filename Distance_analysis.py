import ast
import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

name_code = pd.read_csv('pokemon_code.csv')
name_code.set_index('Code', inplace=True)

def get_name(code):
    try:
        return name_code.loc[code, 'Name']
    except KeyError:
        return "NaN"
    


class ANN(nn.Module):
    def __init__(self, input_size,l1_size,l2_size):
        super(ANN, self).__init__()
        self.fc1 = nn.Linear(input_size, l1_size)  
        self.fc2 = nn.Linear(l1_size, l2_size)          
        self.fc3 = nn.Linear(l2_size, 1)            

    def forward(self, x):
        x = nn.functional.relu(self.fc1(x))
        x = nn.functional.relu(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))  
        return x


model = torch.load('temp_model_256_64_150.pth')
X_tensor = torch.load('X_vectorized_test02.pt').to("cuda")

l = len(X_tensor)



def index_vector(i):
    v = [0]*50
    v[i] = 1
    return v

def pokemon_vector(i):
    X_tensor[:,13:63] = torch.tensor([index_vector(i)]*l).to("cuda")

    return model(X_tensor).squeeze(1)


pv = []
norm = []

for i in range(50):
    pv.append(1-2*pokemon_vector(i)) 
    norm.append(torch.norm(pv[i]).item())

pvs = torch.stack(pv)


def distance(i):
    pv_n = pv[:i]+pv[i+1:]
    pvs = torch.stack(pv_n).t()
    U, S, V = torch.svd(pvs, some=True)
    P = U @ U.t()
    k = torch.matmul(P, pv[i])
    return torch.norm(pv[i]-k).item()

data = []

for i in range(50):
    data.append({'Name':get_name(i),'Winning Rate':(torch.sum(pv[i]).item()/l)/2+0.5,'Distance':distance(i)})

for i in range(49):    
    for j in range(i,50):
        inner_protuct = (torch.dot(pv[i],pv[j])/norm[i]/norm[j]).item()
        data[i][get_name(j)] = inner_protuct
        data[j][get_name(i)] = inner_protuct



df = pd.DataFrame(data)
df.to_csv("distance_analysis.csv")



