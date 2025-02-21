从今天开始我们就进入了专栏的第三个模块，一起来看看大数据开发实践过程中的门道。学习一样技术，如果只是作为学习者，被动接受总是困难的。**但如果从开发者的视角看，很多东西就豁然开朗了，明白了原理，有时甚至不需要学习，顺着原理就可以推导出各种实现细节**。

各种知识从表象上看，总是杂乱无章的，如果只是学习这些繁杂的知识点，固然自己的知识面是有限的，并且遇到问题的应变能力也很难提高。所以有些高手看起来似乎无所不知，不论谈论起什么技术，都能头头是道，其实并不是他们学习、掌握了所有技术，而是他们是在谈到这个问题的时候，才开始进行推导，并迅速得出结论。

我在Intel的时候，面试过一个交大的实习生，她大概只学过一点MapReduce的基本知识，我问她如何用MapReduce实现数据库的join操作，可以明显看出她没学习过这部分知识。她说：我想一下，然后盯着桌子看了两三秒的时间，就开始回答，基本跟Hive的实现机制一样。从她的回答就能看出这个女生就是一个高手，高手不一定要很资深、经验丰富，把握住了技术的核心本质，掌握了快速分析推导的能力，能够迅速将自己的知识技能推进到陌生的领域，就是高手。

这也是我这个专栏的目的，讲述大数据技术的核心原理，分享一些高效的思考和思维方式，帮助你构建起自己的技术知识体系。
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/40/10/b6bf3c3c.jpg" width="30px"><span>纯洁的憎恶</span> 👍（36） 💬（1）<div>基于SQL的大数据仓库引擎panthera的核心任务是把SQL语义与Hive AST对应起来。难点是SQL的语义远比Hive AST丰富，而幸运的事SQL丰富的表意逻辑主要源于它的嵌套子语句，这在Hive AST中是不存在的。但是SQL的嵌套子语句可以等价于若干jion操作。

为了在工程上降低实现难度，特意为每个语法点设计一个对象（类），这就将复杂问题分解为无数个小步骤，可以持续交付，不用长期等待，从而将不可能有条件的变为可能。而且每个类的代码十分简洁，遇到问题也便于各个击破。</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（32） 💬（1）<div>Oracle会有走向衰落吗？</div>2018-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/10/b4/00680e1f.jpg" width="30px"><span>反应慢</span> 👍（5） 💬（1）<div>之前有一段时间在学习函数式编程，和sql一样属于命令式编程，所以感觉以函数去解析sql是水到渠成的事情。不过至今没有动手去实现一下，比较遗憾</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/25/d78cc1fe.jpg" width="30px"><span>都市夜归人</span> 👍（1） 💬（3）<div>   private static SqlASTTransformer tf =
      new RedundantSelectGroupItemTransformer(
      new DistinctTransformer(
      new GroupElementNormalizeTransformer(
      new PrepareQueryInfoTransformer(
      new OrderByTransformer(
      new OrderByFunctionTransformer(
      new MinusIntersectTransformer(
      new PrepareQueryInfoTransformer(
      new UnionTransformer(
      new Leftsemi2LeftJoinTransformer(
      new CountAsteriskPositionTransformer(
      new FilterInwardTransformer(
      &#47;&#47;use leftJoin method to handle not exists for correlated
      new CrossJoinTransformer(
      new PrepareQueryInfoTransformer(
      new SubQUnnestTransformer(
      new PrepareFilterBlockTransformer(
      new PrepareQueryInfoTransformer(
      new TopLevelUnionTransformer(
      new FilterBlockAdjustTransformer(
      new PrepareFilterBlockTransformer(
      new ExpandAsteriskTransformer(
      new PrepareQueryInfoTransformer(
      new CrossJoinTransformer(
      new PrepareQueryInfoTransformer(
      new ConditionStructTransformer(
      new MultipleTableSelectTransformer(
      new WhereConditionOptimizationTransformer(
      new PrepareQueryInfoTransformer(
      new InTransformer(
      new TopLevelUnionTransformer(
      new MinusIntersectTransformer(
      new NaturalJoinTransformer(
      new OrderByNotInSelectListTransformer(
      new RowNumTransformer(
      new BetweenTransformer(
      new UsingTransformer(
      new SchemaDotTableTransformer(
      new NothingTransformer())))))))))))))))))))))))))))))))))))));
