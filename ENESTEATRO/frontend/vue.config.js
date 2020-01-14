const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  publicPath: "/static/",
  outputDir: './dist/',
  chainWebpack: config => {
        config.optimization.splitChunks(false)
        config.plugin('BundleTracker').use(BundleTracker, [{filename: 'webpack-stats.json'}])
        config.resolve.alias.set('__STATIC__', 'static')

        config.devServer
            .public('http://0.0.0.0:8082')
            .host('0.0.0.0')
            .port(8082)
            .hotOnly(true)
            .watchOptions({poll: 1000})
            .https(false)
            .headers({"Access-Control-Allow-Origin": ["\*"]})
  },

  /*"transpileDependencies": [
    "vuetify"
  ]*/
}
