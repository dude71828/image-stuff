from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def upsize(grid, multiplier):
    length = len(grid) * multiplier
    newgrid = np.zeros((length, length, len(grid[0][0])))
    for i in range(length):
        for j in range(length):
            newgrid[i, j] = grid[i//multiplier, j//multiplier]
    return newgrid.astype(np.uint8)

def unitconv(eff, imgarr):
    finalcolor = [0, 0, 0]
    for i in range(grid_size):
        for j in range(grid_size):
            finalcolor += imgarr[i,j] * eff[i,j]
    return finalcolor

def conv(eff, imgarr):
    imgarraylocal = np.copy(imgarr)
    for i in range(semilength, h-semilength):
        for j in range(semilength, w-semilength):
            imgarraylocal[i][j] = unitconv(eff, imgarr[i-semilength:i+semilength+1, j-semilength:j+semilength+1])
    return imgarraylocal


image_path = "pixelimg/pixel bird.png" #pick image
img = Image.open(image_path)
s = 64
output_s = 256

img_resized = img.resize((s, s), Image.NEAREST)
image_array = np.array(img_resized.convert("RGB"))
h = image_array.shape[0]
w = image_array.shape[1]


grid_size = 5 #adjustable

center = grid_size // 2
semilength = grid_size - center - 1
effect_unnorm = np.zeros((grid_size, grid_size))

option = 3
if option == 1:
    for i in range(grid_size): #gaussian
        for j in range(grid_size):
            effect_unnorm[i, j] = 3**(-((i-center)**2) - ((j-center)**2))
elif option == 2: #uniform
    effect_unnorm = np.ones((grid_size, grid_size))
elif option == 3: #custom, change according to grid_size
    effect_unnorm = np.array([
        [0, 0, 1, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 4, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 1]
    ], dtype=np.uint8)


def norm(unnormeffect):
    return unnormeffect / np.sum(unnormeffect)

effect = norm(effect_unnorm)




final_image_array = conv(effect, image_array).astype(np.uint8)
imgf = Image.fromarray((final_image_array)).resize((output_s, output_s), Image.NEAREST)
imgorig = Image.fromarray((image_array)).resize((output_s, output_s), Image.NEAREST)

imgarrf = np.array(imgf)
imgarrorig = np.array(imgorig)

fig, ax = plt.subplots()
img_display = ax.imshow(imgarrf)
ax.axis("off")

def pressed(event):
    img_display.set_data(imgarrorig)
    fig.canvas.draw_idle()
    
def released(event):
    img_display.set_data(imgarrf)
    fig.canvas.draw_idle()
    
fig.canvas.mpl_connect("button_press_event", pressed)
fig.canvas.mpl_connect("button_release_event", released)

plt.show()
