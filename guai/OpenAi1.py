import os
from openai import OpenAI
import cv2 # 新增导入
import oss2 # 新增导入
import time # 新增导入，用于生成唯一文件名
import numpy as np

# 阿里云 OSS 配置 (请替换为您的实际配置)
OSS_ACCESS_KEY_ID = 'LTAI5t5a5MXJtzXPGpDXT5H4'
OSS_ACCESS_KEY_SECRET = 'VhB1EOwenoXS6dZm33eeRPaAwUuD5z'
OSS_ENDPOINT = 'oss-cn-shenzhen.aliyuncs.com'
OSS_BUCKET_NAME = 'ai-companship'

def upload_image_to_oss(image_data):
    auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET_NAME)

    object_name = 'uploaded_image_' + str(int(time.time())) + '.jpeg' # 使用时间戳作为文件名，避免重复
    try:
        bucket.put_object(object_name, image_data)
        image_url = bucket.sign_url('GET', object_name, 3600)
        return image_url
    except Exception as e:
        print(f"OSS 上传失败: {e}")
        return None

def get_response(image_path=None):
    if not image_path:
        print("请上传图片路径")
        return

    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    try:
        # 读取并处理图片
        with open(image_path, 'rb') as f:
            img_bytes = f.read()
        
        img_array = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        if frame is None:
            print("无法读取图片，请重新上传")
            return

        # 上传到OSS并获取分析结果
        ret, buffer = cv2.imencode('.jpeg', frame)
        if not ret:
            print("图片处理失败，请重新上传")
            return
            
        image_url = upload_image_to_oss(buffer.tobytes())
        if not image_url:
            print("图片上传失败，请重新上传")
            return

        # 获取AI分析结果
        completion = client.chat.completions.create(
            model="qwen-vl-max",
            messages=[
                {"role": "system", "content": [{"type": "text", "text": "You are a helpful assistant."}]},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": image_url}},
                    {"type": "text", "text": "请帮我进行舌诊辅助，如果你没看清图中的舌头，请回复我'请重新上传图片'"}
                ]}
            ],
            stream=True
        )

        # 处理AI响应
        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end='', flush=True)
        
        if "请重新上传图片" in full_response:
            print("\nAI未识别到舌头，请重新上传清晰的舌头图片")
        else:
            print("\n\n完整回复：")
            print(full_response)
            
    except Exception as e:
        print(f"处理过程中发生错误: {e}")
        print("请重新上传图片")

if __name__ == '__main__':
    # 必须传入图片路径
    get_response(image_path="C:/Users/ASUS/Desktop/下载.webp")
    # 如果不传入参数，则会使用默认的在线图片URL
    get_response()