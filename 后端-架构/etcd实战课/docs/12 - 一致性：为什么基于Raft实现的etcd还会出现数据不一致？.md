你好，我是唐聪。

今天我要和你分享的主题是关于etcd数据一致性的。

我们都知道etcd是基于Raft实现的高可用、强一致分布式存储。但是有一天我和小伙伴王超凡却遭遇了一系列诡异的现象：用户在更新Kubernetes集群中的Deployment资源镜像后，无法创建出新Pod，Deployment控制器莫名其妙不工作了。更令人细思极恐的是，部分Node莫名其妙消失了。

我们当时随便找了一个etcd节点查看存储数据，发现Node节点却在。这究竟是怎么一回事呢？ 今天我将和你分享这背后的故事，以及由它带给我们的教训和启发。希望通过这节课，能帮助你搞懂为什么基于Raft实现的etcd有可能出现数据不一致，以及我们应该如何提前规避、预防类似问题。

## 从消失的Node说起

故事要从去年1月的时候说起，某日晚上我们收到一个求助，有人反馈Kubernetes集群出现了Deployment滚动更新异常、节点莫名其妙消失了等诡异现象。我一听就感觉里面可能大有文章，于是开始定位之旅。

我首先查看了下Kubernetes集群APIServer、Controller Manager、Scheduler等组件状态，发现都是正常。

然后我查看了下etcd集群各节点状态，也都是健康的，看了一个etcd节点数据也是正常，于是我开始怀疑是不是APIServer出现了什么诡异的Bug了。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/22/3b/46/3701e908.jpg" width="30px"><span>Coder</span> 👍（10） 💬（1）<div>精彩，总体上获得以下收获:
1. 基础篇知识学以致用，问题定位、分析思路
2. 不一致bug原因，复制状态机模式的问题，应用日志条目到状态机时，因etcd里面含有各种业务逻辑，无法保证各个节点都成功
3. 了解几个常见不一致的bug， 这个老师能给下详细的github issue、pr地址，还需要深入消化小才能彻底搞懂
4. 最佳实践干货满满，感受到了老师在这块的丰富经验，我感觉监控key数挺好用的，也简单，数据安全是红线，定时备份太重要了，否则遇到老师说的数据不一致bug，就欲哭无泪了</div>2021-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/1f/abb7bfe3.jpg" width="30px"><span>yangf</span> 👍（8） 💬（3）<div>在项目中大量使用了 etcd，这里介绍两个曾经遇到的问题。
1. 使用 etcd watch，在 go watch client 中出现大量内存堆积的问题，一度怀疑是 etcd lib 的问题，深入定位后发现是从 watch channel 中消费速度小于 key 变更速度导致。（在我的个人博客里记录了这个问题：https:&#47;&#47;amyangfei.me&#47;2020&#47;12&#47;19&#47;best-practice-with-go-etcd&#47;#Consume-data-from-the-watch-response-channel-ASAP ）
2. 使用 etcd lease 的一系列问题，包括 concurrency 包提供的 `session.Done` 通知存在延迟问题，etcd lease 删除 key 也存在的延迟删除问题。（个人博客里还有一篇文章对 lease 的一些实现原理和使用注意点做了分析：https:&#47;&#47;amyangfei.me&#47;2020&#47;12&#47;27&#47;thinking-about-etcd-lease&#47;）

遇到 etcd 使用问题经常搜索，还见到过唐老师提的 issue&#47;pr :-)</div>2021-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d8/63/e4c28138.jpg" width="30px"><span>春风</span> 👍（2） 💬（2）<div>老师，leader需要法定人数，脑裂在什么情况下发生呢</div>2021-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/d6/b2/449b4ae3.jpg" width="30px"><span>shp</span> 👍（1） 💬（1）<div>请问老师，每隔30分钟备份一次，如果需要使用备份恢复数据，那么在备份后到使用备份恢复前这段时间的数据操作是不是会全部丢失，还是有什么方法只恢复损坏的数据？</div>2021-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/38/4f89095b.jpg" width="30px"><span>写点啥呢</span> 👍（1） 💬（1）<div>请教唐老师，04节内容中介绍etcd写请求流程中涉及到多个log，不稳定raft log-&gt;wal -&gt; 稳定raft log，能不能请老师进一步介绍下这三个日志的用处和关系呢？特别是在涉及到节点崩溃数据恢复时候这几个日志是如何配合恢复数据的？

谢谢老师</div>2021-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/31/1a/fd82b2d5.jpg" width="30px"><span>Tachone</span> 👍（0） 💬（0）<div>apply 失败为啥不强制设置raft状态机为error呢，拒绝写入，这样应该是最安全的，不会出现数据不一致了还在写入</div>2023-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/28/cb/7431e82e.jpg" width="30px"><span>yybear</span> 👍（0） 💬（0）<div>获取各个节点的 revision 和 boltdb hash 值，若出现 Follower 节点的 revision 大于 Leader 等异常情况时，就可以认为不一致
---------------------------------
revision 是apply时递增的，如果follower的apply处理速度大于Leader 的速度，是存在Follower 节点的 revision 大于 Leader的情况吧？</div>2021-10-08</li><br/>
</ul>