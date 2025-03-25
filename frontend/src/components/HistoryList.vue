<template>
  <div class="history-list">
    <h2>历史问题与答案</h2>
    <ul>
      <li v-for="(item, index) in questions" :key="index">
        <strong>问题：</strong> {{ item.question }} <br />
        <strong>答案：</strong> {{ item.answer }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'HistoryList',
  props: {
    questions: Array
  }
}
</script>

<style scoped>
.history-list {
  margin-top: 20px;
}
ul {
  list-style-type: none;
  padding-left: 0;
}
li {
  margin-bottom: 10px;
  border: 1px solid #ccc;
  padding: 10px;
}
</style>
