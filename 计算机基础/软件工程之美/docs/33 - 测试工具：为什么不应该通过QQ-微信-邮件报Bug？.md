你好，我是宝玉。十多年前，当我还是个野路子程序员时，我在外面接私活做项目，客户在使用过程中遇到了Bug，直接就截个图，或者是用Word文档整理在一起，从QQ或者邮件上把Bug信息发送给我，我收到后再修复更新上线。

而现在正规的软件项目已经不会再用这种原始的方式来报Bug了，而是会借助测试工具来帮助报告和跟踪Bug，即使你偶尔能看到有项目还在采用原始方式报Bug，你肯定也会觉得这样做不专业。

但不知道你有没有仔细想过这个问题，为什么现在不通过QQ/微信/邮件报Bug，又有哪些测试工具可以帮助你更好地发现、报告和跟踪软件中的Bug呢？今天我们来展开讨论这个问题。

## Bug跟踪工具

我想你对于Bug这个词一定不陌生，它是我们软件中的缺陷或错误。这个词的诞生也很有意思。

> 1947年9月9日，一只小飞蛾钻进了哈佛大学的一台计算机电路里，导致系统无法工作，操作员把飞蛾贴在计算机日志上，写下了“首个发现Bug的实际案例”。

[![](https://static001.geekbang.org/resource/image/79/3c/796010fd083207b660547887bbc5893c.png?wh=740%2A583 "图片来源：WikiPedia")](http://en.wikipedia.org/wiki/Software_bug)

虽然Bug的历史已经有60多年了，然而Bug跟踪工具却没有出现太久。软件项目中最早也是通过邮件、即时通讯等原始方式报告Bug，直到1992年才有第一个专业的Bug跟踪软件[GNATS](http://www.gnu.org/software/gnats/)。

在这之后才逐步有了像Bugzilla、Jira、MantisBT等专业的Bug跟踪工具。而现在，Bug跟踪工具已经成为软件项目中必不可少的工具之一。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/76/93/c78a132a.jpg" width="30px"><span>果然如此</span> 👍（9） 💬（1）<div>对于自动化测试一直有些疑问，如果每次发布都对所有方法自动化测试：
1. 一定会耗费很多时间；
2. 数据库产生很多测试历史数据；
3. 写测试用例能达到覆盖率高的写代码技巧，如边界测试代码、幂等测试代码如何实现。</div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/04/ec/0539c89d.jpg" width="30px"><span>易林林</span> 👍（8） 💬（1）<div>在集中办公的时候，很多人喜欢用微信&#47;QQ去聊工作上的事情，一会儿@这个，一会儿@那个，一些重要的信息很快就被淹没了，很难去挑出对自己有用的信息。对于这种情况，我一般很少去理会别人发了什么信息，也不会随时在电脑上开着微信&#47;QQ等着闪亮的出现，要么通过各种管理工具沟通（邮件、Bugfree、Jira等等），要么当面或电话沟通，这样问题才能得到有效的、高效的解决。但在这样做之前，我会在合适的场合说出这样做的原因和相应的解决办法，避免让他人误解。</div>2019-05-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoOGZ6lbHiboIZMN9USbeutnmCWBahVLtSlKlIENKvrZQCUQzpzeZQOxTntIkBUeDk6qZUPdqmfKrQ/132" width="30px"><span>宝宝太喜欢极客时间了</span> 👍（4） 💬（1）<div>老师，对测试这块一直很疑惑，测试脚本、测试用例、测试数据这三者如何配合一起通过CI进行自动化测试？</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/eb/20492a37.jpg" width="30px"><span>一路向北</span> 👍（3） 💬（1）<div>用qq和微信等作为bug管理，与其说是用它来做管理，不如说是用它做驱动。很多问题是在客户那边发现，因此他们第一反馈就是即时通讯工具反馈，我们也就根据这个来解决bug问题。
对于小公司（10来个人）来说，管理一套系统和维护一个流程，总觉得需要付出比较大的代价，是不是这样呢？以前试过禅道，用了一段时间之后也放弃了。需要专门的人员来维护推动。
</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/02/db/e86294b7.jpg" width="30px"><span>谢禾急文</span> 👍（2） 💬（1）<div>看到这篇文章，我想到了我之前的一个想法，就是通过用一个工具记录我自己开发过程中遇到的所有bug，通过记录、分析、反思这些bug，能够有助于提升我的编程能力，有助于避免犯同样的错误。我觉得你上面说的那些工具，能够满足我的需求。如果有一个网站，能够提供bug记录、分享、解答的工能，是不是能够满足某些用户的需求(好像stackoverflow就是这样的工具)。</div>2019-06-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoOGZ6lbHiboIZMN9USbeutnmCWBahVLtSlKlIENKvrZQCUQzpzeZQOxTntIkBUeDk6qZUPdqmfKrQ/132" width="30px"><span>宝宝太喜欢极客时间了</span> 👍（2） 💬（2）<div>老师，测试用例英文test case为什么叫测试用例而不叫测试例呢？有没有test use case一说？</div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/65/55/274df2e8.jpg" width="30px"><span>邢爱明</span> 👍（2） 💬（1）<div>自动化测试，个人理解最大的困难是开发人员的心理和认知，理解测试工作不只是测试人员的职责，开发人员应对软件的交付质量负起更大的职责。</div>2019-05-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/m2baiaoDn4II6piarRCeVK4JGah8gzF0m9J6r35xDTEMUUaUrzf23jhRa0aicTeUXDv29ZkicicaI44Fhfn6NrSeHiaQ/132" width="30px"><span>calvins</span> 👍（1） 💬（1）<div>受教了，很多测试都明白，就是没有执行力，这篇分享了很多测试相关工具，很nice，可以更多的了解，丰富知识广度。</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（1） 💬（2）<div>1、软件测试不仅仅是发现Bug，另外更重要的是预防Bug，还有为领导者作决策。2、DevOps 中测试还可以左移(预防)和右移(在生产环境中测试)。3、测试工具不是银弹，作为一名优秀的测试工程师，主力应该在分析与设计测试用例。</div>2019-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/37/02/84c544b2.jpg" width="30px"><span>geek_sunpiaoliang</span> 👍（1） 💬（2）<div>目前java  主流的测试工具有哪些，比较稳定的，测试web及测试接口</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/15/11/abb7bfe3.jpg" width="30px"><span>成</span> 👍（1） 💬（1）<div>服务端通过编写单元测试没啥问题，app方面好像少不了人工测试，现在测试人员主要覆盖app测试，并且每个迭代测试时间比较长，上线后问题还不少。app测试如何更好引入自动化测试？</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/54/ef/3cdfd916.jpg" width="30px"><span>yu</span> 👍（1） 💬（1）<div>程式碼就像程序員的名片，要對寫出來的代碼負責，最好的負責方式就是寫測試代碼，讓每次代碼變動，都不會影響到其他代碼的運行，避免所謂的改 A 壞 B，節省迂迴的時間浪費。也為 CI&#47;CD 做好準備，無論目前有沒有。

程序員不想寫測試在我們公司的原因大多是，不知道怎麼開始寫，不知道重點應該測試什麼。先寫測試的開發模式讓他們覺得不習慣，但這些都是過程，培養良好的撰寫測試代碼習慣後，開發品質更有保證，提升開發效率，提升個人能力，我想都是有幫助的。

程序難免有 Bug ，透過追蹤軟件，良好的管控 Bug 數量與修復進度，並且補足測試。</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>如果想要最大化工具的价值，及时发现问题，还要考虑将测试工具的应用自动化，加入到你的持续集成流程中去。--记下来</div>2022-07-04</li><br/>
</ul>