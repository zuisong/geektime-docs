你好，我是唐聪。

在使用etcd过程中，我们经常会面临着一系列问题与选择，比如：

- etcd是使用虚拟机还是容器部署，各有什么优缺点？
- 如何及时发现etcd集群隐患项（比如数据不一致）？
- 如何及时监控及告警etcd的潜在隐患（比如db大小即将达到配额）？
- 如何优雅的定时、甚至跨城备份etcd数据？
- 如何模拟磁盘IO等异常来复现Bug、故障？

今天，我就和你聊聊如何解决以上问题。我将通过从etcd集群部署、集群组建、监控体系、巡检、备份及还原、高可用、混沌工程等维度，带你了解如何构建一个高可靠的etcd集群运维体系。

希望通过这节课，让你对etcd集群运维过程中可能会遇到的一系列问题和解决方案有一定的了解，帮助你构建高可靠的etcd集群运维体系，助力业务更快、更稳地运行。

## 整体解决方案

那要如何构建高可靠的etcd集群运维体系呢?

我通过下面这个思维脑图给你总结了etcd运维体系建设核心要点，它由etcd集群部署、成员管理、监控及告警体系、备份及还原、巡检、高可用及自愈、混沌工程等维度组成。

![](https://static001.geekbang.org/resource/image/80/c2/803b20362b21d13396ee099f413968c2.png?wh=1920%2A1409)

## 集群部署

要想使用etcd集群，我们面对的第一个问题是如何选择合适的方案去部署etcd集群。

首先是计算资源的选择，它本质上就是计算资源的交付演进史，分别如下：
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/ae/37b492db.jpg" width="30px"><span>唐聪</span> 👍（20） 💬（2）<div>最近我们开源了一个etcd一站式治理平台kstone.
Kstone 是一个针对 etcd 的全方位运维解决方案，提供集群管理（关联已有集群、创建新集群等)、监控、备份、巡检、数据迁移、数据可视化、智能诊断等一系列特性。
Kstone 将帮助你高效管理etcd集群，显著降低运维成本、及时发现潜在隐患、提升k8s etcd存储的稳定性和用户体验。
https:&#47;&#47;github.com&#47;tkestack&#47;kstone, 欢迎大家star、fork，并加入我们，推动kstone越来越好。</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/53/2b/94b5b872.jpg" width="30px"><span>ly</span> 👍（11） 💬（3）<div>唐老师，在实际的使用中，有一些问题需要咨询您下，还望指点下，多谢老师
1、 etcd auto compact 有推荐的值吗？
2、 etcd backup 是否需要在每个节点上执行？learner 节点 db 文件时候可以当做备份文件来使用？ learner 节点后面可以支持 snapshot吗？ 
3、 etcd 是否需要单独部署，与其他组件分开来？
4、 etcd 巡检有没有开源项目推荐？</div>2021-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9d/84/171b2221.jpg" width="30px"><span>jeffery</span> 👍（5） 💬（1）<div>kubeadm部署.k8s版本升级遇到过数据不一致的情况.还好有backup😀大赞 巡检和混搭工程！level有提高了</div>2021-03-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/1pMbwZrAl5g8ZRC5SOlz9VQOVRGN5V1rFNwsmEehicGzxMRicGj330jNfwTE1MRLaZTdSvX8R2YJVEh8DrYnMVAQ/132" width="30px"><span>Geek_edd932</span> 👍（2） 💬（2）<div>唐老师，我们生产上有3园区，分别是ABC园区，其中AB园区同城。AB园区到C园区有20-30ms的网络延迟。之前集群部署了7个节点，在A部署2节点，在B部署3节点，在C部署2节点。由于网络故障等原因Leader转移到少数派C园区，导致请求延迟将近100ms，从而影响业务。
目前想在AB园区部署节点数量为5的主ETCD集群，其中A园区2个节点，B园区3个节点。在C园区部署节点数量为3的备ETCD集群。通过Maker-mirror工具实现主备ETCD集群数据同步。应用从主ETCD集群存取数据，当主ETCD集群不肯用时，切到备ETCD集群存取数据。由此实现三园区高可用低延迟。
老师，帮忙看看此方案可行性。是否有更好的方案？</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/01/35/1c440045.jpg" width="30px"><span>不想说</span> 👍（1） 💬（1）<div>kubeadm部署堆叠的，每个node有etcd和master的组件的方式可以吗？机器数不是很多</div>2021-07-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/1pMbwZrAl5g8ZRC5SOlz9VQOVRGN5V1rFNwsmEehicGzxMRicGj330jNfwTE1MRLaZTdSvX8R2YJVEh8DrYnMVAQ/132" width="30px"><span>Geek_edd932</span> 👍（0） 💬（1）<div>唐老师，我看了您上次发给我的斗鱼文章，里面提到了腾讯云etcd集群同步工具etcd-syncer，这个工具是开源的吗？</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d9/84/9b03cd04.jpg" width="30px"><span>lidabai</span> 👍（0） 💬（1）<div>用kubeadm的方式部署etcd，是先部署kubernetes集群还是先部署etcd？</div>2021-08-10</li><br/><li><img src="" width="30px"><span>Geek_daf51a</span> 👍（0） 💬（3）<div>老师我们目前是通过bitnami提供etcd helm来部署的，与推荐等业务使用</div>2021-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/fd/60/68c27acf.jpg" width="30px"><span>柠檬🍋</span> 👍（1） 💬（0）<div>唐老师，请教个问题，etcd必须部署在ssd上面吗？etcd对磁盘最低的性能要求（支持k8s集群能够健康稳定运行）是多少呢？</div>2022-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/9d/2b/fefc2b53.jpg" width="30px"><span>王山石</span> 👍（0） 💬（0）<div>唐老师，您好。我看腾讯云开发了异地容灾工具etcd-syncer，不知道这个开源了没有？</div>2023-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/0b/37/20ac0432.jpg" width="30px"><span>sunnoy</span> 👍（0） 💬（0）<div>其实部署最好的etcd集群工具是k3s </div>2023-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e3/48/510fd23d.jpg" width="30px"><span>hifine</span> 👍（0） 💬（1）<div>老师，有空麻烦回一下，我网上找了好久关于 learner 的说明，包括官网，都没有相关操作的资料。
问题是这样：
我们有 A和B两个区，A 部署3个节点的集群，B区使用一个 learner 做灾备，请问如果A区全部故障了，我这个 learner 该怎么操作？

