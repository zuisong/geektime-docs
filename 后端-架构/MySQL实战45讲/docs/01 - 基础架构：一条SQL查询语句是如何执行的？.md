你好，我是林晓斌。

这是专栏的第一篇文章，我想来跟你聊聊MySQL的基础架构。我们经常说，看一个事儿千万不要直接陷入细节里，你应该先鸟瞰其全貌，这样能够帮助你从高维度理解问题。同样，对于MySQL的学习也是这样。平时我们使用数据库，看到的通常都是一个整体。比如，你有个最简单的表，表里只有一个ID字段，在执行下面这个查询语句时：

```
mysql> select * from T where ID=10；
```

我们看到的只是输入一条语句，返回一个结果，却不知道这条语句在MySQL内部的执行过程。

所以今天我想和你一起把MySQL拆解一下，看看里面都有哪些“零件”，希望借由这个拆解过程，让你对MySQL有更深入的理解。这样当我们碰到MySQL的一些异常或者问题时，就能够直戳本质，更为快速地定位并解决问题。

下面我给出的是MySQL的基本架构示意图，从中你可以清楚地看到SQL语句在MySQL的各个功能模块中的执行过程。

![](https://static001.geekbang.org/resource/image/0d/d9/0d2070e8f84c4801adbfa03bda1f98d9.png?wh=1920%2A1440)

MySQL的逻辑架构图

大体来说，MySQL可以分为Server层和存储引擎层两部分。

Server层包括连接器、查询缓存、分析器、优化器、执行器等，涵盖MySQL的大多数核心服务功能，以及所有的内置函数（如日期、时间、数学和加密函数等），所有跨存储引擎的功能都在这一层实现，比如存储过程、触发器、视图等。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/4a/22/2681d602.jpg" width="30px"><span>林晓斌</span> 👍（774） 💬（12）<div>感谢大家的积极评论。
答案是分析器。
@threefat 提到Oracle，MySQL确实在设计上受Oracle影响颇深。
@圈圈圆圆  高性能MySQL里面概念学得好。
@Yezhiwei 等几位，说正文里面已经暗示答案的同学，你们这么机智👍🏿

后面每期的问题，我们会在下一期的结尾的给出解释，不过只是“参考”哦，以评论区的质量，我估计到时候只需要引用优秀评论就好了 ^_^
</div>2018-11-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eq2fAjzw4bRgOory5XZqlTbSic7p4MmlK6g4wIdQ5628frjibBZ9QyAHrjqnm0TYaO1rePpiaoSv6xzQ/132" width="30px"><span>threefat</span> 👍（384） 💬（7）<div>课后答案:分析器。Oracle会在分析阶段判断语句是否正确，表是否存在，列是否存在等。猜测MySQL也这样。</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/d5/88beb15a.jpg" width="30px"><span>李志博</span> 👍（119） 💬（13）<div>应该是分析器吧，老师我还有个问题，如果有memory 引擎，还有redis 存在的必要吗，应该是有的吧，两者的场景？</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（283） 💬（21）<div>我认为是优化器的，优化器会进行优化分析，比如用先执行哪个条件，使用哪个索引。如果没有对应的字段就会报错的，我看其他评论说是执行器，原因是这个时候才打开表获取数据，但是表的字段不是数据啊，是事先定义好的，所以可以直接读取的，不需要打开表。这是我的看法，希望老师点评一下是否正确</div>2018-11-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoKKuJnRI0xFuHWwyXcTRJN5DSic0pGz4uOykEL7SNInMoGHgHfkhgquABeksv9dmfM6Bc42HFk0aQ/132" width="30px"><span>郭</span> 👍（442） 💬（26）<div>有个问题不太明白，为什么对权限的检查不在优化器之前做？</div>2018-11-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epfVZHmbUnsxU67FwotibOjM0Obc47VWMyRBmY06AjqTp0C96A8zhUULWjBerK3XtPC7Q8LVClzPxA/132" width="30px"><span>尼古拉斯·赵四</span> 👍（404） 💬（35）<div>我创建了一个没有select权限的用户，执行select * from T where k=1，报错“select command denied”，并没有报错“unknown column”，是不是可以说明是在打开表之后才判断读取的列不存在？</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（348） 💬（17）<div>为该讲总结了几个问题, 大家复习的时候可以先尝试回答这些问题检查自己的掌握程度:

	1. 
MySQL的框架有几个组件, 各是什么作用? 
	2. 
Server层和存储引擎层各是什么作用?
	3. 
you have an error in your SQL syntax 这个保存是在词法分析里还是在语法分析里报错?
	4. 
对于表的操作权限验证在哪里进行?
	5. 
执行器的执行查询语句的流程是什么样的? 
</div>2018-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bd/c0/57b06721.jpg" width="30px"><span>深藏Blue</span> 👍（234） 💬（12）<div>入手比较晚，说下个人对为什么是分析器的看法。
连接器：门卫，想进请出示准入凭证（工牌、邀请证明一类）。“你好，你是普通员工，只能进入办公大厅，不能到高管区域”此为权限查询。   
分析器：“您需要在公司里面找一张头发是黑色的桌子？桌子没有头发啊！臣妾做不到”
优化器：“要我在A  B两个办公室找张三和李四啊？那我应该先去B办公室找李四，然后请李四帮我去A办公室找张三，因为B办公室比较近且李四知道张三具体工位在哪”
执行器：“好了，找人的计划方案定了，开始行动吧，走你！糟糕，刚门卫大哥说了，我没有权限进B办公室”</div>2019-01-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ9oIRvWZARRmB2hNAmSKOQddHYBJr3QXoT8ibtFicfj46PBOTOwGib6WAA3ES2HzzqqXl4ccEEwrLXw/132" width="30px"><span>yezhizi</span> 👍（156） 💬（10）<div>源码安装完MySQL之后,使用Debug模式启动
mysqld --debug --console &amp;后，
mysql&gt; create database wxb;
Query OK, 1 row affected (0.01 sec)

mysql&gt; use wxb;
Database changed
mysql&gt; create table t(a int);
Query OK, 0 rows affected (0.01 sec)

mysql&gt; select * from t where k=1;
ERROR 1054 (42S22): Unknown column &#39;k&#39; in &#39;where clause&#39;

T@4: | | | | | | | | | error: error: 1054  message: &#39;Unknown column &#39;k&#39; in &#39;where clause&#39;&#39;

Complete optimizer trace:
答案就很清楚了
</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/2c/92c7ce3b.jpg" width="30px"><span>易轻尘</span> 👍（96） 💬（11）<div>靠着耐心翻完所有留言以后，强烈建议极客时间app出一个回到顶部的功能！

另外总结一下在评论中看到的问题的解答
1. 连接器是从权限表里边查询用户权限并保存在一个变量里边以供查询缓存，分析器，执行器在检查权限的时候使用。
2. sql执行过程中可能会有触发器这种在运行时才能确定的过程，分析器工作结束后的precheck是不能对这种运行时涉及到的表进行权限校验的，所以需要在执行器阶段进行权限检查。另外正是因为有precheck这个步骤，才会在报错时报的是用户无权，而不是 k字段不存在（为了不向用户暴露表结构）。
3. 词法分析阶段是从information schema里面获得表的结构信息的。
4. 可以使用连接池的方式，将短连接变为长连接。
5. mysql_reset_connection是mysql为各个编程语言提供的api，不是sql语句。
6. wait_timeout是非交互式连接的空闲超时，interactive_timeout是交互式连接的空闲超时。执行时间不计入空闲时间。这两个超时设置得是否一样要看情况。</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/13/31ea1b0b.jpg" width="30px"><span>峰</span> 👍（85） 💬（6）<div>分析器，感觉老师故意只讲了词法语法解析，却没有讲语义解析。很坏⊙∀⊙！</div>2018-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/3c/47d70fdc.jpg" width="30px"><span>ditiki</span> 👍（71） 💬（1）<div>请问能否在专业名词旁边加上它们的英文名称，比如分析器，优化器等等。谢谢！</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/bc/c1266b7e.jpg" width="30px"><span>400磅</span> 👍（59） 💬（5）<div>总结：
客户端连接到服务端，获取到权限等信息， 然后在连接的有效时长内(interactive_timeout和wait_timeout参数控制， 5.7版本会断开可以自动重连)对sql进行处理。

首先会判断查询缓存是否开启，如果已经开启，会判断sql是select还是update&#47;insert&#47;delete，对于select，尝试去查询缓存，如果命中缓存直接返回数据给客户端， 如果缓存没有命中，或者没有开启缓存， 会进入到下一步分析器。

分析器进行语法分析、词法分析，检查sql的语法顺序等得到解析树， 然后预处理器对解析树进一步分析，验证数据表、字段是否存在，通关之后sql进入下一步优化器，所以课后问题一定是分析器阶段了。

优化器对sql执行计划分析， 得到最终执行计划，得到优化后的执行计划之后交给执行器。

执行器调用存储引擎api执行sql，得到响应结果， 将结果返回给客户端，如果缓存是开启状态， 会更新缓存。

问题1：
    在缓存开启状态下， 要判别sql是select还是其他类型，保证只有select才去查询缓存，那么这个判断操作是何时进行的呢？ 我猜测在查询缓存之前， 但是分析器也要对sql关键字进行分析，再分析一遍岂不是重复？ 因为我没有看源码，所以这一块不明白， 如果我来设计的话， 可能是把查询缓存这个模块在分析器阶段来执行， 由分析器进行关键字解析，判断是何种sql语句，如果是select， 再去查询缓存， 如果不是继续往下进行好像更合理，看到大家都说先查询缓存，没有命中再去分析器， 感觉不太通。
    
问题2：
    在mysql中通过“explain extended和show warnings”命令来查看的sql， 是不是优化器重写之后的sql？ 以前我看到一本书中提到，也可能是一篇博客，mysql的单表的union查询其实会优化成or查询， 但是show warnings看到的还是union查询语句，所以有此疑问。

问题3：
    update等sql清空缓存是在sql执行完返回结果给客户端之前还是之后， 还是说同时进行的， 会不会存在清空缓存失败， 但是告诉客户端update success， 缓存的地方一直不是很清楚， 所以正好 will be removed in a future releas， 真是一个大快人心。</div>2018-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f5/de/c33e531e.jpg" width="30px"><span>Jason</span> 👍（51） 💬（2）<div>1，连接
连接管理模块，接收请求；连接进程和用户模块，通过，连接线程和客户端对接
2，查询
查询缓存 Query Cache
分析器，内建解析树，对其语法检查，先from，再on，再join，再where......；检查权限，生成新的解析树，语义检查（没有字段k在这里）等
优化器，将前面解析树转换成执行计划，并进行评估最优
执行器，获取锁，打开表，通过meta数据，获取数据
3，返回结果
返回给连接进程和用户模块，然后清理，重新等待新的连接

请大神指正😂</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e5/3a/f66372a8.jpg" width="30px"><span>徐远</span> 👍（37） 💬（4）<div>最近开发人员说他们客户端连MySQL时，会有突然断开，然后又自动恢复的情况，我改了connection_timeout参数，但是今天听您介绍说到wait_timeout参数，我有点迷了，请教老师我的情况属于哪种呢</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b1/0e/72590f9c.jpg" width="30px"><span>happyLifehappyGirl</span> 👍（28） 💬（6）<div>刚开始我跟晓斌哥说我要去你专栏下面征婚，他说他去顶帖，所以我买这个专栏不是为了学习……因为我工作可能简单增删改查保证事务一致就够了，况且现在的项目只有缓存没有db，能不学的一定懒得学，最主要的是大神这么厉害我觉得我也学不会。
前天有人说他这个sql要执行一下午，我说你写那么多like废话，你加个索引呗但他那个表只有一列，里面是扩展字段，说加不了索引，所以我也不知道接下来怎么办。

今天打扫卫生想找个东西听，大神还是心目中的大神，深入浅出幽默风趣浅显易懂，小学课文的故事都能拿来当例子开篇，从简单的select开始。我这种技术小白是能不太动脑听得懂的。
推荐给平时需要和数据库打交道的同学，更推荐给做高可用做运维的朋友。
最后，蚂蚁招人，容我打个广告，服务端开发，测试，双十一高可用运维团队，统统招人，喜欢的就是你们这些业余时间还这么爱学习专栏选的还是高质量专栏的，级别没有上限，放眼望去单身白富美一堆（我除外）团队主管好氛围好上升空间大
简历砸来1038248065@qq.com
（为避免被人肉我就先不写公司邮箱了#可能我也是想多了#）
#诶我说好的我来学习的，我今天学了四节了没有骗你#
————我是一条不正经的评论————你还看完了那就砸个简历来一起来快乐工作开心生活</div>2018-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f3/63/c0c4f15d.jpg" width="30px"><span>啊油酱紫哇</span> 👍（26） 💬（1）<div>迫不及待想看第一篇文章。 加班回来收拾下刚好到这个点。 希望自己加油。</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f6/9c/b457a937.jpg" width="30px"><span>不能扮演天使</span> 👍（23） 💬（3）<div>不明白分析器到查询缓存那个箭头代表啥意思？</div>2019-02-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（22） 💬（1）<div>想请问一下老师，最后说的引擎扫描的行数和实际扫描的行数是不一样的，那引擎扫描的行数具体指的是什么？存储引擎只是负责存储和提取吗？那么不同的存储引擎大致有何区别呢？自己只是写过一些简单的SQL语句，从来没有接触过数据库底层，描述不到位的地方还请老师指正，谢谢老师</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/df/e7/4ce5ed27.jpg" width="30px"><span>lunung</span> 👍（20） 💬（3）<div>wait_timeout 是客户端 非交互式的连接时间，如果程序连接mysql SERVER，是交互连接,关联的时间参数为interactive_timeout, 这两个时间参数需要尽量一致吗,一般设置多少合适?
query_cache_size 参数虽然不用了,我想确认下,关闭情况是 query_cache_size=0 要匹配参数query_cache_type=off吗？ 还是直接query_cache_size=0 即可？</div>2018-11-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL17yp3TmdQNXWELQvjIA2azwZ6ib7Riae9Hcf2YFl1uvnvocQoicTOtJLnvjUPtpbYhSng7DtPR9lfg/132" width="30px"><span>wvalianty</span> 👍（14） 💬（1）<div>1、mysql主要组成部分，连接器，优化器，执行器，存储引擎。
2、连接器，验证账号密码，维持链接，超时自动断开，链接过程复杂，建议使用长链接，连接比较占用内存，需要定时断开，5.7之后可以使用mysql_reset_connection。
3、分析器，验证语法的合规性，把sql转换成mysql内部识别的语句，表明转换成对应的id。
4、判断sql内部的执行顺序。
5、执行器，验证操作库表是否有权限，调存储引擎接口查询数据。
6、慢查询日志rows_examined，记录查询的时候扫描了多少行，相同表有肯能次数不同。</div>2019-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/0b/20123c7a.jpg" width="30px"><span>fireflyc</span> 👍（11） 💬（6）<div>图片用什么画的？方便告知一下名字吗？</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/20/3a/90db6a24.jpg" width="30px"><span>Long</span> 👍（11） 💬（2）<div>老师你好，准备重新复习所有的课程。
每天都在等你的更新，每篇都能学到新的知识。希望把我之前回答别人的数据库知识时候的词语：应该，估计，我理解，可能是。。。这样的一些词语都渐渐去除了。

这边有2个问题：复习第一篇的时候发现2个疑问，认真看了大部分留言后发现问题没有关闭，特此再问下：
问题1：和下面三位同学有类似的疑问：关于没有权限操作表的时候的报错：
@von，@尼古拉斯赵四，@学徒（可以直接评论区搜索这些同学的名字）
如果分析器已经知道了“unknown column”之后，为什么还会报错：“select command denied”。你之前的回答是：由于安全考虑，用户没有权限操作这个表，那么也不需要告诉用户这么多，直接告诉用户没有权限。

【重点疑问】如果是按照这样的话，且对表的权限检查都在执行器的话，那么每个sql在执行的时候至少都会执行到执行器吗？

因为同时看到文中在执行器章节：于是就进入了执行器阶段，开始执行语句。开始执行的时候，要先判断一下你对这个表 T 有没有执行查询的权限，如果没有，就会返回没有权限的错误，如下所示。
SELECT command denied to user &#39;b&#39;@&#39;localhost&#39; for table &#39;T&#39;


问题2：两位测试结果不一样
@yezhizi 
yezhizi的测试结果是Complete optimizer trace:
@黑龍Dr夢，从他的描述来看，测试结果应该是分析器

没有本项目上的MySQL权限，等明天自己本地版下好后，测试下结果。
也请老师也帮忙分析下我的疑惑，多谢。</div>2019-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/70/97/e5bf9ddb.jpg" width="30px"><span>橡皮泥boy</span> 👍（11） 💬（4）<div>【对文章的疑问】
老师好，文里遇到临时内存会跟随长连接的存在而存在，直到连接被销毁。
我想问对是，这部分临时内存是由于什么产生？为什么不提前释放呢？mysql有用到内存池吗？</div>2018-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/eb/a5/f28bfac7.jpg" width="30px"><span>Harley</span> 👍（10） 💬（1）<div>现在有一个普通用户的长连接，权限是select，现在我另开一个root用户会话，把这个普通用户的权限做了修改，加上了insert的权限，在没有断开这个普通用户的长连接，但是发现该长连接可以进行insert，这个现象跟文中所说的已经存在的长连接必须要先断开才可以应用新权限是冲突的。请问这是什么原因？</div>2019-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ed/a1/d2953af8.jpg" width="30px"><span>Together</span> 👍（10） 💬（5）<div>【对权限检验的一点疑问】在连接器里已经做过了权限验证，为什么在执行器里还要再做一次？</div>2018-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/df/04/ca6e1f76.jpg" width="30px"><span>苍天大树</span> 👍（9） 💬（1）<div>两个不同引擎的mysql 表能联表查询吗？</div>2018-12-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIKa0PdjFnEpvGFBcED2P28ugPmwwRoCbeUfulpGEye8964F4nwChQyVfgVUia74TyDISvXTYJfQpA/132" width="30px"><span>Nick</span> 👍（9） 💬（1）<div>文中join的例子，内表和外表 都有高区分度条件的情况下，先过滤出两表符合条件的记录，再对这些记录做join，可不可以？感觉这样性能更高。</div>2018-11-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/RNO4yZyBvic914hewmNNE8iblYDcfv5yGHZ9OnKuCuZXNmGR0F5qV3icKLT2xpMt66GyEpicZVvrmz8A6TIqt92MQg/132" width="30px"><span>啊啊啊哦哦</span> 👍（8） 💬（1）<div>短链接。  假设 代码执行2次select语句。  每次都会重新建立连接吗</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2f/47/eadc8482.jpg" width="30px"><span>luoChao</span> 👍（8） 💬（3）<div>为什么那个逻辑架构图，会有从分析器指向查询缓存的→箭头。</div>2018-12-28</li><br/>
</ul>