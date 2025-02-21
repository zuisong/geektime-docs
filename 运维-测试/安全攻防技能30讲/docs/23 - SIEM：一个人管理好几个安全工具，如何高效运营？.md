你好，我是何为舟。

在前面的课程中，我们介绍了一些常见的安全产品。但实际上，解决公司的安全问题，并不是部署了这些安全产品就万事大吉了。安全防护的过程是一个与黑客持续进行攻防对抗的过程，黑客总是能够发现新的方法，绕过安全产品的防护，实施攻击。

如果黑客绕过安全产品，我们应该如何及时发现黑客的攻击呢？具体来说，我们应该如何对黑客的攻击路径和攻击产生的影响进行统计分析？以及在发现黑客的攻击之后，我们要如何提取攻击特征，补充安全产品的检测规则呢？这些都是我们需要持续关注的事情。因此，我们常说“建立一个安全体系很简单，运营好一个安全体系却很复杂”。

我们经常会使用SIEM（Security Information and Event Management，安全信息和事件管理），来帮助我们运营一个安全体系。通过SIEM，我们可以将散落于各个系统、设备和安全产品中的日志进行汇总和梳理，快速串联出黑客的完整攻击路径，更高效地完成安全体系运营的工作。

那SIEM究竟是如何高效运营安全体系的呢？下面，我们一起来看。

## SIEM有哪些功能？

我们先来说一下SIEM是什么。简单来说，SIEM就是一个基于各类日志，提供安全运营和管理能力的统一平台。基于这个定义，我们来总结一下SIEM的功能。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（3） 💬（1）<div>个人觉得SIEM的问题与现状和现在对于DBA的需求非常类似：项目的开始和高速发展&#47;后期需要。
和一些企业聊过：数据库上云了就可以不用DBA了，可是过了个2-3年后发现没有还是不行，团队大了数据库又不止一种了没有就更加不行；造成了一个很鸡肋的现状。开始设计阶段需要-能大幅控制和保证效率，中间阶段不需要-数据量不大只能纯监工，高速发展阶段需要-性能优化。
上述是跟着老师学到现在的最现实的感受：互联网安全的事情现阶段确实和数据系统的现状非常类似。
感谢老师的分享：期待后续的更新。</div>2020-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/d3/bcb7a3fd.jpg" width="30px"><span>半兽人</span> 👍（1） 💬（1）<div>正好之前看过Google出的书：SRE，运营确实是个比较大的话题，强调开发与运维人员要一起配合。Google干脆直接定义出一个SRE的岗位</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（2）<div>1，如何评估SIME的ROI来评估是否使用或不使用SIME，若使用是自己开发还是买商用的？2，SIME只有大公司才有可能使用吧？中小型公司没几个安全工貝，没有必要用SIME吧？3，可以使用splunk来建设SIME吗？听说splunk很贵但很好，在SIME用到splunk的企业多吗？</div>2020-03-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKgiaOK3jrpyibibqrT9zb5deKkTRzejW3VckqOOsYUpiaGqXn3uzB13yoOFyzlYtacKuY30icGbia9MRmg/132" width="30px"><span>爱学习的超人张</span> 👍（1） 💬（0）<div>老师好，我看您提到了很多次“安全运营”，请问安全运营的含义是什么呢？都包含了哪些操作呢？</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/f9/caf27bd3.jpg" width="30px"><span>大王叫我来巡山</span> 👍（1） 💬（0）<div>没有一劳永逸，只能不断战斗</div>2020-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/18/ed/80a212c7.jpg" width="30px"><span>Dolphin</span> 👍（0） 💬（0）<div>SIEM和SOC的区别是？</div>2022-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（0）<div>大数据工程师上线</div>2021-07-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/qzricN4j5oafQ5MB6pd6uRv7FHic5XicTPicpkqwd1Ea8TWSCbT9Z0RQgH8zvricickGx3epKV3OtrpDGNqcFvKatoibg/132" width="30px"><span>Geek_b8316f</span> 👍（0） 💬（1）<div>老师你好，请问下SIEM与日志审计，态势感知的区别</div>2021-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（0） 💬（0）<div>课后思考：想像一下，如果公司使用了很多安全产品，那么首先需要有个面板能够看到所有安全产品的状态，方便管理; 另外需要SIEM要收集安全产品的用户登录日志，行为日志，查看是否有异常用户，是否有非法操作；还有需要将所有安全产品本身的监控日志关联起来，就像文中说的要能够根据这些数据进行发现追踪；需要SIEM能将所有安全产品的日志按照某一个标准相关关联，方便分析，也要求遇到异常事件报警给相应人员及时排查；</div>2020-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/af/a5/afa1d7d7.jpg" width="30px"><span>hasWhere</span> 👍（0） 💬（0）<div>安全之路任重道远</div>2020-02-10</li><br/>
</ul>