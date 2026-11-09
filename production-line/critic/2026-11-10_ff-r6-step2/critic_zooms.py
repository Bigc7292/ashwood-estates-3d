from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS=None
P=Image.open('/workspace/critic-wt-first-floor/active/approved-cad-v4/png/FP-4B-FF_V4_long7680.png').convert('RGB')
O=Image.open('r6_overlay_long.png').convert('RGB')
k=0.18307; X=lambda x:int(1278.9+x*k); Y=lambda y:int(1334.5+y*k)
Z={'bath1_lift_D4':(7500,6800,13200,9700,2),'bed2_dress_D8_D12':(2400,13400,4900,17300,3),'jdress_D9_D10_D11':(7700,13900,12900,17300,2),'W9_bed2_south':(0,19600,4700,21300,2),'mbath_showers':(0,10500,4600,13700,2),'jbath_shower':(10000,13900,13000,17200,2),'bath2':(0,13600,3000,16500,3)}
for n,(a,b,c,dd,s) in Z.items():
    box=(X(a),Y(b),X(c),Y(dd)); p=P.crop(box); o=O.crop(box); W,H=p.width*s,p.height*s
    m=Image.new('RGB',(W*2+10,H+20),'white'); m.paste(p.resize((W,H),Image.LANCZOS),(0,20)); m.paste(o.resize((W,H),Image.LANCZOS),(W+10,20))
    ImageDraw.Draw(m).text((4,4),f'{n}: LEFT V4 FF long7680 x{s} | RIGHT critic overlay of r6 data',fill='black'); m.save(f'z_{n}.png'); print(n,m.size)
