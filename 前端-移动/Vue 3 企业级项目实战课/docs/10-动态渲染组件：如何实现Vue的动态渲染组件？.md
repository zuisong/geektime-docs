你好，我是杨文坚。

前两节课，我们已经入门了Vue.js 3.x自研组件库的开发和组件库的主题方案设计，还了解了按钮组件这一基础组件的开发流程及其主题化实现。

组件库，核心是将不同类型的功能组件聚合起来，提供给业务前端开发者按需选择，用到实际前端页面上。接下来的几节课，我们主要会一步步开发不同类型的Vue.js 3.x的组件，打造属于自己的Vue.js 3.x企业级自研组件库。

今天，我们先学习组件库里常见的一种组件类型，**动态渲染组件**。

## 什么是动态渲染组件？

在平时工作中用Ant Design或者Element Plus等前端组件库时，相信你经常会用到对话框、消息提醒和侧边抽屉等组件，来做一些信息的动态显示和动态操作，这类组件都可以通过函数式的方式直接调用。

这类组件从功能上分类，一般被称为“反馈类型组件”。如果从技术实现方式上归类，就可以归纳为“动态渲染组件”。**那我们如何从技术实现的角度，理解动态渲染组件呢？**

从字面意义可以看出来，动态渲染组件就是通过“动态”的方式来“渲染”组件，不需要像常规 Vue.js 3.x组件那样，把组件注册到模板里使用。

所以，动态渲染组件的两个技术特点就是：

- 以直接函数式地使用来执行渲染，使用者不需要写代码来挂载组件；
- 组件内部实现了动态挂载和卸载节点的操作。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/cc/b7/c9ec5b8c.jpg" width="30px"><span>文艺理科生</span> 👍（1） 💬（1）<div>如果写一个成熟的弹窗组件是不太容易的，可以参考popper js，简单的一个组件，做了很多事情</div>2022-12-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rUqhSN2OVg5aHw10Hxib61nGv1SXxD6zowFl27oSm9Y6g8grRpTxCxwk7qg14a1TtmpzMTM2y810MnibBhwn75Mg/132" width="30px"><span>初烬</span> 👍（1） 💬（1）<div>老师，你好问一下，这边为什么在挂载dom的时候选择createApp。而不是是用telport</div>2022-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/0e/ce/1e02a513.jpg" width="30px"><span>刘大夫</span> 👍（0） 💬（1）<div>前辈您好，想问一下，在 vue3 中，想实现 vue2 里动态组件 component 和 v-bind=&quot;$listeners&quot;  的功能该怎么做呢，我看文档，component 被划到了选项式 api 的范畴，那用组合式 api 的方式，该怎么去实现呀</div>2023-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cf/56/eb1e7efc.jpg" width="30px"><span>Anne</span> 👍（0） 💬（1）<div>有个问题请老师解惑，多个应用实例之间数据能否共享，如何共享？比如主应用引入ant design vue组件库，副应用如何共享使用？
</div>2023-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/cf/84/88a54107.jpg" width="30px"><span>沧海一粟</span> 👍（0） 💬（1）<div>在创建应用实例的时候为啥不直接使用要作为根组件的而是要多包一层组件</div>2023-01-08</li><br/><li><img src="" width="30px"><span>珍爱学习账号</span> 👍（0） 💬（1）<div>整个过程，我们可以用最简单的 Vue.js 3.x 代码实现：
下面这段代码
h(DialogComponent, {}); } });
应该h(ModuleComponent, {}); } });
搞混了。</div>2022-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/ae/27/74828c37.jpg" width="30px"><span>ZR-rd</span> 👍（0） 💬（1）<div>请问下老师，Dialog 组件一般还可以通过声明组件的方式使用，通过 visible 属性控制显示，如何做到这两者都支持呢</div>2022-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5c/31/d7b92b6b.jpg" width="30px"><span>癡癡的等你歸</span> 👍（0） 💬（1）<div>数据通信我觉得应该是通过参数传入和方法传出，当成一个普通的组件一样使用吧。</div>2022-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/56/08/bd75f114.jpg" width="30px"><span>WGH丶</span> 👍（0） 💬（0）<div>妙啊，我之前也搞过动态渲染组件，今天一看，很多考虑不周。学到很多，给作者打call~

本期思考题：

函数很容易实现相互通信，调用时可以通过函数参数传递信息。动态组件可以暴露一些回调函数来包装好数据，让调用组件获取即可。</div>2022-12-18</li><br/>
</ul>