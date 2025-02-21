你好，我是柳胜。

上一讲，我们学习了单元测试，在验证业务逻辑方面，它的优势在于速度又快，阶段又早。既然单元测试看起来是一个完美的自动化测试方案，那为什么还需要集成测试呢？

我在[第二讲](https://time.geekbang.org/column/article/497405)的3KU原则说过，测试需求首先要找ROI最高的截面来验证。在金字塔模型里，ROI最高的就是单元测试，如果无法实现，才回退到ROI第二高的截面，一直到ROI最低的端到端测试。

那集成测试存在的价值，一定是做得了单元测试层面做不到的事，否则，集成测试这个概念就没必要存在。那这些事具体有哪些呢？你要是能找到这些事，就找到了集成测试省力又见效的窍门。今天咱们就一起寻找这个答案。

## 集成测试和单元测试

上一讲我们学过了代码四象限法则，产品的代码按照业务相关性和依赖程度，可以划分到下面四个象限里。

![图片](https://static001.geekbang.org/resource/image/53/cb/538461c119ff8ac736750f27ea60a7cb.jpg?wh=1920x1501)

那集成测试和单元测试分别应该归到第几象限呢？

集成测试，顾名思义，是验证本服务代码和其他进程的服务能不能一起配合工作。在上面的四象限里，集成测试的活动领域就在“依赖代码”象限，而单元测试的活动领域是在“领域代码”象限。

我再用图解的方式划分一下地盘，你会看得更清楚。

![图片](https://static001.geekbang.org/resource/image/3f/45/3f6fc585e1af8bc0a110c83776781045.jpg?wh=1920x1203)

这张图里的信息量很大，展示了单元测试和集成测试的各自战场，我来跟你细说一下。

单元测试掌管领域代码的测试，这些领域代码只是负责数据计算，并不会触及外部依赖。像上一讲的changeEmail方法，只是计算出一个新的餐馆数目，单元测试只需要验证这个计算逻辑是否正确就好了。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/c3/a9/aa5a5d8b.jpg" width="30px"><span>朝如青丝暮成雪</span> 👍（4） 💬（1）<div>老师有推荐的单元测试练手的项目嘛？看完文档觉得自己好像会了，但是实际上手可能差点意思</div>2022-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/e4/94b543c3.jpg" width="30px"><span>swordman</span> 👍（1） 💬（1）<div>找到Happy Path，除了看代码以外，我想到的一个办法，是通过覆盖率把Happy path找出来。把这些测试案例都执行一遍，看依赖代码类的覆盖情况，如果能一个或几个的组合，能覆盖到所有的外部依赖交互点，就找到了Happy path。</div>2022-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bd/65/fbdf4fc1.jpg" width="30px"><span>羊羊</span> 👍（0） 💬（1）<div>想问下老师，为什么测试用例需要“5. 检验 Mock 的 MessageBus 里的消息”？Moke 的 MessageBus 需要实现SendEmailChangedMessage的功能么？还是只需要按照 IMessageBus 中的定义返回期望结果？</div>2022-07-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLw3jpao45frZibQIAicWBfc7ofgrm5gJLiaFQSj5u2DDvkjy3ia5goicJLJlgVtZ0HryiaXb2VqpTSQT5Q/132" width="30px"><span>lisa</span> 👍（0） 💬（1）<div>我理解完全可控依赖和不完全可控依赖不是一个推荐策略或者二选一策略，他是一个组合策略。这个组合也是有技巧的，需要建立在对不完全可控依赖的对象的逻辑理解上吧？</div>2022-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-02-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqE0GaxHXGoJbWk2F2cYoClmwyulCzUgqMj9u3xzBfEkqLRfvd08o1Fd9WMAfJFHUKU6hhjEDSCGQ/132" width="30px"><span>Geek_2f2844</span> 👍（0） 💬（0）<div>老师您本章只讲了单元测试、集成测试和UI测试，没有讲到接口测试，是因为这块对测试来说最熟悉么。不过我理解集成测试也算是接口测试的一种吧，主要关注与外部服务交互的接口测试</div>2022-09-05</li><br/>
</ul>