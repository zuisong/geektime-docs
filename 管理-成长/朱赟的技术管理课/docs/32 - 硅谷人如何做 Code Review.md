今天技术管理课的主题是： Code Review，也就是我们常说的代码评审。Code Review 主要是在软件开发的过程中，对源代码进行同级评审，其目的是找出并修正软件开发过程中出现的错误，保证软件质量，提高开发者自身水平。

和国内的工程师聊天，发现国内公司做代码评审的比例并不算高，这可能和各公司的工程师文化有关系。不过硅谷稍具规模的公司，代码评审的流程都是比较规范的，模式也差不多。

## 首先是两个概念

在进入正题之前，先介绍两个概念，一个是 Commit，一个 PR。硅谷大部分公司都使用 GitHub 企业版管理自己的代码仓库，GitHub 里的 Commit 和 PR 的概念在代码审核中非常重要。

**1 Commit。**就是 GitHub 上的一次“ Commit ”行为，这是可以单独保存的源代码的最小改动单位。

**2 PR。**也就是 Pull Request，是一次代码提交请求。一个 PR 可以包含一次 Commit，也可以是多个。提交请求后 GitHub 会在相关页面上显示这次提交请求的代码和原代码的所有不同之处，这就是本次 PR 的所有改动。

请求提交后，其他工程师可以在 PR 的页面上提出意见和建议，也可以针对某一些代码的改动进行讨论，也可以给整体评价。代码的作者也可以回复这些意见和建议，或者按照建议进行改动，新的改动将为本次 PR 中提交新 Commit（也可以覆盖之前的 Commit）。

关于 GitHub 和 Pull Request，池老师最近在他的公众号里写了一篇“  
[GitHub 为编程世界带来了什么改变](http://mp.weixin.qq.com/s/Ed_qK-Y8hh1hW_CCs6o7KA) ”，这篇文章中有比较详细的描述，你可以参考学习。

## 其次，我来谈谈代码合并规则

一般情况下，所有的 PR 都必须有至少一个人认可，才能进行合并。如果改动的内容涉及多个项目，则需要每个项目都有相关人员认可才能合并。还有一些特别关键的代码，比如支付相关的，通常也会需要支付组的人确认才行。

在代码合并之前，进行 Code Reivew 的工程师们会在 GitHub 的相关页上给出各种评论，页面是共享的，这些信息大家都能看到。

有些评论是询问，代码的作者直接回复或解释就行，有些是指出代码的问题，代码作者可能会据此改动，也可能不会同意，那就需要回复评论，阐述观点，你来我往。有时候一个实现细节，讨论的主题可以多达十几条或几十条，最终需要达成一致才能进行合并。

## 再次，帮助别人成长，而不是帮他写代码

以前有朋友会说：“看到代码写得太差，觉得来回评论效率太低，干脆自己冲上去搞定” 。曾经我也有过类似的想法，不过我慢慢意识到这并不是一个合适的想法。

首先，从对方的角度来说，代码写不好，可能是对业务不熟悉，对编程语言不熟悉，也可能是对公司代码的整体架构不熟悉。如果你帮他 “写” ，而不是耐心指出哪里有问题，那么下一次他可能还是不知道怎么做。这样不仅无益于别人成长，有的时候甚至会让别人有挫败感。

并且，帮别人写代码的方式可扩展性很差。即使 Code Review 会花掉十倍于你自己写的时间和精力，但它会让人明白代码应该怎么写，从长远来看，这其实是在一定程度上 “复制” 你的生产力。

你不能什么都自己写，尤其是开始带项目、带新人以后。每天 Review 五个人的代码和写五个人的代码，长期而言哪个更合算呢？答案显然是前者。

写代码是一个学习过程，怎么做一个好的代码审核人更是一个学习和成长的过程。自己绕过一个坑不难，难的是看到别人那么走，远远地你就能告诉他那里有个坑，而他在你的指导下，以后也会帮忙指出别人的类似问题。

我在这一点上最近感触尤为深刻。随着团队越来越大，新人也越来越多，有一段时间我每天工作的一半时间都在 Review 别人的代码，写评论。

这样做的初期确实比较辛苦，不过效果也随之慢慢显现，大部分时间工程师们已经可以进行相互 Reivew 代码了，于是我可以腾出很多时间来做别的工作，代码质量也得到了保障。

## 提交代码的类型

在进行 Code Review 之前，要搞清楚提交的代码到底是干嘛的，然后进行针对性的审核。我们一般把提交的代码分成四类。

1. Bug 修复。一般公司都有独立的 Bug 追踪和管理系统，每个 Bug 都有一个票据。代码提交的 PR，一般和票据是关联的。
2. 代码优化。比如文件的移动和拆分，部分函数的重构等。
3. 系统迁移。包括代码库拆分，用另一种语言重写等。
4. 新系统和新功能。新功能在实现之前都需要进行设计审核，最终版本的设计文档会包括数据库的 Schema、API 的签名（ Signature ）、代码的流程和模块等内容；相关代码的提交，也就是 PR，一般是和设计文档挂钩的。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/61/985f3eb7.jpg" width="30px"><span>songyy</span> 👍（57） 💬（1）<div>写蛮棒的，我比较喜欢文中的观点: 1) 代码审查可以让工作可扩展; 2) 审查边界情况; 3) 代码回滚的例子; 4) 那段Ruby代码的考虑点问题; 5)有ui改动相关的，要给改动前和改动后的对比图(这点我一直在做，也在要求别人做 😁)

此外，从我经验上，还有这么几点:
1) 持续集成环境可以跑测试，测试结果可以自动加到PR上面(我觉得你们肯定是有在这么做的 😁)。这样子让review的人有个更好的信心
2) 代码在build的过程中，可以加上linter，进行code style的检查(我觉得这个你们肯定也在做 😁)。持续集成环境可以把检查结果加在PR上面。我们公司在用code climate的Chrome plugin，这样子做code review的人就不需要提style相关的改动了:能让机器做的事，就没必要让人来做
3) 如果希望强制互相的代码审查，可以在github里面设置，比如master branch，是protected branch，只有在ci通过，有人approve了这个pull request之后才允许merge
4) 在pull request本身要给足context信息，从而让进行review的人很容易搞清楚这个pr在做什么;在之后希望溯源什么改动的时候，在定位到这个pr时，也可以更好地了解当时做这个改动的原因。</div>2018-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/96/d01ebfe7.jpg" width="30px"><span>archmageforac</span> 👍（13） 💬（1）<div>我是做Android开发的，负责的是公司Android APP内的一个模块，整个APP是插件化的架构，即APP本身所在项目是一个空壳，通过配置来决定哪些模块会集成进APP。我们这边的做法是：

