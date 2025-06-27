import websocket
import json
import base64
import hashlib
import hmac
from urllib.parse import urlencode
import datetime
from wsgiref.handlers import format_date_time
from time import mktime

# 替换为你在讯飞开放平台申请的APP ID、API Key和API Secret
APP_ID = "your_app_id"
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"

# 超拟人语音合成API的WebSocket地址
WEBSOCKET_URL = "wss://cbm01.cn-huabei-1.xfyun.com/v1/private/mcd9m97e6"

# 发声音人选择“聆玉言”
VCN = "x5_lingyuan_flow"

def assemble_ws_auth_url(request_url, method="GET"):
    """
    组装带有鉴权参数的WebSocket URL
    """
    # 解析URL
    u = parse_url(request_url)
    host = u.host
    path = u.path

    # 获取当前时间
    now = datetime.datetime.now()
    date = format_date_time(mktime(now.timetuple()))

    # 构造签名原始字符串
    signature_origin = f"host: {host}\ndate: {date}\n{method} {path} HTTP/1.1"

    # 生成签名
    signature = hmac.new(API_SECRET.encode('utf-8'), signature_origin.encode('utf-8'), digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(signature).decode('utf-8')

    # 构造Authorization
    authorization_origin = f'api_key="{API_KEY}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')

    # 组装查询参数
    query_params = {
        "host": host,
        "date": date,
        "authorization": authorization
    }

    return f"{request_url}?{urlencode(query_params)}"

def parse_url(request_url):
    """
    解析请求URL
    """
    if "://" not in request_url:
        raise ValueError("Invalid URL format")
    schema, rest = request_url.split("://", 1)
    if "/" not in rest:
        raise ValueError("Invalid URL format")
    host, path = rest.split("/", 1)
    path = f"/{path}"
    return type('Url', (object,), {"host": host, "path": path, "schema": schema})()

def text_to_speech(text):
    """
    发送文本到讯飞语音合成服务，并保存合成的语音
    """
    # 组装鉴权后的WebSocket URL
    ws_url = assemble_ws_auth_url(WEBSOCKET_URL)

    # 构造请求头
    header = {
        "app_id": APP_ID,
        "status": 2
    }

    # 构造语音合成参数
    parameter = {
        "oral": {
            "oral_level": "mid"
        },
        "tts": {
            "vcn": VCN,
            "speed": 50,
            "volume": 50,
            "pitch": 50,
            "bgs": 0,
            "reg": 0,
            "rdn": 0,
            "rhy": 0,
            "audio": {
                "encoding": "lame",
                "sample_rate": 24000,
                "channels": 1,
                "bit_depth": 16,
                "frame_size": 0
            }
        }
    }

    # 构造请求数据
    payload = {
        "text": {
            "encoding": "utf8",
            "compress": "raw",
            "format": "plain",
            "status": 2,
            "seq": 0,
            "text": base64.b64encode(text.encode('utf-8')).decode('utf-8')
        }
    }

    # 构造完整的请求消息
    message = {
        "header": header,
        "parameter": parameter,
        "payload": payload
    }

    # 连接到WebSocket服务器
    ws = websocket.create_connection(ws_url)

    # 发送请求消息
    ws.send(json.dumps(message))

    # 接收响应消息
    while True:
        response = ws.recv()
        try:
            response_data = json.loads(response)
        except json.JSONDecodeError:
            print("Received non-JSON data:", response)
            continue

        # 检查是否是音频数据
        if "payload" in response_data and "audio" in response_data["payload"]:
            audio_data = response_data["payload"]["audio"]["audio"]
            # 将Base64编码的音频数据解码
            decoded_audio = base64.b64decode(audio_data)

            # 保存音频文件
            with open("output.mp3", "wb") as audio_file:
                audio_file.write(decoded_audio)

            print("语音合成成功，音频已保存为output.mp3")
            break

    # 关闭WebSocket连接
    ws.close()

# 示例文本
text = "你好，欢迎使用讯飞超拟人语音合成服务。"

# 运行函数
text_to_speech(text)