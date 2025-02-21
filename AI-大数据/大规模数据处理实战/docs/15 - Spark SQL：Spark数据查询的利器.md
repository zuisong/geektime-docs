你好，我是蔡元楠。

上一讲中，我介绍了弹性分布式数据集的特性和它支持的各种数据操作。

不过在实际的开发过程中，我们并不是总需要在RDD的层次进行编程。

就好比编程刚发明的年代，工程师只能用汇编语言，到后来才慢慢发展出高级语言，如Basic、C、Java等。使用高级语言大大提升了开发者的效率。

同样的，Spark生态系统也提供很多库，让我们在不同的场景中使用。

今天，让我们来一起探讨Spark最常用的数据查询模块——Spark SQL。

## Spark SQL 发展历史

几年前，Hadoop/MapReduce在企业生产中的大量使用，HDFS上积累了大量数据。

由于MapReduce对于开发者而言使用难度较大，大部分开发人员最熟悉的还是传统的关系型数据库。

为了方便大多数开发人员使用Hadoop，Hive应运而生。

Hive提供类似SQL的编程接口，HQL语句经过语法解析、逻辑计划、物理计划转化成MapReduce程序执行，使得开发人员很容易对HDFS上存储的数据进行查询和分析。

在Spark刚问世的时候，Spark团队也开发了一个Shark来支持用SQL语言来查询Spark的数据。

Shark的本质就是Hive，它修改了Hive的内存管理模块，大幅优化了运行速度，是Hive的10倍到100倍之多。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/9e/6550a051.jpg" width="30px"><span>:)</span> 👍（33） 💬（2）<div>任何一个生命力的存在与发展都源于历史背景下的需求。
1.  hive sql虽好，但是限制了spark的发展，hive sql已经满足不了广发人民群众对spark sql的的强烈需求，我们需要进入社会主义社会，你却还是用石头打猎，，不行滴，，
2. RDD是spark这座大厦的基石，那块砖就是RDD。RDD赋予了灵活性，但带来了另一个问题就是复杂性。灵活性和复杂性是一对永久不变的矛盾。
3.Dataset与DataFrame。我现在要建个房子，你直接给我4面墙一个顶就够了，不要一块砖一块砖的给我，我不但很懒而且很笨。Dataset与DataFrame是根据通用结构化数据处理的建立在RDD之上的封装。带来的便易性但是降低了一定的灵活性。</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（26） 💬（1）<div>待处理数据的schema是静态的且对其完全掌控的情况下用DataSet，反之用DataFrame</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ee/16/742956ac.jpg" width="30px"><span>涵</span> 👍（18） 💬（2）<div>老师好，我猜想DataSet适用于每列类型程序都很确定时使用，而DataFrame适用于列的类型不确定，类似于generic的类型，拿到数据后根据数据类型再进行不同的处理。是否可以这样理解?</div>2019-05-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELtsib7NQO2NaEubNbfbAqh8FQDibTuUon1QNHvbV1vD1Vo9vO8wymibTria6nIO3hakJNfrY1okseuRQ/132" width="30px"><span>Geek_9319</span> 👍（6） 💬（2）<div>到底 DataSet是DataFrame的特例？还是DataFrame 是DataSet的特例？</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1a/f9/180f347a.jpg" width="30px"><span>朱同学</span> 👍（4） 💬（1）<div>大部分情况下用dataset都没问题，限制因素主要是spark版本</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/c0/cb5341ec.jpg" width="30px"><span>leesper</span> 👍（5） 💬（0）<div>感觉这就是传说中的Schema-on-read，传统的数据仓库只能存储结构化数据，对于非结构化数据的，后来有了data lake</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f3/dc/80b0cd23.jpg" width="30px"><span>珅剑</span> 👍（3） 💬（0）<div>DataSet在需要访问列中的某个字段时是非常方便的，但是如果要写一些适配性很强的函数时，如果使用DataSet，行的类型无法在编译时确定，可能是各种case class，这时候用DataFrame就可以比较好地解决问题</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/a0/3da0e315.jpg" width="30px"><span>茂杨</span> 👍（1） 💬（0）<div>越来越喜欢spark了, 有了dataframe和dataset，就可以用sql这种函数式语言做项目了</div>2020-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e9/116f1dee.jpg" width="30px"><span>wy</span> 👍（1） 💬（0）<div>dataframe是dataset的子集，类型是row，所以dataframe适合那些编译阶段无法确定字段数量和类型的查询，dataset适用那些编译阶段就明确知道字段详细详细信息的场景。</div>2019-11-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erdpKbFgRLnicjsr6qkrPVKZcFrG3aS2V51HhjFP6Mh2CYcjWric9ud1Qiclo8A49ia3eZ1NhibDib0AOCg/132" width="30px"><span>西北偏北</span> 👍（1） 💬（0）<div>Rdd是spark最底层的核心数据结构，但直接使用rdd的门槛较高，你得知道那些地方可以优化，比如filter要写在group之前。如若不然，写出来的计算，性能其差。


