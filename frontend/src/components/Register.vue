<template>
  <div class="register">
    <h2>注册</h2>
    <form @submit.prevent="submitRegister">
      <div class="form-group">
        <label for="username">用户名：</label>
        <input type="text" v-model="username" id="username" required />
      </div>
      <div class="form-group">
        <label for="email">邮箱：</label>
        <input type="email" v-model="email" id="email" required :class="{'input-error': emailError}" />
        <p v-if="emailError" class="error">请输入有效的邮箱地址</p>
      </div>
      <div class="form-group">
        <label for="password">密码：</label>
        <input type="password" v-model="password" id="password" required :class="{'input-error': passwordError}" />
        <p v-if="passwordError" class="error">密码长度必须至少 6 位，并包含数字和特殊字符</p>
      </div>
      <div class="form-group">
        <label for="confirmPassword">确认密码：</label>
        <input type="password" v-model="confirmPassword" id="confirmPassword" required />
      </div>
      <button type="submit" :disabled="loading">注册</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">注册成功！请登录。</p>
    <p>已有账号？<router-link to="/login">登录</router-link></p>
  </div>
</template>

<script>
import axios from '../utils/axios'

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      loading: false,
      error: '',
      success: false,  // 用于显示注册成功信息
      emailError: false,
      passwordError: false,
    }
  },
  methods: {
    // 注册前检查邮箱和密码的有效性
    validateInputs() {
      this.emailError = !/\S+@\S+\.\S+/.test(this.email); // 简单的邮箱验证
      this.passwordError = !(this.password.length >= 6 && /\d/.test(this.password) && /[!@#$%^&*(),.?":{}|<>]/.test(this.password));
      return !this.emailError && !this.passwordError;
    },

    async submitRegister() {
      if (this.password !== this.confirmPassword) {
        this.error = '两次输入的密码不一致';
        return;
      }

      if (!this.validateInputs()) {
        return; // 输入验证未通过
      }

      this.loading = true;
      this.error = '';
      this.success = false;
      try {
        const response = await axios.post('/register', {
          username: this.username,
          email: this.email,
          password: this.password
        });
        this.success = true;  // 注册成功后显示成功信息
        setTimeout(() => {
          this.$router.push('/login'); // 注册成功后跳转到登录页
        }, 2000);
      } catch (error) {
        this.error = error.response?.data?.detail || '注册失败，请稍后重试';
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.register {
  max-width: 450px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-size: 14px;
  color: #555;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ccc;
  box-sizing: border-box;
  transition: border-color 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #4CAF50;
}

input.input-error {
  border-color: red;
}

button {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:hover {
  background-color: #45a049;
}

.error {
  color: red;
  font-size: 12px;
  margin-top: 5px;
}

.success {
  color: green;
  font-size: 14px;
  margin-top: 10px;
}

p {
  text-align: center;
  font-size: 14px;
}

router-link {
  color: #4CAF50;
  text-decoration: none;
}

router-link:hover {
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 600px) {
  .register {
    width: 90%;
    padding: 15px;
  }

  h2 {
    font-size: 20px;
  }

  button {
    padding: 10px;
  }
}
</style>
