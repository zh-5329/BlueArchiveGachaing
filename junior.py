'''初级交互类：Textbox, Scrollbar'''
from primary import*
class TextBox(Blitable):
    def clear(self):
        self.text=""
        self.tick=0
        self.work=F
        self.delete=0
        self.cur_at=0
        self.cur_move=0
    def __init__(self, size:tuple, pos:tuple, font:pg.font.Font=DFT_Font, initial_text:str="", line_break=F):
        '''pos:文本框的左上角'''
        '''title:标题图片(not used)'''
        '''size: 边框，文本框的大小'''
        '''font:字体'''
        '''bcol, ccol, ucol: 文本框颜色，文字颜色, 光标颜色（在 background!=None 时，acol 没有什么用）'''
        '''length:每一行文字个数上限'''
        '''rowh:行高'''
        '''cur_T, cur_delay, cur_width:光标闪烁周期, 光标移动延迟, 光标宽度'''
        '''del_delay:连续删除延迟'''
        self.clear()
        self.pos, self.size=pos, size
        self.text=initial_text
        self.font, self.length, self.rowh=font, -1, font.size("爨")[1]*1.2
        self.ccol, self.bcol, self.ucol=BLACK, WHITE, GRAY
        self.del_delay=DFT_Delete_Delay
        self.cur_delay=DFT_Cursor_Delay
        self.cur_T=DFT_Cursor_Period
        self.cur_width=1
    def set_color(self, char_color=BLACK, box_color=WHITE, cursor_color=GRAY):
        self.ccol, self.bcol, self.ucol=dcp(char_color), dcp(box_color), dcp(cursor_color)
    def set_cursor(self, cursor_period=DFT_Cursor_Period, cursor_delay=DFT_Cursor_Delay, cursor_width=1, cursor_color=GRAY):
        self.cur_T, self.cur_delay, self.cur_width, self.ucol=cursor_period, cursor_delay, cursor_width, dcp(cursor_color)
    def clone(self):
        textbox=TextBox(dcp(self.size), dcp(self.pos), self.font, dcp(self.text))
        textbox.set_color(self.ccol, self.bcol, self.ucol)
        textbox.length=self.length
        return textbox
    def draw_cursor(self, board:Surf):
        x=self.font.size(self.text[:self.cur_at])[0]
        pg.draw.line(board, self.ucol, (x, 2), (x, self.rowh-2), self.cur_width)
    def image(self):
        k=self.length
        s=self.text
        n=len(s)
        board=scp(self.size, self.bcol)
        if k!=-1:
            text=[s[i:min(i+k, n)]for i in range(0, (n+k-1)//k)]
            pass
        else:
            board.blit(self.font.render(self.text, T, self.ccol, self.bcol), (0, 0))
        if self.tick%self.cur_T<self.cur_T//2 and self.work:
            self.draw_cursor(board)
        return board
    def update(self):
        if not self.work:
            return
        self.tick+=1
        if self.delete>self.del_delay and self.cur_at!=0:
            self.text=self.text[:self.cur_at-1]+self.text[self.cur_at:]
            self.cur_at-=1
        if self.delete>0:
            self.delete+=1
        if self.cur_move!=0:
            self.cur_move+=sign(self.cur_move)
        if abs(self.cur_move)==1 or abs(self.cur_move)>self.cur_delay:
            self.cur_at=max(0, min(self.cur_at+sign(self.cur_move), len(self.text)))
    def deal(self, event:Event, rel_pos=(0, 0)):
        if not self.work:
            if event.type == pg.MOUSEBUTTONDOWN:
                if cover(self.rect(), minus(event.pos, rel_pos)):
                    self.work=T
            if not self.work:
                return
        if event.type == pg.MOUSEBUTTONDOWN:
            if not cover(self.rect(), minus(event.pos, rel_pos)):
                self.work=F
        elif event.type == pg.KEYDOWN:
            k=event.key
            u=event.unicode
            if k==pg.K_BACKSPACE:
                self.delete=1
                if self.cur_at!=0:
                    self.text=self.text[:self.cur_at-1]+self.text[self.cur_at:]
                    self.cur_at-=1
            elif k==pg.K_LEFT:
                self.cur_move=-1
                self.cur_at=max(0, min(self.cur_at-1, len(self.text)))
            elif k==pg.K_RIGHT:
                self.cur_move=1
                self.cur_at=max(0, min(self.cur_at+1, len(self.text)))
            elif k==pg.K_HOME:
                self.cur_at=0
            elif k==pg.K_END:
                self.cur_at=len(self.text)
            elif u.isascii() and len(u)==1 and 31<ord(u)<127:
                self.text=self.text[:self.cur_at]+u+self.text[self.cur_at:]
                self.cur_at+=1
        elif event.type == pg.KEYUP:
            self.cur_move=self.delete=0
    def detail(self):
        print(f"cursor: at={self.cur_at}, move={self.cur_move}, tick={self.tick}")
        print(f"delete: {self.delete}")
    def blitme(self, screen:Surf, mode=-4, pos=(0, 0)):
        self.update()
        super().blitme(screen, mode, pos)

class Slider(Button):
    def __init__(self, pic:Surf, lim:tuple, mode=1):
        '''mode:0水平, 1竖直(not used)'''
        super().__init__(pic, (0, lim[0]))
        self.lim, self.mode=lim, mode
        self.pos=(0, lim[0])
    def move(self, displace):
        self.pos=(0, min(self.lim[1], max(self.lim[0], self.pos[1]+displace)))
    def rate(self):
        return (self.pos[1]-self.lim[0])/(self.lim[1]-self.lim[0])
    def clone(self):
        return Slider(self.pic, dcp(self.lim), self.mode)

class ScrollBar(Blitable):
    def __init__(self, pos, bar_pic:Surf=pic_scrollbar, slider_pic:Surf=pic_slider, scroller_pic:Surf=pic_scroller, size=(24, 108), mode=1, scrollspeed=DFT_SCROLLSPEED):
        self.size, self.pos, self.mode=size, pos, mode
        self.bar_pic=bar_pic
        scr_size=scroller_pic.get_size()
        sld_size=  slider_pic.get_size()
        self.l=scr_size[1]
        scale(scroller_pic, (size[0], self.l))
        scale(  slider_pic, (size[0], self.l))
        self.bar_pic=scale(bar_pic, (size[0], size[1]-self.l*2))
        self.scroller=[Button(scroller_pic, (0, 0)), Button(flip(scroller_pic, 1), (0, size[1]-self.l))]
        self.follow=F
        self.state=0
        self.speed=scrollspeed
        self.slider=Slider(slider_pic, (self.l, size[1]-self.l-sld_size[1]))
    def clone(self):
        s=ScrollBar(dcp(self.pos), self.bar_pic, size=dcp(self.size), mode=self.mode, scrollspeed=self.speed)
        s.slider=self.slider.clone()
        s.scroller=[self.scroller[0].clone(), self.scroller[1].clone()]
        return s
    def switch(self, state=BLIT|WORK):
        self.state^=state
        self.slider.state=self.scroller[0].state=self.scroller[1].state=self.state
    def image(self):
        board=Surf(self.size)
        self.scroller[0].blitme(board)
        board.blit(self.bar_pic, (0, self.l))
        self.scroller[1].blitme(board)
        self.slider.blitme(board)
        return board
    def deal(self, event:Event, rel_pos=(0, 0)):
        if event.type == pg.MOUSEBUTTONDOWN:
            pos=minus(minus(event.pos, rel_pos), self.pos)
            if self.scroller[0].bepressed(pos):
                self.slider.move(-self.speed)
            elif self.scroller[1].bepressed(pos):
                self.slider.move(self.speed)
            elif self.slider.bepressed(pos):
                self.follow=T
        elif event.type == pg.MOUSEBUTTONUP:
            self.follow = F
        elif event.type == pg.MOUSEMOTION:
            if self.follow:
                self.slider.move(event.rel[self.mode])
    def rate(self):
        return self.slider.rate()

# class Figure(Blitable):
#     def __init__(self, variable):
#         self.v=variable