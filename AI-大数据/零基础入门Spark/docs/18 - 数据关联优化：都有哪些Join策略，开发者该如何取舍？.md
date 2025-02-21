你好，我是吴磊。

在上一讲，我们分别从关联形式与实现机制这两个方面，对数据分析进行了讲解和介绍。对于不同关联形式的用法和实现机制的原理，想必你已经了然于胸。不过，在大数据的应用场景中，数据的处理往往是在分布式的环境下进行的，在这种情况下，数据关联的计算还要考虑网络分发这个环节。

我们知道，在分布式环境中，Spark支持两类数据分发模式。一类是我们在[第7讲](https://time.geekbang.org/column/article/421566)学过的Shuffle，Shuffle通过中间文件来完成Map阶段与Reduce阶段的数据交换，因此它会引入大量的磁盘与网络开销。另一类是我们在[第10讲](https://time.geekbang.org/column/article/423878)介绍的广播变量（Broadcast Variables），广播变量在Driver端创建，并由Driver分发到各个Executors。

因此，从数据分发模式的角度出发，数据关联又可以分为Shuffle Join和Broadcast Join这两大类。将两种分发模式与Join本身的3种实现机制相结合，就会衍生出分布式环境下的6种Join策略。

那么，对于这6种Join策略，Spark SQL是如何支持的呢？它们的优劣势与适用场景都有哪些？开发者能否针对这些策略有的放矢地进行取舍？今天这一讲，咱们就来聊聊这些话题。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/27/bd/95/882bd4e0.jpg" width="30px"><span>Abigail</span> 👍（15） 💬（2）<div>Broadcast Join 中相比 SMJ，HJ 并不要求参与 Join 的两张表有序，也不需要维护两个游标来判断当前的记录位置，只要在 Build 阶段构建的哈希表可以放进内存就行。这个时候，相比 NLJ、SMJ，HJ 的执行效率是最高的。因此，当Broadcast Join 的前提条件存在，在可以采用 HJ 的情况下，Spark 自然就没有必要再去用 SMJ 这种前置开销（排序）比较大的方式去完成数据关联。</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/cd/04/e27b7803.jpg" width="30px"><span>小新</span> 👍（8） 💬（1）<div>SMJ 在执行稳定性方面，远胜于 HJ,这句话怎么理解？
还有在做等值关联时，优先级是：Broadcast HJ Shuffle SMJ Shuffle HJ那什么情况下Shuffle HJ会启用呢？</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（2） 💬（4）<div>“学习过 Shuffle 之后，我们知道，Shuffle 在 Map 阶段往往会对数据做排序，而这恰恰正中 SMJ 机制的下怀。”
老师问下这里 join 之前应该还得再排一次序吧？因为 map 阶段的排序只能保证 reduce task 从每个 map task 拉取过来的数据片段是有序的，但是多个数据片段之间还是无序的吧</div>2021-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/7d/57/c94b6a93.jpg" width="30px"><span>王璀璨</span> 👍（1） 💬（1）<div>老师最近在用spark重构pandas的时候遇到一个问题，在udf中使用filter查询的时候报错

temp_data = hospital_data_sheet1.groupby([&#39;hcp_id&#39;, &#39;hcp_name&#39;]).count().select(&#39;hcp_id&#39;, &#39;hcp_name&#39;)

def get_data(data1): 
    search_data = hospital_data_sheet1.select((hospital_data_sheet1[&#39;hcp_id&#39;] == data1))
    total = data1
    return total
    
get_number = F.udf(get_data, StringType())
result_data = temp_data.withColumn(&#39;total&#39;, get_number(temp_data[&#39;hcp_id&#39;]))
result_data.show()

最后报错  _pickle.PicklingError: Could not serialize object: TypeError: cannot pickle &#39;_thread.RLock&#39; object   不知道为什么会这样，请老师看一下
</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/6d/c20f2d5a.jpg" width="30px"><span>LJK</span> 👍（1） 💬（1）<div>老师好，工作中碰到过ERROR BroadcastExchangeExec: Could not execute broadcast in 300 secs.的报错，请问这种报错的排查思路以及有哪些可能的原因导致的呢？</div>2021-11-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/IcDlyK6DaBrssVGlmosXnahdJ4bwCesjXa98iaapSDozBiagZTqSCok6iaktu2wOibvpNv9Pd6nfwMg7N7KTSTzYRw/132" width="30px"><span>慢慢卢</span> 👍（0） 💬（1）<div>&quot;学习过 Shuffle 之后，我们知道，Shuffle 在 Map 阶段往往会对数据做排序，而这恰恰正中 SMJ 机制的下怀。对于已经排好序的两张表，SMJ 的复杂度是 O(M + N)，这样的执行效率与 HJ 的 O(M) 可以说是不相上下。再者，SMJ 在执行稳定性方面，远胜于 HJ，在内存受限的情况下，SMJ 可以充分利用磁盘来顺利地完成关联计算。因此，考虑到 Shuffle SMJ 的诸多优势，Shuffle HJ 就像是关公后面的周仓，Spark SQL 向来对之视而不见，所以对于 HJ 你大概知道它的作用就行。&quot;

这段里面提到SMJ可以利用磁盘完成计算，结合前面提到内存管理，能使用磁盘的除了cache、shuffle write外，也就是说内存计算其他过程也会使用到磁盘(比如SMJ)，但我理解内存计算应该完全在内存中，不然就不会有OOM了。  所以这点我没有搞懂，辛苦老师指导解释下。</div>2021-12-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIjUDIRQ0gRictgQpjWia38qjN3pYicfzahAwbntWq93CorhjiaIOVh7j2Fj6a9WxUW85icMxF3r2Ymblg/132" width="30px"><span>Geek_038655</span> 👍（0） 💬（1）<div>请问：大表join大表怎么优化？</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/c2/97/80119860.jpg" width="30px"><span>思绪纷繁</span> 👍（1） 💬（0）<div>【由于左表与右表在并行度（分区数）上是一致的】
想问下，只要做shuffle join操作，左表和右表的的并行度一定是一样的吗？</div>2023-06-06</li><br/><li><img src="" width="30px"><span>InfoQ_11351e216def</span> 👍（0） 💬（0）<div>老师您好，想问一下，这里 shuffle 的时候会基于 hash 对两个表的数据分区，这只能保证等值关联的情况节点上有对应的数据，那如果不是等值关联呢？比如 a.id &lt; b.aid这种类似的情况，那岂不是驱动表的每条数据都需要扫描被驱动表的每条数据吗？spark 如何做到呢？</div>2024-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/26/eb/24e0ac9c.jpg" width="30px"><span>嬴梦川</span> 👍（0） 💬（0）<div>shuffle write 过程中对结构中的数据记录按（目标分区 ID，Key）排序， 排列后的结果应该不光对“目标分区 ID”有序，也应该对“Key”有序。这样在reduce阶段拉取数据时再做一次时间复杂度为O(N)归并排序就行了。不会改变复杂度O(M+N)的最终结果</div>2023-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/26/eb/24e0ac9c.jpg" width="30px"><span>嬴梦川</span> 👍（0） 💬（0）<div>第六章中, shuffle write 过程中对结构中的数据记录按（目标分区 ID，Key）排序， 排列后的结果应该不光对“目标分区 ID”有序，也应该对“Key”是有序的吧</div>2023-09-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJUlRd4IKK2GA1rLcIeJlXsialRZPLTuWdUllEZGK05zsA5ma3V0E2icJWic7HiaregPeAnYv1N6Xfhpw/132" width="30px"><span>18736416569</span> 👍（0） 💬（0）<div>老师好，前几天跑任务时遇到了关于join的一个问题，很是不解：逻辑是这样的：a表id去left join b表的id_1或者id_2，我用的是a.id = b.id_1 OR a.id = b.id_2，发现spark采用的是BroadCastNestedLoopJoin,难道这不算是等值连接吗？</div>2023-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b3/15/30822e33.jpg" width="30px"><span>小麦</span> 👍（0） 💬（1）<div>【由于左表与右表在并行度（分区数）上是一致的】
想问下，如果是 Hadoop RDD，左表数据量很大，以 128M 划分成10个分区，而右表只有2个分区。如何进行后续的计算呢？</div>2022-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e7/8e/318cfde0.jpg" width="30px"><span>Spoon</span> 👍（0） 💬（0）<div>使用Boradcast SMJ需要前置排序，纯内存的排序最好也需要O(nlgn)的复杂度，更何况是Sorted Merge可能还会利用磁盘排序，这就得不偿失了</div>2022-04-10</li><br/>
</ul>