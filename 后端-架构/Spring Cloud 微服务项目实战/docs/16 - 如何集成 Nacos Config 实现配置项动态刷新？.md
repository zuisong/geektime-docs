你好，我是姚秋辰。

在上一节课，你已经了解了配置中心在微服务架构中的作用和应用场景。今天我们就来学习如何让应用程序从Nacos分布式配置中心获取配置项。通过这节课的学习，你可以掌握微服务架构下的配置管理方式，知道如何通过动态配置推送来实现业务场景。

今天课程里将要介绍的动态推送是互联网公司应用非常广泛的一个玩法。我们都知道互联网行业比较卷，卷就意味着业务更新迭代特别频繁。

就拿我以前参与的新零售业务为例，运营团队三天两头就要对线上业务进行调整，为了降低需求变动带来的代码改动成本，很多时候我们会将一些业务抽离成可动态配置的模式，也就是**通过动态配置改变线上业务的表现方式**。比如手机APP上的商品资源位的布局和背景等，这些参数都可以通过线上的配置更新进行推送，不需要代码改动也不需要重启服务器。

接下来，我先来带你将应用程序接入到Nacos获取配置项，然后再来实现动态配置项刷新。本节课我选择coupon-customer-serv作为改造目标，因为customer服务的业务场景比较丰富，便于我们来演示各个不同的场景和用法。

接入Nacos配置中心的第一步，就是要添加Nacos Config和Bootstrap依赖项。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/d9/4d/4b95a228.jpg" width="30px"><span>一念之间</span> 👍（9） 💬（1）<div>老师您好,我要在在工具类中静态方法中使用nacos配置动态刷新,怎么实现</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（3） 💬（1）<div>长轮询是基于推和拉的这种方案，RocketMQ 和 Kafka 消费端消费消息也是长轮询，主动推的话，消费端可能顶不住，另外，zk 作为配置中心的 watch 机制好像是基于事件监听，主动推？现在 nacos 的普及度怎么样，是大厂都在用吗？感觉小公司，都是以前用的啥，就用啥，微服务这一套，也不引入，也不关注服务治理，出来问题，就是重启，手动刷数据</div>2022-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（3） 💬（1）<div>话说我直接用@NacosValue注解是不是相当于@Value和@RefreshScope，同时给安排了？</div>2022-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（3） 💬（1）<div>请教老师两个问题：
Q1：本篇（16篇）问题：从配置中心获取的配置项放在哪里？
       应用从nacos config获取的配置项，保存在什么地方？
       是保存到application.yml中吗？ 还是保存在内存中？
Q2：16篇之前的问题：服务层需要加原controller的注解吗？
      16篇之前的某篇有一个问题，此篇中有一句话：&quot;微服务甚至可以把controller去掉，
       服务层挂上@ResponseBody直接对外暴露service&quot;?
      去掉controller，那么，服务层除了加@ResponseBody以外，是否需要添加
      RestController、RequestMapping等注解吗？
    （为了找到出处，我用这句话中的几个关键字搜了全部文章，都没有找到，很奇怪啊。
         如果老师也想不起来这句话，那就直接评论这句话吧）</div>2022-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dc/e6/cfb409ab.jpg" width="30px"><span>intomymind</span> 👍（2） 💬（1）<div>关于长轮询机制有以下几个问题
Q1：客户端发起长轮询后，nacos收到这个请求，此时没有配置发生变化，那么此时服务端会hold这个请求，此时客户端是在等着吗？
Q2：如果nacos服务端发生了配置变化，发送了一个事件，客户端会监听这个事件，毕竟是两个服务，那这个事件是如何进行传输的，是用tcp还是http?</div>2022-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/c4/6b143e3a.jpg" width="30px"><span>carl</span> 👍（1） 💬（1）<div>老师，nacos dev环境的yml配置文件在哪里领取？</div>2022-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a1/6d/a4ff33bb.jpg" width="30px"><span>Lee</span> 👍（1） 💬（1）<div>请教老师一个问题，refreshScope注解不添加的话，在动态改变nacos的value，也会在服务日志里面打印出来的，老师说必须要加才可以Nacos Config 中的属性变动就会动态同步到当前类的变量中。如果不添加 RefreshScope 注解，即便应用程序监听到了外部属性变更，那么类变量的值也不会被刷新。</div>2022-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/33/74/d9d143fa.jpg" width="30px"><span>silentyears</span> 👍（0） 💬（1）<div>老师好，有这么一个业务场景：配置系统A将配置数据推送到服务系统集群B上的jvm缓存中，想观测统计B集群中哪些机器已收到该配置。
实现思路：B节点缓存收到配置以后，更新nacos配置，（通过本篇机制）nacos通知A，A收到通知后记录B节点机器IP。
问题有：1、会不会有并发问题，B节点几十台，A收到通知后来不及记录ip；2、通知内容该怎么包含哪些要素，怎么设计；
</div>2023-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ce/cc/ec5895b0.jpg" width="30px"><span>找工作</span> 👍（0） 💬（2）<div>姚老师，我注册中心配置的很顺利，配置中心搞了半天没搞定，com.alibaba.nacos.client.naming 报错NET WORK unreachable</div>2022-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cf/81/96f656ef.jpg" width="30px"><span>杨逸林</span> 👍（0） 💬（1）<div>还是代理，无处不在的代理。Scope 可以自定义，Spring Batch 里面也有自定义的 Scope，有对应的 Scope 接口，也有同名的 RefreshScope 这个类，会在 BeanFactory 初始化的时候新加载这个 Scope。
```
	&#47;**
	 * Creates a scope instance and gives it the default name: &quot;refresh&quot;.
	 *&#47;
	public RefreshScope() {
		super.setName(&quot;refresh&quot;);
	}
```

