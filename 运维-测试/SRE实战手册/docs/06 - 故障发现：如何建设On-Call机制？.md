你好，我是赵成，从今天开始，我们进入课程实践篇的内容。

在上一部分，我们学习了SRE的基础，需要掌握的重点是SLI和SLO以及Error Budget（错误预算）策略。SLI是我们选择的衡量系统稳定性的指标，SLO是每个指标对应的目标，而我们又经常把SLO转化为错误预算，因为错误预算的形式更加直观。转化后，我们要做的稳定性提升和保障工作，其实就是想办法不要把错误预算消耗完，或者不能把错误预算快速大量地消耗掉。

这么说，主要是针对两种情况：一种是我们制定的错误预算在周期还没有结束之前就消耗完了，这肯定就意味着稳定性目标达不成了；另一种情况是错误预算在单次问题中被消耗过多，这时候我们也要把这样的问题定性为故障。

今天，我们就来聊一聊，为了最大程度地避免错误预算被消耗，当我们定义一个问题为故障时，我们应该采取什么措施。

## 聚焦MTTR，故障处理的关键环节

好了，我们先回顾下在第1讲的时候，提到故障处理的环节就是MTTR，它又细分为4个指标：MTTI、MTTK、MTTF和MTTV，之所以分组分块，也是为了更加有目的性地做到系统稳定性。

