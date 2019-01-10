# coding:utf-8

import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter


chars = string.digits + string.ascii_letters



def rndChars(bit_num=4):
    global chars
    chars = random.sample(chars, bit_num)

def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


def rndChar(i):
    return chars[i]

def rndColor2():
    return (random.randint(30, 120), random.randint(30, 120), random.randint(30, 120))

def genCode():
    height = 60
    width = 240
    image = Image.new('RGB', (width, height), (255, 255, 255))  # 白色画布
    font = ImageFont.truetype(r"C:\Windows\Fonts\Arial.ttf", 36)  # 画笔字体
    draw = ImageDraw.Draw(image)  # 绘画对象
    for i in range(width):
        for j in range(height):
            draw.point((i, j), fill=rndColor())  # 随机逐像素填充颜色


    for i in range(4):
        draw.text((60 * i + 10, 10), rndChar(i),
                font=font, fill=rndColor2())  # 文本绘画

    image = image.filter(ImageFilter.BLUR)  # 产生模糊感
    image.save('code.jpg', 'jpeg')
    image.show()

rndChars()
genCode()
