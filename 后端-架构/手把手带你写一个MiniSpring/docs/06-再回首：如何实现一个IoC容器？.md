你好，我是郭屹。

第一阶段的学习完成啦，你是不是自己也实现出了一个简单可用的IoC容器呢？如果已经完成了，欢迎你把你的实现代码放到评论区，我们一起交流讨论。

我们这一章学的IoC（Inversion of Control）是我们整个MiniSpring框架的基石，也是框架中最核心的一个特性，为了让你更好地掌握这节课的内容，我们对这一整章的内容做一个重点回顾。

### IoC重点回顾

IoC是面向对象编程里的一个重要原则，目的是从程序里移出原有的控制权，把控制权交给了容器。IoC容器是一个中心化的地方，负责管理对象，也就是Bean的创建、销毁、依赖注入等操作，让程序变得更加灵活、可扩展、易于维护。

在使用IoC容器时，我们需要先配置容器，包括注册需要管理的对象、配置对象之间的依赖关系以及对象的生命周期等。然后，IoC容器会根据这些配置来动态地创建对象，并把它们注入到需要它们的位置上。当我们使用IoC容器时，需要将对象的配置信息告诉IoC容器，这个过程叫做依赖注入（DI），而IoC容器就是实现依赖注入的工具。因此，理解IoC容器就是理解它是如何管理对象，如何实现DI的过程。

举个例子来说，我们有一个程序需要使用A对象，这个A对象依赖于一个B对象。我们可以把A对象和B对象的创建、配置工作都交给IoC容器来处理。这样，当程序需要使用A对象的时候，IoC容器会自动创建A对象，并将依赖的B对象注入到A对象中，最后返回给程序使用。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/2c/b8/fcaca637.jpg" width="30px"><span>郭硕</span> 👍（7） 💬（1）<div>老师多讲一些在SUN公司能了解到的关于Spring的内幕吗，比如出了什么特性，当时SUN内部的反应。目前老师讲的这些在网上基本都能搜到，没有比一般的博主深入太多。感觉不能体现出来老师的在SUN任职过的特殊经历，更想听听当时的历史背景和演化的过程。</div>2023-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/93/2d3d5868.jpg" width="30px"><span>Jay</span> 👍（3） 💬（1）<div>有两个问题需要请教一下老师：
1. 构造器注入和setter注入对比中构造器优点第三条：“适用于生命周期较短的对象，对象在实例化时会获得所需要的的依赖，对象销毁时也会自动释放”。
目前我们所实现的IoC容器还没有对象销毁功能，所有的示例都还保存在容器中，那也就不会被JVM回收吧？后续是否需要实现bean的销毁功能呢？

2. 没想明白怎么实现“构造器注解autowired注入”：autowired processor是在bean实例化之后，也就是构造函数完成之后，那这个时候还如何通过autowired注入呢?这个时候构造函数要么调用完成了，要么调用失败了呀？</div>2023-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（2） 💬（1）<div>请问：ThreadLocal方法有数据一致性问题吗？假设两个线程共享数据A，线程1在自己的ThreadLocal中有副本A1，线程2在自己的ThreadLocal中有副本A2，那么，A1、A2和A之间会存在数据一致性问题吗？ A1、A2需要更新到A吗？</div>2023-03-25</li><br/><li><img src="" width="30px"><span>Geek_a551cb</span> 👍（0） 💬（1）<div>ListableBeanFactory和ConfigurableBeanFactory都继承自BeanFactory；ConfigurableListableBeanFactory又继承ListableBeanFactory和ConfigurableBeanFactory；可不可以改成ConfigurableListableBeanFactory继承Listable、Configurable和BeanFactory;重复继承总感觉不好</div>2024-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/ff/d2/c1f5334d.jpg" width="30px"><span>dirtychill</span> 👍（1） 💬（0）<div>https:&#47;&#47;github.com&#47;DirtyBit64&#47;Mini-Spring.git  
跟着课程一节一节做的，有完整的提交记录，和课程源码不完全相同，因为遇到了一些bug，不过已经解决</div>2024-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/e6/9f/90fcfb8a.jpg" width="30px"><span>星光灼人</span> 👍（0） 💬（0）<div>老师，构造器注入时，如果有很多类，岂不是每个类都判断一下</div>2025-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6c/a3/7d60e2a0.jpg" width="30px"><span>1184507801</span> 👍（0） 💬（1）<div>老师 04 ioc 您回答的 支持多个注解的问题 ，新增RequireAnnotationBeanPostProcessor 类，那是不是还得创建相应的BeanFactory，后面的步骤是啥啊</div>2024-04-16</li><br/><li><img src="" width="30px"><span>Geek_08c860</span> 👍（0） 💬（0）<div>代码仓库：https:&#47;&#47;gitee.com&#47;funktest7ff&#47;mini-spring
划分了多个模块，每个模块是一个版本的实现</div>2023-12-20</li><br/>
</ul>