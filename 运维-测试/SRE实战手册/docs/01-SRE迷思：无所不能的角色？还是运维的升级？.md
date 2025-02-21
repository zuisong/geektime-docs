你好，我是赵成。

作为这个课程的第一讲，我先从实践的角度，和你聊聊应该怎么理解SRE。

为什么要强调是实践的角度呢？

开篇词里我们就提到过，有人认为SRE就是一个岗位，而且是一个具备全栈能力的岗位，只要有这么一个人，他就能解决所有稳定性问题。这还只是一种理解，而且这个理解多是站在管理者的角度。

也有人站在运维人员的角度，认为做好SRE主要是做好监控，做到快速发现问题、快速找到问题根因；还有人站在平台的角度，认为做好SRE要加强容量规划，学习Google做到完全自动化的弹性伸缩；甚至还有人认为，SRE就是传统运维的升级版，把运维自动化做好就行了。

你看，其实不同的人站在不同的角度，对SRE的理解就会天差地别，但是好像又都有各自的道理。

所以，我特别强调实践的角度，我们不站队，就看真实的落地情况。我总结了一下从实践角度看SRE的关键点，就一个词：**体系化**。**SRE是一套体系化的方法，我们也只有用全局视角才能更透彻地理解它。**

好了，下面我们就一起来看怎么理解SRE这个体系化工程。

## SRE，我们应该怎么来理解它？

