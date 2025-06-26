#coding=utf-8
#import libs 
import sys
import os
from   os.path import abspath, dirname
sys.path.insert(0,abspath(dirname(__file__)))
import Project7_cmd
import Project7_sty
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
class  Project7:
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
        Fun.G_UICommandDictionary[uiName]=Project7_cmd
        Fun.Register(uiName,'root',root)
        style = Project7_sty.SetupStyle(isTKroot)
        self.UIJsonString = '{"Version": "1.0.0", "UIName": "Project7", "Description": "", "WindowSize": [1481, 953], "WindowPosition": "Center", "WindowHide": false, "WindowResizable": true, "WindowTitle": "乖乖女--老人智能陪伴系统", "DarkMode": false, "BorderWidth": 0, "BorderColor": "#ffffff", "DropTitle": false, "DragWindow": false, "MinSize": [0, 0], "ResolutionScaling": true, "PopupDebugDialog": false, "TransparentColor": null, "RootTransparency": 255, "ICOFile": "C:/Users/linjiqing/Downloads/PyMe1.5.1.2-win64/PyMe1.5.1.2/Ico/free/ICO_Home.png", "ICOMode": "File", "WinState": 1, "WinTopMost": false, "BGColor": "#EFEFEF", "GroupList": {}, "WidgetList": [{"Type": "Form", "Index": 1, "AliasName": "Form_1", "BGColor": "#EFEFEF", "Size": [1481, 953], "PlaceInfo": null, "BGImage": "Resources/创建网页背景图.png", "BGImageWrap": "Zoom", "EventList": {"Load": "Form_1_onLoad"}}, {"Type": "Frame", "Index": 7, "AliasName": "Frame_1", "ParentName": "Form_1", "Layer": "lower", "PlaceInfo": [-7, 159, 285, 832, "nw", true, false], "Visible": true, "Size": [285, 832], "BGColor": "#EFEFEF", "Relief": "flat", "ScrollRegion": null}, {"Type": "Button", "Index": 4, "AliasName": "Button_3", "ParentName": "Frame_7", "PlaceInfo": [52, 360, 170, 89, "nw", true, false], "Visible": true, "Size": [170, 89], "BGColor": "#333333", "ActiveBGColor": "#EEEEEE", "Text": "健康档案", "FGColor": "#000000", "ActiveFGColor": "#000000", "Font": ["Microsoft YaHei UI", 14, "bold", "roman", 0, 0], "BGImage": "Resources/未标题-1.png", "Compound": "center", "RoundCorner": 20, "Relief": "raised", "EventList": {"Command": "Button_3_onCommand"}}, {"Type": "Button", "Index": 3, "AliasName": "Button_2", "ParentName": "Frame_7", "PlaceInfo": [51, 214, 171, 92, "nw", true, false], "Visible": true, "Size": [171, 92], "BGColor": "#333333", "ActiveBGColor": "#EEEEEE", "Text": "智能体检", "FGColor": "#000000", "ActiveFGColor": "#000000", "Font": ["Microsoft YaHei UI", 14, "bold", "roman", 0, 0], "BGImage": "Resources/未标题-1.png", "Compound": "center", "RoundCorner": 20, "Relief": "raised", "EventList": {"Command": "Button_2_onCommand"}}, {"Type": "Button", "Index": 2, "AliasName": "Button_1", "ParentName": "Frame_7", "PlaceInfo": [52, 70, 169, 90, "nw", true, false], "Visible": true, "Size": [169, 90], "BGColor": "#333333", "ActiveBGColor": "#EEEEEE", "Text": "智能陪伴", "FGColor": "#000000", "ActiveFGColor": "#000000", "Font": ["Microsoft YaHei UI", 14, "bold", "roman", 0, 0], "BGImage": "Resources/未标题-1.png", "Compound": "center", "RoundCorner": 20, "Relief": "raised", "EventList": {"Command": "Button_1_onCommand"}}]}'
        Form_1 = Fun.CreateUIFormJson(uiName,root,isTKroot,style,self.UIJsonString)
        #Inital all element's Data 
        Fun.InitElementData(uiName)
        #Call Form_1's OnLoad Function
        Fun.RunForm1_CallBack(uiName,"Load",Project7_cmd.Form_1_onLoad)
        #Add Some Logic Code Here: (Keep This Line of comments)



        #Exit Application: (Keep This Line of comments)
        if self.isTKroot == True and Fun.GetElement(self.uiName,"root"):
            self.root.protocol('WM_DELETE_WINDOW', self.Exit)
            self.root.bind('<Configure>', self.Configure)
            if self.rootZoomed == True and isinstance(self.root,tkinter.Tk) == True:
                self.root.state("zoomed")
                Fun.SetUIState(uiName,"zoomed")
                self.rootZoomed = False
            
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
            Fun.SetCanvasBGImage(self.uiName,'Form_1',"Resources/创建网页背景图.png",'Zoom')
            Fun.ReDrawCanvasRecord(self.uiName)
        if self.root == event.widget and (self.configure_event is None or self.configure_event[2]!= event.width or self.configure_event[3]!= event.height):
            uiName = self.uiName
            self.configure_event = [event.x,event.y,event.width,event.height]
            Fun.ResizeRoot(self.uiName,self.root,event)
            Fun.ResizeAllChart(self.uiName)
            pass
#Create the root of tkinter 
if  __name__ == '__main__':
    Fun.RunApplication(Project7)
