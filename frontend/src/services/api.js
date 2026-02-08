import axios from "axios";

const api = axios.create({
  baseURL: "https://fake-news-api-l558.onrender.com",
});

export default api;
