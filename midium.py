'''中级交互类:Page'''
from junior import*
class Page(Blitable):
    def clear(self):
        self.button=self.scrollbar=self.text=self.textbox=[]
    def __init__(self, background:Surf, pos:tuple, size=None):
        self.background=background
        self.size=background.get_size() if size==None else size
        self.pos, self.cur=pos, (0, 0)
        self.button=[]
        self.scrollbar=[]
        self.textbox=[]
        self.text=[]
        self.running=F
    def switch(self):
        self.running=not self.running
    def add_scrollbar(self, scrollbar:ScrollBar=ScrollBar((0, 0)), mode=-4, rel_pos=(0, 0)):
        s=scrollbar.clone()
        s.pos=calc_pos(add(rel_pos, s.pos), self.size, s.size, mode)
        self.scrollbar.append(s)
    def add_button(self, button:Button, mode=-4, rel_pos=(0, 0)):
        b=button.clone()
        b.pos=calc_pos(add(rel_pos, b.pos), self.size, b.pic.get_size(), mode)
        self.button.append(b)
    def add_textbox(self, textbox:TextBox, mode=-4, rel_pos=(0, 0)):
        t=textbox.clone()
        t.pos=calc_pos(add(rel_pos, t.pos), self.size, t.size, mode)
        self.textbox.append(t)
    def add_text(self, text:Text=Text(""), mode=-4, rel_pos=(0, 0)):
        t=text.clone()
        t.pos=calc_pos(add(rel_pos, t.pos), self.size, t.image().get_size(), mode)
        self.text.append(t)
    def set_text(self, i=0, text:Text=Text(""), mode=-4, rel_pos=(0, 0)):
        t=text.clone()
        t.pos=calc_pos(add(rel_pos, t.pos), self.size, t.image().get_size(), mode)
        if i<len(self.text):
            self.text[i]=t
        else:
            self.text.append(t)
    def image(self, show_all=F):
        if show_all:
            board=self.background.copy()
            for L in [self.text, self.scrollbar, self.button, self.textbox]:
                for l in L:
                    l.blitme(board)
            return board
        
        board=self.background.copy().subsurface(self.cur, self.size)
        rc=Rect(self.cur, self.size)
        for L in [self.text, self.scrollbar[1:], self.button, self.textbox]:
            for l in L:
                if Rel(l.rect(), rc)>0:
                    l.blitme(board, -4, neg(self.cur))
        if len(self.scrollbar)>0:
            self.scrollbar[0].blitme(board)
        return board
    def deal(self, event:Event):
        for t in self.textbox:
            t.deal(event, self.pos)
        for s in self.scrollbar:
            s.deal(event, self.pos)
    def update(self):
        if len(self.scrollbar)>0:
            self.cur=(0, int(self.scrollbar[0].rate()*(self.background.get_size()[1]-self.size[1])))
        for t in self.textbox:
            t.update()

class ChatBox(Page):
    def __init__(self):
        pass
