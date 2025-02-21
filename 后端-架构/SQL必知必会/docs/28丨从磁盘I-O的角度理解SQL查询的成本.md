在开始今天的内容前，我们先来回忆一下之前的内容。

数据库存储的基本单位是页，对于一棵B+树的索引来说，是先从根节点找到叶子节点，也就是先查找数据行所在的页，再将页读入到内存中，在内存中对页的记录进行查找，从而得到想要数据。你看，虽然我们想要查找的，只是一行记录，但是对于磁盘I/O来说却需要加载一页的信息，因为页是最小的存储单位。

那么对于数据库来说，如果我们想要查找多行记录，查询时间是否会成倍地提升呢？其实数据库会采用缓冲池的方式提升页的查找效率。

为了更好地理解SQL查询效率是怎么一回事，今天我们就来看看磁盘I/O是如何加载数据的。

这部分的内容主要包括以下几个部分：

1. 数据库的缓冲池在数据库中起到了怎样的作用？如果我们对缓冲池内的数据进行更新，数据会直接更新到磁盘上吗？
2. 对数据页进行加载都有哪些方式呢？
3. 如何查看一条SQL语句需要在缓冲池中进行加载的页的数量呢？

## 数据库缓冲池

磁盘I/O需要消耗的时间很多，而在内存中进行操作，效率则会高很多，为了能让数据表或者索引中的数据随时被我们所用，DBMS会申请占用内存来作为数据缓冲池，这样做的好处是可以让磁盘活动最小化，从而减少与磁盘直接进行I/O的时间。要知道，这种策略对提升SQL语句的查询性能来说至关重要。如果索引的数据在缓冲池里，那么访问的成本就会降低很多。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/7c/8ef14715.jpg" width="30px"><span>NIXUS</span> 👍（83） 💬（7）<div>请问下老师，缓冲池和查询缓存是一个东西吗？</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/46/d0/6bafd7d4.jpg" width="30px"><span>DZ</span> 👍（54） 💬（2）<div>顺序读的页面平均加载效率更高是因为顺序读更贴合存储介质的物理特性，即一次顺序读取一批相邻物理块的效率，大于多次随机访问不连续的物理块的效率。

缓冲池机制和页面加载方式是计算机体系结构的经典方式，首先必须承认两个客观事实，一是资源有限，二是时间有限。从硬盘到内存再到CPU缓存，价格和效率永远存在矛盾，只能通过多级缓存的形式，将更贵的资源留给更热的数据。</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/eb/b8/22065888.jpg" width="30px"><span>小年</span> 👍（11） 💬（1）<div>老师，不止可否在哪一期讲一讲面试的时候常考的一些SQL相关的内容呀？感觉这些索引深入了以后面试不太会涉及到，抱歉功利了点因为最近在秋招各种面试，担心看的太深了反而暂时用不到...</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4d/5e/c5c62933.jpg" width="30px"><span>lmtoo</span> 👍（7） 💬（4）<div>innodb_buffer_pool_size是缓存池总大小吗？如果缓存池个数大于1，那每个缓冲池大小是不是innodb_buffer_pool_size&#47;innodb_buffer_pool_instances?</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/1a/20977779.jpg" width="30px"><span>峻铭</span> 👍（6） 💬（3）<div>SELECT comment_id, product_id, comment_text, user_id FROM product_comment WHERE comment_id = 900001;
SELECT comment_id, product_id, comment_text, user_id FROM product_comment WHERE comment_id BETWEEN 900001 AND 900100;
这两句查询的last_query_cost都是4.724，说明这不是页
官网：https:&#47;&#47;dev.mysql.com&#47;doc&#47;refman&#47;8.0&#47;en&#47;server-status-variables.html

The total cost of the last compiled query as computed by the query optimizer. This is useful for comparing the cost of different query plans for the same query. The default value of 0 means that no query has been compiled yet. The default value is 0. Last_query_cost has session scope
对同一个查询语句的不同查询计划的代价进行计较，选择代价最小的。last_query_cost得到的值只是一个查询计划的评分值，不是页

