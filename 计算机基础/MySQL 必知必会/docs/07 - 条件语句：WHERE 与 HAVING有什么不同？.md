你好，我是朱晓峰。

我们在进行查询的时候，经常需要按条件对查询结果进行筛选，这就要用到条件语句WHERE和HAVING了。

WHERE是直接对表中的字段进行限定，来筛选结果；HAVING则需要跟分组关键字GROUP BY一起使用，通过对分组字段或分组计算函数进行限定，来筛选结果。虽然它们都是对查询进行限定，却有着各自的特点和适用场景。很多时候，我们会遇到2个都可以用的情况。一旦用错，就很容易出现执行效率低下、查询结果错误，甚至是查询无法运行的情况。

下面我就借助项目实施过程中的实际需求，给你讲讲WHERE和HAVING分别是如何对查询结果进行筛选的，以及它们各自的优缺点，来帮助你正确地使用它们，使你的查询不仅能够得到正确的结果，还能占用更少的资源，并且速度更快。

## 一个实际查询需求

超市的经营者提出，要查单笔销售金额超过50元的商品。我们来分析一下这个需求：需要查询出一个商品记录集，限定条件是单笔销售金额超过50元。这个时候，我们就需要用到WHERE和HAVING了。

这个问题的条件很明确，查询的结果也只有“商品”一个字段，好像很容易实现。

假设我们有一个这样的商品信息表（demo.goodsmaster），里面有2种商品：书和笔。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLZKoB7sooIiaCHqcdNGI97WI3ZJLJph4mibIiat1qRvrBmkicZTEYvyT5iax1vlLFFgk2xgUibmnWvkicWA/132" width="30px"><span>朱晓峰</span> 👍（6） 💬（1）<div>你好，我是朱晓峰，下面我就来公布一下上节课思考题的答案：

上节课，我们学习了如何进行多表查询。下面是思考题的答案：

如果不能使用外键约束，你可以在应用层增加确保数据完整性的功能模块，比如删除主表记录时，增加检查从表中是否应用了这条记录的功能，如果应用了，就不允许删除。</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/01/2e/5d3d4b86.jpg" width="30px"><span>青雘</span> 👍（6） 💬（1）<div>有数据库的数据包吗 ？ 这咋动手 没有数据</div>2021-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c9/23/76511858.jpg" width="30px"><span>洛奇</span> 👍（6） 💬（3）<div>筛选条件放在ON或者WHERE子句中，都是一样的吧？</div>2021-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/bd/6d/7010f98e.jpg" width="30px"><span>SharpBB</span> 👍（2） 💬（1）<div>WHERE
	直接用表字段对数据集进行筛选 得到较少的数据集 再进行连接 资源占用少 执行效率高
HAVING
	需要将数据准备好 并进行分组形成集合 再对该集合进行having条件的筛选
两者区别
	1.where先筛选后连接 having先连接后筛选 where的效率更高
	2.where可以直接用 而having必须和group by一起用才可以
	3.可以在having中用函数 但where不行 所以having可以做一些更nb的查询</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/28/69/b013f07d.jpg" width="30px"><span>hello</span> 👍（1） 💬（1）<div>sql语句的执行顺序，不是先执行join 再执行where吗？老师在提到where优点的时候说where的优点是先筛选在关联。这里似乎跟sql执行的顺序有了矛盾呢</div>2021-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/52/56/6ac8be3c.jpg" width="30px"><span>Cheese</span> 👍（0） 💬（1）<div>group by不是很理解，和having配合在一起使用有点懵了。</div>2022-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0d/78/aa5f920d.jpg" width="30px"><span>Bird</span> 👍（0） 💬（3）<div>老师您好，用 HAVING 查询单笔超过 50 元商品的 SQL 中，用到了 HAVING max(a.salesvalue)&gt;50

这个 max() 我不太理解，是指在分组后对每个组中的 salesvalue 取最大值再和 50 比较吗？

这块不明白导致后面原文说的“第三步，对分组后的数据集进行筛选，把组中字段“salesvalue”的最大值 &gt;50 的组筛选出来。”就更不明白了。

