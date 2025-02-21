你好，我是徐文浩。

在上一讲里，我们已经了解了Bigtable的整体架构，知道作为一个分布式数据系统，里面“分布式”的部分是怎么设计的了。那么，今天我就带你一起来详细深入到Bigtable的“数据”部分里，去看看它是怎么回事儿。而且今天的这一讲，我们会“超越”Bigtable的论文，深入到MemTable和SSTable的具体实现。搞清楚这些问题，不仅对你学懂Bigtable不可或缺，也对你深入理解计算机底层原理有所帮助。

在学习完这一讲之后，我希望你能掌握好这两个知识点：

- 首先，自然是Bigtable本身的单个Tablet是如何提供服务的。
- 其次，是我们如何利用好硬件特性，以及合理的算法和数据结构，让单个Tablet提供足够强劲的性能。

当你把这两个知识点掌握清楚了，你就能很容易学会怎么实现一个单机存储引擎，并且能够对硬件性能、算法与数据结构的实际应用有一些心得。

## Bigtable的读写操作

在讲解Bigtable底层是怎么读写数据之前，我们先来看一看，Bigtable读写数据的API长什么样子。下面是论文里面提供的一段代码：

```c++
// Open the table
Table *T = OpenOrDie("/Bigtable/web/webtable");

// Write a new anchor and delete and old anchor
RowMutation r1(T, "com.cnn.www");
r1.Set("anchor:www.c-span.org", "CNN")
r1.Delete("anchor:www.abc.com");
Operation op;
Apply(&op, &r1);
```
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（21） 💬（1）<div>徐老师好，这一讲解决了我在上一讲产生的好几个疑问，第一是随机写和顺序写为什么性能一样，第二是随机读为什么比写操作慢一个数量级。通过对dblevel-handbook的学习，我对MemTable和SSTable也有了更深的认识。

回答老师的问题，我们可以先看看读写操作在哪些地方会涉及SSTable。在向Bigtable写入数据时，会先写内存MemTable，MemTable增长到一定规模后，将它持久化成一个不可变的SSTable，这个过程是Minor Compaction的一部分，Bigtable在后台合并SSTable，对每一个Key只保留最近若干个版本的Value，这个过程被成为Major Compaction。在从BigTable读取数据时，先从MemTable中读取，读不到就从SSTable中读。为了加快SSTable的读取，BigTable实现了Scan Cache和Block Cache，这些缓存是针对单个SSTable，而不是把好几个SSTable混在一起缓存。因为不同的SSTable是独立的，也就为单独删除一个SSTable提供了可能性。一个Tablet包含哪些SSTable记录在METADATA表中，也就能做到先标记后删除的方式。先标记后删除可以让实际的删除操作在后台执行，加快前台操作的响应时间。</div>2021-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a2/fb/94af9cf1.jpg" width="30px"><span>Alex</span> 👍（3） 💬（1）<div>因为数据连续存储，删除数据就需要先打标记，再Major Compaction时忽略掉原SSTable里删除标记的数据生成新的SSTable</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4b/83/18bf997c.jpg" width="30px"><span>天空小白菜</span> 👍（2） 💬（0）<div>先回答老师的问题，标记本质上也是数据的一个版本，读数据时默认是读最新版本，如果读到的最新版本是删除标记，那么就直接返回数据不存在即可。数据的真正擦除可以在compaction的时候实现。

提个问题，bigtable支持单行的事务，由于一行可能涉及到多个列族，而不同列族的数据又是存储在不同的gfs文件中，那么单行事物就有意味着对多个tablet server请求的原子性，请问bigtable在这个地方是如何实现的。</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/10/c6/5e7f3148.jpg" width="30px"><span>Somnus💫</span> 👍（1） 💬（0）<div>收获满满，看下来其实大多都是计算机中非常常规的思想，学习了操作系统，但是Google能将这些东西落到应用生产，真的很牛！不管是操作系统的设计，还是分布式解决一些问题，点到面，其实本质思想都是相同的，关键是怎么用起来。</div>2021-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（1） 💬（0）<div>收获满满</div>2021-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/22/b2/83847bb5.jpg" width="30px"><span>YaoQi</span> 👍（0） 💬（0）<div>老师, 看完有个疑问: 磁盘的顺序读写和随机读写是文件系统控制的, 怎么保证写文件是顺序写呢?</div>2023-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/c1/2dde6700.jpg" width="30px"><span>密码123456</span> 👍（0） 💬（0）<div>首先，为什么会出现过期的SSTable？因为多个SSTable已经合并好了，才会出现。既然新的SStable已经生成，那么老的自然要标记出来，并把它清理。</div>2023-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/20/b7/bdb3bcf0.jpg" width="30px"><span>Eternal</span> 👍（0） 💬（0）<div>老师的文章开门见山告诉你要点，学会要点的收益，文风很nice</div>2023-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/15/8e/ae3304c2.jpg" width="30px"><span>demo</span> 👍（0） 💬（0）<div>数据的真正删除是在合并SSTable也就是进行多路归并的时候进行的,这样还是顺序读写,性能高,如果不标记逻辑删除而使用物理删除,那就是随机硬盘的随机读写了,性能会非常差.</div>2022-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>老师， 能重点解读一下 tablet 的扩容之后的迁移吗？</div>2022-01-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（0） 💬（0）<div>因为sstable是不可变的，如果里面数据被标记为可以清理，标记就是以后不读取这个sstable ，因为是不可变，也不会像处理引用那种复杂关系，清理线程不会影响工作线程。</div>2021-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bb/cc/fac12364.jpg" width="30px"><span>xxx</span> 👍（0） 💬（0）<div>因为我们查询一条数据实际上是要结合memTable + SSTable的，所有地方都过完了才知道一条记录的最新状态，因此标记这条记录被删除就能够生效。</div>2021-11-26</li><br/><li><img src="" width="30px"><span>Geek_88604f</span> 👍（0） 💬（2）<div>“当 MemTable 的大小超出阈值之后，我们会遍历 MemTable“，请教老师，这里为啥要遍历?</div>2021-10-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKhuGLVRYZibOTfMumk53Wn8Q0Rkg0o6DzTicbibCq42lWQoZ8lFeQvicaXuZa7dYsr9URMrtpXMVDDww/132" width="30px"><span>hello</span> 👍（0） 💬（0）<div>如果不是先标记后删除，那删除就变成一个随机访问磁盘的操作，不管是HDD还是SSD，随机访问的性能都比顺序访问的性能差很多。而先标记后删除，是一个顺序写盘的操作，极大的提升了性能。</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/4e/be2b206b.jpg" width="30px"><span>吴小智</span> 👍（0） 💬（1）<div>想请教老师，Tablet server 是如何处理 split 的，会做些什么，流程是哪些？如何保证与 metadata 的数据一致？</div>2021-10-11</li><br/>
</ul>