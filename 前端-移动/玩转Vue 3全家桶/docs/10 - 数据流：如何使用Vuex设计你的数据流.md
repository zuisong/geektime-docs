你好，我是大圣，欢迎进入课程的第10讲。

前面的基础入门篇中的几讲，都是针对Vue本身的进阶内容。通过这几讲，我们巩固和进阶了Composition API、组件化和动画等关键知识，Vue本身的知识点已经掌握得差不多了。那么从这一讲开始，我们进入课程的全家桶实战篇。

在全家桶实战篇，我们将一同学习Vue 3的生态，包括Vuex、vue-router、Vue Devtools等生态库，以及实战开发中需要用到的库。这⼀模块学完，你就能全副武装，应对复杂的项目开发也会慢慢得心应手。

今天，我先来带你认识一下Vue全家桶必备的工具：Vuex，有了这个神兵利器，复杂项目设计也会变得条理更清晰。接下来，让我们先从Vuex解决了什么问题说起。

## 前端数据管理

首先，我们需要掌握前端的数据怎么管理，现代Web应用都是由三大件构成，分别是：组件、数据和路由。关于组件化开发，在前面的[第8讲](https://time.geekbang.org/column/article/435439)中，已经有详细的讲解了。这一讲我们思考一个这样的场景，就是有一些数据组件之间需要共享的时候，应该如何实现？

解决这个问题的最常见的一种思路就是：专门定义一个全局变量，任何组件需要数据的时候都去这个全局变量中获取。一些通用的数据，比如用户登录信息，以及一个跨层级的组件通信都可以通过这个全局变量很好地实现。在下面的代码中我们使用\_store这个全局变量存储数据。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/c8/4a/3a322856.jpg" width="30px"><span>ll</span> 👍（39） 💬（2）<div>非常棒的一节，在学习内容的过程中，我也在回顾之前学习关于 Vuex 的知识，在写miniVuex 的实现的代码后，对组件化有了新的认识，简单说下体会。

 “组件化” 是解决“复杂”问题的重要思想。其实现就是一个个“组件”，即使表现方式不同，核心还是 MVX 的模型。

 这样理解，组件内的 state 就是 model，渲染出来的“图形”就是 view，而这个 X 是这 model 与 view 的“沟通方式”，它可以是 control，也可以是 view model，大概就这个意思。这里要注意，model 和 view 不应该直接沟通。

我们现在的工作就是在“搭积木”，怎么搭很重要，但是了解手中的“积木”也同样重要。

Vue2 提供的积木有 MVX(一般组件)，VX(函数式组件)，MX(vuex)；而 Vue3 通过 CompositionAPI 提供了 M，一个只有 M 的“组件”，也是Vue3灵活原因之一。

到这，我发现，其实 Vuex 也是组件，没有 View 的组件，有 Model（state），有 X（mutation，action），它的逻辑和其他组件一样，想要变更“状态”，必须通过X。就这样“管家”诞生了。

可是具体这个是怎么实现的？
大概说下几个API：install，provide，use 等，大圣讲的很清楚，回头多看几遍，最主要的是多写写。</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/42/59/67b7709b.jpg" width="30px"><span>一个小🍎</span> 👍（23） 💬（1）<div>我Vuex4都还没学完，Pinia就出来了，学不完了。
（话说想请教大圣老师，在前端技术发展如此之快的情况下，我们应该如何做取舍呢？）</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/27/d6/c318bd20.jpg" width="30px"><span>乐叶</span> 👍（16） 💬（5）<div>  constructor(options) {
    this._state = reactive({
      &#47;&#47;  data: options.state
      data: options.state()
    })
    this.mutations = options.mutations
  }

  get state() {
    return this._state.data
  }

options.state这样写使用调试发现获取到的是函数
options.state()写成这样才可以正常运行</div>2021-11-08</li><br/><li><img src="" width="30px"><span>Geek_4578dc</span> 👍（7） 💬（1）<div>建议大圣老师把每节的代码放出来，这样有利于阅读</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fd/6b/d91521bf.jpg" width="30px"><span>也許有一天</span> 👍（6） 💬（1）<div>我们公司导入rxjs来取代vuex，不得不说rxjs是真的猛...</div>2021-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9a/f5/71eee10b.jpg" width="30px"><span>深蓝</span> 👍（4） 💬（1）<div>状态管理感觉是前端代码的核心，其他所有组件，监听数据流的变化，或改变数据，然后与这个数据流相关的页面组件作出响应变化，动态菜单，导航栏，以及主页面的组件就随之改变了，整个Web服务就动起来了，最近几天vuex 看的有点晕，有个地方有点疑惑

