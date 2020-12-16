module.exports = {
  configureWebpack: {
    devServer: {
      headers: { "Access-Control-Allow-Origin": "*" }
      // should be taken care of when deployed publicly
    }
  },
  transpileDependencies: ["vuetify"]
};
