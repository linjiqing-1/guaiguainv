try:
    import pyaudio
    print("pyaudio 库已安装。")
except ImportError:
    print("pyaudio 库未安装。请尝试运行: pip install pyaudio")

try:
    import webrtcvad
    print("webrtcvad 库已安装。")
except ImportError:
    print("webrtcvad 库未安装。请尝试运行: pip install webrtcvad")

try:
    import appbuilder
    print("appbuilder 库已安装。")
except ImportError:
    print("appbuilder 库未安装。请尝试运行: pip install appbuilder")