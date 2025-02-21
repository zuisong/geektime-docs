你好，我是柳胜。

上一讲，我们分析了传统自动化测试设计态和运行态存在的鸿沟，并且提出了一个更科学的Job模型的设想。如下图所示，这个模型包含七个核心属性，其实也是后续在设计自动化测试案例时，我们需要考虑的七个方面，也是后续开发中要去实现的Interface（接口）。

模型属性我们上一讲开了个头，重点讲了Dependency和TestData，Dependency描述业务关联性、阻断错误、缩短执行时间，TestData可以实现一份代码多组数据运行，提升自动化测试的ROI。

今天咱们继续分析剩下的模型属性，勾勒整个Job模型的全貌，这样你就能进一步掌握自动化测试设计建模的利器了。

![图片](https://static001.geekbang.org/resource/image/b7/59/b7b0596e823yya466ff87373b205e359.jpg?wh=1920x1310)

## 模型属性

自动化测试有一个令人头疼的问题——不稳定，经常失败，有没有办法通过设计攻克这个难题呢？

自动化测试Job像开发的微服务一样，都是独立的运行单元，我们可以通过给每个Job增加一个**TestConfig**，它的数据表达类型是HashMap，每一条记录代表一个配置，我们通过修改配置来控制Job的运行。结合实践，**有三个关键配置，可以增强自动化测试的健壮性和诊断性，分别是：日志级别、超时时间以及重试次数**。

Log是诊断程序运行问题最有力的工具，自动化测试也不例外，通过定义不同的log级别和相应输出信息，把它应用在不同环境下，可以形成一个自动化测试诊断策略。比如，Log level 如果是debug级别，抓取环境信息、屏幕截图、运行时堆栈，用于在自动化测试开发阶段做调试。Error级别记录出错trace和调用Job链状态，用在自动化测试生产运行环境。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1a/78/a5/5c1e285e.jpg" width="30px"><span>Hedy</span> 👍（2） 💬（1）<div>API测试和UI自动化是如何聚合呢 好奇 😯</div>2022-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bd/65/fbdf4fc1.jpg" width="30px"><span>羊羊</span> 👍（1） 💬（1）<div>API测试和UI自动化聚合是不是就是前面讲到的“皮下测试”？例如需要测试用户的VIP的状态改变，使用API去更改用户状态，因为要等到用户VIP过期是不现实的，然后用UI层面测试检查在UI层面用户的状态是不是正确变化。
个人理解，测试Job模型是设计模式“依赖倒置”原则在测试设计中的体现。</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4a/57/3f68946c.jpg" width="30px"><span>On</span> 👍（1） 💬（1）<div>老师，大数据项目的测试，有哪些更适合大数据特点的优秀的工具&#47;框架？
本节所讲的微测试 Job 模型是否同样适用于大数据项目的软件测试？谢谢老师。</div>2022-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4a/57/3f68946c.jpg" width="30px"><span>On</span> 👍（1） 💬（1）<div>老师，目前这个微测试 Job 模型有已经落地实现、稳定运行的框架或工具吗？</div>2022-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c2/c6/88d0c7b2.jpg" width="30px"><span>一默</span> 👍（0） 💬（1）<div>老师，我感觉，现在定义的这些就像是面向对象的一个变种。而job就是类。就是在把软件开发的概念引入到软件测试中，把测试做为一个系统在设计和实现。不知道我理解的对不对。请老师指教。谢谢</div>2022-05-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLw3jpao45frZibQIAicWBfc7ofgrm5gJLiaFQSj5u2DDvkjy3ia5goicJLJlgVtZ0HryiaXb2VqpTSQT5Q/132" width="30px"><span>lisa</span> 👍（0） 💬（1）<div>testData和input的数据结构有什么区别？</div>2022-05-05</li><br/><li><img src="" width="30px"><span>woJA1wCgAA3aj6p1ELWENTCq8KX2zC2w</span> 👍（0） 💬（1）<div>我们的平台设计跟老师说的吻合呢</div>2022-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/4b/be/72f099ae.jpg" width="30px"><span>发现生活的美好</span> 👍（0） 💬（0）<div>使用Job模型构建出来的自动化项目 一般用在什么场景下呢？</div>2022-11-03</li><br/>
</ul>