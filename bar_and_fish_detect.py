from PIL import Image
import numpy as np
from PIL import ImageDraw
import os
from scipy import stats
import mss,time
from pynput.mouse import Button, Controller

mouse = Controller()

# hold
mouse.press(Button.left)

# release
mouse.release(Button.left)

class mode_object:
    def __init__(self, mode = None, count = 0):
        self.mode = mode
        self.count = count

def get_mode(arr):
    # filter out None values
    valid = arr[arr != np.array(None)]
    if len(valid) == 0:
        return mode_object(0,0)
    valid = valid.astype(float)
    values, counts = np.unique(valid, return_counts=True)
    mode = values[np.argmax(counts)]
    count = np.max(counts)

    mode_object1 = mode_object(mode,count)
    return mode_object1


def detect_bar_and_stem(img, y=422, x_start=873, x_end=1687):
    #img = np.array(Image.open(img_path))
    row = img[y, x_start:x_end]

    green_pixels = []
    yellow_pixels = []

    for i, pixel in enumerate(row):
        r, g, b = pixel[0], pixel[1], pixel[2]
        if g >= 240 and b > 140 and r < 150:
            green_pixels.append(x_start + i)
        if r > 200 and g > 150:
            yellow_pixels.append(x_start + i)

    green_mid = None
    green_left = None
    green_right = None
    stem_x = None

    if len(green_pixels) > 0:
        green_left  = green_pixels[0]
        green_right = green_pixels[-1]
        green_mid   = (green_left + green_right) / 2

    if len(yellow_pixels) > 0:
        stem_x = int(np.average(yellow_pixels))

    return green_left, green_right, green_mid, stem_x

def bar_consensus_check(img):
    green_lefts  = []
    green_rights = []
    green_mids   = []
    stem_xs      = []

    for i in range(0, 21, 5):
        green_left, green_right, green_mid, stem_x = detect_bar_and_stem(img, i)
        green_lefts.append(green_left)
        green_rights.append(green_right)
        green_mids.append(green_mid)
        stem_xs.append(stem_x)

    green_lefts  = np.array(green_lefts)
    green_rights = np.array(green_rights)
    green_mids   = np.array(green_mids)
    stem_xs      = np.array(stem_xs)

    result = [get_mode(green_lefts), get_mode(green_rights), get_mode(green_mids), get_mode(stem_xs)]
    most_common_coords = [result[0].mode, result[1].mode, result[2].mode, result[3].mode]
    count = [result[0].count, result[1].count, result[2].count, result[3].count]

    average = np.mean(count)

    if average != 0 and average >= 3:
        return most_common_coords[0], most_common_coords[1], most_common_coords[2], most_common_coords[3]
    else:
        return None, None, None, None  # not reliable enough
    

def visualise_detection(img_vis, green_left, green_right, green_mid, stem_x, save_path, y_center=422):
    draw    = ImageDraw.Draw(img_vis)
    arrow_height = 30

    if green_mid is not None:
        draw.line([(int(green_mid), y_center - arrow_height), (int(green_mid), y_center)], fill=(0, 255, 0), width=3)
        draw.polygon([
            (int(green_mid) - 6, y_center - 10),
            (int(green_mid) + 6, y_center - 10),
            (int(green_mid),     y_center)
        ], fill=(0, 255, 0))

    if stem_x is not None:
        draw.line([(stem_x, y_center - arrow_height), (stem_x, y_center)], fill=(255, 0, 0), width=3)
        draw.polygon([
            (stem_x - 6, y_center - 10),
            (stem_x + 6, y_center - 10),
            (stem_x,     y_center)
        ], fill=(255, 0, 0))

    if green_mid is not None and stem_x is not None:
        diff = stem_x - green_mid
        if diff > 5:
            direction   = "HOLD →"
            arrow_start = (int(green_mid), y_center - 50)
            arrow_end   = (stem_x, y_center - 50)
            arrow_color = (255, 165, 0)
        elif diff < -5:
            direction   = "← RELEASE"
            arrow_start = (stem_x, y_center - 50)
            arrow_end   = (int(green_mid), y_center - 50)
            arrow_color = (0, 200, 255)
        else:
            direction   = "CENTERED ✓"
            arrow_start = None
            arrow_color = (255, 255, 0)

        if arrow_start:
            draw.line([arrow_start, arrow_end], fill=arrow_color, width=3)
            draw.polygon([
                (arrow_end[0],     arrow_end[1] - 6),
                (arrow_end[0],     arrow_end[1] + 6),
                (arrow_end[0] + (10 if diff > 0 else -10), arrow_end[1])
            ], fill=arrow_color)

        draw.text((900, 380), f"diff={diff:.0f}  {direction}", fill=(255, 255, 255))

    img_vis.save(save_path)
    print(f"Saved: {save_path}")


'''
Old main function to use the folders for test images and run the function

folders = {
    "minigame_on":  r"D:\Jeff\Palworld Fishing Project\screenshots\minigame_on",
    "minigame_off": r"D:\Jeff\Palworld Fishing Project\screenshots\minigame_off",
}

for folder_name, folder_path in folders.items():
    print(f"\n=== {folder_name} ===")
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            img_path  = os.path.join(folder_path, filename)
            results_folder = r"D:\Jeff\Palworld Fishing Project\screenshots\annotated_results"
            filename = folder_name + "_" + filename
            save_path = os.path.join(results_folder,filename)  # filename already has .png

            green_left, green_right, green_mid, stem_x = bar_consensus_check(img_path)

            if green_mid is None:
                print("No minigame detected")
            visualise_detection(img_path, green_left, green_right, green_mid, stem_x, save_path)
            
            print(f"  {filename}: green_mid={green_mid}, stem_x={stem_x}")
'''
#fixing monitor resolution, update to have a dynamic resolution
MONITOR = {
    "left":   1920,        # monitor left edge
    "top":    -266 + 415,  # monitor top + our bar y start
    "width":  2560,        # full width
    "height": 25,          # just the bar height!
}

if __name__ == "__main__":

    print('in main')

    with mss.MSS() as sct:
        frame_count = 0
        fps_start = time.time()

        while True:
            frame_start = time.time()
            
            # capture
            t1 = time.time()
            raw  = sct.grab(MONITOR)
            img  = Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX")

            # convert to numpy array
            img = np.array(img)
            t2 = time.time()

            # run bar_consensus_check
            green_left, green_right, green_mid, stem_x = bar_consensus_check(img)
            t3 = time.time()
            if(stem_x is None or green_mid is None):
                print("minigame_off")
            # decide and act on mouse
            else:
                print('minigame_on')
                holding = False
                diff = stem_x - green_mid

                if diff > 0 and not holding:
                    holding = True
                    mouse.press(Button.left)
                elif diff < 0:
                    mouse.release(Button.left)
                    holding = False

            t4 = time.time()

            print(f"capture={t2-t1:.3f}s  detect={t3-t2:.3f}s  mouse={t4-t3:.3f}s")

            # sleep for remainder of 40ms
            elapsed = time.time() - frame_start
            print(0.04 - elapsed)
            time.sleep(max(0, 0.04 - elapsed))
        
