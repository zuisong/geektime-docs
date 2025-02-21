不知不觉，我已经介绍完了GUI测试相关的知识点，你可以先回顾一下这些知识点，是否还有不清楚的地方，也欢迎你给我留言进行讨论。同时，我希望这些知识点，已经帮你搭建了GUI自动化测试的知识体系。

那么，今天我将从实际工程应用的角度，和你一起聊聊GUI测试的稳定性问题。

如果你所在的公司已经规模化地开展了GUI测试，那我相信你们也一定遇到过测试稳定性的问题。**GUI自动化测试稳定性，最典型的表现形式就是，同样的测试用例在同样的环境上，时而测试通过，时而测试失败。** 这也是影响GUI测试健康发展的一个重要障碍，严重降低了GUI测试的可信性。

所以，今天我分享的主题就是，如何提高GUI测试的稳定性。虽然从理论上来讲，GUI测试有可能做到100%稳定，但在实际项目中，这是一个几乎无法达到的目标。根据我的经验，如果能够做到95%以上的稳定性，就已经非常不错了。

要提高GUI测试稳定性，首先你需要知道到底是什么原因引起的不稳定。你必须找出尽可能多的不稳定因素，然后找到每一类不稳定因素对应的解决方案。

为此，根据我的实践经验，以及所遇到的场景，我为你总结了五种造成GUI测试不稳定的因素：

1. 非预计的弹出对话框；
2. 页面控件属性的细微变化；
3. 被测系统的A/B测试；
4. 随机的页面延迟造成控件识别失败；
5. 测试数据问题。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/95/4544d905.jpg" width="30px"><span>sylan215</span> 👍（57） 💬（4）<div>1. 非预期弹框：
对于非预期的弹框也可以通过检查置顶窗口是否是预期软件窗口，从而确定是否被第三方弹框影响。
2. 页面控件变化：
如果是 selenium 的话，建议优先使用 xpath，这样就算 id、clases、name 等控件属性改变，只有不是页面改版，应该不会影响自动化稳定性。
3. A&#47;B 测试页面：
判断当前页面属于哪个分支，然后走兼任处理逻辑，同意这个方案。其实很多地方都可以通过类似的兼容方案进行处理，比如第一个非预期弹框，也可以算是异常场景的兼容处理。
4. 页面延迟：
重试机制确实是个好办法，但是如果用例都是因为重试才执行正确，有可能会漏出和缓存相关的问题，因为重试应该算一个独立测试场景了，现在是把它作为主要测试场景了。
这地方我记得 selenium 有一个函数可以设定一个最大超时时间，在这个时间之前都会等待，一旦超时时间内满足了继续执行的条件，也可以立刻执行，这个方法还是比较不错的，既保证了用例操作的预期性，也解决了延迟的不可控的问题。
5. 测试数据问题：
构造自动化数据时要特别注意，构造一些带特殊字段的数据库信息，最好是超出常人操作的数据信息，这样可以有效避免数据被误修改的风险，当然，还有一个处理办法在 15 讲的时候提到过，就是先检查测试数据是否存在&#47;异常，不存在或异常都进行重建即可，这部分也算是测试代码的兼容处理吧。
以上，欢迎沟通交流，公众号「sylan215」</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/55/b3ab84a2.jpg" width="30px"><span>张红占</span> 👍（2） 💬（1）<div>能否通过实例讲解 总结的有点high level</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c2/a7/c4de1048.jpg" width="30px"><span>涅槃Ls</span> 👍（0） 💬（1）<div>打卡17</div>2018-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/44/c2d77269.jpg" width="30px"><span>hi ！girl</span> 👍（0） 💬（1）<div>老师，步骤级别、页面级别和业务流程级别的重试机制可以给一个实例吗</div>2018-08-06</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eppQqDE6TNibvr3DNdxG323AruicIgWo5DpVr6U7yZVNkbF2rKluyDfhdpgAEcYEOZTAnbrMdTzFkUw/0" width="30px"><span>图·美克尔</span> 👍（0） 💬（1）<div>异常场景恢复模式是将在整个操作过程外加try catch实现的吗？</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c7/c6/35cc7c7c.jpg" width="30px"><span>Robert小七</span> 👍（0） 💬（1）<div>异常恢复场景是否包含了重试机智？如何解决定位失败后可能产生的无限重试？</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c2/b8/ec758482.jpg" width="30px"><span>Cynthia🌸</span> 👍（13） 💬（1）<div>页面延迟那个，具体表现应该就是找不到元素吧，那么等一等是不是就可以找到了？
我记得selenium里面有等待函数，而且还可以用sleep。
之前做过的项目，最早没有加等待，就经常因为不稳定而报错，加上等待之后这种概率少多了</div>2018-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dc/33/a68c6b26.jpg" width="30px"><span>捷后愚生</span> 👍（7） 💬（0）<div>老师全面总结了GUI测试稳定性的种种问题，如果在面试过程中被问到“你是如何应对GUI自动化测试不稳定问题”时，根据老师这篇文章回到，底气十足。

