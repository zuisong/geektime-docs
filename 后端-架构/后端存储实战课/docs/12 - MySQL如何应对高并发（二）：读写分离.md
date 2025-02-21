你好，我是李玥。

上节课我和你讲了，使用Redis作为MySQL的前置缓存，可以帮助MySQL挡住绝大部分的查询请求。这种方法对于像电商中的商品系统、搜索系统这类与用户关联不大的系统，效果特别的好。因为在这些系统中，每个人看到的内容都是一样的，也就是说，对后端服务来说，每个人的查询请求和返回的数据都是一样的。这种情况下，Redis缓存的命中率非常高，近乎于全部的请求都可以命中缓存，相对的，几乎没有多少请求能穿透到MySQL。

但是，和用户相关的系统，使用缓存的效果就没那么好了，比如说，订单系统、账户系统、购物车系统等等。在这些系统里面，每个用户需要查询的信息都是和用户相关的，即使是同一个功能界面，那每个人看到的数据都是不一样的。

比如说，“我的订单”这个功能，用户在这里看到的都是自己的订单数据，我打开我的订单缓存的数据，是不能给你打开你的订单来使用的，因为我们两个人的订单是不一样的。这种情况下，缓存的命中率就没有那么高，还是有相当一部分查询请求因为命中不了缓存，打到MySQL上。

那随着系统用户数量越来越多，打到MySQL上的读写请求也越来越多，当单台MySQL支撑不了这么多的并发请求时，我们该怎么办？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/e7/76/79c1f23a.jpg" width="30px"><span>李玥</span> 👍（30） 💬（5）<div>Hi，我是李玥。

这里回顾一下上节课的思考题：

课后请你想一下，具体什么情况下，使用Cache Aside模式更新缓存会产生脏数据？欢迎你在评论区留言，通过一个例子来说明情况。

说一种可能产生脏数据的情况：

使用Cache Aside模式来更新缓存，是不是就完全可以避免产生脏数据呢？也不是，如果一个写线程在更新订单数据的时候，恰好赶上这条订单数据缓存过期，又恰好赶上一个读线程正在读这条订单数据，还是有可能会产生读线程将缓存更新成脏数据。但是，这个可能性相比Read&#47;Write Through模式要低很多，并且发生的概率并不会随着并发数量增多而显著增加，所以即使是高并发的场景，这种情况实际发生的概率仍然非常低。

既然不能百分之百的避免缓存的脏数据，那我们可以使用一些方式来进行补偿。比如说，把缓存的过期时间设置的相对短一些，一般在几十秒左右，这样即使产生了脏数据，几十秒之后就会自动恢复了。更复杂一点儿的，可以在请求中带上一个刷新标志位，如果用户在查看订单的时候，手动点击刷新，那就不走缓存直接去读数据库，也可以解决一部分问题。</div>2020-03-24</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoxUFAanq6rz2MqHXtn7vAvyIe0ljoqCtX3gnqZujLk7x90llHedHqCpHCnbYJeZmPX06Y6OFlibpQ/132" width="30px"><span>王佳山</span> 👍（21） 💬（4）<div>这篇文章中提到的同一个事务会路由到主库是什么意思？</div>2020-06-15</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/4pFDynicvRnrTTRavia64UAknQjyX3KFfm67W4AZG52wm2TgwL1FWNX1zhIlIVgicPw2jzPqKASAib5nI1QfY6pc2Q/132" width="30px"><span>上山砍柴</span> 👍（7） 💬（1）<div>老师您好！读写分离后，是否可以满足高并发写呢，比如秒杀系统，能够满足瞬间大量订单创建写数据库吗？</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（6） 💬（1）<div>HAproxy keepalived是和mysql部署在同一台机器上的吗？还是部署在单独的机器上的？</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/d7/5d2bfaa7.jpg" width="30px"><span>Aliliin</span> 👍（33） 💬（3）<div>在上家公司，我记得我写订单支付成功之后需要送优惠券的业务，也导致赠送优惠券不成功。
测试环境怎么都不出问题，后来才想到的是主从的问题，之后就修改成功了，从主库查询并增加优惠券。忙到半夜。这个课程真是太好了。</div>2020-03-24</li><br/><li><img src="" width="30px"><span>Mongo</span> 👍（17） 💬（0）<div>- Redis作为 MySQL前置
  针对类似电商类看到的结果是一样的效果很好
  针对看到的内容各不相同的时候，效果一般
