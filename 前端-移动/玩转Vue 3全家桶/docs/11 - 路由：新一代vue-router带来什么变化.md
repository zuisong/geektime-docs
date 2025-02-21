你好，我是大圣。

在上一讲中，我带你了解了Vuex这个数据管理框架的使用方法，以及Vue 3中数据管理框架的来源、实战细节和相关的原理。

其实项目中除了数据管理，路由系统也是非常核心的模块。所以在这一讲中，我会先带你了解一下前端开发方式的演变，让你明白前端路由因何而来，之后再讲解前端路由的实现原理。最后，我会再带你手写一个vue-router，并在这个过程中为你补充相关的实战要点，让你对如何用好vue-router有一个直观体验。

## 前后端开发模式的演变

在jQuery时代，对于大部分Web项目而言，前端都是不能控制路由的，而是需要依赖后端项目的路由系统。通常，前端项目也会部署在后端项目的模板里，整个项目执行的示意图如下：

![图片](https://static001.geekbang.org/resource/image/26/2b/26ddd952f1f7d6dc3193af5be57e202b.jpg?wh=1569x462)

jQuery那个时代的前端工程师，都要学会在后端的模板，比如JSP，Smatry等里面写一些代码。但是在这个时代，前端工程师并不需要了解路由的概念。对于每次的页面跳转，都由后端开发人员来负责重新渲染模板。

前端依赖后端，并且前端不需要负责路由的这种开发方式，有很多的优点，比如开发速度会很快、后端也可以承担部分前端任务等，所以到现在还有很多公司的内部管理系统是这样的架构。当然，这种开发方式也有很多缺点，比如前后端项目无法分离、页面跳转由于需要重新刷新整个页面、等待时间较长等等，所以也会让交互体验下降。
<div><strong>精选留言（26）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/c8/4a/3a322856.jpg" width="30px"><span>ll</span> 👍（50） 💬（5）<div>本节又是收获满满，巩固加回顾了关于前端路由的整体知识结构，有一下几点：

1. 什么是路由
   所谓 router 是干什么的？是指 route 的，这里中文翻译的是 “路”。何为“路由”，可能是“路由哪里 
   来&quot;；这里的“路”，广义上来说是“资源”，可以是“页面”，也可以是 json 音视频等等。

   如果把路由具象化，它是这么个东西；你告诉它一串神秘的代码（地址，url等），它给你“宝贵的资
   源”，它就是个“指路的”。

   路由是“天然”存在的，因为我们所有在网上的行为本质都是向“某个地方”要“某些资源”

 2. 前后端路由的区别的补充
    传统方式与SPA“页面跳转”的问题涉及一个核心的问题，是“导航流程”，具体可以参考，李兵老师 
    《浏览器工作原理与实践》中导航流程一节。

    导航流程简单说，就是浏览器地址栏输入地址后，到浏览器准备渲染页面前这个阶段。开始流程的 
    一个标志，就是浏览器标签页标题左边开始转圈圈。

    传统的开发模式写出的页面，在每一次请求网络资源的过程，理论上都有这个流程。这可能就是两者 
    之间性能差异所在

    而 SPA 开发模式，网络资源用 XMLHttpRequest 调用，页面部分用JS“模拟”页面刷新。这里JS模拟部
    分就是现在所学 vue-router 的工作。

 3. 关于路由实现
    总结下，时间以2014年，HTML5标准作为分野，分两个部分
    – API：location.hash；Event：hashchange
    – API：history.pushState，history.replaceState；Event：popstate

    这个就是前端路由的实现核心，如果对具体API感兴趣，可以参考《Javascript 高级程序设计》第4
    版，12章，关于 BOM 的描述。

    大致意思是 hash 的改变不触发页面 reloads；pushState，replaceState 改变 history 也不触发
    reloads。浏览器的这种行为，是根据 HTML5 这个标准实现的

    然后，第一个API支持了路由的 hash 模式，在这之前 hash 的应用 &lt;a id=&quot;xxx&quot;&gt; 在页面中的定位，
    第二个API支持了路由的 history 模式，但这个需要后端配合调整下后端路由；为什么，试着将要跳 
    转的地址复制到浏览器地址栏，然后按回车，分析下页面渲染的过程，大概就清楚了。</div>2021-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3a/e2/c48bd3b7.jpg" width="30px"><span>Kevin</span> 👍（7） 💬（4）<div>关于webHashHistory,和webHistory 我这里有一个实践要注意的点，不知是否正确。
就是是否需要服务器这个角色参与。
whh，完全是在浏览器中完成的路由行为。
wh 可能是要有服务器参与的 
这一点，在最近的项目中，将vue项目打包直接放到Android assert目录下时，使用两种路由一个404, 一个正常，后续改成了whh了

请大佬，解惑。</div>2021-11-10</li><br/><li><img src="" width="30px"><span>Geek_4578dc</span> 👍（3） 💬（1）<div>大圣 实战代码仓库地址 能发一下吗</div>2021-11-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIdLUtkvdNcLTEebUx5rY36rzibJjMeiazPbIvGtNWWKE0iafVpNticFNFakUHVKjEy6ztqn3TX002ueQ/132" width="30px"><span>balabla</span> 👍（2） 💬（1）<div>大圣老师，看完之后，仍有几个问题，求翻牌+1
1.能说下vue-router3.x到vue-router4.x有什么需要重点关注的地方嘛
2.vue-router3.x和vue-router4.x 从底层实现原理上，是否有变化
3.代码里current 的响应式用的 ref 和用vue.util.definereactive 效果一样嘛</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/0e/32/df72d0c1.jpg" width="30px"><span>Jerry.L</span> 👍（1） 💬（1）<div>大圣老师，我跟你一样的代码，为什么在命令行提示：[@vue&#47;compiler-sfc] `defineProps` is a compiler macro and no longer needs to be imported.然后在浏览器控制台又提示：Uncaught SyntaxError: The requested module &#39;&#47;src&#47;router&#47;grouter&#47;index.js&#39; does not provide an export named &#39;default&#39;。</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5d/22/6e78881e.jpg" width="30px"><span>Aaron</span> 👍（1） 💬（1）<div>老师好，调用 pushState replaceState 并不会触发 popstate 事件，监听通常需要 hack 这两个 api。
https:&#47;&#47;developer.mozilla.org&#47;en-US&#47;docs&#47;Web&#47;API&#47;PopStateEvent#:~:text=Note%3A%20Just%20calling%20history.pushState()%20or%20history.replaceState()%20won%27t%20trigger%20a%20popstate%20event.</div>2021-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/ff/d1/7a4a6f4f.jpg" width="30px"><span>风一样</span> 👍（1） 💬（3）<div>老师请问Router对象的install，是在哪里用呢？在源码中没有看到，还有install函数的参数，是什么对象呢？</div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/22/41/f179e7b5.jpg" width="30px"><span>香橙派来的</span> 👍（1） 💬（1）<div>有了 RouterView 组件后，我们再来实现 router-link 组件。我们在 grouter 下面新建文件 RouterILnk.vue，并写入下面的代码。代码中的 template 依然是渲染一个 a 标签，只是把 a 标签的 href 属性前面加了个一个 #， 就实现了 hash 的修改。

老师，这一段中的 “新建文件RouterILnk.vue ” 与下文的注册 “import RouterLink from &#39;.&#47;RouterLink.vue&#39; ”的文件名字对不上，应该是打错了，会找不到资源</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/4a/75/51435f4b.jpg" width="30px"><span>@</span> 👍（1） 💬（1）<div>
&lt;template&gt;
    &lt;a :href=&quot;&#39;#&#39;+props.to&quot;&gt;
        &lt;slot &#47;&gt;
    &lt;&#47;a&gt;
&lt;&#47;template&gt;

&lt;script setup&gt;
let props = defineProps({
    to:{type:String,required:true}
})

&lt;&#47;script&gt;

这里是否需要引入下defineProps，大段代码部分能否内部写点注释
建议老师跟着文章里的代码打一遍，看看能不能跑通
代码上 有些马虎  是否是从课件里粘出来的时候整漏了</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/d8/96/dcf52430.jpg" width="30px"><span>关关君</span> 👍（1） 💬（4）<div>很早啊就知道History这个API了但是没用过也用不上，但今天用History写路由的时候，看了API才发现使用history.pushState()方法的时候不会触发 popstate 这个事件，只有当浏览器操作行为的时候才会触发，就比如back forward。
所以在实现的时候调用完pushState之后我手动修改的current.value 的值才成功了。</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/a8/8da58e53.jpg" width="30px"><span>海阔天空</span> 👍（1） 💬（2）<div>现在一般都用history路由了吧，history路由与html5的配合更好，能充分利用html5的特性，比如html5中监听滚动条的状态等，history都可以监听</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/02/9d/566b9065.jpg" width="30px"><span>拼搏、进取</span> 👍（1） 💬（1）<div>const comp = computed(()=&gt;{
    const route = router.routes[0].children.find(
        (route) =&gt; route.path === router.current.value    )

    return route?route.component : null
})
大圣老师， router.routes[0].children，这里报错了。我改成outer.routes.find()......</div>2021-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/22/32/10c26ee4.jpg" width="30px"><span>一线蓝光</span> 👍（1） 💬（2）<div>在计算匹配的组件时，我们直接取得 children 匹配即可。这里我使用children匹配不上，直接使用router.routes进行的匹配， 麻烦问下是什么原因呢</div>2021-11-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/8NIo06kqG0V5GL2UvFVBVkkuKdhT3BjO8ZUIibvXmFSgc0tvsOiaH9IibchvMKtpdnfKfFckuhdcicyghVV30BDhicA/132" width="30px"><span>Devo Zou</span> 👍（0） 💬（1）<div>function createWebHistory() {
  function bindEvents(fn) {
    window.addEventListener(&quot;popstate&quot;, fn);
  }
  return {
    bindEvents,
    url: window.location.pathname || &quot;&#47;&quot;,
  };
}

另外再把RouterLink里面的a标签href的 &#39;#&#39; 去掉就可以实现history 模式了。不知道这样实现对不对[捂脸]
</div>2021-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/6b/91/168e10a1.jpg" width="30px"><span>bugu</span> 👍（0） 💬（1）<div>本期bug题解：https:&#47;&#47;github.com&#47;HaoChunYang&#47;vue3-class&#47;blob&#47;main&#47;todo-list&#47;src&#47;router&#47;hrouter&#47;RouterView.vue
哈哈</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9f/90/4656119a.jpg" width="30px"><span>拖鞋</span> 👍（5） 💬（0）<div>补充一下 vue-router 4.x 已经废弃了 hashchange 统一使用 popstate</div>2022-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/1f/0d/576f1266.jpg" width="30px"><span>郭庆</span> 👍（3） 💬（0）<div>history.pushState()并不会触发监听的popstate事件，得自己手动改current.value的值。。。
</div>2022-05-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/18yCkSMTZyw78cUmquiceycC9lDnUFqFO1dU44jG0j9lCr7LB0oDOQ5uMylBNarIAzOnbrR4Vfdab6wO4FQIQLw/132" width="30px"><span>艾瑞</span> 👍（3） 💬（5）<div>老师 想问下hash模式和history模式在实际项目开发怎么去选择用哪个呢</div>2022-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/03/d7/33eabc6a.jpg" width="30px"><span>挙</span> 👍（2） 💬（0）<div>【2014 年之后，因为 HTML5 标准发布，浏览器多了两个 API：pushState 和 replaceState。】虽然2014年正式发布，但2008年草案发布后就很多浏览器支持了，连ie10都支持它</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/db/58/a7a0a85b.jpg" width="30px"><span>二饼</span> 👍（1） 💬（0）<div>大圣在评论区提到的：history 有利于 seo，这一点我以前使用一些博客页面生成工具上有体会，hash 不便于 seo，为了便于搜索引擎爬虫的爬取必须得做站点地图。</div>2022-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6a/95/7fb852e8.jpg" width="30px"><span>阡陌r</span> 👍（0） 💬（0）<div>1.动态路由
2.路由守卫
3.懒加载</div>2025-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/f2/30/5b677e8d.jpg" width="30px"><span>Yvan</span> 👍（0） 💬（0）<div>如果有手写history路由就更好了</div>2022-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/43/d32dd35a.jpg" width="30px"><span>子铭</span> 👍（0） 💬（0）<div>从模板到单面应用之间，是不是还少了一个多页应用，多页应用也是可以独立部署的，而且也属于jquery时代的。</div>2022-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/04/8d/005c2ff3.jpg" width="30px"><span>weineel</span> 👍（0） 💬（0）<div>function createWebHashHistory(){
    function bindEvents(fn){
        window.addEventListener(&#39;hashchange&#39;,fn)
    }
    return {
        bindEvents,
        &#47;&#47; 改成 url: () =&gt; window.location.hash.slice(1) || &#39;&#47;&#39;
        url:window.location.hash.slice(1) || &#39;&#47;&#39;
    }
}

在 Router 的构造函数里就改成函数取 url,面向接口编程。
this.history.bindEvents(()=&gt;{
    this.current.value = this.history.url()
 })

那么实现history 模式就简单了，只要实现一个 createWebHistory 函数返回用 state api 实现的 bindEvents，和 url 函数的对象就好了。</div>2021-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/08/5c/5c160dcf.jpg" width="30px"><span>不必在乎我是谁</span> 👍（0） 💬（0）<div>一楼一楼</div>2021-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/91/2b/d919ae25.jpg" width="30px"><span>Pride and Prejudice</span> 👍（0） 💬（0）<div>👍🏻</div>2021-11-10</li><br/>
</ul>