你好，我是唐聪。

在前面的课程里，我和你多次提到过etcd数据存储在boltdb。那么boltdb是如何组织你的key-value数据的呢？当你读写一个key时，boltdb是如何工作的？

今天我将通过一个写请求在boltdb中执行的简要流程，分析其背后的boltdb的磁盘文件布局，帮助你了解page、node、bucket等核心数据结构的原理与作用，搞懂boltdb基于B+ tree、各类page实现查找、更新、事务提交的原理，让你明白etcd为什么适合读多写少的场景。

## boltdb磁盘布局

在介绍一个put写请求在boltdb中执行原理前，我先给你从整体上介绍下平时你所看到的etcd db文件的磁盘布局，让你了解下db文件的物理存储结构。

boltdb文件指的是你etcd数据目录下的member/snap/db的文件， etcd的key-value、lease、meta、member、cluster、auth等所有数据存储在其中。etcd启动的时候，会通过mmap机制将db文件映射到内存，后续可从内存中快速读取文件中的数据。写请求通过fwrite和fdatasync来写入、持久化数据到磁盘。

![](https://static001.geekbang.org/resource/image/a6/41/a6086a069a2cf52b38d60716780f2e41.png?wh=1920%2A1131)

上图是我给你画的db文件磁盘布局，从图中的左边部分你可以看到，文件的内容由若干个page组成，一般情况下page size为4KB。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/47/88/0968576d.jpg" width="30px"><span>issac</span> 👍（10） 💬（2）<div>唐聪老师，能把每节课的思考题解答一下吗？觉得都是重点有意思的地方，非常感谢老师的辛苦付出！</div>2021-02-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIVvyFCLRcfoWfiaJt99K0wiabvicWtQaJdSseVA6QqWyxcvN5nd2TgZqiaUACc94bBvPHZTibnfnZfdtQ/132" width="30px"><span>Geek_7d539e</span> 👍（2） 💬（1）<div>事务提交原理 这小节，没有讲清楚单个的客户端事务请求跟批量事务的关系。麻烦老师再放大讲讲下？多谢。老师看着很年轻，造诣确不一般，了不起。</div>2021-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/38/4f89095b.jpg" width="30px"><span>写点啥呢</span> 👍（1） 💬（1）<div>请问下唐老师，文章中“boltdb API”一节的示例代码里，&quot;defer tx.Rollback()&quot;将事务回滚放到defer链里，如果事务正常提交了，这时候defer链再调用Rollback会是什么效果？是不是Rollback报错而我们直接忽略掉？</div>2021-02-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLDUJyeq54fiaXAgF62tNeocO3lHsKT4mygEcNoZLnibg6ONKicMgCgUHSfgW8hrMUXlwpNSzR8MHZwg/132" width="30px"><span>types</span> 👍（0） 💬（3）<div>是key-value数据与consistent index在同一个boltdb事务中更新

请问consistent index 在哪边更新的？</div>2021-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/ae/37b492db.jpg" width="30px"><span>唐聪</span> 👍（17） 💬（0）<div>文中提到的bbolt是etcd社区基于boltdb fork的一个版本，etcd社区负责维护此版本，原因是boltdb作者认为boltdb已经足够成熟稳定，经过了大规模生产环境检验，新特性和优化点合入会对boltdb稳定性造成一定的影响，个人没更多时间再投入到boltdb上，因此boltdb项目变成archived状态</div>2021-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/39/85/c6110f83.jpg" width="30px"><span>黄骏</span> 👍（1） 💬（0）<div>“下来是两个字节描述 boltdb 的版本号 0x2” ，这里应该是4个字节的版本号吧？</div>2022-11-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/LMxoNLiaufeVaoVdTFFrBfwIVXOx9hJ70Luk9yKshFwjLlSIibjdbtOpj956mjM8RfoEMd7XgNTFfKJBxtDL3iaeQ/132" width="30px"><span>登顶计划</span> 👍（1） 💬（1）<div>老师您好，请问bbolt工具在哪里下载呢?</div>2022-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/73/7e/791d0f5e.jpg" width="30px"><span>菜花</span> 👍（0） 💬（0）<div>第二行的讲解是不是 有问题。或者是哪个图有问题。 有点蒙了。请老师抽空给解答一下。真的。</div>2024-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/e4/04/18933a58.jpg" width="30px"><span>心如水滴</span> 👍（0） 💬（0）<div>课后题：
db文件掉电后，key-value数据落库后应该不能损坏。
通过重启etcd后，boltdb需要重新扫描数据构建meta page索引。</div>2024-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/bd/27/3f349c83.jpg" width="30px"><span>南北</span> 👍（0） 💬（0）<div>开篇的问题，为什么etcd适合读多写少的场景？boltdb使用b+ tree组织数据，读取数据时，访问磁盘的次数有限，内存还有可能做缓存，而写的commit需要rebalance，对磁盘又大量的写入</div>2022-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（0） 💬（1）<div>第二行首先含有一个 4 字节的 magic number(0xED0CDAED)，这个为什么与图里的显示顺序不一样？</div>2022-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/34/ac/96e81b64.jpg" width="30px"><span>Zed</span> 👍（0） 💬（0）<div>etcd里面是批量攒够一定的操作再commit，其中某一项put如果失败也只是打印falt日志，没有其他处理，这种时候不会出现数据不一致的问题吗？</div>2022-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d0/b4/a6c27fd0.jpg" width="30px"><span>John</span> 👍（0） 💬（0）<div>如果写leafpage部分成功部分失败，这种情况怎么处理？</div>2022-08-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/LMxoNLiaufeVaoVdTFFrBfwIVXOx9hJ70Luk9yKshFwjLlSIibjdbtOpj956mjM8RfoEMd7XgNTFfKJBxtDL3iaeQ/132" width="30px"><span>登顶计划</span> 👍（0） 💬（0）<div>老师。下载这个bbolt源码，使用不了，请问可以帮忙指点下不。</div>2022-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/db/50/c2d07bb1.jpg" width="30px"><span>L。</span> 👍（0） 💬（0）<div>老师 一组相同的key 对应一个bucket吗 还是不同的key 对应不同的bucket</div>2022-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/db/50/c2d07bb1.jpg" width="30px"><span>L。</span> 👍（0） 💬（0）<div>老师 请问下 key和bucket有没有什么关系 是不是 key必须放在bucket里</div>2022-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/46/0f/f6cfc659.jpg" width="30px"><span>mckee</span> 👍（0） 💬（0）<div>思考题：
1.db 文件会损坏吗？数据会丢失吗？ 
应该不会，只是meta page没更新？
2.为什么 boltdb 有两个 meta page
备份容灾，如果其中一个meta invalid，就使用另外一个meta</div>2022-05-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLDUJyeq54fiaXAgF62tNeocO3lHsKT4mygEcNoZLnibg6ONKicMgCgUHSfgW8hrMUXlwpNSzR8MHZwg/132" width="30px"><span>types</span> 👍（0） 💬（1）<div>作者你好，meta page中保存的写事务ID，跟consistent index， 以及raft中的applied index之间是什么关系，是否可以解释下</div>2021-10-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLDUJyeq54fiaXAgF62tNeocO3lHsKT4mygEcNoZLnibg6ONKicMgCgUHSfgW8hrMUXlwpNSzR8MHZwg/132" width="30px"><span>types</span> 👍（0） 💬（0）<div>前面涉及到的consistent index，以及写事务批量提交，在这篇文章中没有关联起来。
</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5b/0d/597cfa28.jpg" width="30px"><span>田奇</span> 👍（0） 💬（0）<div>```
type raftLog struct {
	&#47;&#47; storage contains all stable entries since the last snapshot.
	storage Storage

	&#47;&#47; unstable contains all unstable entries and snapshot.
	&#47;&#47; they will be saved into storage.
	unstable unstable

	&#47;&#47; committed is the highest log position that is known to be in
	&#47;&#47; stable storage on a quorum of nodes.
	committed uint64
	&#47;&#47; applied is the highest log position that the application has
	&#47;&#47; been instructed to apply to its state machine.
	&#47;&#47; Invariant: applied &lt;= committed
	applied uint64

	logger Logger

	&#47;&#47; maxNextEntsSize is the maximum number aggregate byte size of the messages
	&#47;&#47; returned from calls to nextEnts.
	maxNextEntsSize uint64
}

```
老师，请问这里的 Storage 接口具体实现在哪里啊，我只看到一个 MemoryStorage 实现了这个接口，但是你说 v3 用boltdb 替换了这个实现，但是我并没有在源码中搜索到这个 boltdb 实现这个接口的地方，很奇怪，具体是哪个包里啊</div>2021-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/76/7d/04c95885.jpg" width="30px"><span>Index</span> 👍（0） 💬（2）<div>请问老师一个问题，在事务提交的时候，有三个持久化的操作，比如只持久化成功一个，后面两个由于崩溃失败了，这样会有数据不一致的问题吗？也就是说所有的持久化能否保证原子性？</div>2021-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/38/4f89095b.jpg" width="30px"><span>写点啥呢</span> 👍（0） 💬（0）<div>请问唐老师，能否介绍下etcd层的事务和boltdb事务之间的对应关系，是否一个etcd的事务过程中在boltdb会产生多个还是一个事务？

如果一个etcd事务对应的是多个boltdb事务，这样能提升上层事务的并发度，通过etcd的buffer读和mvcc锁来保证事务隔离性，是这样的话，当上层etcd事务回滚的话boltdb层该如何做呢？是否是提交新的boltdb事务来回滚bolt数据页呢？

如果etcd和boldb事务是一对一关系的话，可能会涉及到一个etcd事务写入的bolt数据页在事务提交前如何被其它事务访问的问题，请问老师这时候对这种被etcd事务写入数据的内存脏页，它的数据如果需要被其它事务读和写的时候是怎样的机制？

另外09章提到了利用一个mvcc锁来在etcd层实现可串行事务隔离级别，能否有篇章介绍下mvcc锁的具体使用，比如除了可串行之外还有哪些地方用到了，使用的时候锁的粒度如何？

最后想问下etcd的隔离级别，是在哪里配置的，比如mysql可以通过set来配置全局&#47;会话隔离界别那样

问题有点多，麻烦老师指点下。

谢谢</div>2021-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>每个 page  大小不是 4096 个字节吗？为什么 bbolt dump .&#47;db 0 打印出来的字节那么少的</div>2021-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4f/12/e1564440.jpg" width="30px"><span>浮生六记</span> 👍（0） 💬（2）<div>&quot;其次 etcd 通过合并多个写事务请求，通常情况下，是异步机制定时（默认每隔 100ms）将批量事务一次性提交（pending 事务过多才会触发同步提交）， 从而大大提高吞吐量，对应上面简易写事务图的流程三。&quot;

你好，你在03章节有过这段介绍。我有个疑问，异步提交的事务，突然crash的话，如果保证安全写入磁盘呢？是boltdb有什么机制保证吗？我在本章节也没有看到相关内容，就此请教一下。</div>2021-02-20</li><br/>
</ul>