你好，我是徐文浩。

课程进行到这里，我们对于各类大数据系统的论文的解读，就已经结束了。不过，真的要把大数据系统运用到实践当中，我们仍然会遇到很多挫折。在2010年，我第一次开始使用Hadoop。在读完了论文和教程，开始撰写Java MapReduce的代码之后，我的第一感觉是“大数据不过如此”。

不过，在逐步深入尝试利用数据做越来越多的事情之后，我们遇到了越来越多意料之外的问题。大部分困难的来源，往往并不是纯粹的技术问题。毕竟，那些问题都可以靠读代码、记日志、找个环境复现问题来解决。更多的挑战，来自于**系统和系统之间的“鸿沟”，不同团队和角色之间的“鸿沟”**。

日志格式的含义、工程师和数据科学家之间的技能树的差异，乃至于不同数据报表之间的依赖关系，都会成为我们快速分析数据、产出结论的鸿沟。难以精确定义的业务目标，与实际需要精确定义才能变成代码的技术开发之间的鸿沟，更是挡在大部分数据科学家面前的一座大山。

那么，对于这样看似软性的问题，我们是不是只能靠“加强沟通”来解决呢？接下来，我们就一起来看看，Twitter这家公司是怎么做的吧。今天，就请你和我一起来读一读《[Scaling big data mining infrastructure: the twitter experience](http://cs-sys-1.uis.georgetown.edu/~jl1749/cs_class_public_html/mapreduce_crs/material/Lin_Ryaboy_2012.pdf)》这篇论文。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（3） 💬（0）<div>徐老师好，当数据遇上AI，需要从源头来规范日志格式，用一种语言处理整个流程，这一切都是为了提升数据科学家的工作效率。这说明数据的价值来自于分析，以及所得出的结论。在阅读《Streaming System》时我以为流式处理是大数据未来的方向，但是我最近在读《数学之美》和《智能时代》，发现大数据的价值在于服务于AI，而AI的重点不在于实时性，而在于海量、完备性和相关性。实时处理是当今的热点，不过比起追逐潮流，更重要的是理解数据，才构建高效的大数据环境，让数据发挥价值。</div>2022-01-19</li><br/><li><img src="" width="30px"><span>Geek_88604f</span> 👍（0） 💬（0）<div>看来大数据需要和数据仓库建模理论结合</div>2022-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>clickhouse 这些sql 系统的 udf 可以用python 来实现机器学习吗？</div>2022-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（0）<div>良好管理的元数据，会大大提升数据科学家们的工作团队效率。这个深有体会，我们之前数据字典不规范，导致部门之间的信息不均衡，后来通过统一数据字典以及可视化的方式，来统一信息的一致性</div>2022-01-19</li><br/>
</ul>