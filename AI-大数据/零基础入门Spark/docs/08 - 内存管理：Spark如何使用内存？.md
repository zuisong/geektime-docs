你好，我是吴磊。

在[第6讲](https://time.geekbang.org/column/article/420399)，我们拜访了斯巴克建筑集团的分公司，熟悉了分公司的办公环境与人员配置，同时用“工地搬砖的任务”作类比，介绍了Spark Shuffle的工作原理。

今天这一讲，我们再次来到分公司，去看看斯巴克公司都在承接哪些建筑项目，以及这些项目是如何施工的。通过熟悉项目的施工过程，我们一起来学习Spark的内存管理。

![图片](https://static001.geekbang.org/resource/image/2f/63/2fe7ba37365ca1b0da67f83eb859f663.jpg?wh=1920x1016 "斯巴克建筑集团分公司")

相比其他大数据计算引擎，关于Spark的特性与优势，想必你听到最多的字眼，就是“内存计算”。**合理而又充分地利用内存资源**，是Spark的核心竞争力之一。因此，作为开发者，我们弄清楚Spark是如何使用内存的，就变得非常重要。

好啦，闲言少叙，请你戴好安全帽，跟我一起再次去拜访斯巴克集团分公司吧。不过，在正式“拜访”之前，我们还有一项准备工作要做，那就是先了解清楚Spark的内存区域是怎样划分的。

## Spark内存区域划分

对于任意一个Executor来说，Spark会把内存分为4个区域，分别是Reserved Memory、User Memory、Execution Memory和Storage Memory。

![图片](https://static001.geekbang.org/resource/image/c3/7b/c317aa36c594b6ccc93a8a65b5bcf57b.jpg?wh=1920x1010 "Spark内存区域划分")

其中，Reserved Memory固定为300MB，不受开发者控制，它是Spark预留的、用来存储各种 Spark 内部对象的内存区域；User Memory用于存储开发者自定义的数据结构，例如RDD算子中引用的数组、列表、映射等等。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/26/eb/24e0ac9c.jpg" width="30px"><span>嬴梦川</span> 👍（0） 💬（0）<div>Reserved Memory: 300M = 0.3G
User Memory: (10GB-300M)*(1-0.8) = 1988M = 1.94G
Storage Memory: (10GB-300M)*0.8*0.4=3180.8M=3.11G
Execution Memory: (10GB-300M)*0.8*(1-0.4)=4771.2M=4.66G</div>2023-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/bb/a1a61f7c.jpg" width="30px"><span>GAC·DU</span> 👍（12） 💬（1）<div>R:300M
U:(10240 - 300) * (1 - 0.8) =1988
E:(10240 - 300) * 0.8 * (1 - 0.4) = 4771.2
S:(10240 -300) * 0.8 * 0.4 = 3180.8
老师实际生产环境，把spark. executor. memory设置为物理内存的80%合理吗？</div>2021-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/cd/04/e27b7803.jpg" width="30px"><span>小新</span> 👍（6） 💬（1）<div> Storage memory与Execution Memory之间抢占时，会有一个最小阈值吗？不可能全部抢占完吧？</div>2021-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/2b/86/318e6ff3.jpg" width="30px"><span>井先生</span> 👍（5） 💬（1）<div>既然user memory存储用户自定义的数据结构，我在纯sql的spark job中是不是把spark.memory.fraction设置很大的值，只给user memory留比较小的空间以提高execution和storage memory的大小，进而提高内存的使用率呢</div>2021-09-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/qmdZbyxrRD5qQLKjWkmdp3PCVhwmWTcp0cs04s39pic2RcNw0nNKTDgKqedSQ54bAGWjAVSc9p4vWP8RJRKB6nA/132" width="30px"><span>冯杰</span> 👍（4） 💬（2）<div>在实际工作中发现，设置的executor内存，还要扣除1&#47;10的大小，剩余的9&#47;10才能参与老师说的公式计算。   看了别人的博客，说是jvm中的Survivor，只能有1个被真正用起来。       Spark UI上显示的结果，也刚好能够反映这个问题</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8e/d3/1a3bb2cc.jpg" width="30px"><span>Botanic</span> 👍（2） 💬（1）<div>老师好，我想请假一个问题。python中，如果wordCount加上take(5)这个算子后，数据类型就从RDD转化为list了，那么后面再使用saveAsTextFile算子就会报错，因为处理它要求前面的数据类型是RDD。这种情况应该怎么处理呢？谢谢</div>2021-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/da/c7/66f5fcea.jpg" width="30px"><span>大志</span> 👍（2） 💬（2）<div>error: not found: value MEMORY_ONLY

import org.apache.spark.storage.StorageLevel._
wordCounts.persist(MEMORY_ONLY)  &#47;&#47; 就可以了</div>2021-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/d6/ad/850992a5.jpg" width="30px"><span>William</span> 👍（0） 💬（1）<div>老师，假设设定了spark.memory.storageFraction=0.4，那这部分用于存储的内存也是向计算内存转换的是吧？ 那设定这个参数的意义是什么呢，单纯为了在计算内存足够的情况下预留储存空间吗？</div>2021-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/9d/0ff43179.jpg" width="30px"><span>Andy</span> 👍（0） 💬（1）<div>Execution = (10G-300M)* 0.8 * (1-0.4) = 4771.2M 
User = (10G-300M) * (1-0.8) = 1988M
Reserved = (10G-300M)* 0.8 * 0.4 = 3180.8M
Storage = 300M
</div>2021-11-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epGTSTvn7r4ibk1PuaUrSvvLdviaLcne50jbvvfiaxKkM5SLibeP6jibA2bCCQBqETibvIvcsOhAZlwS8kQ/132" width="30px"><span>Geek_2dfa9a</span> 👍（0） 💬（1）<div>这里粗略估计1GB为1000MB
Reserved Memory = 300MB
Execution Memory + Storage Memory = (10GB - 0.3GB) * 0.8 = 9.7GB * 0.8 = 7.76GB
User Memory = 9.7GB - 7.76GB = 1.94GB
Execution Memory = 7.76GB * (1 - 0.4) = 7.76GB * 0.6 = 4.66GB
Storage Memory = 7.76GB - 4.66GB = 3.1GB
</div>2021-09-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJbmJViaa9UH5EVehq7EiayKzEy5FUPpjmZkicg0jxy2sJycTFYbyM3wWzqy1goZhZj2wsrWATDoia9Ww/132" width="30px"><span>Geek_796a41</span> 👍（0） 💬（1）<div>老师，我想问下spark.memory.fraction 和 spark.memory.storageFraction这两个值在设置的时候都有什么参考？</div>2021-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/26/eb/24e0ac9c.jpg" width="30px"><span>嬴梦川</span> 👍（0） 💬（0）<div>Reserved Memory: 300M = 0.3G
User Memory: (10GB-300M)*(1-0.8) = 1988M = 1.94G
Storage Memory: (10GB-300M)*0.8*0.4=3180.8M=3.11G
Execution Memory: (10GB-300M)*0.8*(1-0.4)=4771.2M=4.66G</div>2023-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/9a/63dc81a2.jpg" width="30px"><span>Geek1185</span> 👍（0） 💬（0）<div>老师，我在工作中发现一个10TB任务量的spark任务中，executor的fraction只有0.3，memory为6g，这样usermemory就会非常大，而工作区和暂存区只有2g不到，这合理吗</div>2023-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/46/eb/44d4f887.jpg" width="30px"><span>王鑫</span> 👍（0） 💬（0）<div>老师您好，spark的堆内内存和堆外内存在什么情况下如何分配使用，堆外内存直接受spark管理，没有jvm。为什么不多使用堆外内存</div>2022-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/6f/ac3003fa.jpg" width="30px"><span>xiong</span> 👍（0） 💬（0）<div>spark的memory模型是在jvm中的新声代区划分出来的吗？</div>2022-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/d3/0a/92640aae.jpg" width="30px"><span>我爱夜来香</span> 👍（0） 💬（1）<div>老师,会不会存在storage空间不足,无法缓存RDD的情况,这时候怎么办?
</div>2022-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4c/d2/f12dd0ac.jpg" width="30px"><span>翡翠小南瓜</span> 👍（0） 💬（0）<div>为了触发cache，调用了count操作，但实际跑的程序，记录很多时，count操作貌似也挺耗时的；假如某个RDD第一次生成时时候，调用了cache，但不触发action操作，后面对这个RDD多次转换，最后执行了一次action，这样是不是最后action的时候才才进行了cache，这是对应用来说实际没啥用了了？？，还有这时候程序结束了，这块cache是怎么处理的呢</div>2022-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5e/d9/28c7a551.jpg" width="30px"><span>晓波.参云木</span> 👍（0） 💬（0）<div>Reserved:300M
User:(1024*10 - 300) * (1 - 0.8) =1988
Execution:(1024*10 - 300) * 0.8 * (1 - 0.4) = 4771.2
Storage:(1024*10 -300) * 0.8 * 0.4 = 3180.8</div>2022-03-21</li><br/>
</ul>