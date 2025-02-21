你好，我是吴磊。

上一讲我们说，Spark SQL已经取代Spark Core成为了新一代的内核优化引擎，所有Spark子框架都能共享Spark SQL带来的性能红利，所以在Spark历次发布的新版本中，Spark SQL占比最大。因此，Spark SQL的优化过程是我们必须要掌握的。

Spark SQL端到端的完整优化流程主要包括两个阶段：Catalyst优化器和Tungsten。其中，Catalyst优化器又包含逻辑优化和物理优化两个阶段。为了把开发者的查询优化到极致，整个优化过程的运作机制设计得都很精密，因此我会用三讲的时间带你详细探讨。

下图就是这个过程的完整图示，你可以先通过它对优化流程有一个整体的认知。然后随着我的讲解，逐渐去夯实其中的关键环节、重要步骤和核心知识点，在深入局部优化细节的同时，把握全局优化流程，做到既见树木、也见森林。

![](https://static001.geekbang.org/resource/image/f3/72/f3ffb5fc43ae3c9bca44c1f4f8b7e872.jpg?wh=6539%2A1200 "Spark SQL的优化过程")

今天这一讲，我们先来说说Catalyst优化器逻辑优化阶段的工作原理。

## 案例：小Q变身记

我们先来看一个例子，例子来自电子商务场景，业务需求很简单：给定交易事实表transactions和用户维度表users，统计不同用户的交易额，数据源以Parquet的格式存储在分布式文件系统。因此，我们要先用Parquet API读取源文件。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/20/d6/b9513db0.jpg" width="30px"><span>kingcall</span> 👍（37） 💬（3）<div>问题1：开发阶段要有极客精神，尽量将优化实现在自己的代码里，而不是依赖框架，因为框架是一个普世的优化，还有就是如果我们根据业务特点进行了优化再加上框架本身带来的优化能给我们的程序带来一个更好的性能提升,也就是说上层自我优化和底层框架优化。
问题2：与偏函数对应的一个定义就是我们数学意义上的函数，一个输入自变量x对应一个输出因变量y，也就是y 可以表示成x 的一个特定的运算，并且这个运算关系是确定的，但是scala 中的偏函数它表示的是一种匹配关系，有点类似if else if ... else ，只有匹配上了才有对应的值，否则输出的就是默认值
Spark 之所以用偏函数，而不是普通函数来定义 Catalyst 的优化规则，是因为规则是预先定义的，不可能满足所有的情况，所以需要一个兜底，而这正好满足偏函数的特点。
</div>2021-04-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo2GMhevabZrjINs2TKvIeGC7TJkicNlLvqTticuM5KL8ZN80OC2CnrsUyzPcZXO4uptj4Q1S4jT2lQ/132" width="30px"><span>jerry guo</span> 👍（8） 💬（3）<div>1. 既然 Catalyst 在逻辑优化阶段有 81 条优化规则，我们还需要遵循“能省则省、能拖则拖”的开发原则吗？你能说说 Spark 为什么用偏函数，而不是普通函数来定义 Catalyst 的优化规则吗？
答：要。战略上用开发原则，战术上依赖Catalyst。

2.你能说说 Spark 为什么用偏函数，而不是普通函数来定义 Catalyst 的优化规则吗？
答：网上搜到一篇文章
&quot;The pattern matching expression that is passed to transform is a partial function, meaning that it only needs to match to a subset of all possible input trees. Catalyst will tests which parts of a tree a given rule applies to, automatically skipping over and descending into subtrees that do not match. This ability means that rules only need to reason about the trees where a given optimization applies and not those that do not match. Thus, rules do not need to be modified as new types of operators are added to the system.&quot; 这段不是很懂，大概意思是因为偏函数没有包括所有的情况，所以正好，符合定义的rule就优化，不符合就不处理，这样子比较省事；另外由于一开始没有完全定义出全部的情况（可能也定义不出来），所以这也有一定的灵活性，再新加了operator之后，也不需要改rule了。望老师指点。 

3. 另外我有个问题，RDBMS的SQL优化很早之前是基于Rule，后面变成了基于Cost。根据本篇的讲解，Catalyst和Tunsgen，都是基于Rule的，网上搜索了一下，Catalyst也可以基于cost。老师可以讲讲对CBO的看法吗？比如CBO如何和Catalyst，Tusgen一起工作？或者以后CBO会变成主流吗？</div>2021-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/26/db/27724a6f.jpg" width="30px"><span>辰</span> 👍（4） 💬（1）<div>老师，执行计划中的project是什么意思啊，大概知道是和映射的关系，可不可以理解成相当于action算子一样</div>2021-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/53/dcec6fdc.jpg" width="30px"><span>mini希</span> 👍（4） 💬（1）<div>老师好，针对列剪裁是否只有列式的存储才能享受到扫描的优化效果，行存还是会扫描整行所有字段？</div>2021-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/a2/5252a278.jpg" width="30px"><span>对方正在输入。。。</span> 👍（3） 💬（1）<div>老师的课，我是越看越爽，看完就有一种“老子天下无敌了”的感觉，哈哈哈哈哈</div>2021-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/55/41/b68df312.jpg" width="30px"><span>农夫三拳</span> 👍（1） 💬（2）<div>老师 想问个问题，这个缓存是根据 查询树或者查询树的一部分作为key，进行缓存，匹配到了 就替换当前节点或者整棵树。  请问下 这个缓存是针对哪个阶段的查询树呢？是  解析，优化前，优化后，还是物理计划阶段？  我个人理解是优化后阶段。</div>2021-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/65/0f/7b9f27f2.jpg" width="30px"><span>猿鸽君</span> 👍（1） 💬（3）<div>请问老师知道sparksql有时在执行insert overwrite hive table（静态分区）特别慢的原因吗？我翻了内外网都只给出了解决方案，却没有原因……</div>2021-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（1） 💬（1）<div>偏函数只针对部分输入来输出结果，而每个函数对应的优化规则也是有限的，再搭配模式匹配，很完美的应用场景哈哈</div>2021-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/09/7f2bcc6e.jpg" width="30px"><span>sky_sql</span> 👍（1） 💬（1）<div>老师好，RDD api有点类似MR编程，Spark SQL有点类似hive，过程都包括使用 Antlr 实现 SQL 的词法和语法解析，后面也有Schema 信息验证，优化环节谓词下推、列剪裁等？</div>2021-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5d/b6/bedadca5.jpg" width="30px"><span>Marco</span> 👍（0） 💬（1）<div>spark只用启发式的规则优化吗，有没有基于成本模型的优化？</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a2/4b/b72f724f.jpg" width="30px"><span>zxk</span> 👍（0） 💬（1）<div>问题1：Spark 里的优化只是一种普世的优化，力求在尽可能覆盖绝大部分通用场景，减少对开发者的要求。但实际开发中场景千差万别，Spark 不一定能覆盖到所有场景，因此仍需要我们尽可能遵循这些开发原则。
问题2：对偏函数不是很熟悉，猜测是尽可能的拆解函数粒度，给 Spark 留出更多的优化空间。比如之前老师就有个 label encoding 的例子，将函数拆分为偏函数后，Spark 自动进行优化，性能有很大提升。</div>2021-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b2/9c/b7b9896c.jpg" width="30px"><span>王云峰</span> 👍（0） 💬（0）<div>谢谢作者，我悟道了</div>2023-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/a3/f2/ab8c5183.jpg" width="30px"><span>Sampson</span> 👍（0） 💬（1）<div>磊哥，想请问下在逻辑计划解析阶段是否应该还有词法解析，语法解析等步骤？如果有的话，是使用的什么方式做的呢 ？ </div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/20/9e/145df9a3.jpg" width="30px"><span>liangzai</span> 👍（0） 💬（2）<div>从cache manager中查询计划，这个没太懂，请问这个缓存的计划是从哪里来的呢？</div>2022-05-28</li><br/>
</ul>