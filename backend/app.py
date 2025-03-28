from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 启用CORS支持

@app.route('/', methods=['GET', 'POST'])
def chat():
    print(request.method)
    if request.method == 'POST':
        try:
            data = request.get_json()
            print(data)
            if not data:
                return "对不起，我没有收到消息内容", 400
                
            message = data.get('message', '')
            if not message:
                return "对不起，消息内容不能为空", 400

            # 这里是一个简单的回复逻辑，后续可以替换为真正的LLM服务
            if "你好" in message or "hello" in message.lower():
                return "你好！很高兴见到你！"
            elif "天气" in message:
                return "抱歉，我目前还不能查询天气信息。"
            elif "名字" in message:
                return "我是AI助手，很高兴为您服务！"
            else:
                return f"我收到了你的消息：{message}。请问还有什么我可以帮你的吗？"
                
        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return "对不起，服务器处理消息时出现错误", 500
            
    return "你好！我是AI助手，很高兴为您服务。"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=32101, debug=True) 