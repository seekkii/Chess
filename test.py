from dataclasses import replace
import sys
from turtle import update
from sqlalchemy import false, true
from tables import Col
import wx



row, col = (8, 8)
arr = [[' ']*8 for _ in range(8)]
castle_white = true
castle_black = true


arr[0][0] = 'br'
arr[0][1] = 'bK'
arr[0][2] = 'bb'
arr[0][3] = 'bq'
arr[0][4] = 'bk'
arr[0][5] = 'bb'
arr[0][6] = 'bK'
arr[0][7] = 'br'

arr[7][0] = 'wr'
arr[7][1] = 'wK'
arr[7][2] = 'wb'
arr[7][3] = 'wq'
arr[7][4] = 'wk'
arr[7][5] = 'wb'
arr[7][6] = 'wK'
arr[7][7] = 'wr'

for i in range(8):
    arr[1][i] = "bp"
for i in range(8):
    arr[6][i] = "wp"

def exist(x,y):
    if x >-1 and x < 8 and y >-1 and y < 8:
        return True

def pmoveb(x,y):
    if x == 1:
        if arr[x][y] == 'bp':
            if arr[x+2][y] == ' ':
                arr[x+2][y] = 'x'
                arr[x+1][y] = 'x'#if x is in first rank, mark 2 squares aboves as valid move
    
   
    if exist(x+1,y-1):
        if (arr[x+1][y-1])[0] == 'w':
            arr[x+1][y-1] = "x%s" % arr[x+1][y-1]
    
    if exist(x+1,y+1):
        if (arr[x+1][y+1])[0] == 'w':
            arr[x+1][y+1] = "x%s" % arr[x+1][y+1]
    
    if exist(x+1,y):
        if (arr[x+1][y])[0] == ' ':
            arr[x+1][y] = 'x' 
    
    return arr

def pmovew(x,y):
    if x == 6:
        if arr[x][y] == 'wp':
            if arr[x-2][y] == ' ':
                arr[x-2][y] = 'x'
                arr[x-1][y] = 'x'
   
    if exist(x-1,y+1):
        if (arr[x-1][y+1])[0] == 'b':
            arr[x-1][y+1] = "x%s" % arr[x-1][y+1]
    
    if exist(x-1,y-1):
        if (arr[x-1][y-1])[0] == 'b':
            arr[x-1][y-1] = "x%s" % arr[x-1][y-1]
    
    if exist(x-1,y):
        if (arr[x-1][y])[0] == ' ':
            arr[x-1][y] = 'x' 

    return arr

def kingm(x,y,side):
    for j in range(3):
        for i in range(3):
            if exist(x - 1 + j, y - 1 + i):
                if arr[x - 1 + j][y - 1 + i] == ' ':
                    arr[x - 1 + j][y - 1 + i] = 'x'
                else:
                    if arr[x-1+j][y- 1 + i][0] != arr[x][y][0]:
                        arr[x-1+j][y-1+i] = "x%s" % arr[x-1+j][y-1+i]

    return arr

def bim(x,y,side):
    avail = [[[x + i, y + i] for i in range(1, 8)],
                 [[x + i, y- i] for i in range(1, 8)],
                 [[x - i, y + i] for i in range(1, 8)],
                 [[x - i, y - i] for i in range(1, 8)]]

    for i in (avail):
        for j in i:
            if exist(j[0],j[1]):
                if arr[j[0]][j[1]] == ' ':
                    arr[j[0]][j[1]] = 'x'
                else:
                    if (arr[j[0]][j[1]])[0] != side:
                        arr[j[0]][j[1]] = "x%s" %  arr[j[0]][j[1]]
                    break
    return arr
    
def rom(x,y,side):
    avail = [[[x + i, y] for i in range(1, 8 - x)],
             [[x - i, y] for i in range(1, x + 1)],
             [[x, y + i] for i in range(1, 8 - y)],
             [[x, y - i] for i in range(1, y + 1)]]

    for i in avail:
        for j in i:
            if exist(j[0],j[1]):
                if arr[j[0]][j[1]] == ' ':
                    arr[j[0]][j[1]] = 'x'
                else:
                    if arr[j[0]][j[1]][0] != side:
                        arr[j[0]][j[1]] = "x%s" %  arr[j[0]][j[1]]
                    break
    return arr

def Km(x,y,side):
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i ** 2 + j ** 2 == 5:
                if exist(x + i, y + j):
                    if arr[x + i][y + j] == ' ':
                        arr[x + i][y + j] = 'x'
                    else:
                        if arr[x + i][y + j][0] != side:
                            arr[x + i][y + j] = "x%s" %  arr[x+i][y+j]
    return arr

def qm(x,y,side):
    bim(x,y,side)
    rom(x,y,side)
    return arr

def in_check(side):
    for i in range (row):
        for j in range (col):
            if arr[i][j][0] == 'b':
                movewhat(arr[i][j],i,j)
    return

def removex(arr):
    for i in range(8):
        for j in range(8):
           
            if (arr[i][j])[0]=='x' and len(arr[i][j])>1:
                arr[i][j] = arr[i][j][1]+arr[i][j][2]
                print(arr[i][j])
            if (arr[i][j]) == 'x':
                arr[i][j] = ' '

def movewhat(name,x,y):
    if name[0] == 'w' and name[1] == 'p':
        pmovew(x,y)
    if name[0] == 'b' and name[1] == 'p':
        pmoveb(x,y)
    if name[1] == 'k':
        kingm(x,y,name[0])
    if name[1] == 'r':
        rom(x,y,name[0])
    if name[1] == 'b':
        bim(x,y,name[0])
    if name[1] == 'K':
        Km(x,y,name[0])
    if name[1] == 'q':
        qm(x,y,name[0])
    






