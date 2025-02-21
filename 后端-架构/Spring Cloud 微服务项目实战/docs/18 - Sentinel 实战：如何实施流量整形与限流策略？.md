你好，我是姚秋辰。

今天我们来学习Sentinel组件最为核心的功能：流量整形（也可以叫流控）。

在这节课，我会通过项目实战将优惠券系统集成到Sentinel中，对用户领券和查找优惠券两个场景添加流控规则。在这个过程中，我会带你了解Sentinel的三种流控模式，以及对应的流控效果。此外，我还会针对Sentinel框架做一个小扩展，对特定的调用来源做流控。掌握了这些内容之后，你就可以清楚如何用流控手段来降低高并发场景下的系统压力。

在进行实战项目之前，我需要带你搭建Sentinel控制台。你可以把它看作一个中心化的控制中心，所有的应用程序都会接入这个控制台，我们可以在这里设置各种流控规则，这些规则也会在应用程序中实时生效。

## 运行Sentinel控制台

我们可以从[Sentinel官方GitHub](https://github.com/alibaba/Sentinel/releases)的Release页面下载可供本地执行的jar文件，为了避免版本不一致导致的兼容性问题，我推荐你下载1.8.2.Release版本。在该版本下的Assets部分，你可以直接下载sentinel-dashboard-1.8.2.jar这个文件。

![图片](https://static001.geekbang.org/resource/image/e6/41/e6d555a468cb66cb0c753c84457ee641.png?wh=911x229)

下载好文件之后，你可以使用命令行进入到这个jar包所在的目录，然后就可以直接执行下面这行命令启动Sentinel控制台了。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/ff/9355810e.jpg" width="30px"><span>海布里王力宏</span> 👍（5） 💬（1）<div>“第二种流控效果 Warm Up 则实现了“预热模式的流控效果”，这种方式可以平缓拉高系统水位，避免突发流量对当前处于低水位的系统的可用性造成破坏。举个例子，如果我们设置的系统阈值是 QPS=10，预热时间 =5，那么 Sentinel 会在这 5 秒的预热时间内，将限流阈值从 3 缓慢拉高到 10。为什么起始阈值是 3 呢？因为 Sentinel 内部有一个冷加载因子，它的值是 3，在预热模式下，起始阈值的计算公式是单机阈值 &#47; 冷加载因子，也就是 10&#47;3=3。我截了一张图，你可以参考一下，看看 Warm Up 配置项是如何填写的。”

新年快乐，对预热还是不理解，如果设置了预热，是不是意味着QPS达到阈值的时候，会降为1&#47;3的QPS，然后再拉升。还是这个预热只是针对系统的启动阶段？

</div>2022-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a8/9c/643646b9.jpg" width="30px"><span>wake</span> 👍（2） 💬（2）<div>配置应该是：

spring:
  cloud:
    sentinel:
      transport:
        # sentinel api端口，默认8719
        port: 8719
        # dashboard地址
        dashboard: localhost:8080</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2e/74/88c613e0.jpg" width="30px"><span>扶幽</span> 👍（1） 💬（1）<div>老师请教下，在warm-up的模式下，阈值在不断的攀升过程中，其它超过当前时间节点的请求是通过快速失败的方式被拒绝了吗？还是进入队列了呢？</div>2023-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/d2/40/2abbda81.jpg" width="30px"><span>Dean</span> 👍（1） 💬（1）<div>老师好，想咨询一下熔断限流的阈值如何确定具体的值，是拍脑袋想的吗？还是有一定的策略去定义</div>2023-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d9/31/22fc55ea.jpg" width="30px"><span>Believe</span> 👍（0） 💬（1）<div>关联流控规则不得行，也不报错，在直接流控规则生效的前提下，直接修改为关联流控，添加关联资源都不行</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/79/27/7ac85e6f.jpg" width="30px"><span>王志成</span> 👍（0） 💬（1）<div>我在coupon-calculation-serv 项目中集成Sentinel 的时候，报了Could not bind properties to &#39;SentinelProperties&#39; 。
说是 让我Add an implementation, such as Hibernate Validator, to the classpah

为什么 Sentinel 会需要添加 Hibernate 呢，客户端在使用 Sentinel还需要持久化数据吗？</div>2022-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7a/5f/c05cd5dc.jpg" width="30px"><span>Ronnie</span> 👍（0） 💬（1）<div>热点规则配置怎么存储呢，比如用户id=1的限流20，用户id=2的限流30，这些配置不可能一个一个去控制台配置吧</div>2022-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/71/552e4afb.jpg" width="30px"><span>next station</span> 👍（0） 💬（1）<div>姚老师，请教个问题：流控规则--链路流控，无效；也百度了一下，配置spring.cloud.sentinel.web-context-unify=false无效。麻烦老师指导一下

代码如下：

```
    &#47;&#47; 读取优惠券
    @GetMapping(&quot;&#47;getTemplate&quot;)
&#47;&#47;    @SentinelResource(value = &quot;getTemplate&quot;)
    public CouponTemplateInfo getTemplate(@RequestParam(&quot;id&quot;) Long id){
        log.info(&quot;Load template, id={}&quot;, id);
        return couponTemplateService.loadTemplateInfo(id);
    }

    @GetMapping(&quot;&#47;getTemplate1&quot;)
&#47;&#47;    @SentinelResource(value = &quot;getTemplate1&quot;)
    public CouponTemplateInfo getTemplate1(@RequestParam(&quot;id&quot;) Long id){
        log.info(&quot;Load template, id={}&quot;, id);
        return couponTemplateService.loadTemplateInfo(id);
    }


资源
public interface CouponTemplateService {
    &#47;&#47; 通过模板ID查询优惠券模板
    @SentinelResource(value = &quot;loadTemplateInfo&quot;)
    CouponTemplateInfo loadTemplateInfo(Long id);
}

```</div>2022-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/71/f0/07c72ca6.jpg" width="30px"><span>勤奋的樂</span> 👍（0） 💬（1）<div>请问添加流控规则，sentinel控制台直接弹窗显示失败，报错日志如下，是什么原因呢？
2022-05-06 15:37:21.357 ERROR 61049 --- [nio-8081-exec-1] c.a.c.s.d.controller.FlowControllerV1    : Failed to add new flow rule, app=coupon-template-serv, ip=localhost

com.alibaba.csp.sentinel.dashboard.client.CommandFailedException: 

2022-05-06 15:37:22.724 ERROR 61049 --- [Worker-thread-6] c.a.c.s.dashboard.metric.MetricFetcher   : fetch metric http:&#47;&#47;localhost:8081:8719&#47;metric?startTime=1651822634000&amp;endTime=1651822640000&amp;refetch=false error

org.apache.http.client.ClientProtocolException: URI does not specify a valid host name: http:&#47;&#47;localhost:8081:8719&#47;metric?startTime=1651822634000&amp;endTime=1651822640000&amp;refetch=false
	at org.apache.http.impl.nio.client.CloseableHttpAsyncClient.determineTarget(CloseableHttpAsyncClient.java:121) [httpasyncclient-4.1.3.jar!&#47;:4.1.3]
	at org.apache.http.impl.nio.client.CloseableHttpAsyncClient.execute(CloseableHttpAsyncClient.java:102) [httpasyncclient-4.1.3.jar!&#47;:4.1.3]
	at org.apache.http.impl.nio.client.CloseableHttpAsyncClient.execute(CloseableHttpAsyncClient.java:92) [httpasyncclient-4.1.3.jar!&#47;:4.1.3]
	at com.alibaba.csp.sentinel.dashboard.metric.MetricFetcher.fetchOnce(MetricFetcher.java:214) [classes!&#47;:na]
	at com.alibaba.csp.sentinel.dashboard.metric.MetricFetcher.lambda$doFetchAppMetric$3(MetricFetcher.java:282) [classes!&#47;:na]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[na:1.8.0_312]
	at java.util.concurrent.FutureTask.run(FutureTask.java:266) ~[na:1.8.0_312]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[na:1.8.0_312]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[na:1.8.0_312]
	at java.lang.Thread.run(Thread.java:748) ~[na:1.8.0_312]

</div>2022-05-06</li><br/><li><img src="" width="30px"><span>Geek_e93c48</span> 👍（0） 💬（1）<div>姚老师请教个问题，Sentinel限流的排队模式下，会将所有QOS都排队吗？还是只是创建一个固定大小的队列存储固定的QPS，超过部分直接抛弃。</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/34/cf/0a316b48.jpg" width="30px"><span>蝴蝶</span> 👍（0） 💬（2）<div>现在天天加班，没法学实践，我先看完</div>2022-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/d9/4d/4b95a228.jpg" width="30px"><span>一念之间</span> 👍（0） 💬（3）<div>老师,生产环境中使用时您建议是用注解方式,还是统一封装基于sentinel的starter</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/96/fb/af39abb1.jpg" width="30px"><span>黄叶</span> 👍（0） 💬（1）<div>老师，配置的地址应该是spring.cloud下吧，文章是在application下</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（33） 💬（1）<div>限流算法：滑动窗口，令牌桶，漏桶
Sentinel 的流量控制有三种：
快速失败：应该采用滑动窗口算法，当滑动时间窗口内的QPS超过一定的阀值，Sentinel 直接抛出异常
排队等待：采用漏桶算法，所有请求数据包进入漏桶进入排队等待，漏桶以一定的速率放行，达到匀速的效果的
Warm Up：采用令牌桶算法，动态的调整令牌桶的容量大小，达到预热的效果
</div>2022-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/71/f0/07c72ca6.jpg" width="30px"><span>勤奋的樂</span> 👍（1） 💬（1）<div>记一个坑，我本地启动sentinel后，控制台接口绑定在8081端口，template模块接口注解@SentinelResource(value=&quot;getTemplate&quot;)后，调用接口，sentinel控制台不显示服务，需要配置clientIp后sentinel才能正确显示刚刚配置的服务：
sentinel:
      transport:
        # sentinel api端口，默认8719
        port: 8719
        # dashboard地址
        dashboard: localhost:8081
        clientIp: localhost:8081</div>2022-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f4/c7/037235c9.jpg" width="30px"><span>kimoti</span> 👍（0） 💬（0）<div>底层应该是令牌桶算法</div>2022-01-21</li><br/>
</ul>