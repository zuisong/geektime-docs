你好，我是徐文浩。

在上节课里，我们一起了解了Spanner的整体架构。Spanner的整个架构并不会让人有什么意外之喜，遵循的仍然是标准的分布式数据库的架构设计，通过对于数据分区、Paxos同步复制等一系列的机制来实现一个超大规模的全球数据库。而对于网络延时，则是选择了对数据分区进行“调度”的策略，让数据尽可能接近读写它的用户，而不是让一份数据在所有的Zone里出现一份。

不过，其实对于Spanner这样的系统来说，**最有挑战的问题**并不是如何调度数据，而是在这样一个“全球”数据库里，如何实现事务。这个问题，也就是我们这节课的主题了。这节课，我会主要带你学习这两个知识点：

- 分布式数据库，会面临哪些我们意想不到的挑战。特别是其中不可靠的网络和不可靠的时钟，会为我们实现事务带来哪些困扰。
- 为什么Megastore这样简单的两阶段事务难以解决这些挑战，而Spanner是如何设计机制，来解决这个问题的。

相信学完了这节课，你能对Spanner面临的时钟误差下的可线性化挑战有所了解，也能对分布式数据库事务的实现有更深一步的掌握。

## Megastore的事务性能怎么样？

我们先来回顾下Megastore的数据库事务实现。在Megastore里，我们只能在单个实体组上实现一阶段事务。一旦需要跨越两个实体组，我们要么放弃事务性，采用Megastore的消息机制，要么我们就要选择两阶段事务。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（8） 💬（0）<div>徐老师好，看直播的时候有时候会卡顿，当我重新连接服务器之后，看的内容不是最新的，而是掉线前看过的内容。如果两个人同时用手机看直播，很可能出现一个人看到的内容落后另一个人看到的内容，那个看到落后内容的人要么会带上耳机，假装别人正在看的直播不存在，要么关掉自己的手机，凑过去和别人一起看。</div>2021-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（4） 💬（0）<div>spanner的设计中通过原子钟和GPS的方式来保证时钟偏移误差压缩在一定范围内，这个技术方式不适合绝大部分的企业，因为成本太高了，而且专门维护这个也需要很多成本和时间的。但是有时候更多就是考虑引入外部的全局事务ID中心，这个方案会更加常见一点。

另外关于前面提到的分布式事务的可线性化问题，这里其实目前在文件系统中有类似的解决方案。文件系统中管理磁盘空间的时候，有几个结构，分别是可用空间，正在申请的空间，延迟释放的空间等等，因为有时候删除数据也需要时间的，但是先把日志记录起来，然后把释放的空间加到延迟释放这里，等到全部搞定了，再放到可用空间里面。

那么在银行转账这个例子中，就是冻结资金，可用资金等来管理了，在转账前，日志先落盘记录起来，然后把可用资金划扣掉，接收方也是先放到冻结资金金额里面等方式来处理，这样的操作，更加精细化一点。</div>2022-02-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（1） 💬（1）<div>世界杯期间A和B在赌球，A已经看到结果说“给钱，给钱”，B说“扯呢，这不还有两分钟了么”。</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0f/70/f59db672.jpg" width="30px"><span>槑·先生</span> 👍（0） 💬（0）<div>事务加上时钟，好复杂</div>2022-06-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIdnSiabibmLk7teCAGI3p3duEnpfKO3icUriaDjQHXtk3icSZibNH2IAyl0RA85edZY4lehqmy3uguQcUQ/132" width="30px"><span>夏至</span> 👍（0） 💬（0）<div>分布式事物的坑很多，实际应用系统设计基本都是在避免分布式事物的前提下，使用分布式读写提高性能和可用性。</div>2022-02-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（0） 💬（1）<div>既然spanner实现分布式事务也是需要两阶段提交，megastore也是需要两阶段提交，通过原子钟 +GPS 时钟的metastore是不是也能实现同样的效果？</div>2022-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（0）<div>处理时间的问题一致是痛点，其一是时间同步；其二是处理时区的时间。</div>2021-11-22</li><br/>
</ul>