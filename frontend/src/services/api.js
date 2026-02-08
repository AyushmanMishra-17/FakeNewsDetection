import axios from "axios";

const api = axios.create({
  baseURL: "https://fake-news-api-uwv8.onrender.com",
});

export default api;