1  vue &lt; script&gt; computed &lt;&#47;script&gt;
2 vuex  也有 getters 

两者都是计算属性，这里绕来绕去，还是理不清这里怎么使用最好？

</div>2021-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fc/e6/2cff4a89.jpg" width="30px"><span>醉月</span> 👍（4） 💬（1）<div>大圣老师Pinia会有涉及吗</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/78/7f/ef0e0ec8.jpg" width="30px"><span>uncle 邦</span> 👍（3） 💬（1）<div>count 不是使用 ref 直接定义，而是使用计算属性返回了 state.state.count，也就是刚才在 src&#47;store&#47;index.js 中定义的 count。这个 &quot; state.state.count&quot; 是不是要改成 “store.state.count”</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/7c/c6/dd01049e.jpg" width="30px"><span>Mercurywithu</span> 👍（2） 💬（1）<div>请问下大圣老师。install 方法为什么会在main.js入口处app.use(store)的时候，执行这个函数调用。是内置的api么、</div>2022-01-15</li><br/><li><img src="" width="30px"><span>xiaxiaxiaxia</span> 👍（2） 💬（1）<div>为什么在代码示例里总是省略那么多你觉得我们都会懂的代码呢。。。。对新手一点也不友好。。。</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fa/e4/0b55683f.jpg" width="30px"><span>小灰</span> 👍（2） 💬（1）<div>大圣老师   请教下vuex的模块化   </div>2021-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9a/f5/71eee10b.jpg" width="30px"><span>深蓝</span> 👍（2） 💬（1）<div>在看GitHub 其他开源项目代码，使用vuex 创建好store 引用的时候经常看到$store 一直不太理解这的$的含义？</div>2021-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/20/88/42d3b1fb.jpg" width="30px"><span>JIo</span> 👍（2） 💬（3）<div>真心觉得这种设计到多段代码的课程应该出视频课 而不是音频课 各种中英文错综穿插 代码还需要截图在旁边才能听讲 效果真的不如视频来的快。。。</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/bd/7a/37df606b.jpg" width="30px"><span>乔帆 Kayla</span> 👍（1） 💬（1）<div>STORE_KEY 的值定为 __store__ , 有什么特殊含义或特殊处理吗?</div>2021-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/1c/e2/8048fff4.jpg" width="30px"><span>KLonILo</span> 👍（1） 💬（1）<div>盛哥，最近刚好碰到一个用户信息存储的问题，我们是多页面，vuex的话刷新就没了，所以是否将用户名同时存储本地来结合使用呢？或者你有没有比较好的方案提点提点，感恩~</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/39/8c/3be6991a.jpg" width="30px"><span>韩仕杰</span> 👍（1） 💬（1）<div>老师，vue3中，尤大不推荐用vuex来做状态管理，您对这方面怎么看呢？</div>2021-11-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/8YX35AFKL60uUNM5YGloEx8uDbv0VGB5VddYvqKDgPRiauyW1ggJIs9p6B7ad3AricFMZAp8ahAqP4FmzaTP1few/132" width="30px"><span>葱味黑咖啡</span> 👍（1） 💬（1）<div> 第一次使用vuex是在vue2时，用来存储登录的用户数据，但vuex是没有持久化数据的，所以还得配合着localstorage和sessionstorage来用，比较好奇为什么vuex不提供数据持久化的实现？</div>2021-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8d/ff/986ffb41.jpg" width="30px"><span>轻飘飘过</span> 👍（1） 💬（1）<div>1. 看provide和inject那地方mini-vuex的封装有点懵，说“provide 注册了数据后，所有的子组件都可以通过 inject 获取数据”，但是mini-vuex只是封装了函数并不是组件，后来看官方文档才知道这个在调用use的时候进行注入了全局组件上了。要是大圣老师再写详细点就好了。
2. 有个疑问，使用app.use(store)进行注入vuex，为啥不封装成vueuse模块，在app.ts中用composition Api引入呢？</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/23/20/5fd6ed6f.jpg" width="30px"><span>碎竹落棋</span> 👍（1） 💬（1）<div>github源码中，this.getters[name] = computed(() =&gt; fn(this.state))，为什么需要用computed去包住呢？</div>2021-11-13</li><br/><li><img src="" width="30px"><span>Ty丶汤圆圆</span> 👍（1） 💬（4）<div>想问下大圣啊，因为vuex有刷新的问题，所以项目里通常把 vuex 和 Storage 结合在一起做数据持久化，但是用多了就会产生为什么不直接用 Storage 存取数据的疑问。封装后存取数据也一样很方便嘛，还是说仅仅是因为 vuex 有响应式功能呢。希望大圣帮忙解答下，谢谢~</div>2021-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/8e/80/2ad9e9f5.jpg" width="30px"><span>Q</span> 👍（0） 💬（1）<div>老师,为什么我在组件内import { useStore } from &#39;vuex&#39;之后在下面获取不到store的实例,并且总是给我[Vue warn]: inject() can only be used inside setup() or functional components这个警告,我在挂载store的地方实际上是可以获取到store的实例的</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/48/7c/2aaf50e5.jpg" width="30px"><span>coder</span> 👍（0） 💬（1）<div>这章的代码github上没有啊</div>2022-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/1f/24/24f15e57.jpg" width="30px"><span>朗</span> 👍（0） 💬（1）<div>class Store {
    constructor(opts) {
        this.$options = opts
        this._state = reactive({
            data: opts.state()
        })

        this._mutations = opts.mutations

    }

    get state() {
        return this._state.data
    }

    commit = (type, payload) =&gt; {
        const entry = this._mutations[type]

        return entry &amp;&amp; entry(this.state, payload)
    }

    install(app) {
        app.provide(STORE_KEY, this)
    }
}

