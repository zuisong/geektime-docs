你好，我是唐聪。

你知道吗？ 虽然Kubernetes社区官网文档目前声称支持最大集群节点数为5000，但是云厂商已经号称支持15000节点的Kubernetes集群了，那么为什么一个小小的etcd能支撑15000节点Kubernetes集群呢？

今天我就和你聊聊为了支撑15000节点，Kubernetes和etcd的做的一系列优化。我将重点和你分析Kubernetes针对etcd的瓶颈是如何从应用层采取一系列优化措施，去解决大规模集群场景中各个痛点。

当你遇到etcd性能瓶颈时，希望这节课介绍的大规模Kubernetes集群的最佳实践经验和优化技术，能让你获得启发，帮助你解决类似问题。

## 大集群核心问题分析

在大规模Kubernetes集群中会遇到哪些问题呢？

大规模Kubernetes集群的外在表现是节点数成千上万，资源对象数量高达几十万。本质是更频繁地查询、写入更大的资源对象。

首先是查询相关问题。在大集群中最重要的就是如何最大程度地减少expensive request。因为对几十万级别的对象数量来说，按标签、namespace查询Pod，获取所有Node等场景时，很容易造成etcd和kube-apiserver OOM和丢包，乃至雪崩等问题发生。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIkLFmZdzwjU2p6cQb8ZehefhibVicNyHq2KFHyibicHLgEo9u8hLibvKmBfmSfZWEQhW4l3CElBc5fo8Q/132" width="30px"><span>Geek_e5cec2</span> 👍（7） 💬（1）<div>支持和生产用差距很大、etcd不改造、还是有差距、感觉讲的不透。生产最大问题还是APIserver负载问题：
1.默认情况下APIserver endpoints过多、本身k8s的负载即使是轮训其实本身而言是不均衡的、很容易APIserver长时间后oom、因为大部分是长链接。这个时候最合适的是最小链接访问。需要依赖lb之类的
2.APIserver in cluster访问容易出问题、in cluster走的一般是service ip。这时候很容易有netfilter问题、不管走的是iptables或者ipvs。
3.in cluster也会负载不均衡、因为endpoints也是轮询。轮询不是最小链接轮询。这里不换成lb还是很难。
4. 极端情况下会触发 list -&gt; watch -&gt; too old resource version -&gt; list 的恶性循环。
5. etcdserver: request is too large问题、本身APIserver序列化的问题。
6.还有日志输出不合理导致APIserver抖动等等。</div>2022-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/38/4f89095b.jpg" width="30px"><span>写点啥呢</span> 👍（5） 💬（1）<div>请问老师，etcd的并发读特性由于会复制写事务的内存，在并发量大的时候是不是会进一步加大内存压力，导致OOM的风险？</div>2021-03-05</li><br/><li><img src="" width="30px"><span>InfoQ_aeed61b02780</span> 👍（2） 💬（1）<div>老师，我理解etcd的一次snapshot save也就是一次expensive request。
目前我们通过snapshot save备份任务时固定出现&quot;request result took too long&quot;的问题，请问下老师，这块有哪些优化的空间呢？</div>2021-08-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7RiaNu1mRU2deLcEHf4adPClhFbWQf1dFGDhODtu2rDYwK7BDJicdia7Ou19OlZZPzLRW7cEVlQ5jeg/132" width="30px"><span>13950387940</span> 👍（1） 💬（1）<div>不不不，不是原地升级呢。我之前表达的不是很明确，是这样的。

node节点只要一重启，重启后该node上所有的docker容器都会重新创建，我的容器是有状态服务，里面存在数据。所以我不想他这么做，找了很多资料都没这方面的解决办法</div>2021-09-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7RiaNu1mRU2deLcEHf4adPClhFbWQf1dFGDhODtu2rDYwK7BDJicdia7Ou19OlZZPzLRW7cEVlQ5jeg/132" width="30px"><span>13950387940</span> 👍（0） 💬（1）<div>老师你好，我想问一下您，我也是做云平台的。
我想问一下k8s上创建的pod基于docker的，重启之后pod里的docker就会重建。查资料也没有什么解决办法，看日志是因为重启后pod ip的原因，不知道老师是否有遇到这样的问题，希望能指点一二</div>2021-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4c/83/7788fc66.jpg" width="30px"><span>Simon</span> 👍（0） 💬（4）<div>思考题:

应该是能保证的, 

apiserver会把continueToken返回到client, client发现返回的结果中continueToken不为空时, 下次请求会带着continueToken请求apiserver

请问老师是这样的吗?</div>2021-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/68/83/ecd4e4d6.jpg" width="30px"><span>WGJ</span> 👍（0） 💬（0）<div>老师,Kubernetes 为了维持上万节点的心跳，会产生大量写请求, 这句话中的心跳请求为什么也算是写请求,会触发写的动作吗</div>2023-04-23</li><br/><li><img src="" width="30px"><span>Geek_acb401</span> 👍（0） 💬（0）<div>赞</div>2022-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b4/00/bfc101ee.jpg" width="30px"><span>Tendrun</span> 👍（0） 💬（0）<div>这个watchCache的维护流程老师可以介绍下么，比如这个cache初始化的时候是如何选择数据的，比如缓存了pod类型的数据，那么这么多pod对象从那个版本开始缓存呢？或者list之后缓存全部版本数据么，但是好像这个缓存都大小的，合适不合适缓存全部数据呢？而且如果缓存过小，如果连当前所有pod的最新一个版本的数据都缓存不了，那这个时候怎么办呢</div>2022-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4b/80/27be4a80.jpg" width="30px"><span>Trouble man</span> 👍（0） 💬（0）<div>总结的太好！</div>2021-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/61/e6/fedd20dc.jpg" width="30px"><span>mmm</span> 👍（0） 💬（2）<div>工作中遇到apiserver报resource version冲突，更新资源失败的错误，apiserver的trace日志记录读资源性能在500ms左右，怀疑是etcd和apiserver性能问题，导致informer没能获取到资源更新，controller继续用旧的resource version去更新资源，导致resource version冲突报错，但是此时etcd和apiserver的性能问题该如何排查呢
还遇到过apiserver报list&amp;watch失败，应该也是etcd性能问题导致，请问排查etcd性能问题常用的操作有哪些？</div>2021-03-21</li><br/>
</ul>