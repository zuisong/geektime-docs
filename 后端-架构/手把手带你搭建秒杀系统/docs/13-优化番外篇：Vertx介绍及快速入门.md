你好，我是志东，欢迎和我一起从零打造秒杀系统。

经过前面课程的学习，我们知道Nginx和Tomcat都可以做网关服务，并且从理论出发做了分析比对，也从实践上做了相应服务的开发，那么今天我们将学习一款优秀的、可开发网关服务的技术，即Vertx。该技术的总体性能要优于Tomcat，但弱于Nginx。其在国内的普及度相对国外来说还是比较低的，但已经有些公司开始尝试使用了，比如京东的PC商详页服务、秒杀Web服务都是用它来开发的，并且线上实际效果也很不错。

接下来我们将对Vertx做个简单的介绍，并实际搭建一个Vertx项目，来替换demo-web的角色，重新构造秒杀Web系统的一环。

## **Vertx简介**

我们先了解一下Vertx可以用来干什么，这样我们才能在已知的技术栈中找出一个和其相对应的技术来帮助理解。

首先它可以开发Web服务，这点Nginx、Tomcat也能做。

其次它也有点像Spring，它提供了完整的生态，包括Vertx Web、Vertx Core、Vertx Unit等模块，但它和Spring也不是互斥关系，我们待会搭建的项目中就会使用Vertx+Spring，它们可以配合使用。

然后它还提供了很多其他的能力，比如EventBus的消息机制，实现服务间通信，同时它还可以支持多种语言的开发。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/af/af/8b03ce2c.jpg" width="30px"><span>GengTeng</span> 👍（1） 💬（1）<div>Vert.X 3.X 深度使用者。写异步回调太痛苦，如果不想写回调地狱，就要用 Future 组合链，写起来仍然痛苦，每个IO的地方都会把上下文割裂开。Java 没有 async&#47;await ，玩异步IO就是痛苦啊。Go那个简陋的语法又看不上，连个泛型都没有，最后去写Rust了，async&#47;await&#47;tokio&#47;actix 真的香啊。</div>2021-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（1） 💬（0）<div>多年以前用过Vert.x 2，开发上的体验接近Node.js（毕竟原本就叫Node.x）。缺点是招不到人，招进来的Java开发都只会写Spring，对着Vert.x代码只会干瞪眼。</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e6/09/1eca92c9.jpg" width="30px"><span>止水</span> 👍（0） 💬（0）<div>spring的react,这个模型和vertx类似吗，也是异步非阻塞的框架。能简单对比下吗？</div>2023-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/82/3c21b30c.jpg" width="30px"><span>梅子黄时雨</span> 👍（0） 💬（0）<div>学习了。</div>2022-11-25</li><br/>
</ul>