上一节我们讲了基于XML的SOAP协议，SOAP的S是啥意思来着？是Simple，但是好像一点儿都不简单啊！

你会发现，对于SOAP来讲，无论XML中调用的是什么函数，多是通过HTTP的POST方法发送的。但是咱们原来学HTTP的时候，我们知道HTTP除了POST，还有PUT、DELETE、GET等方法，这些也可以代表一个个动作，而且基本满足增、删、查、改的需求，比如增是POST，删是DELETE，查是GET，改是PUT。

## 传输协议问题

对于SOAP来讲，比如我创建一个订单，用POST，在XML里面写明动作是CreateOrder；删除一个订单，还是用POST，在XML里面写明了动作是DeleteOrder。其实创建订单完全可以使用POST动作，然后在XML里面放一个订单的信息就可以了，而删除用DELETE动作，然后在XML里面放一个订单的ID就可以了。

于是上面的那个SOAP就变成下面这个简单的模样。

```
POST /purchaseOrder ...
```
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/6f/63/abb7bfe3.jpg" width="30px"><span>扬～</span> 👍（16） 💬（3）<div>文本传输最终都会转化为二进制流啊，为什么文本要比二进制rpc占用带宽？</div>2018-11-10</li><br/><li><img src="" width="30px"><span>起风了001</span> 👍（6） 💬（3）<div>文本传输最终都会转化为二进制流啊，为什么文本要比二进制rpc占用带宽？

1
2018-11-10
作者回复: 数字2如果用int传输用几个bit，如果是字符串呢？

这个有点疑问, 用int传输需要32或者64位; 字符串的话, 看编码, 如果是utf8编码的话, 还是1个字节8bit即可表示.....</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ed/f1/e31585a8.jpg" width="30px"><span>jonhey</span> 👍（5） 💬（1）<div>看到这里，强烈建议老刘基于此教程，丰富一下内容，写本书，估计能成为网络、云计算、网络编程、微服务领域集大成的经典教材</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/85/7c/03a268fe.jpg" width="30px"><span>leohuachao</span> 👍（4） 💬（1）<div>我觉得RESTFul架构流行，也得益于前端框架的丰富吧，要不然维护客户端会话也够难实现</div>2018-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/1f/a58f27de.jpg" width="30px"><span>罗瑞一</span> 👍（3） 💬（1）<div>问个问题，购买这个动作，是告诉服务端减一，难受没有办法做到只告诉服务端结果吧</div>2019-04-04</li><br/><li><img src="" width="30px"><span>Geek_f6f02b</span> 👍（2） 💬（2）<div>RESTful 模型如何实现幂等，这个表示没有想通，就是好比之前SOAP，你告诉我减库存，我就执行减，减后还剩多少，是否成功返回，但是如果是客户端直接减去库存，然后告诉我说，将库存设置成这么多，服务端只要告诉我是否成功，并发了怎么解决，多个人同时请求，如果库存为10，5个请求都是减1，如果前面失败，但是后面成功，前面分别说将库存设置成9、8、7、6，都失败了，最后一个说设置成5成功了，感觉会有问题。</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/24/df/645f8087.jpg" width="30px"><span>Yayu</span> 👍（1） 💬（1）<div>JSON-RESTful 算是一种协议吗？把它理解成一种规范会更好吧？</div>2018-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（0） 💬（1）<div>底子好，学起什么来都快</div>2019-05-25</li><br/><li><img src="" width="30px"><span>起风了001</span> 👍（0） 💬（1）<div>我们平时设计的api, 比如购买东西, 是传的数量, 而不是传库存剩余多少呀. 传数量应该是主流才是, 所以传数量不是RESTful模式吗?</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/de/17/75e2b624.jpg" width="30px"><span>feifei</span> 👍（55） 💬（0）<div>在讨论 RESTful 模型的时候，举了一个库存的例子，但是这种方法有很大问题，那你知道为什么要这样设计吗？

此方法的问题在于，不是解决问题，而是将数据状态进行了转移，将状态交给存储，这样业务将可以无状态化运行，这种设计可以很好的解决扩展的问题，因为无状态，可以进行负载均衡！使用集群化来解决单机的问题。

基于文本的 RPC 虽然解决了二进制的问题，但是它本身也有问题，你能举出一些例子吗？

1，效率问题，程序与文本之间转换效率低，因而不适合内部大数据交换，因为文本利用阅读，对外采用较好

