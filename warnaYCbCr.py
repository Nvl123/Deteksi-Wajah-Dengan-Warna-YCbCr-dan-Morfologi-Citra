import cv2
import numpy as np

def ekualiasiwarna(image):
    channels = cv2.split(image)
    equalized_channels = [cv2.equalizeHist(channel) for channel in channels]
    result = cv2.merge(equalized_channels)
    return result

def contrastStrech(gambar):
    min_nilai = np.min(gambar)
    max_nilai = np.max(gambar)
    strech = (gambar - min_nilai) * (255.0 / (max_nilai - min_nilai))
    strech = strech.astype(np.uint8)
    return strech

def StrechPerCahnel(gambar):
    channels = cv2.split(gambar)
    strechChannel = [contrastStrech(channel) for channel in channels]
    return cv2.merge(strechChannel)

# Membaca citra
citra = cv2.imread("C:\\Users\\ASUS\\Documents\\SEMESTER 4\\PENGOLAHAN CITRA DIGITAL\\UAS\\CITRA TUGAS UAS\\bersama.jpg")

# Kontras stretching pada setiap channel
citra1 = StrechPerCahnel(citra)

# Equalisasi warna pada citra yang sudah di-stretch
citra2 = ekualiasiwarna(citra1)

# Konversi citra ke ruang warna YCrCb
konversi = cv2.cvtColor(citra2, cv2.COLOR_BGR2YCrCb)

# Pisahkan channel Y, Cr, dan Cb
y, cb, cr = cv2.split(konversi)


# Threshold pada channel Cb
_, bin = cv2.threshold(cb, 150, 255, cv2.THRESH_BINARY)


# Membuat matriks structuring element berbentuk elips
size = 5
matriks_SE = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))


# Operasi morfologi erosi, dilasi, dan closing
erosi = cv2.morphologyEx(bin, cv2.MORPH_ERODE, matriks_SE, iterations=3)
dilasi = cv2.morphologyEx(erosi, cv2.MORPH_DILATE, matriks_SE, iterations=30)
closing = cv2.morphologyEx(dilasi, cv2.MORPH_CLOSE, matriks_SE, iterations=20)

# Masking dengan operasi bitwise and
masking = cv2.bitwise_and(bin, closing)
masking2 = cv2.bitwise_and(citra, citra, mask=masking)

# Menampilkan citra-citra hasil pemrosesan
cv2.imshow('Original Image', citra)
cv2.imshow('Contrast Stretched Image', citra1)
cv2.imshow('Equalized Image', citra2)
cv2.imshow('YCbCr Image', konversi)
cv2.imshow('Binary Mask', bin)
cv2.imshow('Final Masked Image', masking2)
cv2.imshow('channel CB', cb)
cv2.imshow('channel cr', cr)
cv2.imshow('channel y', y)

cv2.waitKey(0)
cv2.destroyAllWindows()
