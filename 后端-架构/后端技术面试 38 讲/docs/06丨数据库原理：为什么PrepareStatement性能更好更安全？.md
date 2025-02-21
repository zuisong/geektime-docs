做应用开发的同学常常觉得数据库由DBA运维，自己会写SQL就可以了，数据库原理不需要学习。其实即使是写SQL也需要了解数据库原理，比如我们都知道，SQL的查询条件尽量包含索引字段，但是为什么呢？这样做有什么好处呢？你也许会说，使用索引进行查询速度快，但是为什么速度快呢？

此外，我们在Java程序中访问数据库的时候，有两种提交SQL语句的方式，一种是通过Statement直接提交SQL；另一种是先通过PrepareStatement预编译SQL，然后设置可变参数再提交执行。

Statement直接提交的方式如下：

```
statement.executeUpdate("UPDATE Users SET stateus = 2 WHERE userID=233");
```

PrepareStatement预编译的方式如下：

```
PreparedStatement updateUser = con.prepareStatement("UPDATE Users SET stateus = ? WHERE userID = ?"); 
updateUser.setInt(1, 2); 
updateUser.setInt(2,233); 
updateUser.executeUpdate();
```

看代码，似乎第一种方式更加简单，但是编程实践中，主要用第二种。使用MyBatis等ORM框架时，这些框架内部也是用第二种方式提交SQL。那为什么要舍简单而求复杂呢？

要回答上面这些问题，都需要了解数据库的原理，包括数据库的架构原理与数据库文件的存储原理。

## 数据库架构与SQL执行过程

我们先看看数据库架构原理与SQL执行过程。

关系数据库系统RDBMS有很多种，但是这些关系数据库的架构基本上差不多，包括支持SQL语法的Hadoop大数据仓库，也基本上都是相似的架构。一个SQL提交到数据库，经过连接器将SQL语句交给语法分析器，生成一个抽象语法树AST；AST经过语义分析与优化器，进行语义优化，使计算过程和需要获取的中间数据尽可能少，然后得到数据库执行计划；执行计划提交给具体的执行引擎进行计算，将结果通过连接器再返回给应用程序。
<div><strong>精选留言（25）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/14/e1/ee5705a2.jpg" width="30px"><span>Zend</span> 👍（6） 💬（1）<div>请问老师，在进行事务操作时，事务日志文件会记录更新前的数据记录，这个记录更新前的数据记录是 什么意思，是把更新之前的数据都查询出来，记录到事务日志文件嘛</div>2019-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/6c/785d9cd3.jpg" width="30px"><span>Snooker</span> 👍（4） 💬（1）<div>看文章讲解，聚簇索引，不止备份了整个表数据，增删改查开销也大，所以应减少不必要的聚簇索引，除主键外其他可考虑使用非聚簇索引。
那如何指定索引为非聚簇索引呢？</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/14/e1/ee5705a2.jpg" width="30px"><span>Zend</span> 👍（4） 💬（2）<div>请问一下老师PreparedStatement经过语法分析生成的抽象语法树，再经过语义分析和优化器处理后生成的执行计划，会有缓存吗？</div>2019-12-01</li><br/><li><img src="" width="30px"><span>开心小毛</span> 👍（1） 💬（3）<div>请问李老师，既然数据库连接会占用内存，那么传统web应用为什么不干脆在每一次接受http请求时建立数据库连接，然后再在http访问结束后断开数据库连接？
建立数据库连接会耗CPU吗？（假设数据库服务自身已经有线程池等待被连接，web应用也缓存了地址密码等配置信息）</div>2020-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/20/95/89bd2c38.jpg" width="30px"><span>pcz</span> 👍（0） 💬（1）<div>老师：PrepareStatement提交带占位符的sql进行预处理的意思是：执行到语义分析和优化器这一步，但是不执行引擎？那这个sql的赋值过程是什么样的？</div>2021-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/d2/7024431c.jpg" width="30px"><span>探索无止境</span> 👍（0） 💬（1）<div>老师您好，文中提到“每个节点存储 1000 多个数据，这样树的深度最多只要 4 层，就可存储数亿的数据”，严谨来说应该是三层即可，1000*1000*1000，我是这么计算的</div>2020-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/48/75/02b4366a.jpg" width="30px"><span>乘坐Tornado的线程魔法师</span> 👍（0） 💬（2）<div>请问下，文中的第一个B+树示意图的第一层中间节点，8和34中间的部分是不是也应该指向一个子节点？</div>2019-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8b/4b/9e0d334f.jpg" width="30px"><span>⛽️🦆</span> 👍（113） 💬（6）<div>您好，老师：
回答上述问题
1.创建多的索引，会占用更多磁盘空间。如果有一张很大的表，索引文件的大小可能达到操作系统允许的最大文件限制；
2.对于DML操作的时候，索引会降低他们的速度。因为MySQL不仅要把搞定的数据写入数据文件，而且它还要把这些改动写入索引文件;
改善数据库性能：
1.索引优化，选择合适的索引列，选择在where、group by、order by、on 从句中出现的列作为索引项，对于离散度不大的列没有必要创建索引。
2.索引字段越小越好。
3.SQL语句的优化、数据表结构的优化。
    3.1：选择可存数据最小的数据类型，选择最合适的字段类型，进行数据的存储;
    3.2：数据量很大的一张表，应该考虑水平分表或垂直分表；
    3.3：尽量不要使用text字段，如果非要用，那么应考虑将它存放另一张表中；
