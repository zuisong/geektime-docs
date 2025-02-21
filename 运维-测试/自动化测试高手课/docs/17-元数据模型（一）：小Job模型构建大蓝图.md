你好，我是柳胜。

在价值篇我们学习了3KU整体最优分层模型。而到了策略篇，又结合一个具体的订餐系统，为你提供了一个测试设计实现案例，演示具体如何应用3KU法则。

不过推演下来，你有没有隐约感觉到，事情有点不对劲了？以前我们是先分层，再在每个层上设计自己的TestCase，UI上的TestCase的功能定义和粒度大小，可能和API层上的TestCase完全不一样。

现在，不同的测试需求，可能会落到不同的分层截面上去做自动化。甚至，一个测试需求的不同部分，也可以放在不同截面上。比如，你可以在API上测试createOrder，在UI上测试verifyOrder，只要这样做ROI最高。

所以，在3KU法则下，自动化测试设计是先定义TestCase，然后再判断它应该落在哪个层面。这跟我们以往熟悉的自动化测试设计大相径庭，需要我们在设计方法论上有新的突破。没错，现在我们的挑战是，需要找到一种新的概念指导我们做任务建模和设计，从而跨越各层的“TestCase”。

因为内容比较多，为了让你跟得上，我安排了两讲内容，带你**找到一个测试设计的元数据模型，将各种类型和层次的测试纳入到这同一个模型里。一生二，二生三，三生万物，从这一个模型里，衍生出我们自动化测试中所需要的设计方法和策略、执行计划，效益度量甚至生死定夺等等一切**。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/bd/65/fbdf4fc1.jpg" width="30px"><span>羊羊</span> 👍（3） 💬（1）<div>以前在传统软件公司做自动化的时候，在testcase 管理系统中，设置了自动化选项，如果这个设置为 true。就需要制定一个自动化测试的配置文件的 p4 地址，是一个xml文件。也就是一个配置文件，其中包含了这个自动化测试用例 runner，参数等。用测试平台的 rest api，把这个xml文件和使用的硬件信息，作为 data 参数，发送一个post请求，测试平台会在返回一个url。打开这个url，能看到这个自动化测试的执行情况。
但是自动化测试和手工测试的用例，在描述标准上没有统一。想知道老师的公司是如何管理测试用例的？</div>2022-08-01</li><br/><li><img src="" width="30px"><span>woJA1wCgAA3aj6p1ELWENTCq8KX2zC2w</span> 👍（1） 💬（1）<div>我们不光有前置，还有后置并配合数据库做数据恢复。</div>2022-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（1）<div>自动化测试和手工测试共用一套案例模型和设计方法。TestSuite 和 TestCase 这些概念已经过时了，需要找到新的模型。2. 自动化测试设计本质是软件设计，精髓在于对测试场景的抽象和建模。这就像开发软件先设计 Interface 一样，而自动化测试工具和框架属于实现层面，用哪个取决于需求，而不能削足适履。</div>2022-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/e4/94b543c3.jpg" width="30px"><span>swordman</span> 👍（0） 💬（1）<div>自动化测试 Job这个提法，首次看到，非常感兴趣！我去年学习了《高效自动化测试平台设计与开发实战》，里面将自动化测试平台，抽象成测试资源，测试配置，测试报告和日志，测试用例执行四个部分。但没有脱离TestSuite 和 TestCase模型，因此没有Dependency部分。看完那本书后，我有一个疑惑：不同的TestCase，可能是用多种语言或多种测试框架开发的，如何将多种语言的TestCase整合在一起，让它们可以协同工作呢？希望Job模型，能够给我一个解决思路。</div>2022-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/7e/62/48045bee.jpg" width="30px"><span>Sarah</span> 👍（0） 💬（1）<div>期待下一讲！
在实际项目中，设计用例时Input Output Data都已完善，DAO有做但不够可以继续完善，缺少Dependency 部分，感觉这个思路非常有用，目前团队面临的问题就是，测试案例设计方法论逐渐完善，自动化实现也逐步跟上，做到跟测试案例匹配，但是执行时间过长，失败率较高。完善DAO加入Dependency 或许可以解决一部分问题</div>2022-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/5d/71/4f6aad17.jpg" width="30px"><span>Sophia-百鑫</span> 👍（0） 💬（0）<div>写测试案例会有precondition，即前置依赖。就是老师提到的dependency，使用dependency更有系统或代码设计的味道。老师分享的很棒。请问如何加入自动化测试高手微信群？非常感谢</div>2023-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/ae/246a031b.jpg" width="30px"><span>格</span> 👍（0） 💬（0）<div>醍醐灌顶，谢谢🙏</div>2022-10-25</li><br/>
</ul>