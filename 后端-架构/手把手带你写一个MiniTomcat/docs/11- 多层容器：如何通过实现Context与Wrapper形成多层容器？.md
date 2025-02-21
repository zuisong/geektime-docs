你好，我是郭屹。今天我们继续手写MiniTomcat。

上一节课结束后，我们引入了Container对Servlet进行管理，将原本的Connector功能职责进行拆分，让它专门负责通信的管理。并且在第二个部分中，把Container进一步封装成Wrapper，实现Servlet更加精确、完善的管理。

事实上，Tomcat把Wrapper也看作一种容器，也就是隶属于Context之下的子容器（Child Container），所以在原理上是存在多层容器的。一个Server对外提供HTTP服务，它的内部支持管理多个虚拟主机，而每个虚拟主机下又有多个应用，在每个应用内又包含多个Servlet。因此Container存在多个，属于层层嵌套的关系。

![图片](https://static001.geekbang.org/resource/image/4d/5c/4d787012c15e8034a5167a341c3a0a5c.png?wh=1920x1184)

按照Tomcat官方的定义，自外向内分别分为Engine层、Host层、Context层与Wrapper层。我们也参考这个思路，把ServletContainer改成Context，但是我们不打算实现Engine和Host，只用两层Container。

不考虑使用这么多层Container的主要原因在于，Engine与Host本身的结构复杂，而且其思想已经不再符合现在的主流，现在我们使用了容器技术之后，Engine和Host的概念已经弱化很多了。实际上，当我们部署的时候，一个Tomcat一般就只用一个Engine和一个Host，如果需要多个，就用多个容器。用Context和Wrapper两层容器也可以明白地说明Tomcat的多层容器的概念。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师两个问题：
Q1：Tomcat中怎么表示多个Host？用不同的IP吗？
Q2：Engine主要功能是什么？感觉所有的主要功能都已经包含在连接处理、servlet处理了，还能有什么比较大的功能由Engine来处理？</div>2024-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/6e/5435e214.jpg" width="30px"><span>HH🐷🐠</span> 👍（0） 💬（2）<div>加入本层特殊逻辑，我的想法是加入一个前置方法和后置方法， 并且子类可以重写这两个方法。</div>2024-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/fb/b6/728e2d02.jpg" width="30px"><span>偶来人间，风度翩翩</span> 👍（0） 💬（0）<div>文章一开头说的【并且在第二个部分中，把 Container 进一步封装成 Wrapper，实现 Servlet 更加精确、完善的管理。】，是不是应该是【把 Servlet 进一步封装成 Wrapper，】呀？</div>2024-05-26</li><br/>
</ul>