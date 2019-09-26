import os
import sys
from PIL import Image

def Usage():
    print (f'{sys.argv[0]} source-path destination-path width height overlapping-margin')
    sys.exit(1)

def SplitToTiles(src_img, dst_path, w, h, m):
    filename = os.path.splitext(os.path.basename(src_img))[0]
    im = Image.open(src_img)
    im_w, im_h = im.size
    print (f'Image width:{im_w} height:{im_h} will split into ({w} {h}) and overlapping {m} pixels')

    wl = 0
    while wl < im_w - 1:
        wr = wl + w
        if wr >= im_w:
            wr = im_w - 1
        ht = 0
        while ht < im_h - 1:
            hb = ht + h
            if hb >= im_h:
                hb = im_h - 1
            print(f'LEFT: {wl} TOP: {ht} - RIGHT:{wr} BUTTOM:{hb}')
            box = (wl, ht, wr, hb)
            piece = im.crop(box)
            img_path = os.path.join(dst_path,f'{filename} L{wl},T{ht} - R{wr},B{hb}.jpg')
            piece.save(img_path, quality=100)
            
            ht = ht + h - m
        wl = wl + w - m

if __name__=='__main__':
    if len(sys.argv) != 6:
        Usage()

    src_path = sys.argv[1]
    dst_path = sys.argv[2]

    if not os.path.exists(src_path): 
        print (f'path not exists: {src_path}')
        sys.exit(1)

    if not os.path.exists(dst_path):
        os.makedirs(dst_path) 

    w, h = int(sys.argv[3]), int(sys.argv[4])
    m = int(sys.argv[5])

    source_images = os.listdir(src_path)
    for photo in source_images:
        SplitToTiles(os.path.join(src_path, photo), dst_path, w, h, m)
    