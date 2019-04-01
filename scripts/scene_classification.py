import torch
from torch.autograd import Variable as V
import torchvision.models as models
from torchvision import transforms as trn
from torch.nn import functional as F
import os
from PIL import Image
import shutil

# load the pre-trained weights
arch = 'resnet50'
model_file = os.path.abspath('./models/%s_places365.pth.tar' % arch)
# if not os.access(model_file, os.W_OK):
#     weight_url = 'http://places2.csail.mit.edu/models_places365/' + '%s_places365.pth.tar' % arch
#     os.system('wget ' + weight_url)
#     shutil.move('%s_places365.pth.tar' % arch, model_file)

model = models.__dict__[arch](num_classes=365)
checkpoint = torch.load(model_file, map_location=lambda storage, loc: storage)
state_dict = {str.replace(k,'module.',''): v for k,v in checkpoint['state_dict'].items()}
model.load_state_dict(state_dict)
model.eval()


# load the image transformer
centre_crop = trn.Compose([
        trn.Resize((256,256)),
        trn.CenterCrop(224),
        trn.ToTensor(),
        trn.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# load the class label
file_name = os.path.abspath('./models/categories_places365.txt')

# if not os.access(file_name, os.W_OK):
#     synset_url = 'https://raw.githubusercontent.com/csailvision/places365/master/categories_places365.txt'
#     os.system('wget ' + synset_url)
#     shutil.move('categories_places365.txt', os.path.abspath('./models/categories_places365.txt'))


classes = list()

with open(file_name) as class_file:
    for line in class_file:
        classes.append(line.strip().split(' ')[0][3:])
classes = tuple(classes)

# load the test image
# img_name = '/Users/sumitsaha/Desktop/TARP/check_5.jpg'
# if not os.access(img_name, os.W_OK):
#     img_url = 'http://places.csail.mit.edu/demo/' + img_name
#     os.system('wget ' + img_url)
def scene_classification(image):
        img = Image.open(image)
        input_img = V(centre_crop(img).unsqueeze(0))

        # forward pass
        logit = model.forward(input_img)
        h_x = F.softmax(logit, 1).data.squeeze()
        probs, idx = h_x.sort(0, True)

        # print('{} prediction on {}'.format(arch,img_name))
        # output the prediction
        # for i in range(0, 5):
        #     print('{:.3f} -> {}'.format(probs[i], classes[idx[i]]))
        print('{:.3f} -> {}'.format(probs[0], classes[idx[0]]))
        return classes[idx[0]]
