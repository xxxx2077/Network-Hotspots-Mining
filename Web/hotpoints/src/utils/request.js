import axios from "axios";

// axios实例
const instance = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    timeout: 300000
})

// 响应拦截
instance.interceptors.response.use((res) => {
    // 返回响应结果
    return res;
}, err => {
    // 响应失败返回失败信息
    return Promise.reject(err);
})

export default instance