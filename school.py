from pre import*
name_width=6
school_width=6
club_width=6
school=["无", "歌赫娜", "崔尼蒂", "千禧年", "阿拜多斯", "百鬼夜行", "山海经", "红冬"]
club=["无"]
snum=len(school)
class Student:
    def __init__(self, id:int, name:str, star:int, school_id:int, club_id:int, picture:Surf):
        self.id, self.name, self.star, self.sid, self.cid, self.pic=id, name, star, school_id, club_id, picture
    def __str__(self):
        return f'{self.id} {self.name} {self.star} {self.sid} {self.cid}'
    def tostr(self):
        return f'{setlen(self.name, name_width)}: {self.star}, {setlen(school[self.sid], school_width)}, {setlen(club[self.cid], club_width)}, {self.id}'
    def modify(self, variable_name, x):
        v=variable_name
        if v=='name':
            self.name=x
        elif v=='star':
            self.star=x
        elif v=='sid':
            self.sid=x
        elif v=='cid':
                self.cid=x
    def clone(self):
        return Student(dcp(self.name), self.star, self.sid, self.cid)
    def init(file_name:str):
        pass
    def image(self, size=None):
        i=self.pic.copy()
        if size!=None:
            i=scale(i, size)
        return i
    def blitme(self, screen:Surf, pos=(0, 0), size=None, mode=0):
        i=self.image(size)
        screen.blit(i, calc_pos(pos, screen.get_size(), i.get_size(), mode))
stu=[]
stu_star=[[], [], [], []]
class Teacher:
    def __init__(self, id:int, name:str, file="sensei.txt"):
        self.id, self.name=id, name
        self.stone=0
        self.qui=0
        self.file=file
    def init(self, num):
        self.stu=[0]*num
    def get_stone(self, num:int):
        self.stone+=num
    def use_stone(self, num:int):
        self.stone-=num
    def clone(self, id:int):
        T=Teacher(id, dcp(self.name))
        T.get_stone(self.stone)
        return T
    def save(self):
        f=open(DFT_USERFOLDER+"/"+self.file, "w")
        f.write(f"{self.id} {self.name} {self.file} {self.stone}\n")
        f.write(f"")
    def get(self, stu_id):
        self.stu[stu_id]+=1
def stu_init():
    f=open("list.txt", 'r')
    l=f.readlines()
    for i in range(len(l)):
        L=l[i].split(' ')
        stu.append(Student(i, L[0], int(L[1]), int(L[2]), int(L[3]), picture(L[4].strip())))
    for i in stu:
        stu_star[i.star].append(i.id)