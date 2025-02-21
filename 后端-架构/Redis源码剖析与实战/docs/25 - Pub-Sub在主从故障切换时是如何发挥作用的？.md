你好，我是蒋德钧。

在前面两节课，我们学习了哨兵工作的基本过程：哨兵会使用sentinelRedisInstance结构体来记录主节点的信息，在这个结构体中又记录了监听同一主节点的其他哨兵的信息。**那么，一个哨兵是如何获得其他哨兵的信息的呢？**

这其实就和哨兵在运行过程中，使用的**发布订阅（Pub/Sub）**通信方法有关了。Pub/Sub通信方法可以让哨兵订阅一个或多个频道，当频道中有消息时，哨兵可以收到相应消息；同时，哨兵也可以向频道中发布自己生成的消息，以便订阅该频道的其他客户端能收到消息。

今天这节课，我就带你来了解发布订阅通信方法的实现，以及它在哨兵工作过程中的应用。同时，你还可以了解哨兵之间是如何发现彼此的，以及客户端是如何知道故障切换完成的。Pub/Sub通信方法在分布式系统中可以用作多对多的信息交互，在学完这节课之后，当你要实现分布式节点间通信时，就可以把它应用起来。

好了，接下来，我们先来看下发布订阅通信方法的实现。

## 发布订阅通信方法的实现

发布订阅通信方法的基本模型是包含**发布者、频道和订阅者**，发布者把消息发布到频道上，而订阅者会订阅频道，一旦频道上有消息，频道就会把消息发送给订阅者。一个频道可以有多个订阅者，而对于一个订阅者来说，它也可以订阅多个频道，从而获得多个发布者发布的消息。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（7） 💬（0）<div>回答老师的问题：这条命令是不是就是由 pubsub.c 文件中的 publishCommand 函数来处理的呢?

答：并不是publishCommand来执行的

在《哨兵也和Redis一样实例化吗？》这篇文章老师有提到，哨兵模式启动的时候，会把 server.commands 对应的命令表清空，然后在其中添加哨兵对应的命令。所以最后执行的应该是哨兵的 publish 命令，对应的执行函数应该是 sentinelPublishCommand，发送的应该也只是hello频道。

总结：
本篇文章，老师重点介绍了Pub&#47;Sub在主从切换中的作用，以及Pub&#47;Sub是如何初始化的，在redis中，实现发布的函数是 pubsubPublishMessage，而订阅的主要函数是 pubsubSubscribeChannel。
	
在哨兵模式下是通过 sentinelEvent 的方式进行发布的，其调用流程是 sentinelEvent -&gt; pubsubPublishMessage，而哨兵实例的 publish 命令被替换，是通过 sentinelProcessHelloMessage -&gt; sentinelProcessHelloMessage 向其它实例发送 hello 频道的消息，用于同步哨兵实例的基本信息，比如 IP、端口号、quorum 阈值等。</div>2021-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（6） 💬（1）<div>1、哨兵是通过 master 的 PubSub 发现其它哨兵的：每个哨兵向 master 的 PubSub（__sentinel__:hello 频道）发布消息，同时也会订阅这个频道，这样每个哨兵就能拿到其它哨兵的 IP、端口等信息

2、每个哨兵有了其它哨兵的信息后，在判定 Redis 实例状态时，就可以互相通信、交换信息，共同判定实例是否真的故障

3、哨兵判定 Redis 实例故障、发起切换时，都会向 master 的 PubSub 的频道发布消息

4、客户端可以订阅 master 的 PubSub，感知到哨兵工作到了哪个状态节点，从而作出自己的反应

5、PubSub 的实现，其实就是 Redis 在内存中维护了一个「发布-订阅」映射表，订阅者执行 SUBSCRIBE 命令，Redis 会把订阅者加入到指定频道的「链表」下。发布者执行 PUBLISH，Redis 就找到这个映射表中这个频道的所有「订阅者」，把消息「实时转发」给这些订阅者

课后题：在哨兵实例上执行 publish 命令，这条命令是不是就是由 pubsub.c 文件中的 publishCommand 函数来处理的?

以哨兵模式启动的 Redis 实例，会使用新「命令表」。

在 server.c 的 main 函数中可以看到，哨兵模式启动后，会调用 initSentinel 函数。

void initSentinel(void) {
    ...

    &#47;&#47; 只添加 sentinelcmds 下的命令
    for (j = 0; j &lt; sizeof(sentinelcmds)&#47;sizeof(sentinelcmds[0]); j++) {
        int retval;
        struct redisCommand *cmd = sentinelcmds+j;

        retval = dictAdd(server.commands, sdsnew(cmd-&gt;name), cmd);
        serverAssert(retval == DICT_OK);
    }
    ...
}

可以看到只把 sentinelcmds 命令表添加到了 server.commands 中。sentinelcmds 如下：

struct redisCommand sentinelcmds[] = {
    ...
    {&quot;subscribe&quot;,subscribeCommand,-2,&quot;&quot;,0,NULL,0,0,0,0,0},
    {&quot;publish&quot;,sentinelPublishCommand,3,&quot;&quot;,0,NULL,0,0,0,0,0},
    {&quot;info&quot;,sentinelInfoCommand,-1,&quot;&quot;,0,NULL,0,0,0,0,0},
    ...
};

可以看到哨兵的 PUBLISH 命令是由 sentinelPublishCommand 单独实现的，并非普通实例的 publishCommand。</div>2021-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9e/39/139f3ee9.jpg" width="30px"><span>fkc_zyk</span> 👍（1） 💬（0）<div>    addReplyBulk(c,channel);            addReplyBulk(c,message);这两个方法读取的全局数据是什么，分别有什么作用，感觉这两个都是读取订阅列表的客户端实现消息的发送</div>2023-05-19</li><br/>
</ul>