并且rdd没有字段类型名称信息，字段的获取和处理难度较高。


推荐使用spark sql更顶层，提供了schema信息，提供了对查询的优化。</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/37/57/750c641d.jpg" width="30px"><span>linuxfans</span> 👍（1） 💬（0）<div>Dataset具有类型信息，而Dataframe没有，所以当我们要处理类型化数据，例如数值型时，用Dataset更方便。理论上，Dataframe可以用在Dataset的所有地方，只是字段类型要在程序中自己处理。</div>2019-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2b/49/e94b2a35.jpg" width="30px"><span>CoderLean</span> 👍（1） 💬（1）<div>实际上如果只是因为hive的不足，为什么不用impala代替，性能也比sparklsql高</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/45/3addffe7.jpg" width="30px"><span>brv</span> 👍（1） 💬（0）<div>dataset是在dateframe基础上发展起来的，那dateset是dateframe的特例</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（1） 💬（0）<div>1. 对于读写Hive时，适合用Dataframe，可以认为df就是一张表。
2. 对于要操作元组或者case class或者csv等文件时，适合用Dataset，因为是强类型的</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9a/18/3596069c.jpg" width="30px"><span>RocWay</span> 👍（1） 💬（0）<div>老师你好，请教个问题：既然dataframe没有存储具体的类型，那么是否可以认为dataframe具有动态语言的特性？也就是说当数据类型变化后，程序能够自动适应。实现起来可否这样：先判断某个名字的字段是否存在，再做出相应的动作？</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/6f/3d4f7e31.jpg" width="30px"><span>娄江国</span> 👍（0） 💬（0）<div>如果做数据仓库用sparksql做etl，那么数据以什么格式存储最好呢？</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d2/0e/26bf35a4.jpg" width="30px"><span>平安喜乐</span> 👍（0） 💬（0）<div>使用StructField(filedName, StringType, nullable = true)
或者val caseClassDS = Seq(Person(&quot;Andy&quot;, 32)).toDS(）
如果要查整个表的字段  怎么动态的填充数据字段对应的类型</div>2020-04-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/cKeYVTKJCJhrfTCBkEGla1WA7W0S9FPZrTR3ovYJFhcKo7kl72gR9VibCufhHsjOar2Z6mZlFKb8VEkkDv9lqVA/132" width="30px"><span>坤2021牛</span> 👍（0） 💬（0）<div>大部分情况都是用dataset和dataframe,rdd的用于操作细节的地方</div>2019-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f9/45/eaa8beb0.jpg" width="30px"><span>王翔宇🍼</span> 👍（0） 💬（1）<div>何时检测分析错误 的分析错误是指什么？</div>2019-07-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/4lUeUo6LHfsHLYfKaMQXQiaZVyEsqY1nfXU6dP0wN1KCch7LDIZTCO4rJ5mq1SdqY9FibCGMsjFdknULmEQ4Octg/132" width="30px"><span>Geek_f406a1</span> 👍（0） 💬（1）<div>请问作者 &quot;还兼容多种数据格式，包括 Hive、RDD、JSON 文件&quot; 这句话中hive是一种数据格式么？</div>2019-05-30</li><br/>
</ul>