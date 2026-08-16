from PIL import Image, ImageDraw
import math

W, H = 760, 110
FPS = 12
TOTAL = 96
OUT = 'assets/cat-walk.gif'

BG = (13, 17, 23, 0)
BODY = (33, 38, 45, 255)
OUTLINE = (88, 166, 255, 255)
MUTED = (139, 148, 158, 255)
GROUND = (48, 54, 61, 255)


def draw_cat(draw, x, y, phase, lying=False):
    if lying:
        draw.ellipse((x, y+18, x+78, y+48), fill=BODY, outline=OUTLINE, width=2)
        draw.ellipse((x+58, y+9, x+92, y+40), fill=BODY, outline=OUTLINE, width=2)
        draw.polygon([(x+64,y+13),(x+69,y+1),(x+76,y+13)], fill=BODY, outline=OUTLINE)
        draw.polygon([(x+79,y+13),(x+86,y+1),(x+89,y+16)], fill=BODY, outline=OUTLINE)
        draw.arc((x-15,y+15,x+38,y+62), 120, 310, fill=OUTLINE, width=4)
        draw.ellipse((x+45,y+38,x+64,y+49), fill=BODY, outline=OUTLINE)
        draw.line((x+69,y+25,x+75,y+25), fill=(200,210,220,255), width=1)
        draw.line((x+81,y+25,x+87,y+25), fill=(200,210,220,255), width=1)
    else:
        bob = math.sin(phase*2*math.pi)*2
        y += bob
        draw.ellipse((x+16,y+15,x+72,y+43), fill=BODY, outline=OUTLINE, width=2)
        draw.ellipse((x+61,y+7,x+92,y+36), fill=BODY, outline=OUTLINE, width=2)
        draw.polygon([(x+66,y+10),(x+71,y-1),(x+77,y+11)], fill=BODY, outline=OUTLINE)
        draw.polygon([(x+80,y+10),(x+86,y-1),(x+89,y+13)], fill=BODY, outline=OUTLINE)
        tail_swing = math.sin(phase*2*math.pi)*8
        draw.arc((x-6,y+4+tail_swing/3,x+33,y+44), 115, 300, fill=OUTLINE, width=4)
        s = math.sin(phase*2*math.pi)
        for lx, sign in [(28,1),(46,-1),(62,1),(75,-1)]:
            dx = 6*s*sign
            draw.line((x+lx,y+38,x+lx+dx,y+57), fill=OUTLINE, width=4)
            draw.line((x+lx+dx,y+57,x+lx+dx+4*sign,y+57), fill=OUTLINE, width=3)
        draw.ellipse((x+72,y+19,x+74,y+21), fill=(220,235,255,255))
        draw.ellipse((x+82,y+19,x+84,y+21), fill=(220,235,255,255))


frames = []
for i in range(TOTAL):
    img = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(img)
    d.line((28,92,732,92), fill=GROUND, width=2)
    d.text((W//2-42, 74), 'TRI DO', fill=MUTED)
    t = i / TOTAL

    if t < 0.30:
        p = t/0.30
        x = 20 + (330-20)*p
        draw_cat(d, x, 31, p*4, False)
    elif t < 0.55:
        p = (t-0.30)/0.25
        x = 330
        if p < 0.18:
            draw_cat(d, x, 31 + p*35, p*2, False)
        else:
            draw_cat(d, x-8, 38, p, True)
            zoff = int(3*math.sin(p*2*math.pi))
            d.text((428, 23-zoff), 'Z', fill=OUTLINE)
            d.text((445, 13-zoff), 'z', fill=(88,166,255,220))
            d.text((457, 6-zoff), 'z', fill=(88,166,255,180))
    elif t < 0.80:
        p = (t-0.55)/0.25
        x = 330 + (680-330)*p
        draw_cat(d, x, 31, p*4, False)
    else:
        p = (t-0.80)/0.20
        x = 680 - (680-20)*p
        layer = Image.new('RGBA', (110, 75), (0,0,0,0))
        ld = ImageDraw.Draw(layer)
        draw_cat(ld, 8, 5, p*4, False)
        layer = layer.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        img.alpha_composite(layer, (int(x), 26))

    frames.append(img.convert('P', palette=Image.Palette.ADAPTIVE))

frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=int(1000/FPS), loop=0, optimize=True, disposal=2)
print(f'Wrote {OUT}')
