import cv2 as cv

#Fotoğrafları grayscale e dönüştür
img1 = cv.imread('image1.jpg')
img2 = cv.imread('image2.jpg')

img1= cv.resize(img1, (int(img1.shape[1]*0.3), int(img1.shape[0]*0.3)), cv.INTER_AREA)
img2= cv.resize(img1, (int(img2.shape[1]*0.3), int(img2.shape[0]*0.3)), cv.INTER_AREA)

#cv.imshow('img1 normal', img1)
#cv.imshow('img2 normal', img2)

img1_grayscale = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
img2_grayscale = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

#cv.imshow('img1 gray', img1_grayscale)
#cv.imshow('img2 gray', img2_grayscale)

#ORB dedektörünü başlat
orb = cv.ORB_create()

#İki görseldeki anahtar noktaları (Keypoints) ve tanımlayıcıları (Descriptors) bul
kp1, des1 = orb.detectAndCompute(img1_grayscale, None)
kp2, des2 = orb.detectAndCompute(img2_grayscale, None)

#Brute-Force Matcher oluştur
#NORM_HAMMING ORB için en uygun mesafe ölçümüdür. crossCheck=True hatalı eşleşmeleri azaltır.
bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

#Tanımlayıcıları birbiriyle eşleştir ve mesafeye göre (en iyi eşleşmeler) sırala
matches = bf.match(des1, des2)
matches = sorted(matches, key=lambda x: x.distance)

#En iyi ilk 50 eşleşmeyi çiz
img_matches = cv.drawMatches(img1, kp1, img2, kp2, matches[:15], None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

#Sonucu göster
cv.imshow("Piksel Eslesmeleri (ORB)", img_matches)
cv.waitKey(0)
cv.destroyAllWindows()