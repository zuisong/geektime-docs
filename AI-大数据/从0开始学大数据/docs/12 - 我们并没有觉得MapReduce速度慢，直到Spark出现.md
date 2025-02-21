Hadoop MapReduce虽然已经可以满足大数据的应用场景，但是其执行速度和编程复杂度并不让人们满意。于是UC Berkeley的AMP Lab推出的Spark应运而生，Spark拥有更快的执行速度和更友好的编程接口，在推出后短短两年就迅速抢占MapReduce的市场份额，成为主流的大数据计算框架。

读到这里请你先停一下，请给这段看似“没毛病”的引子找找问题。

不知道你意识到没有，我在这段开头说的，“Hadoop MapReduce虽然已经可以满足大数据的应用场景，但是其执行速度和编程复杂度并不让人们满意”，这句话其实是错误的。这样说好像可以让你更加清晰地看到事物发展的因果关系，同时也可以暗示别人自己有洞察事物发展规律的能力。然而，这种靠事后分析的因果规律常常是错误的，**往往把结果当作了原因**。

事实上，在Spark出现之前，我们并没有对MapReduce的执行速度不满，我们觉得大数据嘛、分布式计算嘛，这样的速度也还可以啦。至于编程复杂度也是一样，一方面Hive、Mahout这些工具将常用的MapReduce编程封装起来了；另一方面，MapReduce已经将分布式编程极大地简化了，当时人们并没有太多不满。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/75/e1/bec1e654.jpg" width="30px"><span>光脚的sun</span> 👍（167） 💬（2）<div>老师，现在都说flink更优秀，是不是我们直接跳过mr和spark直接学flink就行了？</div>2018-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（64） 💬（1）<div>spark优势在于迭代式的内存运算，适合于做大数据分析，机器学习之类的，flink是流式计算框架，对于实时性任务也许更好，对于机器学习内任务，spark还是要好点</div>2018-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4f/b2/1e8b5616.jpg" width="30px"><span>老男孩</span> 👍（63） 💬（1）<div>惭愧，我遇到的产品经理或者需求人员，基本上分为两类。一类经常说，这是客户的要求必须马上改，用客户来压制研发。一类比较以自我为中心，把自己的观点等同于用户的观点。常常想当然，结果用户一看不是我想要的。结果就是开发人员一次次的从坑里刚爬上来，又被产品一脚踹下去。有几次我真的无法克制，有一种想套麻袋然后一顿打的冲动。🤔非常赞同老师的观点，不管解决技术问题，还是设计产品都需要深刻的洞察力。想起前面您说的抽象是事物本质的洞察，遇到问题先猫在后面（虽然这种方式比较猥琐），冷静思考，暗中观察，从别人的方案或者错误中总结发现规律，然后顺势而为。</div>2018-11-25</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/eGViaEx6wTjibicgjs760voUJHaaFLwgfib8pHiajqsIElQMoJmwUGz2HNeCOHyChGDSlw1cyMKiaUoK6AIm7PLpL9Kw/132" width="30px"><span>无心乐乐</span> 👍（44） 💬（2）<div>第一次在极客写留言，感觉这个专栏的老师真的是用心良苦，不只是技术的教授，更是经验的传递。
我们常常意识不到问题的存在，直到有人解决了这些问题。
醍醐灌顶，受益良多！！</div>2018-11-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eobHCkMA1WJgZZYRfHqXDeIwybVwSxNGFAWWSunYVNLiaKia6q3rVkG7P8tl4ZcNRI7iaxdZhVckroVA/132" width="30px"><span>Lambda</span> 👍（37） 💬（1）<div>看了一些留言，感觉大家还是”面向工具“学习，对层出不穷的”工具“，感到困惑。但是归根结底，这些工具本身还是计算机科学中很多基础概念的具象化，因此，”面向思想“学习应该是更好的一种做法。先对一种最原始的实现透彻的研究，理解其背后的思想和设计理念，然后再逐步学习后期更为先进的技术，这种学习路径应该更为有效。</div>2018-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/10/3a/053852ee.jpg" width="30px"><span>张小喵</span> 👍（10） 💬（1）<div>老师，我有一个疑问，本节里面的word count示例代码，map完了直接reduce，spark中一个map操作是针对的一个RDD分片，并不是针对的所有的分片（要统计文件的所有分片），我们reduce的操作不是应该处理所有的map数据结果汇集之后的RDD吗，为何只是一个map计算的结果？</div>2019-12-03</li><br/><li><img src="" width="30px"><span>18601611625</span> 👍（6） 💬（1）<div>我最近也在研究Hadoop，但是有一个疑问不知道理解的对不对。Hive Hbase 都是处在HDFS上层的处理框架，而且Hbase和Hive功能基本重叠，为什么HBase不能取代Hive？</div>2019-09-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLeKdLZTWmcxDE7AUnM90naTbDzynshqzILrQAweQXicGgvdg1gImWxeZabiay9LVLsnOCfjj2nZaBA/132" width="30px"><span>eldon</span> 👍（5） 💬（1）<div>学习java 很多人都上来就学各式框架，浮于表面，看到什么就学什么。没有好好学习基础。 我觉得无论学习什么，基础都是最关键的。只有用笨办法打牢基础才能以后快速迭代新知识！</div>2019-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7a/e5/8a2bb5b5.jpg" width="30px"><span>Abyte</span> 👍（5） 💬（1）<div>大数据开发处理数据过程中难免被领导提一些需求，做各种各样的报表统计。我们第一手接触数据，如果我们能再有精力投入业务，是不是也能主动做出一些老板需要的报表统计，提升自己的价值</div>2018-11-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKPBiaSZVibZwoUEUcvbF4JCfOghmvPdUfbFHeDd2g5m6NbuzeN3S3b7KxZCA8FmtrH9N51Z5P177iaA/132" width="30px"><span>小千</span> 👍（4） 💬（1）<div>道理都是相通的，我之前做过摄影师，客户往往对想要的照片没有任何概念，当策划&#47;拍摄&#47;后期出好片子，客户才会说这样的片子是我想要的。反之，片子客户不满意的提问题，往往说不到点子上，比如说客户说表情不满意，其实可能是觉得照片显胖。</div>2018-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/9d/be04b331.jpg" width="30px"><span>落叶飞逝的恋</span> 👍（2） 💬（1）<div>我们常常意识不到问题的存在，直到有人解决了这些问题。非常喜欢这句话。如同：千里马常在，伯乐难寻一个道理，我们往往缺少发现问题的独到眼光。</div>2018-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/09/71/b6638c96.jpg" width="30px"><span>挤挤</span> 👍（2） 💬（1）<div>老师有开其他博客、公众号嘛？想听老师更多的分享</div>2018-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（2） 💬（2）<div>在南方回南天算是典型的例子吧，地板天花墙都冒水，很多人把窗户打开通风，结果更潮湿，开去湿机效果也不怎么好，去查下形成原因，比较好用的方法就是紧闭门窗。</div>2018-11-25</li><br/><li><img src="" width="30px"><span>谢世茂</span> 👍（1） 💬（1）<div>老师，你好，请问下如果需要让深度学习和大数据衔接起来应该怎么做呢？像SPARK这类工具，自带的机器学习算法只有传统的统计机器学习，但是如果要利用深度学习或者GPU应该怎么做数据的架构呢？</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7b/18/6e44e6e0.jpg" width="30px"><span>恺撒之剑</span> 👍（0） 💬（1）<div>老师的课程出来3年多了，又拿出来看了看，真是不一样的风景</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a3/d1/a30a4d06.jpg" width="30px"><span>张闯</span> 👍（0） 💬（1）<div>初始状态：
每个DataNode上存有全部表的分片数据，但每个表在这个DataNode上的分片区域是随机不相关的。
最终状态：
对所有表的数据进行了整合计算处理，处理结果分片存储在不同的DataNode上。

