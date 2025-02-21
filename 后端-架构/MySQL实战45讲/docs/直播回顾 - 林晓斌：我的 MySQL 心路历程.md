在专栏上线后的11月21日，我来到极客时间做了一场直播，主题就是“我的MySQL心路历程”。今天，我特意将这个直播的回顾文章，放在了专栏下面，希望你可以从我这些年和MySQL打交道的经历中，找到对你有所帮助的点。

这里，我先和你说一下，在这个直播中，我主要分享的内容：

1. 我和MySQL打交道的经历；
2. 你为什么要了解数据库原理；
3. 我建议的MySQL学习路径；
4. DBA的修炼之道。

# 我的经历

## 以丰富的经历进入百度

我是福州大学毕业的，据我了解，那时候我们学校的应届生很难直接进入百度，都要考到浙江大学读个研究生才行。没想到的是，我投递了简历后居然进了面试。

入职以后，我跑去问当时的面试官，为什么我的简历可以通过筛选？他们说：“因为你的简历厚啊”。我在读书的时候，确实做了很多项目，也实习过不少公司，所以简历里面的经历就显得很丰富了。

在面试的时候，有个让我印象很深刻的事儿。面试官问我说，你有这么多实习经历，有没有什么比较好玩儿的事？我想了想答道，跟你说个数据量很大的事儿 ，在跟移动做日志分析的时候我碰到了几千万行的数据。他听完以后就笑了。

后来，我进了百度才知道，几千万行那都是小数据。

## 开始尝试看源码解决问题

加入百度后，我是在贴吧做后端程序，比如权限系统等等。其实很简单，就是写一个C语言程序，响应客户端请求，然后返回结果。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/e5/c9/36fdec8e.jpg" width="30px"><span>liuq</span> 👍（37） 💬（1）<div>看了您的心路历程，我丧失了最后的一丝幻想，人与人的差距太大了，我意识到再怎么努力也达不到您刚毕业时的水平</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cb/50/66d0bd7f.jpg" width="30px"><span>杰之7</span> 👍（27） 💬（1）<div>通过这一节的阅读老师的心路历程，给我的第一个感受是老师敢做，很多人包括我自己都是有退缩心理的，但阅读老师的文章，老师是勇往的在向前走。

阅读到后面，越来越能感受到老师文章讲述的计算机基础学科的重要性，这其中就会锻炼人的耐心和技术水准，在老师开发数据库做源码分析时，我想又何止C和C++呢。必定会涉及到计算机操作内存，文件等内容，还有其他一些内容等。

对老师给的多写SQL，尽量少用界面软件，我也非常认同，也是我们熟悉Mysql的必经之路，可以让我们对数据底层的东西建立起我们的感觉，图形界面用多了会让我们失去这项能力。

不敢奢望最后能走多远，能有老师带着学习成长就值得。


