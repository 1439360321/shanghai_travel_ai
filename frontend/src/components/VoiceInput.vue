<template>
  <div>
    <button @click="startVoiceRecognition">点击说话</button>
  </div>
</template>

<script>
export default {
  name: 'VoiceInput',
  methods: {
    startVoiceRecognition() {
      if (!('webkitSpeechRecognition' in window)) {
        alert('您的浏览器不支持语音识别功能');
        return;
      }

      const recognition = new webkitSpeechRecognition();
      recognition.lang = 'zh-CN';
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.onstart = () => {
        console.log('语音识别开始...');
      };

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        this.$emit('voiceInput', transcript);
      };

      recognition.onerror = (event) => {
        console.error('语音识别失败：', event.error);
        alert('语音识别失败，请再试一次');
      };

      recognition.onend = () => {
        console.log('语音识别结束');
      };

      recognition.start();
    }
  }
}
</script>

<style scoped>
button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #45a049;
}
</style>
