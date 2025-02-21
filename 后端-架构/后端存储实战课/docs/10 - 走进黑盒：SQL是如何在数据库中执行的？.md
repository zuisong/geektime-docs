你好，我是李玥。

上一节课我们讲了怎么来避免写出慢SQL，课后我给你留了一道思考题：在下面这两个SQL中，为什么第一个SQL在执行的时候无法命中索引呢？

```
SELECT * FROM user WHERE left(department_code, 5) = '00028';
SELECT * FROM user WHERE department_code LIKE '00028%';
```

原因是，这个SQL的WHERE条件中对department\_code这个列做了一个left截取的计算，对于表中的每一条数据，都得先做截取计算，然后判断截取后的值，所以不得不做全表扫描。你在写SQL的时候，尽量不要在WEHER条件中，对列做任何计算。

到这里这个问题就结束了么？那我再给你提一个问题，这两个SQL中的WHERE条件，虽然写法不一样，但它俩的语义不就是一样的么？是不是都可以解释成：department\_code这一列前5个字符是00028？从语义上来说，没有任何不同是吧？所以，它们的查询结果也是完全一样的。那凭什么第一条SQL就得全表扫描，第二条SQL就可以命中索引？

对于我们日常编写SQL的一些优化方法，比如说我刚刚讲的：“尽量不要在WEHER条件中，对列做计算”，很多同学只是知道这些方法，但是却不知道，为什么按照这些方法写出来的SQL就快？

要回答这些问题，需要了解一些数据库的实现原理。对很多开发者来说，数据库就是个黑盒子，你会写SQL，会用数据库，但不知道盒子里面到底是怎么一回事儿，这样你只能机械地去记住别人告诉你的那些优化规则，却不知道为什么要遵循这些规则，也就谈不上灵活运用。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/51/f7/93020ae2.jpg" width="30px"><span>李鑫</span> 👍（29） 💬（5）<div>老师好,看了你的课程 感觉有点浅，比如这一篇只是简单介绍了下索引和数据的底层存储结构。像页分裂这些更加底层的没有讲到，建议老师后续的课程可以由浅入深。</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fc/9b/0e79a034.jpg" width="30px"><span>暴力的小石头</span> 👍（5） 💬（2）<div>我想问一下，文中提到逻辑执行计划，就是那个像函数调用栈的东西是怎么得来的呀，感觉比explain分析的更深层次，想问一下如何分析出来的</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>存储引擎再执行执行计划的的时候，是把整个执行计划执行完成后把数据返给执行器，还是每执行一条执行计划获取数据就返给执行器，然后执行器在做运算的？
个人认为是整个执行计划执行完成后获得最终的数据在返给执行器，但是这个有没有办法去验证的？</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/4e/d71092f4.jpg" width="30px"><span>夏目</span> 👍（28） 💬（1）<div>主键除了不能太长之外最好能有序，有序的话能减少插入时B+树的排序操作，所以uuid这种不适合做主键</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4c/83/7788fc66.jpg" width="30px"><span>Simon</span> 👍（15） 💬（1）<div>文中说: 每一行数据直接就保存在 B+ 树的叶子节点上
这句话可能会有误会, 
实际上B+树的节点存的是&quot;页&quot;, 而具体的数据在页里面</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/da/dd/1e5e7b0c.jpg" width="30px"><span>image</span> 👍（6） 💬（0）<div>比较典型的是Hive，不少开源组件直接借用其SQL解析器，完成逻辑层优化，物理层用其他方式执行。</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3c/52/5951ffb4.jpg" width="30px"><span>Sinvi</span> 👍（4） 💬（0）<div>推荐隔壁《SQL必知必会》这里有讲比较详细</div>2020-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/69/187b9968.jpg" width="30px"><span>南山</span> 👍（4） 💬（0）<div>很赞同为什么要了解原理的原因，只有知道原理以及内部执行逻辑，遇到问题才能不会像无头苍蝇一样靠运气和蒙。</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/a6/3bddb98c.jpg" width="30px"><span>大叶枫</span> 👍（3） 💬（0）<div>建议配合实际工作场景得问题，逐步深入的来解执行计划的实战用途。</div>2020-03-19</li><br/><li><img src="" width="30px"><span>Geek_fe19fb</span> 👍（2） 💬（0）<div>索引失效的原因：
1. 没有正确的使用like
2. 使用了or  ，索引是符合索引，单列索引是可以的  （跟版本有关系 在MySQL8.0）
3. 不符合前缀索引的用法，带头大哥不能死
4. 索引列使用了函数
5. 索引列类型不一致，导致索引失效
6. 索引列字符集不一致
7. 使用了不等于
8. 范围查询之后的索引都会失效</div>2022-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/90/a8d19e7b.jpg" width="30px"><span>张理查</span> 👍（2） 💬（0）<div>如何diss SQL写得不咋地：并不是说你 SQL 写的不好，而是数据库还不够智能</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>MySQL  的执行计划是如何进行查看的？</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>优化的总体思路是，在执行计划中，尽早地减少必须处理的数据量。--记下来</div>2022-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2022-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/b9/73435279.jpg" width="30px"><span>学习学个屁</span> 👍（0） 💬（1）<div>老师 请问 尽早地执行投影，去除不需要的列；
a,b2表 Join 数据两个都很大, 我在表连接之前 例如 a 表 子查询 条件&gt;50 后 再和b join 这样子也可以尽早的执行投影,不知理解的对吗?  </div>2020-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/6b/e9/7620ae7e.jpg" width="30px"><span>雨落～紫竹</span> 👍（0） 💬（0）<div>请问这个 在最里层进行的范围查找 就是5.6以后引入的索引下推吗  还有 like 的最左匹配 具体 string类型是怎么转换成索引树对下层的范围查询呢</div>2020-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a2/0e/62f10b10.jpg" width="30px"><span>朱朱</span> 👍（0） 💬（0）<div>
        InnodbTreeNodesProject(id=[key], name=[data[1]])
            InnodbFilter(condition=[key &gt; 50])
                InnodbTreeScanAll(tree=[users])
       和

        InnodbTreeNodesProject(id=[key], name=[data[1]])
            InnodbTreeRangeScan(tree=[users], range=[key &gt; 50])  &#47;&#47; 全树扫描再按照主键过滤，直接可以优化为对树的范围查找
        从Sql语句上来说第一个是加where过滤，但不知道第二种是怎么过滤，没有innodbFilter，谢謝了</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（0） 💬（0）<div>其实结合的相对不错的是mongodb,尤其大量的Coding可以用类sql;redis的B+其实还是类似，不过拆分这块确实有些其算法特性-这正是它能普遍流行的所在。</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1a/05/f154d134.jpg" width="30px"><span>刘楠</span> 👍（0） 💬（0）<div>看了下mysql还是有点蒙，慢慢理解了</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a4/27/15e75982.jpg" width="30px"><span>小袁</span> 👍（0） 💬（3）<div>如何结合文章理解小表驱动还是大表驱动呢？我还是想不清楚。</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/13/31ea1b0b.jpg" width="30px"><span>峰</span> 👍（0） 💬（0）<div>基本上就是一个提供了命令式的语言，用户告诉告诉数据库做什么东西就行。没有sql 就一般在存储层简单封装了一层对外的接口，而这层接口就和存储模型有很大关系，比如hbase ，redis 都是健值存储，所以对外主要操作就是get put 等等。</div>2020-03-19</li><br/>
</ul>