看这个代码就知道是怎么回事了。如果看到 ManagedOperation 这种注解，不用管，这只是 JMX 的内容，用不到的就不用了解。

Apollo 没有加这个 Scope 一样能用，之前小马哥对比过这两个，Apollo 不太符合 Spring Cloud 的规范。更好的，我觉得 Spring Cloud Config 还行，之前的作业就是让我们自定义个其中的配置的 Repository，以某一个文件变动为配置变动。Spring Cloud Config 的抽象写的还行。</div>2022-01-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eq6pWvKsV4rzQ62z5MDEjaEU5MbDfmzbA62kUgoqia2tgKIIxw4ibkDhF7W48iat5dT8UB9Adky2NuzQ/132" width="30px"><span>小仙</span> 👍（20） 💬（0）<div>在不使用 @RefreshScope 的情况下，通过 Spring Environment 对象也能获取到 Nacos 最新的环境变量</div>2022-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（5） 💬（2）<div>RefreshScope 动态刷新背后的实现原理？
当配置中心配置变更后，客户端长轮询拉取到最新配置变更，spring 上下文，能监听到配置的变更，更新上下文的配置为最新的，然后重新 get bean，bean 的初始化流程中，把新的配置，注入到 bean 中，进而实现 bean 中的那些属性配置都是最新的，是这个流程不。</div>2022-05-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/4VCgcBbU51SiasW8tpjYwdqBGe2RNIy6neuI7AEjCQ6t9qqXw6tXpZ2bDCoxJhWqQJv2LlFmemVYJCrLze2Aa7g/132" width="30px"><span>beatdrug</span> 👍（2） 💬（0）<div>被RefreshScope注释的类会生成代理类，依赖注入只是引入代理类，当容器监听到RefreshEvent事件，会清除容器缓存中被代理的目标对象，所以之后方法调用会触发代理类去容器重新生成并获取目标对象，这个时候就会用新配置初始化对象了；由于基于代理的方式实现的，如果目标对象没有接口或者用final修饰的话，RefreshScope也会失效</div>2022-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/5d/c5dc789a.jpg" width="30px"><span>珠穆写码</span> 👍（2） 💬（0）<div>通过发布application的RefreshEvent事件来刷新RefreshScope的Bean, 调用ContextRefresh.refresh的方法去重新创建bean</div>2022-01-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/uUNsibxx9EvpiaeG5VVd6slEia0QGFsIdOPwxxz7NmulA1dpSDktTmcV9pa6DPiaj1aj8T9eafVfDSYq8TiaKVxw8sg/132" width="30px"><span>Geek_09b0c3</span> 👍（0） 💬（0）<div>之前在线上出现了nacos动态更新配置 应用假死的现象 最明显的特点在于日志不再打印。但是过后本地压测没有复现，这个是为什么呢</div>2025-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/21/3b/7f01e158.jpg" width="30px"><span>陈志男</span> 👍（0） 💬（0）<div>读取其他配置文件 如果失效的话可以试试下面这种
```
ext‐config[0]:
  data‐id: hello.yml
  group: EXT_GROUP
  refresh: true
```</div>2022-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f1/1a/b1de30c8.jpg" width="30px"><span>Geek_ea3747</span> 👍（0） 💬（0）<div>ConfigurationProperties</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/50/2b/2344cdaa.jpg" width="30px"><span>第一装甲集群司令克莱斯特</span> 👍（0） 💬（0）<div>Apollo 、Nacos 还是企业用的比较多的分布式应用配置中心。</div>2022-01-17</li><br/>
</ul>