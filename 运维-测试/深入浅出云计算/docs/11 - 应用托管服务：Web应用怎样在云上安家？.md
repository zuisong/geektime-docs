你好，我是何恺铎。今天我们来谈谈云上的应用托管服务。

从互联网诞生开始，网站就一直是人接触内容的主要窗口，是互联网应用的主要形态。所以许多的编程语言和技术栈在争夺开发者的时候，都是以支持网站应用的开发作为主要的发力点。

这个浪潮催生了各类动态网站编程技术，和各种Web后端框架的兴起。而随着AJAX应用和移动互联网的到来，Web已经不只是网站了，它还包括各种各样的API。我们可以把它们统称为Web应用。

Web应用，显然是一个极为普遍的需求，也是一个巨大的市场。所以，作为承载一切的云计算，当然需要为Web应用的运行提供最好的场所、能力和辅助。

不过，你当然也可以使用虚拟机和其他IaaS组件来搭建你的网站。但用IaaS，你需要操心的事情比较多，包括虚拟机的创建、运行环境的搭建和依赖安装、高可用性和水平扩展的架构等等。而且一旦应用的规模大了，每次应用的更新升级也会是件麻烦事，另外你还要操心Web漏洞的弥补修复。

**那么，能不能有一个平台服务，来帮助我们解决所有这些基础架构问题，让我们只需要专注于应用构建本身就好了呢？**当然是有的，这就是云上应用托管PaaS服务的由来。

## 什么是应用托管服务？

和每一项云服务一样，应用托管类服务也是从简单到复杂、从功能单一到丰富强大这样一路走来的。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/70/35/28758547.jpg" width="30px"><span>何恺铎</span> 👍（18） 💬（0）<div>[上讲问题参考回答] 
1. 如果要临时对外分享对象，一般对象存储都有一个生成临时链接的功能。它会通过签名生成相关token（token会附着在生成的url中），并允许你设置一个过期时间，到期以后这个链接会立刻失效。你要保存好这个私密的url，发送给你授权的用户来使用。
2. 关于大数据量上传云端，不少同学都提到了并发上传、压缩上传等最佳实践，但这些无法突破网络带宽的瓶颈。为了解决上传速度慢的问题，云厂商其实都提供了离线数据上传的服务，比如AWS Snowball、Azure Data Box、阿里云闪电立方等。这些服务通过和专用的物理存储设备配合，能实现PB级数据的迁移，俗称“寄硬盘”。</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a4/49/1c8598d1.jpg" width="30px"><span>军舰</span> 👍（16） 💬（1）<div>问题二：应用托管服务将运行环境与应用进行了分离，只需要发布应用，让应用部署更轻量化；容器解决了应用部署对运行环境依赖的一致性问题，运行环境和应用打包在一起。应用托管服务往往解决的是一种单一运行环境的需求，对于需要定制化和多运行环境的依赖就不适合了，容器很好的解决了这个问题，运行环境和应用的适配在开发的时候已经解决了，部署后开箱即用。</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6d/ea/2c5fcdb1.jpg" width="30px"><span>睡觉也在笑</span> 👍（6） 💬（2）<div>老师，我是银行科技人员。因为行业的原因一般不会选用公有云的产品，您知道那些私有云产品也支持这么完备的云服务吗？我们也想交流和了解一下。</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/71/ed/45ab9f03.jpg" width="30px"><span>八哥</span> 👍（3） 💬（1）<div>Beanstalk技术上类似Google App Engine吗？paas环境最大弊端就是不支持文件写到本地磁盘，只有临时磁盘，导致应用迁移过来，要修改代码。</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（0） 💬（1）<div>这个其实就让我想到了阿里的POLARDB和OceanBase：集群建好了，基本监控搭建好了；你只需要用就行，给你个接口去导入\导出数据，不过因此不少深层的分析就需要付费。
Docker其实最大的便利之处在于多应用的隔离：企业的各组织之间更新代码的速度不同；Docker便于彼此之间隔离使得服务器上安装的应用不那么乱且便于管理。
谢谢老师今天的分享：期待后续的课程。</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f2/70/8159901c.jpg" width="30px"><span>David Mao</span> 👍（1） 💬（0）<div>老师，最近在做IaaS的技术选型，私有云部分有腾讯云Tstack, Ucloud, 华三，Dell,前两者是openstack,后两者是VMware,从技术角度，老师倾向于哪个？谢谢</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/c4/4ee2968a.jpg" width="30px"><span>艾利特-G</span> 👍（0） 💬（0）<div>公有云之间应用托管服务的配置应该都有区别，我想容器服务也会有区别，用惯了一家再用另一家，还得熟悉下，虽然应该也是大同小异。
容器服务下，提交的artifacts是容器，运行时没有编程语言限制，只有一个通用的容器运行时，而应用服务还有编程语言运行时的种类。早期的容器其实也没有解决跨语言应用的配置不同的问题，Docker公司解决了容器统一打包这个问题。</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/14/99/5b1ed92b.jpg" width="30px"><span>戴斌</span> 👍（0） 💬（0）<div>期待更新</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d0/51/f1c9ae2d.jpg" width="30px"><span>Sports</span> 👍（0） 💬（0）<div>阿里云貌似应用托管服务这一块功能做的没有azure和aws多啊</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/4e/be2b206b.jpg" width="30px"><span>吴小智</span> 👍（0） 💬（2）<div>根绝托管服务，比较适合与前端页面的托管。如果系统比较复杂，比如说需要用到数据库、消息队列等组件，这种方式还适合嘛？如何与其他系统交互呢？</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/22/e0/6295a753.jpg" width="30px"><span>Harvey</span> 👍（0） 💬（0）<div>1 我猜是用来支持持续交付各阶段不同环境部署的需求
2 解决环境一致问题</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/25/66/4835d92e.jpg" width="30px"><span>潘政宇</span> 👍（0） 💬（0）<div>不错的服务</div>2020-03-27</li><br/>
</ul>