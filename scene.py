from school import*

START_INTERVAL=2000

class StartPage(Page):
    def __init__(self, background:Surf):
        super().__init__(background, (0, 0))
        self.add_button(BUTTON_START)
    def switch(self):
        super().switch()
        self.button[0].switch()
    def deal(self, event):
        super().deal(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            return self.button[0].bepressed(event.pos)
        else:
            return F
        
STARTPAGES=[StartPage(i) for i in START_PIC]

def calc_alpha(t, T):
    return int(448-64*(abs(5*t-T)+abs(5*t-4*T))/T)

class StartScene(Scene):
    def __init__(self, screen:Surf, player):
        super().__init__(screen, player, *STARTPAGES)
        self.page[-1].switch()
    def update(self):
        k=self.tick%(START_INTERVAL*len(STARTPAGES))//START_INTERVAL
        if self.tick%START_INTERVAL==0:
            self.page[k-1].switch(), self.page[k].switch()
        self.page[k].background.set_alpha(calc_alpha(self.tick%START_INTERVAL, START_INTERVAL))
        super().update()
    def deal(self, event):
        if event.type==pg.QUIT:
            exit()
        res=0
        for p in self.page:
            if p.running:
                res|=p.deal(event)
        if res:
            self.running=F
    def run(self):
        self.running=T
        while self.running:
            for event in pg.event.get():
                self.deal(event)
            self.update()



NAMING_LEN_LIM=15
NAMING_TITLE_TEXT=Text("回忆你的名字", (0, 0), font("SimYou", 40))
NAMING_EMPTYERROR_TEXT=Text("名字不能为空", (0, -100), font("SimHei", 32), RED)
NAMING_LENGTHERROR_TEXT=Text("名字长度不能超过%d"%NAMING_LEN_LIM, (0, -100), font("SimHei", 32), RED)
NAMING_TEXTBOX=TextBox((300, 40), (10, 60), font("SimHei", 20))
NAMING_BGPAGE=Page(pic_5, (0, 0))

class NamingPage(Page):
    def __init__(self, mode=0):
        super().__init__(scp((320, 720), TURQUOISE), (960, 0))
        self.add_button(BUTTON_ASSURE, 0)
        self.add_textbox(NAMING_TEXTBOX)
        self.add_text(NAMING_TITLE_TEXT, mode=-3)
        self.mode=mode
    def deal(self, event):
        super().deal(event)
        if event.type==pg.MOUSEBUTTONDOWN and self.button[0].bepressed(minus(event.pos, self.pos)):
            if 0<len(self.textbox[0].text)<=NAMING_LEN_LIM:
                return self.textbox[0].text
            else:
                self.set_text(1, NAMING_EMPTYERROR_TEXT if len(self.textbox[0].text)==0 else NAMING_LENGTHERROR_TEXT, 3)
        return ""
    def switch(self):
        super().switch()
        for i in [self.button, self.scrollbar]:
            for j in i:
                j.switch()

NAMINGPAGE=NamingPage()

class NamingScene(Scene):
    def __init__(self, screen:Surf, player):
        super().__init__(screen, player, NAMINGPAGE, NAMING_BGPAGE)
    def switch(self):
        self.page[0].switch()
        self.page[1].switch()
        self.running=T
    def deal(self, event:Event):
        super().deal(event)
        name=self.page[0].deal(event)
        if name:
            self.running=F
            self.p.name=name

SIZE_GACHAPAGE=(640, 670)
POS_GACHAPAGE=(640, 50)
pic_gachaBG=scp(SIZE_GACHAPAGE, AZURE)
pic_gachaBG.blit(pic_select, calc_pos((0, 0), SIZE_GACHAPAGE, pic_select.get_size(), 3))
pic_STUDENTPAGE=scp((640, (len(stu)+8)*(SMALLHEIGHT+20)), AZURE)
class StudentPage(Page):
    def __init__(self, player):
        super().__init__(pic_STUDENTPAGE.copy(), POS_GACHAPAGE, SIZE_GACHAPAGE)
        self.p=player
        self.add_scrollbar(ScrollBar((0, 0), size=(24, 480)))
    def switch(self):
        super().switch()
        self.update(self.running)
        self.scrollbar[0].switch()
    def update(self, flag=F):
        super().update()
        if not self.running or not flag:
            return
        self.background=pic_STUDENTPAGE.copy()
        for i in range(len(stu)):
            stu[i].blitme(self.background, (30, i*SMALLHEIGHT+20), 1, -4)
            Text(f"{self.p.stu[i]}", (0, 0),  font("SimHei", 30), (20, 20, 60)).blitme(self.background, -4, (330, i*SMALLHEIGHT+100))
        
class GachaPage(Page):
    def __init__(self):
        super().__init__(pic_gachaBG, POS_GACHAPAGE)
        self.add_button(BUTTON_ONE, -1, (5, 200))
        self.add_button(BUTTON_TEN, 1, (-5, 200))
        self.add_button(BUTTON_SELECT, 4)
        self.num=0
    def switch(self):
        super().switch()
        for b in self.button:
            b.switch()
    def deal(self, event):
        if event.type==pg.MOUSEBUTTONDOWN:
            for i in range(len(self.button)):
                if self.button[i].bepressed(minus(event.pos, self.pos)):
                    return i
        return -1
    def one(self, flag):
        if flag:
            return stu_star[3][choose([1]*len(stu_star[3]))]
        s=choose(psb)
        return stu_star[s][choose([1]*len(stu_star[s]))]
    def ten(self, flag):
        s=[choose(psb)for i in range(10)]
        if not flag and s[9]<2:
            s[9]=2
        if flag and s[9]<3:
            s[9]=3
        return [stu_star[s[i]][choose([1]*len(stu_star[s[i]]))] for i in range(10)]
    def image(self):
        i=super().image()
        Text(f"{self.num}", (330, 615), font("SimHei", 30), AZURE).blitme(i)
        return i
pic_UIPage=scp((640, 50), DARKAZURE)
pic_UIPage.blit(pic_stone, (160, 5))
pic_UIPage.blit(pic_qui, (320, 5))
class GachaUIPage(Page):
    def __init__(self, player):
        super().__init__(pic_UIPage, (640, 0))
        self.p=player
        self.add_button(BUTTON_STU, -4, (5, 5))
    def switch(self):
        super().switch()
        for b in self.button:
            b.switch()
    def image(self):
        i=super().image()
        i.blit(Text(f"{self.p.stone}", (0, 0), font("SimHei", 30), (20, 20, 60)).image(), (200, 5))
        return i
    def deal(self, event):
        if event.type==pg.MOUSEBUTTONDOWN:
            if self.button[0].bepressed(minus(event.pos, self.pos)):
                return T
        return F

GETPOS=[(i*130+10, 10)for i in range(5)]+[(i*130+10, 200)for i in range(5)]
SIZE_GACHAGETPAGE=(640, 720)

class GachaGetPage(Page):
    def __init__(self):
        super().__init__(pic_archive, (0, 0))
        self.add_button(BUTTON_ASSURE, 3, rel_pos=(0, -10))
        self.id=None
    def image(self):
        if self.id==None:
            return self.background
        i=scp(SIZE_GACHAGETPAGE, TURQUOISE)
        if type(self.id)==list:
            for j in range(len(self.id)):
                stu[self.id[j]].blitme(i, GETPOS[j], 0.5, -4)
        else:
            stu[self.id].blitme(i)
        return i
    def deal(self, event):
        if event.type==pg.MOUSEBUTTONDOWN:
            return self.button[0].bepressed(minus(event.pos, self.pos))

class GachaScene(Scene):
    def __init__(self, screen, player):
        super().__init__(screen, player, GachaPage(), GachaUIPage(player), GachaGetPage(), StudentPage(player))
        self.num=self.cnt=0
    def switch(self):
        super().switch()
        self.page[0].switch()
        self.page[1].switch()
        self.page[2].switch()
    def deal(self, event):
        super().deal(event)
        if self.page[0].running:
            flag=self.page[0].deal(event)
            if flag==0:
                self.one()
            if flag==1:
                self.ten()
            if flag==2:
                pass
        self.page[0].num=self.num
        if self.page[1].running:
            flag=self.page[1].deal(event)
            if flag:
                self.page[0].switch()
                self.page[3].switch()
        if self.page[3].running:
            flag=self.page[3].deal(event)
            if flag:
                pass
    def one(self):
        if self.p.stone<ONE_STONE:
            return 0
        self.p.use_stone(ONE_STONE)
        self.num+=1
        self.cnt+=1
        if self.cnt>=gUARANTEE:
            id=self.page[0].one(T)
            self.cnt=0
        else:
            id=self.page[0].one(F)
            if stu[id].star==3:
                self.cnt=0
        self.p.get(id)
        self.page[2].id=id
        return 1
    def ten(self):
        if self.p.stone<TEN_STONE:
            return 0
        self.p.use_stone(TEN_STONE)
        self.num+=10
        self.cnt+=10
        if self.cnt>=gUARANTEE:
            id=self.page[0].ten(T)
            self.cnt=0
        else:
            id=self.page[0].ten(F)
            if 3 in [stu[i].star for i in id]:
                self.cnt=0
        for i in id:
            self.p.get(i)
        self.page[2].id=id
        return 1