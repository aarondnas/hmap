import cv2
from hmap import Gradient_Huemap_Stream
import numpy as np
import matplotlib.pyplot as plt


image = cv2.imread('test_assets/test2.png')
#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("INPUT", image)
cv2.waitKey(0)
cv2.destroyAllWindows()


#image1d = np.linspace(0, 255, 256)
#image = np.tile(image1d, (100, 1)).astype(int)
#plt.imshow(gradient_2d, cmap='gray')
#plt.show()


scale_factor = 1
cold_color = (4, 0, 255)
hot_color = (21, 255, 0)
#cold_color = (41, 245, 27) # grey/blueish
#hot_color = (237, 38, 197) # pink
#gradiation_steps = 256 # 256 == max
clockwise = True

huemap_instance = Gradient_Huemap_Stream(image,scale_factor,cold_color,hot_color,clockwise)
result_image =  huemap_instance.stream_gradient_huemap(image) # result is rgb format

result_image = cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR)
cv2.imshow("RESULT", result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
#plt.imshow(result_image)
#plt.show()



# stream variante: steps mit 256 vorgegeben, streamresolution einmal am Anfang eingestellt (nicht jedes mal neu angepasst)
# kann rgb bild oder schwarz weiß bild übergeben
# Bild wird als RGB zurückgegeben
# Achtung! cv2.imshow intepretiert alles als BGR