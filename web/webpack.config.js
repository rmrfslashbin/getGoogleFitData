const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CopyPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const HtmlWebpackExternalsPlugin = require('html-webpack-externals-plugin')
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
    //mode: 'development',
    entry: './src/app.js',
    devtool: 'inline-source-map',
    devServer: {
        https: true,
        contentBase: './dist'
    },
    output: {
        path: path.resolve(__dirname, 'dist'),
    },
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [
                    { loader: process.env.NODE_ENV !== 'production' ? 'style-loader' : MiniCssExtractPlugin.loader}, // creates style nodes from JS strings
                    { loader: "css-loader"}, // translates CSS into CommonJS
                    { 
                        loader: "sass-loader",  // compiles Sass to CSS, using Node Sass by default
                        options: {
                            sassOptions: {
                                includePaths: ['./node_modules']
                            }
                        }
                    }
                ]
            },
            {
                test: /\.(png|svg|jpg|gif)$/,
                use: [
                    'file-loader'
                ]
            }
        ]
    },
    plugins: [
        new HtmlWebpackPlugin({
            title: 'Google Fit Heartbeats',
            meta: {viewport: 'width=device-width, initial-scale=1, shrink-to-fit=no'}
        }),
        new HtmlWebpackExternalsPlugin({
            externals: [
                {
                    module: 'google-roboto',
                    entry: {
                        path: 'https://fonts.googleapis.com/css?family=Roboto:300,400,500',
                        type: 'css',
                    },
                },
            ],
        }),
        new CleanWebpackPlugin(),
        new MiniCssExtractPlugin({
            filename: "[name].css",
            chunkFilename: "[id].css"
        }),
        new CopyPlugin([
            {from: "data/data.json", to: "data.json"}
        ]),
    ],
    resolve: {
    extensions: ['.js', '.scss']
  }
};
