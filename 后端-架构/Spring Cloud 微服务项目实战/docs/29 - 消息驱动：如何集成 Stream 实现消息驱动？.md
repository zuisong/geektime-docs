你好，我是姚秋辰。

在上节课中，我们通过一些实际案例了解到了消息驱动技术的应用场景，这节课我们就使用Spring Cloud Stream技术来一场演练，基于RabbitMQ消息中间件来落地实践场景。

以往我们在项目中使用Stream时，大都是使用经典的@Input、@Output和@StreamListener等注解来注册消息生产者和消费者，而Stream在3.1版本之后在这几个注解上打了一个@Deprecated标记，意思是这种对接方式已经被淘汰了，不推荐继续使用。取而代之的是更为流行的Functional Programming风格，也就是我们俗称的函数式编程。

从近几年的技术发展趋势就可以看出来，函数式编程成了一种技术演进的趋势，它能让你以更少的代码和精简化的配置实现自己的业务逻辑。函数式编程和约定大于配置相结合的编程风格比较放飞自我，在接下来的实战环节中，你就会体会到这种less code style的快感了。

因为函数式消息驱动在同一个应用包含多个Event Topic的情况下有一些特殊配置，所以为了方便演示这个场景，我选择了Customer服务中的两个具有关联性的业务，分别是用户领取优惠券和删除优惠券，这节课我们就将这两个服务改造成基于消息驱动的实现方式。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="" width="30px"><span>Carla</span> 👍（6） 💬（1）<div>约定的多了，怎么感觉反而变得麻烦了😂</div>2022-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/df/52/05358975.jpg" width="30px"><span>曹亮</span> 👍（5） 💬（1）<div>老师，请教一下，在微服务项目中Stream和mq结合使用，和直接在服务里将消息发送到mq，这两种有什么区别？用stream的优势体现在哪里？</div>2022-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/c1/2dde6700.jpg" width="30px"><span>密码123456</span> 👍（3） 💬（1）<div>感觉，这配置好难。配了好几天都没有配好。</div>2022-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a8/9c/643646b9.jpg" width="30px"><span>wake</span> 👍（1） 💬（3）<div>老师如果我其它方法名也叫addCoupon会被误认为消费者吗？或者说只有返回值为Consumer才会被认定为消费者，那如果有两个同样的返回Consumer的addCoupon方法呢</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/4d/f5/2e80aca6.jpg" width="30px"><span>奔跑的蚂蚁</span> 👍（1） 💬（1）<div>我们项目用了spirng.cloud.stream.rocketMq  出了异常是自动重试，老师能讲讲原理嘛  能自定义重试间隔是次数嘛（是不是mq里面配置的）</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5b/20/ae2d4489.jpg" width="30px"><span>zkr</span> 👍（0） 💬（1）<div>为啥生产者发消息，消费者接受消息不用指定队列名和routing key？队列这个我还能理解，我试了下是按topic名+group名自动生成了一个，但是为啥topic模式不用指定routing key？</div>2022-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/4d/f5/2e80aca6.jpg" width="30px"><span>奔跑的蚂蚁</span> 👍（0） 💬（2）<div>试了下spring-cloud-starter-stream-rocketmq 的 function binding 
第一次发送消息会报日志
DefaultBinderFactory      : Retrieving cached binder: rocketmq
DirectWithAttributesChannel    : Channel &#39;unknown.channel.name&#39; has 1 subscriber(s).
BeanFactoryAwareFunctionRegistry : Looking up function &#39;streamBridge&#39; with acceptedOutputTypes: [application&#47;json]

.MessagingMethodInvokerHelper   : Overriding default instance of MessageHandlerMethodFactory with provided one.


这些都正常嘛
</div>2022-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>请教老师几个问题：
Q1：消费者标识是否可以不用方法名，另外指定一个？
Q2：“采用了 Consumer 的实现方式”，“添加消息消费者”部分的这句话中，consumer的实现方式是指什么？笔误吗？
Q3 ：“return request -&gt; ”，request从哪里来？
CouponConsumer类中，addCoupon方法中直接用了request，此request从哪里来的？
Q4：配置文件中，binders下面的my-rabbit，这个名字是任意的吗？
  如果有多个，其他的也要起一个不同的名字吗？ 比如my-rabbit2,
  my-kafka等
Q5： 交换机和队列是怎么对应的？
A 两个交换机，两个队列，每个交换机都可以将消息发送到两个队列吗？
B 队列的名字，用点号分成两部分，有什么含义吗？</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f4/c7/037235c9.jpg" width="30px"><span>kimoti</span> 👍（1） 💬（0）<div>消费消息发生异常,消息重新进入队列重新消费</div>2022-05-06</li><br/>
</ul>