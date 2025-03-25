<template>
  <div class="profile">
    <h2>个人资料</h2>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <p><strong>用户名：</strong> {{ user.username }}</p>
      <p><strong>邮箱：</strong> {{ user.email }}</p>
      <button @click="logout">退出登录</button>
    </div>
  </div>
</template>

<script>
import axios from '../utils/axios'

export default {
  name: 'Profile',
  data() {
    return {
      user: {},
      loading: true
    }
  },
  created() {
    this.fetchProfile()
  },
  methods: {
    async fetchProfile() {
      const token = localStorage.getItem('token');
      if (!token) {
        // 如果没有 Token，跳转到登录页
        this.$router.push('/login');
        return;
      }

      try {
        const response = await axios.get('/profile', {
          headers: { Authorization: `Bearer ${token}` }
        })

        // 假设后端返回的数据是 { username: 'user123', email: 'user123@example.com' }
        this.user = response.data
      } catch (error) {
        console.error('获取个人资料失败:', error)
        // 如果是认证失败（401），跳转到登录页
        if (error.response && error.response.status === 401) {
          this.$router.push('/login');
        }
      } finally {
        this.loading = false
      }
    },
    logout() {
      localStorage.removeItem('token')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
/* 个人资料样式 */
.profile {
  max-width: 600px;
  margin: auto;
}
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
