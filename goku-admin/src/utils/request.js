import axios from 'axios';

Promise.prototype.finally = function (callback) { // eslint-disable-line
  const P = this.constructor;
  return this.then(
    value => P.resolve(callback()).then(() => value),
    reason => P.resolve(callback()).then(() => { throw reason; }),
  );
};

const instance = axios.create({
  baseURL: '/api/',
});

instance.interceptors.request.use((config) => {
  if (config.headers.Authorization === undefined) {
    config.headers.Authorization = localStorage.getItem('token');
  }
  return config;
}, (error) => {
  return Promise.reject(error);
},
);

instance.interceptors.response.use((response) => {
  return response.data.response;
}, (error) => {
  const { status, data } = error.response;
  return Promise.reject({ status, message: data.response });
});

export default instance;