Step 0. Push检查：在每次push之前，检查提交者是否已经自测过了自己修改代码相关的全部分支，并会生成一个自测覆盖率，提交到commit信息中。如果自测覆盖率过低，reviewee需要给出合理原因解释。
Step 1. Merge检查：在提交PR前，先进行代码静态检查，比如lint检查、组里资深工程师根据业务制定的“坏味道”检查等，这样可以避免绝大部分低级错误和常见的共性错误。
Step 2. 人工review，reviewer会指定一个资深同学和一个新人，资深同学把关，新人学习和了解其他同学coding的思路。同时也鼓励新人提出自己的见解，进行思想碰撞。reviewee是新人的话，reviewer会更加注重实现细节，会讨论和比较其他的实现方式；是资深同学的话，会更加侧重在整体架构设计上。
Step 3. 代码合入后，会走一个自动化的打包和集成工作。打包后会集成进APP，这个过程会在APP范围内进行全局检查，确保没有底层项目接口变更导致上层项目接口调用失败的问题。
Step 4. 集成后形成一个apk，然后跑自己业务以及整个APP核心路径的单元测试。这一步其实目前我们还没有，但我觉得是有必要的，正在计划推动落地。</div>2019-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/73/ae/d602cecf.jpg" width="30px"><span>杨石坡</span> 👍（8） 💬（0）<div>我们也有代码审核，但是我认为很失败，主要表现在形同虚设。
原因如下:
1.领导分配任务时，没有给评审分配时间。在相同的时间内，在原有工作量之上在加入代码评审，评审就是负担，应付了事；再说代码评审有没有奖惩。不看代码，接先approval然后merge就成了最常见的做法。
2.pr看不懂
    a.pr说明描述不清或者没有描述。
    b.pr里面包含很多东西。
