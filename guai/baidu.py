# 安装说明：
# 执行如下命令，快速安装Python语言的最新版本AppBuilder-SDK（要求Python >= 3.9)：
# pip install --upgrade appbuilder-sdk
import appbuilder
import os

# 设置环境中的TOKEN，以下TOKEN请替换为您的个人TOKEN，个人TOKEN可通过该页面【获取鉴权参数】或控制台页【密钥管理】处获取
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-7KwdqqmhmK1wW2AOTEQNu/2012c7d2f02e44984e2ead62e6030a4067481a69"

# 从AppBuilder控制台【个人空间】-【应用】网页获取已发布应用的ID
app_id = "eefb8cfc-bb6f-43df-b4bd-3b64ea3a8202"

app_builder_client = appbuilder.AppBuilderClient(app_id)
conversation_id = app_builder_client.create_conversation()

resp = app_builder_client.run(conversation_id, "我昨天遇到谁了啊")
print(resp.content.answer)