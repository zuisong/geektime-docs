作为一个软件开发工程师，你对数据库肯定再熟悉不过了。作为主流的数据存储系统，它在我们的业务开发中，有着举足轻重的地位。在工作中，为了加速数据库中数据的查找速度，我们常用的处理思路是，对表中数据创建索引。那你是否思考过，**数据库索引是如何实现的呢？底层使用的是什么数据结构和算法呢？**

## 算法解析

思考的过程比结论更重要。跟着我学习了这么多节课，很多同学已经意识到这一点，比如Jerry银银同学。我感到很开心。所以，今天的讲解，我会尽量还原这个解决方案的思考过程，让你知其然，并且知其所以然。

### 1.解决问题的前提是定义清楚问题

如何定义清楚问题呢？除了对问题进行详细的调研，还有一个办法，那就是，通过**对一些模糊的需求进行假设，来限定要解决的问题的范围**。

如果你对数据库的操作非常了解，针对我们现在这个问题，你就能把索引的需求定义得非常清楚。但是，对于大部分软件工程师来说，我们可能只了解一小部分常用的SQL语句，所以，这里我们假设要解决的问题，只包含这样两个常用的需求：

- 根据某个值查找数据，比如select * from user where id=1234；
- 根据区间值来查找某些数据，比如select * from user where id &gt; 1234 and id &lt; 2345。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（260） 💬（23）<div>个人觉得B+tree理解起来真不难，抓住几个要点就可以了：
1. 理解二叉查找树
2. 理解二叉查找树会出现不平衡的问题（红黑树理解了，对于平衡性这个关键点就理解了）
3. 磁盘IO访问太耗时
4. 当然，链表知识跑不了 —— 别小瞧这个简单的数据结构，它是链式结构之母
5. 最后，要知道典型的应用场景：数据库的索引结构的设计

还记得，在学生时代，不好好学数据结构的我，当看到这个高大尚的名词“B+tree”时，我心里无比惊慌：这东西貌似不简单。^_^   那时，也有着王争老师说的这种情况：B-tree，这是B减树；肯定还有个正常的B树；B+tree，这是B加树；然后在我的脑海里面，想当然地认为，它们之间有着这样的大小关系：B-tree &lt; B tree &lt; B+tree  
----------
对于思考题，@老杨 大哥的回答我觉得很到位了。 我只做一下补充：
第一题： 对于B+tree叶子节点，是用双向链表还是用单链表，得从具体的场景思考。我想，大部分同学在开发中遇到的数据库查询，都遇到过升序或降序问题，即类似这样的sql: select name,age, ... from where uid &gt; startValue and uid &lt; endValue order by uid asc(或者desc)，此时，数据底层实现有两种做法：
1）保证查出来的数据就是用户想要的顺序
2）不保证查出来的数据的有序性，查出来之后再排序
以上两种方案，不加思考，肯定选第一种，因为第二种做法浪费了时间（如果选用内存排序，还是考虑数据的量级）。那如何能保证查询出来的数据就是有序的呢？单链表肯定做不到，只能从头往后遍历，再想想，只能选择双向链表了。此时，可能有的同学又问了：双向链表，多出来了一倍的指针，不是会多占用空间嘛？  答案是肯定的。可是，我们再细想下，数据库索引本身都已经在磁盘中了，对于磁盘来说，这点空间已经微不足道了，用这点空间换来时间肯定划算呀。顺便提一下：在实际工程应用中，双向链表应用的场景非常广泛，毕竟能大量减少链表的遍历时间

