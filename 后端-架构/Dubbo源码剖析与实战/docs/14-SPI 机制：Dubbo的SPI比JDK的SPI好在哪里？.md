你好，我是何辉。今天我们来深入研究Dubbo源码的第三篇，SPI 机制。

SPI，英文全称是Service Provider Interface，按每个单词翻译就是：服务提供接口。很多开发底层框架经验比较少的人，可能压根就没听过这个SPI 机制，我们先简单了解一下。

这里的“服务”泛指任何一个可以提供服务的功能、模块、应用或系统，这些“服务”在设计接口或规范体系时，往往会预留一些比较关键的口子或者扩展点，让调用方按照既定的规范去自由发挥实现，而这些所谓的“比较关键的口子或者扩展点”，我们就叫“服务”提供的“接口”。

比较常见的SPI机制是JDK的SPI，你可能听过，其实Dubbo中也有这样的机制，在前面章节中，我们接触过利用Dubbo的SPI机制将过滤器的类路径配置到资源目录（resources）下，那为什么有了JDK的SPI后，还需要有Dubbo的SPI呢？究竟Dubbo的SPI比JDK的SPI好在哪里呢？

带着这个问题，我们开始今天的学习。

## SPI是怎么来的

首先要明白SPI到底能用来做什么，我们还是结合具体的应用场景来思考：

![图片](https://static001.geekbang.org/resource/image/96/16/96d18b286701b156793yy91yy441de16.jpg?wh=1920x981)

app-web 后台应用引用了一款开源的 web-fw.jar 插件，这个插件的作用就是辅助后台应用的启动，并且控制 Web 应用的核心启动流程，也就是说这个插件控制着 Web 应用启动的整个生命周期。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/31/4e/78/ee4e12cc.jpg" width="30px"><span>Lum</span> 👍（1） 💬（2）<div>dubbo得spi加载还是要依赖java的spi的 在 loadLoadingStrategies策略中调用原生的ServiceLoador加载dubbo的load策略，记录一下，另外dubbo的spi还支持自适应扩展等，老师没有讲解一下</div>2023-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/f6/67/791d0f5e.jpg" width="30px"><span>小华</span> 👍（0） 💬（0）<div>老师你好，有两个问题：
1、JDK SPI的示例代码中，我运行main函数没有得到打印，调试发现while(it.hasNext())没有进去，是因为我用了JDK17吗？
2、trpc-go的插件化设计也是通过实现框架预定义的标准接口，支持开发者自己实现，利用配置文件注入，和Dubbo SPI有什么区别吗</div>2023-12-28</li><br/>
</ul>