通过上一篇文章对不同的DBMS的介绍，你应该对它们有了一些基础的了解。虽然SQL是声明式语言，我们可以像使用英语一样使用它，不过在RDBMS（关系型数据库管理系统）中，SQL的实现方式还是有差别的。今天我们就从数据库的角度来思考一下SQL是如何被执行的。

关于今天的内容，你会从以下几个方面进行学习：

1. Oracle中的SQL是如何执行的，什么是硬解析和软解析；
2. MySQL中的SQL是如何执行的，MySQL的体系结构又是怎样的；
3. 什么是存储引擎，MySQL的存储引擎都有哪些？

## Oracle中的SQL是如何执行的

我们先来看下SQL在Oracle中的执行过程：

![](https://static001.geekbang.org/resource/image/4b/70/4b43aeaf9bb0fe2d576757d3fef50070.png?wh=1176%2A420)  
从上面这张图中可以看出，SQL语句在Oracle中经历了以下的几个步骤。

1. 语法检查：检查SQL拼写是否正确，如果不正确，Oracle会报语法错误。
2. 语义检查：检查SQL中的访问对象是否存在。比如我们在写SELECT语句的时候，列名写错了，系统就会提示错误。语法检查和语义检查的作用是保证SQL语句没有错误。
3. 权限检查：看用户是否具备访问该数据的权限。
4. 共享池检查：共享池（Shared Pool）是一块内存池，最主要的作用是缓存SQL语句和该语句的执行计划。Oracle通过检查共享池是否存在SQL语句的执行计划，来判断进行软解析，还是硬解析。那软解析和硬解析又该怎么理解呢？
   
   在共享池中，Oracle首先对SQL语句进行Hash运算，然后根据Hash值在库缓存（Library Cache）中查找，如果存在SQL语句的执行计划，就直接拿来执行，直接进入“执行器”的环节，这就是软解析。
   
   如果没有找到SQL语句和执行计划，Oracle就需要创建解析树进行解析，生成执行计划，进入“优化器”这个步骤，这就是硬解析。
5. 优化器：优化器中就是要进行硬解析，也就是决定怎么做，比如创建解析树，生成执行计划。
6. 执行器：当有了解析树和执行计划之后，就知道了SQL该怎么被执行，这样就可以在执行器中执行语句了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/b1/982ea185.jpg" width="30px"><span>美妙的代码</span> 👍（14） 💬（2）<div>老师，那两张，oracle，mysql 的大图。是哪儿的。有没有高清的啊。很多小字看不清楚。能否给个高清的链接。</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ef/86/12f95d66.jpg" width="30px"><span>FATMAN89</span> 👍（10） 💬（1）<div>老师讲的挺好的，想请问老师，课程所用到的数据库在哪里可以获得呢，多谢</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a0/3f/06b690ba.jpg" width="30px"><span>刘桢</span> 👍（50） 💬（13）<div>今年考研必上北京邮电大学！</div>2019-06-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/fUDCLLob6DFS8kZcMUfxOc4qQHeQfW4rIMK5Ty2u2AqLemcdhVRw7byx85HrVicSvy5AiabE0YGMj5gVt8ibgrusA/132" width="30px"><span>NO.9</span> 👍（15） 💬（1）<div>C,共享池。
讲的好系统啊，有种想学个花拳绣腿，结果教我九阳神功的感觉。</div>2019-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fd/dc/245fee32.jpg" width="30px"><span>张驰皓</span> 👍（13） 💬（1）<div>感觉 MySQL 部分的第二张图（流程图）有点问题，“缓存查询”后“找到”分支的箭头应该不用再指向”缓存查询“吧？</div>2019-12-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLbchZfeEnshPuUwEsQkn1XbWxjs3rRUpSRUxjW4q7rOcrPvXld0IxEZ1jlpEJdklFeEVERJoOfibg/132" width="30px"><span>qf年间</span> 👍（8） 💬（1）<div>文中多次提到执行计划，这是一个什么东西呢，可否具体讲解一下，或者举例说明</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/4e/fd946cb2.jpg" width="30px"><span>allean</span> 👍（7） 💬（1）<div>共享池</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（6） 💬（1）<div>再次听一遍不一样的东西还是会发现不一样的收货:这大概就是数据库用的多了有时代码层确实没啥 ，可是切换中的优化过程还是会疏漏某些分析细节。
explain已经用到了极致，忘了优化的极限其实是多种方式的相辅相成；profile早期用过，反而这几年用的很少很少；explain更加管用-在多种数据库中，反而忘了有时需要一些简单的手段辅以。</div>2019-06-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqjbwXwF3YUcSw7A8v6f0sAYzQMloOWg62aciaGfzZWibRw2jjTja1Vwh5CLVGZdseM6gSBnC1hRzEQ/132" width="30px"><span>firstblood</span> 👍（1） 💬（1）<div>MyISAM 和InnoDB的比较参考https:&#47;&#47;www.jianshu.com&#47;p&#47;a957b18ba40d 这个文章</div>2019-09-25</li><br/><li><img src="" width="30px"><span>Geek_d3a509</span> 👍（0） 💬（1）<div>Oracle中绑定变量：SQL语句中相同的操作对不同的变量值用一个变量来代替，使得Oracle中要做硬解析变成软解析，以减少Oracle在解析上花费的时间
优点：减少了很多不必要的硬解析，将由软解析代替，大大降低数据库花费在SQL解析上的资源开销（时间与空间的浪费）。
缺点：绑定了变量之后优化比较困难，使用绑定之后可能对执行计划有一定的影响，导致执行计划的出错。比如很多重复的语句使用一个变量代替，那么可能就第一条解析正确，余下的就不能正确执行。
InnoDB的特性与使用场景（mysql5.5及以后版本默认存储引擎）：事务型存储引擎，支持ACID特性；支持行级锁。适用大多数OLTP应用
MyISAM的特性与使用场景：不支持事务，表级锁。适用（1）非事务性应用  （2）只读型应用    （3）空间型应用

选择题选C</div>2019-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/e6/67b0b711.jpg" width="30px"><span>大海</span> 👍（0） 💬（1）<div>对于代码部分提个建议，复制出来的内容最好时可以直接使用的。
mysql&gt; show profile for query 2;
现在复制出来的是这样，需要自己把前面的部分去掉，才能用。</div>2019-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/61/37/a4c4c0ab.jpg" width="30px"><span>止戈</span> 👍（0） 💬（1）<div>老师请问什么时候会讲到具体使用方法？</div>2019-09-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK009KMmXKFVeR6ja1dDB69lZEbUiabA8r8QnChtcIEWsqsO42opsXQ7A9pnezCz38lqbuKxrczCMA/132" width="30px"><span>Geek_c76f38</span> 👍（0） 💬（1）<div>SQL&gt; select * from player where player_id = 10001;
代码在手机上看用显示不完整，难道每条都要复制出来才能看？有没有什么办法解决一下</div>2019-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0f/71/9273e8a4.jpg" width="30px"><span>时间是最真的答案</span> 👍（0） 💬（1）<div>C. 共享池
文中提到过</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d3/dc/d216d40c.jpg" width="30px"><span>鱼🐟</span> 👍（0） 💬（1）<div>你们的服务器是不是挂了，经常不能访问</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（0） 💬（1）<div>使用事务用innodb，非事务使用my</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/5d/1f7de6dd.jpg" width="30px"><span>取舍</span> 👍（0） 💬（1）<div>明白了老师</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/af/1cb42cd3.jpg" width="30px"><span>马以</span> 👍（0） 💬（2）<div>迫切想要得到表结构脚本
</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（0） 💬（1）<div>💪</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/63/a94f339e.jpg" width="30px"><span>Devo</span> 👍（0） 💬（1）<div>mysql的执行计划如何绑定呢？老师能详细讲下mysql 的mvcc原理吗，让小白也能看懂，谢谢！</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/d7/9af5dd29.jpg" width="30px"><span>痛…</span> 👍（0） 💬（1）<div>存储在共享池</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/3f/09308258.jpg" width="30px"><span>雨先生的晴天</span> 👍（0） 💬（1）<div>1. 绑定变量：就是在 SQL 语句中使用变量，通过不同的变量取值来改变的执行结果。
优点：减少硬解析。
缺点:  难以优化，参数不同导致执行效率不同。

MyISSAM 速度快，占用资源少，但是不知道事务，外键。
InnoDB 存储引擎：它是 MySQL 5.5.8 版本之后搜索引擎。支持事务，行级锁定，外键。

选择题： C， 共享池。</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6b/8f/eba34b86.jpg" width="30px"><span>星光</span> 👍（0） 💬（1）<div>答案是C共享池。
顺便咨询下老师，您在开篇词里说“为专栏建了一个王者荣耀数据库和 NBA 球员数据库”。那么请问我们可以远程连接它进行操作吗？</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/15/b4/adefadc6.jpg" width="30px"><span>jeric</span> 👍（0） 💬（1）<div>共享池</div>2019-06-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIsJ4ZpKgUPQ8euPymt3Yl8KZX78R6mnB0WKspVoWPAbDsoqTs8AWjG9AlO4ibhnK5ITVtJ5M6RpVg/132" width="30px"><span>敏儿</span> 👍（0） 💬（1）<div>C共享池</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/b9/17ab13f1.jpg" width="30px"><span>都是弟弟</span> 👍（0） 💬（1）<div>学习了</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/95/bf/4a30ba94.jpg" width="30px"><span>暖冬°</span> 👍（0） 💬（1）<div>老师，你好第一次得知mysql还能选择存储引擎！
课堂上的学习没有这么的深入，这个课程很有意思
但是怎么去手动选择存储引擎呢？
答案选共享池</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/4f/65abc6f0.jpg" width="30px"><span>KaitoShy</span> 👍（100） 💬（0）<div>1. 绑定变量概念：sql语句中使用变量，通过不同的变量值来改变sql的执行结果
优点：减少硬解析，减少Oracle的工作量
缺点：参数不同导致执行效率不同，优化比较难做。
2.MyISAM的使用场景为读写分离的读库， 而InnoDB为写库
3. C共享池，看图中有个Shared SQL Area。</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/90/4e/efaea936.jpg" width="30px"><span>墨禾</span> 👍（76） 💬（4）<div>【回答3个问题】
1、oracle中的绑定变量指的是 sql语句在执行时，通过改变不同的变量值来改变sql的执行结果；
优点：避免硬解析，提高SQL语句执行的效率；
缺点：如果使用绑定变量，那么优化器就会忽略直方图的信息，在生成执行计划的时候可能不够优化。

2、MyISAN：
不支持事务、外键，速度快、资源占有少；
InnoDB：支持实物、外键、聚集索引，5.6版本以后的mysql支持全文索引；

使用场景：
需要支持事物的场景考虑InnoDB；
以读为主的数据表用MyISAM；
MyISAM奔溃后的系统的恢复较困难，没有要求的话可以用；
不知道选什么数据库合适的话，用InnoDB不会差【5.5版本以后的mysql默认的引擎是InnoDB】

3、oracle在共享池中进行缓存。

【学习总结】
1、get一个学习方法
培养抽象事物的能力，掌握学习要点，如sql知识，重点掌握sql执行的原理，因为在不同的数据库中，sql执行的原理大同小异，只是在执行的顺序上有所不同。
2、get一个oracle sql优化的技巧
通过绑定变量，优化sql结果
3、get一个oracle、mysql共同的执行sql的原理
SQL语句-》缓存查询-》解析器-》优化器-》执行器
【PS:老师后面能不能推荐一些实战项目练习，来巩固知识点呢？】</div>2019-06-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep8ibEQqN1SlfsuVzTATiatUt007dhCNpvKDicrcsYQP0MgWtIk92304jrQ5tV4ibfoToYwRLfNeicTuQA/132" width="30px"><span>虫子的一天</span> 👍（28） 💬（0）<div>老师好，我原来用SQLSERVER比较多，经常会碰到参数化的SQL查询中，因为SQLSERVER已经缓存了查询计划，导致某些特定参数查询效率很低的事情(刚才文中也有提及Oracle也有类似问题)。
我刚听讲似乎MySQL是没这个机制的，是否MySQL就不会碰到类似问题?
另外如果不让SQLserver使用缓存的查询计划，每次都重新生成，又导致CPU高，MYSQL又是如何避免类似问题的
感谢</div>2019-06-17</li><br/>
</ul>