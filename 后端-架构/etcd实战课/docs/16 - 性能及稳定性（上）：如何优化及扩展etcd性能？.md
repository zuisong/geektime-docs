你好，我是唐聪。

在使用etcd的过程中，你是否吐槽过etcd性能差呢？ 我们知道，etcd社区线性读[压测结果](https://etcd.io/docs/v3.4.0/op-guide/performance/)可以达到14w/s，那为什么在实际业务场景中有时却只有几千，甚至几百、几十，还会偶发超时、频繁抖动呢？

我相信不少人都遇到过类似的问题。要解决这些问题，不仅需要了解症结所在，还需要掌握优化和扩展etcd性能的方法，对症下药。因为这部分内容比较多，所以我分成了两讲内容，分别从读性能、写性能和稳定性入手，为你详细讲解如何优化及扩展etcd性能及稳定性。

希望通过这两节课的学习，能让你在使用etcd的时候，设计出良好的业务存储结构，遵循最佳实践，让etcd稳定、高效地运行，获得符合预期的性能。同时，当你面对etcd性能瓶颈的时候，也能自己分析瓶颈原因、选择合适的优化方案解决它，而不是盲目甩锅etcd，甚至更换技术方案去etcd化。

今天这节课，我将重点为你介绍如何提升读的性能。

我们说读性能差，其实本质是读请求链路中某些环节出现了瓶颈。所以，接下来我将通过一张读性能分析链路图，为你从上至下分析影响etcd性能、稳定性的若干因素，并给出相应的压测数据，最终为你总结出一系列的etcd性能优化和扩展方法。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/22/3a/de/e5c30589.jpg" width="30px"><span>云原生工程师</span> 👍（8） 💬（4）<div>分析透彻，还有压测数据，有两个收获，鉴权接口之慢，线性读性能随写请求下降之快，请问一下，增加节点能提升线性读性能吗，求压测数据，谢谢老师</div>2021-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/38/4f89095b.jpg" width="30px"><span>写点啥呢</span> 👍（7） 💬（1）<div>请问唐老师，能否详细介绍证书验证机制与密码验证机制的不同之处，为什么它相比密码验证能够提升性能并避免token复用问题？（我理解证书验证基于RSA非对阵加密算法，成本也高）。谢谢老师</div>2021-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9d/84/171b2221.jpg" width="30px"><span>jeffery</span> 👍（6） 💬（2）<div>图文并茂形象生动！每章都很👍！引入 cache 实现缓存 expensive read request 的结果后.怎么维护缓存数据与 etcd 保持强一致性.cache是指内核cache还是别的！突然宕机会不会丢数据.谢谢老师</div>2021-02-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/YbUxEV3741vKZAiasOXggWucQbmicJwIjg3HDE58oyibYXbSop9QQFqZ7X6OhynDoo6rDHwzK8njSeJjN9hx3pJXg/132" width="30px"><span>黄堃健</span> 👍（0） 💬（0）<div>老师， 03中，有这么一段话：首先 boltdb key 是版本号，put&#47;delete 操作时，都会基于当前版本号递增生成新的版本号，因此属于顺序写入。    

但是这里又说随机写。 随机写是在哪一个场景导致的， 是由于boltdb遇到重平衡，分裂导致随机写的吗？
</div>2024-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/46/2a/46c2774c.jpg" width="30px"><span>孔宣</span> 👍（0） 💬（0）<div>唐老师，kstone现在还在维护吗？加了微信没人回复。想在生产上使用，想咨询几个问题</div>2023-04-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epG46rRwzg6HEJBHk01x0j9NGxeG41H3iadrkwlPEfQIic4edZ9JClFHZiafMwxeia0NOpNr8PaS2zOMw/132" width="30px"><span>牛学真</span> 👍（0） 💬（0）<div>收获很大</div>2022-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/60/89/1f424b14.jpg" width="30px"><span>Zhenng</span> 👍（0） 💬（0）<div>老师，我在测etcd集群读性能的时候线性读的性能可以达到14w&#47;s,但是串行读的性能跟线性读的性能相同，也是14w&#47;s，这是为什么？我的etcd版本是3.5.2</div>2022-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/11/f1/ae514e6e.jpg" width="30px"><span>Simon😜</span> 👍（0） 💬（0）<div>老师，多租场景下（不同业务做数据隔离，假设100个业务)，使用证书认证，假设10万个客户端连接，线性读的qps能达到多少呢？</div>2021-04-24</li><br/>
</ul>