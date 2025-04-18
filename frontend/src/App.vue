<template>
  <div id="app">
    <!-- 背景视频 -->
    <div class="background-video-container">
      <video autoplay muted loop class="background-video">
        <!-- 这里的路径根据你的视频文件实际存放位置来设置 -->
        <source src="./assets/background-video.mp4" type="video/mp4">
        <source src="./assets/background-video.webm" type="video/webm">
        您的浏览器不支持视频标签。
      </video>
    </div>

    <!-- 导航栏 -->
    <nav class="main-nav">
      <div class="logo-container">
        <img src="../src/assets/logo.jpg" alt="上海Logo" class="logo-img">
      </div>
      <div class="nav-links">
        <router-link to="/">首 页</router-link>
        <span v-if="!isLoggedIn"> | </span>
        <router-link to="/recommendations">推 荐</router-link>
      </div>
    </nav>

    <!-- 主内容区 -->
    <div class="main-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Microsoft YaHei', sans-serif;
}

body {
  /* background-color: #f4f4f4; */
}

/* 背景视频容器 */
.background-video-container {
  position: fixed;
  top: 0;
  left: 0;
  margin-top: 80px; 
  width: 100%;
  height: 100%;
  z-index: -1; /* 确保视频在背景 */
}

.background-video {
  object-fit: cover; /* 使视频填充整个容器 */
  width: 100%;
  height: 100%;
}

.content {
  position: relative;
  z-index: 1; /* 确保内容在视频前面 */
  text-align: center;
  padding: 50px;
  color: white;
}

/* 导航条样式 */
.main-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 5%;
  background: url('../src/assets/main-nav-background.png') center/cover no-repeat;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.logo-container img {
  height: 50px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-links a {
  color: black;
  text-decoration: none;
  font-size: 2.5rem;
  transition: color 0.3s ease;
}

.nav-links a:hover {
  color: #ffd700;
}

/* 主内容样式 */
.main-content {
  margin-top: 100px; /* 为固定导航留出空间 */
  padding: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-links {
    width: 100%;
    justify-content: center;
  }
}
</style>
