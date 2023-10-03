import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk

testImage = cv2.imread('test2.png')
#testImage = cv2.cvtColor(testImage, cv2.COLOR_BGR2RGB)
img = cv2.cvtColor(testImage, cv2.COLOR_BGR2GRAY)
#testImage = Image.open('test.jpg')
testImage = np.asarray(testImage)
print(testImage)


def hmap(mapTemp, img):
        
        width = img.shape[0]
        height = img.shape[1]

        #setting up selected mapTemp
        if mapTemp == 1:
            heatMap_array = hmap_setup(current_cmap = 'cmap_plasma.jpg')
        elif mapTemp == 2:
            heatMap_array = hmap_setup(current_cmap = 'cmap_plasma.jpg')
        elif mapTemp == 3:
            heatMap_array = hmap_setup(current_cmap = 'cmap_plasma.jpg')
        else: heatMap_array = hmap_setup(current_cmap = 'cmap_plasma.jpg')

        # create blank rgb on which new image wil be projected
        blank_rgb = np.zeros((width, height, 3))
        blank_rgb = blank_rgb.astype(int)
    
        # (no clipping included)
        index_matrix = cv2.normalize(img, img, 0, len(heatMap_array), cv2.NORM_MINMAX)
        index_matrix = index_matrix.astype(int)


        print(blank_rgb)
        print(blank_rgb.shape)
        print('üüüüüüüüüüüüüüüüüüüüüüüüüüüüü')
        print(heatMap_array)
        print('üüüüüüüüüüüüüüüüüüüüüüüüüüüüü')
        print(index_matrix)


        for x in range(width):
            for y in range(height):
                t = index_matrix[x][y]
                print(t)
                blank_rgb[x][y] = heatMap_array[t-1]
        blank_rgb = np.uint8(blank_rgb)

        return blank_rgb


def hmap_setup(current_cmap):

        ## Loading JPG file as Heat Map
        color_arr = cv2.imread(current_cmap)
        color_arr = cv2.cvtColor(color_arr, cv2.COLOR_BGR2RGB)

        ## Analyzing Heat Map PNG and storing in array
        cmap_dim = color_arr.shape
        cmap_height = cmap_dim[0]
        cmap_width = cmap_dim[1]
        counter = 0
        heatMap_array = []

        while counter < cmap_height:
            for i in range(cmap_height):
                for j in range(1):
                    r = color_arr[i][1][0]
                    g = color_arr[i][1][1]
                    b = color_arr[i][1][2]
                    rgb_val = (r,g,b)
                    heatMap_array.append(rgb_val)
                    counter +=1

        ## reverses Heat Map Image
        heatMap_array = heatMap_array[::-1]
        
        #temp_range = maximum - minimum

        #temp_unit_range = maximum - minimum
        #temp_unit=int(len(heatMap_array)/temp_unit_range)

        #return heatMap_array, temp_unit, temp_range
        return heatMap_array




testImage = hmap(1,testImage)
testImage = ImageTk.PhotoImage(Image.fromarray(testImage))
testImage = Image.fromarray(testImage)
plt.imshow(testImage)
plt.show(testImage)