第二题：
答案是「肯定的」。如同@老杨 大哥说的，JDK中的LinkedHashMap为了能做到保持节点的顺序（插入顺序或者访问顺序），就是用双向链表将节点串起来的。 其实，王争老师在《散列表(下）》那一堂课中就已经深入讲解了LinkedHashMap，如果理解了那篇，这个问题应该不难。
-------
最后，我发现王争老师布置的这些课后思考题，都涉及到了之前学到的内容，不知道是有意还是无意的，嘻嘻！

这节的思考题花了蛮多时间进行思考，才能给出以上答案，希望王争老师帮看看是否有不对的地方，谢谢！


</div>2019-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/de/17/75e2b624.jpg" width="30px"><span>feifei</span> 👍（40） 💬（11）<div>老师，看了你的讲解，对于B+树的原理，我基本理解了，我又找了b+树的代码实现，也搞懂怎么回事了，当我看懂了，这个B+树的实现了之后，我就有个问题，这个B+树该如何保存到磁盘中呢？我搜索了好多，也没有找到相关的一个代码，你有这相关的资料吗？这种数据一般是如何保存的？谢谢</div>2019-01-24</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/icVicpGetZfB4tJVH5N9vA0JJkhRmw0TNAMUmRoKO2219S0up6IHmo2dPXAxWu9pm49YlAz0oYZLWcu9yXqIgMZA/132" width="30px"><span>hnbc</span> 👍（27） 💬（5）<div>老师，我想问一下100叉树为什么是3次io操作，不应该是4次吗，100的4次方是1亿</div>2019-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/08/91caf5c1.jpg" width="30px"><span>Harry陈祥</span> 👍（22） 💬（4）<div>您好。有次面试，面试官直接问我，什么数据结构可以做到O(logn)的范围查询？ 当时没有想到填表，想到了B+树，而且数据库索引确实也是用的B+树。
那么问题来了，跳表和B+树在实现难度和性能上有什么区别，在数据量很大的情况下，表现性能如何，为什么redis选跳表？ 谢谢老师</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（10） 💬（3）<div>请问：
第一段代码，第9行：
PAGE_SIZE = (m-1)*4[keywordss 大小]+m*8[children 大小]
1，这个8指的是引用（指针）占的内存大小吗？
2，引用大小是怎么计算的？和机器是多少位的有什么关系吗？
望争哥回复，谢谢！</div>2019-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e4/e8/a1703783.jpg" width="30px"><span>mrlay</span> 👍（6） 💬（4）<div>维持b+树的特性的策略有了，但是如何实现这个策略 以及一些其他问题解决的策略的实现 我有些发怵的感觉，大家一般都是怎么过来的呢？</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ed/4e/ef406442.jpg" width="30px"><span>唯她命</span> 👍（5） 💬（2）<div>老师，现在觉得 你画的图 都是B树  而不是B+树</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ed/4e/ef406442.jpg" width="30px"><span>唯她命</span> 👍（5） 💬（1）<div>老师   网上查到的资料  说有k个子树的中间节点包含有k个元素（B树中是k-1个元素） 
和你讲的不同 </div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6c/e9/377a3b09.jpg" width="30px"><span>H.L.</span> 👍（3） 💬（3）<div>叶子节点的数据是如何存储的？比如mysql的b+树，key放在一堆，data放在一堆？</div>2019-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（0） 💬（2）<div>对于这样的查询语句&quot;select * from table where user_id &lt; 1000&quot;, 是如何在叶子节点上进行遍历的？是找到1000之后往前遍历，还是从开始遍历到1000？</div>2019-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/81/4a/dcc563fb.jpg" width="30px"><span>shinee_x_X</span> 👍（0） 💬（1）<div>很想问问老师mysql的索引和数据是怎么存储的，因为是一页页拿数据的，一页就是一个节点，那只拿一页数据的话，一个节点的孩子节点地址是怎么得到的</div>2019-10-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIjRETqRjvLESLDZkNTjIiaSibtNYBaS1o8WMUicOFn3ycF3Mgh6LRJibqSBjVBjiaO2ibW0gHkafATb21A/132" width="30px"><span>lmdcx</span> 👍（0） 💬（1）<div>&quot;理论上讲,对跳表稍加改造,也可以替代 B 树,作为数据库的索引实现的&quot;
隔壁的林晓斌说了：数据库技术发展到今天，跳表、LSM 树等数据结构也被用于引擎设计中</div>2019-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/94/1c72edcd.jpg" width="30px"><span>老衲爱清扬</span> 👍（0） 💬（6）<div>王老师，请问B+树每个节点的大小是16KB，不是4KB的吧</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e2/ab/430c24df.jpg" width="30px"><span>zqing</span> 👍（0） 💬（2）<div>不管是内存中的数据，还是磁盘中的数据，操作系统都是按页（一页大小通常是 4KB，这个值可以通过 getconfig PAGE_SIZE 命令查看）来读取的，一次会读一页的数据。如果要读取的数据量超过一页的大小，就会触发多次 IO 操作。所以，我们在选择 m 大小的时候，要尽量让每个节点的大小等于一个页的大小。读取一个节点，只需要一次磁盘 IO 操作。——-一个节点超过一个pagesize 为啥会触发多次IO操作？这个是不是写的有问题？</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/d0/616045b5.jpg" width="30px"><span>兰鑫</span> 👍（0） 💬（1）<div>二叉查找树改造成支持区间查找的过程，即叶子节点通过链表链接，这样就支持区间查找了。关于这个点，我很好奇文章中的示例，改造之后根节点是27，这个27是怎么选出来的呢？</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/48/75/02b4366a.jpg" width="30px"><span>乘坐Tornado的线程魔法师</span> 👍（0） 💬（4）<div>关于非叶子节点和叶子节点的公式。老师可否再给予下指点。感谢！
PAGE_SIZE = (m-1)*4[keywords 大小]+m*8[children 大小]
为什么 第一个系数是m-1而不是m? 这个公式是某个特定例子的公式还是通用公式？

PAGE_SIZE = k*4[keywords 大小]+k*8[dataAddresses 大小]+8[prev 大小]+8[next 大小]
prev大小是值得，链表中前一个节点的数据占用空间大小嘛？</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/48/75/02b4366a.jpg" width="30px"><span>乘坐Tornado的线程魔法师</span> 👍（0） 💬（1）<div>最后一张图中，&quot;非叶子节点中，子节点小于3个就合并”。根据B+树的特点，每个节点中子节点的个数不能小于m &#47; 2 (5 &#47; 2 = 2)。那么这句话是否应该改成“非叶子节点中，子节点小于2个就合并”？请老师指正</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/03/11/f58c6278.jpg" width="30px"><span>你好呀</span> 👍（0） 💬（1）<div>oracle的btree索引有时候不去位图索引  是btree需要的io次数比位图多吗？  位图又是如何优化的？</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/00/f6/f6cf138c.jpg" width="30px"><span>Kermit Sun</span> 👍（0） 💬（1）<div>问一个问题，具体节点的key是如何计算出来的呢？如果like模糊查询字段a，左边精确，右边模糊，是否能够使用btree？</div>2019-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d0/c7/62de0458.jpg" width="30px"><span>谭小谭</span> 👍（0） 💬（1）<div>老师，你说的 B+ 树的节点只存储索引，而 mysql 的 InnoDB中的索引又是采用 B+ 树来实现的，这里该怎么理解节点只存储索引呢，感觉要绕进去了啊。</div>2019-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0a/dd/88fa7b52.jpg" width="30px"><span>Geek_41d472</span> 👍（0） 💬（1）<div>以前看高性能mysql的时候就讲了B+树，不过没讲这么仔细，一直没搞清楚某些时候插入数据会导致节点分裂，今天算是搞明白了。原以为这章节会把B+的增强改查某个节点的代码实现写出来，还是有点小失望，哈哈，如果有老师能讲下就更完美了</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（363） 💬（6）<div>听专栏，听到了自己的名字，不敢相信，看了文稿，确实是自己。真是受宠若惊！</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/f7/3a493bec.jpg" width="30px"><span>老杨同志</span> 👍（80） 💬（7）<div>问题一，双向链表，方便asc和desc。
问题二，可以支持区间查询。java中linkedHashMap就是链表链表+HashMap的组合，用于实现缓存的lru算法比较方便，不过要支持区间查询需要在插入时维持链表的有序性，复杂度O(n).效率比跳表和b+tree差</div>2019-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cc/33/19f150d9.jpg" width="30px"><span>城</span> 👍（78） 💬（0）<div>1.链表是双向链表，用以支持前后遍历
2.散列表的节点用链表串起来，并不能实现范围查询，因为散列表本身无序，而B+树是基于二叉查找树演变而成，是有序的</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/d5/e23dc965.jpg" width="30px"><span>Felix Envy</span> 👍（25） 💬（2）<div>看到留言里很多同学都说第二题答案是肯定的，有点不同意。
如果区间边界值在在散列表中没有命中，那么就无法定位区间的起始节点。
如有错误望指出～</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/dc/c3/e4ba51d5.jpg" width="30px"><span>Flash</span> 👍（15） 💬（6）<div>对于第二题，觉得Jerry银银的答案有问题，可能会误导其他人。希望老师能指正一下，我觉得用链表将散列表节点串起来，不能支持按区间查找。因为散列表的节点是无序的，除非先遍历把散列表的节点放到数组中，进行排序，再用LinkedHashMap遍历存储，这样链表中串的节点才是有序的，直接用链表串散列表节点，是不支持按区间查找的。</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/cd/1e/692c3313.jpg" width="30px"><span>复兴</span> 👍（12） 💬（9）<div>innodb的聚簇索引，不是将数据存储在叶子节点上嘛，这里又说叶子节点不存储数据。</div>2019-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f4/e2/dbc4a5f2.jpg" width="30px"><span>朱东旭</span> 👍（11） 💬（3）<div>这里讲的仅仅是单列索引，实际项目中组合索引使用应该比单列索引多，组合索引版的B+树是如何实现的，这个重要的知识点似乎被遗漏了。</div>2019-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5e/57/fb18c46a.jpg" width="30px"><span>嗯嗯</span> 👍（7） 💬（0）<div>对作者说的那个m云里雾里</div>2019-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/88/d0/6e75f766.jpg" width="30px"><span>有朋自远方来</span> 👍（4） 💬（0）<div>1.利用磁盘预读功能2.主簇索引
觉得这两点也很重要。</div>2019-01-16</li><br/>
</ul>