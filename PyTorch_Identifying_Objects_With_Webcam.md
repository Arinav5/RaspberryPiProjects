# Computer Vision -- Identifying Objects on Campera with PyTorch 

Lab Date: Mar 4
Due Date: 2:00pm Mar 16

## Image Classification Workflow - Fashion MNIST

- First we trained the model on Google Colab and used the Fashion MNIST. After training the model we import the .pth file onto the raspberry pi. And then we wrote the code below and ran it on thonny. 
```Python
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
import torchvision.transforms as transforms
import time

# ---- 1. Define the EXACT same architecture used in training ----
class GarmentClassifier(nn.Module):
    def __init__(self):
        super(GarmentClassifier, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 4 * 4, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 4 * 4)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# ---- 2. Load trained weights ----
model = GarmentClassifier()
model.load_state_dict(torch.load("my_model.pth", map_location="cpu"))
model.eval()
print("Model loaded successfully on Raspberry Pi")

# ---- 3. Class label mapping ----
classes = ('T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
           'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot')

# ---- 4. Preprocess your image ----
# The image should already be preprocessed to 28x28 grayscale
# Use the provided "Image Preprocess" script from the Asset folder
# OR do it manually here:
transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

img_path = "tshirt.jpeg"  # <-- Change to your image filename
pil_img = Image.open(img_path).convert("L")  # Convert to grayscale

img_t = transform(pil_img)
images = img_t.unsqueeze(0)  # Add batch dimension: [1, 1, 28, 28]

# ---- 5. Run inference and measure time ----
start_time = time.time()
print(start_time)
with torch.no_grad():
    outputs = model(images)
    pred = outputs.argmax(dim=1).item()

end_time = time.time()
print(end_time)
inference_time = (end_time - start_time) * 1000  # in milliseconds

# ---- 6. Print results ----
print(f"Predicted class index: {pred}")
print(f"Predicted label: {classes[pred]}")
print(f"Inference time: {inference_time:.2f} ms")


```

- This code told is that the image we uploaded was a shirt. The projected accuracy was 88.8 percent. 

## Real-Time Video Frame Classification

- First we downloaded the txt file with over 1000 objecto categories on the terminal. Then we wrote the following code to use a web camera and classify the objects we put in front of the camera into one of the categories. Below is the code:
```Python
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
import torchvision.transforms as transforms
import time

# ---- 1. Define the EXACT same architecture used in training ----
class GarmentClassifier(nn.Module):
    def __init__(self):
        super(GarmentClassifier, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 4 * 4, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 4 * 4)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# ---- 2. Load trained weights ----
model = GarmentClassifier()
model.load_state_dict(torch.load("my_model.pth", map_location="cpu"))
model.eval()
print("Model loaded successfully on Raspberry Pi")

# ---- 3. Class label mapping ----
classes = ('T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
           'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot')

# ---- 4. Preprocess your image ----
# The image should already be preprocessed to 28x28 grayscale
# Use the provided "Image Preprocess" script from the Asset folder
# OR do it manually here:
transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

img_path = "tshirt.jpeg"  # <-- Change to your image filename
pil_img = Image.open(img_path).convert("L")  # Convert to grayscale

img_t = transform(pil_img)
images = img_t.unsqueeze(0)  # Add batch dimension: [1, 1, 28, 28]

# ---- 5. Run inference and measure time ----
start_time = time.time()
print(start_time)
with torch.no_grad():
    outputs = model(images)
    pred = outputs.argmax(dim=1).item()

end_time = time.time()
print(end_time)
inference_time = (end_time - start_time) * 1000  # in milliseconds

# ---- 6. Print results ----
print(f"Predicted class index: {pred}")
print(f"Predicted label: {classes[pred]}")
print(f"Inference time: {inference_time:.2f} ms")


```

- Next, we changed the threads and used the command "htop" to wee how much of the cpu was being used as the amount of threads changed. 
With one thread you can clearly tell the CPU usage is on one core

![[20260304_15h40m44s_grim.png]]

With three threads it is a bit harder to tell but the CPU usage is higher and the FPS increased
![[20260304_15h42m33s_grim.png]]

