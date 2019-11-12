from PIL import Image
import pytesseract
import cv2
import os
import numpy as np

class ocr:
    def __init__(self, imagePath, thresholdVal):
        self.imagePath = imagePath
        self.thresholdVal = thresholdVal

    def set_image_dpi(self):
        im = Image.open(self.imagePath)
        length_x, width_y = im.size
        factor = min(1, float(1024.0 / length_x))
        size = int(factor * length_x), int(factor * width_y)
        im_resized = im.resize(size, Image.ANTIALIAS)
        filename = "{}.png".format(os.getpid())
        im_resized.save(filename, dpi=(300, 300))
        return filename

    def image_deskewing(self, image, threshold):
        coords = np.column_stack(np.where(threshold > 0))
        angle = cv2.minAreaRect(coords)[-1]

        if angle < -45:
            angle = -(90 + angle)
        else :
            angle = -angle

        (h, w) = image.shape[:2]

        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1)
        rotated = cv2.warpAffine(threshold, M, (w, h),
            flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    def image_to_text(self):
        resizedImage = self.set_image_dpi()
        image = cv2.imread(resizedImage)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # self.thresholdVal : 110 # npwp / other
        # self.thresholdVal : 80 # ktp
        _, threshold = cv2.threshold(gray, self.thresholdVal, 255, cv2.THRESH_BINARY)
        rotated = self.image_deskewing(image, threshold)

        filename = "binarize.png"
        cv2.imwrite(filename, rotated)

        text = pytesseract.image_to_string(Image.open(filename), lang="ind")
        return text