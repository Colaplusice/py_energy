#encoding=utf-8
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import  os
import random
import math,string

font_path = '/Library/Fonts/Arial.ttf'

#几位验证码
number=4

#图片的高度和宽度
size=(100,40)

#背景
bgcolor=(255,255,255)

#字体颜色
fontcolor=(0,0,255)

#干扰颜色
linecolor=(255,0,0)


draw_line=True


line_number=(1,5)

#画线
def gene_line(draw,width,height):
    begin=(random.randint(0,width),random.randint(0,height))
    end=(random.randint(0,width),random.randint(0,height))
    draw.line([begin,end],fill=linecolor)


def gene_code(save_path,filename):
    width,height=size
    image=Image.new('RGBA',(width,height),bgcolor)

    font=ImageFont.truetype(font_path,25)
    draw=ImageDraw.Draw(image)

    text=gen_text()
    print(text)
    font_width,font_height=font.getsize(text)
    draw.text(((width-font_width)/number,(height-font_height)/number),text,fill=fontcolor)
    if draw_line:
        gene_line(draw,width,height)
        gene_line(draw,width,height)
        gene_line(draw,width,height)
        gene_line(draw,width,height)
        gene_line(draw,width,height)
    image=image.transform((width+20,height+10),
                          Image.AFFINE,
                          (1,-0.3,0,-0.1,1,0),
                          Image.BILINEAR
                          )
    #滤镜 边界加强
    # image=image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    # path=save_path+'/'+filename+'.png'
    # if not os.path.isfile(path):
    #     os.mkdir(path)
    image.save('%s/%s.png'%(save_path,filename))
    print("savepath:",save_path)
    return image,text

#生成验证码数字
def gen_text():
    #source是字母
    source=list(string.ascii_letters)
    for index in range(0,10):
        source.append(str(index))
            #返回随机生成的验证码和数字
        return ''.join(random.sample(source,number))

if __name__ == '__main__':
    gene_code('/Users/fanjialiang2401/Desktop','test')