def move(old,new):
    arr[new[0]][new[1]] = arr[old[0]][old[1]]
    arr[old[0]][old[1]] = ' '
    
    if new[0] == 0 and arr[new[0]][new[1]] == 'wp':
        arr[new[0]][new[1]] = 'wq'
    
    if new[0] == 7 and arr[new[0]][new[1]] == 'bp':
        arr[new[0]][new[1]] = 'bq'

def clear(arr):
    for i in range(8):
        for j in range(8):
            if (arr[i][j])[0] == 'x':
                arr[i][j] == ' '


for i in range(8):
    print(arr[i])
    print('\n')


def scale_bitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result

SIZE = 400
class Mywin(wx.Frame): 
          
    def __init__(self, parent, title,click = False, turn = 1): 
        super(Mywin, self).__init__(parent, title = title,size = (SIZE+15,SIZE+40))  
        self.InitUI() 
        self.click = click
        self.turn = turn
        
         
    def InitUI(self): 
        self.Bind(wx.EVT_PAINT, self.OnPaint) 
        self.Centre() 
        self.Show(True)
        self.Bind(wx.EVT_LEFT_UP, self.onClick)
       
        

    def onClick(self, event):
        pt = event.GetPosition()
        x, y = pt/(SIZE/8)
        if (self.turn %2 == 1 and arr[y][x][0] == "b") or (self.turn %2 == 0 and arr[y][x][0] == "w"):
            print(self.turn)
            print(arr[y][x][0])
            return
        if arr[y][x] == " ":
            print("There is no piece to click on")
            return
        if (self.click == False):
            self.click = True
            self.old = y, x 
            movewhat(arr[y][x],y,x)
            for i in range(8):
                    print(arr[i])
                    print('\n')
            self.Refresh()
        else:
            if (self.click == True):
               
                if self.old!=(y,x) and arr[y][x][0] == 'x':
                    move(self.old,(y,x))
                    self.turn +=1
                    removex(arr)
                if arr[y][x][0]!='x':
                    removex(arr)

                self.Refresh()
                self.click = False

                

        
    def OnPaint(self, e): 
        dc = wx.PaintDC(self) 
        pen = wx.Pen(wx.Colour(0,0,0)) 
        dc.SetPen(pen) 
        for i in range(8): 
            for j in range(8):
                if (i+j) % 2 == 0:
                    dc.SetBrush(wx.Brush("grey", wx.SOLID))
                else:
                    dc.SetBrush(wx.Brush("white", wx.SOLID))
                if arr[i][j][0] == 'x':
                    dc.SetBrush(wx.Brush("green", wx.SOLID))
                        
                dc.DrawRectangle(j*SIZE/8,i*SIZE/8,SIZE/8,SIZE/8)
                if arr[i][j].replace('x','') == 'wp':
                    dc.DrawBitmap(wp,j*SIZE/8,i*SIZE/8,True)
                if arr[i][j].replace('x','') == 'wr':
                    dc.DrawBitmap(wr,j*SIZE/8,i*SIZE/8,True)
                if arr[i][j].replace('x','') == 'wK':
                   dc.DrawBitmap(wK,j*SIZE/8,i*SIZE/8,True)
                if arr[i][j].replace('x','') == 'wb':
                    
                    dc.DrawBitmap(wb,j*SIZE/8,i*SIZE/8,True)
                if arr[i][j].replace('x','') == 'wq':
                    dc.DrawBitmap(wq,j*SIZE/8,i*SIZE/8,True)
                if arr[i][j].replace('x','') == 'wk':
                    dc.DrawBitmap(wk,j*SIZE/8,i*SIZE/8,True)
                if arr[i][j].replace('x','') == 'bp':
                    dc.DrawBitmap(bp,j*SIZE/8,i*SIZE/8,True)
                if arr[i][j].replace('x','') == 'br':
                    dc.DrawBitmap(br,j*SIZE/8,i*SIZE/8,True)
                if arr[i][j].replace('x','') == 'bK':
                    dc.DrawBitmap(bK,j*SIZE/8,i*SIZE/8,True)
                if arr[i][j].replace('x','') == 'bb':
                    dc.DrawBitmap(bb,j*SIZE/8,i*SIZE/8,True)
                if arr[i][j].replace('x','') == 'bq':
                    dc.DrawBitmap(bq,j*SIZE/8,i*SIZE/8,True)
                if arr[i][j].replace('x','') == 'bk':
                    dc.DrawBitmap(bk,j*SIZE/8,i*SIZE/8,True)
                
     




ex = wx.App() 
Mywin(None,'Drawing demo') 
wp = wx.Bitmap("wp.png")
wp = scale_bitmap(wp, 50, 50) 

wr = wx.Bitmap("wr.png")
wr = scale_bitmap(wr, 50, 50)

wK = wx.Bitmap("wkn.png")
wK = scale_bitmap(wK, 50, 50)

wb = wx.Bitmap("wb.png")
wb = scale_bitmap(wb, 50, 50)

wq = wx.Bitmap("wq.png")
wq = scale_bitmap(wq, 50, 50)

wk = wx.Bitmap("wk.png")
wk = scale_bitmap(wk, 50, 50) 

br = wx.Bitmap("br.png")
br = scale_bitmap(br, 50, 50)

bK = wx.Bitmap("bkn.png")
bK = scale_bitmap(bK, 50, 50)

bb = wx.Bitmap("bb.png")
bb = scale_bitmap(bb, 50, 50)

bq = wx.Bitmap("bq.png")
bq = scale_bitmap(bq, 50, 50)

bk = wx.Bitmap("bk.png")
bk = scale_bitmap(bk, 50, 50) 

bp = wx.Bitmap("bp.png")
bp = scale_bitmap(bp, 50, 50)

ex.MainLoop()  

