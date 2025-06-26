#coding=utf-8
#import libs 
import sys
import Fun
import EXUIControl
import os
import tkinter
from   tkinter import *
import tkinter.ttk
import tkinter.font
from   PIL import Image,ImageTk

ElementBGArray={}  
ElementBGArray_Resize={} 
ElementBGArray_IM={} 

#Add your Varial Here: (Keep This Line of comments)
#Setup UI Style
def SetupStyle(isTKroot=False):
    style = tkinter.ttk.Style()
    return style
#Define UI Class
class  1:
    def __init__(self,root,isTKroot = True,params=None):
        uiName = Fun.GetUIName(root,self.__class__.__name__)
        self.uiName = uiName
        style = SetupStyle(isTKroot)
        Fun.Register(uiName,'UIClass',self)
        self.root = root
        self.isTKroot = isTKroot
        self.firstRun = True
        Fun.Register(uiName,'root',root)
        root['background'] = '#f8f9fa'
        #Create the elements of root 
        #Inital all element's Data 
        Fun.InitElementData(uiName)
        #Call Form_1's OnLoad Function
        Fun.RunForm1_CallBack(uiName,"Load",self.Form_1_onLoad)
        #Add Some Logic Code Here: (Keep This Line of comments)

    #GetRootSize
    def GetRootSize(self):
        return Fun.GetUIRootSize(self.uiName)
    #GetAllElement
    def GetAllElement(self):
        return Fun.G_UIElementDictionary[self.uiName]

#Create the root of tkinter 
if  __name__ == '__main__':
    Fun.RunApplication(1)