这个类在使用的时候该有多麻烦啊？</div>2019-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/3c/eee3e6f5.jpg" width="30px"><span>galen</span> 👍（29） 💬（1）<div>因为SQL语句在程序运行前已经进行了预编译，在程序运行时第一次操作数据库之前，SQL语句已经被数据库分析，编译和优化，对应的执行计划也会缓存下来并允许数据库已参数化的形式进行查询，当运行时动态地把参数传给PreprareStatement时，即使参数里有敏感字符如 or &#39;1=1&#39;也数据库会作为一个参数一个字段的属性值来处理而不会作为一个SQL指令，如此，就起到了SQL注入的作用了</div>2018-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/53/b8fe4560.jpg" width="30px"><span>欧嘉权Felix</span> 👍（15） 💬（0）<div>如果用statement jdbc会简单拼接字符串然后作为sql执行
preparedstatement就会进行预编译 对其中的换行符等字符做转义 对注入的sql会起到混淆的作用
mybatis这些orm框架也是基于preparedstatement mybatis尽量使用#占位符</div>2018-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/15/c3/d8564fe2.jpg" width="30px"><span>Well_Ksun</span> 👍（9） 💬（0）<div>老师能简单聊聊presto吗？也是faceboook开源出来的。据说AWS 的 Athena 就是基于 Presto 的产品。</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cb/50/66d0bd7f.jpg" width="30px"><span>杰之7</span> 👍（8） 💬（0）<div>从这篇文章开始，大数据技术的体系架构知识就告一段落，但并不意味着已经完全掌握，我需要不断的回顾体系架构原理，这样才会有可能沿着这个思路有自己的一点拓展。回到本篇内容，如何自己开发SQL引擎，由于Hive语法元素少于标准SQL,且不支持复杂的嵌套子查询，所以开发的难点就是如何将复杂嵌套消除转化成标准SQL。在老师讲述的过程中，主要通过装饰模式等价转化类的构造，对于每一种新的语法通过开发新的Transformer类，然后通过组合模式将抽象语法树AST进行遍历，最后转化成Hive格式的抽象语法树。通过这样的整个过程，就完成的对Hive语法解析器的替换，保留了Hive语义分析器。通过本节的学习，我相信老师说的这套思路，那些技术厉害的人不是掌握了每一种技术，而是掌握了技术背后的体系和原理，当有新的技术出现时，同样先去思考技术背后的原理是什么，这样就算没有参与其中的技术，也会新的技术有一个好的认识。</div>2018-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/43/50/ef2cfbce.jpg" width="30px"><span>蒙</span> 👍（6） 💬（0）<div>sql预编译，应该是将原始sql先解析成语法树，入参不能影响语法树的变化</div>2020-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ad/07/20e7d3cf.jpg" width="30px"><span>GeekGay</span> 👍（4） 💬（0）<div>https:&#47;&#47;github.com&#47;lealone

来看看我们桂林的大才子zhh-4096，一个人开发6年的列锁极数据库，之前也去淘宝做个一两年数据库产品的。</div>2019-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/be/693b5e5e.jpg" width="30px"><span>周翔</span> 👍（4） 💬（0）<div>预编译就是sql命令的模板归模板，参数归参数，参数就不会混合到原sql，改变原有的sql语句和执行逻辑。除了数据访问框架本身prepare statement功能，还可以从服务层接收参数就可以屏蔽。</div>2018-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e1/e7/d1b2e914.jpg" width="30px"><span>明亮</span> 👍（3） 💬（1）<div>可以推荐一些SQL解析的来源产品和资料吗
</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/c5/c9a67483.jpg" width="30px"><span>Oliver</span> 👍（3） 💬（0）<div>保证用户输入的内容仅仅且只能作为查询条件，涉及一些字符转义操作</div>2018-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/a2/33be69a6.jpg" width="30px"><span>毛毛</span> 👍（2） 💬（0）<div>PreparedStatement会先初始化SQL，语句中只有部分变量可以被“？”替代，所以sql注入的攻击方式无效。</div>2018-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/08/1c/ef15e661.jpg" width="30px"><span> 臣馟飞扬</span> 👍（1） 💬（0）<div>貌似Panthera项目没有掀起任何波澜。。。</div>2020-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/ba/032800bc.jpg" width="30px"><span>cwx0220</span> 👍（1） 💬（0）<div>正常情况下，当http请求参数带有sql语句的条件时，在 SQL 注入中，参数值作为 SQL 指令的一部分，会被数据库进行编译&#47;解释执行。当使用了 PreparedStatement，带占位符 ( ? ) 的 sql 语句只会被编译一次，之后执行只是将占位符替换为参数值，并不会再次编译&#47;解释，因此从根本上防止了 SQL 注入问题。</div>2019-03-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLrlbht91jCquMssicPD3LjnQI2ialTPMfA7ia6Htkw37NicUZFHjfVr0GVgGtoCPgRVCgNG7hmPzoLsQ/132" width="30px"><span>Geek_43ecfe</span> 👍（0） 💬（0）<div>就我个人实践而言，为了能让 NOT IN 计算结果符合 SQL 标准，Left Outer Join 改写是不够的，处理 Null 值方面存在欠缺；比如 1 NOT IN (Null, 2, 3) 按照 SQL 标准计算结果是 Unknown（1 &lt;&gt; Null AND 1&lt;&gt;2 AND 1&lt;&gt;3），作为 Where 条件的话 1 对应的记录会被过滤，实际使用 Left Outer Join 重写的话，1 对应的记录由于没有 IN List 元素匹配，会被 Left Outer Join 补 Null，最后通过 IS NULL 保留。。。。</div>2024-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2f/b4/35a23718.jpg" width="30px"><span>zhaixc</span> 👍（0） 💬（0）<div>李老真的厉害，用一些看似简单的方法，解决非常复杂的问题，然后还有很好的效果。</div>2024-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7a/93/c9302518.jpg" width="30px"><span>高志强</span> 👍（0） 💬（0）<div>&quot;希望让那些在 Oracle 上运行良好的 SQL 可以直接运行在 Hadoop 上~&quot; 我在想不经过hive语法分析器直接提交到hadoop运行多好啊</div>2023-10-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJUzv6S9wroyaa2CANjhHJcwRwNESncu4lfWTtdkMh3viaVCgEg5vMXFJ4Ne4SaDtLNd9dvkUrFqPg/132" width="30px"><span>精思入神</span> 👍（0） 💬（0）<div>这节最大的启发是，要从设计者的角度去理解，而不是老以学习者自居。否则，永无出头之日矣。</div>2022-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>猜测数据库引擎会通过某种方式，把参数就用作参数而不会作为SQL语句去执行。
凡事常用带入创造者的方式去思考，确实是个好方法，长期训练也许，真能做到庖丁解牛的效果。</div>2019-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（0）<div>Hive QL也支持预编译吗？</div>2019-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/25/898dea4e.jpg" width="30px"><span>桃园悠然在</span> 👍（0） 💬（0）<div>请问老师，如果目前手头使用的hive可以支持嵌套子查询，是否说明已经定制优化过了？</div>2018-12-29</li><br/>
</ul>