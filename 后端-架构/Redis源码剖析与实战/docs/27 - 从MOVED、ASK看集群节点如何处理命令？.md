你好，我是蒋德钧。

在上节课一开始我给你介绍了，我们在Redis Cluster这个模块中会学习三部分内容：节点间如何传递信息和运行状态、节点如何处理命令，以及数据如何在节点间迁移。那么通过上节课的学习，现在我们已经了解了Gossip协议的基本实现，也就是支持集群节点间信息和运行状态传递的数据结构、关键函数设计与实现。

所以在今天这节课，我们就来了解下集群命令处理的实现。这部分内容不仅包括了集群节点处理一个命令的基本流程，更重要的是，我们可以掌握集群特定命令MOVED、ASK是如何实现的。这两个命令对应了Redis Cluster中请求重定向的处理场景，了解了这部分内容之后，我们就可以参考Redis Cluster，来设计和实现分布式系统中的请求重定向。

接下来，我们先来看下集群节点处理一个命令的基本流程，这可以让我们对集群节点的实现有个整体观。

## 集群节点处理命令的基本流程

我在[第14讲](https://time.geekbang.org/column/article/411558)中提到过，Redis server处理一条命令的过程可以分成四个阶段，分别是**命令读取、命令解析、命令执行和结果返回**。而和单个Redis server一样，Redis Cluster中的节点，也是按照相同的阶段来处理命令的。

因此，集群节点在各阶段处理命令的入口函数和单个Redis server也是一样的，如下图所示。你也可以再去回顾下第14讲中，我介绍的命令处理详细流程。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（10） 💬（0）<div>1、cluster 模式的 Redis，在执行命令阶段，需要判断 key 是否属于本实例，不属于会给客户端返回请求重定向的信息

2、判断 key 是否属于本实例，会先计算 key 所属的 slot，再根据 slot 定位属于哪个实例

3、找不到 key 所属的实例，或者操作的多个 key 不在同一个 slot，则会给客户端返回错误；key 正在做数据迁出，并且访问的这个 key 不在本实例中，会给客户端返回 ASK，让客户端去目标节点再次查询一次（临时重定向）；key 所属的 slot 不是本实例，而是其它节点，会给客户端返回 MOVED，告知客户端 key 不在本实例，以后都去目标节点查询（永久重定向）

课后题：processCommand 函数在调用完 getNodeByQuery 函数后，实际调用 clusterRedirectClient 函数进行请求重定向前，会根据当前命令是否是 EXEC，分别调用 discardTransaction 和 flagTransaction 两个函数。这 2 个函数的目的是什么?

看代码逻辑，只有当 n == NULL || n != server.cluster-&gt;myself 时，才会调用这 2 个方法。

其中，如果当前执行的是 EXEC 命令，则调用 discardTransaction。这个函数表示放弃整个事务，它会清空这个 client 之前缓存的命令队列，放弃事务中 watch 的 key，重置 client 的事务标记。

如果当前命令不是 EXEC，而是一个普通命令，则调用 flagTransaction。这个函数会给当前 client 打上一个标记 CLIENT_DIRTY_EXEC，如果后面执行了 EXEC，就会判断这个标记，随即也会放弃执行事务，给客户端返回错误。

也就是说，当集群不可用、key 找不到对应的 slot、key 不在本实例中、操作的 keys 不在同一个 slot、key 正在迁移中，发生这几种情况时，都会放弃整个事务的执行。</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（3） 💬（0）<div>回答老师的问题：
按照我个人理解，不知道是否准确。 我们先了解一下Redis事务的实现方式，命令在multiState中是以队列的形式保存着的，只有当执行EXEC的时候，才会按照队列顺序依次执行里面的命令，否则会调用queueMultiCommand将命令保存到这个队列中，而事务在Redis中是以client的维度开启的，如果一个client开启了事务，那么它结构体中的flags会被设置为CLIENT_MULTI（在事务中），那么问题中的两个函数的作用是什么？

        1、【discardTransaction】：直接丢弃当前的事务，清空multiState队列里面的命令，并且会对事务中的key unWatch。
        2、【flagTransaction】：将client的flages设置为CLIENT_DIRTY_EXEC（事务最终将在EXEC的时候也会失败）。

两个方法刚好对应了client在事务中，执行EXEC命令和普通命令的两种情况。Redis是发现当getNodeByQuery返回的clusterNode节点不是自己的时候才会执行这两个方法，并且当Redis以集群模式运行的时候，跨节点是不支持事务，如果发现当前client有事务开启的情况，可能是之前开启的，那么当getNodeByQuery发现不是自己的时候需要把之前的事务废弃。如果命令直接就是EXEC了那么直接调用discardTransaction丢弃事务，如果是事务中的某个命令出现这种情况(例如：开启事务后发生迁移)，则调用flagTransaction，等到EXEC的时候一样丢弃。

补充：
    集群中涉及MULTI&#47;EXEC的操作需要让key都在同一节点上面，如果不在会返回 MOVED 信息或者直接返回error信息。</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6c/b5/32374f93.jpg" width="30px"><span>可怜大灰狼</span> 👍（0） 💬（0）<div>只要能够进入n == NULL || n != server.cluster-&gt;myself，都表示需要重定向客户端了。如果当前是execCommand，discardTransaction就释放整个multi阶段缓存下来的命令。否则就打一个脏标识CLIENT_DIRTY_EXEC</div>2021-10-12</li><br/>
</ul>