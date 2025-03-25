<template>
  <div id="app">
    <!-- 头部导航栏 -->
    <nav>
      <div class="logo">
        <a href="/">上海旅行助手</a>
      </div>
      <div class="nav-links">
        <a href="/">首页</a>
        <a href="/recommendations">旅行推荐</a>
        <a href="/profile">个人资料</a>
        <a href="/activities">活动</a>
        <a href="/messages">消息</a>
        <a v-if="!isLoggedIn" href="/login">登录</a>
        <a v-if="isLoggedIn" href="/logout" @click="logout">退出</a>
      </div>
      <div class="search">
        <input v-model="searchQuery" type="text" placeholder="搜索目的地..." />
        <button @click="search">搜索</button>
      </div>
    </nav>

    <!-- 主页内容显示区域 -->
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isLoggedIn: false,  // 用户是否登录
      searchQuery: ''  // 搜索关键词
    };
  },
  methods: {
    logout() {
      this.isLoggedIn = false;
      // 处理登出逻辑，例如清除令牌，重定向到首页等
    },
    search() {
      if (this.searchQuery) {
        // 处理搜索逻辑，可以跳转到搜索结果页面
        this.$router.push({ path: '/search', query: { q: this.searchQuery } });
      }
    }
  },
  created() {
    // 检查用户是否登录，例如通过 Vuex 或 cookie 判断
    // 假设你在 Vuex 中存储登录状态
    // this.isLoggedIn = this.$store.state.isLoggedIn;
  }
};
</script>

<style scoped>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Arial', sans-serif;
  background-color: #f4f4f4;
  color: #333;
}

/* 头部导航栏样式 */
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #4CAF50;
  padding: 15px 30px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

nav .logo a {
  color: white;
  font-size: 24px;
  font-weight: bold;
  text-decoration: none;
}

nav .nav-links {
  display: flex;
  align-items: center;
}

nav .nav-links a {
  color: white;
  margin: 0 15px;
  text-decoration: none;
  font-size: 18px;
  transition: color 0.3s ease;
}

nav .nav-links a:hover {
  color: #ddd;
}

nav .search input {
  padding: 8px 12px;
  font-size: 16px;
  border-radius: 5px;
  border: none;
  margin-right: 10px;
}

nav .search button {
  padding: 8px 16px;
  font-size: 16px;
  background-color: white;
  color: #4CAF50;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

nav .search button:hover {
  background-color: #45a049;
}

/* 响应式设计：在小屏幕设备上调整布局 */
@media (max-width: 768px) {
  nav {
    flex-direction: column;
    align-items: flex-start;
    padding: 10px;
  }

  nav .logo a {
    font-size: 20px;
  }

  nav .nav-links {
    flex-direction: column;
    width: 100%;
    margin-top: 10px;
  }

  nav .nav-links a {
    margin: 10px 0;
    font-size: 16px;
  }

  nav .search {
    margin-top: 10px;
    width: 100%;
  }

  nav .search input {
    width: calc(100% - 100px);
  }

  nav .search button {
    width: 80px;
  }
}

/* 页面内容样式 */
#app {
  margin-top: 20px;
  padding: 0 20px;
}

h2 {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

h3 {
  font-size: 20px;
  color: #555;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 10px;
}

button:hover {
  background-color: #45a049;
}

form {
  display: flex;
  flex-direction: column;
}

form div {
  margin-bottom: 15px;
}

form label {
  font-size: 16px;
  margin-bottom: 5px;
}

form input {
  padding: 8px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

form button {
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

form button:hover {
  background-color: #45a049;
}
</style>
