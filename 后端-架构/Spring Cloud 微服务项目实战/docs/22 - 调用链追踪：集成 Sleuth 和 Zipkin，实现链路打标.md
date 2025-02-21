你好，我是姚秋辰。

在上节课中，我们讲了链路追踪技术在线上故障排查中的重要作用，以及Sleuth是如何通过“打标记”来实现链路追踪的。

今天，我们就通过实战来落地一套完整的调用链追踪方案。在实战阶段，我会为你详细讲解Sleuth在调用链中传递标记信息的原理。为了进一步提高线上故障排查效率，我们还会搭建Zipkin组件作为链路追踪的数据可视化工具，并通过一条高可用的数据传输通道，借助RabbitMQ将日志信息从应用服务器传递到Zipkin服务器。当你学完这节课，你就可以掌握“调用链追踪”方案搭建的全过程了。

链路打标是整个调用链追踪方案的基础功能，所以我们就先从这里开始，在实战项目中集成Sleuth，实现日志打标动作。

## 集成Sleuth实现链路打标

我们的微服务模块在运行过程中会输出各种各样的日志信息，为了能在日志中打印出特殊的标记，我们需要将Sleuth的打标功能集成到各个微服务模块中。

Sleuth提供了一种无感知的集成方案，只需要添加一个依赖项，再做一些本地启动参数配置就可以开启打标功能了，整个过程不需要做任何的代码改动。

所以第一步，我们需要将Sleuth的依赖项添加到模板服务、优惠计算服务和用户服务的pom.xml文件中。具体代码如下。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/26/14/85/73e55be5.jpg" width="30px"><span>~</span> 👍（21） 💬（2）<div>https:&#47;&#47;github.com&#47;openzipkin&#47;zipkin&#47;blob&#47;master&#47;zipkin-storage&#47;mysql-v1&#47;src&#47;main&#47;resources&#47;mysql.sql 
这是官方仓库中给的 MySQL 改造的脚本，创建一个 zipkin 的 db 库；之后可以从 https:&#47;&#47;github.com&#47;openzipkin&#47;zipkin&#47;blob&#47;16857b6cc3&#47;zipkin-server&#47;src&#47;main&#47;resources&#47;zipkin-server-shared.yml 配置文件中看到 mysql 的配置项，然后对照着之前老师给的命令，添加上 MySQL 的即可。
我的命令：
java -jar zipkin-server-2.23.9-exec.jar --STORAGE_TYPE=mysql --MYSQL_HOST=127.0.0.1 --MYSQL_TCP_PORT=3306 --MYSQL_USER=root --MYSQL_PASS=123456 --MYSQL_DB=zipkin --RABBIT_ADDRESSES=127.0.0.1:5672</div>2022-02-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er6ADlY3IFt3Rs1aVDyrTO2ytQZDiciaXVKgxCnsqZJUQHzH6I0I6PYvdoiaI6rkm7OLOxHia7t1icDyBQ/132" width="30px"><span>yinwenping</span> 👍（8） 💬（1）<div>这种traceid只是在两个服务直接适用吗？比如服务A调用服务B，而服务B内部时线程池处理的，线程池还能用A的traceid吗？</div>2022-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0f/d7/31d07471.jpg" width="30px"><span>牛年榴莲</span> 👍（2） 💬（1）<div>Zipkin 好像不支持告警，有没有能根据链路追踪情况进行告警的组件呢？</div>2022-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（2） 💬（1）<div>下面四个问题是在第21篇提的，不过在21篇留言中没有发现，很奇怪。重新提一次。
老师新年快乐，请教四个问题：
Q1: 实际的线上系统，用户请求是直接到gateway吗？还是需要在gateway的前面加一个节点？如果需要，一般用什么？Nginx吗？
Q2：Sleuth是怎么产生TraceID、Span ID、Parent Span ID的？
Q3：时间同步问题：Sleuth通过时间来排序，如果不同服务所在机器的时间不是同步的，会有什么问题？怎么解决？
Q4：Sleuth是怎么实现“打标”的？怎么获取到微服务之间的调用信息的？又是怎么影响到日志组件(e.g,logback)的？通过拦截器实现的吗？</div>2022-02-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/m7fLWyJrnwEPoIefiaxusQRh6D1Nq7PCXA8RiaxkmzdNEmFARr5q8L4qouKNaziceXia92an8hzYa5MLic6N6cNMEoQ/132" width="30px"><span>alex_lai</span> 👍（1） 💬（1）<div>rabbitmq的配置没有提 需要单独启动 配置queue
么？</div>2022-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>Q1：&quot;# 每秒采样数字最高为100      rate: 1000&quot;
        注释为100，实际是1000，是笔误吗？
