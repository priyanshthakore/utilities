import cv2

image = cv2.imread("image.jpg")
image = cv2.resize(image, (1280, 720))
print(image.shape)
# image = cv2.rectangle(image, (left, top),(left+width, top+height), (0, 0, 255, 0), 2)
cv2.rectangle(image, (527, 332),(527+193, 332+90), (0, 0, 255, 0), 2)
cv2.imshow("Frame",image)
cv2.waitKey(0)