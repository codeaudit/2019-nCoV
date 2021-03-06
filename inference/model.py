import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models

# ALexNet
class SiameseNet(nn.Module):
    def __init__(self):
        super(SiameseNet, self).__init__()
        self.alex_net = models.alexnet(pretrained=True).features
        self.liner    = nn.Sequential(nn.Linear(12544, 6272))
        self.out      = nn.Linear(6272, 1)
        self.sig      = nn.Sigmoid()

    def cnn(self, x):
        x = self.alex_net(x)
        x = x.view(x.size()[0],-1)
        x = self.liner(x)
        return x

    def forward(self, x1, x2, flag):
        cnn1  = self.cnn(x1)
        cnn2  = self.cnn(x2)
        dis   = torch.abs(cnn1 - cnn2)
        out   = self.out(dis)
        f_out = None
        if flag:
            f_out = self.sig(out)
        else:
            f_out = out
        return f_out