我的疑问是，需求是找到比 50 大的就好，不理解这里为什么用到求最大值。求的是哪些数据范围的最大值呢？</div>2021-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/e6/eb/7b7c0101.jpg" width="30px"><span>彭彬</span> 👍（0） 💬（1）<div>HAVING 后面的条件，必须是包含分组中的计算函数的条件，或者select后面的字段</div>2021-09-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLzJr3dmr96ULaeQQJrslQcSZfH8fwPug8q42Y69q0daYarUbx1b0U1iadjcTtOmUicDnlx968SLLkw/132" width="30px"><span>born</span> 👍（0） 💬（1）<div>在“查询单笔销售金额超过 50 元的商品”例子中的第三步，GROUP BY只用goodsname字段结果只返回了组中的第一条数据，想要返回图示中的两条数据还要添加另外的字段吧</div>2021-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/95/11/eb431e52.jpg" width="30px"><span>沈康</span> 👍（0） 💬（1）<div>有这样一种说法：HAVING 后面的条件，必须是包含分组中的计算函数的条件，你觉得对吗？为什么？

我认为是对的，既然 having是在group之后的筛选，那么只能选择group的计算函数</div>2021-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c9/23/76511858.jpg" width="30px"><span>洛奇</span> 👍（0） 💬（1）<div>本文中最后一条SQL的两处SUM(b.salesvalue)是不是会重复计算？它们可以合并吗？</div>2021-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（11） 💬（6）<div>之前刚学习数据库的时候，也会混淆WHERE和HAVING。今天学习了这一节，又有了更加清晰地认知。

WHERE是针对数据库文件的发挥作用，而HAVING是针对结果集发挥作用。WHERE所能作用的字段条件要是数据表文件中真实存在的字段，而having只是根据前面查询出来的结果集再次进行查询。

这样看来HAVING后面不一定要是包含分组中的计算函数的条件。例如以下两条语句就是等效的：

select goods_price, goods_name from goods where goods_price &lt; 100

select goods_price, goods_name from goods having goods_price &lt; 100
</div>2021-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/95/77f5aa52.jpg" width="30px"><span>不管</span> 👍（2） 💬（0）<div>对于0基础的来说这个还是太难了</div>2022-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0f/97/372d8628.jpg" width="30px"><span>星空下</span> 👍（2） 💬（0）<div>having可以替代where  只是要与group by联合使用。后跟条件不一定是分组函数</div>2021-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/a1/03/dff6bc2f.jpg" width="30px"><span>me</span> 👍（1） 💬（0）<div>SQL逻辑查询语句执行顺序 
不应该是连表后再where嘛？ （下方是执行顺序）
SELECT DISTINCT &lt;select_list&gt;
FROM &lt;left_table&gt;
&lt;join_type&gt; JOIN &lt;right_table&gt;
ON &lt;join_condition&gt;
WHERE &lt;where_condition&gt;
GROUP BY &lt;group_by_list&gt;
HAVING &lt;having_condition&gt;
ORDER BY &lt;order_by_condition&gt;
LIMIT &lt;limit_number&gt;</div>2022-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2e/7e/a15b477c.jpg" width="30px"><span>Noya</span> 👍（0） 💬（0）<div>在MySQL中，查询的执行顺序通常是这样的：

FROM &#47; JOIN: 首先执行FROM和JOIN子句以确定被查询的数据集​1​.
WHERE: 然后执行WHERE子句以过滤不满足条件的记录​2​​3​.
GROUP BY: 如果存在GROUP BY子句，则在WHERE子句之后执行，以基于一个或多个列的值对数据进行分组​2​​3​.
HAVING: 在GROUP BY子句之后执行HAVING子句，以过滤不满足条件的组​4​​3​.
这种执行顺序可以确保在连接表并应用WHERE子句过滤记录之后，再应用GROUP BY和HAVING子句。所以，是的，你的陈述基本上是正确的：WHERE子句是在连接（JOIN）操作之后、在HAVING子句之前执行的，而HAVING子句是在连接（JOIN）和WHERE子句之后执行的。</div>2023-10-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/j24oyxHcpB5AMR9pMO6fITqnOFVOncnk2T1vdu1rYLfq1cN6Sj7xVrBVbCvHXUad2MpfyBcE4neBguxmjIxyiaQ/132" width="30px"><span>vcjmhg</span> 👍（0） 💬（0）<div>不是的，普通的查询条件也是可以放在后面的</div>2023-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/62/f99b5b05.jpg" width="30px"><span>曙光</span> 👍（0） 💬（0）<div>“单笔销售金额超过 50 元的商品”，感觉有歧义，一笔销售金额有两个商品，且相加大于50，如果max(a.salesvalue)&gt;50，会丢失“书”这个商品。
老师用GROUP BY b.goodsname做分组，用max查结果，我的理解是，”查不同类型的商品，且价格有超过50&quot;</div>2022-09-25</li><br/>
</ul>