你好，我是徐文浩。

在上节课里，我们了解了Raft算法，知道了它是怎么把“状态机复制”这样一个问题，拆解成了Leader选举、日志同步以及安全性三个子问题。那么，今天这节课，我们会进一步深入来了解Raft算法的另外几个问题。

这些问题，虽然在实践中我们必然会遇到，但是之前讲解各类分布式系统的时候，我们很少提到。正好，趁此机会，我们可以对在Raft集群中如何动态增减服务器，以及如何为Raft的状态机创建快照加以学习，并予以掌握。

# 成员变更（Membership Change）

无论是上节课我们讲解Raft的算法，还是之前我们在Chubby的论文里介绍的Paxos算法，我们都没有讲解往集群里增减服务器会发生什么情况。但是，这种情况其实是运维这些系统时，必然会遇到的情况。

比如，我们遇到某台服务器硬件故障了，需要往集群里增加一台服务器，并把坏了的服务器去掉。或者，我们为了系统的可用性考虑，往原先3台服务器组成的Raft集群里，加两台变成5台服务器，这样我们可以容忍集群里挂掉两台服务器，而不是原先的一台。

最简单的增减服务器的方式，当然是把整个集群停机，修改配置然后重启。但是，我们使用Raft这样的算法就是为了高可用性，所以显然我们不能这么做。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/c9/5d03981a.jpg" width="30px"><span>thomas</span> 👍（1） 💬（2）<div>当时的 Leader 是 Cold​ 老配置里的服务器，而不是 Cnew​ 里的服务器。一旦提交成功，我们的集群里就已经没有这个服务器的位置了。那该怎么办呢？
---------------&gt;
Cnew配置不是包含Cold的配置吗， 为什么会没有这个服务器的位置？比如old配置[A,B,C], 新增一台，new配置[A,B,C,D]</div>2023-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/c9/5d03981a.jpg" width="30px"><span>thomas</span> 👍（0） 💬（0）<div>按服务器 B 的配置后更新，在没有更新的时候，它觉得有 2 服务器的投票就是多数通过了；
----------》
成员变更的配图有问题， B配置没更新的时候，服务器B还不知道新加进来的服务器D, 怎么可能D会选择B</div>2023-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/04/30/7f2cb8e3.jpg" width="30px"><span>CRT</span> 👍（0） 💬（0）<div>加一天日志，标记前面哪些日志是需要逻辑删除的，后面不扫描即可</div>2022-01-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIVR2wY9icec2CGzZ4VKPdwK2icytM5k1tHm08qSEysFOgl1y7lk2ccDqSCvzibHufo2Cb9c2hjr0LIg/132" width="30px"><span>dahai</span> 👍（0） 💬（0）<div>Raft集群 仍然可能会遇到：即使是压实后的数据仍然接近单机的存储，这时候可能要替换现有的机器换成更高配置的机器，这种情况下怎么处理？</div>2021-12-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（0） 💬（0）<div>思考题：类似lsm tree的方式，通过append only把删除某条记录追加进去。</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2c/56/ff7a9730.jpg" width="30px"><span>许灵</span> 👍（0） 💬（0）<div>关于思考题，应该可以用标记删除，加append only的方式进行，同时在log compaction的时候再进行物理删除</div>2021-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（0）<div>关于思考题，我的想法是，采用dataflow的高低水位方式来处理，从其它节点同步数据是低水位，自己节点写入数据是高水位。如果需要删除日志，从低水位复写就好了，同时利用了硬盘顺序写</div>2021-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/bb/abb7bfe3.jpg" width="30px"><span>csyangchsh</span> 👍（0） 💬（1）<div>关于思考题，当找到共同点后，是否可以直接将共同点之前的日志复制到新文件，在新文件上日志写入就可以是append only方式了。因为有快照机制，共同点之前的日志数量应该不会很多。</div>2021-12-27</li><br/>
</ul>