</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2e/74/88c613e0.jpg" width="30px"><span>扶幽</span> 👍（5） 💬（1）<div>是因为磁盘IO时寻道和半圈旋转时间较长吗？</div>2019-11-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/fUDCLLob6DFS8kZcMUfxOc4qQHeQfW4rIMK5Ty2u2AqLemcdhVRw7byx85HrVicSvy5AiabE0YGMj5gVt8ibgrusA/132" width="30px"><span>NO.9</span> 👍（5） 💬（1）<div>老师 你好，请教一个问题，
看完本章前面的部分之后忽然间意识到：
      数据库Down掉之后的Recover，只能是用最新对backup+checkpoint+transaction的log 恢复，就是因为commit的内容还没有从缓冲池写入磁盘。</div>2019-08-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/lfMbV8RibrhFxjILg4550cZiaay64mTh5Zibon64TiaicC8jDMEK7VaXOkllHSpS582Jl1SUHm6Jib2AticVlHibiaBvUOA/132" width="30px"><span>用0和1改变自己</span> 👍（4） 💬（4）<div>1,顺序读取是一种批量读取，读取的数据都是相邻的，所以不需要每一页都进行I&#47;O操作，平均下来就效率更高了。
2.缓存池的刷新机制和许多缓存都是一样的，达到一定数量后进行更新，以达到提升性能都目的。</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/69/bf/58f70a2a.jpg" width="30px"><span>程序员花卷</span> 👍（3） 💬（1）<div>第一个问题
我们的数据在磁盘上是相邻存储的，当我们将数据从磁盘中加载读取到缓冲区的时候，就直接一堆一堆的读取，根本不需要单独的去对某个数据进行I&#47;O的操作，这样效率就会很高，（重点在于数据在磁盘中是相邻存储的）

第二个问题
缓冲池这个东西应该跟计算机组成原理中的高速缓冲区（Cpu Cache)是一个道理的，访问速度比内存快，内存又比磁盘快，CPU在进行数据读取的时候，首先就会去访问Cache，只有当Cache中找不到数据的时候，CPU才会去访问内存，将内存中的数据加载到Cache中，然后在进行访问！这是缓冲区比较快的一方面原因，其次就是有个东西叫做“局部性原理“，包括了时间局部性和空间局部性，在访问数据的时候，这个时间局部性就起作用了，刚刚被访问过的数据，会很快的被访问到，这样CPU花在等待内存访问的时间就大大的缩短了。
我觉得CPU这个访问数据的方式和数据库中访问的方式的原理是一样的！CPU中是CPU Cache,数据库中呢是比如”Redis缓存、MemCache缓存”等！

不知道上述总结是否正确，但是我觉得万变不离其宗，很多东西只是换了一种方式去操作而已，其根本的原理是不变的！有不对的地方，还请老师指正！
</div>2019-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ff/1c/d049776e.jpg" width="30px"><span>wonderq_gk</span> 👍（3） 💬（1）<div>如何把数据放到缓冲池

</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ff/1c/d049776e.jpg" width="30px"><span>wonderq_gk</span> 👍（2） 💬（1）<div>老师，我这里size是32M，为什么也是有8个缓冲池</div>2019-08-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er4HlmmWfWicNmo3x3HKaOwz3ibcicDFlV5xILbILKGFCXbnaLf2fZRARfBdVBC5NhIPmXxaxA0T9Jhg/132" width="30px"><span>Geek_Wison</span> 👍（2） 💬（2）<div>老师，您好。这一节讲的数据库缓存池和新版本MySQL8.0取消的缓存指的是同一个东西吗？
如果是的话，那这节课的内容只在旧版本的mysql成立，在新版本的mysql（取消了缓存的版本）就没用了？</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（1） 💬（1）<div>你能解释下相比于单个页面的随机读，为什么顺序读取时平均一个页面的加载效率会提高吗？
和硬盘的结构有关，硬盘如果读取连续的页，那平均延时和寻道时间平均到每个页面就非常少了，甚至非常接近读取一个页面的效率。

