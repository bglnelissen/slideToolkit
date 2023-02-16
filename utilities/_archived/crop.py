import cv2
from sys import argv

top = float(argv[1])
bottom = float(argv[2])
left = float(argv[3])
right = float(argv[4])
path = argv[5]

def crop_img(img):
    center_x, center_y = img.shape[1] / 2, img.shape[0] / 2    
    left_x, right_x = center_x - img.shape[1]*left / 2, center_x + img.shape[1]*right / 2
    top_y, bottom_y = center_y - img.shape[0]*top / 2, center_y + img.shape[0]*bottom / 2
    img_cropped = img[int(top_y):int(bottom_y), int(left_x):int(right_x)]
    return img_cropped


img = cv2.imread(path)
img_cropped = crop_img(img)
cv2.imwrite("cropped_" + path,img_cropped)
