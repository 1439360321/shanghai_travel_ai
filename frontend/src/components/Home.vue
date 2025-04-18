<template>
  <div class="Home">
    <!-- 提问表单 -->
    <AskForm @submitQuestion="handleSubmitQuestion" />

    <!-- 加载状态提示 -->
    <div v-if="loading" class="loading">
      正在加载...
    </div>
  </div>
</template>

<script>
import AskForm from './AskForm.vue'
import axios from 'axios'

export default {
  name: 'Home',
  components: {
    AskForm,
  },
  data() {
    return {
      loading: false,
      questions: []  // 用于存储提问和回答
    }
  },
  methods: {
    // 处理文本提问
    async handleSubmitQuestion(question) {
      this.loading = true;
      try {
        const response = await axios.post('http://localhost:8000/ask', {question});
        const answer = response.data.answer;
        this.questions.push({question, answer});
      } catch (error) {
        console.error('提交提问时出错:', error);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.Home {
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

.loading {
  font-size: 18px;
  color: #ff9800;
  text-align: center;
  margin-top: 20px;
}

.ask-form {
  margin-top: 20px;
}
</style>
