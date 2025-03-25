<template>
  <div>
    <button @click="clearHistory">清除历史记录</button>
  </div>
</template>

<script>
export default {
  name: 'ClearHistory',
  methods: {
    clearHistory() {
      this.$emit('clearHistory');
    }
  }
}
</script>

<style scoped>
button {
  padding: 10px 20px;
  background-color: #f44336;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #d32f2f;
}
</style>
