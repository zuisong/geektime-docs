你好，我是宝玉。这些年，有关DevOps的概念很火，大家都在讨论DevOps，有人说DevOps就是自动化运维，有人说DevOps是流程和管理，还有人说DevOps是一种文化。以前的运维工程师也纷纷变成了DevOps工程师。

今天，我将带你一起了解一下，究竟什么是DevOps？DevOps到底要做什么事情？

## 传统的运维模式以及面临的挑战

在传统的瀑布模型开发中，软件生命周期中的运行维护这部分工作通常是交给运维工程师来完成的。

当开发人员完成编码，测试人员测试验收通过后，到了要发布的时候，就会将程序交给运维人员部署发布到生产环境。

![](https://static001.geekbang.org/resource/image/2b/e0/2b3c01636b37728e5684d9bbc5e383e0.png?wh=1200%2A400)  
（图片来源：[The Product Managers’ Guide to Continuous Delivery and DevOps](http://www.mindtheproduct.com/2016/02/what-the-hell-are-ci-cd-and-devops-a-cheatsheet-for-the-rest-of-us/)）

除了程序的部署更新，传统运维工程师最重要的职责就是保障线上服务的稳定运行。对服务器24小时监控，有意外情况发生时需要及时处理和解决。

除此之外，还有日常的更新维护，比如说安装升级操作系统、安装更新应用软件，更新数据库、配置文件等。

早些年这种运维模式运行的很好，但随着这些年互联网发展，有两个主要的因素对传统的运维模式产生了很大挑战。

第一，服务器规模快速增长和虚拟化技术的高速发展。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/57/aa/d6dc3632.jpg" width="30px"><span>林云</span> 👍（13） 💬（1）<div>需要指出“Devops工程师”是一个概念错误。事实上Devops并不是一个职位，如果按照文中所说：“Devops工程师帮助团队搭建CI&#47;CD工具”则应该叫做持续交付工具架构师，而这与文首所说：“运维工程师纷纷改名Devops工程师”在工程师的技术栈领域互相矛盾，难道所有持续交付系统都是由运维工程师搭建的吗？

而《Devops实施手册》提出了DevOps能力中心的核心角色其中包括：协调资源的项目经理；推动工具方案实施与评价结果的执行经理；交付DevOps平台的基础架构经理；DevOps教练和技术布道者。由这些角色配合才能完成传统企业Devops的全面转型。
即使是初创企业推行Devops也不是只有一个工具链工程师可以完成的。

参考连接：https:&#47;&#47;www.jianshu.com&#47;p&#47;7cf36451ee83?from=groupmessage</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/53/5d/46d369e5.jpg" width="30px"><span>yellowcloud</span> 👍（6） 💬（1）<div>前面听老师介绍了很多自动化测试的方法、工具以及现在的devOps，听到这些可以快速提高生产效率的方法，使我有点跃跃欲试了。宝玉老师能不能介绍一整套可以简易部署使用的devOps的工具，方便小公司快速部署、实现，在实践中感受devOps的魅力。</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/57/aa/d6dc3632.jpg" width="30px"><span>林云</span> 👍（5） 💬（1）<div>如果标题改成“Devops这样实施就对了”也许会好些。这样至少不会混淆所有Devops实施的工作只需要一个角色就能完成。（招聘岗位title写着Devops工程师？一定是一个不懂Devops的HR所为）

就像文中提到的“道 法 术”概念，首先有定义，然后根据定义建立体系，而不是使用有争议的词汇，让读者对论述产生误解。

就像软件工程通过一套方法使得软件交付可预期，Devops如何实施也是一套严谨的知识体系，有不同的分工和角色。只有用严谨的方法才能得到可预期的结果。</div>2019-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/60/f5439f04.jpg" width="30px"><span>Geek_dn82ci</span> 👍（3） 💬（1）<div>我个人觉得devops是个很大的概念，理论上开看更侧重的是一种协作方式，也就是想法先行，单从目前的IT业态发展趋势来看，devops下面包含了很多学科，与基础设施相关的云计算，容器化，自动化运维监控等，与软件工程相关的敏捷开发，CI&#47;CD，微服务等，以及与组织架构相关的诸如SRE这种角色的导入还有OKR考核方式等</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/10/b6bf3c3c.jpg" width="30px"><span>纯洁的憎恶</span> 👍（3） 💬（1）<div>传统运维工作：程序部署到生产环境、保障服务器稳定运行、日常更新维护（操作系统、应用软件、数据库、配置文件）。

变化：服务器规模与日俱增，因此带来的自动化运维计划的普遍应用；生产环境程序部署的频率更高，高频部署与系统稳定的冲突助长引发运与开发的职能壁垒。

运维人员的新要求：应用大量自动化运维技术，具备搭建自动化运维工具或功能的能力，更多的了解、参与、引导开发环节工作。

DevOps的道：开发与运维紧密协作的工作方式，以更快更可靠的构建、测试、发布软件。

DevOps的术：通过软件技术打通开发与运维环节的信息壁垒，提高软件工程全过程自动化水平，固化、引导跨职能协作文化，提升整体效能。

本公司有多个外包团队，每个规模都比较小，所以往往几个人同时负责产品、测试、运维的工作，没有明确的分工反而挺高效。规模较大的公司由于管理的项目更负责、人员也更多样，所以岗位上区分的比较明确，也有利于专注本职工作。但这也在一定程度上助长了岗位壁垒，需要强调跨职能协作的工作方式与手段。“分分合合”的过程中，效率是不变的追求。</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/c2/e9fa4cf6.jpg" width="30px"><span>Charles</span> 👍（3） 💬（1）<div>曾经部门里有一个运维工程师觉得工作不饱和，成就感不强，一个是因为业务一直上不去规模，还有一个是他自己也有一点焦虑，觉得基础的运维越来越被云计算厂商给做完了，所以他就想到自己开发一点日志监控和预警、甚至应用程序的性能追踪和异常发现，今天看到老师的文章，发现这种发现问题解决问题方式在实践devops的方式好像也挺好的，并且更容易落地</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/04/ec/0539c89d.jpg" width="30px"><span>易林林</span> 👍（3） 💬（1）<div>对于Devops我只是听说过，并没有具体的去了解过它的使用和应用场景。根据宝玉老师的讲述，Devops 的基础是自动化，那么自动化之外好像更多的是一种概念，可以因环境而产生各种不同的方式和方法，并没有比较明确的定论。感觉就像敏捷开发一样，满足敏捷宣言思想的操作都可以是敏捷开发，最终适合自己或团队的才是最好的。</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（2） 💬（1）<div>搭建自动化测试，自动化部署，自动化监控系统，都自动化了，开发都做了，是不是就不需要运维和测试了.......</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（1） 💬（1）<div>1、有什么软件企业不适用于DevOps 吗？比如嵌入式软件产品？2、有没有一套比较成熟拿来可用的DevOps 产品，比如Tomcat+mysql+git的？3、现在有DevTestOps概念，DevOps 与DevTestOps区别在哪儿？</div>2019-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9b/a7/440aff07.jpg" width="30px"><span>风翱</span> 👍（1） 💬（1）<div>确实说出了目前我们团队中的痛点，不同岗位人员之间的不理解。 不同岗位工作内容的渗透，跨职能协作，是可以融入我们的团队中的方法。当然这个不是能一步促成的事，需要一步一步走。</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/25/c4cc1e9f.jpg" width="30px"><span>巫山老妖</span> 👍（0） 💬（1）<div>关于这一节的内容，我最大的感受就是不仅仅只是运维工程师需要学习DevOps，而是所有开发都应该学习DevOps，开发和运维本身就分不开，构建协作的文化，提升研发效能，不管对产品还是团队都是非常好的实践</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>DevOps 的主要原则就是自动化、信息透明可测量、构建协作文化。--记下来</div>2022-07-06</li><br/>
</ul>