import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk

class Gradient_Huemap_Stream():
    
    def __init__(self, image,scale_factor,cold_color,hot_color,clockwise):
        self.cold_color = cold_color
        self.hot_color = hot_color
        self.clockwise = clockwise
        self.width = int(image.shape[1]*scale_factor)
        self.height = int(image.shape[0]*scale_factor)
        self.blank_rgb = np.zeros((int(self.height), int(self.width), 3)).astype(int)
        self.scale_factoruc = scale_factor




    def standardize_image_channels(img):
        if len(img.shape) == 2: pass
        elif len(img.shape) == 3 and img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img




    def generate_rgb_gradient_linear(cold_color, hot_color, steps):

        # Erstellen der Interpolationsschritte
        r = np.linspace(cold_color[0], hot_color[0], steps)
        g = np.linspace(cold_color[1], hot_color[1], steps)
        b = np.linspace(cold_color[2], hot_color[2], steps)

        #gradient = np.vstack((r, g, b)).T.astype(int) # Kombinieren der RGB-Werte zu einem Array
        gradient = np.vstack((r, g, b)).T.astype(int) # Kombinieren der RGB-Werte zu einem 2D-Array
        
        return gradient
    



    def generate_rgb_gradient_circle(cold_color, hot_color, steps, clockwise):

        # Konvertieren der Eingabefarben von RGB zu HSV
        cold_color_hsv = cv2.cvtColor(np.uint8([[cold_color]]), cv2.COLOR_RGB2HSV)[0][0]
        hot_color_hsv = cv2.cvtColor(np.uint8([[hot_color]]), cv2.COLOR_RGB2HSV)[0][0]

        # Extrahieren der HSV-Komponenten
        h1, s1, v1 = cold_color_hsv
        h2, s2, v2 = hot_color_hsv

        if clockwise:
            if h2 < h1:
                max_h_value = 179
                steps_part1 = int(np.ceil((max_h_value - h1) / (max_h_value - h1 + h2) * steps))
                steps_part2 = steps - steps_part1
                part1 = np.linspace(h1, max_h_value, steps_part1, endpoint=False)
                part2 = np.linspace(0, h2, steps_part2, endpoint=True)
            else:
                part1 = np.linspace(h1, h2, steps)
                part2 = np.array([], dtype=np.float64)  # leeres Array für den Fall h2 >= h1
        else:
            if h1 < h2:
                max_h_value = 179
                steps_part1 = int(np.ceil(h1 / (h1 + (max_h_value - h2 + 1)) * steps))
                steps_part2 = steps - steps_part1
                part1 = np.linspace(h1, 0, steps_part1, endpoint=False)
                part2 = np.linspace(max_h_value, h2, steps_part2, endpoint=True)
            else:
                part1 = np.linspace(h1, h2, steps)
                part2 = np.array([], dtype=np.float64)  # leeres Array für den Fall h1 >= h2
        
        # Kombinieren der beiden Teile
        result = np.concatenate((part1, part2))
        
        # Umwandeln der Zahlen in HSV-H-Werte
        h = result % 180  # 180, da der maximale HSV H-Wert 179 ist
        s = np.linspace(s1, s2, steps)
        v = np.linspace(v1, v2, steps)

        # Kombinieren der HSV-Werte zu einem 2D-Array
        gradient_hsv = np.vstack((h, s, v)).T.astype(np.uint8)

        # Konvertieren des HSV-Gradienten zurück in RGB
        gradient_rgb = cv2.cvtColor(gradient_hsv.reshape(-1, 1, 3), cv2.COLOR_HSV2RGB).reshape(-1, 3)

        return gradient_rgb




    def stream_gradient_huemap(self,img):
        self.steps = np.max(img) - np.min(img)
        self.gradient = Gradient_Huemap_Stream.generate_rgb_gradient_linear(self.cold_color,self.hot_color,self.steps)

        blank_rgb = self.blank_rgb

        img = cv2.resize(img, (int(self.width),int(self.height)), interpolation=cv2.INTER_AREA)
        img = Gradient_Huemap_Stream.standardize_image_channels(img)  # standadize image color channels (every input image will be converted to 256 greyscale image)
        gradiation_matrix = cv2.normalize(img, img, 0, len(self.gradient)-1, cv2.NORM_MINMAX).astype(int) # contains the calculated step/greyscale value for every pixel on the image
        blank_rgb = self.gradient[gradiation_matrix]
        result = np.uint8(blank_rgb)

        return result