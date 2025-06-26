# coding=utf-8
import sys
import os
import appbuilder
from os.path import abspath, dirname

sys.path.insert(0, abspath(dirname(__file__)))
import tkinter as tk
from tkinter import scrolledtext, messagebox

# 设置环境中的TOKEN
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-flztb2R538LAXAgy85qiY/c366d8d8bc0982810d257021b162f7e5c6218ca0"

# 从AppBuilder控制台获取已发布应用的ID
app_id = "f2272872-30f2-41c2-bdc5-a0d20d571dde"

# 初始化AppBuilder客户端
app_builder_client = appbuilder.AppBuilderClient(app_id)
conversation_id = None


class AppBuilderChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文字对话")
        self.root.geometry("600x500")

        # 创建UI元素
        self.create_widgets()

        # 初始化会话
        self.initialize_conversation()

    def create_widgets(self):
        # 聊天历史显示区域
        self.chat_history = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_history.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 输入框和按钮区域
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        self.user_input = tk.Entry(input_frame, width=45)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_input.bind("<Return>", self.on_enter_key)

        self.send_button = tk.Button(input_frame, text="发送", command=self.on_send_click)
        self.send_button.pack(side=tk.RIGHT)

    def initialize_conversation(self):
        global conversation_id
        try:
            conversation_id = app_builder_client.create_conversation()
            self.update_chat_history("系统", "会话已初始化，请输入您的问题")
        except Exception as e:
            messagebox.showerror("错误", f"初始化会话失败: {str(e)}")

    def on_send_click(self):
        user_message = self.user_input.get().strip()
        if user_message:
            self.send_message(user_message)
            self.user_input.delete(0, tk.END)

    def on_enter_key(self, event):
        self.on_send_click()
        return "break"  # 阻止默认的Enter键行为

    def send_message(self, user_message):
        # 显示用户消息
        self.update_chat_history("用户", user_message)

        # 显示"正在思考"
        self.update_chat_history("系统", "正在思考...")

        # 异步发送消息到AppBuilder
        self.root.after(100, self._send_message_to_appbuilder, user_message)

    def _send_message_to_appbuilder(self, user_message):
        global conversation_id
        try:
            # 移除"正在思考"消息
            self.remove_last_message()

            # 调用AppBuilder API
            resp = app_builder_client.run(conversation_id, user_message)

            # 显示AI回复
            self.update_chat_history("AI", resp.content.answer)
        except Exception as e:
            # 移除"正在思考"消息
            self.remove_last_message()

            # 显示错误消息
            self.update_chat_history("系统", f"发生错误: {str(e)}")

    def update_chat_history(self, sender, message):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)

    def remove_last_message(self):
        self.chat_history.config(state=tk.NORMAL)

        # 删除最后两行（消息和空行）
        content = self.chat_history.get(1.0, tk.END)
        lines = content.splitlines()
        if len(lines) >= 2:
            start_index = f"{len(lines) - 1}.0"
            self.chat_history.delete(start_index, tk.END)

        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = AppBuilderChatApp(root)
    root.mainloop()
import appbuilder
import os

# 设置环境中的TOKEN，以下TOKEN请替换为您的个人TOKEN，个人TOKEN可通过该页面【获取鉴权参数】或控制台页【密钥管理】处获取
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-flztb2R538LAXAgy85qiY/c366d8d8bc0982810d257021b162f7e5c6218ca0"

# 从AppBuilder控制台【个人空间】-【应用】网页获取已发布应用的ID
app_id = "f2272872-30f2-41c2-bdc5-a0d20d571dde"

app_builder_client = appbuilder.AppBuilderClient(app_id)
conversation_id = app_builder_client.create_conversation()

resp = app_builder_client.run(conversation_id, "汕头今天天气怎么样")
print(resp.content.answer)
