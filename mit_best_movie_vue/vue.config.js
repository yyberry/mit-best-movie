const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    https: false,  // 启用 HTTPS
    host: '0.0.0.0',
    port: 8080,
  },
})
