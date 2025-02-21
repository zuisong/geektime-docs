你好，我是Barry。

我们都知道网站的美观性非常重要，不同的网站也会有不同的设计风格。比如工具类网站一般比较简洁，娱乐类的网站一般比较丰富多彩，办公类网站比较商务，学习类的网站比较学院风。

我们的视频平台是娱乐性质的网站，应该丰富多彩，比较有活力。而平台众多页面中，首页是用户进入一个平台的入口，也是流量最大的地方。

这节课，我们就从首页入手，一起来应用前面讲过的CSS + Element-UI ，学习一下如何设计和实现页面的开发。

## 首页该如何设计？

我们先来思考一下，网站首页应该如何设计。

首页最直接的作用就是把平台的主要功能展示给用户。不过首页要展示的东西通常比较多，所以需要设计分区，每个分区负责展示一类事物。

为了方便你理解，我们一起观察一些常见的网站都是怎么做的。首先来看看百度，可以看到百度首页核心的搜索功能放在了Header的下面，再往下放的是一些次要的功能——推荐和热搜。

核心功能、推荐和热搜这三块就形成了首页的三个分区。

![](https://static001.geekbang.org/resource/image/77/30/77b0ea3dc9ce48571590aca01yyf8a30.jpg?wh=2874x1546)

我们再来看一下京东的页面。  
![](https://static001.geekbang.org/resource/image/fb/e5/fbb8956c9402c058c37fc58781yy27e5.jpg?wh=2878x1328)

![](https://static001.geekbang.org/resource/image/3e/f8/3e0df79309819393e6bdee38c9ba25f8.jpg?wh=2870x1488)

可以看到，Header下面是核心商品搜索功能和各项菜单栏，中间是广告轮播区。再往下是相对重要的秒杀商品，接下来是各种频道和商品。

例子看完了，我们再来归纳总结一下。**首页的定位是要展示一个网站具有的功能，同时也像分发器一样是跳转到其他页面的开始。**首页需要按功能做分区，核心位置要突出展示核心功能，按重要程度依次往下。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/a1/12/24024e2b.jpg" width="30px"><span>radeon</span> 👍（2） 💬（1）<div>根据老师的vue2代码主体逻辑，我使用vue3+ts搭建了项目，对于项目文件结构不清晰或者想用vue3的朋友们可以看过来，现在已完成首页静态页面部分，代码已发布在github以及gitee，并使用MIT协议开源，欢迎大家前来指点或者在此基础上继续开发或改进！
github: https:&#47;&#47;github.com&#47;0x3147&#47;just-see-it 
gitee: https:&#47;&#47;gitee.com&#47;kang-jiaxing&#47;just-see-it</div>2023-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（1）<div>sudo npm install --save vue-content-loader
Password:
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
npm ERR! 
npm ERR! While resolving: vue-test-1@1.0.0
npm ERR! Found: vue@2.7.14
npm ERR! node_modules&#47;vue
npm ERR!   vue@&quot;^2.5.2&quot; from the root project
npm ERR! 
npm ERR! Could not resolve dependency:
npm ERR! peer vue@&quot;^3&quot; from vue-content-loader@2.0.1
npm ERR! node_modules&#47;vue-content-loader
npm ERR!   vue-content-loader@&quot;*&quot; from the root project
npm ERR! 
npm ERR! Fix the upstream dependency conflict, or retry
npm ERR! this command with --force, or --legacy-peer-deps
npm ERR! to accept an incorrect (and potentially broken) dependency resolution.
npm ERR! 
npm ERR! See &#47;Users&#47;kindyli&#47;.npm&#47;eresolve-report.txt for a full report.

npm ERR! A complete log of this run can be found in:
npm ERR!     &#47;Users&#47;kindyli&#47;.npm&#47;_logs&#47;2023-06-17T12_56_24_738Z-debug-0.log</div>2023-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（4）<div>老师，求助
Module build failed: 

    .icon-fire {
        .icon(&quot;&#47;Users&#47;kindyli&#47;zz&#47;vue-test-1&#47;src&#47;assets&#47;image&#47;Index&#47;icon_fire.png&quot;);
      ^
.icon is undefined

这个.icon是需要在哪里定义的</div>2023-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（2）<div>老师上传的代码好像只有对应的文件，没有完整的项目结构，会缺少部分文件依赖，比如这节这个组件BulletListLoader</div>2023-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（1）<div>老师，你好，点击事件 goDetail(main_recommend) 这个main_recommend这个参数是如何传递的，或者说，一个点击事件，处理点击函数可以传递哪些参数</div>2023-06-17</li><br/><li><img src="" width="30px"><span>Geek_d671c1</span> 👍（0） 💬（2）<div>index文件报错：Cannot find module &#39;vue-content-loader&#39; or its corresponding type declarations.ts(2307)

你好，请问这个问题如何解决？</div>2023-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/9d/91d795cf.jpg" width="30px"><span>ZENG</span> 👍（0） 💬（2）<div>老师，请问一下在 MyHeader 组件中使用 ElementUI 下拉菜单，其中每个 item 都有加上 @click.native，这个和原来不加上 native 有什么区别呢？我搜索了一下我的理解是父组件引入的子组件，如果直接使用@click事件是不会有作用的，使用@click.native就可以触发事件，是不是相当代替$emit的作用呢</div>2023-06-14</li><br/><li><img src="" width="30px"><span>Geek_d671c1</span> 👍（0） 💬（1）<div>你好，有整个项目的源码吗，不按照课时区分？</div>2023-06-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI7Bm7xdbwqoWPaDwqn6WESYL5QY8X8r3Q1P7UEIeDWictxJWEIJLluhIDHF7b0wFpbiav3gYToBBYg/132" width="30px"><span>Geek_840593</span> 👍（0） 💬（1）<div>老师能放一下前端部分的项目结构吗？初学者有点懵</div>2023-05-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI7Bm7xdbwqoWPaDwqn6WESYL5QY8X8r3Q1P7UEIeDWictxJWEIJLluhIDHF7b0wFpbiav3gYToBBYg/132" width="30px"><span>Geek_840593</span> 👍（0） 💬（1）<div>JSX 表达式必须具有一个父元素?请问这个怎么处理？</div>2023-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（0）<div> For Vue 2 &amp; Nuxt 2, use vue-content-loader@^0.2 instead.</div>2023-06-17</li><br/>
</ul>