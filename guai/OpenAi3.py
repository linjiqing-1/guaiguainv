import cv2
import os
from openai import OpenAI
import numpy as np
import time
import requests
import oss2
import threading
import queue

# 定义一个队列用于线程间通信
frame_queue = queue.Queue(maxsize=1) # 队列大小为1，只保留最新帧

# 全局标志，用于控制线程的运行和退出
running = True

def upload_image_to_oss(image_data): # 接受图像数据而不是路径
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
    try:
        bucket.put_object(object_name, image_data) # 直接上传字节数据
        # 生成签名的 URL
        image_url = bucket.sign_url('GET', object_name, 3600)  # 有效期为 3600 秒
        return image_url
    except Exception as e:
        print(f"OSS 上传失败: {e}")
        return None

def camera_capture_thread(cap):
    global running
    while running:
        start_time = time.time()

        ret, frame = cap.read()
        if not ret:
            print("无法从摄像头获取图像")
            running = False
            break

        # 将帧放入队列，如果队列已满则丢弃旧帧
        if not frame_queue.full():
            try:
                frame_queue.get_nowait() # 尝试清空旧帧
            except queue.Empty:
                pass
            frame_queue.put(frame)

        # 控制拍照频率为 0.01 秒
        elapsed_time = time.time() - start_time
        sleep_time = 0.01 - elapsed_time
        if sleep_time > 0:
            time.sleep(sleep_time)

def image_processing_thread():
    global running
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),  # 从环境变量读取
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    last_output_time = time.time()
    while running:
        try:
            frame = frame_queue.get(timeout=0.1) # 从队列中获取帧，设置较短超时
            # 将图像帧编码为 JPEG 格式的字节流
            ret, buffer = cv2.imencode('.jpeg', frame)
            if not ret:
                print("图像编码失败")
                continue
            image_data = buffer.tobytes()

            # 将图像上传到 OSS 并获取有效的 URL
            image_url = upload_image_to_oss(image_data)

            if image_url:
                # 使用通义千问-QVQ-Max 模型进行图像分析
                try:
                    completion = client.chat.completions.create(
                        model="qvq-max",  # 使用通义千问-QVQ-Max 的 model code
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
                                        "text": "分析人的情绪，并给一些对身体健康有好处的建议，请使用第一人称与我对话,请记住你的职责是为我提供关怀与温暖"
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
                            # print(chunk.choices[0].delta.content, end='', flush=True) # 移除实时打印

                    current_time = time.time()
                    if current_time - last_output_time >= 10:
                        print("\n完整回复：")
                        print(full_response)
                        last_output_time = current_time

                except Exception as e:
                    print(f"\n请求过程中发生错误：{e}")
            else:
                print("未获取到有效的图片URL，跳过AI分析。")
        except queue.Empty:
            # 队列为空，继续等待新帧
            continue
        except Exception as e:
            print(f"图像处理线程发生错误: {e}")

def get_response_from_camera():
    global running
    running = True

    cap = cv2.VideoCapture(0)  # 参数0表示使用默认摄像头

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    # 启动摄像头捕获线程
    capture_thread = threading.Thread(target=camera_capture_thread, args=(cap,))
    capture_thread.start()

    # 启动图像处理线程
    processing_thread = threading.Thread(target=image_processing_thread)
    processing_thread.start()

    # 主线程负责显示和按键监听
    while running:
        try:
            # 尝试从队列中获取最新帧进行显示
            frame = frame_queue.get(timeout=0.001) # 设置一个很短的超时，避免阻塞
            cv2.imshow('Camera', frame)
        except queue.Empty:
            pass # 队列为空，继续循环等待

        # 监听按键，'e'键退出
        if cv2.waitKey(1) & 0xFF == ord('e'):
            running = False

    # 等待线程结束
    capture_thread.join()
    processing_thread.join()

    # 释放摄像头资源并关闭窗口
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    get_response_from_camera()