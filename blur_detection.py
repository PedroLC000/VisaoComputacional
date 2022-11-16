import cv2
import os
import re

def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

threshold = 6 
contDesfoque = 0 
validaDesfoque = 10 

# loop over the input images
for imagePath in sorted_alphanumeric(os.listdir('.\\frames')):
	# load the image, convert it to grayscale, and compute the
	# focus measure of the image using the Variance of Laplacian
	# method
    fullpath = os.path.join(".\\frames", imagePath)
    image = cv2.imread(fullpath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)
    text = "Focado"
    # if the focus measure is less than the supplied threshold,
    # then the image should be considered "blurry"
    if fm < threshold:
        text = "Desfocado"
        contDesfoque = contDesfoque + 1
    else:
        contDesfoque = 0
    if contDesfoque > validaDesfoque:
        text = "Muito tempo desfocado (Aviso)"
    # show the image
    cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    cv2.imshow("Imagem", image)
    key = cv2.waitKey(0)