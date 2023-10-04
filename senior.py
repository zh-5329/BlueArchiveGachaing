'''高级交互类：Scene'''
from midium import*


class Scene:
    def __init__(self, screen:Surf, player, mainpage, *args):
        self.screen=screen
        self.tick=0
        self.running=F
        self.p=player
        self.page=[mainpage]
        for i in args:
            if isinstance(i, Page):
                self.page.append(i)
    def switch(self):
        self.running=not self.running
    def add_page(self, page):
        self.page.append(page)
    def blitme(self):
        for page in self.page:
            if page.running:
                page.blitme(self.screen)
    def update(self):
        self.tick+=1
        for page in self.page:
            page.update()
        self.blitme()
        pg.display.update()
    def deal(self, event):
        if event.type==pg.QUIT:
            self.p.save()
            exit()
    def run(self):
        while self.running:
            for event in pg.event.get():
                self.deal(event)
            self.update()
            CLOCK.tick(fps)

class PictureScene(Scene):
    def __init__(self, screen:Surf, player, page, T=600):
        self.screen=screen
        self.tick=0
        self.running=F
        self.p=player
        self.page=[page]
    def switch(self):
        super().switch()
        self.page[0].switch()

class TimeScene(Scene):
    def __init__(self, screen:Surf, player, T, page, *args):
        super().__init__(screen, player, page, *args)
        self.T=T
    def switch(self):
        super().switch()
        for p in self.page:
            p.switch()
    def update(self):
        print(self.tick, self.T)
        if self.tick>=self.T:
            self.running=F
        super().update()