学习到老师的解决问题的思路，一是遇到问题，不是马上就想着具体怎么解决，而是先分析出现问题的原因。如在面试中。被问到“你是如何应对GUI自动化测试不稳定问题”时，你直接给出几条解决措施，看上去已经回到了面试官的问题，但是如果你能用先分析问题原因，再给出解决方案，给人的感觉思维缜密。二是遇到需要机器解决的问题，想想如果人工去解决、去操作是怎么做的，是不是有可借鉴的地方。

因为网络原因，页面元素出现的时间长短不同，在代码层面，加入等待机制，也是解决稳定性问题的一个方法。</div>2020-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/4a/20/2dbdb6d9.jpg" width="30px"><span>why</span> 👍（3） 💬（0）<div>感谢，我知道面试中，面试官问我解决过什么问题，我答什么了。</div>2020-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/26/154f9578.jpg" width="30px"><span>口水窝</span> 👍（2） 💬（0）<div>网络不稳定，无线与流量切换，浏览器版本升级等造成GUI测试不稳定。</div>2019-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dc/33/a68c6b26.jpg" width="30px"><span>捷后愚生</span> 👍（1） 💬（0）<div>看同学们的留言，非常优秀。
本来以为老师的文章已经很全面，看留言还是有另外的补充，赞！</div>2020-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/57/c3/58582b99.jpg" width="30px"><span>Cassie</span> 👍（1） 💬（0）<div>我们的软件产品用到了eclipse，也会跟着eclipse的升级而升级，当然频率会低一些。但由于eclipse升级，我们用QFT开发的自动化测试脚本常常不能运行，主要是新版本中的component发生了变化，必须adapt脚本来识别新的component才行。这块的工作量有时候会很大，改脚本改得很痛苦。请问茹老师有没有什么解决&#47;缓解的办法？谢谢！</div>2020-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3e/45/3879f334.jpg" width="30px"><span>Tron</span> 👍（1） 💬（0）<div>Robotframework中的Wait until xxx timeout=30s其实也是用的重试模式</div>2019-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d0/5d/9f9d73fe.jpg" width="30px"><span>文大头</span> 👍（1） 💬（0）<div>我遇到的更多的不稳定，大多是开发对页面做了修改，特别是页面框架的改动，导致元素定位失败。为此，定位元素时尽可能使用元素的相对位置，而不是绝对的xpath路径定位，xpath中也选取相对稳定的元素属性定位，另外xpath本身也支持模糊匹配，我很少需要单独写模糊匹配的代码。
针对延时问题，除了前面留言说的硬等到超时报错外，可以观察是否有其他元素在正常情况下是跟被测元素一起出现的，如果有，就检测那个元素出现了，被测元素是否也出现，没有就直接报错；检测元素消失也类似。</div>2018-08-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/FGeCDgpXdhsXseIGF3GCzZibDJlOfO4KDqPJkMra2e0TJj3QVQk4t1oEd1BuQPtYOeavFyYxicd5fTZ33tIbPOZQ/132" width="30px"><span>付晓杰</span> 👍（0） 💬（0）<div>五种造成 GUI 测试不稳定的因素：
（1）非预计的弹出对话框；
可以引入“异常场景恢复模式”来解决
（2）页面控件属性的细微变化；
可以使用“组合属性”定位控件，并且可以通过“模糊匹配技术”提高定位识别率。
（3）被测系统的 A&#47;B 测试；
需要在测试用例脚本中做分支处理，并且需要脚本做到正确识别出不同的分支。
（4）随机的页面延迟造成控件识别失败；
可以引入重试机制，重试可以是步骤级别的，也可以是页面级别的，甚至是业务流程级别的。
（5）测试数据问题。</div>2022-09-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/FGeCDgpXdhsXseIGF3GCzZibDJlOfO4KDqPJkMra2e0TJj3QVQk4t1oEd1BuQPtYOeavFyYxicd5fTZ33tIbPOZQ/132" width="30px"><span>付晓杰</span> 👍（0） 💬（0）<div>五种造成 GUI 测试不稳定的因素：
1.非预计的弹出对话框；
       1)GUI 自动化测试用例执行过程中，操作系统弹出的非预计对话框
       2)被测软件本身也有可能在非预期的时间弹出预期的对话框
