你好，我是郭屹。

到这一节课，我们的Spring AOP部分也就结束了，你是不是跟随我的这个步骤也实现了自己的AOP呢？欢迎你把你的实现代码分享出来，我们一起讨论，共同进步！为了让你对这一章的内容掌握得更加牢固，我们对AOP的内容做一个重点回顾。

### 重点回顾

Spring AOP是Spring框架的一个核心组件之一，是Spring面向切面编程的探索。面向对象和面向切面，两者一纵一横，编织成一个完整的程序结构。

在AOP编程中，Aspect指的是横切逻辑（cross-cutting concerns），也就是那些和基本业务逻辑无关，但是却是很多不同业务代码共同需要的功能，比如日志记录、安全检查、事务管理，等等。Aspect能够通过Join point，Advice和Pointcut来定义，在运行的时候，能够自动在Pointcut范围内的不同类型的Advice作用在不同的Join point上，实现对横切逻辑的处理。

所以，这个AOP编程可以看作是一种以Aspect为核心的编程方式，它强调的是将横切逻辑作为一个独立的属性进行处理，而不是直接嵌入到基本业务逻辑中。这样做，可以提高代码的可复用性、可维护性和可扩展性，使得代码更容易理解和设计。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/b5/a4/67d6e3cb.jpg" width="30px"><span>__@Wong</span> 👍（3） 💬（2）<div>这个课程终于学完了，讲实话收获很多。上班偷着看课程到周末写代码，前前后后花了一个多月的时间。之前也有看过spring的源码，但是看后基本忘记了。感谢本课程作者，将Spring庞大的体系进行了拆解剥离出主干，大大降低了spring学习起来的困难程度，学完对spring的体系也有了深层次的认识。一方面对spring的流程加深了理解，另一方面学习spring的优秀的架构体系设计。  git地址贴这里了，喜欢的点个小星星，建议一开始使用maven来构建项目方便很多 期待后续miniTomcat课程。
https:&#47;&#47;github.com&#47;hhhhhzj&#47;mini-spring&#47;tree&#47;master</div>2023-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6c/a3/7d60e2a0.jpg" width="30px"><span>1184507801</span> 👍（0） 💬（1）<div>老师你发的源码地址失效了啊</div>2024-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（0） 💬（1）<div>期待miniTomcat课程</div>2023-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>PatternMatchUtils是SDK提供的，怎么增加方法？派生一个类吗？</div>2023-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/11/d7e08b5b.jpg" width="30px"><span>dll</span> 👍（0） 💬（0）<div>终于花了一个礼拜摸鱼学完了，我的代码在https:&#47;&#47;github.com&#47;dll02&#47;mini_spring ，环境搭建最大的难度是idea启动tomcat那里，主要需要确认编译后的代码处在out目录里生成的文件结构是否是预期的，启动以后打开tomcat对应的manager页面，检查加载进tomcat的模块名字，最后还需要注意tomcat和使用http serverlet包的匹配，其他的网上都有资料，对照检查。
很期待老师其他的课程，手写tomcat啥的，自己学习如何从零造框架确实很有助于自己学习理解代码，精进自己的代码手艺。
谢谢老师分享教学。</div>2023-08-16</li><br/>
</ul>