我针对 learner 操作一直提示 rpc not supported for learner 错误：

ETCDCTL_API=3 .&#47;etcdctl --endpoints=172.168.111.129:62379 member promote ebcec9c01f280618       
{&quot;level&quot;:&quot;warn&quot;,&quot;ts&quot;:&quot;2022-08-25T14:31:06.673+0800&quot;,&quot;caller&quot;:&quot;clientv3&#47;retry_interceptor.go:62&quot;,&quot;msg&quot;:&quot;retrying of unary invoker failed&quot;,&quot;target&quot;:&quot;endpoint:&#47;&#47;client-3c29945a-de04-4bec-9ad3-48c50f3fd135&#47;172.168.111.129:62379&quot;,&quot;attempt&quot;:0,&quot;error&quot;:&quot;rpc error: code = Unavailable desc = etcdserver: rpc not supported for learner&quot;}
Error: etcdserver: rpc not supported for learner</div>2022-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e3/48/510fd23d.jpg" width="30px"><span>hifine</span> 👍（0） 💬（0）<div>老师好，请问A和B跨区，B区部署learner, A区故障时，learner该如何操作，网上资料太少了，搜边了都没找到，我操作learner一直提示 rpc not supported for learner</div>2022-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ca/79/139615aa.jpg" width="30px"><span>Magic Star Trace</span> 👍（0） 💬（0）<div>我们线上 etcd  是用虚拟机部署的，没有在k8s集群内 能否将error级别的日志 重定向到其他目录呢？</div>2021-03-29</li><br/>
</ul>