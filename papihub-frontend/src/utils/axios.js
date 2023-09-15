// config

// ----------------------------------------------------------------------

import axios from "axios";

const axiosInstance = axios.create({
  validateStatus: function (status) {
    return true; // 任何状态码都视为成功
  }
});

axiosInstance.interceptors.response.use(
    (response) => {
      const res = response.data;
      return {...res, response};
    },
    (error) => Promise.reject(
        (error.response && error.response.data) || 'Something went wrong')
);

export default axiosInstance;
