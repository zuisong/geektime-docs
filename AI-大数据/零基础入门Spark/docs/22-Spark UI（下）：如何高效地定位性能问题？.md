你好，我是吴磊。

在上一讲，我们一起梳理了Spark UI的一级入口。其中Executors、Environment、Storage是详情页，开发者可以通过这3个页面，迅速地了解集群整体的计算负载、运行环境，以及数据集缓存的详细情况。不过SQL、Jobs、Stages，更多地是一种罗列式的展示，想要了解其中的细节，还需要进入到二级入口。

沿用之前的比喻，身为“大夫”的开发者想要结合经验，迅速定位“病灶”，离不开各式各样的指标项。而今天要讲的二级入口，相比一级入口，内容更加丰富、详尽。要想成为一名“临床经验丰富”的老医生，咱们先要做到熟练解读这些度量指标。

![图片](https://static001.geekbang.org/resource/image/56/d2/56563537c4e0ef597629d42618df21d2.png?wh=718x52 "Spark UI导航条：一级入口")

所谓二级入口，它指的是，**通过一次超链接跳转才能访问到的页面**。对于SQL、Jobs和Stages这3类入口来说，二级入口往往已经提供了足够的信息，基本覆盖了“体检报告”的全部内容。因此，尽管Spark UI也提供了少量的三级入口（需要两跳才能到达的页面），但是这些隐藏在“犄角旮旯”的三级入口，往往并不需要开发者去特别关注。

接下来，我们就沿着SQL -&gt; Jobs -&gt; Stages的顺序，依次地去访问它们的二级入口，从而针对全局DAG、作业以及执行阶段，获得更加深入的探索与洞察。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM4gIlRyVTOlTP8p1ucUN7Ahf2XMAicFpOHfk2UcrxEFm8GKIyCKGxd0PgBU0tMKwfPia8Ulk6rYBHVw/132" width="30px"><span>Geek_d4ccac</span> 👍（1） 💬（4）<div>老师好！有两个问题 1）括号里面的min，med，max是对什么取的极小，中数和极大。2）上一节设置了2 executor 每个3 GB memory， 为啥”peak memory total”会是18.8GB呢？ 谢谢！</div>2021-11-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJcoaDg65dGx3qBibvWM03AibqEH6AbYgU1BNALkhZokhX4L3uMausN374mWOtpMRaCto93dbsSKYtQ/132" width="30px"><span>Geek_1e4b29</span> 👍（1） 💬（2）<div>一直对spill mem有点迷糊，假设有一份数据，按spark数据结构，在内存要100G，放磁盘要150G，如果executor是20G的话，忽略其他存储，spill memory以及spill disk大概是多少? 😂</div>2021-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/cd/04/e27b7803.jpg" width="30px"><span>小新</span> 👍（0） 💬（1）<div>请问原始数据在内存中展开之后的总大小，这句话怎么理解？</div>2021-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/d6/b9513db0.jpg" width="30px"><span>kingcall</span> 👍（0） 💬（2）<div>我在把最后的结果show 出来的时候，为啥会提交两个job 呢？ 下面是截图
https:&#47;&#47;kingcall.oss-cn-hangzhou.aliyuncs.com&#47;blog&#47;img&#47;image-20211029160825553.png</div>2021-10-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJIocn8OMjfSGqyeSJEV3ID2rquLR0S6xo0ibdNYQgzicib6L6VlqWjhgxOqD2iaicX1KhbWXWCsmBTskA/132" width="30px"><span>虚竹</span> 👍（0） 💬（0）<div>D &#47; P ~ M &#47; C，来相应地调整 CPU、内存与并行度，从而减低任务的调度开销。其中，D 是数据集尺寸，P 为并行度，M 是 Executor 内存，而 C 是 Executor 的 CPU 核数。波浪线~ 表示的是，等式两边的数值，要在同一量级。 老师好，辛苦给一个带单位的实际的例子，谢谢</div>2025-02-04</li><br/><li><img src="" width="30px"><span>Geek_3277ae</span> 👍（0） 💬（0）<div>您好，shuffle read time时间过长是什么原因呢？是computing time的10-20倍左右</div>2023-08-01</li><br/>
</ul>