import cv2
import os
from openai import OpenAI
import numpy as np
import time
import requests
import oss2

def upload_image_to_oss(image_path):
    # 阿里云 OSS 配置
    access_key_id = 'LTAI5t5a5MXJtzXPGpDXT5H4'  # 替换为您的 Access Key ID
    access_key_secret = 'VhB1EOwenoXS6dZm33eeRPaAwUuD5z'  # 替换为您的 Access Key Secret
    endpoint = 'oss-cn-shenzhen.aliyuncs.com'  # 替换为您的 Endpoint
    bucket_name = 'ai-companship'  # 替换为您的 Bucket 名称

    # 初始化 OSS 客户端
    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    # 上传文件
    object_name = 'uploaded_image.jpeg'  # OSS 中的文件名
    with open(image_path, 'rb') as fileobj:
        bucket.put_object(object_name, fileobj)

    # 生成签名的 URL
    image_url = bucket.sign_url('GET', object_name, 3600)  # 有效期为 3600 秒
    return image_url

def get_response_from_camera():
    # 初始化摄像头
    cap = cv2.VideoCapture(0)  # 参数0表示使用默认摄像头

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    # 获取摄像头帧率
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = 1.0 / fps  # 帧间隔时间

    while True:
        start_time = time.time()

        # 从摄像头读取一帧图像
        ret, frame = cap.read()
        if not ret:
            print("无法从摄像头获取图像")
            break

        # 显示摄像头图像
        cv2.imshow('Camera', frame)

        # 将图像保存到临时文件
        temp_image_path = "temp_camera_image.jpeg"
        cv2.imwrite(temp_image_path, frame)

        # 将图像上传到 OSS 并获取有效的 URL
        image_url = upload_image_to_oss(temp_image_path)

        # 使用通义千问-Omni-Turbo-Realtime 模型进行图像分析
        try:
            client = OpenAI(
                api_key=os.getenv("DASHSCOPE_API_KEY"),  # 从环境变量读取
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )
            completion = client.chat.completions.create(
                model="qwen-omni-turbo-realtime",  # 使用通义千问-Omni-Turbo-Realtime 的 model code
                messages=[
                    {
                        "role": "system",
                        "content": [{"type": "text", "text": "You are a helpful assistant."}]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url
                                }
                            },
                            {
                                "type": "text",
                                "text": "分析人的情绪"
                            }
                        ]
                    }
                ],
                stream=True
            )

            full_response = ""
            for chunk in completion:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    print(chunk.choices[0].delta.content, end='', flush=True)
            print("\n完整回复：")
            print(full_response)

        except Exception as e:
            print(f"\n请求过程中发生错误：{e}")

        # 计算剩余等待时间以保持帧率
        elapsed_time = time.time() - start_time
        remaining_time = frame_interval - elapsed_time
        if remaining_time > 0:
            time.sleep(remaining_time)

        # 按下'q'键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放摄像头资源并关闭窗口
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    get_response_from_camera()