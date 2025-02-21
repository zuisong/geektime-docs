你好，我是何恺铎。

欢迎你来到我们《深入浅出云计算》课程的第9讲，这也是我们PaaS篇的第1讲。让我们继续精彩的云计算之旅。

PaaS，对你来说也许不是一个陌生的词汇，你可能早已从业界大咖或身边同事的高谈阔论中屡次听到这个字眼。不过，很多人对于PaaS服务的评价，可是既有“真香快来”的赞赏，也不乏“大坑勿入”的批评，面对如此两极分化的评价，你估计也有点拿不定主意。这些如雷贯耳的PaaS服务们，究竟靠不靠谱、好不好用呢？

作为极客时间的一名“极客”，咱们人云亦云可不行，必须要建立起对PaaS的系统认知。从今天开始，我们就来好好地研究一下PaaS。

让我们先从它的定义说起。

## 什么是PaaS？

在IaaS篇中，我们主要是侧重于基础设施类的云服务，尤其是虚拟机、云磁盘、云网络等服务。它们的特点是，和传统IT基础设施往往有一个对应关系，所以被称为基础设施即服务（Infrastructure-as-a-Service）。

今天我们的主角**PaaS** （Platform-as-a-Service），则是指云计算提供的平台类服务，在这些平台的基础上，用户可以直接开发、运行、管理应用程序，而无需构建和维护底层的基础设施。

用更通俗的话来说，**PaaS是在IaaS的基础上又做了许多工作，构建了很多关键抽象和可复用的单元，让我们用户能够在更上层进行应用的构建，把更多精力放在业务逻辑上。**
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/70/35/28758547.jpg" width="30px"><span>何恺铎</span> 👍（13） 💬（0）<div>[上讲问题参考回答] 
1. “Cloud Shell”是云厂商为你提供的Shell交互环境（通常是免费的），默认安装了官方的CLI工具。你可以直接在上面很方便地执行云资源管理等脚本操作，免去了自己安装维护一个虚拟机的麻烦。
2. 资源组是用来管理账户中各类云资源的一个逻辑上的集合。它有两个特点，一是能够囊括各种不同类型的资源，二是一个资源只能属于一个资源组。一般可以用资源组来表达和标记整个系统中具备一定规模的“模块”或“组件”，以便你对账户中的资源进行分类管理和成本归属的计算。</div>2020-03-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（13） 💬（2）<div>这个问题答不上来了，因为公司业务的限制导致我们没有使用公有云的任何paas相关服务，我们的业务是出包到客户场内由交付工程师去部署，都是一些对客户极其敏感的客户，所以暂时用不上公有云。

但是我能说一下我们没用paas的极低的效率～ 
我们的产品是基于k8s的，日志服务、监控服务、kafka服务，es服务，数据库服务.....当然也包括底层k8s的运维，都是我能搞，这还不是重点，重点是每次有人申请一套环境，我们还有从创建虚拟机到部署出产品给他们整出一套来，这就有了n套环境，每个环境出了问题都要我们解决，最多的时候一周有一半的时间花在这个上面，周报都不知道咋写～