![](https://static001.geekbang.org/resource/image/3d/dd/3dd910e354da003e234b0340b68e76dd.jpg?wh=1940%2A1166)

那么，这四个环节，在我们故障处理MTTR又各自占多长时间呢？下面这个MTTR的时长分布图，是IBM在做了大量的统计分析之后给出的。  
![](https://static001.geekbang.org/resource/image/e5/fd/e5b28b0bed414afe8feda4f67b21a6fd.jpg?wh=1884%2A1837)  
我们可以看到，MTTK部分，也就是故障定位部分的时长占比最大。这一点，我们应该都会有一些共鸣，就是绝大部分的故障，往往只要能定位出问题出在哪儿了，一般都可以快速地解决故障，慢就慢在不知道问题出在哪儿，所以说我们大部分时间都花在寻找问题上了。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/86/06/72b01bb7.jpg" width="30px"><span>美美</span> 👍（20） 💬（1）<div>谷歌SRE应急时间处理策略有一条是：由万（全）能工程师解决生产问题 向 手持“运维手册”的经过演练的on-call工程师 演进，核心思路是建设故障处理SOP，保证SRE可以处理大多数故障。这个思路是否和确保关键角色在线冲突！</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/62/0a4e5831.jpg" width="30px"><span>soong</span> 👍（16） 💬（1）<div>监控体系解决的问题是给我们提供一个视角，更快发现或感知到问题发生。On-Call机制想要解决的在于真正去处理、解决问题的部分，关注点是有效性与机制建设本身。
没有监控系统的支撑，感知到故障发生所需的时间就要很久；没有高效的On-Call机制，处理并解决故障问题的时间也会被拉长，老师文中也有举例！从重要性的层面来看，两者是相互促进、相互支撑的作用。
从公司的发展过程来看，我个人认为，先建设一个能有效运行的监控系统，随后跟进On-Call机制的建设，是一个可行的路线！先建设On-Call机制，如果缺乏有效的监控系统，从提升系统的稳定性来看，针对性似显不足。希望看到老师的观点！</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/22/75/79693c63.jpg" width="30px"><span>EQLT</span> 👍（10） 💬（1）<div>ON-call机制重要，毕竟监控体系是持续优化进步的过程，而业务的故障是随时发生，优先恢复业务是最高优先级。良好的on-call机制既能保障业务，也能将处理过的故障快速反馈到监控体系，进一步优化监控体系，达到双赢。</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fb/b2/57cf8247.jpg" width="30px"><span>moqi</span> 👍（7） 💬（2）<div>在某某公司的运维小伙和我提起过，他们那的系统出了问题，SRE的第一件事是写故障报告，第二件事是解决问题，坑爹的是解决问题的时候还得不停的回复boss们的询问，更坑爹的是其他的SRE没有任何的协作机制，看他一人在那忙死，没有丝毫的互备机制，老大们似乎也不觉着这是个巨大的问题。

有再强大的监控体系，但没有协同作战的意识，这样团队里的成员哪来的团队荣誉感

这套On-call响应机制很棒，应该是团队不停的磨合和共创出来的</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/e6/50da1b2d.jpg" width="30px"><span>旭东(Frank)</span> 👍（4） 💬（1）<div>熟悉某个系统的最快最好的方式就是参与 On-Call，而不是看架构图和代码。

这块感觉应该是精通系统细节</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/03/8d/38a98dc6.jpg" width="30px"><span>牧野静风</span> 👍（3） 💬（1）<div>对于中小型企业的我们来说，运维能做的就是做好各种监控体系，尽可能在用户反馈问题之前监控到故障，进行恢复。我们的做法是，每个项目有个Leader，出问题运维，开发，DBA协同处理，小团队这样配合解决问题还是挺快的。但是以前遇到过凌晨出现问题，各种人员Call不上，所以我们上线尽量放在周一到周四</div>2020-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/60/90/521a6bcf.jpg" width="30px"><span>daniel＿yc</span> 👍（3） 💬（1）<div>从事一线运维工作6年了，最大的感受就是能力强的能被累死，我们行业比较特殊，基本上每个大的客户现场都有人驻守，加上客户自己的保障人员。有完整的on-call流程，奇葩的是，出现问题，第一反应是找能力强的人来解决，而当时当班的人只是用来传话的。。这就导致能力强的人被累死，基本上没周末没假期。。。。</div>2020-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d0/51/f1c9ae2d.jpg" width="30px"><span>Sports</span> 👍（2） 💬（1）<div>第一次听赵成老师的声音，还挺有磁性的，哈哈</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9e/d3/abb7bfe3.jpg" width="30px"><span>wholly</span> 👍（2） 💬（1）<div>看完老师的课程，很想从开发转岗到SRE，感觉很刺激😂</div>2020-03-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（1） 💬（1）<div>on—call和监控，我感觉是鸡生蛋蛋生鸡的问题。首先oncall不能没有监控作为基础，要不然只能靠人工反馈了，单纯有监控没有oncall不能及时解决问题。

监控对事故复盘有很好的作用，能完善oncall的指标，oncall反过来也能促进监控的发展，又是相辅相成的关系。

但是如果这两个都没有的情况下，先建设哪一个。
这个时候业务量不大，可以先建设监控，然后根据客服用户反馈解决事故，通过事故复盘增加oncall机制。</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/61/50/f5cc9f43.jpg" width="30px"><span>huadongjin</span> 👍（1） 💬（2）<div>MTTR的流程说的真好，在日常的稳定性工作中对这块有概念，但一直没有抽象出来，听赵老师你一讲，顿时豁然开朗。也给的工作规划起到了指导作用，那就是如何去缩短MTTI和MTTK的时长，提高故障修复效率，进而减少故障持续时长。我准备从告警和全网变更入手，这两项是故障的狼烟和故障的推手，在有疑似故障或故障定位中，拉取近一段时间的变更事件，包括安全、系统、网络、发布、数据库、中间件等变更类型，去协助定位故障。相信对他们的掌握有利于站在更高的角度看问题。请问这样的思路可行嘛，赵老师。</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>关于On Call流程机制的建设说到了痛点，往往就是系统出问题了，不能迅速的联系对应的责任人</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（1） 💬（1）<div>老师提及了错峰上班，可能我所经历的某些企业就是直接的翻班，这是国内IDC机房普遍使用的策略。必要时候这种翻班是从部门经理层一直到一线员工，集体翻班或者延长工作时间去保障其稳定性。
监控的体系再怎么做其实都是后知后觉，就像SRE中说及&quot;没有故障是特殊现象“，有问题有故障才是常态，故而On-call的机制是第一时间处理问题；二者又是相互的。只有在解决完处理完成后才能进一步去改善监控体系。
谢谢老师今天的分享：期待后续的课程。</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/38/2d/9c971119.jpg" width="30px"><span>若丶相依</span> 👍（0） 💬（1）<div>On-Call 更优先高一些，监控体系可以后期补。
On-Call 表示有人正在处理问题，监控只是更快的定位问题。</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3f/0d/1e8dbb2c.jpg" width="30px"><span>怀揣梦想的学渣</span> 👍（0） 💬（0）<div>我在运维某城市云平台时，遇到一个故障确认的坑。业务A需要组件1，2，3.组件1的资源占用90%时，会导致组件2资源占用攀升，组件3会因为组件2的响应时延，直接导致业务A整体不可用。组件1的资源占用到80%时，居然没人没系统告警提示，直到业务A崩掉，才发现出问题了，我当时真是哭死。
on call这部分，我感觉华为的接口人方式对我比较舒适，接口人有全局地图，可以精准的拉人判断问题，当研发A判断是组件1故障时，接口人拉研发B介入，研发B判断难以继续分析时，接口人直接管理升级拉入有更高视角的研发判断应该由哪个组件负责人继续介入。接口人计算修复时间，在不同时间范围拉不同的人，现场只需要和接口人保持信息同步即可。这点对于在客户现场处理问题的人，压力会小很多，也不必担心找错人影响研发休息。但对接口人可能工作压力比较大，他们需要精准判断，对系统全局了解。知道哪部分故障应该找谁。</div>2023-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/b3/6f/a57c81f4.jpg" width="30px"><span>hanson</span> 👍（0） 💬（0）<div>Google 工作手册中提到监控、告警是SRE必要的两大核心原则，可见建设监控体系更重要，同时提倡系统自动化机制。在On-Call 方面投入的也是有考虑时间和成本付出的，所以Google的 On-Call 文化注重个人的健康。
在SRE方面不是付出健全的情况情况下，既重视建设监控系统，同时On-Call 的投入成本也是非常高的。</div>2023-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/86/8e52afb8.jpg" width="30px"><span>花花大脸猫</span> 👍（0） 💬（0）<div>建设监控体系更加重要！但是对于监控体系中出现的 问题，如何快速的去定位解决，需要on-call机制及时的介入</div>2022-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0f/d5/73ebd489.jpg" width="30px"><span>于加硕</span> 👍（0） 💬（0）<div>又来回顾了一下，赵老师咨询个问题，MTTR的各项时间占比给的这个图是有代表性的吗？能否告知从哪里统计的结果 ，另外蘑菇街在MTTR各阶段的时间大概是多少，能否告知下呢？我们做个参考。谢谢</div>2022-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/05/3797d774.jpg" width="30px"><span>forever</span> 👍（0） 💬（0）<div>应该优先建立on-call机制，因为应用已经上线了，出了故障就需要找到一个关键工程师进行响应，监控体系可以根据on-call的一些历史数据进行针对性建设，这样未来监控体系也会更加实用</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/eb/ef/fc2d102c.jpg" width="30px"><span>老张</span> 👍（0） 💬（0）<div>我们之前还有专门的NOC团队，专门负责五步法中的故障监控、消息分发、问题上升及拉群和后续的组织复盘工作。</div>2022-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f4/89/86a8220a.jpg" width="30px"><span>牧野</span> 👍（0） 💬（0）<div>hello 赵老师，最近领了公司的回滚方案任务，一头雾水，今天看到老师的讲解有了一点想法，不知道是否正确：
MTTR：MTTI =&gt; MTTK =&gt; MTTF =&gt; MTTV
在可回滚的前提下：回滚将执行流程优化为：MTTI =&gt; MTTV，消除MTTK，MTTF时间消耗(预计有50%)
这个可以理解为做回滚的出发点吗?</div>2021-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0f/d5/73ebd489.jpg" width="30px"><span>于加硕</span> 👍（0） 💬（0）<div>SRE的On-Call 主要讲的是面对故障的应急手段；和参考手册处理日常事务；
在我们实际的On-Call中，还有答复业务研发的各类运维问题；这个方面，可以接入智能问答系统，设置语料库自动+人工并行答疑，并对答疑过程进行数据分析，找出答疑最多的问题，进行针对性培训和需求提炼优化运维产品。</div>2020-10-26</li><br/>
</ul>