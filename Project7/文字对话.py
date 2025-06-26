#coding=utf-8
#import libs 
import sys
import os
from   os.path import abspath, dirname
sys.path.insert(0,abspath(dirname(__file__)))
import 文字对话_cmd
import 文字对话_sty
import Fun
import EXUIControl
EXUIControl.FunLib = Fun
EXUIControl.G_ExeDir = Fun.G_ExeDir
EXUIControl.G_ResDir = Fun.G_ResDir
import tkinter
from   tkinter import *
import tkinter.ttk
import tkinter.font
from   PIL import Image,ImageTk

#Add your Varial Here: (Keep This Line of comments)
#Define UI Class
class  文字对话:
    def __init__(self,root,isTKroot = True,params=None):
        uiName = Fun.GetUIName(root,self.__class__.__name__)
        self.uiName = uiName
        Fun.Register(uiName,'UIClass',self)
        self.root = root
        self.configure_event = None
        self.isTKroot = isTKroot
        self.firstRun = True
        self.rootZoomed = False
        Fun.G_UIParamsDictionary[uiName]=params
        Fun.G_UICommandDictionary[uiName]=文字对话_cmd
        Fun.Register(uiName,'root',root)
        style = 文字对话_sty.SetupStyle(isTKroot)
        self.UIJsonString = '{"Version": "1.0.0", "UIName": "文字对话", "Description": "", "WindowSize": [960, 640], "WindowPosition": "Center", "WindowHide": false, "WindowResizable": true, "WindowTitle": "文字对话", "DarkMode": false, "BorderWidth": 0, "BorderColor": "#ffffff", "DropTitle": false, "DragWindow": true, "MinSize": [0, 0], "ResolutionScaling": true, "PopupDebugDialog": false, "TransparentColor": null, "RootTransparency": 255, "ICOFile": null, "WinState": 1, "WinTopMost": true, "BGColor": "#f8f9fa", "GroupList": {}, "WidgetList": [{"Type": "Form", "Index": 1, "AliasName": "Form_1", "BGColor": "#f8f9fa", "Size": [960, 640], "PlaceInfo": null, "BGImage": "Resources/未标题-1.png", "BGImageWrap": "Zoom", "EventList": {"Load": "Form_1_onLoad"}}, {"Type": "Text", "Index": 3, "AliasName": "Text_1", "ParentName": "Form_1", "PlaceInfo": [49, 43, 846, 466, "nw", true, false], "Visible": true, "Size": [846, 466], "BGColor": "#FFFFFF", "AutoWrap": true, "FGColor": "#b8860b", "Font": ["Microsoft YaHei UI", 14, "normal", "roman", 0, 0], "Relief": "flat"}, {"Type": "Button", "Index": 4, "AliasName": "Button_1", "ParentName": "Form_1", "PlaceInfo": [753, 544, 142, 74, "nw", true, false], "Visible": true, "Size": [142, 74], "BGColor": "#4FC1E9", "ActiveBGColor": "#AC92EC", "Text": "提交", "FGColor": "#EC87C0", "ActiveFGColor": "#b8860b", "Font": ["Microsoft YaHei UI", 14, "bold", "roman", 0, 0], "Relief": "flat", "EventList": {"Command": "Button_1_onCommand"}}, {"Type": "Entry", "Index": 5, "AliasName": "Entry_1", "ParentName": "Form_1", "PlaceInfo": [51, 544, 666, 74, "nw", true, false], "Visible": true, "Size": [666, 74], "BGColor": "#FFFFFF", "BGColor_ReadOnly": "#f8f9fa", "FGColor": "#000000", "Font": ["Microsoft YaHei UI", 14, "normal", "roman", 0, 0], "InnerBorderColor": "#000000", "TipFGColor": "#888888", "Relief": "sunken"}]}'
        Form_1 = Fun.CreateUIFormJson(uiName,root,isTKroot,style,self.UIJsonString)
        #Inital all element's Data 
        Fun.InitElementData(uiName)
        #Call Form_1's OnLoad Function
        Fun.RunForm1_CallBack(uiName,"Load",文字对话_cmd.Form_1_onLoad)
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
    def GetRootSize(self):
        return Fun.GetUIRootSize(self.uiName)
    def GetAllElement(self):
        return Fun.G_UIElementDictionary[self.uiName]
    def Escape(self,event):
        if Fun.AskBox('提示','确定退出程序？') == True:
            self.Exit()
    def Exit(self):
        if self.isTKroot == True:
            Fun.DestroyUI(self.uiName,0,'')

    def Configure(self,event):
        Form_1 = Fun.GetElement(self.uiName,'Form_1')
        if Form_1 == event.widget:
            Fun.SetCanvasBGImage(self.uiName,'Form_1',"Resources/未标题-1.png",'Zoom')
            Fun.ReDrawCanvasRecord(self.uiName)
        if self.root == event.widget and (self.configure_event is None or self.configure_event[2]!= event.width or self.configure_event[3]!= event.height):
            uiName = self.uiName
            self.configure_event = [event.x,event.y,event.width,event.height]
            Fun.ResizeRoot(self.uiName,self.root,event)
            Fun.ResizeAllChart(self.uiName)
            pass
#Create the root of tkinter 
if  __name__ == '__main__':
    Fun.RunApplication(文字对话)
