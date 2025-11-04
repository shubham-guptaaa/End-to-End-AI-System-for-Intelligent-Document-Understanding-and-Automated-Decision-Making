# resume_heatmap.py
import cv2
import numpy as np
from PIL import Image

def draw_heatmap_on_image(image_path, box_score_list, save_path):
    """
    box_score_list: list of tuples (x0,y0,x1,y1, score) where score is 0..1
    Produces a blended heatmap saved to save_path and returns save_path.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image for heatmap: " + image_path)

    mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.float32)

    for (x0, y0, x1, y1, score) in box_score_list:
        # clamp coords inside image
        x0 = max(0, int(round(x0)))
        y0 = max(0, int(round(y0)))
        x1 = min(img.shape[1]-1, int(round(x1)))
        y1 = min(img.shape[0]-1, int(round(y1)))
        if x1 <= x0 or y1 <= y0:
            continue
        mask[y0:y1, x0:x1] = np.maximum(mask[y0:y1, x0:x1], float(score))

    # normalize mask to [0,255]
    mask_uint8 = (255 * (mask / (mask.max() if mask.max() > 0 else 1))).astype('uint8')

    # colorize
    heatmap_color = cv2.applyColorMap(mask_uint8, cv2.COLORMAP_JET)

    # combine
    output = cv2.addWeighted(img, 0.6, heatmap_color, 0.4, 0)

    # ensure directory exists
    out_dir = os.path.dirname(save_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    cv2.imwrite(save_path, output)
    return save_path
