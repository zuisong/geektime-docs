你好，我是葛俊。今天，我将与你分享优化流程中，代码入库前的开发流程。

代码入库之前的开发活动，主要包括编码、调测调优、静态检查、自动化测试、代码审查等。这是开发者编写代码的步骤，自然是提高研发效能的关键环节。

![](https://static001.geekbang.org/resource/image/44/28/44e048f968b603e49136b10f5dbdf728.png?wh=2475%2A525)

图1 本地开发流水线

提高开发者编写代码的效能，关键在于让开发者不受阻塞、不受不必要的干扰，从而全身心地聚焦在产品开发上。我把这种不受阻塞的开发状态叫作**持续开发**。

一个团队如果能够做到持续开发，那么它的有效产出自然会很好。而对于个人开发者而言，持续开发能够帮助我们把精力集中在技术本身，对技术和个人能力的提升都大有裨益，所以是一种很好的开发体验。

在我看来，持续开发的基本原则主要包括两条：

1. 规范化、自动化核心步骤；
2. 快速反馈，增量开发。

接下来，我们就一起看看这两条核心原则吧。

## 规范化、自动化核心步骤

要让开发者聚焦于开发，就必须把研发流程中可以自动化的步骤尽量自动化。因为一般不可能完成所有步骤的自动化，所以我推荐的方式是：分析关键路径上的活动，以及耗时较长的活动，然后投入精力优化这些步骤。

首先，我们需要明确具体的开发步骤有哪些。我将其归纳为以下三大步：

1. 获取开发环境，包括获取开发机器、配置环境、获取代码等。
2. 在本地开发机器上进行开发，包括本地的编码、调测、单元测试等。
3. 代码入库前，把改动提交到检查中心（比如Gerrit），再进行一轮系统检查，主要包括代码检查、单元测试、代码审查等，通过之后再入库。
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/c8/6af6d27e.jpg" width="30px"><span>Y024</span> 👍（14） 💬（1）<div>搭车推荐 IntelliJ 下的效率神器插件 JRebel，可以免手工重启，快速生效文件改动最新效果。
http:&#47;&#47;plugins.jetbrains.com&#47;plugin&#47;4441-jrebel-for-intellij</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（9） 💬（2）<div>1. 在开发环境方面，你有没有尝试过在 Docker 里面进行开发？你觉得这种方式的好处是什么，弊端又是什么呢？
在之前的项目中有用过Docker来搭建开发环境，主要是一些中间件，例如后端数据库，solr，elk等。带来的好处是每个开发人员可以很快在本地搭建一套开发环境，彼此不会有冲突，不好的地方是Docker文件和镜像的维护，需要额外的精力。


2. 有些开发者喜欢写好一个比较大的功能单元，然后再一口气调测。你觉得这样做的好处和坏处，各是什么呢？
这种做法的好处是写代码的时候可以更加专注，不好的地方是如果开发人员经验不够，这种方式就会变为调试驱动开发，反而会降低效率。
不同的人会有不同的开发方法，我认为并没有普适所有人的方法，对于经验非常丰富的开发人员来说，怎样做都会得心应手。想一想纸带编程时期，哪有什么单元测试。</div>2019-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b4/00/661fb98d.jpg" width="30px"><span>追忆似水年华</span> 👍（9） 💬（2）<div>我的开发方式可能比较另类，也比较不合规。公司买的是阿里云的 Windows 服务器，我现在常常都是直接通过远程桌面连接到服务器上，用 VSCode 开发前后端项目。前端用 Vue 全家桶，后端用 Node.js + nodemon，有改动之后立刻生效，最大的好处就是快，见效快 😂
之所以这样做，是因为我们公司就俩开发，一人负责一大摊子事，所以常常用各种野路子，怎么方便怎么来，哈哈。</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/52/bd/abb7bfe3.jpg" width="30px"><span>电线杆儿</span> 👍（5） 💬（1）<div>@在开发环境方面，你有没有尝试过在 Docker 里面进行开发？你觉得这种方式的好处是什么，弊端又是什么呢？
#好处：A节约开发资源（多个开发人员共用一台docker开发机器，基于容器的资源隔离，抽象成多个开发机，提高单台机器的使用率）B快速搭建（新来的开发同事可以迅速创建一套或多套开发环境，基于镜像的一致性，保证环境创建过程中不踩坑，节约项目融入时间，同时，如果环境遭到破坏，或开发机不可用，可以迅速迁移到其他docker开发机）C轻松构建（很多时候出了搭建开发环境，还要搭建构建环境，通过docker提供的各种工具镜像，可以实现轻松构建自己的代码）缺点：A资源控制（对于性能要求高的服务，docker开发环境不如独立开发机性能高，虽然使用cgroup技术，但是docker还是会占用部分资源，对于独立性要求高的开发不利） B镜像构建（从传统方式到docker开发，需要构建基础镜像，代码、日志要持久化出来，通过sftp与IDE实现实时保存更新，基础镜像如果不够灵活，使用中会遇到问题）C需要了解docker命令（对没接触过docker的有一定的学习成本，并且查看日志，和启动服务等操作会变得跟传统方式不同）D网络限制（docker默认采用bridge方式提供小二层网络，比较抽象，对于需要独立IP资源的服务不友好，当然可以更改网络模式，但是需要整个公司的网络支持）
@有些开发者喜欢写好一个比较大的功能单元，然后再一口气调测。你觉得这样做的好处和坏处，各是什么呢？
#好处A功能完整（这样一个功能可以根据项目需求周期来决定要不要该功能整体，如果较小的功能单元，后期可能会根据项目需求不断调整，经验不足就会对项目其他功能造成影响）坏处A需求见效慢（开发周期长，问题暴露滞后，不利于敏捷开发，可能会错过需求的最佳上线周期）B项目返工修复困难（单元大，设计的模块多，如果有BUG，修复起来很难）C不利于持续交付（如果要走持续交付路线，就要频繁上线，尽可能的优化上线流程，如果很久才开发一个功能并上线，即便有问题，也会觉得是个例）</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/3b/969eedf2.jpg" width="30px"><span>robincoin</span> 👍（4） 💬（1）<div>怎么用线上的数据给开发人员进行开发测试呢</div>2019-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（2） 💬（2）<div>监听文件变动并重启服务的事情我做过。

当时是用lua开发的一个项目，lua本身还是支持热更新的，不需要重启进程.

我就在代码逻辑中定时扫描文件的变动情况，有过变动且最近5秒未再变时就热更新加载代码。
（因为在网络传输文件的过程中，如果文件没传完，就开始了重载流程，就会出现语法错误。）

这样我用vim在服务器上开发时，只要一保存，就触发了重载。
另外我会单独开一个终端在tail日志，如果有问题，可以及时的发现。

从这也能看出，我喜欢小步走。</div>2019-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/09/f2/6ed195f4.jpg" width="30px"><span>于小咸</span> 👍（2） 💬（2）<div>如果工程比较大，编译需要很久的话，自动编译并重启服务是不是就不太合适了？</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（1） 💬（1）<div>发现解释性或者脚本型的语言做持续集成都比较方便，工具也多，但是像我们主要用C++的，好像没有这样的自动化工具链吧。老师对这个有经验或者建议吗？</div>2020-02-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Qp9dYsewprexf2zo45CPoZ4rmQTBzx8hxTzzeibduV7nichZV9CicgicPPHZ7ZsTlehiaAWqrQswcp3m9KUFkueej6Q/132" width="30px"><span>大河</span> 👍（1） 💬（1）<div>Docker开发对于前后端没有分离的项目来说，前端会省去大量的搭建项目的时间，直接使用后端搭建好的环境，然后去提交代码进行联调。</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/a2/e21abfee.jpg" width="30px"><span>Marco</span> 👍（1） 💬（3）<div>老师,有自动化的一套工具介绍吗?</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ad/95/2d248ac2.jpg" width="30px"><span>师傅又被抓走了</span> 👍（1） 💬（1）<div>采用虚拟机作为个人开发机------这个比较高效，值得学习！</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（1） 💬（2）<div>老师，数据那一块怎么管理呢，比如初始数据</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ba/bd/6f2f078c.jpg" width="30px"><span>Marvin</span> 👍（1） 💬（1）<div>1、使用docker对前端或者硬件需求较苛刻的开发不是很友好，好处是开发环境搭建迅速零维护。2、较大功能单元，不利于单元测试，不利于后期维护，不利于工作拆解，不利于发现问题，好处是功能相对集中，持续开发时间较长。</div>2019-09-02</li><br/><li><img src="" width="30px"><span>Geek_b43d27</span> 👍（0） 💬（1）<div>据说facebook有很多的外包测试人员啊。所以是不是还是有很多测试的？</div>2020-11-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLOMFSAg7ZEtwgdqTZMhjvdlOcRbHWTzDCBJMqdzpIqxQIRuE2aHianHHFibv1bGfAjnzmBpSJxx9MA/132" width="30px"><span>oliver</span> 👍（0） 💬（1）<div>采用docker作为个人开发机的话是否意思是在服务器上开一个docker？还是把docker模板文件拉下来到本机环境运行？
如果用docker开发。是否只能用vim，无法用idea之类的IDE了？</div>2020-04-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJOlibibPFEWOib8ib7RtfAtxND5FUqCxxoeTuLAbBI9ic23xuwdXT4IyiaWq3Fic9RgEAYI0lBTbEp2rcg/132" width="30px"><span>Jingxiao</span> 👍（5） 💬（0）<div>作者背景这么强，课这么好，只有这么点订阅真是可惜</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d7/43/3f5c39aa.jpg" width="30px"><span>Miracle</span> 👍（0） 💬（0）<div>我们一开始自己构建了一套虚拟机作为开发测试环境，内置各种辅助工具，并且可以提前拉好代码，配置好测试数据，效果非常好，但是虚拟机环境交付效率比较低，又升级到了docker，但是是一种胖容器，原生docker但做了扁平网络，自己做ip分配，开发基本感知不到自己用的是容器，还是ssh连接的。所有开发，测试，自动化测试都用这一套，效率直接起飞。和老师这套理论不谋而合。
但问题是，生产环境需要独立容器部署，容易出现环境不一致。</div>2024-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/70/e7/82cd831d.jpg" width="30px"><span>Timothy</span> 👍（0） 💬（0）<div>老师分享很精彩，想顺便请问下，C++与Qt结合的技术栈下，有没什么推荐的自动化工具呢？</div>2024-02-24</li><br/><li><img src="" width="30px"><span>刘兆峰</span> 👍（0） 💬（0）<div>团队目前使用华为云的DevCloud平台，代码提交时可以做到对全量代码仓库进行自动化检查，但是我期望是仅对本次提交的代码做检查，是否有这样的工具支持</div>2022-07-30</li><br/><li><img src="" width="30px"><span>nate_luo</span> 👍（0） 💬（0）<div>1. 我是做嵌入式开发的，编译的时候是用docker的。因为交叉编译环境依赖比较多，很多库还必须指定版本，做成docker是会比较方便，但仅限于编译使用，mount文件夹过去。
2. 嵌入式开发做单元测试也比较麻烦，一来C的单元测试就不如其他语言容易，二来交叉编译后的可执行文件必须加到板子上才能跑，我想知道葛老师有什么建议？</div>2022-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/4d/2116c1a4.jpg" width="30px"><span>Bravery168</span> 👍（0） 💬（0）<div>各种工具和基础设施的建设和优化真是一个需要长期投入和持续的过程。不过要做好了，也能产生很大的收益，能够赋能业务研发团队提高效率，加快产出。</div>2021-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/82/40/02ae9409.jpg" width="30px"><span>Learner</span> 👍（0） 💬（0）<div>写好一个比较大的功能单元似乎没任何优点，就是给让Dev逃避小步提交，快速迭代，持续集成</div>2021-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9d/f0/6c34b90f.jpg" width="30px"><span>David</span> 👍（0） 💬（0）<div>👍</div>2019-10-18</li><br/>
</ul>