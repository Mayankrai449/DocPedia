const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',  // All API requests will be prefixed with '/api'
    createProxyMiddleware({
      target: 'http://127.1.1.1:5000',  // The URL of your FastAPI backend
      changeOrigin: true,
      pathRewrite: {
        '^/api': '',  // Remove '/api' prefix when forwarding to the backend
      },
    })
  );
};
