你好，我是唐聪。

在使用etcd的过程中，你是否被异常内存占用等现象困扰过？比如etcd中只保存了1个1MB的key-value，但是经过若干次修改后，最终etcd内存可能达到数G。它是由什么原因导致的？如何分析呢？

这就是我今天要和你分享的主题：etcd的内存。 希望通过这节课，帮助你掌握etcd内存抖动、异常背后的常见原因和分析方法，当你遇到类似问题时，能独立定位、解决。同时，帮助你在实际业务场景中，为集群节点配置充足的内存资源，遵循最佳实践，尽量减少expensive request，避免etcd内存出现突增，导致OOM。

## 分析整体思路

当你遇到etcd内存占用较高的案例时，你脑海中第一反应是什么呢？

也许你会立刻重启etcd进程，尝试将内存降低到合理水平，避免线上服务出问题。

也许你会开启etcd debug模式，重启etcd进程等复现，然后采集heap profile分析内存占用。

以上措施都有其合理性。但作为团队内etcd高手的你，在集群稳定性还不影响业务的前提下，能否先通过内存异常的现场，结合etcd的读写流程、各核心模块中可能会使用较多内存的关键数据结构，推测出内存异常的可能原因？

全方位的分析内存异常现场，可以帮助我们节省大量复现和定位时间，也是你专业性的体现。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/4e/c266bdb4.jpg" width="30px"><span>[小狗]</span> 👍（17） 💬（3）<div>大佬，我想阅读下etcd的源码，有什么建议吗？ 目前只是为了简历好看些，以后会深度学习下</div>2021-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/65/b7/058276dc.jpg" width="30px"><span>i_chase</span> 👍（5） 💬（1）<div>这一期的思考题有答案吗</div>2022-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a2/94/ae0a60d8.jpg" width="30px"><span>江山未</span> 👍（3） 💬（2）<div>老师，想问下。工作中有用到etcd，如果想通过看etcd源码提升了解的话，建议从哪里入手呢。
如果可能的话，也希望能像你一样，为社区做一些贡献。
直接从启动命令看下去吗？还有就是 treeindex和bbolt有必要看吗。</div>2021-03-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep075ibtmxMf3eOYlBJ96CE9TEelLUwePaLqp8M75gWHEcM3za0voylA0oe9y3NiaboPB891rypRt7w/132" width="30px"><span>shuff1e</span> 👍（3） 💬（1）<div>etcd v2 的 key-value 都是存储在内存树中，具体指的是什么呢</div>2021-02-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epRVT3U6UOpRAoOOYMm0flMeX4P1VJpSnZBlaBvdW4KhWKr0BunLFlCxibdHc9s6VArA124FpwzRiaw/132" width="30px"><span>guoqp</span> 👍（0） 💬（0）<div>老师好，我们生产环境使用了3.5版本，内存持续涨，压缩和快照效果一般，后来通过手动碎片整理内存才趋于稳定。每次手动处理或加cron处理总觉得不是最优解，是否有其他方式，例如优化配置参数</div>2024-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/46/2a/46c2774c.jpg" width="30px"><span>孔宣</span> 👍（0） 💬（0）<div>大佬，能给个联系方式吗？想请教一下kstone方面的问题，目前的问题主要是：
1、能否支持3.5.0版本的etcd集群新建？
2、是否支持指定不同的k8s集群来新建etcd集群？在dashbord上没看到这能力
3、目前支持的k8s版本相对老旧，是否有升级计划，我们也可以共建</div>2023-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/46/2a/46c2774c.jpg" width="30px"><span>孔宣</span> 👍（0） 💬（0）<div>请问，kstone目前最新只支持etcd的3.4.13版本，但我们对etcd 3.5版本有强需求，支持3.5版本，需要做改造吗？盼复。。。微信加的kstone助手，没人理</div>2023-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/3e/925aa996.jpg" width="30px"><span>HelloBug</span> 👍（0） 💬（0）<div>一个客户端是一个Client，watch一个key是一个watcher，gRPC Watch Stream 数如何确定呢？</div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/3e/925aa996.jpg" width="30px"><span>HelloBug</span> 👍（0） 💬（0）<div>&gt;其次是 goroutines 泄露导致内存占用高。此问题可能会在容器化场景中遇到。etcd 在打印日志的时候，若出现阻塞则可能会导致 goroutine 阻塞并持续泄露，最终导致内存泄露
老师，这里不太明白，为什么打印日志阻塞会导致内存泄露呢？</div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/ff/cbe8fb58.jpg" width="30px"><span>sxfworks</span> 👍（0） 💬（0）<div>这几天看了etcd的源码，最开始一直好奇leader和follower怎么只同步一次snapshot，是我看错了，还是真的这么粗暴😂</div>2021-05-29</li><br/>
</ul>