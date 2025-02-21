你好，我是李智慧。

从这节课开始，我们将结合具体的案例，来看看怎么设计高并发系统，你也可以学习具体的软件设计文档写法了。这个模块，我们先来看看，当高并发遇到海量数据处理时的架构。

在社交媒体上，人们经常需要分享一些URL，但是有些URL可能会很长，比如：`https://time.geekbang.org/hybrid/pvip?utm_source=geektime-pc-discover-banner&utm_term=geektime-pc-discover-banner`

这样长的URL显然体验并不友好。我们期望分享的是一些更短、更易于阅读的短URL，比如像 `http://1.cn/ScW4dt` 这样的。当用户点击这个短URL的时候，可以重定向访问到原始的链接地址。为此我们将设计开发一个短URL生成器，产品名称是“Fuxi（伏羲）”。

我们预计Fuxi需要管理的短URL规模在百亿级别，并发吞吐量达到数万级别。这个量级的数据对应的存储方案是什么样的？用传统的关系数据库存储，还是有其他更简单的办法？此外，如何提升系统的并发处理能力呢？这些是我们今天要重点考虑的问题。

## 需求分析

短URL生成器，也称作短链接生成器，就是将一个比较长的URL生成一个比较短的URL，当浏览器通过短URL生成器访问这个短URL的时候，重定向访问到原始的长URL目标服务器，访问时序图如下。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1f/3c/10/61efe672.jpg" width="30px"><span>向东是大海</span> 👍（40） 💬（1）<div>短URL使用URL Base64 编码，其中的-和_字符显得有点突兀，特别是在开头或结尾是时。短URL使用Base62编码是否更好？</div>2022-02-21</li><br/><li><img src="" width="30px"><span>老码不识途</span> 👍（39） 💬（3）<div>再加一个架构的约束：只有2万块钱的预算 ^_^</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/47/3b/70198ceb.jpg" width="30px"><span>Aibo</span> 👍（34） 💬（6）<div>个人感觉内存中存储短url的数据结构是不是用环形数组会好一点.
短url的场景下，使用链表会有两个缺点
1. gc压力大，频繁申请内存空间
2.格外的指针开销，短url才6byte，指针就占1byte，也就是内存中10g数据1个多g都是指针
</div>2022-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/ba/50/6c2ef3cf.jpg" width="30px"><span>Spark</span> 👍（30） 💬（6）<div>对自增长短 URL可以进行如下优化：
在设计的短链接的时候采用这样的方法：
根据自增主键id将前面补0（4位短链接补至7位，6位短链接补至10位，8位短链接补至14位）如主键：123，补0至0000123
倒转补完0之后的id，如3210000
将倒转之后的短链接十进制转62进制。将3210000转62进制
本质上来讲，因为用户不知道你补位的位数，所以无法反推出你之前的短链接与之后的短链接。
在自增的选择上，可以选择redis的自增机制。
是不是这样，我也可以满足并发的需求，毕竟计算速度远大于查找。
同时，清理的过程也更加简单，只需要在达到自增补位上限的时候，将自增变为1重新发号即可
当然，从技术上讲，他是可预测的，毕竟短链就这么多位，猜测（7-14进行枚举），但是面对大部分业务来说，他已经满足部分不可预测的需求。</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fb/7b/2d4b38fb.jpg" width="30px"><span>Jialin</span> 👍（16） 💬（7）<div>问题一:如何解决相同的原始链接生成不同的短链接？
当要给一个原始网址生成短网址的时候，我们要先拿原始网址在数据库中查找，看数据库中是否已经存在相同的原始网址了。如果数据库中存在，那我们就取出对应的短网址，直接返回给用户。并给短网址和原始网址这两个字段，都添加索引。短网址上加索引是为了提高用户查询短网址对应的原始网页的速度，原始网址上加索引是为了加快通过原始网址查询短网址的速度。
问题二:并发量是如何计算的？
基于利特尔法则（Little&#39;s law）得知，并发度 = QPS * 平均耗时，所以，2 万 QPS，10ms 平均响应时间，真正的并发量只有 200。</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b9/32/84346d4a.jpg" width="30px"><span>雪碧心拔凉</span> 👍（12） 💬（1）<div>看了下评论区的，大部分都是通过布隆过滤器来解决不能重复，有一下几个疑惑点。
1、已使用的数据还会被回收，因此布隆过滤器的数据还存在删除的操作，或者每次回收时重构布隆过滤器？
2、布隆过滤器本身有一定的误判率，如果存在，但是实际可能不存在，这时要走生成的逻辑，请求耗时可能大于10ms。当然这个可以通过调整布隆过滤器的参数降低概率