另外，对于今天学习的缓冲池机制和数据页加载的方式，你有什么心得体会吗？
缓冲机制在计算机性能优化随处可见，其理论依据就是计算机的局部性原理，空间局部性，时间局部性。</div>2019-08-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/QD6bf8hkS5dHrabdW7M7Oo9An1Oo3QSxqoySJMDh7GTraxFRX77VZ2HZ13x3R4EVYddIGXicRRDAc7V9z5cLDlA/132" width="30px"><span>爬行的蜗牛</span> 👍（0） 💬（1）<div>1. 因为一次顺序读取的话，单次读取的数据页比较大， 落实到每个页的平均时间比较低，2. checkpoint 的落盘机制印象深刻， 有点类似异步的机制；</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/5e/b8fada94.jpg" width="30px"><span>Ryoma</span> 👍（14） 💬（0）<div>在什么情况下，数据不在缓冲池中，而是在内存中，此时从内存中读取？</div>2020-03-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLLn1y9RSL9JcACGRVkkhkEmjH7z1eiag763CVKwn3Mzb3djbibwbx0fgZqyBpPozGLOicnllSfydEng/132" width="30px"><span>qijj</span> 👍（1） 💬（0）<div>oracle 也是这么处理的吗？</div>2020-04-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJafX5kNYJKpD9czE7pjYJtDWnuHeWQLtkfyAtPYUicbiafAUBvUqSnKTM3bahib1wURcRg2miaOFGnpQ/132" width="30px"><span>jacksnow</span> 👍（1） 💬（0）<div>老师，有个问题请教一下:
如果是两个表进行join操作，比如
select a.*, b.* 
from a join b on a.xxx = b.xxx &#47;&#47; 第一步
where a.id = &#39;xxxx&#39; &#47;&#47; 第二步
第一步是进行数据组装
第二部是进行条件筛选.
我的问题是：
第一步组装数据的意思是不是在磁盘上通过a和b两个表的page页组装成新的page页，并且需要新分配磁盘空间来存储这些新的page页，查询完成之后再将这些page页进行回收？
第二步是否是在新组装出来的page页中通过索引进行查询，并将查到的page load到内存中来？</div>2020-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/55/fe/e8fb06fb.jpg" width="30px"><span>梁</span> 👍（1） 💬（1）<div>我想SSD磁盘在单个页面随机读的效率是否不会比单个页面顺序读的效率差了，SSD寻道时间才0.1ms。</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/55/fe/e8fb06fb.jpg" width="30px"><span>梁</span> 👍（1） 💬（0）<div>我想要是全闪存磁盘的话，就算是单个页面的随机读，效率也不会比顺序读取时平均一个页面的加载效率差，</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/dd/c3/6bb8b410.jpg" width="30px"><span>一米阳光</span> 👍（1） 💬（1）<div>老师，ssd硬盘也存在随机读吗，还是只是减少了机械硬盘的寻道</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>一个查询语句没执行前，怎么判断其执行效率的？（推测至少和索引相关），不过这样可能会不准吧！所以，优化查询语句的时候，才提供了强制走某个索引的情况。还有其他什么判断依据吗？</div>2024-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/85/49/585c69c4.jpg" width="30px"><span>皮特尔</span> 👍（0） 💬（2）<div>SSD不存在顺序读的问题，所以数据库优化有一个简单粗暴的方案：上SSD</div>2021-06-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLg04lnicnUNWXFF2yyk7neSxl7fuI5LBZRYFRDEM8qhyPC3bDwFhz6FLx2NiaGFqa8ZpAz33Thj3cg/132" width="30px"><span>Geek_dd3623</span> 👍（0） 💬（0）<div>缓存池的数据是怎么进行淘汰的呢?  是用 LRU 算法吗</div>2021-04-04</li><br/><li><img src="" width="30px"><span>你的代码有灵魂吗？</span> 👍（0） 💬（0）<div>相比于单个页面的随机读取，顺序读取的页面平均读取时间更少的原因是：每次单个页面随机读取都要花费不少时间用于寻找页面所在的位置，而顺序读取只需在开始时花费一些时间寻找第一个页面的位置，之后就可以直接顺序读取了，不用再去寻找后续的页面位置。</div>2020-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/92/02/288a6b8c.jpg" width="30px"><span>陈柏林</span> 👍（0） 💬（0）<div>我可以理解成删除也是先操作的数据缓冲池再定时更新到磁盘达到永久删除的效果吗？而删除也可能只是把记录从链表，但实际的数据还存在内存中，只是我们没有地址指向这个地址，所以算是删除了</div>2020-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/cd/f6/30ff4666.jpg" width="30px"><span>UKNOW</span> 👍（0） 💬（0）<div>“如果你使用的是 MySQL MyISAM 存储引擎，它只缓存索引，不缓存数据，对应的键缓存参数为 key_buffer_size，你可以用它进行查看。如果你使用的是 InnoDB 存储引擎，可以通过查看 innodb_buffer_pool_size 变量来查看缓冲池的大小”  

