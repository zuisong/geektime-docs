你好，我是景霄。

上一节，我们简单介绍了量化交易的历史、严谨的定义和它的基本组成结构。有了这些高层次的基本知识，接下来我们就分模块，开始讲解量化交易系统中具体的部分。

从这节课开始，我们将实打实地从代码出发，一步步设计出一套清晰完整、易于理解的量化交易系统。

一个量化交易系统，可以说是一个黑箱。这个黑箱连接交易所获取到的数据，通过策略运算，然后再连接交易所进行下单操作。正如我们在输入输出那节课说的那样，黑箱的特性是输入和输出。每一个设计网络交互的同学，都需要在大脑中形成清晰的交互状态图：

- 知道包是怎样在网络间传递的；
- 知道每一个节点是如何处理不同的输入包，然后输出并分发给下一级的。

在你搞不明白的时候，可以先在草稿纸上画出交互拓扑图，标注清楚每个节点的输入和输出格式，然后想清楚网络是怎么流动的。这一点，对网络编程至关重要。

现在，我假设你对网络编程只有很基本的了解。所以接下来，我将先从 REST 的定义讲起，然后过渡到具体的交互方式——如何通过 Python 和交易所进行交互，从而执行下单、撤单、查询订单等网络交互方式。

## REST 简介

什么是 REST API？什么是 Socket？有过网络编程经验的同学，一定对这两个词汇不陌生。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/bc/cb39ed38.jpg" width="30px"><span>自由民</span> 👍（10） 💬（10）<div>为注册sandbox的账号折腾了半天，停在创建账号那里就不动了。不知道是不是墙的原因，挂了梯子终于注册好了，但是却要验证手机号码，开始我瞎填的美国加州，用网上的美国手机号接收验证码也不行。最后用另一个邮箱注册了，可以选中国的，手机也能接收到验证码。
思考题:应该不行，对并发程序，先运行的未必时间戳在前，而用递增序列则可以确保先开始的顺序一定在前。
课程的练习代码: https:&#47;&#47;github.com&#47;zwdnet&#47;PythonPractice</div>2019-10-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJOlibibPFEWOib8ib7RtfAtxND5FUqCxxoeTuLAbBI9ic23xuwdXT4IyiaWq3Fic9RgEAYI0lBTbEp2rcg/132" width="30px"><span>Jingxiao</span> 👍（50） 💬（5）<div>思考题答案：事实上，在要求不是很严格的低频交易中，timestamp 是可以作为 nonce 存在的，它满足单调递增不重复的特性，比如一小时只会发送几个交易请求的波段策略中，timestamp 完全没问题。但是，在频率较高的交易中，timestamp 可能就不是那么适合。如果你使用协程来编程，或者使用类似 node.js 这样的异步编程工具或语言，那么你的代码很可能在发送的时候，并不是按照你想要的顺序发送给服务器，就会出现 timestamp 更大的请求反而更早发送。其次，在网络传输中，不同的包也可能有完全不同的抵达顺序，虽然你可以通过一些编程技巧来实现按顺序传输，但是如果你需要多台机器进行较为高频的交易。而且需要对同一个仓位（同一个 API Key）进行操作，就可能会变得比较麻烦。
</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/29/d6816ebf.jpg" width="30px"><span>小侠龙旋风</span> 👍（18） 💬（1）<div>知识点很多，整理一下。
1. 非对称加密：
    加密：公钥加密，私钥解密；
    签名：私钥签名，公钥验签。
2. hmac.new(key, str, digestmod)
    key是密钥；str是欲加密的串；digestmod是hmac加密算法
3. 最后一句打印语句可以写成如下看着更清晰：
    print(json.dumps(new_order, indent=4))
4. 在草稿纸上画出交互拓扑图
5. 如何设计符合RESTful特征的API
6. Keep-Alive: timeout=5, max=100

思考题：
测试了一下timestamp效果，代码如下：
import time
import datetime
current_time = datetime.datetime.now()
print(int(datetime.datetime.timestamp(current_time)*1000))
print(int(time.mktime(current_time.timetuple())*1000))

同样都是时间戳，timestamp是带毫秒的，具备单调递增、加密混乱的特质。
文中有句话是这么说的：&quot;当某个后来请求的nonce比上一个成功收到的请求的nonce小或者相等的时候，Gemini便会拒绝这次请求&quot;。
说明Gemini不希望http请求在一秒内发生多次。应该是反爬用的吧~
用timestamp是可以精确到毫秒的，意味着每毫秒可以请求发送的nonce都不一样。