export { useStore, createStore }

问下 return entry &amp;&amp; entry(this.state, payload)  中的this.state参数，是个方法，但这里没有调用，是怎么获取这个方法里return的this._state.data呢</div>2021-11-25</li><br/><li><img src="" width="30px"><span>一块小砖头</span> 👍（0） 💬（1）<div>The requested module &#39;&#47;src&#47;store&#47;gvuex.js?t=1637723171450&#39; does not provide an export named &#39;default&#39;     有人遇到了这个问题么？</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f7/0b/b01f1d68.jpg" width="30px"><span>百事可乐</span> 👍（0） 💬（1）<div>constructor （）{

 this.$options = options;
        this._state = reactive({
            data: options.state()     &#47;&#47; 这里文章这里最后改成  options.state  好像不对吧
        })
        this._mutations = options.mutations
}</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d6/d0/288c673c.jpg" width="30px"><span>瓦力</span> 👍（0） 💬（1）<div>感觉vuex的很大部分逻辑来自于redux，概念基本相同：store、state、action、reducer(mutation)、middleware(commit)，UI与逻辑分离，action触发state改变，并且state是immutable的。</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/e5/b6980a7a.jpg" width="30px"><span>无双</span> 👍（0） 💬（1）<div>大圣老师,请问vuex如何处理刷新丢失数据的问题，我自己的处理方式是把Storage封装到vuex中，但感觉不是很好。</div>2021-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/02/9d/566b9065.jpg" width="30px"><span>拼搏、进取</span> 👍（0） 💬（1）<div>getters:{ double(state){ return state.count*2 } }, 这个getters如何实现的呢</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/f9/39492855.jpg" width="30px"><span>阿阳</span> 👍（0） 💬（1）<div>在实现mini版的vuex时，以下代码this._state = reactive({ data: options.state })，这里是不是应该是options.state()，是一个函数调用。因为在创建store时，state已经写成了一个函数了。</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/fc/5a/3d4cb5ab.jpg" width="30px"><span>1023</span> 👍（0） 💬（7）<div>第一个示例报错，获取不到store是什么原因呢</div>2021-11-08</li><br/>
</ul>