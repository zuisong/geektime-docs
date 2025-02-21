你好，我是丁威。

在课程正式开始之前，我想先分享一段我的经历。我记得2020年双十一的时候，公司订单中心有一个业务出现了很大程度的延迟。我们的系统为了根据订单状态的变更进行对应的业务处理，使用了RocketMQ的顺序消费。但是经过排查，我们发现每一个队列都积压了上千万条消息。

当时为了解决这个问题，我们首先决定快速扩容消费者。因为当时主题的总队列为64个，所以我们一口气将消费者扩容到了64台。但上千万条消息毕竟还是太多了。还有其他办法能够加快消息的消费速度吗？比较尴尬的是，没有，我们当时能做的只有等待。

作为公司消息中间件的负责人，在故障发生时没有其他其他补救手段确实比较无奈。事后，我对顺序消费模型进行了反思与改善。接下来，我想和你介绍我是如何优化RocketMQ的顺序消费性能的。

## RocketMQ顺序消费实现原理

我们先来了解一下 RocketMQ 顺序消费的实现原理。RocketMQ支持局部顺序消息消费，可以保证同一个消费队列上的消息顺序消费。例如，消息发送者向主题为ORDER\_TOPIC的4个队列共发送12条消息， RocketMQ 可以保证1、4、8这三条按顺序消费，但无法保证消息4和消息2的先后顺序。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/02/78/23c56bce.jpg" width="30px"><span>james</span> 👍（2） 💬（5）<div>其实顺序消费速率的瓶颈在业务，也就是消费者的处理逻辑，并不在MQ, 感觉这个方案走偏了，根据阿姆达尔定律，你应该做的是改变最能提升性能的地方，而不是在一个本来就很快的地方</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/31/4318a7fa.jpg" width="30px"><span>Louise</span> 👍（1） 💬（1）<div>你好，丁威老师能不能课后题目都有个答案，像mysql45讲专栏一样呢？因为自己这方面接触少，有些问题还真想不出来，看评论也看的不是很懂</div>2022-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/69/ed/2ea74ecd.jpg" width="30px"><span>越过山丘</span> 👍（1） 💬（1）<div>丁威老师，请教一下，如果一批消息中有一条消息出了问题，导致阻塞了一个消费线程很长时间，按照最小位点提交的策略，这个是不是会导致位点一直不推进了</div>2022-09-11</li><br/><li><img src="" width="30px"><span>Geek_9a02e8</span> 👍（0） 💬（2）<div>1、上报最小位点？那不是下次拉取的时候还从这个偏移量开始拉取，不是一直重复拉同一批数据了吗？
2、开始的顺序消费模型怎么保证队列顺序的？虽然取数据到提交的过程都加锁了，可是实际消费是放到消费线程池了呀，这种异步没法保证顺序的吧？
3 好多地方提到队列，我都分不清是客户端的什么队列还是服务端的什么队列了…</div>2023-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2b/bb/5cf70df8.jpg" width="30px"><span>嘉嘉☕</span> 👍（0） 💬（1）<div>老师好，请问下，rocketmq实现的顺序消费 不算是关联顺序性吗？</div>2023-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/fa/e2990931.jpg" width="30px"><span>文敦复</span> 👍（0） 💬（1）<div>提个思路，请教下：1优化消费者代码，如果不行，那么2提升消费者数量，如果已经达到队列长度，那么3重建一个长度队列更大的主题，改原消费者代码为按照业务逻辑重新分发消息到新的主题，老的消费者代码放到新的消费者这里。不知道如何评价？😅</div>2022-12-15</li><br/><li><img src="" width="30px"><span>Geek_9d39c4</span> 👍（0） 💬（2）<div>老师请教一下顺序消费 假设现在有两个队列 order1的状态变迁发送到q1 order2的发送到q2 order3的发送到q1 此时order3是不是要等order1全部都消费完才能消费order3</div>2022-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/56/2f/4518f8e1.jpg" width="30px"><span>放不下荣华富贵</span> 👍（0） 💬（1）<div>所以作者的方案是：在顺序消费队列的消费者内引入线程池，再次拆分可并行的任务进行执行？

然后激进的先更新位点后分发任务，宁可丢消息，也不会大批量重复消费造成位点回溯？</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8a/5a/b67a82e3.jpg" width="30px"><span>shen</span> 👍（0） 💬（0）<div>有两个问题咨询下老师
1，开头增加机器到64台，是单机处理不过来了吗？如果处理不过来后面改造增加线程处理也应该处理不过来吧
2，为什么不增加队列数量？集群队列是64，那么增加到128，256，是不是也可以达到相同的目的</div>2023-10-07</li><br/><li><img src="" width="30px"><span>Geek_460f3a</span> 👍（0） 💬（0）<div>老师您好，为啥每次拉去完消息都要先暂停，再恢复，是为了啥
while (isRunning) {
                    List&lt;MessageExt&gt; records = consumer.poll(consumerPollTimeoutMs);
                    submitRecords(records);
                    consumerLimitController.pause();
                    consumerLimitController.resume();
                }</div>2023-03-10</li><br/><li><img src="" width="30px"><span>Geek_460f3a</span> 👍（0） 💬（0）<div>代码有bug，DefaultMQLitePushConsumer的isRunning永远是false，永远不会拉数据</div>2023-03-07</li><br/>
</ul>