2，相比于二进制rpc,传输需要的带宽更大，二进制的rpc因为可以使用专用的客户短和服务器代码，可以更好的压缩数据，以提供更大的吞吐量</div>2018-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/b5/0737c1f2.jpg" width="30px"><span>kuzan</span> 👍（14） 💬（1）<div>crud的语义离业务有点远，客户端往往不想关心crud，客户端关注的语义是业务，比如审批、下单，添加好友。感觉用http这几个method做语义就把服务变成了dao，一个贫血服务</div>2018-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（12） 💬（0）<div>题目1:
库存的问题是：存在并发，导致库存可能为负值。
用Restful来进行无状态的访问，库存量即状态由业务层来解决。
题目2:
用文本来进行RPC的请求和响应，占用的字节数大。
</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/86/e3/28d1330a.jpg" width="30px"><span>fsj</span> 👍（10） 💬（2）<div>没有restful api之前的json api 是什么样子的？感觉对于客户端同学，不了解之前是什么样子，很难体会到restful api的有点。</div>2018-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5e/2b/df3983e2.jpg" width="30px"><span>朱显杰</span> 👍（8） 💬（0）<div>能不能谈谈dubbo和springcloud在服务发现方面的优缺点？</div>2018-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c2/e0/7188aa0a.jpg" width="30px"><span>blackpiglet</span> 👍（6） 💬（0）<div>第一题，我的理解是，资源最终还是有状态的，所以 rest 方式，是把状态转移到了数据库和客户端。那么数据库的抗压能力和稳定性就非常重要了，这也是为什么最近有这么多内存数据库和键值数据库的原因。另外客户端有状态也会造成很多麻烦，毕竟这是不受开发人员控制的，如果逻辑没有切割清楚，升级会非常痛苦。
第二题，能想到的主要是性能的损耗，毕竟传输的内容更多了，单位带宽下能传输的信息总量会有明显下降。</div>2018-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/8e/0a546871.jpg" width="30px"><span>凡凡</span> 👍（5） 💬（0）<div>第一个问题有点模糊，感觉这个设计没有问题，任何传输方式，一旦经过网络，都会发生很多可能性，必须做幂等处理。如果指的是服务端无状态的话，原因就是提升扩展性，应对C端用户的大规模和并发。

第二个问题，主要在于序列化和传输。序列化方面由于有格式就不如二进制紧凑，传输的数据量相对来说要大。另一个是二进制可以自定义规范，或者编码方案，传输路径上，数据被截获，也不容易解析。</div>2018-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/32/fc/5d901185.jpg" width="30px"><span>vic</span> 👍（4） 💬（0）<div>楼上那位，登陆动作可以看作是对session的CRUD操作</div>2018-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/27/b4/df65c0f7.jpg" width="30px"><span>| ~浑蛋~</span> 👍（1） 💬（0）<div>基于文本的 RPC怎么做文件传输，base64编码吗</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/5e/7b/0e1eb97a.jpg" width="30px"><span>luojielu</span> 👍（1） 💬（0）<div>存在并冲突的问题，比如两个都是出库的操作，两个操作都在未减库存前的时间点查询了库存，然后都返回了服务端减去库存后的数量，正确的结果应该是分开执行</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4a/8a/c1069412.jpg" width="30px"><span>makermade</span> 👍（1） 💬（0）<div>讲得很好</div>2018-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/a1/43d83698.jpg" width="30px"><span>云学</span> 👍（1） 💬（0）<div>这篇把无状态服务讲透彻了，太棒了</div>2018-08-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/uktgj5R0p78c67oLib8EuRMRCgP8yjxnZ1ibVOuibhRZvjJpKSJNaTl0UlEfGyiaaiaGyPmqpGYpibTt0QopX1qtWfQQ/132" width="30px"><span>杨大小最嗨皮</span> 👍（0） 💬（0）<div>RESTful的解释太精彩了 语义修改基于资源 无状态指服务端维护资源状态 客户端维护会话状态</div>2024-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/50/2b/2344cdaa.jpg" width="30px"><span>第一装甲集群司令克莱斯特</span> 👍（0） 💬（0）<div>太赞了！</div>2023-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/90/a0/162f298a.jpg" width="30px"><span>Kanon°</span> 👍（0） 💬（0）<div>soap是指传输xml格式的接口，restful是传输json格式的接口，是这样定义的吗？；如果使用http请求传输xml中包了个json，这种叫什么？还是没有理清到底什么是soap接口，什么是restful接口，有没有严格的规范定义</div>2021-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/e1/b7be5560.jpg" width="30px"><span>sam</span> 👍（0） 💬（1）<div>表述性状态转移就是由前端转移到后端吗</div>2020-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/72/85/c337e9a1.jpg" width="30px"><span>老兵</span> 👍（0） 💬（0）<div>1. 库存的例子restful存在的问题，在于并发的请求，可能会导致库存变成负数
2. 基于文本的rpc问题传输量大，且存在序列化和反序列化的操作（伴随着大量的计算）</div>2020-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/21/b1/87d742bf.jpg" width="30px"><span>在下科南有何贵干</span> 👍（0） 💬（1）<div>那我在手机app上看的B站的视频进度，为什么可以同步到PC的网页上呢？它在B站服务器上还是无状态化吗？</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/39/f9/b2fe7b63.jpg" width="30px"><span>King-ZJ</span> 👍（0） 💬（0）<div>在应用层SOAP和RESTful中做资源的调度，有自己的系统运作的模式。</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/81/1c614f4a.jpg" width="30px"><span>stg609</span> 👍（0） 💬（0）<div>想问下，关于库存问题的最终答案在课程哪一讲中有公布吗？</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/65/03/973b24ec.jpg" width="30px"><span>谢晋</span> 👍（0） 💬（0）<div>1、库存的扣减，需要考虑幂等性 ，商品的库存也是一种资源，但是好像没有删除库存一说，只有修改和查询。
2、基于文本的RPC是指的SOAP吗？</div>2019-05-12</li><br/>
</ul>