你好，我是蔡元楠。

今天我要分享的主题是Kappa架构。

同样身为大规模数据处理架构，Kappa架构这把利用Kafka锻造的“屠龙刀”，它与Lambda架构的不同之处在哪里呢？

上一讲中，我讲述了在处理大规模数据时所用到经典架构，Lambda架构。我先来带你简要回顾一下。

![](https://static001.geekbang.org/resource/image/8f/23/8fe667211309978b2dd6cb6948939923.jpg?wh=634%2A227)

Lambda架构结合了批处理和流处理的架构思想，将进入系统的大规模数据同时送入这两套架构层中，分别是批处理层（Batch Layer）和速度层（Speed Layer），同时产生两套数据结果并存入服务层。

批处理层有着很好的容错性，同时也因为保存着所有的历史记录，使产生的数据集具有很好的准确性。速度层可以及时地处理流入的数据，因此具有低延迟性。最终服务层将这两套数据结合，并生成一个完整的数据视图提供给用户。

Lambda架构也具有很好的灵活性，你可以将现有开源生态圈中不同的平台套入这个架构，具体请参照上一讲内容。

## Lambda架构的不足

虽然Lambda架构使用起来十分灵活，并且可以适用于很多的应用场景，但在实际应用的时候，Lambda架构也存在着一些不足，主要表现在它的维护很复杂。

使用Lambda架构时，架构师需要维护两个复杂的分布式系统，并且保证他们逻辑上产生相同的结果输出到服务层中。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/e7/87/9ad59b98.jpg" width="30px"><span>程序设计的艺术</span> 👍（28） 💬（2）<div>有几个地方没太明白：
1.批处理数据具有很高的准确性，实时运算处理就没有？
2.关于数据错误，两者应该都有吧？数据错误后两者的处理不一样吗？比如10个任务中的3个有错误，批处理和实时处理都应该可以找到3个任务重新计算吧？
为什么实时运算需要完全从头计算所有任务？
谢谢</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1a/f9/180f347a.jpg" width="30px"><span>朱同学</span> 👍（24） 💬（3）<div>我感觉这是用队列代替了hdfs</div>2019-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/9e/6550a051.jpg" width="30px"><span>:)</span> 👍（21） 💬（1）<div>1.kappa架构使用更少的技术栈，实时和历史部分都是同一套技术栈。lambda架构为了解决历史部分和实时部分可能会使用不同的技术栈。

2.kappa架构使用了统一的处理逻辑。而lambda架构分别为历史和实时部分使用了两套逻辑。一旦需求变更，两套逻辑都要同时变更。

3.kappa架构具有流式处理的特点和优点。比如可以具有多个订阅者，比如具有更高的吞吐量。

</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/38/05/67aae6c8.jpg" width="30px"><span>Rainbow</span> 👍（18） 💬（1）<div>spark算kappa架构吗？批处理 流处理一套</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/43/b89372d1.jpg" width="30px"><span>T</span> 👍（10） 💬（2）<div>有个问题不明白，实时数据量很大的化，每次都从头计算，是否削弱了速度层实时性的特点，这样不和初心违背了么？</div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/e4/afacba1c.jpg" width="30px"><span>孙稚昊</span> 👍（8） 💬（1）<div>这样批和流的压力就全压到kafka 上了，对kafka并发的要求也非常高，应该只有kafka 能做到这件事了吧
</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2b/49/e94b2a35.jpg" width="30px"><span>CoderLean</span> 👍（7） 💬（2）<div>不可能啊，如果要保存长久的数据，那么kafka的集群容量得有多大，按每天就一个t来说，加上默认副本3，那一年要存的数据量就得很多了。 这还可能只是其中一个业务。国内有小公司敢这样做吗</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（6） 💬（1）<div>如果批处理比较多的话，每次都从kafka的earlist offset消费的话，第一会耗费很长很长时间，而且消费者如果资源不够多，会导致任务堆积的吧。所以kappa不适合批处理多的架构。

