#coding=utf-8
import sys
import os
import appbuilder
from   os.path import abspath, dirname
sys.path.insert(0,abspath(dirname(__file__)))
import tkinter
from   tkinter import *
import Fun
uiName="文字对话"
ElementBGArray={}
ElementBGArray_Resize={}
ElementBGArray_IM={}


# 设置环境中的TOKEN，以下TOKEN请替换为您的个人TOKEN，个人TOKEN可通过该页面【获取鉴权参数】或控制台页【密钥管理】处获取

os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-flztb2R538LAXAgy85qiY/c366d8d8bc0982810d257021b162f7e5c6218ca0"



# 从AppBuilder控制台【个人空间】-【应用】网页获取已发布应用的ID

app_id = "f2272872-30f2-41c2-bdc5-a0d20d571dde"



app_builder_client = appbuilder.AppBuilderClient(app_id)

conversation_id = app_builder_client.create_conversation()
resp = app_builder_client.run(conversation_id, input())
print(resp.content.answer)
#Form 'Form_1's Event :Load
def Form_1_onLoad(uiName):
    
   pass

#Button 'Button_1' 's Command Event :
def Button_1_onCommand(uiName,widgetName,threadings=0):
    Fun.Gettext(uiName,"Entry_1"")
    input(resp)
    pass
