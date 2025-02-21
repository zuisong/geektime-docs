你好，我是王磊。

从第18讲，我们开始介绍查询过程中全部重要节点的相关技术，从并行框架到查询执行引擎，再从关联运算符到行式和列式存储。今天这一讲我们面临最后的一个步骤，直接和磁盘打交道，实现最终的数据存储，这就是存储引擎。

## RUM猜想

说到数据存储，我相信很多人都有一种直觉，那就是读写两种操作的优化在很多时候是互斥的。

我们可以想一下，数据以什么形式存储，可以实现最快的写入速度？答案肯定是按照顺序写入，每次新增数据都追加在文件尾部，因为这样物理磁盘的磁头移动距离最小。

但这种方式对于读取显然是不友好的，因为没有任何有意义的数据结构做辅助，读操作必须从头到尾扫描文件。反过来，如果要实现更高效的读取，就要设计更复杂的数据结构，那么写入的速度当然就降低了，同时在存储空间上也会有额外的要求。

2016年的一篇论文将我们这种朴素的理解提升到理论层面，这就是RUM猜想。RUM猜想来自论文“[Designing Access Methods: The RUM Conjecture](https://stratos.seas.harvard.edu/files/stratos/files/rum.pdf)”（Manos Athanassoulis et al.(2016)），同时被SIGMOD和EDBT收录。它说的是，对任何数据结构来说，在Read Overhead（读）、Update Overhead（写） 和 Memory or Storage Overhead（存储） 中，同时优化两项时，需要以另一项劣化作为代价。论文用一幅图展示了常见数据结构在这三个优化方向中的位置，这里我摘录下来便于你理解。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/13/e103a6e3.jpg" width="30px"><span>扩散性百万咸面包</span> 👍（12） 💬（1）<div>思考题：
使用Bloom Filter的改造版，现在不用来判断某个key是否不存在，而判断某个key的前缀是否不存在。比如说我要查300-000 到 300-999的区间，那么他们拥有共同前缀300，我只要判断这个前缀是不是在当前SSTable里即可。</div>2020-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（3） 💬（2）<div>课后题：
这样问，那就一定是可以了。但很遗憾，能力有限想不到。scan了的话，如果是常规的行式存储,bf起不到作用，毕竟边界不存在不等于边界内部不存在。

22讲下来的感觉:
有种搭建空中楼阁的感觉,费力还容易忘。这篇专栏前边,其实最好有篇实战做铺垫,比如tidb。两相验证虚实结合才能学得扎实。</div>2020-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d0/15/c5dc2b0d.jpg" width="30px"><span>James</span> 👍（2） 💬（3）<div>想问下老师，就是我查一个键值对的时候，对于L1 往后的层级我是怎么找到对应的key的，我看图中画的是很多个区间，是去顺序遍历一遍这些区间，然后去对应的区间找元素吗（在区间内是通过调表算法来找元素的），还是说用二分法这类的算法来找到是哪个区间呢。PS:这个区间是可以不连续的吧（只要不重合就行）,比如[a,b) [e,f]
</div>2021-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/54/9c214885.jpg" width="30px"><span>kylexy_0817</span> 👍（1） 💬（1）<div>NewSQL的存储数据结构和策略和ES的十分相似。ES确实不是数据库，它不具备数据库应有的特性，例如事务等。之前的留言不严谨😄</div>2020-11-11</li><br/><li><img src="" width="30px"><span>licl1008</span> 👍（1） 💬（1）<div>想问一下 写放大和空间放大具体有啥区别 写得多了不是磁盘空间就占用更多了吗？</div>2020-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（1） 💬（1）<div>即使不是前缀相同，范围查询也可以一个一个key去尝试，bf是内存操作，还是比磁盘快吧</div>2020-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/84/28b633bd.jpg" width="30px"><span>sanstyle</span> 👍（0） 💬（1）<div>L0 中的 key 是交叉的，所以读取 L0 的所有 SSTable 写入 L1，来保证 L1 开始的 SSTable 都是 key 不重叠的。
在 L1 划分边界的时候，[e, k) 里面是有交叉 key 的，重新划分为 [e, f), [f, k)，怎么保证这两个 SSTable 不交叉？</div>2021-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/32/1c/3e3cdad2.jpg" width="30px"><span>Jackson</span> 👍（0） 💬（1）<div>CockroachDB 也推出了自己的存储引擎 Pebble，主要目的是解决工程问题，包括解决 CGo barrier 问题和避免 Rust 功能膨胀带来的变更风险。—— Rust应该是Rocksdb吧？笔误？</div>2021-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6c/b5/32374f93.jpg" width="30px"><span>可怜大灰狼</span> 👍（0） 💬（1）<div>数据块里是按照顺序存储了很多条数据。我想对数据块建立一级布隆过滤器实例，这样scan定位起始和终止对应的数据块，应该能提速不少。
如果把数据块按照大小分级，类似LSM的level层那样。是不是会更快些？</div>2020-09-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（4） 💬（0）<div>为什么RUM是个猜想而不是个定论呢？这东西第一眼看上去好像CAP理论，不过CAP已经被证明了</div>2020-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（1） 💬（0）<div>lsm最核心的是顺序写特性，即使写放大和b+一样大，因为顺序写比随机写还是快很多。写放大和空间放大比较影响ssd的寿命。</div>2020-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/a2/55/1092ebb8.jpg" width="30px"><span>边城路远</span> 👍（0） 💬（0）<div>老师，有个地方有点问题，应该是&quot;Delta Tree 采用了类似 B+ Tree 的结构&quot;</div>2021-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e9/116f1dee.jpg" width="30px"><span>wy</span> 👍（0） 💬（0）<div>如果以后固态硬盘成本降下来，都是用固态硬盘的话，lsmtree的作用是不是就不大了</div>2021-01-30</li><br/>
</ul>