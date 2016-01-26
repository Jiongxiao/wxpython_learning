# -*- coding: utf-8 -*-

import wx
import os
import random
import copy

class Frame(wx.Frame):
    """docstring for Frame"""
    def __init__(self,title):
        super(Frame,self).__init__(None,-1,title,
                style=wx.DEFAULT_FRAME_STYLE^wx.MAXIMIZE_BOX^wx.RESIZE_BORDER)

        self.colors = {0:(204,192,179),2:(238, 228, 218),4:(237, 224, 200),
                8:(242, 177, 121),16:(245, 149, 99),32:(246, 124, 95),
                64:(246, 94, 59),128:(237, 207, 114),256:(237, 207, 114),
                512:(237, 207, 114),1024:(237, 207, 114),2048:(237, 207, 114),
                4096:(237, 207, 114),8192:(237, 207, 114),16384:(237, 207, 114),
                32768:(237, 207, 114),65536:(237, 207, 114),131072:(237, 207, 114),
                262144:(237, 207, 114),524288:(237, 207, 114),1048576:(237, 207, 114),
                2097152:(237, 207, 114),4194304:(237, 207, 114),
                8388608:(237, 207, 114),16777216:(237, 207, 114),
                33554432:(237, 207, 114),67108864:(237, 207, 114),
                134217728:(237, 207, 114),268435456:(237, 207, 114),
                536870912:(237, 207, 114),1073741824:(237, 207, 114),
                2147483648:(237, 207, 114),4294967296:(237, 207, 114),
                8589934592:(237, 207, 114),17179869184:(237, 207, 114),
                34359738368:(237, 207, 114),68719476736:(237, 207, 114),
                137438953472:(237, 207, 114),274877906944:(237, 207, 114),
                549755813888:(237, 207, 114),1099511627776:(237, 207, 114),
                2199023255552:(237, 207, 114),4398046511104:(237, 207, 114),
                8796093022208:(237, 207, 114),17592186044416:(237, 207, 114),
                35184372088832:(237, 207, 114),70368744177664:(237, 207, 114),
                140737488355328:(237, 207, 114),281474976710656:(237, 207, 114),
                562949953421312:(237, 207, 114),1125899906842624:(237, 207, 114),
                2251799813685248:(237, 207, 114),4503599627370496:(237, 207, 114),
                9007199254740992:(237, 207, 114),18014398509481984:(237, 207, 114),
                36028797018963968:(237, 207, 114),72057594037927936:(237, 207, 114)}

            self.setIcon()
            self.initGame()
            self.initBuffer()
            panel= wx.Panel(self)
            panel.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
            panel.SetFocus()

            self.Bind(wx.EVT_SIZE, self.onSize)
            self.Bind(wx.EVT_PAINT, self.onPaint)
            self.Bind(wx.EVT_CLOSE,self.onClose)
            self.Center()
            self.Show()

            def onPaint(self,event):
                dc= wx.BufferedPaintDC(self,self.buffer)

            def onSize(self,event):
                self.initBuffer()
                self.drawAll()

            def onClose(self,event):
                self.saveScore()
                self.Destroy()

            def loadScore(self):
                if os.path.exists('bestscore.ini'):
                    ff=open('bestscore.ini')
                    self.bstScore=ini(ff.read())
                    ff.close()
            def saveScore(self):
                ff=open('bestscore.ini','w')
                ff.write(str(self.bstScore))
                ff.close()

            def setIcon(self):
                icon = wx.Icon("icon.ico",wx.BITMAP_TYPE_ICO)
                self.SetIcon(icon)

            def initGame(self):
                ################################what?
                self.bgFont = wx.Font(50,wx.SWISS,wx.NORMAL,wx.BOLD,face=u"Roboto")
                self.scFont = wx.Font(36,wx.SWISS,wx.NORMAL,wx.BOLD,face=u"Roboto")
                self.smFont = wx.Font(12,wx.SWISS,wx.NORMAL,wx.NORMAL,face=u"Roboto")
                self.curScore=0
                self.bstScore=0
                self.loadScore()
                self.data=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
                count=0
                while count<2:
                    row=random.randint(0,len(self.data)-1)
                    col=random.randint(0,len(self.data[0])-1)
                    if self.data[row][col]!=0:
                        continue
                    self.data[row][col]=2 if random.randint(0,1) else 4
                    count+=1

            def initBuffer(self):
                w,h=self.GetClientSize()# ???
                self.buffer=wx.EmptyBitmap(w,h)

            def drawAll(self):
                dc= wx.BufferedDC(wx.ClientDC(self),self.buffer)
                self.drawBg(dc)
                self.drawLogo(dc)
                self.drawLabel(dc)
                self.drawScore(dc)
                self.drawTiles(dc)

            def drawChange(self,score):
                dc=wx.BufferedDC(wx.ClientDC(self),self.buffer)
                if score:
                    self.curScore+=score
                    if self.curScore> self.bstScore:
                        self.bstScore=self.curScore
                    self.drawScore(dc)
                self.drawTiles(dc)

            def onKeyDown(self,event):
                keyCode=event.GetKeyCode()

                if keyCode==wx.WXK_UP:
                    self.doMove(*self.slideUpDown(True))
                elif keyCode==wx.WXK_DOWN:
                    self.doMove(*self.slideUpDown(False))
                elif keyCode==wx.WXK_LEFT:
                    self.doMove(*self.slideLeftRight(True))
                elif keyCode==wx.WXK_RIGHT:
                    self.doMove(*self.slideLeftRight(False))

            def slideLeftRight(self, up):
                score=0
                numCols=len(self.data[0])
                numRows=len(self.data)
                oldData=copy.deepcopy(self.data)

                for row in range(numRows):
                    rvl= [self.data[row][col] for col in range(numCols) if self.data[row][col]!=0]
                    if len(rvl)>=2:
                        score=score+self.update(rvl,left)
                    for i in range(numCols-len(rvl)):
                        if left:
                            rvl.append(0)
                        else:
                            rvl.insert(0,0)
                    for col in range(numCols):
                        data[row][col]=rvl[col]
                return oldData!=self.data, score


            def slideUpDown(self, up):
                score=0
                numCols=len(self.data[0])
                numRows=len(self.data)
                oldData=copy.deepcopy(self.data)

                for col in range(numCols):
                    cvl=[self.data[row][col] for row in range(numRows) if self.data[row][col]!=0]
                    if len(cvl)>=2:
                        score=score+self.update(cvl,up)
                    for i in range(numRows-len(cvl)):
                        if up: cvl.append(0)
                        else: cvl.insert(0,0)
                    for row in range(numRows):
                        self.data[row][col]=cvl[row]
                return oldData!=self.data, score

            def update(self, vlist, direct): #up or left
                score=0
                if direct:
                    i=1
                    while i<len(vlist):
                        if vlist[i-1]==vlist[i]:
                            del vlist[i]
                            vlist[i-1]=2*vlist[i-1]
                            score=vlist[i-1]
                            i+=1
                        i+=1
                else:
                    i=len(vlist)-1
                    while i>0:
                        if vlist[i-1]==vlist[i]:
                            del vlist[i]
                            vlist[i-1]*=2
                            score+=vlist[i-1]
                            i-=1
                        i-=1
                return score



            def doMove(self, move, score):
                if move:
