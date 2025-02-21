你好，我是郑晔！

经过前面内容的讲解，我终于把软件设计的基础知识交付给你了，如果你有一定的经验，相信有很多东西你已经可以借鉴到日常工作中了。

但是对于一些同学来说，这些知识恐怕还是有些抽象。那在接下来的几讲中，我会给你讲几个例子，让你看看如何在日常的工作中，运用学到的这些知识，巩固一下前面所学。

我在[第9讲](https://time.geekbang.org/column/article/245878)说过，学习软件设计，可以从写程序库开始。所以，我们的巩固篇就从一个程序库开讲。这是我自己维护的一个开源项目 [Moco](https://github.com/dreamhead/moco)，它曾经获得 2013 年的 Oracle Duke 选择奖。

Moco 是用来做模拟服务器的，你既可以把它当作一个程序库用在自动化测试里，也可以把它单独部署，做一个独立的服务器。我们先来看一个用 Moco 写的测试，感受一下它的简单吧！

```
public void should_return_expected_response() {
  // 设置模拟服务器的信息
  // 设置服务器访问的端口
  HttpServer server = httpServer(12306);
  // 访问/foo 这个 URI 时，返回 bar
  server.request(by(uri("/foo"))).response("bar"); 
  
  // 开始执行测试
  running(server, new Runnable() {
    // 这里用了 Apache HTTP库访问模拟服务器，实际上，可以使用你的真实项目
    Content content = Request.Get("http://localhost:12306/foo")
      .execute()
      .returnContent();
      
    // 对结果进行断言
    assertThat(content.asString(), is("bar"));
  });
}
```

这一讲，我就来说说它的设计过程，让你看看一个程序库是如何诞生以及成长的。

## 集成的问题

不知道你有没有发现，阻碍一个人写出一个程序库的，往往是第一步，也就是**要实现一个什么样的程序库**。因为对于很多人来说，能想到的程序库，别人都写了，再造一个轮子意义并不大。

但是，这种思路往往是站在理解结果的角度。其实，**程序库和所有的应用一样，都是从一个要解决的问题出发。**所以，在日常的繁忙工作中，我们需要偶尔抬头，想想哪些问题正困扰着我们，也许这就是一个程序库或者一个工具的出发点。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/fe/fa/2a046821.jpg" width="30px"><span>人间四月天</span> 👍（13） 💬（1）<div>真的很精辟，开发工作是很讲究套路的，从问题，需求，方案，设计，发现问题很关键，太多开发，眼睛里看不到问题，重复开发，功能不复用，不扩展，性能差，开发效率慢，系统质量低，工作中有太多的痛点，痛点即是问题，不追求问题本质，不勤于思考的开发，就是推代码，能跑就行，不管后续维护。如果发现不了问题，更谈不上解决问题，解决方案和设计，就是解决问题，需要积累经验，不断学习，实践，提升解决问题的能力，只有把发现问题和解决问题都做好的开发，才能成为架构师或者leader，更上一层楼。</div>2020-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2f/c5/55832856.jpg" width="30px"><span>Edison Zhou</span> 👍（6） 💬（1）<div>老师这篇的讲解方式很像是一个TDD的案例，先从一个最基本的测试入手，它代表了一个最小化的核心模型，剩下的就是不断的迭代地去实现它并让测试通过。在不断地迭代中，让测试通过的同时，也在不断地进行重构，“抽丝剥茧”+“分离关注点”，最后形成一个好的设计。</div>2021-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a0/a3/8da99bb0.jpg" width="30px"><span>业余爱好者</span> 👍（4） 💬（1）<div>记得不错的话，spring mvc test里面也有相似的概念，如RequestMatcher，ResponseHandler,今天才明白原来这是一种函数式编程的dsl。moco已clone,学习一下</div>2020-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/24/c6b763b4.jpg" width="30px"><span>桃子-夏勇杰</span> 👍（1） 💬（1）<div>郑大大，很好奇你的moco，也粗略地看了几次。有时间的时候，是否可以来个mock server的竞品分析</div>2020-11-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLsia5hqVlTLn17lUBwSpSUzraib7MSH3gOUNWOx8qUwpz3Lp6gFtkIibOMUAouyMGj5RIeTcePUfNkw/132" width="30px"><span>jg4igianshu</span> 👍（11） 💬（0）<div>https:&#47;&#47;github.com&#47;dreamhead&#47;moco</div>2020-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/88/cdda9e6f.jpg" width="30px"><span>阳仔</span> 👍（6） 💬（0）<div>作为程序猿学习能力应该是自带属性，实际工作中，从解决问题出发，锻炼自身的软件设计和开发能力，这是一个层次。
把问题抽象出来提供一个通用的解决方案，并提供程序库出来，这又是一个层次。
自己和自己维护的代码一起进化，这应该是每一个开发者所追求的
</div>2020-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f4/87/644c0c5d.jpg" width="30px"><span>俊伟</span> 👍（3） 💬（0）<div>郑老师真是我辈楷模。从2018年的10x专栏一直追到现在，常读常新。之前通过郑老师了解到TDD，现在工作中已经离不开这种先进的开发方式了。</div>2023-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/cc/ca22bb7c.jpg" width="30px"><span>蓝士钦</span> 👍（2） 💬（0）<div>在日常工作中，常常因为查bug导致阻碍开发进度，其实也是旧项目单元测试没做好，但是有一部分原因是集成测试没做，有些问题需要整个系统和外部系统串起来完整的调用才能定位问题。我想写一个易于集成测试的DSL，可以将测试人员写好的测试用例的描述内容作为集成测试的逻辑组装。 大多数情况下都是测试人员在写自己的测试代码，通过系统的http接口调用进行测试。很难覆盖到系统和外部系统之间的调用，往往出问题的也是不同团队间的系统间调用，不同系统间调用老师有什么好的建议吗</div>2020-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（0）<div>注意发现身边的小问题，用一个程序库或工具解决它。--记下来
这一讲很贴近开发</div>2022-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/57/2a/cb7e3c20.jpg" width="30px"><span>Nio</span> 👍（1） 💬（0）<div>程序员不能只当一个问题的解决者，还应该经常抬头看路，做一个问题的发现者。
真实生活并不是本该就是现在这样，是存在各种各样的问题的，不应该局限于我们要解决什么问题，更多应该留出时间想想我们有什么问题，我们为什么有这些问题。</div>2022-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a3/e2/5cb4f43f.jpg" width="30px"><span>laolinshi</span> 👍（1） 💬（0）<div>做微服务拆分的时候对于那些新实现的接口，需要跟原有系统的旧接口进行返回内容的比较，以此来保证新接口返回的数据和老接口是一致的，没有缺少需要返回的数据。刚开始的时候对新旧接口是采用肉眼比较的方式来找到差异的地方的，由于接口返回的数据非常多，这个比较过程非常痛苦，而且很容易出错。为了解决肉眼比较带来的困扰，花了一些时间研究了微服务契约测试框架Pact的实现原理，借鉴了框架中用于JSON字符串比较的实现逻辑，自己实现了一套新旧接口返回数据比较的小工具。通过这个工具可以标记出新旧接口返回数据的差异，根据这些差异信息就可以比较容易的发现新接口在逻辑实现的过程中不小心引入的问题。</div>2022-03-30</li><br/>
</ul>