另外，作为taker第二次运行该代码就报出下面的错：
{
    &quot;result&quot;: &quot;error&quot;,
    &quot;reason&quot;: &quot;InsufficientFunds&quot;,
    &quot;message&quot;: &quot;Failed to place buy order on symbol &#39;BTCUSD&#39; for price $3,633.00 and quantity 5 BTC due to insufficient funds&quot;
}</div>2019-07-27</li><br/><li><img src="" width="30px"><span>瞳梦</span> 👍（3） 💬（4）<div>请问gemini sandbox账号怎么注册呢？我在官网只找到了Open a Personal Account和I Represent an Institution</div>2019-07-26</li><br/><li><img src="" width="30px"><span>Xg huang</span> 👍（1） 💬（1）<div>哈哈，深入浅出，赞一个

不过有个地方是否写错？&quot;而小宝在某一天中午 11:59:00，告诉交易所，我要挂一个单子，数量为 0.1 比特币，价格为 10000 美元，低于这个价格不卖。&quot;

是不是1000才对？</div>2019-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4b/bf/d714f592.jpg" width="30px"><span>王帅帅</span> 👍（0） 💬（1）<div>我跑了一遍，提示gemini 交易所正在维护，怎么回事。</div>2020-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bc/29/022905e6.jpg" width="30px"><span>SCAR</span> 👍（13） 💬（0）<div>思考题：
1. 纯粹使用timestamp应该不行，虽然timestamp也是递增的，但是在python里timestamp是float而不是int。
2.但如果基于timestamp抽取出部分应该是可以，比如老师例子中的：
   payload_nonce = str(int(time.mktime(t.timetuple())*1000))
   改成：
   payload_nonce = str(int(t.timestamp())*1000)
   结果应该是一致的。</div>2019-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/92/7b/8c7e3e61.jpg" width="30px"><span>Monroe  He</span> 👍（7） 💬（2）<div>我想问一下老师，有针对国内股票的虚拟交易平台吗
