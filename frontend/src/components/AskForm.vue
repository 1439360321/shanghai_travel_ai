<template>
  <div class="chat-container">
    <!-- 初始居中提问框 -->
    <div v-if="!questionAsked" class="center-ask-form">
      <h1>上海旅行助手</h1>
      <p>帮助您规划行程</p>
      <input
        v-model="question"
        placeholder="请输入你的问题..."
        @focus="moveToBottom"
      />
      <button @click="moveToBottom">开始提问</button>
      
      <!-- 猜你喜欢部分 -->
      <div class="suggested-questions">
        <p>猜你喜欢：</p>
        <div class="question-buttons">
          <button @click="useSuggestedQuestion('给我规划一个3天2夜旅行')">给我规划一个3天2夜旅行</button>
          <button @click="useSuggestedQuestion('上海夜景有推荐吗')">上海夜景有推荐吗</button>
          <button @click="useSuggestedQuestion('上海有哪些美食')">上海有哪些美食</button>
        </div>
      </div>
    </div>

    <!-- 聊天记录（仅在首页显示）-->
    <div v-if="isHomePage" class="chat-messages" ref="chatBox">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['chat-bubble', msg.type]"
      >
        <!-- 对于 recommendation 类型消息使用 v-html 展示 HTML 内容 -->
        <template v-if="msg.type === 'recommendation'">
          <div v-html="msg.text"></div>
        </template>
        <template v-else>
          {{ msg.text }}
        </template>
      </div>
    </div>

    <!-- 固定底部提问框 -->
    <div v-if="questionAsked" class="ask-form">
      <input
        v-model="question"
        placeholder="请输入你的问题..."
        @keyup.enter="submitQuestion"
        @focus="scrollToBottom"
      />
      <button @click="submitQuestion" :disabled="loading">发送</button>
    </div>
  </div>
</template>

<script>
import axios from '../utils/axios';

export default {
  data() {
    return {
      question: '',
      messages: [], // 存储聊天记录
      loading: false,
      questionAsked: false, // 控制是否已经点击开始提问
    };
  },
  computed: {
    isHomePage() {
      return this.$route.path === '/'; // 当前是否在首页
    }
  },
  methods: {
    // 使用推荐问题
    useSuggestedQuestion(question) {
      this.question = question;
      this.moveToBottom();
      // 自动聚焦到输入框，方便用户直接发送
      this.$nextTick(() => {
        document.querySelector('.ask-form input')?.focus();
      });
    },
    moveToBottom() {
      // 隐藏居中提问框，展示底部提问框
      this.questionAsked = true;
      this.scrollToBottom();
    },
    async submitQuestion() {
      if (!this.question.trim()) return;

      const userQuestion = this.question;
      // 显示用户提问气泡
      this.messages.push({ text: userQuestion, type: 'user' });
      this.question = ''; // 清空输入框

      this.loading = true;

      try {
        // 向后端发送问题并获取回答与推荐链接
        const response = await axios.post('/ask', { question: userQuestion });
        const { answer, recommendations } = response.data;
        // 显示机器人的回答气泡
        this.messages.push({ text: answer, type: 'bot' });
        // 如果有相关推荐，则构造 HTML 列表进行展示
        if (recommendations && recommendations.length > 0) {
          const recHtml = `<p>相关推荐：</p><ul>${recommendations
            .map(link => `<li>${link}</li>`)
            .join('')}</ul>`;
          this.messages.push({ text: recHtml, type: 'recommendation' });
        }
      } catch (error) {
        console.error(error);
        this.messages.push({ text: '抱歉，出现错误，请稍后再试。', type: 'bot' });
      } finally {
        this.loading = false;
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const chatBox = this.$refs.chatBox;
        if (chatBox) {
          chatBox.scrollTop = chatBox.scrollHeight;
        }
      });
    }
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 80px); /* 减去顶部导航高度 */
  width: 100%;
  max-width: none;
  margin: 0;
  padding: 0;
  background: rgba(244, 244, 244, 0.4);
  position: fixed;
  top: 80px;
  left: 0;
  overflow-y: auto;
}

/* 中央初始提问框 */
.center-ask-form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 80vh;
  text-align: center;
  background: transparent;
}

.center-ask-form h1 {
  font-size: 2rem;
  margin-bottom: 10px;
}

.center-ask-form p {
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.center-ask-form input {
  padding: 10px;
  border-radius: 25px;
  border: 1px solid #ddd;
  width: 80%;
  font-size: 16px;
  margin-bottom: 10px;
}

.center-ask-form button {
  padding: 10px 15px;
  font-size: 16px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
}

/* 聊天记录区域 */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 80px;
  width: 100%;
  background: transparent;
  max-width: 600px;
  margin: auto;
}

/* 聊天气泡样式 */
.chat-bubble {
  padding: 10px 15px;
  border-radius: 15px;
  word-break: break-word;
  margin-bottom: 10px;
  max-width: 500px;
  display: inline-block;
}

.chat-bubble.user {
  align-self: flex-end;
  background: #4CAF50;
  color: white;
  border-radius: 15px 15px 0 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.chat-bubble.bot {
  align-self: flex-start;
  background: #ddd;
  color: black;
  border-radius: 15px 15px 15px 0;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.chat-bubble.recommendation {
  align-self: flex-start;
  background: #fffbea;
  color: #555;
  border: 1px solid #ffe58f;
  border-radius: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 15px;
}

/* 固定底部提问框 */
.ask-form {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  max-width: 600px;
  width: 90%;
  background: white;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 10px;
}

.ask-form input {
  flex: 1;
  padding: 10px;
  border-radius: 25px;
  border: 1px solid #ddd;
  font-size: 16px;
  outline: none;
}

.ask-form button {
  padding: 10px 15px;
  font-size: 16px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
}

.ask-form button:disabled {
  background: gray;
  cursor: not-allowed;
}

/* 猜你喜欢部分 */
.suggested-questions {
  margin-top: 30px;
  width: 100%;
  text-align: center;
}

.suggested-questions p {
  font-size: 1rem;
  color: #666;
  margin-bottom: 10px;
}

.question-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 80%;
  margin: 0 auto;
}

.question-buttons button {
  padding: 10px 15px;
  background: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 25px;
  cursor: pointer;
  font-size: 14px;
  color: #333;
  transition: all 0.3s;
}

.question-buttons button:hover {
  background: #e0e0e0;
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .chat-container {
    padding-bottom: 60px;
  }
  .ask-form {
    width: 100%;
    bottom: 15px;
  }
  .chat-bubble {
    max-width: 90%;
  }
  .question-buttons {
    width: 100%;
  }
  .question-buttons button {
    font-size: 13px;
    padding: 8px 12px;
  }
}
</style>