# -*- coding: utf-8 -*-
import wx
from math import *

class CalcFrame(wx.Frame):
    def __init__(self, title):
        super(CalcFrame,self).__init__(None,title=title,size=(300,200))
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        vbox= wx.BoxSizer(wx.VERTICAL)
        self.textprint= wx.TextCtrl(self,-1,'',style=wx.TE_RIGHT)
        self.equation=''
        vbox.Add(self.textprint, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=4)

        gridBox= wx.GridSizer(5,4,5,5)
        labels=['AC','DEL','pi','CLOSE','7','8','9','/','4','5','6',
        '*','1','2','3','-','0','.','=','+']
        for label in labels:
            buttonIterm=wx.Button(self,label=label)
            self.createHandler(buttonIterm,label)
            gridBox.Add(buttonIterm,1,wx.EXPAND)
        vbox.Add(gridBox,proportion=1,flag=wx.EXPAND)
        self.SetSizer(vbox)

    #创建按钮处理方法
    def createHandler(self,button,labels):
        item='DEL AC=CLOSE'
        if labels not in item:
            self.Bind(wx.EVT_BUTTON,self.OnAppend,button)
        elif labels=='DEL':
            self.Bind(wx.EVT_BUTTON,self.OnDel,button)
        elif labels=='AC':
            self.Bind(wx.EVT_BUTTON,self.OnAc,button)
        elif labels == '=':
            self.Bind(wx.EVT_BUTTON,self.OnTarget,button)
        elif labels=='CLOSE':
            self.Bind(wx.EVT_BUTTON,self.OnExit,button)

    #添加数字与运算符
    def OnAppend(self,event):
        eventbutton=event.GetEventObject()
        label= eventbutton.GetLabel()
        self.equation+=label
        self.textprint.SetValue(self.equation)

    def OnDel(self, event):
        self.equation=self.equation[:-1]
        self.textprint.SetValue(self.equation)

    def OnAc(self, event):
        self.equation=''
        self.textprint.SetValue(self.equation)

    def OnTarget(self,event):
        string=self.equation
        try:
            target=eval(string)
            self.equation=str(target)
            self.textprint.SetValue(self.equation)
        except:
            dlg=wx.MessageDialog(self,'xxx')
            dlg.ShowModel()
            dlg.Destroy()
    def OnExit(self,event):
        self.Close()


app=wx.App()
CalcFrame(title='Calculator')
app.MainLoop()
