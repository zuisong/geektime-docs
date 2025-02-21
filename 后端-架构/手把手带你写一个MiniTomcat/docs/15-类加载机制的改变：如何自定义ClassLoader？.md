你好，我是郭屹。今天我们继续手写MiniTomcat。

上节课我们引入了多应用的支持，实现了通过路由将请求发送到不同应用中，在这个过程中我们也定义了WebappClassLoader这个自定义的类加载器来进行隔离。

但是光有隔离还不够，因为不同的类加载器有不同的加载方式和顺序，而Java自身的系统级ClassLoader也不能完全满足我们的需要，所以这节课我们要继续扩展这个话题，深入讨论自定义的ClassLoader。

## 类加载器原理

我们平时写程序的时候似乎感觉不到类加载器，其实是因为Java在帮我们默认使用，我们的程序中每涉及到一个类的使用，运行时Java都会通过一个类加载器来加载它。Java里面对它的定义是：类加载器是一个对象，它负责加载别的类（Class Loader is an object that is responsible for loading classes）。

我们简单回顾一下一个Java对象是如何在JVM里面运行起来的。一个简单的语句 `new Test();` 大体会经过下面几个步骤。

步骤一：**类级别的工作。**具体某个类的加载过程只会做一次。

1. 加载：找到class文件，打开并获取它的字节流，按照虚拟机规范存储在JVM里，同时创建一个和它匹配的java.lang.Class类对象。这个时候，类的定义和内存表达就准备好了，但是还没有开始对象的创建。
2. 链接：这个阶段执行类的链接过程，给类分配内存。具体它有三个动作要做。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_50a5cc</span> 👍（2） 💬（1）<div>双亲委托 是 将类的加载放到上一层处理，如果加载到，就不需要重复加载；所以遇到一个User类，不管是版本1，2，都会加载，不会再去处理其他的User类</div>2024-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师几个问题：
Q1：CommonLoader与CommonClassLoader是什么关系？
CommonClassLoader并没有继承CommonLoader。
Q2：Tomcat只有Common加载器吗？
MiniTomcat用Common加载器来加载服务器通用的类，用WebappClassLoader来加载应用的类。但是，文章中讲到的Tomcat的类加载图中，只有Common，并没有WebappClassLoader。
Q3：System是扩展类加载器吗？
文中几个关于类加载的图中，都有“System”这个措辞，它是指扩展类加载器吗？
Q4：类的版本怎么体现？
一个类有多个版本，怎么体现？通过类名字来体现？
Q5：类被加载以后是放在方法区吗？
比如，类Person，被加载以后会创建一个针对Person的对象，假设名字是A。那么，加载以后得类Person和A是被放在内存中的方法区吗？</div>2024-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/6e/5435e214.jpg" width="30px"><span>HH🐷🐠</span> 👍（0） 💬（1）<div>JVM 里一个类的唯一标识是 ClassLoader + 类名,  按照双亲委派模式都是由相同的 ClassLoader 去加载， 无疑会冲突。 老师， 还有一个问题， CommonClassLoader 是不是要指定一下 delegate，默认为 false</div>2024-01-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIDhIpvB4hJnsn4utiatsHtTwriaSiaWXfMc0FyicBKB7Aibh0x5uxQ5TxMIl2ZhZp0G6jHUib9SPf3T76Q/132" width="30px"><span>InfoQ_1f089af08bc8</span> 👍（0） 💬（1）<div>老师能否讲解一下类加载器的findClass(String name)和loadClass(String name)之间有什么关联吗？</div>2024-01-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIDhIpvB4hJnsn4utiatsHtTwriaSiaWXfMc0FyicBKB7Aibh0x5uxQ5TxMIl2ZhZp0G6jHUib9SPf3T76Q/132" width="30px"><span>InfoQ_1f089af08bc8</span> 👍（0） 💬（1）<div>请问老师，URLStreamHandler 这个类的作用是干什么的？</div>2024-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/09/bb/5ffa3534.jpg" width="30px"><span>onefine</span> 👍（0） 💬（0）<div>我认为使用双亲委派模式能实现这个需求啊，上一小节的app1和app2中的servlet 不就是这种情况吗？使用了不同的WebappClassLoader 完成了应用下的 servlet 的加载，这个 WebappClassLoader 也是遵从双亲委派模式的啊...

是我的理解不对吗？期望老师指正！</div>2025-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/fb/b6/728e2d02.jpg" width="30px"><span>偶来人间，风度翩翩</span> 👍（0） 💬（0）<div>请问老师，在Docker、SpringBoot集成Tomat 的背景下，一个JVM进程只会有一个应用服务，所以是不是用双亲加载模式 也不存在隔离的问题了。</div>2025-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2c/68/c299bc71.jpg" width="30px"><span>天敌</span> 👍（0） 💬（0）<div>CommonClassLoader 是否需要将 lib 目录下的所有jar文件读取到，转换成URL传入构造函数才能成功读取？</div>2024-05-24</li><br/>
</ul>