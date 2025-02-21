你好，我是蔡元楠。

今天我要与你分享的主题是“Pipeline：Beam如何抽象多步骤的数据流水线”。

在上两讲中，我们一起学习了Beam是如何抽象封装数据，以及如何抽象对于数据集的转换操作的。在掌握了这两个基本概念后，我们就可以很好地回答Beam编程模型里的4个维度What、Where、When、How中的第一个问题——What了。也就是，我们要做什么计算？想得到什么样的结果？

![unpreview](https://static001.geekbang.org/resource/image/71/bb/71c8ace006d56d7f6fe93cbc56dc91bb.png?wh=1142%2A770)

这个时候你可能已经跃跃欲试，开始想用PCollection和Transform解决我们平常经常会使用到的批处理任务了。没有问题，那我们就先抛开Where、When和How这三个问题，由简至繁地讲起。

现在假设我们的数据处理逻辑只需要处理有边界数据集，在这个情况下，让我们一起来看看Beam是如何运行一套批处理任务的。

## 数据流水线

在Beam的世界里，所有的数据处理逻辑都会被抽象成**数据流水线（Pipeline）**来运行。那么什么是数据流水线呢？

Beam的数据流水线是对于数据处理逻辑的一个封装，它包括了从**读取数据集**，**将数据集转换成想要的结果**和**输出结果数据集**这样的一整套流程。

所以，如果我们想要跑自己的数据处理逻辑，就必须在程序中创建一个Beam数据流水线出来，比较常见的做法是在main()函数中直接创建。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/46/ec914238.jpg" width="30px"><span>espzest</span> 👍（17） 💬（1）<div>bundle怎么聚合成pcollection？  一个bundle处理失败，为什么需要重做前面的bundle？</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（9） 💬（2）<div>bundle随机分配会不会产生数据倾斜？完美并行背后的机制是？beam应该也有类似spark的persist方法缓存转换中间结果，防止出错恢复链太长吧？</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3d/0a/5f2a9a4c.jpg" width="30px"><span>YZJ</span> 👍（8） 💬（1）<div>老师请教个问题：PCollectionA transform PCollectionB, 假如PCollectionB 要比PCollectionA大很多倍，比如transform  是把PCollectionA 中每个字符串重复1000次，那PCollectionB 就要大1000倍，worker会不会有内存溢出问题? spark中可以配置executor 的core和memery来控制每个task内存用量，beam有类似机制吗?不然怎样让资源利用最优化呢?</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（6） 💬（1）<div>Beam的错误处理和RDD的真的很像，因为transformation都是lazy的，只有action才会触发计算，中间的转换过程都是被记录在DAG中的，这就导致中间某个transformation失败之后，需要往上追溯之前的转换，可以理解为是寻找父transformation，然后父transformation还要往上寻找父父transformation，直到没有父transformation为止，就像是类加载机制一样。但是如果能把中间结果保存在内存中，在失败重新计算时，就能提高计算的效率。</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/40/18/cc3804e2.jpg" width="30px"><span>沈洪彬</span> 👍（4） 💬（1）<div>在 Beam 的数据流水线中，当处理的元素发生错误时流水线的的错误处理机制分两种情况

1.单个Transform上的错误处理
如果某个Bundle里元素处理失败，则整个Bundle里元素都必须重新处理

2.多步骤Transform上的错误处理
如果某个Bundle里元素处理失败，则整个Bundle里元素及与之关联的所有Bundle都必须重新处理</div>2019-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/76/3db69173.jpg" width="30px"><span>onepieceJT2018</span> 👍（4） 💬（1）<div>老师 想到一个问题啊 如果有个计算是 需要worker1 和 worker2 都算完的结果再计算 发生worker1 一直错误没通过 这时候worker2会一直傻傻等待嘛</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/e9/95ef44f3.jpg" width="30px"><span>常超</span> 👍（3） 💬（1）<div>&lt;在多步骤的 Transform 上，如果处理的一个 Bundle 元素发生错误了，则这个元素所在的整个 Bundle 以及与这个 Bundle 有关联的所有 Bundle 都必须重新处理。
如果upstream transform里状态有更新操作，重新处理已经成功的bundle会出现数据重复，可能导致状态更新不正确吧？
</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/85/3f161d95.jpg" width="30px"><span>Alpha</span> 👍（1） 💬（1）<div>上一期讲到，PCollection 是有向图中的边，而 Transform 是有向图里的节点。这一期的图咋又变了呢</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/9c/d48473ab.jpg" width="30px"><span>dancer</span> 👍（1） 💬（1）<div>想问老师，一个bundle的数据必须要全部处理完之后才能进行第二个transform吗？如果部分数据经过transform1后就可以继续执行transform2，这样数据并行度会更高吧，为什么没有采用这种机制呢？</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/09/db/19a7c51c.jpg" width="30px"><span>chief</span> 👍（0） 💬（1）<div>老师您好，bundle经过Transform会产生新的bundle，那么是同时保留前后bundle数据还是在新生成的bundle中保留血缘关系？

</div>2019-07-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/jsMMDDzhbsTzhicsGZiaeV0PWSnAS0fBlb1r6CsuB32vr3hRwV9UubmfHQx45v7jtaXajPlQ8kQ17b3zpQzHmqVw/132" width="30px"><span>fy</span> 👍（0） 💬（1）<div>老师，有编程语言基础。我也去Beam看了看教程，请问这个可以直接学吧。还需要其他基础么，比如操作系统，计算机组成原理等</div>2019-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/47/d1/15f1a8ce.jpg" width="30px"><span>TJ</span> 👍（0） 💬（1）<div>能否说一下Beam和底层执行系统的边界在哪里？那些功能由Beam提供,那些由底层如Spark提供?
如果底层是spark，是否PCollection就是RDD?</div>2019-06-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLdWHFCr66TzHS2CpCkiaRaDIk3tU5sKPry16Q7ic0mZZdy8LOCYc38wOmyv5RZico7icBVeaPX8X2jcw/132" width="30px"><span>JohnT3e</span> 👍（0） 💬（1）<div>由于beam优化器，是不是实际产生的bundle要少于逻辑上的个数？</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/44/3c/8bb9e8b4.jpg" width="30px"><span>Mr.Tree</span> 👍（1） 💬（0）<div>错误处理机制有点像MySQL的事务，要么全部成功，要么回滚</div>2022-12-30</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eq4UrqDxicaxiatJOL4CDNZmlsMsn9FPChJUIxaQjTSP552UFZmY4tdlI1Ju0ZiaIFk1yk2A1DJ1qD8w/132" width="30px"><span>jimyth</span> 👍（1） 💬（0）<div>老师你好，既然PCollection 是无序的，请问一下怎么处理数据流中的先后依赖的问题，本节例子的 bound中的数据都是有序的分配的，实际计算过程中是不是会出现 1,3,5出现在一个 bound ;2,4,6 出现在一个 bound
您在 23 讲的例子中，ParDo 是针对单个元素的处理，怎么实现计算2 个元素的累加的呢？
例如下面是一组速度数据
时间                     速度
2019-07-26 00:00:00   10
2019-07-26 00:00:01   15
2019-07-26 00:00:02   20
2019-07-26 00:00:03   40
2019-07-26 00:00:04   70
我需要大概怎么计算加速度，</div>2019-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ef/f1/8b06801a.jpg" width="30px"><span>哇哈哈</span> 👍（0） 💬（0）<div>流式数据也会分bundle吗？那不是变成spark streaming的微型批处理形式了？</div>2022-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/66/04/22190a73.jpg" width="30px"><span>weiming</span> 👍（0） 💬（0）<div>1. PCollection会被划分成多个Bundle（分配多少个是随机的），Bundle会被分配到Worker中处理（分配也是随机的），最终机制保障最大程度的完美并行。
2. 错误处理中有关联Bundle的概念（因为是同一个Worker处理），如果关联Bundle中的一个Bundle失败了，所有关联的Bundle全部重做，主要是考虑到数据持久化的成本。（通过重做消除持久化）
3. 注意有PCollection不可变性，引申到Bundle中的不可变性。 </div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/e6/50da1b2d.jpg" width="30px"><span>旭东(Frank)</span> 👍（0） 💬（0）<div>分而治之</div>2021-01-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/qmdZbyxrRD5qQLKjWkmdp3PCVhwmWTcp0cs04s39pic2RcNw0nNKTDgKqedSQ54bAGWjAVSc9p4vWP8RJRKB6nA/132" width="30px"><span>冯杰</span> 👍（0） 💬（0）<div>从您的描述中可以看出，数据的实际计算和容错都是以分区来进行的，原因在于ParDo模式下同一个Pc下不同的数据记录之间不存在依赖关系即可以完成计算。     在实际计算时，我们处理玩Trasform1得到Pc1，然后在接着计算transform2，那为什么不能以单条数据来并行呢？   即分区内的每一条数据独立完成所有的计算链，而不是要等同一个Pc下的数据都就绪后在执行下一个计算。
关于容错不以单条数据来设计，我倒是能理解，因为要这样做的话，我们必然需要为每条数据都记录他的计算关系，追溯它具体是从上游的哪一条数据来的，这会增加存储的压力。  而以分区来实现容错，我们只需要记录血缘即可，血缘关系太长，可以像Spark那样做一些持久化的操作。</div>2020-04-11</li><br/>
</ul>