前面我们讲过，MapReduce的出现大大简化了大数据编程的难度，使得大数据计算不再是高不可攀的技术圣殿，普通工程师也能使用MapReduce开发大数据程序。但是对于经常需要进行大数据计算的人，比如从事研究商业智能（BI）的数据分析师来说，他们通常使用SQL进行大数据分析和统计，MapReduce编程还是有一定的门槛。而且如果每次统计和分析都开发相应的MapReduce程序，成本也确实太高了。那么有没有更简单的办法，可以直接将SQL运行在大数据平台上呢？

在给出答案前，我们先看看如何用MapReduce实现SQL数据分析。

## MapReduce实现SQL的原理

坚持学习到这里的同学一定还记得，我在专栏第7期留了一道思考题，对于常见的一条SQL分析语句，MapReduce如何编程实现？

```
SELECT pageid, age, count(1) FROM pv_users GROUP BY pageid, age;
```

错过这期内容的同学可以先返回[第7期文章](http://time.geekbang.org/column/article/67968)思考一下这个问题，思考之余也可以看看其他同学给出的方案，我看留言很多同学的思路都是正确的，我们来详细看看MapReduce实现SQL的原理。

这是一条非常常见的SQL统计分析语句，统计不同年龄的用户访问不同网页的兴趣偏好，对于产品运营和设计很有价值。具体数据输入和执行结果请看下面的图示。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/d5/88beb15a.jpg" width="30px"><span>李志博</span> 👍（52） 💬（3）<div>技术嫁接，我还真搞过2个，1个是selenium + 网上找的代码改本机host 实现 自动测试线上的每台机器的功能，另外1个是 java agent + jd-core （一个反编译软件的底层库）实现profile 监控同时能显示线上跑的真实的代码内容</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/87/cf/7bec93d8.jpg" width="30px"><span>朱国伟</span> 👍（20） 💬（1）<div>李老师 在跟着学的过程中 基本上都是现学的 比如 hive
https:&#47;&#47;cwiki.apache.org&#47;confluence&#47;display&#47;Hive&#47;GettingStarted

在学习课程的过程中 是不是先不用对涉及到的这些大数据技术 如hdfs yarn hive等去做深入了解 只需跑一下GettingStared即可 即有个概念</div>2018-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/57/4e/791d0f5e.jpg" width="30px"><span>贺爷</span> 👍（9） 💬（1）<div>李老师，我之前买过您的《大型网站技术架构案例》并学习过，我想问下，对于一个程序员说，技术功底应该达到什么程度才可以去接触、学习和实践架构方面得东西呢？</div>2019-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/b0/30007f3c.jpg" width="30px"><span>大数据技术与数仓</span> 👍（8） 💬（1）<div>package com.company.sparkcore

import org.apache.log4j.{Level, Logger}
import org.apache.spark.{SparkConf, SparkContext}

&#47;**
  * 使用Spark Core的算子实现简单的join操作
  *&#47;
object JoinBySpark {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setAppName(JoinBySpark.getClass.getSimpleName)
      .setMaster(&quot;local&quot;)
    Logger.getLogger(&quot;org.apache.spark&quot;).setLevel(Level.OFF)
    Logger.getLogger(&quot;org.apache.hadoop&quot;).setLevel(Level.OFF)

    val sc = new SparkContext(conf)
    &#47;&#47;通过文本文件创建RDD
    val page_viewRDD = sc.textFile(&quot;file:&#47;&#47;&#47;e:&#47;page_view.txt&quot;)
    val pv_usersRDD = sc.textFile(&quot;file:&#47;&#47;&#47;e:&#47;pv_users.txt&quot;)
    &#47;&#47;提取需要的字段，组合成形如（userid,pageid）的RDD
    val userid_pageidRDD = page_viewRDD.map(_.split(&quot;,&quot;)).map(viewData =&gt; (viewData(1), viewData(0)))
    &#47;&#47;提取需要的字段，组合成形如（userid,age）的RDD
    val userid_ageRDD = pv_usersRDD.map(_.split(&quot;,&quot;)).map(userData =&gt; (userData(0), userData(1)))
    &#47;&#47;对上述的两个RDD执行Join操作，形成形如(userid,(pageid,age))的RDD
    val userid_pageid_ageRDD = userid_pageidRDD.join(userid_ageRDD)
    userid_pageid_ageRDD.collect().foreach(println)
    &#47;&#47;对join操作形成的RDD提取pageid、age字段
    val joinRes = userid_pageid_ageRDD.map(upaData =&gt; (upaData._2._1, upaData._2._2))
    &#47;&#47;打印输出结果
    &#47;&#47;    (1,32)
    &#47;&#47;    (1,25)
    &#47;&#47;    (2,25)
    joinRes.collect().foreach(println)


  }


}</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/37/98991aeb.jpg" width="30px"><span>不似旧日</span> 👍（7） 💬（3）<div>大数据框架可以执行sql,能执行sql的框架有hadoop的hive  spark的sparkSQL,sparkSQL的执行速度要快于hive,
由于大数据框架能执行sql那么是不是可以把这个框架当做数据库来看待?java就能调用大数据服务操作数据了?</div>2019-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6a/2d/ec4ed8ce.jpg" width="30px"><span>shawn</span> 👍（5） 💬（1）<div>李老师，“生成这些函数的 DAG（有向无环图）”，为什么是有向无环图，您可以说说原因嘛。

</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7a/68/d6b53fbb.jpg" width="30px"><span>rains</span> 👍（4） 💬（1）<div>拍照软件和图像编辑美化软件结合起来，变成萌拍，美颜相机</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a0/8e/6e4c7509.jpg" width="30px"><span>一</span> 👍（3） 💬（1）<div>“在我们工作中也可以借鉴一下这种将两种技术嫁接到一起产生极大应用创新性的手段，说不定下一个做出类似Hive这种具有巨大应用价值的产品的人就是你！”老师的这句话好振奋人心啊！</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（3） 💬（1）<div>智能手机就是嘛！ 以前的手机只能打电话，现在可以拍照、打电话、录音，也可以远程操控家电……等等 把操控其他事物的技术嫁接到手机上……</div>2018-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/b2/ce/5638be2b.jpg" width="30px"><span>Flychen</span> 👍（1） 💬（1）<div>小白一个，想体验下hive中跑SQL，有什么在线环境吗</div>2021-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（1） 💬（1）<div>子弹短信，智能音响也算吧。</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5a/9e/8f2ccc1d.jpg" width="30px"><span>有点意思</span> 👍（0） 💬（1）<div>老师好
请教下 HQL和SQL的区别有多大？我去搜集哪些资料才能知道他们的区别？
由于目前我在做协议解析和语法解析 已经有了现成的sql语法解析了  </div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/87/cf/7bec93d8.jpg" width="30px"><span>朱国伟</span> 👍（0） 💬（1）<div>好像只是join的话 并没有reduce这一步骤
SELECT pv.pageid, u.age FROM page_view pv JOIN users u ON (pv.userid = u.userid);

Number of reduce tasks is set to 0 since there&#39;s no reduce operator
Hadoop job information for Stage-3: number of mappers: 1; number of reducers: 0
2018-12-15 17:21:21,269 Stage-3 map = 0%,  reduce = 0%
2018-12-15 17:21:26,382 Stage-3 map = 100%,  reduce = 0%

Total MapReduce CPU Time Spent: 0 msec
OK
1	25
2	25
1	32
Time taken: 26.01 seconds, Fetched: 3 row(s)</div>2018-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8b/82/7f41f664.jpg" width="30px"><span>诺侠</span> 👍（57） 💬（0）<div>jupyter notebook应该算是一个。</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/65/c6/a2111ff3.jpg" width="30px"><span>李</span> 👍（45） 💬（8）<div>此教程适合有一定大数据基础的人，如果是新人，那么肯定是懵懂的</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/47/d217c45f.jpg" width="30px"><span>Panmax</span> 👍（29） 💬（0）<div>Linux 命令中最常用的管道符 | ，就是运用嫁接最多的地方吧。</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/32/3f/fa4ac035.jpg" width="30px"><span>sunlight001</span> 👍（17） 💬（0）<div>Jekins之类的持续集成工具，集成了非常多的工具及模块，比如sonar,git,mail等</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/e9/5955aa73.jpg" width="30px"><span>阿神</span> 👍（11） 💬（1）<div>老师，您好！hive on spark跟spark sql on hive性能上会一样吗，这两种方案怎么选型</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/65/d0/b5b00bc2.jpg" width="30px"><span>在路上</span> 👍（5） 💬（0）<div>当初接触到ajax时就觉得很神奇，了解其实现原理后发现就是已有的两个技术（Javascript+xml）相结合后产生的技术魅力，这就是1+1&gt;2的效果</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fb/6e/c10b9c25.jpg" width="30px"><span>Albert</span> 👍（5） 💬（0）<div>Spring Cloud将各种微服务的基础设施集成在一起，Spring Boot简化应用配置和管理依赖，这两者结合在一起，使得微服务应用能够快速开发和构建</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/38/19/c8d72c61.jpg" width="30px"><span>木白</span> 👍（3） 💬（0）<div>集成的例子太多了，其实目前稍微复杂点的软件都是各种不同的功能结合在一起的。比如微信和支付宝这种，把社交和支付（或者说红包这种特殊的功能）结合起来，我们现在回头去看，可想想到有社交的地方就会有金钱往来，好像是那么理所当然。但是最开始聊天软件出现了好多年业没有出现相应的产品。也许技术和政策是一部分原因，这我就可能不太清楚了。</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（3） 💬（0）<div>婚姻也算是一种嫁接吗？</div>2018-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8e/91/f1bb1d06.jpg" width="30px"><span>梦幻之梦想</span> 👍（3） 💬（0）<div>操作系统</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/9d/be04b331.jpg" width="30px"><span>落叶飞逝的恋</span> 👍（3） 💬（0）<div>多种技术组合而成的软件产品太多了，比如:语音识别技术与搜索引擎技术组合成语音识别技术，比如iphone上的siri 。还有人脸识别技术与监控技术结合及公安系统组合，就可以马路闯红灯，直接暴露闯红灯的身份。</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6d/9c/beaf7642.jpg" width="30px"><span>伊森</span> 👍（3） 💬（0）<div>学习李老师的课，不仅能学习到专业的知识，还引导你更深层次的思考🤔</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cb/50/66d0bd7f.jpg" width="30px"><span>杰之7</span> 👍（2） 💬（0）<div>通过这一节的复习，对大数据仓库Hive有了进一步的理解。

Hive的出现解决的BI工程师进入大数据处理的门槛，当然对于有大数据经验使用MR进行编程处理同样可行。在MR进行大数据处理的过程中需要进行Map，shuffle，reduce阶段。Hive将SQL自动生成MR可执行的代码，提交给Hadoop执行。

对Hive的架构，主要有Mesastore对元数据的记录，Compiler对于查询语句的处理，及支持Where，join     on 等操作。

在技术的不断发展中，出现了多种SQL引擎，它们也共同促进的大数据的发展。</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a2/9b/d7adabb2.jpg" width="30px"><span>东东</span> 👍（1） 💬（0）<div>持续集成（Continuous integration）工具应该算一个吧。CI工具把整个软件工程过程需要的都整合在一起极大的提升了研发效率。常用的把代码仓库、编译工具、部署工具串联起来实现一键部署。</div>2020-02-29</li><br/><li><img src="" width="30px"><span>千回百转无劫山</span> 👍（1） 💬（0）<div>难道不应该讲Antlr 吗？ </div>2019-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/36/d60a6190.jpg" width="30px"><span>mt11912</span> 👍（1） 💬（0）<div>postgresql 数据库支持json数据类型，将结构化数据和非结构化数据整合在一起。</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8b/3c/0462eca7.jpg" width="30px"><span>Tomcat</span> 👍（1） 💬（0）<div>将两种产技术或者产品嫁接起来，可以实现不一样的神奇效果。比如婴儿恒温箱，就是恒温+保暖箱；语音识别技术就是统计学+计算机；手机就是通讯+连接+……等等。
这样的嫁接思维，不仅仅在技术中所向披靡，在商业领域或者人生思考中，也是非常有益处。</div>2019-04-10</li><br/>
</ul>