这句话不太理解， 存储引擎是针对每个表而不同的吧，而缓冲池是针对真个数据库吗？</div>2020-04-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLLn1y9RSL9JcACGRVkkhkEmjH7z1eiag763CVKwn3Mzb3djbibwbx0fgZqyBpPozGLOicnllSfydEng/132" width="30px"><span>qijj</span> 👍（0） 💬（1）<div>last_query_cost 查询到的结果是页还是执行计划的评分？ 看老师正文的意思是页，迫切希望能给个明确答案 </div>2020-04-03</li><br/><li><img src="" width="30px"><span>fgdgtz</span> 👍（0） 💬（0）<div>你好老师，我想问问如果是 order by 多个字段排序的执行流程是什么样的呢？
比如 有40000行 order by a desc,b desc limit 1000 ,a字段有索引，b字段无索引，a字段保存的是时间戳，有少部分时间戳是同样的，此时explain 会有 Using filesort，这样放入sort_buffer 是40000行 还是 大于1000行而小于40000行呢？或是扫描了多少行？</div>2020-03-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJafX5kNYJKpD9czE7pjYJtDWnuHeWQLtkfyAtPYUicbiafAUBvUqSnKTM3bahib1wURcRg2miaOFGnpQ/132" width="30px"><span>jacksnow</span> 👍（0） 💬（0）<div>我看官网上面说，buffer pool的数据结构是一个list的结构，list里面存储的page，那么一个sql是如何命中buffer pool中缓存的page的呢？官网上也没有说明原理是啥，老师能解释一下吗？</div>2020-03-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJafX5kNYJKpD9czE7pjYJtDWnuHeWQLtkfyAtPYUicbiafAUBvUqSnKTM3bahib1wURcRg2miaOFGnpQ/132" width="30px"><span>jacksnow</span> 👍（0） 💬（0）<div>老师，有个问题请教一下:
如果是两个表进行join操作，比如
select a.*, b.* 
from a join b on a.xxx = b.xxx &#47;&#47; 第一步
where a.id = &#39;xxxx&#39; &#47;&#47; 第二步
第一步是进行数据组装
第二部是进行条件筛选.
我的问题是：
第一步组装数据的意思是不是在磁盘上通过a和b两个表的磁盘页组装成新的磁盘页，并且需要新分配磁盘空间来存储这些新的磁盘页？
第二步是否是在新组装出来的磁盘页中通过索引进行查询，并将查到的page load到内存中来？</div>2020-03-10</li><br/>
</ul>