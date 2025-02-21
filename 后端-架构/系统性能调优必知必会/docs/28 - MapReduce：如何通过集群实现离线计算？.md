你好，我是陶辉。

接下来的2节课我将介绍如何通过分布式集群优化计算任务。这一讲我们首先来看对于有边界静态数据的离线计算，下一讲再来看对无边界数据流的实时计算。

对大量数据做计算时，我们通常会采用分而治之的策略提升计算速度。比如单机上基于递归、分治思想实现的快速排序、堆排序，时间复杂度只有O(N\*logN)，这比在原始数据集上工作的插入排序、冒泡排序要快得多（O(N2)）。然而，当单机磁盘容量无法存放全部数据，或者受限于CPU频率、核心数量，单机的计算时间远大于可接受范围时，我们就需要在分布式集群上使用分治策略。

比如，大规模集群每天产生的日志量是以TB为单位计算的，这种日志分析任务单台服务器的处理能力是远远不够的。我们需要将计算任务分解成单机可以完成的小任务，由分布式集群并行处理后，再从中间结果中归并得到最终的运算结果。这一过程由Google抽象为[MapReduce](https://zh.wikipedia.org/wiki/MapReduce) 模式，实现在Hadoop等分布式系统中。

虽然MapReduce已经有十多个年头的历史了，但它仍是分布式计算的基石，这种编程思想在新出现的各种技术中都有广泛的应用。比如当在单机上使用TensorFlow完成一轮深度学习的时间过久，或者单颗GPU显存无法存放完整的神经网络模型时，就可以通过Map思想把数据或者模型分解给多个TensorFlow实例，并行计算后再根据Reduce思想合并得到最终结果。再比如知识图谱也是通过MapReduce思想并行完成图计算任务的。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（7） 💬（1）<div>能够使用mapreduce思想处理的任务是可以分解且子任务之间没有依赖关系，最后可以做合并的类型。</div>2020-07-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLMDBq7lqg9ZasC4f21R0axKJRVCBImPKlQF8yOicLLXIsNgsZxsVyN1mbvFOL6eVPluTNgJofwZeA/132" width="30px"><span>Run</span> 👍（1） 💬（1）<div>多看看算法,数据结构是没错的</div>2020-07-31</li><br/>
</ul>