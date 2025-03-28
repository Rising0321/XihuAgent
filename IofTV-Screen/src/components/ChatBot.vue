<template>
  <div class="chat-container">
    <!-- 机器人图标按钮 -->
    <div class="chat-icon" @click="toggleChat" v-if="!isOpen">
      <span class="robot-icon">🤖</span>
    </div>

    <!-- 聊天窗口 -->
    <div class="chat-window" v-if="isOpen">
      <div class="chat-header">
        <span>AI助手</span>
        <span class="close-btn" @click="toggleChat">✕</span>
      </div>
      
      <div class="chat-messages" ref="messageContainer">
        <div v-for="(message, index) in messages" :key="index" 
             :class="['message', message.type === 'user' ? 'user-message' : 'bot-message']">
          {{ message.content }}
        </div>
      </div>

      <div class="chat-input">
        <div class="input-container">
          <input
            v-model="inputMessage"
            placeholder="请输入消息..."
            @keyup.enter="sendMessage"
            class="message-input"
          />
          <button @click="sendMessage" class="send-button">发送</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatBot',
  data() {
    return {
      isOpen: false,
      inputMessage: '',
      messages: []
    }
  },
  methods: {
    toggleChat() {
      this.isOpen = !this.isOpen
      if (this.isOpen && this.messages.length === 0) {
        // 添加欢迎消息
        this.messages.push({
          content: "你好！我是AI助手，很高兴为您服务。请问有什么我可以帮您的吗？",
          type: 'bot'
        })
      }
    },
    async sendMessage() {
      if (!this.inputMessage.trim()) return

      // 添加用户消息
      this.messages.push({
        content: this.inputMessage,
        type: 'user'
      })

      const userMessage = this.inputMessage
      this.inputMessage = ''

      try {
        // 发送请求到后端
        const response = await fetch('http://localhost:32101', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message: userMessage })
        })

        const data = await response.text()
        
        // 添加机器人回复
        this.messages.push({
          content: data,
          type: 'bot'
        })
      } catch (error) {
        console.error('Error:', error)
        this.messages.push({
          content: '抱歉，服务器出现错误',
          type: 'bot'
        })
      }

      // 滚动到底部
      this.$nextTick(() => {
        const container = this.$refs.messageContainer
        container.scrollTop = container.scrollHeight
      })
    }
  }
}
</script>

<style scoped>
.chat-container {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 1000;
}

.chat-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #0a2444 0%, #1e4976 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 12px 0 rgba(0, 162, 255, 0.2);
  transition: transform 0.3s ease;
  border: 1px solid rgba(0, 162, 255, 0.3);
}

.chat-icon:hover {
  transform: scale(1.1);
  box-shadow: 0 2px 15px 0 rgba(0, 162, 255, 0.3);
}

.robot-icon {
  font-size: 24px;
}

.chat-window {
  position: fixed;
  right: 20px;
  bottom: 20px;
  width: 350px;
  height: 500px;
  background: rgba(13, 19, 35, 0.8);
  border-radius: 10px;
  box-shadow: 0 2px 20px 0 rgba(0, 162, 255, 0.2);
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(0, 162, 255, 0.3);
  backdrop-filter: blur(10px);
}

.chat-header {
  padding: 15px 20px;
  background: linear-gradient(135deg, #0a2444 0%, #1e4976 100%);
  color: #fff;
  border-radius: 10px 10px 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  border-bottom: 1px solid rgba(0, 162, 255, 0.3);
}

.close-btn {
  cursor: pointer;
  font-size: 18px;
  transition: transform 0.3s ease;
  color: rgba(255, 255, 255, 0.8);
}

.close-btn:hover {
  transform: scale(1.1);
  color: #fff;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background: rgba(16, 22, 36, 0.6);
}

.message {
  margin: 10px 0;
  padding: 12px 16px;
  border-radius: 10px;
  max-width: 80%;
  word-break: break-word;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.user-message {
  background: linear-gradient(135deg, #0a2444 0%, #1e4976 100%);
  color: #fff;
  margin-left: auto;
  border: 1px solid rgba(0, 162, 255, 0.3);
}

.bot-message {
  background: rgba(30, 73, 118, 0.3);
  color: #fff;
  border: 1px solid rgba(0, 162, 255, 0.2);
}

.chat-input {
  padding: 15px;
  background: rgba(13, 19, 35, 0.9);
  border-top: 1px solid rgba(0, 162, 255, 0.3);
  border-radius: 0 0 10px 10px;
}

.input-container {
  display: flex;
  gap: 10px;
}

.message-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid rgba(0, 162, 255, 0.3);
  border-radius: 4px;
  outline: none;
  font-size: 14px;
  background: rgba(16, 22, 36, 0.6);
  color: #fff;
}

.message-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.message-input:focus {
  border-color: rgba(0, 162, 255, 0.6);
  box-shadow: 0 0 5px rgba(0, 162, 255, 0.2);
}

.send-button {
  padding: 8px 15px;
  background: linear-gradient(135deg, #0a2444 0%, #1e4976 100%);
  color: #fff;
  border: 1px solid rgba(0, 162, 255, 0.3);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.send-button:hover {
  background: linear-gradient(135deg, #0c2c52 0%, #245a8f 100%);
  box-shadow: 0 0 10px rgba(0, 162, 255, 0.2);
}

.send-button:active {
  background: linear-gradient(135deg, #081d36 0%, #1a4369 100%);
}

/* 自定义滚动条样式 */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: rgba(16, 22, 36, 0.6);
}

.chat-messages::-webkit-scrollbar-thumb {
  background: rgba(0, 162, 255, 0.3);
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 162, 255, 0.5);
}
</style> 