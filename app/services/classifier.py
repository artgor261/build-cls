import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image

from app.core.config import settings


class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_planes, planes, stride=1, downsample=None):
        super().__init__()
        self.conv1 = nn.Conv2d(in_planes, planes, 3, stride, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, 3, 1, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.downsample = downsample

    def forward(self, x):
        identity = x
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        if self.downsample is not None:
            identity = self.downsample(x)
        out += identity
        return F.relu(out)


class ResNet18(nn.Module):
    def __init__(self, num_classes=5):
        super().__init__()
        self.in_planes = 64
        self.conv1 = nn.Conv2d(3, 64, 7, 2, 3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.maxpool = nn.MaxPool2d(3, 2, 1)
        self.layer1 = self._make_layer(64, 2, stride=1)
        self.layer2 = self._make_layer(128, 2, stride=2)
        self.layer3 = self._make_layer(256, 2, stride=2)
        self.layer4 = self._make_layer(512, 2, stride=2)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, num_classes)

    def _make_layer(self, planes, blocks, stride):
        downsample = None
        if stride != 1 or self.in_planes != planes * BasicBlock.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(self.in_planes, planes * BasicBlock.expansion, 1, stride, bias=False),
                nn.BatchNorm2d(planes * BasicBlock.expansion),
            )
        layers = [BasicBlock(self.in_planes, planes, stride, downsample)]
        self.in_planes = planes * BasicBlock.expansion
        for _ in range(1, blocks):
            layers.append(BasicBlock(self.in_planes, planes))
        return nn.Sequential(*layers)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.maxpool(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x


_model: ResNet18 | None = None

IMAGENET_MEAN = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
IMAGENET_STD = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)


def _transform(image: Image.Image) -> torch.Tensor:
    image = image.resize((224, 224), Image.BILINEAR)
    tensor = torch.tensor(list(image.getdata()), dtype=torch.float32).view(224, 224, 3).permute(2, 0, 1)
    tensor = tensor / 255.0
    tensor = (tensor - IMAGENET_MEAN) / IMAGENET_STD
    return tensor


def _load_model() -> ResNet18:
    global _model
    if _model is None:
        _model = ResNet18(num_classes=5)
        state_dict = torch.load(settings.MODEL_PATH, map_location="cpu", weights_only=True)
        _model.load_state_dict(state_dict)
        _model.eval()
    return _model


def predict(image: Image.Image) -> int:
    model = _load_model()
    tensor = _transform(image).unsqueeze(0)
    with torch.no_grad():
        logits = model(tensor)
        return logits.argmax(dim=1).item()
