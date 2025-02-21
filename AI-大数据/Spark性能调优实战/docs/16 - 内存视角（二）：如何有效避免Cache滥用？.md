你好，我是吴磊。

在Spark的应用开发中，有效利用Cache往往能大幅提升执行性能。

但某一天，有位同学却和我说，自己加了Cache之后，执行性能反而变差了。仔细看了这位同学的代码之后，我吓了一跳。代码中充斥着大量的`.cache`，无论是RDD，还是DataFrame，但凡有分布式数据集的地方，后面几乎都跟着个`.cache`。显然，Cache滥用是执行性能变差的始作俑者。

实际上，在有些场景中，Cache是灵丹妙药，而在另一些场合，大肆使用Cache却成了饮鸩止渴。那Cache到底该在什么时候用、怎么用，都有哪些注意事项呢？今天这一讲，我们先一起回顾Cache的工作原理，再来回答这些问题。

## Cache的工作原理

在[存储系统](https://time.geekbang.org/column/article/355081)那一讲，我们其实介绍过RDD的缓存过程，只不过当时的视角是以MemoryStore为中心，目的在于理解存储系统的工作原理，今天咱们把重点重新聚焦到缓存上来。

Spark的Cache机制主要有3个方面需要我们掌握，它们分别是：

- 缓存的存储级别：它限定了数据缓存的存储介质，如内存、磁盘等
- 缓存的计算过程：从RDD展开到分片以Block的形式，存储于内存或磁盘的过程
- 缓存的销毁过程：缓存数据以主动或是被动的方式，被驱逐出内存或是磁盘的过程
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/22/8e/67/afb412fb.jpg" width="30px"><span>Sam</span> 👍（15） 💬（2）<div>老师，您好！~我的知识盲区突现了：
对于老师的第三问，自己摸不着头脑，看老师和同学的回答也看得蒙蒙，感觉缺少了某部分基础知识，但又不知道从哪里补，这种感觉很痛苦~

希望老师能指点迷津。</div>2021-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/22/f04cea4c.jpg" width="30px"><span>Fendora范东_</span> 👍（7） 💬（1）<div>1.M_A_D在storage memory可用的情况下，缓存block过程和M_O过程一样，区别在于storage_memory不够情况下的处理。M_O是通过LRU来驱逐block来获取可用缓存;而M_A_D是通过落盘，落盘流程就是把unroll出来的block，通过putBytes()方法直接进行落盘，BlockID为落盘文件名，便于查找。
2.在M_O模式下，为啥不驱逐同一个RDD的memoryentry。我理解，当前RDD正在缓存，那它马上被用到的概率是最高的(类似LRU思想)，如果它里面memoryentry被驱逐，那需要用的时候又要重新计算，白白增加耗时。
3.在analyzed阶段匹配，我记得是因为在analyzer生效阶段会把unresolverelation直接解析为InMemoryRelation。这样在在Optimizer阶段有些优化规则就省略了，避免应用规则浪费时间</div>2021-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/22/f04cea4c.jpg" width="30px"><span>Fendora范东_</span> 👍（6） 💬（1）<div>还有几个疑问，
1.驱逐memoryentry的时候，图上两个打叉，我理解如果驱逐一个内存还是不够，就驱逐了两个？
2.linkedhashmap是怎样区分不同RDD的block的，k是blockid，v是memoryentry。没看到所属RDD的属性
3.自己设计cacheManager没啥更好想法，求磊哥提示下。。。我理解这个东西放在最前面比较合理，后面针对缓存的逻辑计划进一步应用或省略优化规则</div>2021-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/4e/29/adcb78e7.jpg" width="30px"><span>静心</span> 👍（5） 💬（1）<div>老师，RDD调用 Cache 的时候，文中讲到我们要把待缓存数据赋值给一个变量，然后基于这个变量做后续的etl，能够防止cache miss问题，但是我看了一下rdd cache源码，返回值就是原来的RDD，只是更改了rdd的storageLevel为MEMORY_ONLY（rdd默认缓存级别），所以rdd 调用cache后赋值到一个新变量再做etl 与 不赋值而是基于原有RDD进行etl应该不会有cache miss问题吧，有点不太理解，望老师解疑，谢谢。</div>2021-05-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI9X140JXPuaDB8PibXpwFWds6mZvg1w7THkyB6NjBkP7x4HqSk2wuUvcmDb9O2l0fCkxvB3ibL0L2A/132" width="30px"><span>科学养牛</span> 👍（4） 💬（2）<div>老师，你的意思是调用.cache之后，需要马上接一个action算子吗？
如果我不马上接action算子，只在最后调用一个action算子，比如saveAsTable，那在之前就算用了cachedRdd这个变量多次缓存也不起效果是吗？</div>2021-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（2） 💬（1）<div>1. 第一题，在前面广播变量那一节的课后思考题已经回答过整个MemoryStore和DiskStore的缓存过程了哈哈
2. 因为同一个RDD的Block大概率在接下来就会被用到，因为本身要缓存的就是同一个RDD的其他Block，如果不这样做的话，很可能要缓存的Block被缓存到内存了，却发现要用的Block却被驱逐出内存了
3. 这是我自己的猜测不知道对不对哈哈：像第二种方式那样在数据集上做了一些处理之后进行cache，后续Cache Manager如果采用根据 Optimized Logical Plan 的方式来进行优化的话，那后面所有用到df这个Dataframe的地方，Spark都要解析对应的Optimized Logical Plan和我们之前cache的那个是否相同，这将会非常不可控。而且由于RDD&#47;Dataset&#47;Dataframe的不可变性，我们每次在对数据集进行处理之后，其实都应该养成将其赋值给一个新变量的习惯。</div>2021-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/26/db/27724a6f.jpg" width="30px"><span>辰</span> 👍（2） 💬（1）<div>以及缓存的完全物化的物化是指什么意思呢</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/26/db/27724a6f.jpg" width="30px"><span>辰</span> 👍（2） 💬（1）<div>老师，文中的三种cache方式，我看都没有调用action算子（排除第二种不会cache的场景），是不是意味着都不会缓存落盘的操作</div>2021-04-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJL0JbAgWUIbJedKq4zsohMNj9AVyknp1AaVjLV6bRFDn00sOCBBRPzQAvCoIGWdAfWrJhxSV2M5g/132" width="30px"><span>阳台</span> 👍（1） 💬（2）<div>请问一下老师，什么是同属一个Rdd数据？第一节里面的一个土豆是一个rdd数据，还是三个土豆在一起被称为一个rdd数据</div>2021-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/93/2d3d5868.jpg" width="30px"><span>Jay</span> 👍（1） 💬（4）<div>老师，如果用的是RDD，文中的“Cache方式二”是不是就没有问题了？ </div>2021-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/4b/16ea3997.jpg" width="30px"><span>tiankonghewo</span> 👍（0） 💬（1）<div>为什么cache要在action算子之后,再单独启动一个job缓存数据,这样不是重复计算了吗?已经计算一遍了,为什么不利用呢?</div>2021-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d9/e7/45d9e964.jpg" width="30px"><span>Hiway</span> 👍（0） 💬（1）<div>老师，您好。看到你之前的回答“是的，要先用Action算子来触发缓存的计算，让Spark真正把分布式数据集缓存到内存或是磁盘中去。”我对这句话有点疑惑，请问实际工作环境使用cache也是这样的吗？cache完后接一个count用于触发cache计算。然后再继续写业务逻辑吗？
那不是除了cache的开销，还多了一个count计算的开销</div>2021-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/11/20/9f31c4f4.jpg" width="30px"><span>wow_xiaodi</span> 👍（0） 💬（2）<div>老师，您好，有几个问题想问下：
(1)广播变量默认是存储级别是？如果内存不足，是否是存到disk中？
(2)对于memory only模式，采用lru淘汰缓存。那么如果是memory and disk模式，此时如果内存不足，是否先进行lru淘汰呢？
(3)memory and disk文中说到部分内存，部分disk，那么这个存储占比如何去确定呢？</div>2021-08-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIxKpBQJbxHFG9Wjk73WkbqcGeDrjzwjPSDzLlm8C80U9dVmByrrmBa3LmIoCYUW2H3thj5VfMvGQ/132" width="30px"><span>jasonde</span> 👍（0） 💬（0）<div>memory only 是不是cache， memory and disk 是persist（） 呢</div>2024-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/be/e9/9d597e04.jpg" width="30px"><span>豆豆酱</span> 👍（0） 💬（0）<div>有一个问题哈。先放在ValuesHolder 的数据结构里，然后转换为 MemoryEntry，这其中没有内存开销。想知道transfer这一步的意义是什么呀？有什么必要多这一步呀？求老师解答一下小小疑惑</div>2023-04-25</li><br/><li><img src="" width="30px"><span>Horse_Lion</span> 👍（0） 💬（0）<div>老师，在对spark sql查询结果进行缓存时，发现一个问题，数据操作步骤如下
1:从a表b表c表进行联合查询，并将结果进行缓存
2:将缓存的数据追加写入到a表
3:再将缓存的数据写入到b表

按照我的理解 第二步和第三步写入的数据应该是相同，第二步追加写入触发第一步缓存生效，第三步直接使用缓存的结果

但最终结果是第二步输出到a表的数据和第三步输出到b表的数据 完全没有交集

这是什么原因？难道是因为a表是数据缓存的来源，我又修改了a表数据，缓存被强制清除掉了，导致第三步只能读磁盘重新计算</div>2022-10-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/1hp9kzzuLUVHzmmddIPIO2OgUWr1ibJRr8cMoB7K0fwx8Vmn34L8yN2NoYUtgNicfPGaXKF02pQ2huXd59r2I0kw/132" width="30px"><span>三胖</span> 👍（0） 💬（0）<div>老师，如果缓存级别是MEMORY_ONLY，然后多个rdd抢占资源，结果导致各个rdd的缓存比例都没有达到100%，说明缓存的数据是缺失的，下游要用到缓存的rdd，但是拿到的是有缺失的数据，这还能用吗</div>2022-08-19</li><br/><li><img src="" width="30px"><span>Geek_73cee2</span> 👍（0） 💬（0）<div>老师 您说的这些内存是整个集群的 而不是单个的executors内有多少内存吗  比如storage memory usermemory  还有呢个resever m 300m那个</div>2022-06-12</li><br/>
</ul>