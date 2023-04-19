from typing import List
from PIL import Image
import os
from concurrent.futures import ThreadPoolExecutor

F_IMPORT = "input"
F_EXPORT = "output"

PX_HEIGHT = 14
PX_COLOR = [
    [252, 195, 51],
    [254, 154, 9]
]
PX_POINTS = 4


def is_comp(rgb: tuple) -> bool:
    for i in range(2):
        res = [0.9 < rgb[i]/color[i] < 1.1 for color in PX_COLOR]
        if not any(res):
            return False
    return True


def get_points() -> List[float]:
    step = int(100/(PX_POINTS+1))
    pix = [i/100 for i in range(step, 100, step)]
    return pix[:PX_POINTS]


def img_proc(name: str) -> None:
    path = f"{F_IMPORT}/{name}"
    dest = f"{F_EXPORT}/{name}"
    with Image.open(path) as img:
        img_rgb = img.convert("RGB")
        pix = get_points()
        h = img.height-int(PX_HEIGHT/2)
        for perc in pix:
            rgb = img_rgb.getpixel((int(img.width*perc), h))
            if not is_comp(rgb):
                return
        img = img.crop([0, 0, img.width, img.height-14])
        img.save(dest)


def start():
    if files := os.listdir(F_IMPORT):
        with ThreadPoolExecutor() as w:
            for file in files:
                w.submit(img_proc, file)
