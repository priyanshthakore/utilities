# USAGE : python3 roi_loi_plotting.py --input <input video path/rtsp link> --width <width of image for deepstream> --height <height if image for deepstream>
# example python3 roi_loi_plotting.py --input frame.jpg --width 1920 --height 1080

"""
STEPS 
1-Execute scripts with file path and resolution
2-Press c to capture one image 
3-Draw 4 points of ROI one by one and press any key 
NOTE: After pressing key the ROI will appear
4-Now draw 2 points of Line crossing and press and key
NOTE: After pressing key the crossing LOI will appear
5-Now draw 2 points of Direction and press and key 
NOTE: After pressing key the direction LOI will appear
6-Press any key for the output in terminal 
NOTE: the output in terminal is sequenced according as required by analytics config file

7-Copy and paste the ROI and LOI co-ordinate 
"""
import cv2
import numpy as np
import argparse
import os

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"

def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        a.append(x)
        b.append(y)
        cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=6)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        cv2.imshow("image", img)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--video", required=True,
	help="path to video file")
ap.add_argument("-w","--width", required=True,
    help ="Width of image")
ap.add_argument("-t","--height",required=True,
    help="Height of image")
args = vars(ap.parse_args())

a = []
b = []

cap = cv2.VideoCapture(args["video"])
while True:
    ret, image = cap.read()
    image = cv2.resize(image, (int(args["width"]), int(args["height"])))
    org_image = image.copy()
    image = cv2.putText(image,"Press c to capture image",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    cv2.imshow("frame", image)
    if cv2.waitKey(1) == ord('c'):
        img = org_image.copy()
        break
cap.release()
cv2.destroyAllWindows()

####### ROI  crossing 
cv2.namedWindow("image")
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
cv2.imshow("image", img)
cv2.waitKey(0)

pts = np.array([[a[0],b[0]],[a[1],b[1]],[a[2],b[2]],[a[3],b[3]]], np.int32)
cv2.polylines(img,[pts],True,(0,0,255))
cv2.imshow("image", img)


####### Line crossing 

cv2.namedWindow("image")
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
cv2.imshow("image", img)
cv2.waitKey(0)

img = cv2.line(img, (a[4],b[4]), (a[5],b[5]), (0,0,255), 1)
cv2.imshow("image", img)

####### Direction Line  

cv2.namedWindow("image")
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
cv2.imshow("image", img)
cv2.waitKey(0)

img = cv2.line(img, (a[6],b[6]), (a[7],b[7]), (0,0,255), 1)
cv2.imshow("image", img)
cv2.waitKey(0)

deepstream_roi = str(a[0])+';'+str(b[0])+';'+str(a[1])+';'+str(b[1])+';'+str(a[2])+';'+str(b[2])+';'+str(a[3])+';'+str(b[3])
deepstream_loi = str(a[6])+';'+str(b[6])+';'+str(a[7])+';'+str(b[7])+';'+str(a[4])+';'+str(b[4])+';'+str(a[5])+';'+str(b[5])
print(f"Deepstream ROI Co-ordinate: {deepstream_roi}")
print(f"Deepstream LOI Co-ordinate: {deepstream_loi}")