Kappa架构因为整合了批处理层和速度层，优势就是:
1. 实时性比较高，适合对实时性要求高的场景
2. 业务逻辑可以使用统一的API来编写，那么对于之后的业务需求变更和代码维护都比较友好</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/4f/ff1ac464.jpg" width="30px"><span>又双叒叕是一年啊</span> 👍（4） 💬（1）<div>处理这种大数据量有窗口期的比如近30天的任务聚合计算可以用这种模式吗？是需要用kafka stream？每天都需要计算一次近30天的任务计算全量数据很大都是离线日志产生的数据</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/54/50/8a76a8cc.jpg" width="30px"><span>Zoe</span> 👍（3） 💬（1）<div>老师，请问一下，纽约时报这个例子，是不是每次只处理delta部分而不是把log offset设成0更好一些？
我粗浅的理解是可以把batch layer想成一个cache，感觉这种基于time series的每次只需要处理new data的部分再把结果和之前的cache聚合在一起就可以了？
还是说业界普遍的做法都是从头开始处理，因为相较于找delta考虑overlap的困难就不那么意额外的处理时间和机器运行的成本？</div>2019-05-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL58j1S6Ax1MMagApMzRnIkxy3rYxtmsmQibAst80NRzamx161ibwu6T1jxoicB8yg8TNLI4NZRBzGYg/132" width="30px"><span>tonyzhang</span> 👍（2） 💬（1）<div>老师，我想问一下，像lambda架构分成批处理和实时处理的两层，最终都是输出到对应的结果表供应用层分析；那为什么不能先进行实时计算，再把实时计算的结果写入到批处理的表中，这样批处理的数据就会不断累加，也能达到分析历史整体数据的目的，同时计算任务只需要实时计算的任务，批处理的数据是通过同步的形式进行，维护成本也能降低，不知道我的理解对不对？</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f3/dc/80b0cd23.jpg" width="30px"><span>珅剑</span> 👍（2） 💬（1）<div>新数据视图处理过得数据进度有可能赶上旧的数据视图吗？原先的数据视图应该也是实时不断更新的</div>2019-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/b6/c3e2371a.jpg" width="30px"><span>jasine</span> 👍（2） 💬（1）<div>老师您好，麻烦请教下 如果实时与历史批量流程合在一起 那么重跑的时候kafka offset置成0 到latest这段时间是不是实时就无法提供服务了 怎么解决这个问题呢 感谢</div>2019-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7c/59/26b1e65a.jpg" width="30px"><span>科学Jia</span> 👍（1） 💬（1）<div>老师，女同学举手提问：我不太理解例子中提到重新计算历史数据得到新的视图，这会对实时数据产生什么影响么？或者说实时数据需要依赖批处理的视图么？我还没法把批处理的结果和实时处理结果相结合，能否再具体一点呢？</div>2019-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/93/b8/6510592e.jpg" width="30px"><span>渡码</span> 👍（0） 💬（1）<div>优点：数据统一，算法统一，接口统一
缺点：与现有大数据架构协同处理的兼容性不如lambda</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/b8/92178ccd.jpg" width="30px"><span>ECHO</span> 👍（0） 💬（1）<div>回答貌似不对。这个offset是针对一个消费组的，不是全局。</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/aa/fa/3ad0a689.jpg" width="30px"><span>廖师虎</span> 👍（0） 💬（1）<div>个人觉得Kafka并不适合长期保存和处理海量数据，所以Kappa并不适合海量数据场景。使用Pulsar+Presto倒是可以满足</div>2019-05-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/9chAb6SjxFiapSeicsAsGqzziaNlhX9d5aEt8Z0gUNsZJ9dICaDHqAypGvjv4Bx3PryHnj7OFnOXFOp7Ik21CVXEA/132" width="30px"><span>挖矿的小戈</span> 👍（0） 💬（1）<div>1. kappa架构就是为了解决，lambda架构的复杂性以及维护成本高等痛点；
2. 所以才有了后面的Flink、Beam、Spark这些正在努力做流批统一的框架
3. 不过个人而言，更倾向于Flink这种流处理为核心，批处理只是流处理的一个子集；而Flink对于状态、容错、一致性等等都做得挺好的，很看好
4. 另外，对于Beam正在做的统一大数据编程规范的，也非常看好，哈哈，想想，掌握一套API就可以，底层想跑什么计算引擎，根据场景需求自由选择，美滋滋，不过Flink、Spark国内用的多，Beam貌似用的比较少，不知道国外是什么情况</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（0） 💬（1）<div>老师，我问几个很low的问题，你别介意哈😄
1. apache怎么看哪些项目是属于大数据，否是项级项目，项目创建日期？
2. 如果想了解大数据，IT技术（如编程、架构、运维）的新方向有哪些网站可以看呀？
3. 听说国外是没运维的职位，只有SRE？运维很多开发都代替了运维，还有自动化，运维职位那不是慢慢消失了？</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/74/af/6f39dcf8.jpg" width="30px"><span>奥卡姆剃刀</span> 👍（0） 💬（1）<div>对比lambda和kappa 两种架构的优缺点，总结：没有完美的架构，最好的架构一定是根据业务需求演变过来的。</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/a7/4d41966a.jpg" width="30px"><span>邱从贤※klion26</span> 👍（0） 💬（1）<div>kappa 最好的地方在于代码写一份就好了，维护成本大大降低，曾经核对过 mr 和 storm 产生的结果，真的很麻烦（还只对过一次），如果逻辑变更比较频繁的话，改一次需要对一次</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（0） 💬（1）<div>Kappa是解决lombda架构维护两套处理逻辑的复杂性痛点而诞生的，它使用kafka配合处理流处理业务，具有简单，处理数据快，支持发布订阅模式的优点？。但同时也带来了数据错误和异常处理的成本。
</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（0） 💬（1）<div>kappa架构和lambda架构都有各自的优点和缺点和各自的使用场景。关键是要不要维护两套不同的技术栈，现在像spark和flink都在往批流统一的方向努力，目的就是统一技术栈，减少开发和运维的成本。</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3d/5d/ac666969.jpg" width="30px"><span>miwucc</span> 👍（0） 💬（1）<div>文中说的kappa的两个缺点，不是很理解。