- MySQL 针对高并发方案
  - 分布式存储系统难点
      写难以保证数据一致性
      分布式读相对简单
  - 构建分布式集群
    不建议构建分布式集群，代价大
  - 读写分离方案
    读写分离，可有效分担大量的查询请求
    读写分离，实施比较方便
    - 读写分离方案
      部署一主多从多个 MySQL 实例，并让他们之间保持数据实时同步
      分离应用程序对数据库的读写请求，分别发送到从库和主库
      - 分离读写的方法(推荐第二种)
        1.纯手工方式：修改应用程序 DAO 层代码，定义读写两个数据源，指定每一个数据库请求的数据源
        2.组件方式：也可以使用像 Sharding-JDBC这种集成在应用中的第三方组件来实现，这些组件集成在你的应用程序内，代理应用程序的所有数据库请求，自动把请求路由到对应数据库实例上
        3.代理方式：在应用程序和数据库实例之间部署一组数据库代理实例， 比如 Atlas 或者 MaxScale。对应用程序来说，数据库代理把自己伪装成一个单节点的 MySQL 实例，应用程序的诉讼有数据库请求被发送到给代理，代理分离读写请求，然后转发给对应的数据库实例。
      - 配置多个从库
        推荐使用&quot;HAProxy + Keeplived&quot;组合
    - 读写分离弊端
      可能导致数据不一致的问题，正常不超过1ms
      - 解决方法
        将同步的一些操作放到一个数据库事务中来做，写与读在一个库
        增加一些步骤操作，让 1ms 的同步自然的消耗掉</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d5/e1/a05a9e22.jpg" width="30px"><span>kyll</span> 👍（15） 💬（0）<div>原来用mycat，现在我们使用sharding-jdbc，配置简单，对开发透明。而且看官网上未来发展前景不错。sharding可以做到同一个线程内更新后的查询在主库进行，其他的情况也是在交互上做改进了</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（10） 💬（0）<div>电商直接提示，订单稍后查询😄</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（6） 💬（2）<div>HAProxy+Keepalived这套架构：挺好挺稳定，业界使用率很高。
偷懒点可以直接用云厂商，不过读写分离的能力确实不敢恭维。</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5d/11/e1f36640.jpg" width="30px"><span>怀朔</span> 👍（4） 💬（0）<div>现在主流的都是用proxy的

主备延迟怎么解决呢？ 
1、开启半同步方案
2、尽量在主库里面减少大事务、使用不均匀的话开启写后考虑主库读
3、有能力的话 分库分表
4、增加从库性能
5、如果实在无法追平 从新做从库吧</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/f7/91ac44c5.jpg" width="30px"><span>Mq</span> 👍（4） 💬（0）<div>        我们系统现在从库没有ha的配置，在检测到主从延迟大于几秒后或故障后，把数据源自动切换切换到主库，如果检测一段时间延长减少又把数据源切换到从库，这种方式目前还行，如果并发真上来了，然后主从同步延迟加大导致切换到主库，可能把主库也搞挂。
         缓存有2层，一层是渠道端，策略是我们有更新了发mq消息通知他们删除，一层是我们系统在有导致数据变更的接口调用后会刷缓存，策略是查主库把数据弄到缓存，另外就是设置缓存失效时间，在回到看数据的页面也要几秒，这种针对活跃的数据有较好的效果，不活跃的数据也没有数据延迟的问题</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e7/f0/d0bf3a5f.jpg" width="30px"><span>Regis</span> 👍（3） 💬（0）<div>我们公司web开发才刚刚起步，主要公司内部使用，还用不到读写分离，不过老师讲的很透彻，终于知道为什么有些网站支付后会有几秒等待才会返回结果了</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f8/e5/50b435ca.jpg" width="30px"><span>程七</span> 👍（1） 💬（0）<div>首先，一个读线程A从缓存中获取订单数据，此时缓存中没有该订单数据，所以线程A从数据库中加载数据，并将该数据写入缓存中。