3.pr不给留时间，或者留时间了也没有人看。</div>2018-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/c9/501a1d02.jpg" width="30px"><span>self-discipline</span> 👍（6） 💬（1）<div>首先是招聘到合适的人；其次如果人不行，怎么推进点东西都费劲的；我们这我推进的代码审核，好似把他们打劫了一番，好比老牛不喝水推上刑场一般</div>2018-07-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/QUCB325iaqkJCz8uzRFicXgoISWnlund6DdE25ibjlCTV2zkiccQsZ4Nib9XNdcCJpuPa2XaZ9GnRwp6ibJq4VegHsug/132" width="30px"><span>H</span> 👍（4） 💬（0）<div>很庆幸之前的团队就是这么做的，开始觉得太苛刻，后面慢慢觉得这样对大家(特别是对自己)的成长挺大的。后面我在review别人的代码的时候也“苛刻”了些😬</div>2018-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/96/8f/4efb2862.jpg" width="30px"><span>nigel</span> 👍（4） 💬（0）<div>我想有人来review我的代码，但大哥们都忙。</div>2018-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5b/ea/d49b9301.jpg" width="30px"><span>杨少侠</span> 👍（3） 💬（0）<div>工作时间没时间做review</div>2018-01-24</li><br/><li><img src="" width="30px"><span>木头疙瘩</span> 👍（2） 💬（0）<div>真的挺希望能加入一家有这样环境的公司，然而我呆过的大小厂都没有这个</div>2018-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/fd/e5cd25d2.jpg" width="30px"><span>luming</span> 👍（1） 💬（0）<div>在国内公司，Code review如何能不流于形式还是个挺有挑战性的问题</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/4d/7a/106c3745.jpg" width="30px"><span>mikejiang</span> 👍（1） 💬（0）<div>代码review不太好执行，国人比较爱面子，我一般的做法是，线下反馈review建议。</div>2019-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/0b/fb876077.jpg" width="30px"><span>michael</span> 👍（1） 💬（0）<div>代码审核真的是很重要，不仅使得生产代码有质量保障，也可以提高组员编程水平，也是个相互学习的过程。</div>2018-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/21/ca81fd5d.jpg" width="30px"><span>Lament</span> 👍（1） 💬（0）<div>高校里面，菜鸡互啄其实问题不大，只要言之有物，至少能带来观点的碰撞，不要演变成相互人身攻击或者某些无意义的争论就好，比如Php是最好的语言……很烦。</div>2018-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/e6/87197b10.jpg" width="30px"><span>GeekAmI</span> 👍（1） 💬（0）<div>好吧  你们的代码提交真复杂  </div>2018-01-24</li><br/><li><img src="" width="30px"><span>何慧成</span> 👍（0） 💬（0）<div>review需要特别关注，特别是对新人，要操心的地方不少</div>2020-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/91/f5/6881f336.jpg" width="30px"><span>姑苏小沈🏃🎸</span> 👍（0） 💬（0）<div>我们团队也在实践每个pr需要code review，不过现实中，reviewer都很忙，经常没时间去了解代码的前因后果和深究算法实现，于是这个工作常常流于形式了。</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/1e/c7e77731.jpg" width="30px"><span>Feng</span> 👍（0） 💬（0）<div>组长想推进，但是实在没时间，太忙，也是一种提升方式</div>2018-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/86/f4/331f33a7.jpg" width="30px"><span>anchor</span> 👍（0） 💬（0）<div>有什么好的review工具推荐吗？之前用fisheye git有好的实践方式吗</div>2018-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/86/f4/331f33a7.jpg" width="30px"><span>anchor</span> 👍（0） 💬（0）<div>大家有什么好的review工具，之前都用fisheye</div>2018-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/86/f4/331f33a7.jpg" width="30px"><span>anchor</span> 👍（0） 💬（0）<div>大家有什么好的review工具，之前都用fisheye</div>2018-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/26/1015d573.jpg" width="30px"><span>gevin</span> 👍（0） 💬（0）<div>GitHub 推荐开发时才有GitHub Flow进行协作，原来不是很理解，仅以为PR主要用于向他人的开源项目做贡献。看了安姐这篇文章，才意识到，PR和GitHub Flow，能很好的落实code review，这应该是推荐使用GitHub Flow的一个更重要原因</div>2018-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9d/99/bc41ff8b.jpg" width="30px"><span>xiao</span> 👍（0） 💬（0）<div>请问在各自具体团队上是有专门的code review人员？如果是团队里不是专门评审，那工作量如何平衡</div>2018-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/e2/fc6260fb.jpg" width="30px"><span>ajodfaj</span> 👍（0） 💬（0）<div>在高校，都是菜鸡互啄，就不review了吧</div>2018-01-25</li><br/>
</ul>