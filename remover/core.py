from PIL import Image
import os
from concurrent.futures import ThreadPoolExecutor

F_IMPORT = "input"
F_EXPORT = "output"
H_PX = 14
COL_PX = (252, 195, 51)
COL_PX_2 = (254, 154, 9)
POINTS_PX = 4


def is_comp(rgb: tuple):
    for i in range(2):
        if not (0.9 < rgb[i]/COL_PX[i] < 1.1 or 0.9 < rgb[i]/COL_PX_2[i] < 1.1):
            return
    return True

def img_proc(name: str):
    path = f"{F_IMPORT}/{name}"
    with Image.open(path) as img:
        
        
        w, h = img.size
        step = int(100/(POINTS_PX+1))
        pix = [i/100 for i in range(step, 100, step)]
        pix = pix[:POINTS_PX]
        
        img_rgb = img.convert("RGB")
        for perc in pix:
            rgb = img_rgb.getpixel((int(w*perc), h-int(H_PX/2)))
            if not is_comp(rgb):
                return

        w, h = img.size
        img = img.crop([0,0,w,h-14])
        dest = f"{F_EXPORT}/{name}"
        img.save(dest)
    
    
def start():
    files = os.listdir(F_IMPORT)
    if not files:
        return
    with ThreadPoolExecutor() as w:
        for file in files:
            w.submit(img_proc, file)
    

