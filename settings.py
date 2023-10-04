from basic import*
'''colors(RGB)'''
RED=(255, 0, 0)
BLUE=(0, 0, 255)
GREEN=(0, 255, 0)
BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
YELLOW=(255, 255, 0)
PURPLE=(255, 0, 255)
CYAN=(0, 255, 255)
TURQUOISE=(64, 224, 205)
BROWN=(128, 42, 42)
ORANGE=(255, 128, 0)
GRAY=(192, 192, 192)
PINK=(255, 192, 203)
NAVY=(0, 0, 128)
AZURE=(240, 255, 255)
DARKAZURE=(190, 230, 230)
DARKTURQUIZE=(44, 74, 84)

'''time'''
CLOCK=pg.time.Clock()
fps = 30
DFT_Cursor_Period = 20
DFT_Cursor_Delay = 12
DFT_Delete_Delay = 12
DFT_SCROLLSPEED = 1
'''size'''
W, H=1280, 720

'''pictures'''
pic_cross=picture("cross.png")
pic_heart=picture("heart.png")
pic_slider=picture("slider.png")
pic_scroller=picture("scroller.png")
pic_scrollbar=picture("scrollbar.png")
scp=single_color_pic
'''fonts'''
text_size=14
title_size=24
_TimesNewRomanNames=['TimesNewRoman', 'Times', "TNR"]
_SimHeiNames=['SimHei', 'msyh', "雅黑", "微软雅黑"]
_SimHeiBNames=['SimHeiB', '雅黑粗体']
_SimYouNames=['SimYou', '幼圆']
_ConsolasNames=['Consolas', 'Csls', 'C']
_ConsolasINames=['ConsolasI', 'Cslsi', 'Ci', 'Consolasi', 'CslsI', 'CI']
Font_names={'SimYou':_SimYouNames, 'SimHei':_SimHeiNames, 'SimHeiB':_SimHeiBNames, 
            'Consolas':_ConsolasNames, 'ConsolasI':_ConsolasINames, 'TimesNewRoman':_TimesNewRomanNames}
Font_Name={name:stdname for stdname in Font_names.keys() for name in Font_names[stdname]}
Font_File={'TimesNewRoman':'font/times.ttf', 'Consolas':'font/Consola.ttf', 'ConsolasI':'font/Consolai.ttf', 
           'SimHei':'font/msyh.ttc', 'SimHeiB':'font/msyhbd.ttc', 'SimYou':'font/SIMYOU.ttf'}
def font(name:str, size:int=text_size):
    return Font(Font_File[Font_Name[name]], size)
DFT_Font=font("SimHei", text_size)