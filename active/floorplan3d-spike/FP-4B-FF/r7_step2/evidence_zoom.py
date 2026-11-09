import sys
from PIL import Image, ImageDraw
R=4; U0=(110,100)
src=Image.open('work.png')
def z(ux0,uy0,ux1,uy1,s,out):
    im=src.crop((int((ux0-U0[0])*R),int((uy0-U0[1])*R),int((ux1-U0[0])*R),int((uy1-U0[1])*R))).resize((int((ux1-ux0)*s),int((uy1-uy0)*s)),Image.LANCZOS)
    d=ImageDraw.Draw(im)
    for x in range((ux0//5+1)*5,ux1,5):
        X=(x-ux0)*s; d.line([(X,0),(X,im.height)],fill=(255,0,0) if x%10==0 else (255,190,190),width=1)
        if x%10==0: d.text((X+1,1),str(x),fill=(220,0,0)); d.text((X+1,im.height-12),str(x),fill=(220,0,0))
    for y in range((uy0//5+1)*5,uy1,5):
        Y=(y-uy0)*s; d.line([(0,Y),(im.width,Y)],fill=(0,0,255) if y%10==0 else (190,190,255),width=1)
        if y%10==0: d.text((1,Y+1),str(y),fill=(0,0,220)); d.text((im.width-24,Y+1),str(y),fill=(0,0,220))
    im.save(out)
z(*map(int,sys.argv[1:6]),sys.argv[6])
