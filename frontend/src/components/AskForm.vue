<template>
  <div class="ask-form">
    <input v-model="question" placeholder="请输入你的问题..." />
    <button @click="submitQuestion">提问</button>
    <div v-if="loading">正在加载...</div>
    <div v-if="answer">
      <h2>回答：</h2>
      <p>{{ answer }}</p>
    </div>
  </div>
</template>

<script>
import axios from '../utils/axios.js'

export default {
  name: 'AskForm',
  data() {
    return {
      question: '',
      answer: '',
      sources: [],
      loading: false
    }
  },
  methods: {
    async submitQuestion() {
      if (!this.question.trim()) return
      this.loading = true
      this.answer = ''
      this.sources = []
      try {
        const response = await axios.post('/ask', { question: this.question })
        this.answer = response.data.answer
        this.sources = response.data.sources
      } catch (error) {
        console.error(error)
        this.answer = error.message
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.ask-form {
  max-width: 600px;
  margin: auto;
}
input {
  width: 80%;
  padding: 10px;
  font-size: 16px;
  margin-right: 10px;
}
button {
  padding: 10px 20px;
  font-size: 16px;
}
</style>
