import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

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

def resize_image(image, max_width):
    height, width = image.shape[:2]
    if width > max_width:
        ratio = max_width / width
        new_size = (max_width, int(height * ratio))
        resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
        return resized_image
    return image

def process_image(file_path):
    # Membaca citra
    citra = cv2.imread(file_path)
    if citra is None:
        raise ValueError(f"Cannot open image file: {file_path}")

    # Kontras stretching pada setiap channel
    citra1 = StrechPerCahnel(citra)

    # Equalisasi warna pada citra yang sudah di-stretch
    citra2 = ekualiasiwarna(citra1)

    # Konversi citra ke ruang warna YCrCb
    konversi = cv2.cvtColor(citra2, cv2.COLOR_BGR2YCrCb)

    # Pisahkan channel Y, Cr, dan Cb
    y, cb, cr = cv2.split(konversi)

    # Threshold pada channel Cb
    _, bin = cv2.threshold(cb, threshold_val, 255, cv2.THRESH_BINARY)

    # Membuat matriks structuring element berbentuk elips
    size = 5
    matriks_SE = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))

    # Operasi morfologi erosi, dilasi, dan closing
    erosi = cv2.morphologyEx(bin, cv2.MORPH_ERODE, matriks_SE, iterations=erosion_iter)
    dilasi = cv2.morphologyEx(erosi, cv2.MORPH_DILATE, matriks_SE, iterations=dilation_iter)
    closing = cv2.morphologyEx(dilasi, cv2.MORPH_CLOSE, matriks_SE, iterations=closing_iter)

    # Masking dengan operasi bitwise and
    masking = cv2.bitwise_and(bin, closing)
    masking2 = cv2.bitwise_and(citra, citra, mask=masking)

    return [citra, citra1, citra2, konversi, bin, masking2]

def update_images():
    try:
        images = process_image(file_path)

        img_original = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(resize_image(images[0], 200), cv2.COLOR_BGR2RGB)))
        img_stretched = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(resize_image(images[1], 200), cv2.COLOR_BGR2RGB)))
        img_equalized = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(resize_image(images[2], 200), cv2.COLOR_BGR2RGB)))
        img_ycbcr = ImageTk.PhotoImage(image=Image.fromarray(resize_image(images[3][:, :, 0], 200)))
        img_binary = ImageTk.PhotoImage(image=Image.fromarray(resize_image(images[4], 200)))
        img_masked = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(resize_image(images[5], 200), cv2.COLOR_BGR2RGB)))

        lbl_img1.config(image=img_original)
        lbl_img1.image = img_original
        lbl_img2.config(image=img_stretched)
        lbl_img2.image = img_stretched
        lbl_img3.config(image=img_equalized)
        lbl_img3.image = img_equalized
        lbl_img4.config(image=img_ycbcr)
        lbl_img4.image = img_ycbcr
        lbl_img5.config(image=img_binary)
        lbl_img5.image = img_binary
        lbl_img6.config(image=img_masked)
        lbl_img6.image = img_masked
    except Exception as e:
        print(f"Error: {e}")

def load_image():
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        update_images()

def adjust_threshold(value):
    global threshold_val
    threshold_val = int(value)
    update_images()

def adjust_erosion(value):
    global erosion_iter
    erosion_iter = int(value)
    update_images()

def adjust_dilation(value):
    global dilation_iter
    dilation_iter = int(value)
    update_images()

def adjust_closing(value):
    global closing_iter
    closing_iter = int(value)
    update_images()

# Inisialisasi parameter
file_path = 'download (1).jpeg'
threshold_val = 150
erosion_iter = 2
dilation_iter = 10
closing_iter = 10

# GUI menggunakan tkinter
root = tk.Tk()
root.title('Program Deteksi Wajah')

# Judul
label_title = tk.Label(root, text='Program Deteksi Wajah', font=('Helvetica', 16, 'bold'))
label_title.grid(row=0, column=0, columnspan=4, pady=10)

# Frame untuk penyesuaian parameter
frame_adjustment = tk.LabelFrame(root, text='Adjustment', padx=10, pady=10)
frame_adjustment.grid(row=1, column=0, rowspan=6, padx=10, pady=10, sticky='n')

# Slider dan label untuk menyesuaikan parameter
tk.Label(frame_adjustment, text='Threshold').grid(row=0, column=0, sticky='w')
slider_threshold = tk.Scale(frame_adjustment, from_=0, to=255, orient=tk.HORIZONTAL, command=adjust_threshold)
slider_threshold.set(threshold_val)
slider_threshold.grid(row=0, column=1)

tk.Label(frame_adjustment, text='Erosion Iterations').grid(row=1, column=0, sticky='w')
slider_erosion = tk.Scale(frame_adjustment, from_=1, to=100, orient=tk.HORIZONTAL, command=adjust_erosion)
slider_erosion.set(erosion_iter)
slider_erosion.grid(row=1, column=1)

tk.Label(frame_adjustment, text='Dilation Iterations').grid(row=2, column=0, sticky='w')
slider_dilation = tk.Scale(frame_adjustment, from_=1, to=100, orient=tk.HORIZONTAL, command=adjust_dilation)
slider_dilation.set(dilation_iter)
slider_dilation.grid(row=2, column=1)

tk.Label(frame_adjustment, text='Closing Iterations').grid(row=3, column=0, sticky='w')
slider_closing = tk.Scale(frame_adjustment, from_=1, to=100, orient=tk.HORIZONTAL, command=adjust_closing)
slider_closing.set(closing_iter)
slider_closing.grid(row=3, column=1)

# Button untuk memuat gambar
btn_load = tk.Button(frame_adjustment, text='Load Image', command=load_image)
btn_load.grid(row=4, columnspan=2, pady=10)

# Tempat untuk citra hasil proses di sisi kanan
lbl_img1 = tk.Label(root)
lbl_img1.grid(row=1, column=1, padx=5, pady=5)
lbl_img2 = tk.Label(root)
lbl_img2.grid(row=1, column=2, padx=5, pady=5)
lbl_img3 = tk.Label(root)
lbl_img3.grid(row=1, column=3, padx=5, pady=5)
lbl_img4 = tk.Label(root)
lbl_img4.grid(row=2, column=1, padx=5, pady=5)
lbl_img5 = tk.Label(root)
lbl_img5.grid(row=2, column=2, padx=5, pady=5)
lbl_img6 = tk.Label(root)
lbl_img6.grid(row=2, column=3, padx=5, pady=5)

# Labels untuk setiap citra
tk.Label(root, text='Original Image').grid(row=3, column=1)
tk.Label(root, text='Stretched Image').grid(row=3, column=2)
tk.Label(root, text='Equalized Image').grid(row=3, column=3)
tk.Label(root, text='YCbCr Image').grid(row=4, column=1)
tk.Label(root, text='Binary Image').grid(row=4, column=2)
tk.Label(root, text='Masked Image').grid(row=4, column=3)

# Memuat gambar default saat pertama kali dijalankan
update_images()

root.mainloop()
