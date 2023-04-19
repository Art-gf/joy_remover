from PIL import Image
import os
from concurrent.futures import ThreadPoolExecutor

F_IMPORT = "input"
F_EXPORT = "output"
HEIGHT_PX = 14
COLOR_PX = [
    [252, 195, 51],
    [254, 154, 9]
]
POINTS_PX = 4 


def is_comp(rgb: tuple):
    for i in range(2):
        res = [0.9 < rgb[i]/color[i] < 1.1 for color in COLOR_PX]
        if not any(res):
            return 
    return True

def get_points():
    step = int(100/(POINTS_PX+1))
    pix = [i/100 for i in range(step, 100, step)]
    return pix[:POINTS_PX]

def img_proc(name: str):
    path = f"{F_IMPORT}/{name}"
    dest = f"{F_EXPORT}/{name}"
    with Image.open(path) as img:
        img_rgb = img.convert("RGB")
        w, h = img.size
        pix = get_points()
        for perc in pix:
            rgb = img_rgb.getpixel((int(w*perc), h-int(HEIGHT_PX/2)))
            if not is_comp(rgb):
                return
        img = img.crop([0,0,w,h-14])
        img.save(dest)
    
    
def start():
    if files := os.listdir(F_IMPORT):
        with ThreadPoolExecutor() as w:
            for file in files:
                w.submit(img_proc, file)
    