如果把数据库、监控、k8s这些让运营商提供，一是可靠性有了保障，二是使用更加方便了，不用自己部署相关服务，简单配置即可～</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/82/34/c47ccbeb.jpg" width="30px"><span>mrtwenty</span> 👍（10） 💬（1）<div>用过阿里云的oss，rds、高防、web防火墙，
1、oss 文件独立存储、可以加cdn，节省ecs的带宽，独立存储，安全、负载均衡也不用考虑图片单独存储，几乎无限的空间，不用考虑很多的问题
2、rds数据库，由于公司没有专业的dba，数据库维护，直接交给了阿里云，升级硬件配置也非常方便，兼容原生的mysql ，很好，就是价格有点贵
3、web防火墙，高防这些，只能交给专业的第三方或者阿里云，自己实现 ，几乎不可能，根本扛不住流量的冲击。
</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（5） 💬（1）<div>PaaS其实对于某个领域研究颇深的技术从业者：个人DB领域多年，接手的就是云厂商的RDB，初期操作策略相对简单还好；中后期2.0架构设计就发现对比实际需求在存储引擎、版本、读写分离、性能参数调整方面操作空间蛮有限的。
就像课程中的例子：装修好的房子你直接可以用，但是你发现装修中的许多不合理性你就没办法调整；无法对于数据系统做到真正的扬长避短；尤其当系统越来越大需要各种特性化优化时，根本发挥不出其真正的版本优势所在。厂商的PaaS的架构或内核版本其实相对于主流市场要晚5-10年。
有力使不上这大概是对于专业人员接触此类系统最大的感觉。
谢谢老师今天的分享：期待后续的课程。</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ae/b5/df9e0b81.jpg" width="30px"><span>开心果源～老余</span> 👍（3） 💬（2）<div>希望老师说说PaaS涵盖微服务，容器，devops等服务，PaaS到底还能承载什么应用，讲得太泛泛了。</div>2020-03-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLIuRQaZX70dsBg6khub2VPM1eQAP9IWRWxgOFed3ia4kXyNJInFRicWJ0ibf2YmLsOvJa1sGygGpmJg/132" width="30px"><span>胖子</span> 👍（3） 💬（1）<div>＂如果没有内含的运行环境，那就说明这个 PaaS 属于“开箱即用”的工具类型，也就是直接依靠自身内置功能来向你提供支持或帮助。这时它功能的完善程度，以及和你需求的匹配程度，就比较关键了。＂，这段话不好理解，请问那些场景适用内含运行环境哪些场景适用不含运行环境？</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e8/6d/17e307c0.jpg" width="30px"><span>Yuri</span> 👍（3） 💬（1）<div>之前项目上使用到了MongoDB，然后上云的时候选择了aws号称兼容MongoDB的DocumentDB，然后应用上去跑的时候就各种报错，太坑了，后来只能自己搭建MongoDB了。</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/f3/fc992148.jpg" width="30px"><span>kitsdk</span> 👍（1） 💬（0）<div>不知所云，用张磊大神的话说：经典paas是应用托管服务。</div>2022-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/c6/d8948c7c.jpg" width="30px"><span>lennonHe</span> 👍（1） 💬（0）<div>PaaS 本身也是基于底层 IaaS 构建出来的，使用了云上的各种基础设施。只是这个步骤云服务提供商代替我们用户完成了，还进行了一定程度的封装。

这个部分有点疑问，请教下老师。逻辑上，PaaS本身是基于底层IaaS层构建出来的，但是在实际应用中是否PaaS的服务都是基于IaaS虚拟化出来的资源进行搭建？

目前了解到的，很多情况下大数据服务为了性能考虑，都是直接基于裸机进行部署的，然后通过云管理平台向用户提供服务。这种情况下怎么理解PaaS是基于IaaS进行构建的？</div>2021-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3f/0d/1e8dbb2c.jpg" width="30px"><span>怀揣梦想的学渣</span> 👍（0） 💬（0）<div>我对paas的理解就是自动炒菜的锅。
iaas是需要自己搭建灶台调试锅炉。锅出问题要自己修。锅的功能要自己设置配置。
paas的贴了标签的锅，有专人去维护，上面写着炒鸡肉专用，我按照许可指南投入自己的材料，就能给我炒好的鸡肉。锅的损耗我不关心，烂了就选下一个，我不需要养护炒锅。</div>2023-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8e/10/10092bb1.jpg" width="30px"><span>Luke</span> 👍（0） 💬（0）<div>主要使用了NAS和OSS，这两个倒没有什么自由度的问题，效率和安全性上很好。如果自己部署开源的方案，确实挺麻烦的，还有数据同步等等都需要考虑。</div>2022-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（0） 💬（0）<div>不知道阿里云的日志服务算不算是PaaS.
最近在研究阿里云的k8s,勾选了日志服务后,会自动创建相关的日志.
可以在上面看到很多个人的操作记录, 以及Ingress的日志.
目前还只是初步接触,需要慢慢学习怎么用.

但是感觉默认的配置很强大, 比起自己在es中创建规则, 要方便的太多太多.
也可以看看别人能玩到什么地步.

目前来看,除了费钱,没什么不好的.(目前来看,这个日志费用也非常低)
</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/14/99/5b1ed92b.jpg" width="30px"><span>戴斌</span> 👍（0） 💬（0）<div>NAS、OSS等存储还是提升了效率的</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/73/08/dd9a4a38.jpg" width="30px"><span>小狼</span> 👍（0） 💬（0）<div>腾讯的RDS 阿里的日志服务和redis。</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（0）<div>使用最多的PaaS服务当然是数据库了RDS</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d0/51/f1c9ae2d.jpg" width="30px"><span>Sports</span> 👍（0） 💬（0）<div>目前接触的是基于k8s搭建的一个paas平台，一套部署应用的脚手架，部署应用相对来说要方便一点，缺点就是一些部署选项太多，不太了解k8s可能不太理解，需要一定的学习成本</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f6/8e/c9c94420.jpg" width="30px"><span>俊釆</span> 👍（0） 💬（0）<div>目前接触最多的是k8s，对其中的网络访问配置和认证权限配置比较头疼。</div>2020-03-23</li><br/>
</ul>