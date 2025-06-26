#coding=utf-8
#import libs
import b2_cmd
import b2_sty
import Fun
import tkinter
from   tkinter import *
import tkinter.ttk
import tkinter.font
#Add your Varial Here: (Keep This Line of comments)
#Define UI Class
class b2:
    def __init__(self,root,isTKroot = True,params=None):
        uiName = Fun.GetUIName(root,self.__class__.__name__)
        self.uiName = uiName
        Fun.Register(uiName,'UIClass',self)
        self.root = root
        self.isTKroot = isTKroot
        self.firstRun = True
        self.rootZoomed = False
        Fun.G_UIParamsDictionary[uiName]=params
        Fun.G_UICommandDictionary[uiName]=b2_cmd
        Fun.Register(uiName,'root',root)
        style = b2_sty.SetupStyle(isTKroot)
        self.UIJsonString = '{"Version": "1.0.0", "UIName": "b2", "Description": "", "WindowSize": [960, 640], "WindowPosition": "Center", "WindowHide": false, "WindowResizable": true, "WindowTitle": "Form1", "DarkMode": false, "BorderWidth": 0, "BorderColor": "#ffffff", "DropTitle": false, "DragWindow": true, "MinSize": [0, 0], "TransparentColor": null, "RootTransparency": 255, "ICOFile": null, "WinState": 1, "WinTopMost": true, "BGColor": "#f8f9fa", "GroupList": {}, "WidgetList": [{"Type": "Form", "Index": 1, "AliasName": "Form_1", "BGColor": "#f8f9fa", "Size": [960, 640], "EventList": {"Load": "Form_1_onLoad"}}]}'
        Form_1 = Fun.CreateUIFormJson(uiName,root,isTKroot,style,self.UIJsonString)
        Fun.InitElementData(uiName)
        #Call Form_1's OnLoad Function
        Fun.RunForm1_CallBack(uiName,"Load",b2_cmd.Form_1_onLoad)
        #Add Some Logic Code Here: (Keep This Line of comments)
        #Exit Application: (Keep This Line of comments)
        if self.isTKroot == True and Fun.GetElement(self.uiName,"root"):
            self.root.protocol('WM_DELETE_WINDOW', self.Exit)
            self.root.bind('<Configure>', self.Configure)
            if self.rootZoomed == True and isinstance(self.root,tkinter.Tk) == True:
                self.root.state("zoomed")
                Fun.SetUIState(uiName,"zoomed")
                self.rootZoomed = False
            self.root.bind('<Escape>',self.Escape)

    #GetRootSize
    def GetRootSize(self):
        return Fun.GetUIRootSize(self.uiName)

    #GetAllElement
    def GetAllElement(self):
        return Fun.G_UIElementDictionary[self.uiName]

    def Exit(self):
        if self.isTKroot == True:
            Fun.DestroyUI(self.uiName,0,'')

    def Escape(self,event):
        if Fun.AskBox('提示','确定退出程序？') == True:
            Fun.DestroyUI(self.uiName,0,'')

    def Configure(self,event):
        Form_1 = Fun.GetElement(self.uiName,'Form_1')
        if Form_1 == event.widget:
            Fun.ReDrawCanvasRecord(self.uiName)
        if self.root == event.widget:
            Fun.ResizeRoot(self.uiName,self.root,event)
            Fun.ResizeAllChart(self.uiName)
            uiName = self.uiName
        Fun.ActiveElement(self.uiName,event.widget)

#Create the root of tkinter 
if  __name__ == '__main__':
    Fun.RunApplication(b2)
