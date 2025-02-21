你好，我是葛俊。今天我们来聊聊代码审查的落地。

在上一篇文章中，我和你详细讨论了代码审查的作用，也给出了选择适合自己团队审查方式的建议。但是，仅仅知道要做什么还不够，更重要的是落地。我见到很多国内公司也在尝试使用代码审查，但是效果很不好，往往流于形式，最常听到的一个负面反馈就是“代码审查浪费时间”。

代码审查的成功推行的确不是一件容易的事。今天，我们就一起尝试来解决这个问题。我会从三个方面给出一些建议：

- 第一，在团队内引入代码审查的步骤和方法；
- 第二，成功推进代码审查的关键操作；
- 第三，持续做好代码审查的重要原则。

今天的文章较长，我们现在就进入第一个部分，

## 引入代码审查的步骤和方法

从我的经验来看，要成功引入代码审查，首先要在团队内达成一些重要的共识，然后选择试点团队实行，最后选择合适的工具和流程。

### 1. 代码审查应该计入工作量

代码审查需要时间，这听起来好像是废话，但很多团队在引入代码审查时，都没有为它预留时间。结果是大家没有时间做审查，效果自然也就不好。而效果不好又导致代码审查得不到管理者重视，开发人员更不可能将代码审查放到自己的工作计划中。于是，形成恶性循环，代码审查要么被逐渐废弃，要么流于形式。

之前在Facebook的时候，我们预估工作量的时候就会考虑代码审查的时间。比如，我平均每天会预留1~2个小时用于代码审查，大概占写代码总时间的1/5。同时，代码审查的情况会作为绩效考评的一个重要指标。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/96/dae024ff.jpg" width="30px"><span>john_zhang</span> 👍（25） 💬（2）<div>我们推行过一段时间代码审查，因为三五个人，所以采用的是团体审查，每天半个小时左右，可惜后来开发进度赶，慢慢就没做了，现在开发同事总是以进度赶为由，不太认同代码审查，怎么破？</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（3） 💬（1）<div>老师好!公司的代码规范是用的阿里巴巴开发手册。也和leader沟通过怎么提升代码质量。leader建议多阅读开源项目源码。现状就是忙于业务代码，需求变动，并没太多时间阅读源码，也不知从何入手。以下几个现象比较严重。
1.为了实现业务老写出一个很长的方法，又找不到合适的角度去拆分这个方法。
2.无法平衡效率和可读性。
3.好用的工具库，jdk新特性掌握太少。</div>2019-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f9/36/f44b633e.jpg" width="30px"><span>bidinggong</span> 👍（2） 💬（1）<div>的确如此，必须把代码审查纳入工作量和绩效考核才能真正落实。</div>2020-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/4a/f1/68af6beb.jpg" width="30px"><span>紫色天空</span> 👍（2） 💬（1）<div>1.主观问题：基于代码评审意见作为绩效考评，感觉这个不是很好衡量，这部分是不是占的比能太大，如果占比不太大的话，是不是又会导致某些客观条件下大家不太重视去做代码审查了
2.客观问题：是不是刚开始或者对新手，比较容易提出问题，比如设计上，重构的几大方向上，复杂度上，性能上等。等大家经过一段时间互评后，基本很难找到问题了。此时再遇上比如紧急需求，紧急上线等，大家就会可能没时间review了。所以是不是大家多培训讨论，基本拉齐到同一水平，对代码质量也不错，然后就…又不review了</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（2） 💬（1）<div>非常好的一节课！其实代码审查还有一个重要的作用，就是能提前发现潜在的bug，尤其是在开发人员水平不太一致的时候。高水平程序员通常一眼就能发现潜在的代码问题。</div>2020-02-15</li><br/><li><img src="" width="30px"><span>Donald</span> 👍（1） 💬（1）<div>你好，从目前互联网发展的形势来看，现在越来越的公司的测试人力越来越少，开发测试比越来越高，但是开发对测试的要求却丝毫没有降低，同样要求测试需要对质量保障负责。所以，我想问一下，有什么好的方案解决这个问题吗？</div>2020-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b9/b4/d9edd7c6.jpg" width="30px"><span>Just for fun</span> 👍（1） 💬（1）<div>老师您好，根据文中的建议，一方面要求审查人要及时进行审查，另一方面又要求提交人进行频繁的原子性提交，这样就会导致审查人的工作会被频繁打断，这样不会影响审查人的工作效率吗？我们团队也是要求开发人员小步快跑，但是这样之后发现审查人的工作又被频繁打断，工作效率又降低了很多</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fc/80/21d67b9b.jpg" width="30px"><span>二狗</span> 👍（1） 💬（1）<div>一个功能怎么拆成多个原子提交，关于原子性提交不是很理解  （日常都是一个功能，一个bug一次提交）</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/09/f2/6ed195f4.jpg" width="30px"><span>于小咸</span> 👍（1） 💬（1）<div>葛老师，如果太追求代码的原子性，产生很多提交，会不会导致git太庞大而影响运行呢？</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f9/36/f44b633e.jpg" width="30px"><span>bidinggong</span> 👍（0） 💬（1）<div>引入代码审查的三个步骤：一是，就代码审查的工作量达成共识；二是，选择试点团队；三是，确定审查工具和流程。拿走了，谢谢老师</div>2020-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/4c/e8/c64e9710.jpg" width="30px"><span>chris</span> 👍（0） 💬（1）<div>请教一下老师，请问大概每天1~2小时的审核时间能审核多少代码呢？然后是整个团队人员的都审？每天每人平均产量有多少呢？</div>2020-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/47/30d4b61e.jpg" width="30px"><span>不是云不飘</span> 👍（0） 💬（1）<div>规范和审查一直由项目赶着上线没有实施，导致现在代码的坏味道越来越多，也没有时间去改，感觉一直恶性循环。</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/02/abb7bfe3.jpg" width="30px"><span>Alick</span> 👍（0） 💬（1）<div>葛老师，能否介绍下 Facebook 代码评审的绩效考评方法？

基于评审意见数，觉得纬度单一；基于问题严重性，有易起纷争的担忧；

采取何种代码评审绩效评价方式，能够起到正向积极导向效果？</div>2019-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/86/2b/f82a7d5a.jpg" width="30px"><span>文若</span> 👍（2） 💬（0）<div>老师 传统行业一直用SVN，想转为git，有何利弊？</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7a/5a/4dfb21f7.jpg" width="30px"><span>毕成功 Antony</span> 👍（0） 💬（0）<div>思考题二：Phabricator 使用数据库存储。

这个是不是因为采用了truck-based的模式，分支没有保留，就采用数据库来存储？</div>2021-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ff/52/093bb1a1.jpg" width="30px"><span>小包</span> 👍（0） 💬（1）<div>你见过或者经历过推行代码审查的成功或者失败案例吗？你觉得成功或失败的原因是什么呢？
----
我们也推送过代码评审，做法大同小异，包括统一思想，评估工作量加入code review时间，commits msg规范等，但实际执行下来跟预期有偏差，做的不好

有几点原因：
1、项目推进过程中插入其它临时项目，而有时为了保障原项目进度，会忽略code review
2、部分开发人员工作重，当忙时顾不上code review

想到的解决方案：
1、code review的重要性意识需要加强
2、增加code review负责人，以前是同一个模块的负责人相互review，不同模块的开发是否也能相互review呢（比如做网络模块的review计算模块，不确定好坏，希望老师给个建议）
</div>2021-03-09</li><br/>
</ul>