4.数据库配置的优化：
    4.1：连接数的配置，因为大量的连接，不进行操作，那样也会占用内存。
    4.2：查询缓存的配置，但在MySQL 8.0就删除了此功能。
5.硬件的配置;
 额外加说一下，常见性能的问题：
1.条件字段函数的操作，给索引字段做了函数计算，就会破坏索引值，因此优化器就放弃了走树搜索能够;
2.隐式类型转换，比如数据库字段是varchar类型，创建的索引，但是使用的时候传入的是int类型，那么会走全表扫面;
3.隐式字符编码转换，如果join 两表的时候，两表的字符集不同，也不能用上索引；
</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/84/39/c8772466.jpg" width="30px"><span>无形</span> 👍（8） 💬（0）<div>最近在广告检索中接入了用户画像标签，实现了把一大串嵌套json格式的标签数据表达式，类似dnf表达式，解析为可计算的广告匹配模型，其中就有类似sql一样，对表达式进行格式分析、数据、比较符检验、复杂的逻辑关系转换为容易处理的计算单元，最后生成一个树状匹配模型，通过对模型输入用户数据，进行匹配，并返回符合的用户。
这有点像用户画像标签就是一条SQL，对SQL进行语法分析，生成匹配模型（类比SQL的执行计划），当下次输入用户数据的时候用生成好的匹配模型直接处理数据，不必再重复解析画像标签</div>2019-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8a/7b/c8123a88.jpg" width="30px"><span>尹宗昌</span> 👍（7） 💬（0）<div>索引可以提高查询性能，但是一定要考虑维护索引的成本。空间占用、插入修改的性能影响都要衡量</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d8/5d/07dfb3b5.jpg" width="30px"><span>杯莫停</span> 👍（4） 💬（0）<div>看到预编译这个概念就想到Mybites的变量占位符$和#，前者没有预编译直接以字符串的方式被append到sql语句中，以至于有sql注入被黑客攻击的可能。而#会被预编译成一个符号，在使用的时候再把参数值填进来，这样就避免了sql注入风险。至于原理还要去看源码。</div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a0/d9/49578be1.jpg" width="30px"><span>陈衎</span> 👍（2） 💬（0）<div>索引不是越多越好，索引多了对磁盘容量产生代价。增删改，存储过程等都会涉及到索引的修改，导致效率下降。还有比如字段查询量少，重复多，比如性别等，是没必要建立索引的。觉得索引还是要看使用场景吧，比如数据仓库。

