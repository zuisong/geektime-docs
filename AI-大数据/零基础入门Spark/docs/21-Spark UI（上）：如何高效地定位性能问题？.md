你好，我是吴磊。

到目前为止，我们完成了基础知识和Spark SQL这两个模块的学习，这也就意味着，我们完成了Spark入门“三步走”中的前两步，首先恭喜你！在学习的过程中，我们逐渐意识到，Spark Core与Spark SQL作为Spark并驾齐驱的执行引擎与优化引擎，承载着所有类型的计算负载，如批处理、流计算、数据分析、机器学习，等等。

那么显然，Spark Core与Spark SQL运行得是否稳定与高效，决定着Spark作业或是应用的整体“健康状况”。不过，在日常的开发工作中，我们总会遇到Spark应用运行失败、或是执行效率未达预期的情况。对于这类问题，想找到根本原因（Root Cause），我们往往需要依赖Spark UI来获取最直接、最直观的线索。

如果我们把失败的、或是执行低效的Spark应用看作是“病人”的话，那么Spark UI中关于应用的众多度量指标（Metrics），就是这个病人的“体检报告”。结合多样的Metrics，身为“大夫”的开发者即可结合经验来迅速地定位“病灶”。

今天这一讲，让我们以小汽车摇号中“倍率与中签率分析”的应用（详细内容你可以回顾[第13讲](https://time.geekbang.org/column/article/374776)）为例，用图解的方式，一步步地去认识Spark UI，看一看它有哪些关键的度量指标，这些指标都是什么含义，又能为开发者提供哪些洞察（Insights）？
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/iaQgtbE98VGIVIyribdo6dgLOnaNoe7ZdUuPr60ibsduibscrzQCTzdW2AfL9nxwe8YlSK75gOnK3YbAJKTaFPxibdg/132" width="30px"><span>小李</span> 👍（9） 💬（1）<div>1、我想数量不一致是由于Executors在处理这个application下的所有job(一个job由action算子来触发,每个job又会根据shuffle情况划分出多个stage，每个stage中又会划分出多个task，再根据taskScheduler分配到各个Excecutor)得出来的Complete Tasks。
</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/2c/0a/779abf52.jpg" width="30px"><span>LHF</span> 👍（5） 💬（3）<div>第一个：每个rdd经过处理后，又可能生成其他rdd，这里的tasks应该是显示整个executors处理过的任务数，跟rdd的blocks无关。
第二个：因为代码最后一个是save，会生成一个save的action</div>2021-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/d3/0a/92640aae.jpg" width="30px"><span>我爱夜来香</span> 👍（2） 💬（2）<div>老师,请问下4040端口和8080端口有什么区别和联系啊?</div>2022-01-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM4gIlRyVTOlTP8p1ucUN7Ahf2XMAicFpOHfk2UcrxEFm8GKIyCKGxd0PgBU0tMKwfPia8Ulk6rYBHVw/132" width="30px"><span>Geek_d4ccac</span> 👍（0） 💬（1）<div>老师好！我有一个疑问，所以这一节准备工作部分的code example并不是后面spark ui里跑的code么？ 我这边显示最后是result.collect。。。</div>2021-11-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erG6I79WlHDjs51JOff9GBibD4Fh2PhITQMvmh2aTUVzH2BKia1tFLLoQr7VFeZddywwRoZlVUyhDDQ/132" width="30px"><span>Geek_frank</span> 👍（0） 💬（0）<div>这个可以禁用掉吗，感觉这块也挺占资源的。在开发环境调试的时候可以用用。产线这块最好禁掉</div>2023-08-09</li><br/>
</ul>