from typing import Dict, List, Literal, Tuple

import torch
import torch.nn as nn
import torchvision
from typing import Optional
import birdset.modules.models.resnet_dropout

ResNetVersion = Literal["resnet18", "resnet34", "resnet50", "resnet101", "resnet152"]

class ResNetClassifier(nn.Module):
    """
    A ResNet classifier for image classification tasks.

    Attributes
    ----------
    baseline_architecture : ResNetVersion
        The version of ResNet architecture to use (e.g., ResNet18, ResNet34, ResNet50, etc.).
    num_classes : int
        The number of classes in the classification task.
    num_channels : int, optional
        The number of input channels in the images, by default 1.
    pretrained : bool, optional
        Whether to use a pretrained model, by default False.

    Methods
    -------
    forward(x):
        Performs a forward pass through the network.
    """
    def __init__(
        self,
        baseline_architecture: ResNetVersion,
        num_classes: int,
        num_channels: int = 1,
        pretrained: bool = False,
        pretrain_info: Optional[Dict] = None):
        """
        Constructs all the necessary attributes for the ResNetClassifier object.

        Parameters
        ----------
            baseline_architecture : ResNetVersion
                The version of ResNet architecture to use (e.g., ResNet18, ResNet34, ResNet50, etc.).
            num_classes : int
                The number of classes in the classification task.
            num_channels : int, optional
                The number of input channels in the images, by default 1.
            pretrained : bool, optional
                Whether to use a pretrained model, by default False.
            dropout_rate : float, optional
                The dropout rate, by default 0 (deactivated).
        """
        super(ResNetClassifier, self).__init__()
        self.baseline_architecture = baseline_architecture
        self.num_classes = num_classes
        self.num_channels = num_channels

        # Available resnet versions
        resnet_versions = {
            "resnet18": birdset.modules.models.resnet_dropout.resnet18,
            "resnet34": birdset.modules.models.resnet_dropout.resnet34,
            "resnet50": birdset.modules.models.resnet_dropout.resnet50,
            "resnet101": birdset.modules.models.resnet_dropout.resnet101,
            "resnet152": birdset.modules.models.resnet_dropout.resnet152,
        }

        resnet_model = resnet_versions[baseline_architecture](pretrained=pretrained)

        # Replace the old FC layer with Identity, so we can train our own
        linear_size = list(resnet_model.children())[-1].in_features
        # Replace the final layer for fine-tuning (classification into num_classes classes)
        resnet_model.fc = nn.Linear(linear_size, num_classes)

        # Manually set the number of channels in the first Conv layer according to the shape of our input
        resnet_model.conv1 = nn.Conv2d(
            num_channels, 64, kernel_size=7, stride=2, padding=3, bias=False
        )
        resnet_model.bn1 = nn.BatchNorm2d(64)

        print(resnet_model)
        self.model = resnet_model
        print(self.model)
    
    def forward(self, input_values: torch.Tensor, **kwargs):
        """
        Performs a forward pass through the network.

        Parameters
        -------
        input_values : torch.Tensor
            The input tensor to the network.
        kwargs : dict, optional
            Additional keyword arguments are not used.

        Returns
        -------
        torch.Tensor
            The output of the network.
        """
        return self.model(input_values)

    @torch.inference_mode()
    def get_logits(self, dataloader, device):
        pass

    @torch.inference_mode()
    def get_probas(self, dataloader, device):
        pass

    @torch.inference_mode()
    def get_representations(self, dataloader, device):
        pass
    