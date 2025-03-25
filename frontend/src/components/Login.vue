<template>
  <div class="login">
    <h2>登录</h2>
    <form @submit.prevent="submitLogin">
      <div class="form-group">
        <label for="username">用户名：</label>
        <input type="text" v-model="username" id="username" required />
      </div>
      <div class="form-group">
        <label for="password">密码：</label>
        <input type="password" v-model="password" id="password" required />
      </div>
      <button type="submit" :disabled="loading">{{ loading ? "登录中..." : "登录" }}</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <p>没有账号？<router-link to="/register">注册</router-link></p>
  </div>
</template>

<script>
import axios from '../utils/axios'

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      loading: false,
      error: ''
    }
  },
  methods: {
    async submitLogin() {
      this.loading = true
      this.error = ''
      try {
        const response = await axios.post('/login', {
          username: this.username,
          password: this.password
        })
        localStorage.setItem('token', response.data.access_token)
        this.$router.push('/profile')
      } catch (error) {
        this.error = error.response?.data?.detail || '登录失败，请检查用户名和密码'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
/* 🎨 登录框 */
.login {
  max-width: 400px;
  margin: 60px auto;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  text-align: center;
}

/* 🎯 标题 */
h2 {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

/* 📌 表单样式 */
.form-group {
  text-align: left;
  margin-bottom: 15px;
}

label {
  font-size: 14px;
  font-weight: bold;
  color: #555;
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

/* 🏆 聚焦时高亮输入框 */
input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0px 0px 8px rgba(76, 175, 80, 0.3);
}

/* 🚀 登录按钮 */
button {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  font-weight: bold;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

button:hover {
  background-color: #45a049;
  transform: scale(1.05);
}

/* ⏳ 按钮禁用状态 */
button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* 🚨 错误信息 */
.error {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}

/* 🔗 登录 & 注册链接 */
p {
  font-size: 14px;
  margin-top: 15px;
}

router-link {
  color: #4CAF50;
  text-decoration: none;
  font-weight: bold;
}

router-link:hover {
  text-decoration: underline;
}

/* 📱 响应式设计 */
@media (max-width: 600px) {
  .login {
    width: 90%;
    padding: 15px;
  }

  h2 {
    font-size: 22px;
  }

  button {
    padding: 10px;
  }
}
</style>
