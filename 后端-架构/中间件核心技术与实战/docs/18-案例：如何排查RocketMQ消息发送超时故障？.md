你好，我是丁威。

不知道你在使用RocketMQ的时候有没有遇到过让人有些头疼的问题。我在用RocketMQ时遇到的最常见，也最让我头疼的问题就是**消息发送超时。**而且这种超时不是大面积的，而是偶尔会发生，占比在万分之一到万分之五之间。

## 现象与关键日志

消息发送超时的情况下，客户端的日志通常是下面这样：

![图片](https://static001.geekbang.org/resource/image/97/b3/9742c5e7e8ec8d1aebdc5f76b2a8c2b3.png?wh=1079x207)

我们这节课就从这些日志入手，看看怎样排查RocketMQ的消息发送超时故障。

首先，我们要查看RocketMQ相关的日志，在应用服务器上，RocketMQ的日志默认路径为${USER\_HOME}/logs/rocketmqlogs/ rocketmq\_client.log。

在上面这张图中，有两条非常关键的日志。

- invokeSync：wait response timeout exception.  
  它表示等待响应结果超时。
- recive response, but not matched any request.  
  这条日志非常关键，它表示，尽管客户端在获取服务端返回结果时超时了，但客户端最终还是能收到服务端的响应结果，只是此时客户端已经在等待足够时间之后放弃处理了。

## 单一长连接如何实现多请求并发发送？

为什么第二条日志超时后还能收到服务端的响应结果，又为什么匹配不到对应的请求了呢？
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ1rIbtzMltwtkdOgyk7nxzQOZtocVBwuAsZbUgY2gZHfnds4Onj6Zcxcba7fPI1qyHcb9jzJibZqA/132" width="30px"><span>Geek_9mqneh</span> 👍（3） 💬（3）<div>运维同事分别在客户端和 MQ 服务器上，在服务器上写一个脚本，每 500ms 采集一次 netstat 。从客户端的日志信息发现Recv-Q 中出现大量积压
======
这里MQ服务端采集到的netstat日志Send-Q有积压现象吗？
如果没有积压的话，因为服务器IO线程数量不足导致的问题，为啥会导致客户端的Recv-Q出现积压呢</div>2022-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/69/ed/2ea74ecd.jpg" width="30px"><span>越过山丘</span> 👍（0） 💬（1）<div>return producer.send(msg,500); &#47;&#47;设置超时时间，为 500ms，内部有重试机制

这里的500ms低于 Broker maxWaitTimeMillsInQueue=1000
会不会导致 Broker繁忙时候或者网络抖动时间，响应时间超过了500ms，导致客户端所有消息都重试多次，重试消息和之前的消息都积压在Broker的内存中，一方面对Broker造成压力，影响Broker的正常处理能力，一方面造成消息的重复率变高

目的是让客户端快速</div>2022-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/79/673f4268.jpg" width="30px"><span>小杰</span> 👍（0） 💬（0）<div>请教老师：
1、netstat里面的队列是tcp的发送和接受队列吗？
2、netty的发送缓存和tcp的发送缓存怎么个区别呢？怎么看这两个呢？
3、老师给的那个awk -F &#39;[, ,:]&#39; &#39;$12&gt;2&#39; r.log |wc -l 为啥是12列，咋看不懂呢？

</div>2022-08-04</li><br/>
</ul>