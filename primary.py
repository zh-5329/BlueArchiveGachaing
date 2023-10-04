'''基本交互类：Text, Button'''
from settings import*

class Blitable:
    def image(self)->Surf:
        pass
    def blitme(self, screen:Surf, mode=-4, pos=(0, 0)):
        '''mode:'''
        '''-4 -3 -2'''
        '''-1  0  1'''
        ''' 2  3  4'''
        i=self.image()
        image_size, screen_size=i.get_size(), screen.get_size()
        screen.blit(self.image(), calc_pos(add(pos, self.pos), screen_size, image_size, mode))
    def rect(self)->Rect:
        try:
            return Rect(self.pos, self.size)
        except:
            return Rect(self.pos, self.image().get_size())

class Text(Blitable):
    def __init__(self, text:str, pos:tuple=(0, 0), font:pg.font.Font=DFT_Font, char_color=(0, 0, 0), background_color=None):
        self.text, self.pos, self.font, self.ccol, self.bcol=text, pos, font, char_color, background_color
    def clone(self):
        return Text(dcp(self.text), dcp(self.pos), self.font, dcp(self.ccol), dcp(self.bcol)if self.bcol!=None else None)
    def image(self):
        if self.bcol!=None:
            return self.font.render(self.text, T, self.ccol, self.bcol)
        _c=conjugate_color(self.ccol)
        i=self.font.render(self.text, T, self.ccol, _c)
        i.set_colorkey(_c)
        return i

WORK=1
BLIT=2
class Button(Blitable):
    def __init__(self, pic:Surf, pos:tuple, text:Text=Text("")):
        self.pic, self.text, self.pos=pic, text, pos
        self.state=0
        self.num=0
    def clone(self):
        return Button(self.pic, dcp(self.pos), self.text.clone())
    def switch(self, state=WORK|BLIT):
        self.state^=state
    def bepressed(self, mouse_pos:tuple):
        return cover(self.rect(), mouse_pos) if self.state&WORK!=0 else F
    def press(self, mouse_pos:tuple):
        self.num+=self.bepressed(mouse_pos)
    def image(self):
        i=self.pic.copy()
        self.text.blitme(i, 0)
        return i
