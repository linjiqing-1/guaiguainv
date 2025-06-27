# 设置鉴权参数
import os
import appbuilder

# 设置鉴权参数
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-flztb2R538LAXAgy85qiY/c366d8d8bc0982810d257021b162f7e5c6218ca0"

# 初始化 TTS
tts = appbuilder.TTS()

# 测试文本
text = "欢迎使用语音合成"
message = appbuilder.Message(content={"text": text})

# 调用 TTS
response = tts.run(message)

# 保存为 MP3 文件
with open("output.mp3", "wb") as f:
    f.write(response.content["audio_binary"])

print("语音合成成功，文件已保存为 output.mp3")

