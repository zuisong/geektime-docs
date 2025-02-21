你好，我是王磊，你也可以叫我Ivan。

今天，我想和你聊聊时间的话题。

“时光一去永不回，往事只能回味”，这种咏叹时光飞逝的歌曲，你一定听过很多。但是，在计算机的世界里，时间真的是一去不回吗？还真不一定。

还记得我在[第2讲](https://time.geekbang.org/column/article/272104)提到的TrueTime吗？作为全局时钟的一种实现形式，它是Google通过 GPS和原子钟两种方式混合提供的授时机制，误差可以控制在7毫秒以内。正是在这7毫秒内，时光是可能倒流的。

为什么我们这么关注时间呢？是穿越剧看多了吗？其实，这是因为分布式数据库的很多设计都和时间有关，更确切地说是和全局时钟有关。比如，我们在第2讲提到的线性一致性，它的基础就是全局时钟，还有后面会讲到的多版本并发控制（MVCC）、快照、乐观协议与悲观协议，都和时间有关。

## 常见授时方案

那既然有这么多分布式数据库，授时机制是不是也很多，很复杂呢？其实，要区分授时机制也很简单，抓住三个要素就可以了。

1. 时间源：单个还是多个
2. 使用的时钟类型：物理时钟还是混合逻辑时钟
3. 授时点：一个还是多个

根据排列组合，一共产生了8种可能性，其中NTP（Network Time Protocol）误差大，也不能保证单调递增，所以就没有单独使用NTP的产品；还有一些方案在实践中则是不适用的（N/A）。因此常见的方案主要只有4类，我画了张表格，总结了一下。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/b7/b518912b.jpg" width="30px"><span>KayGuoWhu</span> 👍（15） 💬（1）<div>全局时钟的目的是，生成全局唯一的时间戳。和全局唯一ID的区别和作用，有什么差异？</div>2021-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fa/fd/3a6d013a.jpg" width="30px"><span>朱海昆</span> 👍（11） 💬（1）<div>工作中分布式数据库落地的还是相对少。目前项目各种分布式服务，一般都依赖于一个序列号生成器，一般采用雪花或者雪花变种的一些算法实现。为了保证序列号的唯一或者进一步保证递增，依赖于时钟的同步。现在的做法一般都是结合业务场景，对时钟进行一定的校验，同时对于时钟回拨做一些容错等处理解决问题。
目前主流还是用应用层的方案来解决分布式的各种问题，如果将来分布式数据库成熟了，应用解决方案会大大简化。</div>2020-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/13/e103a6e3.jpg" width="30px"><span>扩散性百万咸面包</span> 👍（9） 💬（2）<div>老师能不能再多解释一下关于多时间源的意思？
１. 我理解多授时点应该是指当前集群有多个可以获取时间的服务器。TiDB的PD是通过集群化来做到高可用的，那么这为什么还被归于单授时点呢？
2. 多时间源怎么理解？文中提到Spanner是GPS＋物理时钟，是说最终的时间计算会通过这２个指标计算的意思吗？如果是单时间源的话，获取的时间只取决于一个因素？</div>2020-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/05/fc/bceb3f2b.jpg" width="30px"><span>开心哥</span> 👍（8） 💬（1）<div>从牛顿力学进入爱因斯坦的相相对论时空！</div>2020-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（5） 💬（1）<div>hlc判断大小是先 高位，再低位，判断的时候本地时间可以忽略吧？</div>2020-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b2/5a/574f5bb0.jpg" width="30px"><span>Lukia</span> 👍（3） 💬（1）<div>“103 到 106 的“可分配时间窗口”，在这个时间窗口内 PD 可以使用系统的物理时间作为高位，拼接自己在内存中累加的逻辑时间，对外分配时间戳。 ” 如果主PD在104发生了故障，切换新主PD之后岂不是105和106的时间窗口都不可用了？</div>2020-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ea/32/1fd102ec.jpg" width="30px"><span>真名不叫黄金</span> 👍（2） 💬（1）<div>感谢老师分享～
顺便说下我对Spanner的理解:
Spanner解决True Time回拨的问题，应该是使用等待～ True Time会返回一个时间区间，保证真实时间是在这个区间内的，那么Spanner会等待这个时间过去，以此保证时钟不会回拨</div>2020-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/71/3d/da8dc880.jpg" width="30px"><span>游弋云端</span> 👍（0） 💬（1）<div>期待老师后续的时钟应用场景恩讲解！</div>2020-08-20</li><br/><li><img src="" width="30px"><span>myrfy</span> 👍（0） 💬（1）<div>时间决定了数据库系统看到的事件发生顺序。对于对同一条记录进行操作的oplog在不同节点之间复制，然后在不同节点apply的时候，决定了谁在谁之前操作</div>2020-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e9/116f1dee.jpg" width="30px"><span>wy</span> 👍（5） 💬（0）<div>单体数据库时代,我们一般都会忽略时间问题，因为即使时间是错的，但是起码它是递增的。但是在分布式数据库中，多个分片可能分布在不同的机房里面，这些机房甚至可能在不同的国家，可能会出现时间倒退的现象，对于分布式数据库的数据一致性的实现来说是影响很大的</div>2021-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/64/36/f14efbe7.jpg" width="30px"><span>Tzen</span> 👍（2） 💬（0）<div>老师，TiDB的TSO时间窗口tso-save-interval默认值好像是3秒</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/44/3c/8bb9e8b4.jpg" width="30px"><span>Mr.Tree</span> 👍（1） 💬（0）<div>全局时钟是保证分布式数据库强一致性必不可少的条件，事务高并发时在没有全局时钟确定唯一并且先后的顺序，数据的强一致性会被打破</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8d/0e/1f49ade9.jpg" width="30px"><span>海鲨数据库架构师_曾院士</span> 👍（1） 💬（0）<div>全局时间是解决在分布式环境下DML操作顺序，并且是唯一性。

全球化部暑时间会成为24个时区。

若统一使用格林唯志时间，那么是不是简单多了？</div>2021-05-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJLxEbhSEziblPNVkr9XFIAzPCib0TQvBxHYwiaKiaib7ExZ8dmUWyqWoibSedACTHCf52INMib80ic92G6wQ/132" width="30px"><span>刘章</span> 👍（0） 💬（0）<div>看的比较费劲，有没有分布式数据库入门级别的教程推荐</div>2022-09-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/WxLKJlXCibwqO92vB8XTicLQiahrhuUEqP7yT9dearZxLzbia7oMdsLmon5J4LJyTfIWchHY3bKfibm1lS1aZarZs4Q/132" width="30px"><span>jie</span> 👍（0） 💬（1）<div>hlc 是矢量时钟吗</div>2022-05-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIKoEicqUZTJly55qoUXRmK4wia7YbnibsMncJaO6tKgKAQNJRfpMsibvfeiaukIibsCsuaic8QjQ3gOoTGA/132" width="30px"><span>张可夫斯基</span> 👍（0） 💬（0）<div>----原文
这三个值分别是 0、1 和 10。按照规则取最大值，所以 B2 的 L 值是 10，也就是 A1 的 L 值，而 C 值就在 A1 的 C 值上加 1，最终 B2 的 HLC 就是 (10,1)。

---问题
    （这里如果B1的L值是最大的，那么B2的L值取B1的L值，B2的C值是在B1的C值上加1吗?（谁的L值大就以谁为基准？</div>2022-03-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIKoEicqUZTJly55qoUXRmK4wia7YbnibsMncJaO6tKgKAQNJRfpMsibvfeiaukIibsCsuaic8QjQ3gOoTGA/132" width="30px"><span>张可夫斯基</span> 👍（0） 💬（1）<div>问题：如果PD写ETCD延迟时间大于窗口大小，PD将最大窗口时间（当前时间+窗口大小）写入ETCD后，PD的系统时间又大于了最大窗口时间，那么PD是不是又要重新申请写入？如果这种延迟一直存在，那就会一直生成不了ID。</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/4e/88/791d0f5e.jpg" width="30px"><span>lei</span> 👍（0） 💬（0）<div>理论性好强，但都是偏OLTP系统，至于OLAP还要自己消化下。有没有交流群，有的话希望加下。或者组织一个，VX：aacc6688521</div>2021-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f2/66/b16f9ca9.jpg" width="30px"><span>南国</span> 👍（0） 💬（1）<div>才疏学浅，感觉时间对于分布式的影响就是事件的顺序了。这也许也是分布式关系型数据库这么看重全局时钟（跨节点的事务需要区分多节点并发事件的顺序），而大多数nosql（我知道的大多数）却不需要的原因吧。</div>2020-08-19</li><br/>
</ul>