所以，计算过程中涉及到联表计算时，就难免需要跨DataNode传输数据。

第一阶段，对DataNode1中的表1进行group by，结果还是存在DataNode1中，假设叫结果1。
第二阶段，需要将结果1与表2进行join。问题来了，表2的数据分布在不同的DataNode上。结果1只是该类结果集的一个分片。因此，能够与该分片join的表2数据也分布在不同的DataNode上。
此时，shuffle需要将各个DataNode上能够与结果1进行join的数据传输到DataNode1上。
当然，也可以反过来，将结果1分别传输到不同DataNode上。即对结果1进行shuffle。
但这样的话总的传输次数会变多？</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a4/bb/dc8e1d69.jpg" width="30px"><span>tom</span> 👍（0） 💬（1）<div>老师，看了这章感觉rdd转换跟java函数式编程很像，也是流式操作吗，调用类似collect这样的方法才会生成新片吗</div>2019-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/75/e1/bec1e654.jpg" width="30px"><span>光脚的sun</span> 👍（0） 💬（1）<div>谢谢老师，你是让我们学会从基础上理解，循序渐进，会更有思考和提升的空间的，很多技术都是在基础上做的改进与创新，一味追求新技术并不能让我们更好的解决问题，而且欠缺了思考的机会</div>2018-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>好吧，老师。学者有点懵了。 没有大数据的基础
问一个 简单的问题：
Spark MapReduce 都是计算框架，
那 Spark 和 Hadoop 是什么关系呢？
</div>2018-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a3/d1/a30a4d06.jpg" width="30px"><span>张闯</span> 👍（78） 💬（0）<div>理解了java8的lambda集合操作相比于传统集合操作的优势，就理解了spark相比于MapReduce的优势。
第一步，将集合对象封装成流式对象。
第二部，将函数传递给流式对象，在流式对象中执行内部循环。
spark之所以快，就是将外部循环替换成了内部循环。
传统的面向对象编程思想下，是将一个集合作为数据对象传递给一个方法，这个方法会return一个新的数据集，然后再把这个新的数据集作为入参传递给下一个方法。一趟接一趟，最终得到想要的数据处理结果。
函数式编程思想是，先把集合封装成流，我把上面两个方法改写成无状态函数丢给这个集合流，对于集合内的每一项会依次执行这两个函数，最终这个集合就是一个新的集合。只循环一趟。
原本需要做连续循环处理的次数越多，spark体现出的效率提升就越明显。