</div>2019-01-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIu1n1DhUGGKTjelrQaLYOSVK2rsFeia0G8ASTIftib5PTOx4pTqdnfwb0NiaEFGRgS661nINyZx9sUg/132" width="30px"><span>Zzz</span> 👍（17） 💬（4）<div>林老师，关于贴吧系统权限脏页刷新的那个例子，有个疑问：既然“MySQL 里面就只有我那一个 select 全表扫描的请求“，为什么会有脏页呢？本来我想的是不是系统崩溃后MySQL在通过redo log恢复，但是恢复不是应该发在MySQL重启后，为select语句提供服务之前吗，它们应该已经刷新到磁盘了。那脏页是哪来的呢？</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e3/2e/77ad18f4.jpg" width="30px"><span>滔滔</span> 👍（10） 💬（1）<div>老师，想问一个关于加锁的问题，在mysql中有很多种锁，比如意向锁，行锁，gap锁，页面锁等等，往往一条复杂的sql语句的执行过程中要加很多的锁，通常情况下，是否存在一个锁申请的队列，并发的事务都向这个队列中提出自己想加的锁的申请，然后引擎根据队列中的顺序依次加锁，还是说加锁过程是原子的一次完成的呢？比如说一个update语句走全表扫描，在rr隔离级别下，会对每一条记录加x锁以及gap锁，这些锁是一次性加上的吗？</div>2018-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/3b/a5fddd35.jpg" width="30px"><span>姚伟</span> 👍（8） 💬（1）<div>老师说的了解数据库原理就是要去读懂MySQL的源代码吗？</div>2018-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（3） 💬（1）<div>老师，我还想问下有没有教程和书教人从零开始实现一个数据库引擎，能够包含基本的数据库原理，我以后想从事分布式存储方面的工作，特别想能自己上手实现一个简易的引擎，但是能力不够，想找个教程</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b9/3b/7224f3b8.jpg" width="30px"><span>janey</span> 👍（2） 💬（3）<div>为什么没有测试怎么学MySQL？业务是MySQL紧耦合的，所以买了这门课，学到这一讲，有一些反复看了几遍，当时觉得懂了，再回头觉得需要分析的时候又忘了……主要接触不到实际的业务，测试时除非客户反馈，太关注单个sql的性能的话对测试效率是不可接受的。边矛盾边学习……</div>2019-03-02</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eptCuRBA5qaBLSeWiadmRtibDATwbTCGbaedich6E4krkBr52YDc8RtCibz8Dz69txWJlLhG3IYozpcJg/132" width="30px"><span>paul.yang</span> 👍（2） 💬（1）<div>老师问个问题，为什么写数据库用c或者c++,是其他语言gc的问题吗？</div>2019-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/59/a01a5ddd.jpg" width="30px"><span>ProgramGeek</span> 👍（2） 💬（1）<div>阅读丁奇老师的 MySQL 心路历程受益匪浅，那么2019 年第一个问题请教下丁奇老师，后续对 MySQL 2PC，3PC方面会做详细的讲解吗？在3PC场景中 MySQL 怎么保证数据的一致性？</div>2019-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/25/348b4d76.jpg" width="30px"><span>墨萧</span> 👍（2） 💬（2）<div>连接失败也不会重连，仍然用原来断掉的连接，所以就报错了。请问老师，怎么重连呢，我在连接url加上了&amp;autoReconnect=true ,好像不起作用啊
</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/40/e0df3b84.jpg" width="30px"><span>力挽狂澜爆炸输出的臭臭宁</span> 👍（1） 💬（1）<div>老师有没有数据库原理的书籍推荐？与MySQL、oracel无关，就是纯粹的讲数据库最基本的原理，不同的数据模型等</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a0/0f/a81993a7.jpg" width="30px"><span>lzw</span> 👍（0） 💬（1）<div>林老师，关于MySQL datetime，timestamp这两个类型的区别在网上能查到很多，但是实际使用的原则却不清楚，能不能帮我解答下到底什么时候适合用哪个类型？</div>2019-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/78/00/31a6dd80.jpg" width="30px"><span>StarkYanng</span> 👍（0） 💬（1）<div>老师您好，看了您的心路历程，有个关于MySQL高可用架构的问题想问下您。比如最简单的主从拓扑结构，您提到了有自动化系统，那这些系统都是各个公司内部自己开发的么？有无开源。因为我的毕设是关于这方面的，谢谢！</div>2019-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/a7/674c1864.jpg" width="30px"><span>William</span> 👍（0） 💬（1）<div>老师的专栏讲的很棒，
对于我个来说也不是一次就能吃透的. 
个人计划：都跟着进度看一遍之后，再重复去学习.





</div>2018-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（0） 💬（1）<div>老师，问下后面会不会讲mysql集群和分库分表的知识</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（0） 💬（1）<div>为什么要了解数据库原理？原因适用与绝大多数技术，比如为什么要了解spring,mybatis,hadoop,spark,redis,zk.....原理？</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5c/f4/88f107d9.jpg" width="30px"><span>令狐少侠</span> 👍（0） 💬（1）<div>老师，后面有关于mysql函数方面的吗？如果没有，可以说说吗</div>2018-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4d/42/8fd7c2e2.jpg" width="30px"><span>朋朋</span> 👍（0） 💬（3）<div>谢谢老师分享， 我听别人说想学mysql 买了那本书 结果吃灰 中间因为索引问题曾经翻开看过 工作中都用序列化 redis key-value啦。不过看了你的专栏 还是很喜欢的。我有一个问题 对业务的理解 如果给你一个业务场景让你合理建立数据库表的能力 如果锻炼呢？ 因为我实际工作中还是用key-value多 但是提升一下场景建表的能力。</div>2018-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/dd/6e/f3cfebc5.jpg" width="30px"><span>峰哥</span> 👍（0） 💬（1）<div>希望老师能不时的提供些好用的工具或者sql，自己写太难了:(</div>2018-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/41/b868f086.jpg" width="30px"><span>小确幸</span> 👍（131） 💬（0）<div>专栏跟到现在，发现老师真的很负责，每篇的很多评论都认真回复。

