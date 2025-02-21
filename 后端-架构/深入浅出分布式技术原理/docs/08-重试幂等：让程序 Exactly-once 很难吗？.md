你好，我是陈现麟。

通过学习“分布式锁”的内容，你已经了解了如何实现一个分布式锁服务，并且知道了在分布式锁的场景下，我们应该如何在正确性、高可用和高性能之间做取舍。那么对于分布式场景下，实例或服务之间的协调问题，我们就心中有数了，你可以根据业务场景，做出最合适的选择，我们又一起往前走了一大步。

但是，在极客时间的开发过程中，你又面临了一个新的问题。在通过 RPC 远程调用极客时间的课程购买接口的过程中，你可能是这样处理 RPC 的响应结果的，先是将“请求超时”的响应结果解释为“课程购买失败”，返回给用户，可是这会影响到用户的正常购买，导致一部分用户放弃。

后来，为了尽可能让用户购买成功，你对“请求超时”响应的请求进行了重试，发现用户的购买成功率确实提高了，但是却有少量的用户反馈说，他只点击了1 次购买，页面却出现了 2 笔支付成功的订单。

这确实是一个两难的问题，要么让一部分用户放弃购买，要么让少量的用户重复购买，难道没有一个好的办法吗？这里我们可以先来分析一下这个问题的根本原因，**在请求的响应结果为“请求超时”的时候，我们不知道这个请求是否已经被远端的服务执行了，进一步来说就是请求的消息，是否精确一次发送到远端服务的问题，即 Exactly-once**。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="" width="30px"><span>松鼠鱼</span> 👍（10） 💬（1）<div>思考题：在 IM 系统中，我们如何实现幂等的消息发送接口？
以Kafka为例，生产者发送消息的时候会带上 ProducerId 和 SequenceNumber，相同批次（batch）的消息 SequenceNumber 是一样的，重复发送时不会被 broker 接受。
同时，开启幂等会默认 acks = -1，也就是一批消息被成功写入需要分区的所有同步副本都接收到才算数，以此确保不丢消息。在这个基础上加上幂等，二者共同保证精确一次。
以上虽然只能确保单次会话、单分区的幂等，但一般情况下，业务上我们会确保某一种类的消息固定发往某一分区（比如根据某个 key 值做哈希取余），而且在消费者端也可以做去重检查，因此问题不大。
如果需要全局的、跨越会话的幂等（精确一次），还是要开事务。</div>2022-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/9d/104bb8ea.jpg" width="30px"><span>Geek2014</span> 👍（3） 💬（1）<div>老师你好，想咨询一下 内部的2pc机制怎么实现额，感觉有点语焉不详额

然后我们在当前请求的内部通过 2PC 的机制，确保该请求的内部状态修改逻辑</div>2022-03-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoxPxEURiaoe5Px5iaTN2lYuGkyljx5AoAa61Qg1nPAKBX57ldwRCqpWSYklIoNkqT0eluB66Yibgx7Q/132" width="30px"><span>处女座♍️</span> 👍（3） 💬（1）<div>现在手里的项目正好是基于netty实现的IM即时消息项目，消息头中存了消息id（基于会话层面的递增id），客户端进入会话后会在分布式缓存中建立会话快照（session），session中会存放接收到的最大id，当服务端接收到消息后会比较当前id和session中的id，如果小于等于视为重复消息丢弃。当然这是个客服系统，可以容忍出现细微误差</div>2022-03-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eppk5Wd7oa28diccJkOicp34R7mcxYEEZxWq7yIOGXAvwcAJF5GOTGVOrN0I3eYfMoMkZLfNIeT2O4A/132" width="30px"><span>Geek_192757</span> 👍（3） 💬（2）<div>请问老师，外部系统2PC方式具体要怎么做？</div>2022-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/14/5a/38d9471c.jpg" width="30px"><span>lz404</span> 👍（1） 💬（1）<div>如果使用另外的存储比方说redis记录幂等，是不是二者之间就很难一致，可能出现没重试或者多重试</div>2022-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（1） 💬（3）<div>前端每次请求会在Header中带一个时间戳。有些接口要求幂等（可以理解为防止重复提交）。每次请求，都会把时间戳作为一个唯一标识来验证接口是不是重复提交。这样的方案可行吗？</div>2022-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e7/261711a5.jpg" width="30px"><span>blentle</span> 👍（0） 💬（1）<div>老师能否提供类似的案例补充说明一下</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>请教老师四个问题：
Q1：怎么标记请求已经处理完成？
Q2：“写处理结果”和“写入数据库”，是两个不同的操作吗？
Q3：全局唯一ID一般怎么产生？
Q4：关于重试幂等，能否举一两个具体的例子？互联网实践的例子。</div>2022-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（1） 💬（0）<div>如果能有一些常见中间件的应用案例列举会更好</div>2022-06-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/icHMBoxO5zDicEgIOkFsZCsbicMAeaW3zd7e6YjJJKfvwu7Q8E3wtpXojfdClOeCGrPicJ16FBpEMicfpuDiariajibDSg/132" width="30px"><span>Jack_1024</span> 👍（1） 💬（0）<div>有没有GitHub具体事例代码呀？大佬</div>2022-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（0） 💬（0）<div>反过来，客户端拉，并自己维护偏移量。如此一来直接没有推送超时成功的场景。</div>2022-02-25</li><br/>
</ul>