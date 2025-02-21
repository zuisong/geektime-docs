你好，我是大圣。

上一讲学完了Vue的编译原理后，我们就把Vue的整体流程梳理完毕了，但是我们在使用Vue的时候，还会用到很多Vue生态的库。所以从今天开始，我会带你了解几个Vue生态中重要成员的原理和源码，今天我先带你剖析一下我们项目中用的工程化工具Vite的原理。

## 现在工程化的痛点

现在前端开发项目的时候，工程化工具已经成为了标准配置，webpack是现在使用率最高的工程化框架，它可以很好地帮助我们完成从代码调试到打包的全过程，但是随着项目规模的爆炸式增长，**webpack也带来了一些痛点问题**。

最早webpack可以帮助我们在JavaScript文件中使用require导入其他JavaScript、CSS、image等文件，并且提供了dev-server启动测试服务器，极大地提高了我们开发项目的效率。

webpack的核心原理就是通过分析JavaScript中的require语句，分析出当前JavaScript文件所有的依赖文件，然后递归分析之后，就得到了整个项目的一个依赖图。对图中不同格式的文件执行不同的loader，比如会把CSS文件解析成加载CSS标签的JavaScript代码，最后基于这个依赖图获取所有的文件。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/5f/eb/ef7aa4c1.jpg" width="30px"><span>特供版</span> 👍（11） 💬（1）<div>流程：
1.  请求 首页http:&#47;&#47;xxx.xxx.xxx&#47; 
2.  返回 index.html
3.  请求 &#47;src&#47;main.js
4. 发现请求js文件，替换路径为相对路径后，返回修改后的js文件
5.  请求 @module&#47;vue
6.  发现请求@module内的文件，替换文件内为相对路径后，返回package.json中module定义的入口文件
7.  请求 .&#47;App.vue
8.  判断 .vue 的请求后，通过 compilerSFC.parse解析 Vue 组件，通过返回的 descriptor.script 获取 js 代码
9.  请求 .&#47;App.vue?type=template
10.  调用 compilerDom.compile 解析 template 内容，直接返回 render 函数</div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/8a/d7/daabec34.jpg" width="30px"><span>tequ1lAneio</span> 👍（3） 💬（3）<div>有源码吗，一直在报process未定义的错误</div>2022-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/7c/3cfece5e.jpg" width="30px"><span>润培</span> 👍（3） 💬（1）<div>模块如果是分散的，可以使用“依赖预构建”，通过预构建生成一个模块，这样只会有一个 http 请求。

https:&#47;&#47;cn.vitejs.dev&#47;guide&#47;dep-pre-bundling.html

https:&#47;&#47;cn.vitejs.dev&#47;config&#47;#dep-optimization-options</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b1/84/d7034d7c.jpg" width="30px"><span>吴颜</span> 👍（2） 💬（1）<div>写的太简单，你这也没写出一个迷你的vite啊</div>2022-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/60/fd/c08731d7.jpg" width="30px"><span>Chen.Lu</span> 👍（0） 💬（1）<div>【Vite 热更新】小模块中 chalk 是定义 log 颜色的工具，不是监听文件&#47;文件夹的工具吧。
chokidar 是监听文件&#47;文件夹的工具</div>2022-01-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIkBhCDbibPDmDTEW6Uia1LAEOcFf75QxA897gcL4oXFMOwgsqFwf7rhPoUoJWgICl0xFT8Iz2cuWRg/132" width="30px"><span>InfoQ_e521a4ce8a54</span> 👍（0） 💬（2）<div>从[Vite 的热更新]开始，代码片段所在的文件目录和所需的依赖就搞不清楚了。。。</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c8/04/fed4c1ad.jpg" width="30px"><span>若川</span> 👍（21） 💬（0）<div>我之前也写过一篇mini-vue的分析文章，感兴趣的可以结合大圣老师的文章对比看看实现～

尤雨溪几年前开发的“玩具 vite”，才100多行代码，却十分有助于理解 vite 原理
https:&#47;&#47;juejin.cn&#47;post&#47;7021306258057592862</div>2022-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0d/37/2bcf8c5f.jpg" width="30px"><span>Geek_37g</span> 👍（1） 💬（0）<div>热更新源码在哪儿呢？</div>2023-07-06</li><br/><li><img src="" width="30px"><span>Geek_07f3c3</span> 👍（0） 💬（1）<div>vite打包时提示包体积过大，请问应该怎压缩呢或者怎么分包</div>2022-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/59/57/7201d6ce.jpg" width="30px"><span>null</span> 👍（0） 💬（0）<div>开发过程中出现加载慢，timeout。</div>2022-02-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJfTnE46bP9zFU0MJicYZmKYTPhm97YjgSEmNVKr3ic1BY3CL8ibPUFCBVTqyoHQPpBcbe9GRKEN1CyA/132" width="30px"><span>逗逼章鱼</span> 👍（0） 💬（0）<div>以后 importmap 会变成主流吗？</div>2022-02-08</li><br/><li><img src="" width="30px"><span>Geek_4da4e1</span> 👍（0） 💬（1）<div>css文件替换换行符windows下不行，&#47;r也有可能</div>2022-01-18</li><br/>
</ul>