2.页面控件属性的细微变化；
3.被测系统的 A&#47;B 测试；
4.随机的页面延迟造成控件识别失败；
5.测试数据问题。</div>2022-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/ec/00/4ce96190.jpg" width="30px"><span>豆豆</span> 👍（0） 💬（0）<div>新手，不知道怎么找出不稳定因素原因。debug大部分时候可以通过，运行的话偶尔能通过。麻了。定位到了代码片段，打开了网页，看不出原因。是一个被div包着的span，说span不可点击。是用模糊匹配采集的xpath。代码不是我写的，我只是针对一些页面元素的属性值和标签变化修改一下。最后生成了一份顺利运行的报告不了了之了。不知道怎么才能找到原因。</div>2021-06-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJibdOKYcFAlp3UKuITmtFMx95Qg9ficIDmCBlk14XHnljX9ias4MiauwGv3vsNrVksUlwT95J13lzK0w/132" width="30px"><span>小寒Edwin</span> 👍（0） 💬（0）<div>老师好，步骤级别的的不稳定，这块的retry大概是怎么的一个实现思路呢？</div>2019-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（0）<div>对于非预计的弹出对话框引起的不稳定，可以引入“异常场景恢复模式”来解决。
问：如何作到随时捕获异常？比如用Java或python 

对于页面控件属性的细微变化造成的不稳定，可以使用“组合属性”定位控件，并且可以通过“模糊匹配技术”提高定位识别率。
需要二次开发

对于 A&#47;B 测试带来的不稳定，需要在测试用例脚本中做分支处理，并且需要脚本做到正确识别出不同的分支。
需要辨别A版本或B版本

对于随机的页面延迟造成的不稳定，可以引入重试机制，重试可以是步骤级别的，也可以是页面级别的，甚至是业务流程级别的。
问：如何看待selenium 中的显示等待或隐式等待，但也要有个等待时间限制。

对于测试数据引起的不稳定，我在这里没有详细展开，留到后续的测试数据准备系列文章中做专门介绍。

还有一种不稳定是上一个测试用例执行失败，没有把测试环境恢复。</div>2018-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e6/eb/68828786.jpg" width="30px"><span>彼端宓悦</span> 👍（0） 💬（0）<div>关于 webdriver 中的二维码登录测试，有什么可行的解决思路吗？</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fb/59/3b19413b.jpg" width="30px"><span>张荣山</span> 👍（0） 💬（0）<div>针对控件的定位，模糊匹配是否会影响整个脚本的运行时间和效率？如何抓取显示时间短的控件并做即时响应感觉会更难。</div>2018-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/43/f9/555d7aa0.jpg" width="30px"><span>人心向善</span> 👍（0） 💬（0）<div>稳定性测试真的让人头疼说心惊胆战一点不为过，举个例子：业务需求要求完成7*24小时的稳定性，跑到尾声的时候发现大量报错且准确率已经不足95%的比例，这种时候是最痛苦的，重新跑吧前面的5.6天就白进行了，不重跑吧，不能保证最终的测试结果，而且还有好多非自然因素，断网或断网环境莫名挂掉，这些都会让稳定性测试猝不及防，顺利的话周期会很短，不顺利的话就很难说要取决的因素太多了……</div>2018-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/3e/82202cc8.jpg" width="30px"><span>月亮和六便士</span> 👍（0） 💬（0）<div>老师每天都期待讲一个高大上的接口测试框架，或者接口测试框架设计思路。</div>2018-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/44/c2d77269.jpg" width="30px"><span>hi ！girl</span> 👍（0） 💬（0）<div>对于第四点，通常需要延迟的主要是涉及网络请求的页面，能否先给出一个合理的动态时间等待，后选择重试呢</div>2018-08-06</li><br/>
</ul>