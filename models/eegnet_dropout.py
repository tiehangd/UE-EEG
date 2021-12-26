##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## Modified from: https://github.com/aliasvishnu/EEGNet
##
## This source code is licensed under the MIT-style license found in the
## LICENSE file in the root directory of this source tree
##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
""" Feature Extractor """
import torch.nn as nn
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
import torch.nn.functional as F
import torch.optim as optim


class EEGNet_Dropout(nn.Module):

    def __init__(self, p=0.2):
        super(EEGNet_Dropout, self).__init__()
        self.Conv2d = nn.Conv2d
        self.conv1 = nn.Conv2d(1, 16, (1, 22), padding = 0)
        self.batchnorm1 = nn.BatchNorm2d(16, False)
        # Layer 2
        self.padding1 = nn.ZeroPad2d((16, 17, 0, 1))
        self.conv2 = nn.Conv2d(1, 4, (2, 32))
        self.batchnorm2 = nn.BatchNorm2d(4, False)
        self.pooling2 = nn.MaxPool2d(4, 4)
        
        # Layer 3
        self.padding2 = nn.ZeroPad2d((2, 1, 4, 3))
        self.conv3 = nn.Conv2d(4, 4, (8, 4))
        self.batchnorm3 = nn.BatchNorm2d(4, False)
        self.pooling3 = nn.MaxPool2d((2, 4))
        self.linear = nn.Linear(4*2*25, 4)
        self.dropout=nn.Dropout2d(p)

    def forward(self, x):
        x = self.dropout(F.relu(self.conv1(x)))
        x = self.batchnorm1(x)
        x = x.permute(0, 3, 1, 2)
        # Layer 2
        x = self.padding1(x)
        x = self.dropout(F.relu(self.conv2(x)))
        x = self.batchnorm2(x)
        x = self.pooling2(x)
        # Layer 3
        x = self.padding2(x)
        x = self.dropout(F.relu(self.conv3(x)))
        x = self.batchnorm3(x)
        x = self.pooling3(x)
        x = x.view(-1, 4*2*25)
        x = self.linear(x)

        return x

        
