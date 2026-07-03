import cv2 as cv
import numpy as np
from transformers import pipeline
from PIL import Image

pipe = pipeline(task="depth-estimation", model="LiheYoung/depth-anything-small-hf")
image = Image.open("photo1.jpg")

# Derinlik haritasını al
sonuc = pipe(image)
depth_image = sonuc["depth"]

# PIL formatındaki görseli OpenCV'nin anlayacağı NumPy dizisine çevir
depth_array = np.array(depth_image)

# OpenCV'nin kullanabileceği formata (0-255 arası) normalize et
depth_normalized = cv.normalize(depth_array, None, 0, 255, cv.NORM_MINMAX, dtype=cv.CV_8U)

# Renkli derinlik haritasını oluştur
depth_colormap = cv.applyColorMap(depth_normalized, cv.COLORMAP_INFERNO)

#Siyah-Beyaz derinlik haritasını 
cv.imshow("Siyah-Beyaz Derinlik", depth_normalized)

#Renkli derinlik haritası
cv.imshow("Renkli Derinlik", depth_colormap)

#Orijinal görsel
orijinal_gorsel_cv = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
cv.imshow("Orijinal Gorsel", orijinal_gorsel_cv)

cv.waitKey(0)
cv.destroyAllWindows()