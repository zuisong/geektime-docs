你好，我是杨文坚。

看到这个题目，你是不是觉得有点疑惑？明明Vue.js 3官方标配的编译工具是Vite，为什么我不先讲Vue.js 3结合Vite进行项目编译，而是先教你用Webpack编译Vue.js 3项目呢？

这是因为，我们这个课程是要做一个“企业级项目的实战”，而在企业技术开发中，第一要素就是保证功能的稳定性和可用性。在这一点上，Webpack比Vite有更大优势。它发布于2013年，拥有较好的技术生态，基本上，你用Webpack项目打包构建遇到任何问题，都能在网上找到相关场景的直接解决方案或者间接解决思路。而Vite比较年轻，在2020年才发布正式版，在技术生态的沉淀上并没有Webpack那么丰富。

所以，这一讲中，我们还是先来讲讲怎么用Webpack来编译Vue.js 3项目。开始之前，我们先来看看除了Webpack生态更稳定的因素外，Webpack和Vite究竟还有什么区别，让你对这两个工具有更深入的了解。

## Webpack和Vite有什么区别？

我在研究技术的时候经常在想，脱离技术的定位来对比技术好坏都是耍流氓。因为每一种流行的技术之所以被人接纳，肯定是有其诞生的定位和开发者的使用定位。所以我们要对比Webpack和Vite，最重要是**对比这两种技术工具的定位**。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Pk7HVX99cBlSOicLoa8KN81xqHa4YzRQsu5PAGTlOJgvChtl7T6BE6gTOhiaVJIcNVxIsRO1libPjdkZ6Sq8Qlp1g/132" width="30px"><span>Geek_b640fe</span> 👍（9） 💬（1）<div>‘NODE_ENV’ 不是内部或外部命令，也不是可运行的程序或批处理文件
windows 环境必须安装 cross-env 模块，并在启动命令前安装
npm i -D cross-env

    &quot;scripts&quot;: {
        &quot;dev&quot;: &quot;cross-env NODE_ENV=development webpack serve -c .&#47;webpack.config.js&quot;,
        &quot;build&quot;: &quot;cross-env NODE_ENV=production webpack -c .&#47;webpack.config.js&quot;
    },</div>2022-12-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/dCfVz7wIUT4fM7zQO3gIwXo3BGodP5FJuCdMxobZ5dXpzBeTXiaB3icoFqj22EbIGCu1xxd1FLo9xic0a2pGnunibg/132" width="30px"><span>风太大太大</span> 👍（5） 💬（1）<div>Webpack 3 4 5每个版本差异还挺大的，plugin变更，语法变更，对缓存的使用程度，打包构建加速那个版本的方案都不同，版本越高越方便</div>2022-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/ae/27/74828c37.jpg" width="30px"><span>ZR-rd</span> 👍（4） 💬（1）<div>老师，大厂一般都是使用 CDN 来导入 Vue 等第三方库的吗？为什么不是直接打包到 bundle 中呢？这样有什么优缺点呢？</div>2022-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/6b/77bb8501.jpg" width="30px"><span>丫头</span> 👍（2） 💬（3）<div>webpack.default.js
webpack.dev.js
webpack.prod.js
不同环境独立文件，会不会更清晰些</div>2022-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/b4/d7a89271.jpg" width="30px"><span>健牌哥.</span> 👍（0） 💬（1）<div>dev配置的devServer把static.directory修改成 path.join(__dirname, &#39;public&#39;)，本地node_modules的vue运行时文件就加载不成功了，index.html已放在public文件夹里。请问下这个怎么解决呢？</div>2023-01-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/1ornnGqSaTxRdbxhUHibeygI3PLtDXAH5GRhRJ286Sbtz7YyGFUHobN2EgiaLhtWn2dLReBRBU1n577DWqrsaBBw/132" width="30px"><span>定宇</span> 👍（0） 💬（1）<div>想問一下，如果在webpack輸出檔案有加hash值的話
ex:
```
output: {
      path: path.join(__dirname, &#39;..&#47;dist&#39;),
      publicPath: &#39;&#47;&#39;,
      filename: &#39;[name].[hash].js&#39;,
}
```

在HtmlWebpackPlugin那邊要怎麼設置呢？</div>2022-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3f/c0/34453755.jpg" width="30px"><span>我只想要简单的小幸福👣</span> 👍（0） 💬（1）<div>完整代码地址打不开，能换一个别的地址吗</div>2022-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/f9/39492855.jpg" width="30px"><span>阿阳</span> 👍（0） 💬（2）<div>在 test: &#47;\.(css|less)$&#47;中，less文件也能直接用css-loader进行处理嘛？不是需要用less-loader进行处理么？</div>2022-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/f9/39492855.jpg" width="30px"><span>阿阳</span> 👍（0） 💬（2）<div>windows环境下，设置环境变量NODE_ENV需要用到cross-env这个包吧？</div>2022-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/bd/ea9c16b8.jpg" width="30px"><span>莫比斯</span> 👍（0） 💬（3）<div>还有老师，我想补充一点点，在line 50 if语句前，可以申明config，let config；</div>2022-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/41/06/58a4cb03.jpg" width="30px"><span>不是牛仔但很忙ᥬ🙂᭄</span> 👍（0） 💬（1）<div>这个课是纯音频课？没有视频？</div>2022-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e7/a0/9a962a74.jpg" width="30px"><span>joker</span> 👍（0） 💬（1）<div>Vite以后会讲吗</div>2022-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/56/08/bd75f114.jpg" width="30px"><span>WGH丶</span> 👍（7） 💬（0）<div>推荐资料：《webpack实战：入门、进阶与调优》。</div>2022-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6a/22/527904b2.jpg" width="30px"><span>hao-kuai</span> 👍（0） 💬（0）<div>在使用体验上来说：vite之于webpack就像webstorm之于vscode</div>2025-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/4b/07/33bc5bbd.jpg" width="30px"><span>文件</span> 👍（0） 💬（1）<div>这里的全局变量window.Vue是什么，求解答。</div>2024-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9f/fd/bb79fa8d.jpg" width="30px"><span>null</span> 👍（0） 💬（1）<div>老师好，我按文档中的配置自己写了一遍，根据git上完整代码补全了 webpack.config 的配置，启动后报错：&quot;Cannot read properties of undefined (reading &#39;createApp&#39;)&quot;，打开network看到 vue.global.js也加载成功了，不知道是什么原因</div>2023-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/89/15/381ce65f.jpg" width="30px"><span>不曾相识</span> 👍（0） 💬（0）<div>如果是webpack5, 可以 这样配置 --env NODE_ENV=production 
用:  const config = (env) =&gt; {
  return 配置对象
}</div>2023-02-26</li><br/>
</ul>