我理解是不是只需要保持一段时间内不重复即可，是否可以把长url(做个md5,降低存储？)和短url存储在缓存(如redis)中，有效期设为一天或者半天，这样能控制一段时间内返回同一个短url即可？</div>2022-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/d9/75dd7cf9.jpg" width="30px"><span>Mew151</span> 👍（12） 💬（1）<div>第1个问题，还可以从另外一个角度考虑：即客户端本地记用户请求过的长-短URL映射，如果用户再次请求同一个长URL，先查客户端本地映射，如果有就直接返回。这种方式能防住大部分正常的客户端重复请求，防不住的是例如恶意攻击者直接抓包调接口，因此服务端的判重还得做。</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/03/77/3f6a76a9.jpg" width="30px"><span>极客</span> 👍（10） 💬（4）<div>加载到预加载短 URL 服务器的 1 万个短 URL 会以链表的方式存储，每使用一个短 URL，链表头指针就向后移动一位，并设置前一个链表元素的 next 对象为 null。这样用过的短 URL 对象可以被垃圾回收。当剩余链表长度不足 2000 的时候，触发一个异步线程，从文件中加载 1 万个新的短 URL，并链接到链表的尾部
-----

这里如果为了高可用是不是需要保存到日志或者redis，要是服务有bug导致频繁重启，那么重启后又要获取1万个。多来几次会浪费很多短地址没有使用。且预生成的144亿次没有继续生成的机制保证。</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/21/14/423a821f.jpg" width="30px"><span>Steven</span> 👍（8） 💬（2）<div>思考题：
1，首先可以明确，一定程度上的重复生成是可以的。
方案一：可以考虑用布隆过滤器；
方案二：考虑Redis中存储长链接 -&gt; 短链接，并设定合理的过期时间，参考课程内容，貌似可以6天，或许1小时就可以。

另外，基于分布式ID生成短URL也是可以的。

2，200 = 20000 * 0.01

问题：“对于这样简单的业务逻辑以及 200 这样的并发压力，我们使用配置高一点的服务器的话，只需要一台短 URL 服务器其实就可以满足了。”，大概是一台什么配置的服务器？</div>2022-03-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo572BONDovD8wvzjwU89bRHVLicHib19MW7ice5Xz9LgsNWXaqx53E1Esd1MsC0hYD9RwRAwwAcgWcA/132" width="30px"><span>cy_walker</span> 👍（8） 💬（2）<div>老师，我有个疑问。就是在生成短链的时候，假如在短时间内有大量需要生成短链的请求，那预先加载的1W个短链就不够了，这种情况该如何解决？直接服务降级？</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（7） 💬（1）<div>第一个问题：

重复生成同一个长URL，带来的问题主要是资源浪费。并且没有处理用户的重复请求。
可以考虑的解决方案是缓存，将每个长URL作为参数缓存起来。保存一段时间，只需要存几天即可。下次请求的时候，地址如果还是同样的长URL，并且命中缓存，那就把现有的短URL直接返回。系统其实并没有做到短URL的目标URL不重复，但是能做到几天内不重复已经足够了。

第二个问题：

10ms=1\100s 也就是说一个请求耗时仅有100分之一秒。100个请求才占1秒的qps。2w➗100=200

