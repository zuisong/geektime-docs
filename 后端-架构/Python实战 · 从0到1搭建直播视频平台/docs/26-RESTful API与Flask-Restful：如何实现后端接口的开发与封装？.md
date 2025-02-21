你好，我是Barry。

我们都知道，直播视频平台采用的是前后端开发模式。除去前端界面的实现，后端接口设计开发也相当重要，我们要从多个维度去考量，其中包含API规范、请求方式、响应处理、返回数据等。这整个实现的过程，我们在后端接口开发前就要做足功课。

我们都知道，直播视频平台采用前后端分离的开发模式。除去前端界面的实现，后端接口设计开发也相当重要，我们要从多个维度去考量，其中包含API规范、请求方式、响应处理、返回数据等。整个实现的过程，我们在后端接口开发前就要做足功课。

这节课，我们就借助Flask-Restful来实现高效的前后端接口开发。Flask-Restful是一个用于Flask的扩展，它让构建RESTful API变得更加容易。为了让你循序渐进地掌握Flask-Restful，我们先来了解一下RESTful API，因为Flask-Restful就是基于RESTful APl 实现的。

## 认识RESTful API

在项目开发过程中，我们的接口调用过程的核心就是前后端通信和数据的交互。

我们提到的REST，它就是一种软件架构风格，它定义了一系列标准和约束，使得应用程序能够以一种统一的方式完成通信和数据交互，实现接口统一化。而**RESTful API是一种基于REST架构的API设计规范**，它遵循REST原则，包括使用标准的HTTP方法（如GET、POST、PUT、DELETE等）、URI设计、配置合理的HTTP状态码等。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1a/0e/df/a64b3146.jpg" width="30px"><span>长林啊</span> 👍（2） 💬（1）<div>思考题：
get：用于获取资源；是幂等的，也就是对同一个URL多次调用返回的结果应该是相同的
post：用于处理提交的数据；post请求一般会产生新的资源，post请求不是幂等的
put：向指定的资源上传新的内容；PUT请求是幂等的
delete：请求服务器删除指定的资源
head：类似于GET请求，但只返回头部信息，不返回实际内容，常用于检查资源是否存在、获取资源的元数据等
options：返回服务器支持的HTTP请求方法，用于查询服务器支持哪些方法</div>2023-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/85/4e/1cecdfba.jpg" width="30px"><span>Rongfan Leo</span> 👍（0） 💬（1）<div>项目代码里是from flask_restful import，文章里是flask_RESTful算什么意思
</div>2024-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>Q1：做一个视频网站，用户一千万，这种规模的网站，后端开发老师会选什么？Java还是Python?
Q2：网站开发，后端和前端的技术栈是相互独立的，对吗？
后端选Java还是Python，都不会影响前端选vue或者React，反过来也一样。这样理解对吗？</div>2023-06-22</li><br/>
</ul>