lambda里面叫Stream，spark里面叫RDD。</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（45） 💬（3）<div>比如学习机器学习，可能有很多人和我有同感，基本上是从入门到放弃。我自己也思考了原因。主要是恐惧心态，因为数学差，恐惧那些数学公式，而现在又崇尚几十天学会xxx，这会让人更加焦虑，更不能静下心学习。所以我认为解决问题主要根本也就是调整心态，想象学数学公式就像谈恋爱，从陌生到熟悉，再到走入婚姻的殿堂，不是一蹴而就，罗马不是一天建成的。所以公式一遍看不懂就看两遍，三遍，刻意练习，逃离舒适区。念念不忘，必有回响！</div>2018-11-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ng7NIuMhg8E3U6DjwJlTKFcEYsTtFJkiag22G13JXSiaobpibfI6MicKg93VNqQnG7Rkvl2OfCsAaSksCAVbNDp8zw/132" width="30px"><span>weiruan85</span> 👍（32） 💬（0）<div>     客户：我想租一匹马，你帮忙打听下一天多钱
     fey： 你租马时干什么用呢，犁地还是自己骑。
     客户：自己骑
     fey：那您骑马时准备干什么去呢
     客户： 我打算骑着买东西
     fey：打算买什么东西呢，去那买呢
    客户：我打算去兰州，买一碗牛肉面
     fey：为什么要求兰州买牛肉面呢
    客户：其他地方的不好吃
      fey：我认识一家兰州人开的牛肉面馆，味道很正宗，你去尝尝。
    客户： 确实好吃，再页不用去兰州了。
     
</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/d6/76fe5259.jpg" width="30px"><span>Dream.</span> 👍（16） 💬（0）<div>乔布斯还在世的时候就说过用户永远不知道他们想要的是什么，只有我们做出来了，他们才发现这就是他们想要的。
这几年来一直将这句话当做自己需求分析时的座右铭。
但一直不能领会其中的精髓，今天看完老师的专栏，有种拨开云雾的感觉。
其实我们大多时候把结果当成了原因，并且缺乏了深度的思考以及洞察力。

</div>2018-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（10） 💬（0）<div>看了这篇文章，这个价格，值了！很值！！超值得！！！不到教我们技术还教我们思想！大神真的很负责👍…
Spark可以代替mapReduce那我理解，是不是可以直接跳过mapReduce直接学习Spark？如果有一个东西比Spark更好，我也直接跳过Spark？
我先把您的大数据学完，再补学java大数据编程，可以吧？
我们在广州骗子太多，学会了观察他们是怎么骗的，总结骗子大部分都是利用贪心骗钱。这个算不😜？</div>2018-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bf/d7/9e2c8648.jpg" width="30px"><span>呆猫</span> 👍（9） 💬（0）<div>我要把这篇文章推荐给我们的产品经理去好好读读</div>2018-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/52/bb/225e70a6.jpg" width="30px"><span>hunterlodge</span> 👍（5） 💬（0）<div>工作中，一个新的方案出现的时候，如果它在某个或某些方面优于当前最好方案，我一定会去思考它的catch(另一面)是什么？比如新方案更快，我就大概会看看它的空间使用率、可维护度、全面度。一般都会发现一些问题。生活里也是如此，对表面上只有好处而无需付出或者代价很低的东西永远保持警惕。说白了，世上没有免费的午餐，一些都是权衡利弊的结果</div>2018-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/27/1d/1cb36854.jpg" width="30px"><span>小辉辉</span> 👍（5） 💬（0）<div>好的提问艺术更能帮助我们深入理解和思考问题</div>2018-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/c7/c0/6263280b.jpg" width="30px"><span>LZP</span> 👍（3） 💬（0）<div>李老师真是富有智慧。掌握科技，亦具备身后的人文素养。好老师，向您学习.
</div>2020-07-02</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK8o3aJz4NdqOCWvTjIPGmRWHt5xicwKGGGRd5icCoiauvvtnEtST0ljsuM23wiaYbZLknASvXmmqfg1w/132" width="30px"><span>茅延安</span> 👍（2） 💬（0）<div>没有足够的实践和深度思考，你就不可能发现问题。
而为了解决问题，为了让团队达成一致或者至少不对立，你需要一些委婉的铺垫，让大家进入你预设的情境，和你一同思考，不跳跃，不突兀，真正激发大家的主观意识。这样既能推动方案，也能产生一些新的洞见和闪光点。</div>2019-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/99/5d603697.jpg" width="30px"><span>MJ</span> 👍（2） 💬（0）<div>直向曲中求，有时候，提出问题的能力更重要。</div>2018-12-07</li><br/>
</ul>