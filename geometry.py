from math import*
from copy import*
import numpy as np
from random import*


T, F=True, False
dcp=deepcopy

'''Point(2D-vector): 2D-tuple'''
def _add(A, B):
    return (A[0]+B[0], A[1]+B[1])
def add(A, B, *args):
    _=_add(A, B)
    for i in args:
        _=_add(_, i)
    return _
def minus(A, B):
    return (A[0]-B[0], A[1]-B[1])
def neg(A):
    return (-A[0], -A[1])
def iprod(A, B):
    return A[0]*B[0]+A[1]*B[1]
def oprod(A, B):
    return A[0]*B[1]-A[1]*B[0]
def size(A):
    return sqrt(iprod(A, A))
def mul(k, A):
    return (k*A[0], k*A[1])
def floordiv(A, k):
    return (A[0]//k, A[1]//k)
def quan(A: tuple):
    return mul(1/size(A), A)
def dist(A, B):
    return size(A-B)
def rotate(A, ar, O=(0, 0)):
    if O[0]==0 and O[1]==0:
        return (A[0]*cos(ar)-A[1]*sin(ar), A[0]*sin(ar)+A[1]*cos(ar))
    return add(O, rotate(A-O, ar))
def sign(x):
    return 0 if x==0 else -1 if x<0 else 1
def arg(x, y):
    if (x==0 and y==0):
        return 0.0
    x/=sqrt(x*x+y*y)
    ar=acos(x)
    return ar if y>=0 else 2*pi-ar
def Arg(A):
    return arg(A[0], A[1])
def direct(ar):
    return (cos(ar), sin(ar))
def pval(ar:float):
    '''[0, 2pi)'''
    return ar-2*pi*int(ar/(2*pi))

class Line:
    '''ax+by+c=0'''
    def _init(self, a, b, c):
        self.a, self.b, self.c=a, b, c
    def __init__(self, *args, **kwargs):
        if len(args)==3:
            self._init(*args)
        elif len(args)==2 and kwargs[0]==tuple and kwargs[1]==float:
            A, ar=args[0], args[1]
            self._init(sin(ar), -cos(ar), cos(ar)*A[1]-sin(ar)*A[0])
        elif len(args)==2 and kwargs[0]==tuple and kwargs[1]==tuple:
            self=Line(args[0], Arg(args[0]-args[1]))
    def __call__(self, A:tuple):
        return self.a*A[0]+self.b*A[1]+self.c
    def arg(self):
        return arg(self.b, -self.a)
    def size(self):
        return sqrt(self.a*self.a+self.b*self.b)
    def __getitem__(self, i:int):
        return self.a if i==0 else self.b if i==1 else self.c
    def __setitem__(self, i:int, k):
        self[i]=k
    def cross(self, A:tuple):
        return self(A)==0
    def __mod__(a, b):
        return Line(a.b*b.c-a.c*b.b, a.c*b.a-b.c*a.a, a.a*b.b-a.b*b.a)
    def __neg__(self):
        return Line(-self.a, -self.b, -self.c)
    def __rmul__(self, k):
        return Line(k*self.a, k*self.b, k*self.c)
    def __mul__(self, k):
        return k*self
    def __str__(self):
        return f"<Line>{(self.a, self.b, self.c)}"
    def __and__(a, b):
        _=a%b
        return (_.a/_.c, _.b/_.c)
    def __or__(a, b):
        return a.a*b.b-a.b*b.a==0 
    def __eq__(a, b):
        _=a%b
        return _.a==_.b==_.c==0
    def sdist(self, A:tuple):
        return self(A)/size((self.a, self.b))
    def dist(self, A:tuple):
        return abs(self.sdist(A))
    def rotate(self, ar, O:tuple):
        B=rotate((self.a, self.b), ar)
        return Line(B[0], B[1], self.c)
    def move(self, direct:tuple):
        return Line(self.a, self.b, self.c-self.a*direct[0]-self.b*direct[1])
    def k(self):
        return self.a/-self.b
    def clone(self):
        return Line(self.a, self.b, self.c)
    
class Ray:
    '''x=x0+t*cos(ar), y=y0+t*sin(ar)'''
    def __init__(self, start:tuple, ar:float):
        self.s, self.ar=start, pval(ar)
    def __init__(self, start:tuple, A:tuple):
        self.s, self.ar=start, Arg(A-start)
    def __neg__(self):
        return Ray(self.s, pi+self.ar)
    def __invert__(self):
        return Ray(self.s, -self.ar)
    def __call__(self, A:tuple):
        r, t=A-self.s, direct(self.ar)
        return (iprod(r, t), oprod(r, t))
    def cross(self, A:tuple):
        C=self(A)
        return C[0]>=0 and C[1]==0
    def dist(self, A:tuple):
        C=self(A)
        return C[1] if C[0]>=0 else sqrt(C[0]*C[0]+C[1]*C[1])
    def rotate(self, ar, O:tuple):
        return Ray(rotate(self.s, ar), self.ar+ar)
    def move(self, direct:tuple):
        return Ray(add(self.s, direct), self.ar)
    def __str__(self):
        return f"<Ray>{self.s, self.ar}"
    def at(self, x, y):
        return add(self.s, direct(self.ar)*x, direct(self.ar+pi/2)*y)
    def toLine(self):
        return Line(self.s, self.ar)
    def clone(self):
        return Ray(dcp(self.s), self.ar)

class Seg:
    '''A:(xA, yA), B:(xB, yB)'''
    def __init__(self, A:tuple, B:tuple):
        self.A, self.B=A, B
    def __init__(self, xA, yA, xB, yB):
        self.A, self.B=(xA, yA), (xB, yB)
    def size(self):
        return size(self.A-self.B)
    def arg(self):
        return Arg(self.B-self.A)
    def __call__(self, P:tuple):
        r, t, I=P-self.A, self.B-self.A, self.size()
        return (iprod(r, t)/I**2, oprod(r, t)/I**2)
    def __neg__(self):
        return Seg(self.B, self.A)
    def __invert__(self):
        return Seg(self.A[0], self.B[1], self.A[1], self.B[0])
    def cross(self, P:tuple):
        C=self(P)
        return 0<=C[0]<=1 and C[1]==0
    def dist(self, P:tuple):
        C=self(P)
        return C[1] if 0<=C[0]<=1 else min(dist(self.A, P), dist(self.B, P))
    def __and__(S1, S2):
        L1, L2=Line(S1.A, S1.B), Line(S2.A, S2.B)
        if L1==L2:
            A, B=S1(S2.A), S1(S2.B)
            if A[0]>B[0]:
                A, B=B, A
            if (B[0]<=1):
                return [] if B[0]<0 else [S1.A] if B[0]==0 else [S1.A if A[0]<=0 else S2.A, S2.B]
            else:
                return [] if A[0]>1 else [S1.B] if A[0]==1 else [S1.A if A[0]<=0 else S2.A, S1.B]
        elif (L1|L2):
            return []
        P=L1&L2
        return [P] if S1.cross(P) and S2.cross(P) else []
    def bisector(self):
        return Line(mul(0.5, add(self.A, self.B)), self.arg()+pi/2)
    def toLine(self):
        return Line(self.A, self.B)
    def toRay(self):
        return Ray(self.A, self.B)
    def clone(self):
        return Seg(dcp(self.A), dcp(self.B))

def _sS(A, B, C):
    return iprod(B-A, C-A)
def sS(A, B, C, *args):
    s=_sS(A, B, C)
    return s if len(args)==0 else s+_sS(A, C, args[0])+sum([_sS(A, args[i], args[i+1])for i in range(len(args)-1)])
def S(*args):
    return abs(sS(*args))
def div_point(A, B, k):
    '''定比分点'''
    return mul(1/(k+1), add(A, mul(k, B)))
def vert(A:tuple, l):
    '''垂线'''
    if type(l)==Line:
        return Line(A, l.arg()+pi/2)
    try:
        return vert(A, l.toLine())
    except:
        return vert(A, Line(l))
def para(A:tuple, l):
    '''平行线'''
    if type(l)==Line:
        return Line(A, l.arg())
    try:
        return para(A, l.toLine())
    except:
        return para(A, Line(l))
def Pbisector(A:tuple, B:tuple):
    '''中垂线'''
    return vert(div_point(A, B, 1), Line(A, B))
def Lbisector(l1:Line, l2:Line):
    '''角平分线'''
    if (l1.arg()==l2.arg()):
        return Line(l1.a, l1.b, (l1.c/l1.size()+l2.c/l2.size())/2)
    elif (l1|l2):
        return None
    return l1.rotate(pval(l2.arg()-l1.arg())/2, l1&l2)

class Circle:
    def _init(self, O:tuple, r):
        self.O, self.r=O, r
    def __init__(self, *args):
        if len(args==2):
            if type(args[1]==tuple):
                self._init(args[0], dist(args[0], args[1]))
            else:
                self._init(args[0], args[1])
        elif len(args==3):
            A, B, C=args[0], args[1], args[2]
            self.O=Pbisector(A, B)&Pbisector(A, C)
            self.r=dist(self.O, A)
    def __init__(self, a:Line, b:Line, c:Line):
        self.O=Lbisector(a, -b)&Lbisector(b, -c)
        self.r=a.dist(self.O)
    def __call__(self, A:tuple):
        return size(minus(A, self.O))-self.r
    def __call__(self, l:Line):
        L=l.move(neg(self.O))
        return (L.a*L.a+L.b*L.b)*self.r*self.r-L.c*L.c
    def clone(self):
        return Circle(dcp(self.O), self.r)

class arc:
    def __init__(self, O:tuple, r:float, arg:tuple, direct=1):
        self.O, self.r, self.arg=O, r, arg, direct
    def __init__(self, A:tuple, B:tuple, C:tuple):
        O=Circle(A, B, C)
        a, b, c=Arg(A-O.O), Arg(B-O.O), Arg(C-O.O)
        self.arg=(a, c)
        self.direct=1 if a<b<c or b<c<a or c<a<b else -1
        self.O=O.O