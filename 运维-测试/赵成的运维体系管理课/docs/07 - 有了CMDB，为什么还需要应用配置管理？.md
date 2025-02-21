今天我们分享的主题是：有了CMDB，为什么还需要应用配置管理？

你不妨先停下来，思考一下这个问题。

我抛出的观点是： **CMDB是面向资源的管理，应用配置是面向应用的管理**。

请注意，这里是面向“资源”，不是面向“资产”，资源 ≠资产。

## CMDB是面向资源的管理，是运维的基石

我们一起来梳理一下，在建设运维的基础管理平台时通常要做的事情。

- **第1步**，把服务器、网络、IDC、机柜、存储、配件等这几大维度先定下来；
- **第2步**，把这些硬件的属性确定下来，比如服务器就会有SN序列号、IP地址、厂商、硬件配置（如CPU、内存、硬盘、网卡、PCIE、BIOS）、维保信息等等；网络设备如交换机也会有厂商、型号、带宽等等；
- **第3步**，梳理以上信息之间的关联关系，或者叫拓扑关系。比如服务器所在机柜，虚拟机所在的宿主机、机柜所在IDC等简单关系；复杂一点就会有核心交换机、汇聚交换机、接入交换机以及机柜和服务器之间的级联关系；
- **第3.5步**，在上面信息的梳理过程中肯定就会遇到一些规划问题，比如，IP地址段的规划，哪个网段用于DB，哪个网段用于大数据、哪个网段用于业务应用等等，再比如同步要做的还有哪些机柜用于做虚拟化宿主机、哪些机柜只放DB机器等。

以上信息梳理清楚，通过ER建模工具进行数据建模，再将以上的信息固化到DB中，一个资源层面的信息管理平台就基本成型了。

但是，**信息固化不是目的，也没有价值，只有信息动态流转起来才有价值**（跟货币一样）。接下来我们可以做的事情：

- **第4步**，基于这些信息进行流程规范的建设，比如服务器的上线、下线、维修、装机等流程。同时，流程过程中状态的变更要同步管理起来；
- **第5步**，拓扑关系的可视化和动态展示，比如交换机与服务器之间的级联关系、状态（正常or故障）的展示等，这样可以很直观地关注到资源节点的状态。

至此，从资源维度的信息梳理，以及基于这些信息的平台和流程规范建设就算是基本成型了。这个时候，以服务器简单示例，我们的视角是下面这样的：  
￼￼
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/eb/14/b6929253.jpg" width="30px"><span>foxracle</span> 👍（4） 💬（1）<div>对于公有云的CMDB的建设，总感觉是重复建设，动力不是那么足，只是说考虑到今后混合云的可能，做一层抽象层来解耦。公有云的CMDB的构建有什么特别的地方么？</div>2018-01-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoib2DhicgRJicgJplnlXjAEwXDBvAvcYkBS1MQQVgL84mrgrvEtH58uU2cicpxbbIQ9qhD6VM2plXYWA/132" width="30px"><span>gaofubin</span> 👍（3） 💬（3）<div>赵老师您好，我想构建cmdb，可是目前的基础资源都是Kubernetes平台，我得怎么把应用和基础资源关联起来呢？请您能提供个想法，多谢</div>2020-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/86/fb/4add1a52.jpg" width="30px"><span>兵戈</span> 👍（3） 💬（1）<div>请教赵老师，CMDB和应用配置管理也是持续集成和发布系统的基石，但如果现状是没有应用配置管理，该如何做好持续发布系统？对于持续发布这一块您有什么好的实践吗？</div>2018-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/99/4f5857a8.jpg" width="30px"><span>竹影</span> 👍（0） 💬（3）<div>读了前面几篇文章后回顾了自己的工作经历，包含应用信息的cmdb也尝试做过，最后公司没有继续投入资源。这个东西真的很重要，梳理清楚记录在册，变更登记，会给工作带来很多方便。问题是要投入多少时间和资源做这个事比较经济呢？</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/e9/1f95e422.jpg" width="30px"><span>杨陆伟</span> 👍（0） 💬（1）<div>老师的思路很开阔，方案很大，请问下在老师的公司实现了吗？</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d2/3b/85338316.jpg" width="30px"><span>可爱(๑• . •๑)</span> 👍（5） 💬（1）<div>推荐文章：
https:&#47;&#47;www.processon.com&#47;view&#47;link&#47;5829a24be4b00c4fc8a221b1?pw=51reboot#map


https:&#47;&#47;mp.weixin.qq.com&#47;s?src=11&amp;timestamp=1627880171&amp;ver=3227&amp;signature=OL2etre4VppMqag1jn1V6vup74DvOcIvjaQ*e7t1SCIM6gKrt5OhY1NAgRvTU6LFul7YEwd80WrIdr6nenXYJae6EvbQArR1B-4B4GZJqmhznpMjx*PH5zarLdVFQsS7&amp;new=1</div>2021-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3f/0d/1e8dbb2c.jpg" width="30px"><span>怀揣梦想的学渣</span> 👍（1） 💬（0）<div>看了本文，对资源梳理有疑惑，是按照个人经验去梳理资源的属性，还是业界有标准可以参考的总分类，或者公司领导关注哪些，我就统计哪些。</div>2022-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/74/ea/10661bdc.jpg" width="30px"><span>kevinsu</span> 👍（0） 💬（0）<div>老哥，运维降低成本有啥好的思路吗？</div>2023-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e3/8a/ed8d1b63.jpg" width="30px"><span>梧桐秋雨</span> 👍（0） 💬（0）<div>主机列表对应的应该是上流量IP（一般是VIP），但针对整个集群模型，包括L4、L7、Real构建起来的模型，要如何管理呢？如何才能做到，相关的IP有问题时，或者全网分布式的集群上线时，可快速剔除故障机或快速上线。</div>2021-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（0） 💬（0）<div>CMDB 是面向资源的管理，应用配置是面向应用的管理。
言简意赅！在微服务体系下，更应该加强应用配置的管理。</div>2020-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/03/8d/38a98dc6.jpg" width="30px"><span>牧野静风</span> 👍（0） 💬（0）<div>看了几个开源的CMDB，做的很是粗糙，听了赵老师一番话，觉得确实梳理的比较透彻，现在这些信息我都是用EXECL管理，太离散了</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/74/ea/10661bdc.jpg" width="30px"><span>kevinsu</span> 👍（0） 💬（0）<div>太棒了，听君一席话 胜读十年书</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a4/39/6a5cd1d8.jpg" width="30px"><span>sotey</span> 👍（0） 💬（0）<div>后悔没有第一时间来追老师的剧，老师写完专栏才来。读了前面几篇就已经如获至宝了，多年的运维积累感觉可以有可能被串起来抽象化平台化了。按耐住一口气读完的冲动，细细品味反复实施。</div>2018-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/29/12/8fa97b5b.jpg" width="30px"><span>昨夜东风吹南山</span> 👍（0） 💬（0）<div>请教下赵老师，有开源的同时支持资源配置和应用配置的cmdb开源软件吗？</div>2018-06-02</li><br/>
</ul>