第一点，说实时数据需要处理数据异常，按理说说lambda结构的速度层也会面对这个问题啊。还是是说kappa的历史数据计算层在计算的时候同时需要清洗数据，而lambda的批处理层是直接读取的清洗好结构化好的数据？

弟二点：说如果历史计算和实时计算需要不同逻辑时候不适用。就在该框架下写两套逻辑不就行了么？为啥非要用lambda架构再写两套逻辑，还面对技术栈切换

</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/f8/c1a939e7.jpg" width="30px"><span>君哥聊技术</span> 👍（0） 💬（1）<div>1.如果批处理和流处理的逻辑一致，那可以选择用kappa架构，否则lambda架构更好

如果选择kappa架构，kafka offset置为0来计算批数据，会不会非常耗时呢？可以用批结果加流结果作为下次计算的批结果吗</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/68/84/9fa4dc6e.jpg" width="30px"><span>小度</span> 👍（0） 💬（1）<div>有没有完美的架构？Kappa 架构Lambda 架构都有优缺点能否融合使用？</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（0） 💬（2）<div>kappa架构优点：
1.流处理和批处理同一套算法逻辑，更简单。
2.数据格式统一，给后端处理带来方便。
3.批量处理的速度更快。
</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/a7/d379ca4f.jpg" width="30px"><span>jon</span> 👍（0） 💬（1）<div>kappa优点：不用分别编写批、流两套处理逻辑，采用发布-订阅模式，接受多个订阅者，可重复消费历史数据。
kappa缺点：在速度层进行大规模实时流处理容易处理数据更新错误，可靠性不如批处理层。
</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（0） 💬（1）<div>如果kafka处理全部数据，数据量非常大会不用卡死？要使用群集吗？</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/16/68/c4d612b3.jpg" width="30px"><span>我只是想改个名字</span> 👍（9） 💬（0）<div>在我看来，Kappa架构和lambda架构没有绝对的谁好，就拿我们现在的业务场景，MySQL同步至tidb平台，原数据进kafka就有可能有问题，而我们又是金融公司，就只能选择lambda架构随时对数据进行校验，对最终数据进行纠正。</div>2019-05-20</li><br/>
</ul>