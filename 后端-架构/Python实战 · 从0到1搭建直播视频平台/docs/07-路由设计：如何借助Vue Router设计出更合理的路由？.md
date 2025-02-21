你好，我是Barry。

上节课我留过一个思考题，如果在我们平台中有一些公共的展示的内容，例如平台的Icon，我们希望在每一个页面都可以看到它，并且点击可以跳回首页，要怎么实现呢？

比较常见的一个做法就是通过路由来管理。实际开发中，一个企业级项目的页面众多，每一个页面都需要有对应的路由地址，为了保证所有链接可用，自然需要统一管理起来。

路由的配置管理在Vue框架开发中非常重要，是我们完成后续各功能模块开发的前提。因为我们需要提前配置好路由，才能控制网址和现实页面的对应关系。

这节课，我们就一起动手实践，最后给我们的视频平台配置路由。在动手之前，我们先简单了解一下 Vue 的官方路由。

## 初识 Vue Router

Vue 的官方路由是Vue Router ，在[第4节课](https://time.geekbang.org/column/article/653986)，我们也了解到过它能帮我们在Vue框架中轻松快捷地配置路由。

我们先来认识一下Vue Router中两个至关重要的标签。

1.router-link：路由的链接标签，to属性是将要跳转的路由地址（即我们预先配置好的路由地址），它的用法似于HTML的&lt;a&gt;标签。

2.router-view：路由组件出口，相当于用来显示路由地址对应组件的HTML&lt;div&gt;标签。

当我们在页面要点击链接跳转到项目中的页面时，链接就要用到router-link标签。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/16/0e/694b1fd5.jpg" width="30px"><span>🤬</span> 👍（2） 💬（1）<div>有些样式和内容不是很明确，能不能放一下代码？</div>2023-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/de/8b/426a6e29.jpg" width="30px"><span>功夫熊猫</span> 👍（1） 💬（1）<div>为啥课本里描述的代码和代码库的代码完全不同，还有人在管理吗？课件里的引入两个组件啥意思，也没找到home.vue，代码库的代码也运行不同，不知道是不是太久了，版本问题导致都失效了。
&#47;&#47;引入两个自己定义好的组件
import Home from &#39;..&#47;pages&#47;Home.vue&#39;
import About from &#39;..&#47;pages&#47;Home.vue&#39;

</div>2023-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/9d/91d795cf.jpg" width="30px"><span>ZENG</span> 👍（1） 💬（1）<div>跟着教程实操一边确实学习到很多

有几点总结一下，
1. vue-router3.x版本和4.x版本的路由配置会有一些差别，如果之前用vue-cli配置是3.x版本的可以按照 https:&#47;&#47;v3.router.vuejs.org&#47;zh&#47;guide&#47;#javascript 这个来，如果是冲重新安装的
npm install vue-router@4，按照 https:&#47;&#47;router.vuejs.org&#47;zh&#47;guide&#47; 来配置

2. 升级 babel7.x
先把 package.json babel 开头的依赖删掉，再删掉 node_modules

然后 package.json 加上：
    &quot;@babel&#47;cli&quot;: &quot;^7.21.5&quot;,
    &quot;@babel&#47;core&quot;: &quot;^7.22.1&quot;,
    &quot;@babel&#47;plugin-proposal-class-properties&quot;: &quot;^7.18.6&quot;,
    &quot;@babel&#47;plugin-transform-classes&quot;: &quot;^7.21.0&quot;,
    &quot;@babel&#47;plugin-transform-runtime&quot;: &quot;^7.22.4&quot;,
    &quot;@babel&#47;preset-env&quot;: &quot;^7.22.4&quot;,
    &quot;babel-loader&quot;: &quot;^8.0.4&quot;,
再 npm install 重新安装一下

然后修改.babelrc为：
{  
  &quot;presets&quot;: [  
    &quot;@babel&#47;preset-env&quot;  
  ],
  &quot;plugins&quot;: [
    &quot;@babel&#47;plugin-transform-runtime&quot;,
    &quot;@babel&#47;plugin-proposal-class-properties&quot;,
    &quot;@babel&#47;plugin-transform-classes&quot;
  ]
}
</div>2023-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（1） 💬（1）<div>我是访问 localhost:8080&#47;#&#47;about 才出现的页面 其实我现在也搞不清楚前端这些东西了</div>2023-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8d/db/c9d3e368.jpg" width="30px"><span>暴走的海鸽</span> 👍（1） 💬（2）<div>Home.vue组件和About.vue组件呢？</div>2023-05-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ3ibJunUcvkAibM9tBDyVB9PoiaWgf3dMZgCBbeAZUF1ISr0fiaicjRjNgThebJyHJHgxr0vjh2JeYSlA/132" width="30px"><span>冯丽娟</span> 👍（0） 💬（1）<div>about页面出不来，我是复制文中的代码的，也出不来，home页面能正常路由。</div>2024-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/0c/f0/c8950925.jpg" width="30px"><span>niniク</span> 👍（0） 💬（1）<div>SyntaxError: lmporting binding name &#39;default&quot; cannot be resolved by star export entries.
老师，这是什么原因呢</div>2024-04-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/wSdBrrprKiafx6c39iadevT8LQmrmLbFR7ewt0hicUaCybI4HvFwahiaIJ2ibqFrwBB5HiaftujHBEDcOdQxvpYoMcBA/132" width="30px"><span>魁</span> 👍（0） 💬（1）<div>想开发一个带有页面分享统计功能的表单页面，能记录打开的表单是由谁分享的，这功能能用带参数的动态路由实现吗？</div>2024-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/de/8b/426a6e29.jpg" width="30px"><span>功夫熊猫</span> 👍（0） 💬（1）<div>老师你好，安装vue-router@4的时候会报错，看起来是不是router 4的版本yao 依赖vue 3.2.0以上版本，但是前边一路教程下来，安装下来的应该是vue2.9.6版本
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
npm ERR! 
npm ERR! While resolving: video@1.0.0
npm ERR! Found: vue@2.7.15
npm ERR! node_modules&#47;vue
npm ERR!   vue@&quot;^2.5.2&quot; from the root project
npm ERR! 
npm ERR! Could not resolve dependency:
npm ERR! peer vue@&quot;^3.2.0&quot; from vue-router@4.2.5
npm ERR! node_modules&#47;vue-router
npm ERR!   vue-router@&quot;4&quot; from the root project
npm ERR! 
npm ERR! Fix the upstream dependency conflict, or retry
</div>2023-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/01/3726cf7c.jpg" width="30px"><span>明仔的阳光午后</span> 👍（0） 💬（1）<div>懒加载的写法二 `ComponentA：resolve=&gt;([&#39;需要加载的路由的地址&#39;，resolve])`没起作用，改成`ComponentA：resolve=&gt;require([&#39;需要加载的路由的地址&#39;，resolve])`之后才起作用</div>2023-08-29</li><br/><li><img src="" width="30px"><span>Geek_88cc02</span> 👍（0） 💬（1）<div>老师，有代码地址吗？叙述过于抽象了 about组件那些都么有，看不懂 我们真没基础</div>2023-06-10</li><br/><li><img src="" width="30px"><span>Geek_88cc02</span> 👍（0） 💬（1）<div>Home 组件  About 组件代码没有讲吧？</div>2023-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/4c/4b/39795aa2.jpg" width="30px"><span>阿望(tom)</span> 👍（0） 💬（1）<div>老师，你的代码Layout 里边 下边 css 用了 less, 但是在文中还有你的git代码里边 没有提到需要安装这个扩展，于是我这边搜了一下 ，按照文中给出的搭建方法，less-loader 还只能安装@5.0.0版本，,另外在 编译过程中 项目并不能100%编译 ，提示 app.vue {parse:&quot;babylon&quot;} 被废弃了 需要换成 {parser::&quot;balbel&quot;} 请问这2个问题，能讲解下吗</div>2023-05-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI7Bm7xdbwqoWPaDwqn6WESYL5QY8X8r3Q1P7UEIeDWictxJWEIJLluhIDHF7b0wFpbiav3gYToBBYg/132" width="30px"><span>Geek_840593</span> 👍（0） 💬（8）<div>ERROR  Failed to compile with 1 errors                                                                                                  18:14:14

 error  in .&#47;src&#47;components&#47;PC&#47;MyHeader.vue

Module build failed: 

.book-header {
  border-bottom: 1px solid @border-color;
                         ^
Variable @border-color is undefined
      in &#47;Users&#47;guoyan&#47;my-project&#47;src&#47;components&#47;PC&#47;MyHeader.vue (line 191, column 27)

 @ .&#47;node_modules&#47;.store&#47;vue-style-loader@4.1.3&#47;node_modules&#47;vue-style-loader!.&#47;node_modules&#47;.store&#47;css-loader@3.2.0&#47;node_modules&#47;css-loader&#47;dist&#47;cjs.js?{&quot;sourceMap&quot;:true}!.&#47;node_modules&#47;vue-loader&#47;lib&#47;style-compiler?{&quot;vue&quot;:true,&quot;id&quot;:&quot;data-v-72e0c896&quot;,&quot;scoped&quot;:true,&quot;hasInlineConfig&quot;:false}!.&#47;node_modules&#47;.store&#47;less-loader@5.0.0&#47;node_modules&#47;less-loader&#47;dist&#47;cjs.js?{&quot;sourceMap&quot;:true}!.&#47;node_modules&#47;vue-loader&#47;lib&#47;selector.js?type=styles&amp;index=0!.&#47;src&#47;components&#47;PC&#47;MyHeader.vue 4:14-463 15:3-20:5 16:22-471
 @ .&#47;src&#47;components&#47;PC&#47;MyHeader.vue
 @ .&#47;node_modules&#47;babel-loader&#47;lib!.&#47;node_modules&#47;vue-loader&#47;lib&#47;selector.js?type=script&amp;index=0!.&#47;src&#47;Layout&#47;Layout.vue
 @ .&#47;src&#47;Layout&#47;Layout.vue
 @ .&#47;node_modules&#47;babel-loader&#47;lib!.&#47;node_modules&#47;vue-loader&#47;lib&#47;selector.js?type=script&amp;index=0!.&#47;src&#47;App.vue
 @ .&#47;src&#47;App.vue
 @ .&#47;src&#47;main.js
 @ multi (webpack)-dev-server&#47;client?http:&#47;&#47;localhost:8080 webpack&#47;hot&#47;dev-server .&#47;src&#47;main.js</div>2023-05-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI7Bm7xdbwqoWPaDwqn6WESYL5QY8X8r3Q1P7UEIeDWictxJWEIJLluhIDHF7b0wFpbiav3gYToBBYg/132" width="30px"><span>Geek_840593</span> 👍（0） 💬（1）<div>npm install vue-router@4

npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
npm ERR! 
npm ERR! While resolving: my-project@1.0.0
npm ERR! Found: vue@2.7.14
npm ERR! node_modules&#47;vue
npm ERR!   vue@&quot;^2.5.2&quot; from the root project
npm ERR! 
npm ERR! Could not resolve dependency:
npm ERR! peer vue@&quot;^3.2.0&quot; from vue-router@4.2.0
npm ERR! node_modules&#47;vue-router
npm ERR!   vue-router@&quot;4&quot; from the root project
npm ERR! 
npm ERR! Fix the upstream dependency conflict, or retry
npm ERR! this command with --force or --legacy-peer-deps
npm ERR! to accept an incorrect (and potentially broken) dependency resolution.
npm ERR! 
npm ERR! 
npm ERR! For a full report see:</div>2023-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>Q1:&lt;my-header ref=&quot;myheader&quot;&gt;&lt;&#47;my-header&gt;，这行代码中， &lt;my-header&gt;是在哪里定义的？或者不需要定义就可以直接使用？  Ref用的myheader又是哪里定义的？ (my-footer也是同样的问题)
Q2：layout组件在template里面也没有使用啊，哪里使用的？</div>2023-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/09/98/397c2c81.jpg" width="30px"><span>贾维斯Echo</span> 👍（0） 💬（3）<div>给个建议,代码放到git上面</div>2023-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/8f/88/3814fea5.jpg" width="30px"><span>安静点</span> 👍（0） 💬（1）<div>我觉得可以建一个git仓库，把每节课的代码放上面。
因为肯定有人是无法跟着一步步都实现的，
很不幸，我就是那个人😂</div>2023-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/03/c5/b3364e49.jpg" width="30px"><span>佩慎斯予氪蕾沐</span> 👍（0） 💬（1）<div>整合 UI 组件库 Element-UI，可以按照官网操作，我个人经常用的是vite的按需引入，在官网按需引入介绍中可能只是按需引入一些组件，样式我认为还需要在全局import elementui的css样式。
我在vant4中就是好奇已经按需引入，但是弹出的组件却没有样式，还需要自己引入，官网按需引入又没有介绍自动引入css样式，需要在全局引入，就这样被坑了十几分钟。</div>2023-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/03/c5/b3364e49.jpg" width="30px"><span>佩慎斯予氪蕾沐</span> 👍（0） 💬（1）<div>this.$router.push(&quot;&#47;video&#47;detail&#47;&quot; + video.id);
在vue3的组合式写法中，也就是setup，没有this, 要使用路由可以用下面的写法
import {useRouter} from &#39;vue-router&#39;
const router ＝useRouter()
router.push(&quot;&#47;video&#47;detail&#47;&quot; + video.id)

前几天写小项目的时候遇见的，useRoute和useRouter的区别是，前者用于获取，后者用于跳转等一系列操作，至少我是这样理解的

在vue3中选项式写法需要export 和 return，而我个人更倾向于组合式，写法更加简洁不需要那两步，不过选项式写法也是可以适应的</div>2023-05-08</li><br/><li><img src="" width="30px"><span>Geek_88cc02</span> 👍（0） 💬（1）<div>&#47;&#47;引入两个自己定义好的组件import Home from &#39;..&#47;pages&#47;Home.vue&#39;import About from &#39;..&#47;pages&#47;Home.vue&#39;

这里是在哪里说了自定义的，没看到</div>2023-06-10</li><br/><li><img src="" width="30px"><span>Geek_88cc02</span> 👍（0） 💬（0）<div>我安装vue 的时候，已经帮我搞定“第二步，我们要定义一个路由配置的文件。比如在项目 src 文件夹下建一个 router 文件夹，然后进入 router 文件夹，在里面创建一个 index.js 文件。”</div>2023-06-10</li><br/>
</ul>