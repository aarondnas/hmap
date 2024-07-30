'''
#scanning heatmap image
class setup():

    gradient = [[]]
    width = 0
    height = 0
    blank_rgb = [[]]

    def hmap_setup(current_cmap, img):

            ## Loading JPG file as Heat Map
            color_arr = cv2.imread(current_cmap)
            color_arr = cv2.cvtColor(color_arr, cv2.COLOR_BGR2RGB)

            ## Analyzing Heat Map PNG and storing in array
            cmap_dim = color_arr.shape
            cmap_height = cmap_dim[0]
            cmap_width = cmap_dim[1]
            counter = 0
            gradient = []

            while counter < cmap_height:
                for i in range(cmap_height):
                    for j in range(1):
                        r = color_arr[i][1][0]
                        g = color_arr[i][1][1]
                        b = color_arr[i][1][2]
                        rgb_val = (r,g,b)
                        gradient.append(rgb_val)
                        counter +=1

            ## reverses Heat Map Image
            gradient = gradient[::-1]

            setup.gradient = gradient
            setup.width = img.shape[0]
            setup.height = img.shape[1]
            setup.blank_rgb = np.zeros((setup.width, setup.height, 3)).astype(int)

            return setup.gradient, setup.blank_rgb
'''

#seaborn