接着，另一个读线程B也从缓存中获取该订单数据，此时缓存中有该数据，线程B直接从缓存中读取该数据并使用。
在此时，写线程C更新了该订单数据，并将数据库中的数据标记为已更新状态。
此时，由于Cache Aside模式，缓存中的订单数据并没有被更新。如果此时读线程A或者B再次读取该订单数据，它们将会从缓存中获取旧的数据，从而得到脏数据。
为了避免这种情况，写线程C在更新数据库后，应该删除缓存中的该订单数据。但是，在这个删除缓存的瞬间，如果读线程B还在使用缓存中的该订单数据，那么它就会得到脏数据。
简而言之，脏数据的产生过程就是由于在删除缓存和更新缓存之间的这个短暂时间内，另一个读线程仍然可以从缓存中获取到旧数据，从而导致数据不一致性。</div>2023-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2d/d7/74fc8f38.jpg" width="30px"><span>灿烂明天</span> 👍（1） 💬（0）<div>老师，HAProxy+Keepalived这个方案具体是怎么做的，谢谢</div>2020-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/bb/7afd6824.jpg" width="30px"><span>闫冬</span> 👍（1） 💬（0）<div>李老师 主从延迟时间比较短的情况 可以在设计上解决 如果延迟时间比较长呢</div>2020-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/a9/cb/a431bde5.jpg" width="30px"><span>木头发芽</span> 👍（1） 💬（1）<div>阿里云的rds自带读写分离功能，连接数据库是一个url，它通过分析sql语句来决定，更新和事务路由到主库，读写到只读从库，对开发来说无感知，运维只要根据压力情况增加或减少主从节点就好。
但老师是不是没有说当单表量太大的时候，读写分离并不能解决压力问题，还得分库</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/18/bf7254d3.jpg" width="30px"><span>肥low</span> 👍（1） 💬（0）<div>主从同步的问题经常遇到,虽然采用公有云,但是很多时候都不能保证毫秒级响应,我这里的方案是,如果存在DML,并且业务方对实时性要求很高的话,那业务上把数据放到Redis这种高性能的Cache中去,如果要求不高就直接读从库,至于啥时候用读库、啥时候用主库,这个跟老师说的一样,我们在框架层面就给保证了,唯一缺憾就是,如何降低延迟,一直在摸索中...</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/84/49/47d48fd0.jpg" width="30px"><span>观弈道人</span> 👍（1） 💬（0）<div>京东那么大数据量，数据应该还是要分片的，没法避免</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（1） 💬（0）<div>对于可能存在主从延迟的地方可以采取强制读主库的措施。</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/13/31ea1b0b.jpg" width="30px"><span>峰</span> 👍（1） 💬（0）<div>写后读，走主库</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1a/05/f154d134.jpg" width="30px"><span>刘楠</span> 👍（1） 💬（0）<div>我们公司用的代理的方式，主从延迟，更新完即读的场景不多，强制读主库解决的，</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fc/d1/57ba44a1.jpg" width="30px"><span>果娞</span> 👍（0） 💬（0）<div>怎么让查询用户信息相关的缓存命中率高一点啊</div>2024-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>除非系统规模真的大到只有这一条路可以走，不建议你对数据进行分片，自行构建 MySQL 集群，代价非常大。--记下来</div>2022-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2022-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/bb/3b/6e020a32.jpg" width="30px"><span>多学多看多记</span> 👍（0） 💬（0）<div>go后端，从组件层面，gorm老框架需要手动区分reader和writer，新框架就不需要区分了，在框架内不做了分离，业务不感知。在系统层面，mysql又做了一层代理，写请求路由到代理的3306端口，读请求路由到3307端口。虽然增加了一层代理，但是分库分表是无感知的，且可以更好地接入k8s集群</div>2022-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/cd/3890be04.jpg" width="30px"><span>小川</span> 👍（0） 💬（0）<div>数据库的查询，是不是默认不带事物的？</div>2021-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ae/8b/43ce01ca.jpg" width="30px"><span>ezekiel</span> 👍（0） 💬（1）<div>Cache Aside模式，如果在缓存和数据库里都加上数据的版本号，是否可以避免更新的时候产生脏数据的问题？或者这样的模式会不会有什么问题？</div>2021-02-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ajNVdqHZLLBllicLBj61g1ibmCeWzLYpQYEteTOtAAAypoIg6CD19ibXQBbM09VsME9Ta1G8ubwk0ibjiacItavibaeg/132" width="30px"><span>seg-上海</span> 👍（0） 💬（0）<div>业务qps一般到什么水平就要读写分离了，上来就设计成读写分离可以吗</div>2020-05-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Cib5umA0W17N9pichI08pnrXAExdbyh7AVzH4nEhD6KN3FXuELk4LJJuqUPPD7xmIy9nq5Hjbgnzic7sVZG5BKiaUQ/132" width="30px"><span>被过去推开</span> 👍（0） 💬（0）<div>公司的业务量不是很大，采用了两个数据源，用aop的方式动态切换数据源</div>2020-04-26</li><br/><li><img src="" width="30px"><span>王杰</span> 👍（0） 💬（0）<div>一般是数据分片，加读写分离，对于那些实时要用的放到同一个数据库事务中去，相当于部分的读也是用的主库</div>2020-04-18</li><br/>
</ul>