昨天回顾了去年2月份老大分享的数据库方面的内容，当时一脸懵逼的内容，现在看了一遍，无压力了 感觉超级棒~

我是软件工程师，平时工作用的是sql server。虽然和mysql不同，不过底层原理都是类似的。最大的收获是老师说的方法论和数据库的原理（以前只知道how，不会去追究why），当我们深入了解底层后，感觉大不同。

实迷途而未远，觉今是而昨非~

多谢老师~</div>2018-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f1/84/7d21bd9e.jpg" width="30px"><span>Goal</span> 👍（53） 💬（0）<div>谢谢老师，让我体会到一个真正做技术人的态度，感谢</div>2018-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/25/f0/b70f7a87.jpg" width="30px"><span>极客007</span> 👍（31） 💬（0）<div>老师，我们公司原来一直用oracle，现在逐渐迁移到了postgresql，他们的底层实现和mysql有相似之处没</div>2018-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（15） 💬（0）<div>此篇不费脑费心，感谢老师的分享，成为技术大牛不是一朝一夕的事，拥有天赋的人会快一点没有天赋的人也有机会。练武不练功，到老一场空。基础很重要呀！没有内功只有招式，想成为高手几乎是不可能。基础是啥？在计算界，我觉得就是：
计算机组成原理
计算机操作系统原理
编译原理
计算机数据库原理
计算网络原理
算法及数据结构
这些如果能掌握的好，就好似张无忌练会了九阳神功，再学别的又快又好，否则他们总会在你前进的路上乱抛石头。
我就常被砸的鼻青脸肿，这些内功的修炼也不是一朝一夕的，路漫漫其修远兮，吾将上下而求索。</div>2019-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c0/34/0574bb44.jpg" width="30px"><span>最初的印象</span> 👍（7） 💬（3）<div>视频链接：https:&#47;&#47;new.qq.com&#47;omn&#47;20181217&#47;20181217A06I3V.html</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2b/58/11c05ccb.jpg" width="30px"><span>布衣骇客</span> 👍（7） 💬（0）<div>工作几年也大都是CURD，然后知道的就是索引的用法创建方式等等，和一些锁的概念以及实现方式，却不知道底层的具体是怎么一步步实现的，为什么sql这样一执行的结果就是这个样子，做的多就是分页查询以及联合查询等等。这个专栏不仅让我知道sql到底是怎么执行的，innDb和myAsm的区别，为什么这样建立索引等等，最后最重要的是学习方法，mysql也许会有更新，但是老师的方法确实一直受用，由衷感谢了...</div>2018-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/2a/e6b443f0.jpg" width="30px"><span>孙荣辛.py</span> 👍（3） 💬（0）<div>褚霸主管阿里云ECS时，也鼓励我们看源码，做技术分享，很愉快的一段时光</div>2022-04-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/glMH9jUOFS96sukOzshKWjQQbJDGc5nm367NlvicGeTSRp7jjLUib2Etrcbzz52ybAqFp40RSPS23v15799f3AHA/132" width="30px"><span>Ahmed</span> 👍（3） 💬（0）<div>老师好，很喜欢您的课程，我刚毕业入职不久，对大数据很感兴趣，但是公司的大数据开发岗位好像和想象的不太一样。更多的是写SQL，python或者shell脚本处理数据，做报表和客户打交道。想问的是，这是不是就是大数据开发的一种（听说阿里也有这种岗位），未来前景怎么样，技术方向有哪些发展或者说自己需要掌握什么技能？谢谢啦</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/20/9a/3b1c65fd.jpg" width="30px"><span>八百</span> 👍（3） 💬（0）<div>😂我看过好多书，就是不主动思考，也不太会总结，所以总是看了忘，忘了看，现在越来越意识到这个问题了，😂学过一点c，不会c++，一直希望有个师傅能够在技术上面给我指导，😂谢谢大佬。</div>2019-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/d7/5d2bfaa7.jpg" width="30px"><span>Aliliin</span> 👍（3） 💬（0）<div>学习用对方法真的很重要，感谢老师。</div>2018-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/83/96/73ff13a0.jpg" width="30px"><span>天亮前说晚安</span> 👍（2） 💬（1）<div>多线程的代码调试是真的麻烦，我都基本靠脑分析，debug辅助。</div>2020-02-27</li><br/>
</ul>