Q2：“如果我们把 probability 设置成小于 1 的数，就说明有的请求不会被采样”
       哪些会被采样？哪些不会被采样？
Q3：“在 OpenFeign 的环节动了一个手脚。Sleuth 通过 TracingFeignClient 类，将一系列 Tag 标记塞进了OpenFeign 构造的服务请求的 Header 结构中”
   A 如果一个组件，sleuth没有适配，能扩展吗？
   B Sleuth对OpenFeign的处理，是通过拦截器实现的吗？</div>2022-02-02</li><br/><li><img src="" width="30px"><span>吴少伟</span> 👍（0） 💬（1）<div>追加一个问题：任务调度开始执行的时候，可以生成traceId等信息啊？ps：自己留言跑哪里去了。。。。咋找不到</div>2022-06-05</li><br/><li><img src="" width="30px"><span>吴少伟</span> 👍（0） 💬（1）<div>老师咨询几个小问题：
1、必须要设置日志级别为debug吗?设置为info是否可以，已经集成了其他的日志收集器了，现在目的只想加上traceId和spanId信息。修改log的配置文件增加这个数据的参数，可以直接打印出来吗？
2、对性能是否有影响？</div>2022-06-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eou1BMETumU21ZI4yiaLenOMSibzkAgkw944npIpsJRicmdicxlVQcgibyoQ00rdGk9Htp1j0dM5CP2Fibw/132" width="30px"><span>寥若晨星</span> 👍（0） 💬（1）<div>我怎么记得要生成链路图，还要再下载一个jar包定时执行一下任务</div>2022-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/4d/f5/2e80aca6.jpg" width="30px"><span>奔跑的蚂蚁</span> 👍（0） 💬（1）<div>请问老师  sleuth依赖 上下游服务器都要加嘛</div>2022-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/34/cf/0a316b48.jpg" width="30px"><span>蝴蝶</span> 👍（0） 💬（1）<div>这个链路表报功能好sao啊，好强大</div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/4d/f5/2e80aca6.jpg" width="30px"><span>奔跑的蚂蚁</span> 👍（0） 💬（1）<div>如果用的rocket mq 咋办，web 直连 zipkin 会产生什么大问题吗</div>2022-03-10</li><br/><li><img src="" width="30px"><span>Geek_7346b9</span> 👍（0） 💬（1）<div>请教下，我启动rabbitmq server 且成功启动后，当我尝试执行启动zipkin（按您给的参数一样），没有一次是成功的。每一次都是timeout问题，我查看了rabbitmq的日志，发现报了client unexpected close socket.而且时间很固定是5秒。请问是哪里问题？即便我配置了rabbitmq.collector.connection-timeout超过10秒，依旧报错</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fb/6c/12fdc372.jpg" width="30px"><span>被水淹没</span> 👍（0） 💬（0）<div>作者还有在关注这个课程吗，有个问题，在springboot3中，sleuth已经过时，转而升级为Micrometer Tracing了，但是我发现Micrometer Tracing的设计理念涉及整套观测性的逻辑，有点复杂，找不到对应的中转MQ的相关配置，请教下老师如何配置呀，还是说Micrometer Tracing并没有支撑，得自己写桥接？</div>2024-09-08</li><br/>
</ul>