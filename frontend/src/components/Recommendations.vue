  <template>
    <div id="app">
      <!-- 推荐页面的内容 -->
      <div class="main-container">
        <!-- 侧边工具栏 -->
        <aside class="sidebar">
          <div class="toolbar">
            <button @click="toggleCategory('attractions')">景点排行</button>
            <button @click="toggleCategory('foods')">美食排行</button>
          </div>
          <div class="ranking-list">
            <ul>
              <li 
                v-for="(item, index) in currentList" 
                :key="item.id"
                :class="{ active: currentIndex === index }"
                @click="selectItem(index)"
              >
                {{ index + 1 }}. {{ item.name }}
              </li>
            </ul>
          </div>
        </aside>

        <!-- 内容展示区 -->
        <main class="content-display">
          <div class="preview-wrapper">
            <div class="description">
              <h2>{{ currentItem.name }}</h2>
              <p>{{ currentItem.description }}</p>
              <div class="image-container">
                <img :src="currentItemImage" :alt="currentItem.name" class="display-image">
              </div>
              <!-- 跳转到 askform 的按钮 -->
              <button class="ask-button" @click="goToAskForm">开始行程规划</button>
            </div>
          </div> 
        </main> 
      </div>
    </div>
  </template>

  <script>
  // 从 data.js 中导入景点和美食数据
  import { attractions, foods } from '../data/data.js';

  export default {
    data() {
      return {
        searchQuery: '', // 用于搜索
        attractions,  // 景点数据
        foods,  // 美食数据
        currentCategory: 'attractions',  // 默认选择景点
        currentIndex: 0,  // 默认选中第一个
      };
    },
    computed: {
      // 根据当前类别（景点或美食）返回相应的列表
      currentList() {
        return this.currentCategory === 'attractions' ? this.attractions : this.foods;
      },
      // 当前选中的项目（景点或美食）
      currentItem() {
        return this.currentList[this.currentIndex];
      },
      // 当前选中项目的图片路径
      currentItemImage() {
        const imagePath = `/assets/images/${this.currentList[this.currentIndex].imageName}.jpg`;  
        return imagePath;
      }
    },
    methods: {
      // 切换类别：景点或美食
      toggleCategory(type) {
        this.currentCategory = type;
        this.currentIndex = 0;
      },
      // 选择某个列表项
      selectItem(index) {
        this.currentIndex = index;
      },
      // 跳转到问答页面
      goToAskForm() {
        // 判断类别，生成问题
        const question = this.currentCategory === 'attractions'
          ? `我想去${this.currentItem.name}`  // 如果是景点，生成“我想去xxx”的问题
          : `我想吃${this.currentItem.name}`; // 如果是美食，生成“我想吃xxx”的问题

        // 跳转到首页并携带问题
        this.$router.push({
          path: '/',
          query: { question }  // 传递问题作为查询参数
        });
      }
    }
  }
  </script>

  <style scoped>
  /* 主页面样式 */
  .main-container {
    margin-top: 80px;
    display: flex;
    gap: 3rem;
    padding: 0 5%;
  }

  .sidebar {
    width: 20%;
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  .toolbar {
  display: flex;
  justify-content: space-between;  /* 两个按钮在一排 */
  margin-bottom: 2rem;
}

.toolbar button {
  flex: 1;  /* 让按钮的宽度平分 */
  padding: 1rem 0;
  margin: 0.5rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1.2rem;
  font-weight: bold;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* 按钮悬停效果 */
.toolbar button:hover {
  background-color: #45a049;
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
}

.toolbar button:active {
  background-color: #388e3c;
  transform: translateY(0);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

  .ranking-list ul {
    list-style: none;
  }

  .ranking-list li {
    padding: 1rem;
    margin: 0.5rem 0;
    background: #f8f8f8;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .ranking-list li:hover {
    background: #e3f4e7;
    transform: translateX(5px);
  }

  /* 内容展示 */
  .content-display {
    flex: 1;
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  .preview-wrapper {
    position: relative;
    height: 500px;
    overflow: hidden;
  }

  .preview-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
    cursor: pointer;
  }

  .preview-image:hover {
    transform: scale(1.02);
  }

  .description {
    margin-top: 1.5rem;
    line-height: 1.8;
    color: #555;
  }

  .ask-button {
    margin-top: 1rem;
    padding: 0.8rem 1.5rem;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.3s ease;
  }

  .ask-button:hover {
    background-color: #45a049;
  }

  /* 响应式设计 */
  @media (max-width: 768px) {
    .main-container {
      flex-direction: column;
      margin-top: 60px;
    }

    .sidebar {
      width: 100%;
      margin-bottom: 2rem;
    }
  }
  </style>
