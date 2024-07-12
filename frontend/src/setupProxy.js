const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',  // prefixed with '/api'
    createProxyMiddleware({
      target: 'http://127.1.1.1:5000',  // backend url
      changeOrigin: true,
      pathRewrite: {
        '^/api': '', 
      },
    })
  );
};
