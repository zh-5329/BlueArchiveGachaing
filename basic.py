import pygame as pg
import os
from geometry import*

pg.init()

Rect=pg.Rect
Surf=pg.Surface
Font=pg.font.Font
Event=pg.event.Event

'''file'''
DFT_PICTUREFOLDER="picture"
DFT_USERFOLDER="user"
DFT_STUFOLDER="stu"#not used
CODE=['UTF-8', 'GBK', 'ASCII', 'UTF-16', 'GB18030', 'BIG5', 'ISO-88591', 'GB23112']
def getcode(data:bytes):
    for code in CODE:
        try:
            data.decode(code)
            if code == 'UTF-8' and data.startswith(b'\xef\xbb\xbf'):
                return 'UTF-8-SIG'
            return code
        except UnicodeDecodeError:
            continue
    return ""
def scan_dir(filepath):
    files=os.listdir(filepath)
    res=[[], []]
    for file in files:
        file_d=os.path.join(filepath, file)
        res[os.path.isdir(file_d)].append(file_d)
            

'''random select'''
def bin_Schoose(Sposibility:list):
    l, r=0, len(list)
    x=random()
    while l<r:
        mid=(l+r)//2
        if Sposibility[mid]<=x:
            r=mid
        else:
            l=mid+1
    return l
def Schoose(Sposibility:list):
    x, i=np.random.uniform(0, Sposibility[-1]), 0
    while Sposibility[i]<=x: i+=1
    return i
def choose(posibility:list):
    Sposibility=[posibility[0]]
    for i in range(1, len(posibility)):
        Sposibility.append(Sposibility[i-1]+posibility[i])
    return Schoose(Sposibility)
def select(items:dict):
    K, V=items.keys(), items.values()
    return K[choose(V)]

'''string operation'''
def setlen(s, l):
    return s[:l] if len(s)>l else s+'  '*(l-len(s))

'''image'''
def picture(filename:str):
    return pg.image.load(DFT_PICTUREFOLDER+"/"+filename)
def Textpic(text:str, font:Font, char_color=(0, 0, 0), background_color=(255, 255, 255)):
    return font.render(text, T, char_color, background_color)
def cover(rect:Rect, A):
    return rect.left<=A[0]<=rect.right and rect.top<=A[1]<=rect.bottom
def scale(pic:Surf, k):
    return pg.transform.scale(pic, k) if type(k)==tuple else pg.transform.scale(pic, mul(k, pic.get_size()))
def flip(pic:Surf, flip_mode=0):
    '''0: 不翻转, 1:竖直翻转, 2:水平翻转, 3:中心翻转'''
    return pg.transform.flip(pic, flip_mode>>1, flip_mode&1)
def single_color_pic(size:tuple, color:tuple):
    s=Surf(size)
    s.fill(color)
    return s
def calc_pos(pos:tuple, screen_size:tuple, image_size:tuple, mode:int):
    '''mode:'''
    '''-4 -3 -2'''
    '''-1  0  1'''
    ''' 2  3  4'''
    return add(pos, ((mode+4)%3*(screen_size[0]-image_size[0])//2, (mode+4)//3*(screen_size[1]-image_size[1])//2))
def rel(A, B):
    if A[0]> A[1]: A[0], A[1]=A[1], A[0]
    if B[0]> B[1]: B[0], B[1]=B[1], B[0]
    if B[1]< A[0]  or A[1]< B[0]: return 0
    if A[0]<=B[0] and B[1]<=A[0]: return 1
    if B[0]<=A[0] and A[1]<=B[0]: return 2
    return 3
def Rel(A:Rect, B:Rect):
    i, j=rel((A.left, A.right), (B.left, B.right)), rel((A.top, A.bottom), (B.top, B.bottom))
    return i if i==j else 0 if i==0 or j==0 else 3
def conjugate_color(rgb:tuple):
    return ((rgb[0]+128)&255, (rgb[1]+128)&255, (rgb[2]+128)&255)

def opp_color(rgb:tuple):
    return (rgb[0]^255, rgb[1]^255, rgb[2]^255)