</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/f1/fd/003cf398.jpg" width="30px"><span>Leader</span> 👍（5） 💬（1）<div>请问老师，为什么经过了MD5或者SHA256 hash之后还要再进行base64，不可以直接使用hash之后的结果吗？研究了一下没想清楚为什么</div>2022-02-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibcRNslcyp7dwIR3TIwvloCibMd7Ew2TB3MU0wISFXEolyuHRtfIriagm6PMX5zQHicmc78BrBcxA6vQ5qnTPCev9A/132" width="30px"><span>jiangjing</span> 👍（4） 💬（3）<div>1s &#47; 1ms = 100 每秒可处理100个请求
2w &#47; 100 = 200 一秒内用一时刻只需要处理200请求

疑问：一般并发就是指qps &#47; tps 吧？还是指这个计算出的200？</div>2022-02-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibbEWWUTH7964UOnwpBPC8Lhb1TS4s7XMEXTPKHPUBlj58GVkdRQRqa6EydIRL2I1uJDzeichLj86gJfTpzcgcCA/132" width="30px"><span>Vincent_</span> 👍（3） 💬（1）<div>1. 查询请求那里就说了有缓存，按照一个生成url访问一般在6天来算，跟查询请求一样，查询的k-v是短-长，只需要生成的时候也生成一份长-短即可，对应的一个缓存查和增，按1ms算，也就2ms。还是符合要求的。对应的就是缓存空间*2。另一种方法是使用布隆过滤器，生成后的长url放入布隆过滤器，新的请求过来如果布隆过滤器拦截，按查询请求看待，如果是误差请求，则再生成短url，对应的误差请求时间会变长，但是因为布隆过滤器极低的误差率，在平均耗时上也是满足要求的。
2. 2w&#47;100 = 200</div>2022-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/68/d4/c9b5d3f9.jpg" width="30px"><span>💎A</span> 👍（3） 💬（4）<div>面试的时候一上来就是百万并发😝</div>2022-02-22</li><br/><li><img src="" width="30px"><span>Geek6900</span> 👍（2） 💬（1）<div>如果取了2w个短URL后，还没有用完，这时服务重启或者宕机，因为只是加载到了内存，相当于会浪费一些短URL，如何解决这种浪费问题？</div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/79/b8ce297e.jpg" width="30px"><span>Winter</span> 👍（2） 💬（1）<div>老师，请问可以用MySQL取代HBASE吗</div>2022-02-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL6sbiaEsWOIFiaCSe0KL1alJcsb9LhNRkQlMpNTbdCoZMqHghfXn02WsjwcWn5A9FfTXx3bkdnxSicg/132" width="30px"><span>Tim</span> 👍（2） 💬（5）<div>1）重复请求生成不同的短链没有问题，这就是老师预留20%多余短链的目的。如果去重的话，可以对长链采用布隆过滤判定是否已经占用
2）200&#47;0.01=20000，反之。</div>2022-02-21</li><br/><li><img src="" width="30px"><span>Geek_46be40</span> 👍（1） 💬（1）<div>URL长度估算那里为啥是64呢，26个字母大小写是52个，再加上0~9个数字，总共是62位啊，为什么是64呢？</div>2022-04-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELtOO0HKrj5SI5JSlmwiaCvaF6GLiaTmf5NX88OZaO3HymTAGTeIoicBUjqzmMF6sF5raPFjuqLFibrrw/132" width="30px"><span>gesanri</span> 👍（1） 💬（1）<div>文中提到预生成URL用布隆过滤器检查是否重复，那布隆过滤器检查是判断一定不存在或可能存在，如果结果是可能存在，那是继续去hdfs里面判断是否存在还是直接丢弃这个URL?继续判断效率会不会有问题，但如果丢弃那也可能造成大量实际不重复的URL被丢弃，而导致6位短链无法生成120亿个，有这种可能吗？</div>2022-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a3/21/abb7bfe3.jpg" width="30px"><span>saber</span> 👍（1） 💬（1）<div>拿短URL的acquireURL方法是带锁的么？如果不带，怎么确保唯一？如果带，怎么确保高性能？</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/11/eb/3cc36d1c.jpg" width="30px"><span>Neon</span> 👍（1） 💬（1）<div>“过期短 URL 清理服务器会每个月启动一次，将已经超过有效期（2 年）的 URL 数据删除，并将这些短 URL 追加写入到短 URL 预生成文件中。”这是对过期短链二次使用的意思吗？</div>2022-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/63/ea/1a128e67.jpg" width="30px"><span>来需求了，很忙</span> 👍（1） 💬（1）<div>为什么生成的短链不直接放到HBASE，被使用的短链去做update，这样不是简单点，也不用引入hdfs</div>2022-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0d/be/6acd4b18.jpg" width="30px"><span>刘帅</span> 👍（1） 💬（1）<div>问题一：原始链接重复生成短url会造成存储资源浪费，计算性能浪费等问题，可以使用布隆过滤器对原始链接进行过滤，存在对应的短url直接返回即可
问题二：2Wqps*10ms=200并发度，即同一时刻只需处理200个并发用户的请求就可满足2Wqps的性能要求</div>2022-02-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJbCmibL1XtPQmCJxUPg8rHLNgBZbor9UxAN3nOLhehicGkUcWGlq2Zic3XgHX1GLeXYJA0H3OPcNKPw/132" width="30px"><span>李焕之</span> 👍（1） 💬（1）<div>李老师好，有两个疑问：1、文中说：每条短 URL 数据库记录大约 1KB。为什么会这么大呢？短+长串应该超不过200字节吧？还是考虑可能会有极端长的url？ 2、6位base64码680亿，预先生成了120亿，还是有很大概率可以使用短URL去撞到长URL呀,六分之一的概率，需要考虑防刷吗？</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/58/f5/abb7bfe3.jpg" width="30px"><span>Tianium</span> 👍（1） 💬（2）<div>需求没有分析生成短url的规模和性能指标吧，一般生成短url的性能可以允许差点，如果不是，那问题一就不能简单用查hbase来解决了，而需要利用列入课程提到的bloom filter以及分布式缓存进一步加速了。</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/24/b807e3ee.jpg" width="30px"><span>linuxcoder</span> 👍（1） 💬（3）<div>请问老师，通过hdfs预加载方案，只有一台服务器能读取偏移量，然后读到10k个地址，放入内存，那负载均衡器如何知道哪个服务器有数据呢？需要把这个10k个短地址放入分布式cache吗？否则的话会有性能瓶颈吗？谢谢</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/24/b807e3ee.jpg" width="30px"><span>linuxcoder</span> 👍（1） 💬（1）<div>思考一：
如果用户重复提交同一个长 URL 请求生成短 URL，每次都会返回一个新的短 URL，这样会导致多个短URL对应一个长URL。如果需求只允许1对1，可以在返回生成的短URL之前去HBase查一下是否生成过了。如果允许N个短URL对应一个长URL，也可以从HBase查一下是否超过了N，如果没有，则返回生成的一个段URL。

思考二：
并发数=QPS*平均响应时间=20000 queries&#47;s * 0.01 s = 200 queries</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8a/5a/b67a82e3.jpg" width="30px"><span>shen</span> 👍（1） 💬（1）<div>2wqps是指每秒钟2w请求，现在10ms响应结果那么平均并发量20000*10&#47;1000=200</div>2022-02-21</li><br/><li><img src="" width="30px"><span>Geek_476dbc</span> 👍（0） 💬（1）<div>“加载到预加载短 URL 服务器的 1 万个短 URL 会以链表的方式存储，每使用一个短 URL，链表头指针就向后移动一位，并设置前一个链表元素的 next 对象为 null。这样用过的短 URL 对象可以被垃圾回收。”预加载如果是纯内存操作，服务重启不就丢了？重新读一批的话有一些短URL就浪费掉了？这里是不是用一个小的redis集群来存更合适一些，服务重启后数据还在。</div>2024-08-10</li><br/>
</ul>