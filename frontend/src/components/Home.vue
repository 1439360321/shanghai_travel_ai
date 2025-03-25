
<template>
  <div class="Home">
    <h1>上海旅行助手</h1>

    <!-- 提问表单 -->
    <AskForm @submitQuestion="addQuestion" />

    <!-- 语音输入 -->
    <VoiceInput @voiceInput="addVoiceQuestion" />

    <!-- 历史记录展示 -->
    <HistoryList :questions="questions" />

    <!-- 清除历史记录 -->
    <ClearHistory @clearHistory="clearHistory" />
  </div>
</template>

<script>
import AskForm from './AskForm.vue'
import HistoryList from './HistoryList.vue'
import ClearHistory from './ClearHistory.vue'
import VoiceInput from './VoiceInput.vue'
import axios from 'axios'

export default {
  name: 'Home',
  components: {
    AskForm,
    HistoryList,
    ClearHistory,
    VoiceInput
  },
  data() {
    return {
      questions: [],
      loading: false  // 添加加载状态
    };
  },
  methods: {
    // 添加提问
    async addQuestion(question) {
      this.loading = true;  // 开始加载
      try {
        // 调用后端 API 获取答案
        const response = await axios.post('http://localhost:8000/ask', {
          question: question
        });
        this.questions.push({
          question: question,
          answer: response.data.answer
        });
      } catch (error) {
        console.error("提交问题时出错", error);
      } finally {
        this.loading = false;  // 加载完成
      }
    },

    // 处理语音识别问题
    async addVoiceQuestion(question) {
      if (!question) return;  // 检查是否有有效的语音识别结果
      this.loading = true;  // 开始加载
      try {
        // 调用后端 API 获取答案
        const response = await axios.post('http://localhost:8000/ask', {
          question: question
        });
        this.questions.push({
          question: question,
          answer: response.data.answer
        });
      } catch (error) {
        console.error("语音输入时出错", error);
      } finally {
        this.loading = false;  // 加载完成
      }
    },

    // 清空历史记录
    clearHistory() {
      if (confirm("您确定要清除所有历史记录吗？")) {
        this.questions = [];
      }
    }
  }
}
</script>

<style>
body {
  font-family: Arial, sans-serif;
  padding: 20px;
}

h1 {
  text-align: center;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.ask-form {
  margin-top: 20px;
}

.loading {
  font-size: 18px;
  color: #ff9800;
}
</style>
