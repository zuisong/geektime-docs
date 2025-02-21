100篇的正文已经全部结束了，估计你学得也有点累了吧？时隔这么久，正文终于结束了，从今天起，我们继续加餐内容。

跟正文内容相比，加餐内容我希望尽量轻松有趣，帮你拓展知识面，主要是课后的一些小分享，有的会以讲故事为主，但我也希望它能给你带来收获。如果能够引发你的思考和共鸣那就更好了。所以，我也希望你在留言区，多说说自己的感受和看法，多多与我互动。

话不多说，让我们正式开始今天加餐的内容吧！

## 为什么国内企业不重视Code Review？

在专栏[第80讲](https://time.geekbang.org/column/article/232687)中，我列举了Code Review的重要性，在项目中执行Code Review会带来哪些好处，以及如何克服一些常见的难题，在项目中启动Code Review等等。今天，我们想再继续这个话题，和你聊一下Code Review。不过，我刚才也说了，今天的内容会相对轻松一些，我会主要给你讲讲我在Google做Code Review的一些经验和心得。

我们都知道，Google在Code Review方面做得非常好，可以说是很多公司学习的榜样。从我个人的经历来说，我的技术成长相当大的一部分得益于当年在Google的Code Review。所以，我也希望更多的同行能意识到Code Review的重要性，能够在项目中推行Code Review，受益于Code Review。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/3b/67/c188d3bc.jpg" width="30px"><span>tingye</span> 👍（126） 💬（11）<div>国内code review难推广的一个原因可能也和文化有关，老外习惯直来直往评价和就事论事，中国人为人处世讲究委婉，要面子，特别同级别同事间往往不好意思直接指出别人的问题</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/85/49/585c69c4.jpg" width="30px"><span>皮特尔</span> 👍（14） 💬（3）<div>之前好像听池老师说过：极客时间团队是有Code Review的。
感觉这件事主要还是看团队吧。</div>2020-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（12） 💬（2）<div>公司让我等制定code review规范，并推广。
ps:现在公司情况：code  review 各自（组）为政。
我了解的几个组是只在乎功能正确性，不怎么在乎编码规范&#47;风格、命名风格。各组的评审流程也不一样。
我现在的思路
1、收集各组的评审方式及规范
2、整合各组的方式和规范结合业界的最佳实践（如google）制定出适合我司的一套规范与流程1.0
3、推广使用，收集反馈，补充和优化规范和流程，避免形式化

小争哥或各位学友有哪些好的建议呢，谢谢</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/39/85/c6110f83.jpg" width="30px"><span>黄骏</span> 👍（4） 💬（1）<div>有时候review同事的pr，一些语法和编程风格的问题比较多，好像重视程度也不够，反馈后新的pr仍然如此，对reviewer来说就不太友好了，觉得我提的问题太傻了么？</div>2020-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/a0/6b/0a21b2b8.jpg" width="30px"><span>迷羊</span> 👍（3） 💬（6）<div>感觉还是没有会 Code Review 的人带</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（2） 💬（1）<div>想了解下Google是如何将这些规范落地的？有什么具体措施国内公司能够借鉴吗？道理大家都懂，但实际操作起来怎么监督实施呢？</div>2020-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/49/3c/5d54c510.jpg" width="30px"><span>skull</span> 👍（0） 💬（2）<div>老师，我看了google的code review最佳实践，发现是以每一次的pull request为维度进行的code review，而我们现在的code review是以项目为维度的，项目提测前进行统一的code review，发现不好的代码，leader让去修改，这样两种方式哪种更好点啊</div>2020-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（53） 💬（4）<div>原因：
1.缺少追求卓越的氛围。先run的理念退化成了能run就行。
2.招聘要求上基本都会有代码设计能力，编码规范，甚至代码洁癖的项。但实际上基本不提，顶多背几个设计模式。那么编码能力就变得很鸡肋，因为它与薪资几乎无关。叫好不叫坐大概就是这个意思。
3.重构本是小步快跑，但我看到的大部分都是重写，而非重构。这就导致认知中的重构成本很高，进而就会排斥。而只写代码不重构代码，在编码能力的提升上是很缓慢的。如果把识别坏代码的能力看作是一把尺子。经常重构的人，这把尺子的精度是一毫米，只写功能的人精度只有一分米。那么在识别坏味道评估改动点时就会很模糊，模糊就更不敢下手，恶性循环。

办法：
1.氛围，国内的开源项目先开始讲究，带个氛围。
2.将编码能力和算法放在同等位置看待。其实编码能力强的人，往往意味着思路清晰，讲究。这种人工作能力一般差不了。
3.普及重构理应小步快跑的理念。把事情拆小，把小事情做好，都很重要。重构需要会拆解工作，然后也别看重构手法简单，刻意训练后也会有质变。（重构是提高普遍认知的有效手段，只有认知上去了codereview才能被 重视）</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/bd/e14ba493.jpg" width="30px"><span>翠羽香凝</span> 👍（45） 💬（2）<div>我同时在美资外企和中国本土企业工作过，看到了另一个方面的问题：在美资企业，往往技术领导者有很大的权限，甚至很多公司的最高领导自己就是技术出身，对技术非常重视，也重视代码质量。
而中国的本土企业，大部分公司的领导都是销售，财务出身，有些甚至来自投行，把PPT看得重于一切，至于代码质量，抱歉，领导可能重来不知道代码还有质量这回事，不是应该完成功能通过测试就OK了吗？
而且，大部分的项目都很短命，就像中国的PPT文化一样，开发项目的目的就是“骗骗你”，钱到手了，项目的是否易于维护，是否易于扩展都并不重要，领导不关心，抱歉，你还真以为你要做一个Facebook呢？看看中国有几个BAT就知道了。</div>2020-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/a4/24955994.jpg" width="30px"><span>progyoung</span> 👍（24） 💬（0）<div>就个人的工作经历来看，很多互联网公司程序员的职责就是完成业务，没有功能bug是第一位的需求，至于代码质量，在leader的眼中根本就不重要。而且一个需求提出之后，恨不得马上就能看到结果，发布上线。在这样的大环境之下，996盛行，code review就被认为是浪费时间，怎么能推行的开呢？</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/75/e7c29de4.jpg" width="30px"><span>wkq2786130</span> 👍（19） 💬（0）<div>我刚开始也不理解code review ，直到有一天发现自己写的代码自己读不懂，然后开始优化，开始写注释，理清主要逻辑，开始分层，开始使用通俗易懂的命名，后来逐渐意识到code review的好处</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ca/c7/00e544c2.jpg" width="30px"><span>黄林晴</span> 👍（10） 💬（0）<div>最后一段说的很扎心
等你当了领导 有了话语权 ……
可能坚持review 的人 由于让同事觉得太苛刻
伤面子，永远很难晋升</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/4e/9b6c9cab.jpg" width="30px"><span>焕伦蔡</span> 👍（8） 💬（1）<div>个人愚见，无法推行code review的原因：
1.很多公司项目本来也就做不大，大不了就费点时间重写呗，有些项目甚至就是做死了，例如Java来说可能一个SSM就搞定了，然后也就没有然后了
2.团队水平有限，团队没有一两个确实有能力的人，都不知道什么样的代码才是优秀的代码，code review就会变得很耗时费力，基本到后面就都没人做了
解决方法：
1.看过《高效能程序员的修炼》一书，觉得有一点很好，那就是确保有多一双眼睛盯着你的代码
2.制定最简单基础的规范，比如说命名为驼峰，不能使用拼音，超过一屏的函数得拆分，然后强制执行，所有人按着这个标准，有时候简单暴力就是最有效的</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/62/a7/3e6fee86.jpg" width="30px"><span>K战神</span> 👍（8） 💬（1）<div>有一次看到新人代码有很多问题时，我马上进行了提交限制权限。每一次提交的代码都发合并请求，我会每一句仔细看，然后评论，改完，再看再评论。效果显著，我们一起根据问题对应到代码整洁之道这本书，看看命中了拿着坑。

还有一次我们同级别的审查我的代码，我当时确实比较排斥，我觉得同级别有经验的一起互相审核，感觉难度确实有些大，大家都在极力表述自己是对的，反而再互相理论。

推行代码审查，前几步确实很费时间，很费精力，后面慢慢就好了，然后这种对代码的极致追求会成为习惯</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（5） 💬（0）<div>我们公司，从18年底就开始接入code review了，然后到现在，大家都把code review当成了一个过场，哎，那谁给我过下代码。个人感觉，code review带来的益处是需要个长期积累的过程，短时间，对个人，对公司来说，带来的益处也许并不明显。但是坚持下去，时间一久，就会得到意外的收获。code review更加是一种态度，一种责任</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/bb/947c329a.jpg" width="30px"><span>程序员小跃</span> 👍（4） 💬（0）<div>比较庆幸自己的第一份真正意义上的工作就有Code Review的存在，让我从菜鸟开始就体会到了Code Review的重要性。当别人监督你的时候，你自然就会给自己绷紧一根筋，刻意需要自己严格按照公司的规范写代码。

可惜后来出圈了，氛围变了，尽管自己刻意练习，但还是不免有松懈的地方。如何破圈？我估计，就是让我更努力点，先成为Leader吧，哈哈</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（3） 💬（0）<div>codeReview和kpi、绩效又不挂钩，老板只关注结果，所以注定cr推行只能流于形式。</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/05/19c5c255.jpg" width="30px"><span>微末凡尘</span> 👍（3） 💬（0）<div>以前写代码从来没有注意代码质量的问题，而是完成功能为第一步，然后就没有然后了，直到我现在入职一家新公司，虽然公司不大，但是有很好的CR习惯，每次提交代码，leader都会review我的代码并且非常细心，耐心的给出修改意见，有助于我代码水平的提高，现在写代码时会不自觉地注意代码书写的规范，因为感觉总有一双眼睛盯着你在。。。</div>2020-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/47/f6c772a1.jpg" width="30px"><span>Jackey</span> 👍（3） 💬（0）<div>能做的就是在自己的团队中大力推广code review，不符合规范的代码一定不能进入repo</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/3b/97/ce00cd8d.jpg" width="30px"><span>coco張</span> 👍（2） 💬（0）<div>我们公司也有code review,外企嘛，很多形式都会有的，但是效果不是特别好，关键还是reviewer的能力不足以支撑给出意见，流程上是加上了，但是merge以后还是一改再改</div>2020-07-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqZIqY4cs6YKNx0OqeMrbjLIicqiafLNtLYJTN2zTtVPlwXZ7qlJ7xrGQictk1xCq5pEsIyqnkiaCib4zQ/132" width="30px"><span>全炸攻城狮</span> 👍（2） 💬（0）<div>code review的前提是知道什么是好代码，以及严格的编码规范。第一点需要有经验的工程师，具备review其他人代码能力的leader，第二点需要借助工具如lint。还有一点是要形成习惯，当成开发任务中的正常环节就好了</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/16/66/083e7f7e.jpg" width="30px"><span>silent</span> 👍（2） 💬（0）<div>国内互联网公司，所有人时间都很紧张，没有时间做cr。当然，根本原因是不重视，毕竟谁代码不行裁掉换一个就好了，不用花时间帮助他提升自己。本质上还是把人当人肉干电池用hhh</div>2020-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/02/6a16058a.jpg" width="30px"><span>liu_liu</span> 👍（2） 💬（0）<div>1. 没有切身体验到 code review 的好处，大多是流于形式的过一遍，或者根本没有。
2. 觉得是种负担，浪费时间。没有把它作为一种可以提高代码质量，发现隐藏问题的方式。
3. 目前我们的 code review 也只是检查些较明显出错的地方，并不细致。
4. 需要对 code review 有丰富经验的人从小范围开始推广，并见到实效，进而逐步铺开。</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（2） 💬（0）<div>我觉得code review好处之一就是帮助部分同学提高编码技能；毕竟工作不像在学校，写的不好的同学老师会手把手教你，code review让大家看到优秀的，也看到槽糕的</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/91/bc/2f338491.jpg" width="30px"><span>long</span> 👍（1） 💬（0）<div>咨询一个问题，是在dev分支还是feature分支做，如过在开发分支做，是不是因为每天提交的过于频繁，并且缺乏逻辑整体性，导致cr效果不理想。</div>2021-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/6b/0b6cd39a.jpg" width="30px"><span>朱月俊</span> 👍（1） 💬（0）<div>我认为有两个原因吧，至于&quot;碍于面子&quot;这种解释有一点站不住脚。
原因一，国内做事比较急躁，只做跟kpi或者okr有直接关系的事，而cr表面上还是阻止功能上线的一个拦路虎，甚至怀疑同事会故意找麻烦，第一印象认为别人是坏的。我印象，脸书有一个价值观，think good.
原因二，老大们只关心业务价值，并且一个团队的寿命比较短，可能3年左右就大换血，老大们才不会去做没有长久的事情。</div>2020-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/42/3e/edb93e8c.jpg" width="30px"><span>青山</span> 👍（1） 💬（0）<div>code review 在17年接触到的，当时写的代码也是什么都没考虑，只要能运行就行。当我第一次提交代码时，说了我代码很多问题，当时我觉得为什么要在意这么多小细节，leader是不是故意刁难我，在一次次的code review中，渐渐的我的思想被改变了，发现以前写的代码是如此的粗糙，让我明白写代码不仅仅是有手就行，感谢当年给我带来code review思想的导师。</div>2020-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/98/cd/d85c6361.jpg" width="30px"><span>丹枫无迹</span> 👍（1） 💬（0）<div>确实，最主要的问题是没有会 Code Review 的人带，不知道怎么去开展。如果完全靠自己摸索，那进展就会缓慢，迟迟不出效果，即便老板一开始是支持的，后面也会开始怀疑，最后可能就是不了了之。</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/b6/abdebdeb.jpg" width="30px"><span>Michael</span> 👍（1） 💬（0）<div>我司这方面做的还可以</div>2020-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/69/187b9968.jpg" width="30px"><span>南山</span> 👍（1） 💬（0）<div>现在所在的团队不做cr，不准提测，也一直在强调cr的重要性，做cr的时候也很认真，挺好，以后自己有话语权一样这么干~</div>2020-06-25</li><br/>
</ul>