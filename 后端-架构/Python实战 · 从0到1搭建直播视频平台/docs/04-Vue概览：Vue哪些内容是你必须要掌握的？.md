你好，我是Barry。

相信想要学习前端的你一定听说过Vue框架。

Vue和React都是Web前端工程师必学必会的框架，在企业中有着广泛的应用。这节课我们就来揭开Vue的神秘面纱，一起来看看Vue里必须掌握的知识点，以及怎样学习Vue才更加高效。

## 初识Vue

![](https://static001.geekbang.org/resource/image/40/8e/40c2c374d4630be6f1e2c7178374f48e.jpg?wh=2890x584)

Vue是一款用于构建用户界面的 JavaScript 框架。它基于标准 HTML、CSS 和 JavaScript 构建，并提供了一套声明式的、组件化的编程模型。无论是简单还是复杂的界面，Vue 都可以胜任，可以说是我们高效开发用户界面的一大利器。

Vue有三个核心特性。

- 声明式渲染：Vue 基于标准 HTML 拓展了一套模板语法，方便我们以声明式描述最终输出的 HTML 和 JavaScript 状态之间的关系。
- 响应性：Vue 会自动跟踪 JavaScript 状态，并在它发生变化时响应式地更新 DOM。
- 双向数据绑定：JS数据的变化会被自动渲染到页面上，Vue还可以自动获取页面上发生变化的表单数据，并更新到JS数据中。

了解Vue的核心特性还远远不够，要真正认识Vue，我们还需要了解Vue的项目框架。

## 目录结构

我们这就来看看Vue的目录包含哪些内容，它们的用途又是什么。

下面是Vue-cli脚手架项目目录，也是我们课程开发中用的标准框架。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/09/98/397c2c81.jpg" width="30px"><span>贾维斯Echo</span> 👍（5） 💬（1）<div>MVVM 是一种软件架构模式，它是 Model-View-ViewModel 的缩写。该模式是由微软推出的，旨在帮助开发者更好地管理前端应用程序中的复杂性。

具体来说，MVVM 将一个前端应用程序分成三个部分：

Model：数据模型层，它代表应用程序中的数据和业务逻辑。
View：视图层，它是用户界面的呈现层，用于展示数据。
ViewModel：视图模型层，它是连接 Model 和 View 的桥梁。ViewModel 将 Model 中的数据转换成 View 中可以显示的格式，并将 View 中的用户操作转换成 Model 中的操作。ViewModel 通常包含一个命令对象（Command），用于触发具体的业务逻辑。
在 Vue 中，Vue 实例就充当了 ViewModel 的角色，模板（template）就是 View 层，而组件中的数据就是 Model 层。Vue 通过数据绑定机制将 ViewModel 和 View 层连接起来，当 ViewModel 中的数据发生变化时，View 层会自动更新，反之亦然，这样就大大简化了前端应用程序的开发过程。</div>2023-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/3a/cdf9c55f.jpg" width="30px"><span>未来已来</span> 👍（3） 💬（1）<div>记录下遇到的问题及解决

vue 版本 2.9.6

1. cnpm 这个是阿里的，需要单独安装，跟 npm 是互补作用
2. vue init webpack my_project 失败，直接拉取最新的 webpack 包到本地，然后把 webpack 替换成 本地路径
3. 安装 chromedriver 失败，直接下载跟本地 chrome 匹配的版本，然后配置到环境变量 path 中
4. npm run dev 启动失败：安照提示安装即可(npm 安装失败可用 cnpm 替代)</div>2023-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（1） 💬（1）<div>老师你好，index.html是一定要的吗？里面有个div id = &#39;app&#39;, 跟 app.vue里面的 div Id = &#39;app&#39;有什么区别，我们new Vue实例#app绑定的是哪个？</div>2023-06-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/1TH46TfPC1KISGHcyD9ggUUOJKjoc3E953RqYiaicsIghQxxUaAvcEhyibSZryhMXUdIt2BqoPacWkiarPia4PX1U7A/132" width="30px"><span>Geek_come</span> 👍（0） 💬（1）<div>老师，您这里应该用编译器带大家走一遍，只是建议</div>2023-11-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/XxMiatkEbd8CrMgKk3NHzEhA2rQvNq2TgnOey35DOWLPpRh39MugzzE4M324pEsmg2JbGiazhVBt9rNZZvapgnicg/132" width="30px"><span>Geek_in7j5o</span> 👍（0） 💬（3）<div>老师，我的node.js和npm版本和你的一样，然后我安装了vue-cli2.5.1，在初始化项目时出现了版本不兼容的情况，于是我把vue-cli2.5.1更新到了2.9.6版本，初始化项目成功，但是之后的初始化中又出现安装 chromedriver 失败，于是我又用了npm cache clean --force  
 npm install chromedriver@2.46.0这两命令，成功了，我想知道我明明是想安装您教的来的，后面不知道为什么偏了，那我的又正不正确呢？
</div>2023-11-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/XxMiatkEbd8CrMgKk3NHzEhA2rQvNq2TgnOey35DOWLPpRh39MugzzE4M324pEsmg2JbGiazhVBt9rNZZvapgnicg/132" width="30px"><span>Geek_in7j5o</span> 👍（0） 💬（1）<div>老师，咱们node.js有版本要求吗，我是在阿里云云服务器上使用宝塔面板来安装node.js的
</div>2023-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/01/3726cf7c.jpg" width="30px"><span>明仔的阳光午后</span> 👍（0） 💬（1）<div>计算属性部分
```
&lt;script&gt;
export default {
    data() {
        return {
            count: 1
        }
    },
    computed: {
        &#47;&#47; 每当 count 改变时，这个函数就会执行
        doubleCount() {
            return count * 2
        }
    }
}
&lt;&#47;script&gt;
```
这里doubleCount直接使用了count而不是this.count，是其他地方有定义吗？我按照代码敲会出现ReferenceError: count is not defined</div>2023-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/f5/72/8cbc5cb3.jpg" width="30px"><span>好困啊</span> 👍（0） 💬（1）<div>要不是chatgpt，这门课程我估计我又是从入门到放弃。搭建环境真的太难了</div>2023-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/f6/91/ff699674.jpg" width="30px"><span>神经蛙</span> 👍（0） 💬（1）<div>这一段有点跟不上，是不是有点过快了。</div>2023-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/4d/161f3779.jpg" width="30px"><span>ls</span> 👍（0） 💬（1）<div>cnpm install --global vue-cli  
---&gt; 是不是多了一个c 
npm install --global vue-cli</div>2023-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（1）<div>老师，你好，请教一下，什么场景应该用compute计算属性和watch属性，这两者应用场景有什么区别呢</div>2023-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（2）<div>npm intsall的时候报错
core-js@2.6.12: core-js@&lt;3.23.3 is no longer maintained and not recommended for usage due to the number of issues. Because of the V8 engine whims, feature detection in old core-js versions could cause a slowdown up to 100x even if nothing is polyfilled. Some versions have web compatibility issues. Please, upgrade your dependencies to the actual version of core-js.</div>2023-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/9d/91d795cf.jpg" width="30px"><span>ZENG</span> 👍（0） 💬（1）<div>MVVM中关键的VM，也就是ViewModel ，连接 Model 和 View ，通过数据绑定等技术，将 Model 和 View “绑定”在一起，实现数据的双向绑定，即在数据发生改变时，View 自动更新，而用户在 View 上的操作也会自动同步到 Model 上。</div>2023-06-03</li><br/><li><img src="" width="30px"><span>Geek_88cc02</span> 👍（0） 💬（4）<div>上面的安装命令是win环境的吗，mac的运行不了，用 npm install -g @vue&#47;cli 才行</div>2023-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：本专栏前端开发IDE是用vue-cli吗？我本机(win10)上装了VSCode，可以吗？（vue-cli和VSCode都是开发框架，vue-cli是命令行方式，VSCode是GUI方式；VSCode包含了vue-cli，vue-cli是VSCode的一个子集，两者关系是这样吗？）
Q2：vue的具体存在形式是什么？是一个库吗？还是一个可执行程序？项目工程的目录中，哪个目录是vue本身的内容？（以前听说过jQuery，就是一个库，在页面中导入jQuery的库即可）
Q3：页面中导入jQuery库以后，jQuery就可以解析、处理页面中jQuery相关的内容。那么，页面中与vue相关的内容，是vue的库处理的吗？还是node.js处理的？
Q4：node.js是支持vue-cli还是vue？node.js、vue-cli、vue，这三者是什么关系？（我的理解：vue-cli需要node.js，vue-cli只是便于vue工程的管理；node.js与vue没有直接关系）</div>2023-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/8f/88/3814fea5.jpg" width="30px"><span>安静点</span> 👍（0） 💬（1）<div>对于俺来说，还是有点复杂。动手找抄两遍先</div>2023-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/04/3c/9f97f7bd.jpg" width="30px"><span>一米</span> 👍（0） 💬（3）<div>思考题：
MVVM是Model-View-ViewModel的缩写，是MVC模式的一种变体。在MVVM中，模型表示应用程序的数据和业务逻辑，视图表示用户界面，而视图模型则充当模型和视图之间的中介。
视图（View）和视图模型（ViewModel）之间的数据绑定是双向的。当视图中的数据发生变化时，视图模型中的数据也会相应地更新。
问题：
老师你好，请问我们项目使用的vue版本是多少啊。我看课程主页说是使用vue2.7，但是这一小节安装的vue-cli是2.5版本的。我想尽量把自己的开发环境配置成和课程中一样的。</div>2023-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/71/48/44df7f4e.jpg" width="30px"><span>凯</span> 👍（0） 💬（0）<div>nodejs 的版本如果是最新的直接安装官网的方法安装，</div>2023-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/3a/cdf9c55f.jpg" width="30px"><span>未来已来</span> 👍（0） 💬（0）<div>记录下遇到的错误：
vue 版本 2.9.6
</div>2023-06-26</li><br/>
</ul>