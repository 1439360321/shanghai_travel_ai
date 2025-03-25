import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://localhost:8010',  // 后端 API 地址
  timeout: 10000
})

export default instance
