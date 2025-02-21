你好，我是大圣，上一讲我们学完vue-router源码，Vue全家桶的生态就基本介绍完了，包括Vue的响应式、运行时、编译器，以及全家桶的vuex和vue-router。

今天我来给你介绍Vue中优化的一个进阶知识点：SSR（Server Side Rendering），也就是服务端渲染。

## SSR是什么

要想搞清楚SSR是什么？我们需要先理解这个方案是为解决什么问题而产生的。

在现在MVVM盛行的时代，无论是Vue还是React的全家桶，都有路由框架的身影，所以，页面的渲染流程也全部都是浏览器加载完JavaScript文件后，由JavaScript获取当前的路由地址，再决定渲染哪个页面。

这种架构下，**所有的路由和页面都是在客户端进行解析和渲染的，我们称之为Client Side Rendering，简写为CSR，也就是客户端渲染**。

交互体验确实提升了，但同时也带来了两个小问题。

首先，如果采用CSR，我们在ailemente项目中执行`npm run build`命令后，可以在项目根目录下看到多了一个dist文件夹，打开其中的index.html文件，看到下面的代码：

```xml
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vite App</title>
    <script type="module" crossorigin src="/assets/index.c305634d.js"></script>
    <link rel="modulepreload" href="/assets/vendor.9419ee42.js">
    <link rel="stylesheet" href="/assets/index.1826a359.css">
  </head>
  <body>
    <div id="app"></div>
    
  </body>
</html>

```
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/36/46/d2c7a84e.jpg" width="30px"><span>kai</span> 👍（3） 💬（0）<div>SSR等并不是什么新技术，早期魔板还是后端处理的时代，这些技术点实现都是一样的原理。</div>2022-07-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eq6UjL0SBicZgyKzsAnCf08l0MibyqxsCecSVXa3tKvSDeDG6XRe1ngziaChRiaRcA0kzOlIwfcnNZvwg/132" width="30px"><span>Alias</span> 👍（1） 💬（1）<div>厉害了，react的next 中有 ssg  概念，看到这里，vue也有，一下子就豁然开朗了，前端框架解决某一类问题的理念都大差不差啊，学习就融会贯通而已</div>2022-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/d0/82/791d0f5e.jpg" width="30px"><span>大将</span> 👍（0） 💬（0）<div>其实完全没有在使用，感觉现在很多情况下对前端的感知已经有些麻木了。</div>2024-03-29</li><br/><li><img src="" width="30px"><span>Geek_c63012</span> 👍（0） 💬（0）<div>1. 减少白屏时间
2. 利于seo优化</div>2023-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/fe/8a/8b5f5a66.jpg" width="30px"><span>下一个起跑点</span> 👍（0） 💬（1）<div>我这个用egg.js渲染出来的首页模板，点击那个num的&lt;h&gt;标签,怎么不能触发click事件啊？你们的能正常js吗</div>2022-06-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/yyibGRYCArsUNBfCAEAibua09Yb9D5AdO8TkCmXymhAepibqmlz0hzg06ggBLxyvXicnjqFVGr7zYF0rQoZ0aXCBAg/132" width="30px"><span>james</span> 👍（0） 💬（0）<div>厉害了，很全面</div>2022-01-19</li><br/>
</ul>