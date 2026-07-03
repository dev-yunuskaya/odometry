import cv2 as cv
import numpy as np
from transformers import pipeline
from PIL import Image

#Pixel ve Depth birim değişimini hesaplama

pipe = pipeline(task="depth-estimation", model="LiheYoung/depth-anything-small-hf")

def getDepthMap(cv_image):
    rgb_image = cv.cvtColor(cv_image, cv.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)
    sonuc = pipe(pil_image)

    depth_array = np.array(sonuc["depth"])
    
    depth_normalized = cv.normalize(depth_array, None, 0, 255, cv.NORM_MINMAX, dtype=cv.CV_8U)
    depth_colormap = cv.applyColorMap(depth_normalized, cv.COLORMAP_INFERNO)

    return depth_normalized, depth_colormap

def getMachedPixels(image1, image2):
    img1_grayscale = cv.cvtColor(image1, cv.COLOR_BGR2GRAY)
    img2_grayscale = cv.cvtColor(image2, cv.COLOR_BGR2GRAY)

    orb = cv.ORB_create()

    kp1, des1 = orb.detectAndCompute(img1_grayscale, None)
    kp2, des2 = orb.detectAndCompute(img2_grayscale, None)

    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    
    best_matches = matches[:50]

    # best_matches ile birlikte kp1 ve kp2'yi de döndür
    return best_matches, kp1, kp2

import cv2 as cv
import numpy as np

def getMatchedPixelsAndDepth(image1, image2):
    # 1. kp1 ve kp2'yi fonksiyon çıktısından içeri al
    best_matches, kp1, kp2 = getMachedPixels(image1, image2)

    # 2. Hem matematiksel (gray) hem görsel (color) derinlik haritalarını alıyoruz
    depth_map1_gray, depth_map1_color = getDepthMap(image1)
    depth_map2_gray, depth_map2_color = getDepthMap(image2)

    dx_list = []
    dy_list = []
    ddepth_list = []

    for match in best_matches:
        x1, y1 = kp1[match.queryIdx].pt
        x2, y2 = kp2[match.trainIdx].pt
        
        x1, y1 = int(x1), int(y1)
        x2, y2 = int(x2), int(y2)

        dx = x2 - x1
        dy = y2 - y1

        # DİKKAT:tek kanallı gray matristen okuyoruz!
        depth1 = float(depth_map1_gray[y1, x1])
        depth2 = float(depth_map2_gray[y2, x2])
        
        ddepth = depth2 - depth1

        dx_list.append(dx)
        dy_list.append(dy)
        ddepth_list.append(ddepth)

    if len(best_matches) > 0:
        avg_dx = np.mean(dx_list)
        avg_dy = np.mean(dy_list)
        avg_ddepth = np.mean(ddepth_list)
    else:
        avg_dx, avg_dy, avg_ddepth = 0, 0, 0

    print("\n--- Eşleşme Analiz Sonuçlari ---")
    print(f"Ortalama X Hareketi (Yatay): {avg_dx:.2f} piksel")
    print(f"Ortalama Y Hareketi (Dikey): {avg_dy:.2f} piksel")
    print(f"Ortalama Derinlik Değişimi   : {avg_ddepth:.2f} birim")
    print("--------------------------------\n")

    img_matches = cv.drawMatches(image1, kp1, image2, kp2, best_matches, None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    return img_matches, avg_dx, avg_dy, avg_ddepth

image1 = cv.imread('image1.jpg')
image2 = cv.imread('image2.jpg')

img_matches, avg_dx, avg_dy, avg_ddepth = getMatchedPixelsAndDepth(image1, image2)

img_matches= cv.resize(img_matches, (int(img_matches.shape[1]*0.3), int(img_matches.shape[0]*0.3)), cv.INTER_AREA)

text_title = "--- Eslesme Analiz Sonuclari ---"
text_x = f"Ort. X Hareketi (Yatay): {avg_dx:.2f} piksel"
text_y = f"Ort. Y Hareketi (Dikey): {avg_dy:.2f} piksel"
text_depth = f"Ort. Derinlik Degisimi : {avg_ddepth:.2f} birim"

font = cv.FONT_HERSHEY_SIMPLEX
font_scale = 0.7            # Yazı büyüklüğü
color = (0, 255, 0)         # Renk BGR formatındadır. (0, 255, 0) = Saf Yeşil
thickness = 2               # Çizgi kalınlığı
line_type = cv.LINE_AA

cv.putText(img_matches, text_title, (20, 40), font, font_scale, (0, 255, 255), thickness, line_type)
cv.putText(img_matches, text_x, (20, 80), font, font_scale, color, thickness, line_type)
cv.putText(img_matches, text_y, (20, 115), font, font_scale, color, thickness, line_type)
cv.putText(img_matches, text_depth, (20, 150), font, font_scale, color, thickness, line_type)


cv.imshow('İmage Matches', img_matches)

#image1= cv.resize(image1, (int(image1.shape[1]*0.3), int(image1.shape[0]*0.3)), cv.INTER_AREA)
#image2= cv.resize(image2, (int(image2.shape[1]*0.3), int(image2.shape[0]*0.3)), cv.INTER_AREA)

    

cv.waitKey(0)
