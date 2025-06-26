#coding=utf-8
import sys
import os
from   os.path import abspath, dirname
sys.path.insert(0,abspath(dirname(__file__)))
import tkinter
from   tkinter import *
import Fun
uiName="Project7"
ElementBGArray={}  
ElementBGArray_Resize={} 
ElementBGArray_IM={} 

#Form 'Form_1's Load Event :
def Form_1_onLoad(uiName,threadings=0):
    pass
#Button 'Button_2' 's Command Event :
def Button_2_onCommand(uiName,widgetName,threadings=0):
    Fun.SetCursor(uiName,widgetName,'hand2')
    #Create the Popup Menu
    widget = Fun.GetElement(uiName,widgetName)
    PopupMenu=tkinter.Menu(widget,tearoff=False)
    PopupMenu.add_command(label="情绪检测",command=lambda:Button_2_onCommand_Menu_情绪检测(uiName,"情绪检测"))
    PopupMenu.add_command(label="舌诊辅助",command=lambda:Button_2_onCommand_Menu_舌诊辅助(uiName,"舌诊辅助"))
    x, y = widget.winfo_pointerxy()
    PopupMenu.post(x,y)
#EventMenu '舌诊辅助' 's Command Event :
def Button_2_onCommand_Menu_舌诊辅助(uiName,itemName):
    pass
#EventMenu '情绪检测' 's Command Event :
def Button_2_onCommand_Menu_情绪检测(uiName,itemName):
    pass
#Button 'Button_1' 's Command Event :
def Button_1_onCommand(uiName,widgetName,threadings=0): 
    PopupMenu=tkinter.Menu(widget,tearoff=False)
    PopupMenu.add_command(label="文字对话",command=lambda:Button_1_onCommand_Menu_文字对话(uiName,"文字对话"))
    PopupMenu.add_command(label="语音对话",command=lambda:Button_1_onCommand_Menu_语音对话(uiName,"语音对话"))
    PopupMenu.add_command(label="数字人对话",command=lambda:Button_1_onCommand_Menu_数字人对话(uiName,"数字人对话"))
    x, y = widget.winfo_pointerxy()
    PopupMenu.post(x,y)
#Button 'Button_3' 's Command Event :
def Button_3_onCommand(uiName,widgetName,threadings=0):
    Fun.SetCursor(uiName,widgetName,'hand2')
#Button 'Button_4' 's Command Event :
def Button_4_onCommand(uiName,widgetName,threadings=0):
    Fun.SetCursor(uiName,widgetName,'hand2')
#Button 'Button_5' 's Command Event :
def Button_5_onCommand(uiName,widgetName,threadings=0):
    Fun.SetCursor(uiName,widgetName,'rightbutton')
#EventMenu '文字对话' 's Command Event :
def Button_1_onCommand_Menu_文字对话(uiName,itemName):
   
    pass

#EventMenu '语音对话' 's Command Event :
def Button_1_onCommand_Menu_语音对话(uiName,itemName):
    pass

#EventMenu '数字人对话' 's Command Event :
def Button_1_onCommand_Menu_数字人对话(uiName,itemName):
    pass

