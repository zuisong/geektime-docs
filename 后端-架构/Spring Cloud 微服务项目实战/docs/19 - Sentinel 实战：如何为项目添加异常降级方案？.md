你好，我是姚秋辰。

上节课我们学习了如何将应用接入Sentinel实现不同的流控效果，今天我们来学习Sentinel组件另一个重要功能：降级熔断。通过这节课，你可以知道如何通过Sentinel的熔断策略处理各种调用异常。除此之外，我还会讲解Sentinel熔断器开关的状态变化过程。

在[第17课](https://time.geekbang.org/column/article/479785)中我们学习过降级和熔断的作用，今天我们就先从降级开始，了解一下如何利用Sentinel的注解指定降级方法。

这里我将以Template服务的模板批量查询接口为例，向你演示如何设置降级方法。为什么我会选择这个接口？因为券模板查询是一个基础服务，很多上游的业务场景都依赖这个接口获取模板信息，所以它的访问压力相比于其它接口就大得多了，也更容易发生各种服务超时之类的异常情况。

如果你已经准备好了，我们就从编写降级逻辑开始吧。

## 编写降级逻辑

上一节课中，我们在Template服务的批量领劵接口之上添加了一个SentinelResource注解，并在其中使用blockHandler属性指定了降级方法的名称。不过呢，这个注解可不是一个万金油注解，它只能在服务抛出BlockException的情况下执行降级逻辑。

什么是BlockException呢？这个异常类是Sentinel组件自带的类，当一个请求被Sentinel规则拦截，这个异常便会被抛出。比如请求被Sentinel流控策略阻拦住，或者请求被熔断策略阻断了，这些情况下你可以使用SentinelResource的blockHandler注解来指定降级逻辑。但是对于其它RuntimeException的异常类型它就无能为力了。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（7） 💬（1）<div>Q1：Sentinel的实现原理是filter还是代理?
在服务调用过程中，sentinel是以filter方式对请求进行处理吗？不过，sentinel能中断正常的调用逻辑，所以感觉也不像是filter。那么，sentinel是通过代理实现的吗？
Q2：能增加自定义的熔断规则吗？
除了自带的三种熔断规则，是否能够增加自定义的熔断规则？如果能增加，有哪些常见的自定义规则？（同样地，对于流控，除了自带的三种流控方法，还可以自定义流控规则吗？）
Q3：服务出错最终是怎么解决的？
降级和熔断只是暂时的处理方法，最终是怎么处理的？最终是要靠人工处理吗？ 比如重启应用、重启机器等。在实际运营中，系统从错误恢复正常，是系统自我调整居多？ 还是人工干预居多？</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1e/cf/97cd8be1.jpg" width="30px"><span>so long</span> 👍（5） 💬（2）<div>老师，请教一个问题，代码中抛出自己封装的业务异常RuntimeException，不想被sentinel的熔断规则统计进去，应该如何处理?</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（1） 💬（2）<div>熔断，首先要进行依赖隔离，只要分出了那些是核心的，那些非核心的，才能做好隔离，Hystrix 记得好像是采用线程池和信号量的方式进行隔离，采用线程池需要会增加线程切换的成本。Sentinel 基于信号量进行隔离，对依赖的某个资源的进行并发数量限制。
俩者都可以采用信号量的方式，但是 Hystrix 好像对于慢调用处理不够及时。

</div>2022-01-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIWaoj5Z7tEickav1BRndKQ46TsPN3ibRYXqTuibfhpjpggrw2GNbdXTLCI5DESSftBCAjuk1490micdA/132" width="30px"><span>紫霞仙子意中人</span> 👍（0） 💬（1）<div>姚老师，请教一个问题。我配置了异常比列降级熔断，在代码中 throw new RuntimeException(&quot;异常&quot;);问题是没有达到我配置的条件，只要代码走抛出异常的那一步，就会直接降级。另外慢调用也不生效。我的限流策略是可以正常执行的。</div>2022-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/6c/d6/22360bd3.jpg" width="30px"><span>海阔天空</span> 👍（0） 💬（2）<div>照着代码写的，配置也是一样的（我习惯用properties格式）。服务启动的时候控制台日志 dataid为null.properties。断点进去看的的时候第一遍dataid是显示的有我配置的值，后面再获取的时候却是null.properties。。。然后又原模原样换成老师的配置，dataid也是显示null.yml。。这是为啥呢？</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（1）<div>日常追更，每次做第一个打卡留言的人</div>2022-01-24</li><br/>
</ul>