可以提供一下相关方面的书籍资料吗</div>2019-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/88/b787338a.jpg" width="30px"><span>devna</span> 👍（6） 💬（0）<div>前段时间刚看完《计算机网络：自顶自下方法》，确实不错，能很快提升对网络的认识，强烈推荐</div>2020-01-19</li><br/><li><img src="" width="30px"><span>karofsky</span> 👍（4） 💬（0）<div>今天再看这篇文章的感受就是，BTC真的涨了好多啊...</div>2021-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d5/ca/488c0688.jpg" width="30px"><span>kang</span> 👍（3） 💬（6）<div>請問大家都是怎麼註冊Genimi 的? 我的註冊國家都被阻擋</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/18/b6/f3f68a39.jpg" width="30px"><span>马建华</span> 👍（2） 💬（3）<div>我是报错：
{&#39;result&#39;: &#39;error&#39;, &#39;reason&#39;: &#39;MissingAccounts&#39;, &#39;message&#39;: &#39;Expected a JSON payload with accounts&#39;}
有谁碰到吗？</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/ec/4b/442dd5f1.jpg" width="30px"><span>及時行樂</span> 👍（2） 💬（0）<div>现在程序跑起来都报错了，这是交易所把API地址改了吗？
{&#39;result&#39;: &#39;error&#39;, &#39;reason&#39;: &#39;EndpointMismatch&#39;, &#39;message&#39;: &#39;EndpointMismatch&#39;}</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/d9/8d/78dd472a.jpg" width="30px"><span>知止。</span> 👍（1） 💬（2）<div>老师，是不是该针对运行可能出现的一些问题给出解答呢？如果网站变更过信息，那么课件相应也得更新一下吧，不然后来订阅学习的人没办法完整学习啊。比如我按照课件内容运行，提示{&#39;result&#39;: &#39;error&#39;, &#39;reason&#39;: &#39;InvalidSignature&#39;, &#39;message&#39;: &#39;InvalidSignature&#39;}，网上都找不到原因，想自己排查错误都不懂如何着手
</div>2020-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/50/26/b0a0b6b5.jpg" width="30px"><span>SuperXiong</span> 👍（1） 💬（7）<div>第一部：注册sandbox没有成功，选了中国区，提交注册表之后，返回一个未知问题。</div>2020-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3d/e1/5279ea2f.jpg" width="30px"><span>鱼鱼鱼培填</span> 👍（1） 💬（1）<div>请教老师一个问题：在Gemini注册账号之后用生成key和secret实现代码，结果一直出现InvalidSignature
试了两种方式：
1、一开始以为是key setting的问题，结果三种都试过还是一样的结果
2、重新生成key和secret，也还是一样的结果
Google查找后发现有人也是一样的结果，但是没有找到解决方案</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（1） 💬（0）<div>老师讲得好啊，妙啊！</div>2019-07-26</li><br/><li><img src="" width="30px"><span>Geek_adeba6</span> 👍（1） 💬（1）<div>想请问如果想实现秒级别的市场行情获取，生产环境下的最佳实践是什么？</div>2019-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/44/3e3040ac.jpg" width="30px"><span>程序员人生</span> 👍（1） 💬（0）<div>timestamp应该不能代替nonce。
当某个后请求的nonce，比上一个成功收到请求的nonce小或者等于时候，服务器会拒绝接收。
但timestamp不行，因为后请求的timestamp，可能会由于各种原因先到服务器，先请求的可能会晚到，并不能体现先后次序。
不知道我理解是否正确？</div>2019-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ab/a8/eb9f186e.jpg" width="30px"><span>SuQiu</span> 👍（1） 💬（1）<div>timestamp也属于自增长，猜测是由于他的可预见性，所以不能代替nonce</div>2019-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第34讲打卡~</div>2024-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/10/78/29bd3f1e.jpg" width="30px"><span>王子瑞Aliloke有事电联</span> 👍（0） 💬（0）<div>网站挂了，我尝试了开梯子与不开梯子，网站都是 500

Request URL:
https:&#47;&#47;exchange.sandbox.gemini.com&#47;register&#47;new-user
Request Method:
POST
Status Code:
500 Internal Server Error
Remote Address:
127.0.0.1:17890
Referrer Policy:
strict-origin-when-cross-origin</div>2023-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/83/8d/03cac826.jpg" width="30px"><span>徐李</span> 👍（0） 💬（0）<div>时间错不能完全保证唯一性</div>2022-04-27</li><br/><li><img src="" width="30px"><span>Geek_56b863</span> 👍（0） 💬（0）<div>老师，requests.post(url,data=None,headers=request_headers) 执行后，等待一会儿会报错：ConnectionError: HTTPSConnectionPool(host=&#39;api.sandbox.gemini.com&#39;, port=443): Max retries exceeded with url: &#47;v1&#47;order&#47;new (Caused by NewConnectionError(&#39;&lt;urllib3.connection.HTTPSConnection object at 0x00000141BA65CAC0&gt;: Failed to establish a new connection: [WinError 10060] 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。&#39;))

科学上网也无法解决，会报出另一个错误：ValueError: check_hostname requires server_hostname

请问老师，这个REQUEST.POST问题，应该如何解决呢？谢谢解答</div>2021-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/58/3e/77c9b529.jpg" width="30px"><span>Sanhong</span> 👍（0） 💬（0）<div>如果报{&#39;result&#39;: &#39;error&#39;, &#39;reason&#39;: &#39;InvalidSignature&#39;, &#39;message&#39;: &#39;InvalidSignature&#39;} ，就检查一下key和secret是否正确；
如果报{&#39;result&#39;: &#39;error&#39;, &#39;reason&#39;: &#39;MissingAccounts&#39;, &#39;message&#39;: &#39;Expected a JSON payload with accounts&#39;}，就检查一下scope是否为Primary，并且Permissions是否有交易权限。</div>2020-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/33/a2/6c0ffc15.jpg" width="30px"><span>皮皮侠</span> 👍（0） 💬（0）<div>谢谢老师教我方法✌️</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/17/96/a10524f5.jpg" width="30px"><span>蓬蒿</span> 👍（0） 💬（0）<div>还有一点就是timestamp在nat网络中会有问题，难以保证单调递增，虽然这种极端情况基本不可能发生</div>2020-04-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/8P1a8D3WButrPQicebnKkrAiaI1lWUfZicWPtWfXHbm9Xv7qb1tkJ7eiaxVG2JfO8mLJt7AzmPXjn0MsgjKBWujFfQ/132" width="30px"><span>余皇南</span> 👍（0） 💬（0）<div>nonce 并不幂等啊？ 因为网络原因会造成 重复下单（首次成功但延迟）的可能；</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/84/70340e87.jpg" width="30px"><span>向南</span> 👍（0） 💬（0）<div>区别在于生成nonce及执行交易的顺讯，会不会出现后生成nonce的交易请求抢先一步提交交易所执行交易，导致先前生成nonce的请求不得已被延后执行时，被交易所拒绝。
若能保证 先一步 生成nonce的交易请求 先执行交易，则二者没啥区别（时间戳是float的不考虑，肯定会转换的）；若不能保证，则nonce更安全些。
但是文中的nonce本质上不也是时间戳吗？
看了Gemini REST API 的文档，文中的例子和Gemini给的例子一毛一样。
还有就是创建master API账户无法进行交易，必须是Primary账户。</div>2020-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/51/86/b5fd8dd8.jpg" width="30px"><span>建强</span> 👍（0） 💬（0）<div>网络编程没有接触过，对这道思考题的个人初步理解：用timestamp代替nonce可能会有隐患，第一，timestamp是时间戳，而nonce要求是整数，可能需要做转换；第二，timestamp需要根据发送方服务器时间来生成，一旦发送方的服务器时间设置错误，有可能造成接收方拒收；第三，用timestamp容易被破解，可能会受第三方的攻击。</div>2020-02-19</li><br/>
</ul>