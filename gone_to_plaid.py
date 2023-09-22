# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 09:17:32 2023

@author: Daniel
"""

from PIL import Image, ImageDraw, ImageOps
import numpy as np
import colorsys
import uuid
import argparse

def main(mode):
    if mode == 'plaid':
        _plaid()
    elif mode == 'buffalo':
        _buffalo()
    elif mode == 'gingham':
        _gingham()


def _gingham(w=1000,h=1000):
    image = Image.new("RGBA", (w,h), "white")
    draw = ImageDraw.Draw(image)
    
    spacing = np.linspace(0,w,20)
    dif = spacing[1]
    
    hue = np.random.randint(0,359)/100
    
    
    color1 = _hsv2rgb(hue,0,1)
    color2 = _hsv2rgb(hue,0.5,1)
    color3 = _hsv2rgb(hue,0.25,1)
    color4 = _hsv2rgb(hue,0.75,1)
    for row in range(len(spacing)):
        if row%2 == 0:
            colors = [color1,color2]
        else:
            colors = [color3,color4]
        for col in range(len(spacing)):
            shape = (spacing[col],spacing[row],spacing[col]+dif,spacing[row]+dif)
            draw.rectangle(shape,fill=colors[col%2])
             
    if np.random.randint(2):
        dlines = _diagonal_lines(w*4,h*4,color="white",n=500)
        image.paste(dlines,(0,0),dlines)
    image.show()
    _save_pattern(image)
    

def _buffalo(w=1000,h=1000):
    image = Image.new("RGBA", (w,h), "white")
    draw = ImageDraw.Draw(image)
    
    spacing = np.linspace(0,w,20)
    dif = spacing[1]
    
    hue = np.random.randint(0,359)/100
    
    color1 = _hsv2rgb(hue,1,1)
    color2 = _hsv2rgb(hue,1,0.5)
    color3 = _hsv2rgb(hue,1,0.25)
    color4 = _hsv2rgb(hue,1,0)
    for row in range(len(spacing)):
        if row%2 == 0:
            colors = [color1,color2]
        else:
            colors = [color3,color4]
        for col in range(len(spacing)):
            shape = (spacing[col],spacing[row],spacing[col]+dif,spacing[row]+dif)
            draw.rectangle(shape,fill=colors[col%2])
               
    if np.random.randint(2):
        dlines = _diagonal_lines(w*4,h*4,color=color1,n=500)
        image.paste(dlines,(0,0),dlines)
    image.show()
    _save_pattern(image)

def _plaid():
    
    w = 250
    h = 250
    sat = np.random.random()
    bkg_hue = np.random.randint(0,359)/100
    box_hue = np.random.randint(0,359)/100
    
    degree_diff = [30,-30,180,-180]
    thick_hue = box_hue-degree_diff[np.random.randint(4)]
    
    bkg_color = _hsv2rgb(bkg_hue,sat,0.8)
    box_color = _hsv2rgb(box_hue,sat,0.5)
    thick_color = _hsv2rgb(thick_hue,sat,0.60)
    
    thin_vals = [0.95,0.60,0.05]
    thin_color = _hsv2rgb(thick_hue,0.15,thin_vals[np.random.randint(2)])
    
    img = Image.new("RGBA",(w,h),bkg_color)
    draw = ImageDraw.Draw(img)
    
    line_offset = np.random.randint(25,50)
    line_offset = np.random.randint(25,50)
    
    line_offset -= line_offset % 5
    line_offset -= line_offset % 5
    
    
    box_offset = np.random.randint(20,40)
    if box_offset %2 !=0:
        box_offset +=1

    vline = (line_offset+box_offset/2,0,line_offset+box_offset/2,h)
    draw.line(vline,fill=thick_color,width=box_offset+1)

    hline = (0,line_offset+box_offset/2,w,line_offset+box_offset/2)
    draw.line(hline,fill=thick_color,width=box_offset+1)
    
    if np.random.randint(2):
        vline1 = (line_offset-box_offset,0,line_offset-box_offset,h)
        draw.line(vline1,fill=thick_color,width=int(box_offset/4+1))
        
        vline2 = (line_offset+box_offset*2,0,line_offset+box_offset*2,h)
        draw.line(vline2,fill=thick_color,width=int(box_offset/4+1))

        hline1 = (0,line_offset-box_offset,w,line_offset-box_offset)
        draw.line(hline1,fill=thick_color,width=int(box_offset/4+1))
        
        hline2 = (0,line_offset+box_offset*2,w,line_offset+box_offset*2)
        draw.line(hline2,fill=thick_color,width=int(box_offset/4+1))
    
    if np.random.randint(2):
        box = (line_offset,line_offset,line_offset+box_offset,line_offset+box_offset)
        draw.rectangle(box,fill=box_color)

    if np.random.randint(2):
        direction = np.random.randint(2)
        if direction:
            extra_line = (0,line_offset*2+box_offset*2,w,line_offset*2+box_offset*2)
        else:
            extra_line = (line_offset*2+box_offset*2,0,line_offset*2+box_offset*2,h)
        draw.line(extra_line,fill=thick_color,width=(int(box_offset/4)))
    num_lines = np.random.randint(3,6)
    if num_lines %2 !=0:
        num_lines +=1
        
    spacing = np.round(np.linspace(0-box_offset/2,box_offset+box_offset/2,num_lines)).astype(int)
    if np.random.randint(2):
        line_offset *=4
    for l in range(num_lines):
        thin_vline = (line_offset+spacing[l],0,line_offset+spacing[l],h)
        draw.line(thin_vline,fill=thin_color,width=int(spacing[1]/3))
        
        thin_hline = (0,line_offset+spacing[l],w,line_offset+spacing[l])
        draw.line(thin_hline,fill=thin_color,width=int(spacing[1]/3))
        

    flipped = ImageOps.flip(img)
    img2 = Image.new("RGB",(w,h*2))
    img2.paste(img,(0,0))
    img2.paste(flipped,(0,h))
    
    mirrored = ImageOps.mirror(img2)
    img3 = Image.new("RGB",(w*2,h*2))
    img3.paste(img2,(0,0))
    img3.paste(mirrored,(w,0))
    
    tile = Image.new("RGB",(w*4,h*4))
    tile.paste(img3,(0,0))
    tile.paste(img3,(w*2,0))
    tile.paste(img3,(0,h*2))
    tile.paste(img3,(w*2,h*2))
    if np.random.randint(2):
        dlines = _diagonal_lines(w*4,h*4,color=bkg_color,n=250)
        tile.paste(dlines,(0,0),dlines)
    tile.show()
    _save_pattern(tile)
    # Generate a random UUID (Universally Unique Identifier)
    

def _hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def _diagonal_lines(w,h,n=40,color=(255,255,255)):
    xspacing = np.linspace(0,w,n)
    yspacing = np.linspace(0,h,n)
    img = Image.new("RGBA",(w,h),(0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    for i in range(n):
        shape = (xspacing[i],0,w,h-yspacing[i])
        draw.line(shape,fill=color,width=1)
        shape = (0,yspacing[i],w-xspacing[i],h)
        draw.line(shape,fill=color,width=1)
    return img

def _save_pattern(image):
    random_uuid = uuid.uuid4()

    # Create a random file name by converting the UUID to a string
    random_file_name = str(random_uuid)

    # You can add a file extension if needed
    random_file_name_with_extension = random_file_name + '.png'
    image.save(random_file_name_with_extension)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Gone to Plaid',
        description='A plaid pattern generator.')
    parser.add_argument(
    '--mode',
    '-m',
    type=str,
    choices=['buffalo', 'gingham','plaid'],
    help='Pattern type to generate.',
    default='plaid'
    )
    
    args = parser.parse_args()
    main(args.mode)