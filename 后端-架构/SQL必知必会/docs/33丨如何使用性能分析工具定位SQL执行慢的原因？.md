在上一篇文章中，我们了解了查询优化器，知道在查询优化器中会经历逻辑查询优化和物理查询优化。需要注意的是，查询优化器只能在已经确定的情况下（SQL语句、索引设计、缓冲池大小、查询优化器参数等已知的情况）决定最优的查询执行计划。

但实际上SQL执行起来可能还是很慢，那么到底从哪里定位SQL查询慢的问题呢？是索引设计的问题？服务器参数配置的问题？还是需要增加缓存的问题呢？今天我们就从性能分析来入手，定位导致SQL执行慢的原因。

今天的内容主要包括以下几个部分：

1. 数据库服务器的优化分析的步骤是怎样的？中间有哪些需要注意的地方？
2. 如何使用慢查询日志查找执行慢的SQL语句？
3. 如何使用EXPLAIN查看SQL执行计划？
4. 如何使用SHOW PROFILING分析SQL执行步骤中的每一步的执行时间？

## 数据库服务器的优化步骤

当我们遇到数据库调优问题的时候，该如何思考呢？我把思考的流程整理成了下面这张图。

整个流程划分成了观察（Show status）和行动（Action）两个部分。字母S的部分代表观察（会使用相应的分析工具），字母A代表的部分是行动（对应分析可以采取的行动）。  
![](https://static001.geekbang.org/resource/image/99/37/998b1a255fe608856ac043eb9c36d237.png?wh=800%2A1523)  
我们可以通过观察了解数据库整体的运行状态，通过性能分析工具可以让我们了解执行慢的SQL都有哪些，查看具体的SQL执行计划，甚至是SQL执行中的每一步的成本代价，这样才能定位问题所在，找到了问题，再采取相应的行动。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/46/d0/6bafd7d4.jpg" width="30px"><span>DZ</span> 👍（39） 💬（1）<div>如果两表关联查询，可以这样理解：

1. ref - 双层循环，直到找出所有匹配。
2. eq_ref - 双层循环，借助索引的唯一性，找到匹配就马上退出内层循环。
3. const: 单层循环。

按照循环次数递减的顺序排列它们，应该是 ref &gt; eq_ref &gt; const，循环次数越少，查询效率越高。</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/ee/33ef689b.jpg" width="30px"><span>土土人</span> 👍（8） 💬（1）<div>oracle是否有对应工呢？</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/6d/c20f2d5a.jpg" width="30px"><span>LJK</span> 👍（5） 💬（1）<div>SHOW PROFILE还会再有细致一点的说明么？一般看到都是sending data这个时间最长，不知道包含了哪些具体操作在里面？</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（30） 💬（2）<div>      explain看的东西不止这点吧：老师是不是针对错了DB，至少现实生产这点东西的定位完全不够；老师在生产中不看表的状态就做explain么？如果表的DML过高的话，explain的操作完全没有价值。
     如果一张表的自增跑到了100万，数据量只有10万；说明这张表可能已经损坏了，第一步就是修复表而不是一开始做explain。就像我们拿到一台设备不是先去测功能，首先应当坚持设备是否完全OK再去测试，数据库不可能拿到的是一张全新的表；首先应当是表的性能评估，然后再说相关的检查吧。
       个人觉得今天的讲解的时候漏了真正的第一步：设备没坚持就开始检查设备性能了。
    </div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（6） 💬（0）<div>你可以讲一下 ref、eq_ref 和 const 这三种类型的区别吗？查询效率有何不同？
ref 是使用了非唯一索引
eq_ref 是使用了主键或唯一索引，一般在两表连接查询中索引
const 是使用了主键或唯一索引 与常量值进行比较

查询效率 ref &lt; eq_ref &lt; const</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/24/5d/65e61dcb.jpg" width="30px"><span>学无涯</span> 👍（3） 💬（1）<div>用EXPLAIN查看SQL执行顺序：如果SQL使用EXISTS嵌套子查询，按说，执行顺序是先执行主查询，再执行子查询，但是EXPLAIN出来的结果是主查询的id为1，子查询的id为2，也就是说是先执行的子查询，这是为什么呢</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（2） 💬（0）<div>想问一下，运维的那个MySQL慢SQL的页面怎么弄出来的的，就是甩给我一个网页地址，里面是SLOW LOG PLATFORM里面的详细慢sql日志，毕竟是页面，感觉看起来要比去服务器看输出友好一点。
是什么工具，搭建在自己的服务器，可以选择数据库，选择用户的查看日志详情，自己玩，安装的话对服务器要求高吗
</div>2021-04-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（2） 💬（0）<div>当前会话是代表什么，当前事务么</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/41/bb/21ce60d2.jpg" width="30px"><span>安静的boy</span> 👍（2） 💬（0）<div>index_merge的那个例子中，查询的type怎么是ref</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/45/d1621188.jpg" width="30px"><span>学渣汪在央企打怪升级</span> 👍（1） 💬（0）<div>EXPLAIN那里有些不太清楚，还有要是有一些经验上的阈值分析就好了</div>2020-03-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLNibQE85E0sLs4iaTIAwsTlGLfk58apdzNI1QwU4tiakuMlQ6B2AAicBw4bGSU3bNWMC85UvjcylzyAQ/132" width="30px"><span>Geek_cdf4b1</span> 👍（0） 💬（0）<div>老师，文中“如何使用 EXPLAIN 查看执行计划”部分，“我们对 product_comment 数据表进行查询，设计了联合索引composite_index (user_id, comment_text)，然后对数据表中的comment_id、comment_text、user_id这三个字段进行查询，最后用 EXPLAIN 看下执行计划”。
执行计划 TYPE 应该是 ALL，当使用联合索引composite_index (comment_id, comment_text, user_id) 时，TYPE 是 index。</div>2023-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9c/69/d16ea710.jpg" width="30px"><span>andy</span> 👍（0） 💬（0）<div>等待时间和执行时间是在哪里查？</div>2021-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/73/abb7bfe3.jpg" width="30px"><span>beyondzhao</span> 👍（0） 💬（0）<div>老师，想问下，慢查询里最后那个例子里，采用 mysqldumpslow 按时间排序查看前两条 SQL 查询语句，查询结果里第二条查询语句 Time=164.04s（656s），括号里的656秒表示什么意思呢？哪一个才是这条 SQL 语句查询的耗时呢?</div>2020-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2e/8c/b261e15a.jpg" width="30px"><span>张滔</span> 👍（0） 💬（1）<div>我给领导提出的建议是开启慢查询，然后根据慢查询来优化sql，但领导说这样的话工作会拖拖沓沓，要求我把我们系统的所有sql整理出来进行优化，您赞同我领导的做法吗？</div>2020-04-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/EcYNib1bnDf5dz6JcrE8AoyZYMdqic2VNmbBtCcVZTO9EoDZZxqlQDEqQKo6klCCmklOtN9m0dTd2AOXqSneJYLw/132" width="30px"><span>博弈</span> 👍（0） 💬（0）<div>通过本章学习，了解了如何使用性能分析工具定位SQL执行慢的原因，希望能在实践中运用。</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/61/47/0a6e9729.jpg" width="30px"><span>竹影</span> 👍（0） 💬（0）<div>多表联查的时候，SQL的执行顺序是怎样的？where后什么时候执行？</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d4/ca/bdb348db.jpg" width="30px"><span>law</span> 👍（0） 💬（0）<div>生产环境遇到一种情况，有两个组合索引：coupon_code(tenant_id,coupon_code,platforms), idx_eq_coupon8(tenant_id,end_date,state),有个查询条件按照第二个组合索引的条件查询，但没有用到第二个索引，而是用到了第一个，麻烦老师帮忙分析下这种情况怎么定位什么原因？</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/66/23/d67cc01a.jpg" width="30px"><span>Jack 乐</span> 👍（0） 💬（1）<div>老师，你好！百万级大表创建联合索引，导致阻塞现象，如何解决？</div>2019-08-28</li><br/>
</ul>