我先给你分享一张图，这是结合我自己团队的日常工作，做出来的SRE稳定性保障规划图。  
![](https://static001.geekbang.org/resource/image/31/f6/31144fb00cf21005a8d0ae3dc02378f6.jpg?wh=3037%2A1874)  
我们最初画这张图是为了提高故障处理效率，将每个阶段可以做的事情填了进去，并在实践中不断补充完善，最终形成了我们探索SRE的框架图。你应该也发现了，这里面很多事情都很常见，比如容量评估、故障演练、服务降级、服务限流、异常熔断、监控告警等等。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/03/fe/d2c856c5.jpg" width="30px"><span>无聊的上帝</span> 👍（49） 💬（4）<div>说下我的感受。
DevOps主要是以驱动价值交付为主，搭建企业内部的功效平台。
SRE主要需要协调多团队合作来提高稳定性。
例如：
- 与开发和业务团队落实降级
- 在开发和测试团队内推动混沌工程落地
- 与开发团队定制可用性衡量标准
- 与开发，测试，devops，产品团队，共同解决代码质量和需求之间的平衡问题。
</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/43/1aa8708a.jpg" width="30px"><span>子杨</span> 👍（28） 💬（1）<div>听成哥这么一说，顿时有种豁然开朗的感觉。降低 MTTR，提升 MTBF。而 MTTR 里面，MTTI 一定要快。不过这里有一点不太理解，平常都是要以业务恢复为第一优先级的，这时候可能回滚变更操作就非常重要了，然后再去定位根因，先定位根因再去恢复业务，这个是有适用场景的吧。</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6b/3a/1ed3634f.jpg" width="30px"><span>云峰</span> 👍（10） 💬（1）<div>赵老师，好。SRE是否从项目开始就需要参与系统架构设计？如果只是在项目上线运行后才接触，遇到架构不合理的地方如何处理？</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/64/5b/2591309e.jpg" width="30px"><span>海峰</span> 👍（9） 💬（1）<div>看赵老师之前的书讲：SRE是 用软件工程的方法重新设计和定义运维。</div>2020-03-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKagLyKbgMsyKTrLplWu3iauiaGh97dhwFbfQ7RSoCx1SYiaL3icV3UsA5njaUVIYV01a1d2gBzf4CCbQ/132" width="30px"><span>海格</span> 👍（8） 💬（1）<div>SRE解决运维领域的故障目标，DevOps更偏向于为价值导向的效率目标，但是这个又是你中有我，我中有你，互相成就的一个过程，在实践SRE体系过程中，不可避免的要使用到一些DevOps中的一些技术，方法论，组织文化等，通过这些，达成一致目标。~~~</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6c/67/07bcc58f.jpg" width="30px"><span>虹炎</span> 👍（6） 💬（3）<div>感觉要做好sre ,  带头人至少是优秀架构师水准。普通开发只能做好分内事，慢慢学习经验。</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/92/be/8de4e1fe.jpg" width="30px"><span>kaizen</span> 👍（6） 💬（3）<div>SRE  要求对公司业务架构要有一个宏观的了解</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fe/ff/daf96217.jpg" width="30px"><span>null</span> 👍（5） 💬（3）<div>class SRE implements DevOps 
可以简单理解为DevOps 是一种接口，但是没说怎么实现，SRE 提供了一种视角，这么做在Google 成功过，可以结合自己企业的特点去实现DevOps 这个接口，做有自己特色的‘SRE’ 即可。</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/62/0a4e5831.jpg" width="30px"><span>soong</span> 👍（3） 💬（1）<div>个人认为：DevOps整体的表现倾向于价值交付，与敏捷的价值观贴合；而SRE的侧重点在于保障系统的稳定运行，通过系统稳定性实现价值最大化！两者有不同，也有交叉，他们不是非此即彼的选项。至于哪种更好，主要看团队的实际情况，产品本身所处的阶段，是另一个重要的考量依据！</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0f/d5/73ebd489.jpg" width="30px"><span>于加硕</span> 👍（3） 💬（2）<div>赵老师你好，听完本篇我又重新听了开篇。您接下来所讲的内容，应该都是基于团队已经在SRE实践的道路上。1.那么我们该如何判断某条业务线是否值的推行SRE体系呢？(业务的背景大致可以理解为:既追求稳定性，又不过分追求,且DevOps成熟度基本满足业务需求)


下面是自己对DevOps，SRE概念理解的方式，欢迎指正：
a. 人们对SRE理解存在偏差，是因为局限个人经验与当下所处维度(IT环境)造成的；通常当我们对一个概念理解存在模糊状态时，通过追溯到它的历史起源，对于理解它会更加深刻，也更加能够看清它真正的意图。
b. 一个职位的兴起，绝不是凭空在当前维度出现的，兴许是上游出现了某种压力&#47;变化，于是下游便出现某个职位来应对这种压力&#47;变化。

文章结尾补充一个问题：DevOps与SRE矛盾点：
c. devops解决全栈交付，全栈交付是非稳定性因素之一，而SRE关注稳定性</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ab/f1/cd9ab023.jpg" width="30px"><span>潜行</span> 👍（3） 💬（2）<div>我们是只有三个人的运维小团队，而且职能也没有分的那么清楚细，基本上是每个人所有的事情都做，而SRE又涉及到这么多方面。请问老师，对于我们这种小团队，要实践SRE应该先从哪方面入手？</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8f/d3/333f912a.jpg" width="30px"><span>乐迪_张建</span> 👍（2） 💬（1）<div>个人觉得DEVOPS目的是更快的创新和更好的客户体验。SER的目的是最快的速度恢复故障！不管是AWS的DEVOPS还是GG的SRE，适合的才是最好的！都是在慢慢通往这个道路上。最后隐隐约约:SRE和DevOps它有，它无:它无，它有！不知道用语言怎么表达</div>2020-03-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLke9yyicW4DA3fvmjEXJqnqBiciaUM0R421fvoqVZfvPvDwoTfFo0wjVd9VrMHibk6QgN4PjB00YPXYw/132" width="30px"><span>Geek_642328</span> 👍（1） 💬（1）<div>老师您好，
我现在有一个困境，运维关注生产环境的稳定性，线上升级变更操作，我们希望次数尽可能可控，但目前公司产品迭代快，版本更新快，线上升级频繁。在这个过程中，生产环境的稳定性我要如何去把控</div>2021-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/66/00/b7b58d74.jpg" width="30px"><span>我？好吧好吧！</span> 👍（1） 💬（1）<div>有个小疑问~当稳定性提高到一定程度时，技术手段对稳定性的推动就会减速或者陷入瓶颈，这个时候往往需要增加成本稳定性才能获得进一步的提高（资源较多冗余）。老师如何看待这种用成本换取稳定性的模式？</div>2020-04-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（1） 💬（3）<div>虽然现在是在做devops，我们公司没有sre的岗位，听完这节课之后还是对这两个岗位有了一定的认识。
devops目标是提升开发效率和提升交付效率。
sre是保证服务稳定。
devops针对的是交付产品和开发者，sre针对的是服务。
一个追求交付在产品的质量上的快，一个是追求产品部署之后部署的稳。

在请教老师个问题，是不是sre岗位在to c的公司居多呢，国内sre现状是咋样的呢。</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b1/81/13f23d1e.jpg" width="30px"><span>方勇(gopher)</span> 👍（0） 💬（1）<div>赵老师的课程让我收益匪浅，结合我最近的实战，总结了一些经验，希望老师和大家多多指教。SRE 实战 (01)|初识 SRE，探索 SRE 如何推进技术债务改造http:&#47;&#47;gk.link&#47;a&#47;10zgb</div>2021-09-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJqYTKNBfYia33zDPkn8IULD1OwibzjuV4APicvLFEZgKjysec8vYyPsXVJF5BZpmObBcnN8Gic0yBicmQ/132" width="30px"><span>西湖游侠</span> 👍（0） 💬（1）<div>说的很清楚，SRE就是一个体系化工程</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/03/d9/7538e630.jpg" width="30px"><span>终身学习者</span> 👍（0） 💬（2）<div>赵老师，其实从实际问题处理的情况看，根因分析放在故障定位是不太合适的，这样会耽误故障恢复的，重点应该放在如何恢复。比如很多时候我们找到异常组件进行隔离就可以了，然后在事后分析那个组件的异常原因。</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/f7/abb7bfe3.jpg" width="30px"><span>刘冲</span> 👍（0） 💬（3）<div>我想问个问题，怎么算一个故障？客户投诉或者自己发现？或者有些问题可能是故障有些可能不是故障，粒度怎么界定</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/7a/29814b43.jpg" width="30px"><span>硕</span> 👍（0） 💬（1）<div>传统的运维很容易变成开发的工具人。sre 通过自动化系统、制定规范流程等工资将自己脱离工具人角色，再运用运维体系丰富的知识结合当前线上的实际情况，尽可能提升线上稳定性</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/76/994a9929.jpg" width="30px"><span>OlafOO</span> 👍（0） 💬（1）<div>MTTF，还有种缩写是Mean Time To Failure ，平均故障前的时间，和文章里的MTBF一个意思。可用性的计算公式MTTF&#47;MTTR+MTTF 是稳定性领域的第一性原理，，这个在左耳听风的专栏弹力设计里也有讲到。。。缩写方式太多😂</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/85/d91dec8c.jpg" width="30px"><span>Warm</span> 👍（0） 💬（2）<div>devops只是sre中的一环，提供高效的交付，测试，发布。</div>2020-03-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rkfQQekacJcVEP7icwfF1ibvzolibHgibibPqg9aIich1vd4ffmMj4CJH64BcqJsXcSFB9BVxb9YUH5rb5T78EUOcKJQ/132" width="30px"><span>春来草自青</span> 👍（0） 💬（1）<div>无论sre还是devops，从实用的角度看，哪个能够更简单高效低成本地解决眼下的痛点，并为以后的技术演进保留足够的想象空间，就选哪个。行业不缺牛人，也不缺顶尖技术，但每家公司的条件和能负担的成本是不一样的，设合自己的才是最好的</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（0） 💬（1）<div>DevOps的课程其实自己学习的蛮深包括相关书籍可以说不少都看了一遍，相关工具如果要花费大量时间可能对我而言确实有点难，尤其运维【注：我所值的运维不仅仅是指系统，包括数据库、操作系统、机房。。。这个整体】
不过开发能力的短板对我而言确实短时间难以提升太多：效率和平台体系的合理结合，如何二者互补我觉得才是更加去追求的。
我们常说万能的运维：其实运维大多数在coding能力方面还是无法和开发比，不过在效率与性能排查方面又是开发无法做到的。故而我记得老师课程中推荐《SRE Google运维解密》书中强调的内容就如老师今天流程图中的oncall，其实DevOps同样看如何去解释和理解；就像DevOps经常和敏捷混淆一样。
平台体系的思路去做好就好：过分去追求SRE或者DevOps，可能我们反而会迷失其本意。
谢谢老师的分享：我觉得听课的过程又可以再把老师的书和课程在看一遍了；说不定课程结束自己的版本就出来了。</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（0） 💬（2）<div>sre包括devops</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/bb/a1a61f7c.jpg" width="30px"><span>GAC·DU</span> 👍（0） 💬（1）<div>SRE和DevOps对比，从以往的工作实战经验理解前者更具备全局战略意义，如果硬性对比，SRE更像是军队里面的参谋长，而DevOps更像是指导员。这是两个个性的独立存在，选择个性最属于你的那个准没毛病。</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/01/d3/5cbaeb95.jpg" width="30px"><span>HUNTER</span> 👍（1） 💬（0）<div>除了故障平均时间间隔和故障修复时间，衡量标准里是否还应该有故障影响半径呢</div>2021-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3f/86/4e2d599b.jpg" width="30px"><span>NICE</span> 👍（0） 💬（0）<div>SRE和DevOps有相同的价值和不同的实现价值方式方法。我个人理解DevOps更加的侧重于软件工程开发，发布测试相关的持续自动化价值流，让用户更快的获得反馈。SRE更侧重于稳定性，服务保障有点类似于L1加L2加L3。
快速发布和服务稳定性运行都是给业务增加价值和减少损失的方法。</div>2024-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2a/ff/a9d72102.jpg" width="30px"><span>BertGeek</span> 👍（0） 💬（0）<div>sre体系，更多能直接的反映出企业运维架构和能力水准
devops体系，更多能直接反应企业开发快速交付和快速上线部署的能力</div>2022-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/ef/de0374ac.jpg" width="30px"><span>祝洪娇</span> 👍（0） 💬（0）<div>SRE更适合很少有需求变更的项目，主要是进行系统运维，侧重维护保持系统的稳定性。
DevOps更适合需求变更比较频繁的项目，侧重快速稳定交付。
但是大部分项目都需要二者相结合，在持续交付的同时保持系统的稳定性。</div>2022-05-02</li><br/>
</ul>