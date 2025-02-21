你好，我是何辉。今天是我们深入研究Dubbo源码的第四篇，Wrapper 机制。

Wrapper，很多人从单词层面来解读，很容易理解成是Java包装类，或者是装饰器设计模式，其实都不是，它是Dubbo中的一种动态生成的代理类。

一听到代理，你可能已经想到了 JDK 和 Cglib 两个常见的代理，JDK 代理是动态生成了一个继承 Proxy 的代理类，而 Cglib 代理是动态生成了一个继承被代理类的派生代理类，既然都有现成的动态生成代理类的解决方案了，为什么 Dubbo 还需要动态生成自己的代理类呢？

带着这个问题，我们开始今天的学习。

## 不足与缺失

首先得弄明白一件事情，现有的 JDK 和 Cglib 代理为什么不能满足 Dubbo 的诉求？

### 1. JDK 代理

在“[泛化调用](https://time.geekbang.org/column/article/613308)”讲中我们讲过，泛化调用三部曲中第一个关键环节，通过接口类名、接口方法名、接口方法参数类名、业务请求参数，这四个维度的字段发起远程调用。

结合具体的应用场景来思考，有三个请求，每个请求中的四个字段值都不一样，现在要发往提供方服务：

![图片](https://static001.geekbang.org/resource/image/a1/56/a1295407baaa44dce7ce695964c8ba56.jpg?wh=4440x1836)

而提供方服务，需要在统一的入口中接收请求，然后派发到不同的接口服务中去。简单点说，提供方服务要做的就是，构建通用的接收请求入口，然后进行分发调用不同接口服务而已。**如果要针对这个统一的入口进行编码实现，你会怎么写呢？**
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1f/da/9a/ed524797.jpg" width="30px"><span>斯瓦辛武Roy</span> 👍（3） 💬（1）<div>给老师点个赞，这样的底层代码真的有助于P6的进步，希望春节期间不停更哈</div>2023-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/85/d2/045c63fb.jpg" width="30px"><span>王建新</span> 👍（0） 💬（2）<div>他到底是怎么代理生成那块if else的没看到原理呀</div>2023-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a0/cb/aab3b3e7.jpg" width="30px"><span>张三丰</span> 👍（0） 💬（2）<div>&quot;但是这么一来，如何生成动态代理类的逻辑就至关重要了，而且万一我们以后有自主定制的诉求，想修改这段生成代理类的这段逻辑，反而受 Cglib 库的牵制。&quot;

老师，这个能举个例子么？  是怎么牵制的？</div>2023-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8a/f4/fbbe4601.jpg" width="30px"><span>_Axios丶靜ﻩ</span> 👍（0） 💬（0）<div>这里的wrapper机制和ExtentionLoader里面的iswrapclass有关系吗，我觉得是没有啥关系</div>2025-01-11</li><br/>
</ul>