优化性能和提高查询效率，个人觉得是一种编码习惯和思想过程，比如小表驱动大表，根据实际合理创建表结构范式，建立联合查询一次到位避免回表，清楚select ，join，group by，having，where，order by这些执行顺序。设计健壮灵活的数据表结构。</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/84/39/c8772466.jpg" width="30px"><span>无形</span> 👍（2） 💬（0）<div>数据变动的时候同时需要更新索引，索引多了，数据变动的效率就会降低，索引也是文件，会占用更多的磁盘空间
。
另外，我之前提到的要动手实现的高性能检索系统，在数据的存储部分，用文件存储，为了提高文档的检索效率，为文件创建了索引，索引是这种格式id:start:length，
文档id:在文件中的起始位置:文档的长度，索引文件是排序过得，例如下面这种格式
0000000001:0000000000:0000000100
0000000002:0000000100:0000000300
0000000007:0000000400:0000001000
在不加载完整索引文件的情况下，这样可以通过offset快速读取每个索引数据，因为是排序过的，二分查找快速查找到文档的起始位置和大小，就可以迅速在文件中找到文档，测试了下，文档数据量160w，最多20次就可以查找到文档，耗时200-300微妙，如果对索引文件进行分片存储还会更快</div>2019-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f4/87/644c0c5d.jpg" width="30px"><span>俊伟</span> 👍（2） 💬（0）<div>1.索引较多，插入删除的时候会有额外的开销。
2.索引字段尽量小，因为索引字段的大小会影响每一个b+树节点数据块中的数据项的个数。
3.多了解业务，有些地方可以使用索引有些则不用。
4.可以综合利用联合索引和单独索引</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/80/2b/ef1581b5.jpg" width="30px"><span>米兰的小铁匠</span> 👍（1） 💬（0）<div>思考总结：PrepareStatement预编译、然后设置可变参数再执行提交。
1、介绍了Sql执行流程：
查询：连接器-查询缓存-分析器-优化器-执行器
更新：获取数据（数据页内存中判断）-更新（更新到内存中）prepare redolog-完成后binlog-redolog
2、PrepareStatement：预处理使效率高、防止Sql注入
3、底层结构：B+树
多叉树：矮，文件io少
节点不存储数据，只是索引
链表讲叶子节点串联一起，方便区间查找
一般情况，根节点会存储再内存中，其他节点存储再磁盘</div>2021-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（1） 💬（0）<div>用一篇文章来讲数据库原理，感觉还是有点困难的。如果想要入门，那么推荐《SQL必知必会》专栏；如果想要深入学习 MySQL，那么推荐丁奇的《MySQL实战45讲》。

PrepareStatement 应该是属于编程语言还是数据库驱动？很久以前，用 C# 连接 Oracle 的时候就接触过 PrepareStatement 的概念，Java 连接 MySQL 或者 Oracle 肯定也有，毫无疑问 SQL Server 也不会缺少这个概念。

而且有点也都类似，在提高性能的同时避免注入攻击。

我的印象里隐约有，使用 PrepareStatement 并不利于数据库的 SQL 查询结果缓存，没有找到出处。但是现在新版本的 MySQL 似乎已经弃用了查询缓存。

能理解数据库存储原理（B+树），能分清楚主键聚簇索引和非聚簇索引，能看懂执行计划的程序员，都是好程序员。</div>2020-10-18</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（1） 💬（0）<div>聚簇索引,叶子节点指向了记录。
非聚簇索引，叶子节点指向了主键。
索引肯定不是越多越好，不然就会默认创建。索引有成本，成本来自于存储成本和插入删除时候的维护成本，如果查询得到的好处不足以抵消维护和存储成本，就是不值得的。</div>2019-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/1a/389eab84.jpg" width="30px"><span>而立斋</span> 👍（1） 💬（0）<div>李老师，堪比百科全书啊！非常接地气！给老师提个建议，文章中有些是针对MySQL说的，有些不是，希望老师能区分一下。
索引么，也是一种空间换时间的思路，细思极恐。改善数据库访问性能的手段也不应该仅限于索引这种手段。</div>2019-11-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIeWDmWuCHppRXeQiaCGcSf8gib4Sb0HohDicQ5A4ZtW79wNCLWqyObmkQYibpOydCWNGIu2NK6iaKaMsw/132" width="30px"><span>Geek_5180b5</span> 👍（0） 💬（1）<div>处理中占位符参数的替换，就是在真正执行sql的时候才替换，可以这样理解嘛。。</div>2021-05-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM70nnPpGc2c9vic68lB3ndZxlWLwXakhpkq8ZzZSPRusynorCafpoAYxkicOYhRic9GTEqWjhagDLp6w/132" width="30px"><span>Geek__风雨</span> 👍（0） 💬（0）<div>分析器，优化器（待执行的sql），执行器，执行引擎</div>2020-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/7a/02fdf1a2.jpg" width="30px"><span>FreezeSoul</span> 👍（0） 💬（0）<div>感谢，之前只是知道preparestatement会生成语法树避免的注入，现在才明白是生成执行计划，避免的注入</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/20/5d/69170b96.jpg" width="30px"><span>灰灰</span> 👍（0） 💬（0）<div>打卡</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（0）<div>SQL 的分析器 包括词法分析器和语法分析器，经过词法分析器生成 AST ，不是语法分析</div>2019-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/48/75/02b4366a.jpg" width="30px"><span>乘坐Tornado的线程魔法师</span> 👍（0） 💬（9）<div>印象中丁奇的《MySQL实战45讲》中，也讲到了回表。但是文中提到的MySQL是聚簇索引，不需要回表。是不是这里面有些概念需要根据具体情况再进一步拆分讨论。并不能一概而论？</div>2019-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/7c/03/2941dea7.jpg" width="30px"><span>幸福来敲门</span> 👍（0） 💬（0）<div>哎</div>2019-11-29</li><br/>
</ul>