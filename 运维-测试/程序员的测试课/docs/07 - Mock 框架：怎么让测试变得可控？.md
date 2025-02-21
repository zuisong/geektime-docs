你好，我是郑晔！

上一讲，我们谈到测试不好测，关键是软件设计问题。一个好的设计可以把很多实现细节从业务代码中隔离出去。

之所以要隔离出去，一个重要的原因就是这些实现细节不那么可控。比如，如果我们依赖了数据库，就需要保证这个数据库环境同时只有一个测试在用。理论上这样不是不可能，但成本会非常高。再比如，如果依赖了第三方服务，那么我们就没法控制它给我们返回预期的值。这样一来，很多出错的场景，我们可能都没法测试。

所以，在测试里，我们不能依赖于这些好不容易隔离出去的细节。否则，测试就会变得不稳定，这也是很多团队测试难做的重要原因。不依赖于这些细节，那我们的测试总需要有一个实现出现在所需组件的位置上吧？或许你已经想到答案了，没错，这就是我们这一讲要讲的 Mock 框架。

## 从模式到框架

**做测试，本质上就是在一个可控的环境下对被测系统/组件进行各种试探。**拥有大量依赖于第三方代码，最大的问题就是不可控。

怎么把不可控变成可控？第一步自然是隔离，第二步就是用一个可控的组件代替不可控的组件。换言之，用一个假的组件代替真的组件。

这种用假组件代替真组件的做法，在测试中屡见不鲜，几乎成了标准的做法。但是，因为各种做法又有细微的差别，所以，如果你去了解这个具体做法会看到很多不同的名词，比如：Stub、Dummy、Fake、Spy、Mock 等等。实话说，你今天问我这些名词的差异，我也需要去查找相关的资料，不能给出一个立即的答复。它们之间确实存在差异，但差异几乎到了可以忽略不计的份上。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/95/4544d905.jpg" width="30px"><span>sylan215</span> 👍（7） 💬（1）<div>1、这一讲主要是讲 Mock 的，对于自动化测试来说，这个技术确实很关键，当然，老师也在文中建议慎用，使用的前提是，我们真的明白这些技术的作用和副作用。

2、前一讲说了测试要减少耦合性，同时我们为了保证测试目的的唯一性，就引入了 Mock 技术，它一定程度上，让我们的关注点更集中；

3、和 Mock 技术类似，我们还可以了解 Stub、Dummy、Fake、Spy 等技术，同样是帮忙我们优化测试目的，简化测试实现的；

4、Mock 等模拟对象，可以让我们方便的模拟传参和不同返回值的情况，这些如果是在实际业务环境中，构造起来可能会非常麻烦；

5、非测试目的的过程中的 verify 要慎用，避免降低用例的适用性，也会增加用例的维护成本；

以上，期待后续的精彩内容。</div>2021-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（6） 💬（4）<div>请教一下老师， 
把第三方mock掉了，
那么如何验证 我们请求第三方的参数是否正确， 我们到第三方的请求是否可以正常运行。</div>2021-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4f/bf/6584bdeb.jpg" width="30px"><span>阿姆斯壮</span> 👍（5） 💬（1）<div>今天又忍不住上来分享一下。把郑大之前的课程应用到工作之后。先从「坏味道」入手，利用函数式编程消除大量重复代码。不做CVS程序员。当工作和学习充分结合起来后，发现每天的工作都充满了乐趣。总感觉工作时间好快。（一天7个小时）不需要加班。可能我们公司是一个不务正业的IT公司。接下来，就是期待郑大的测试课。把自动化测试这块也应用到工作中。</div>2021-08-18</li><br/><li><img src="" width="30px"><span>byemoto</span> 👍（4） 💬（2）<div>如果存在多层, 那么每层对下层依赖的对象都需要做Stub&#47;Mock吗? 比如AggregateService依赖多个Service对象, 而各个Service对象又有自己的Repository, 那么在测试AggregateService时, 需要对各个Service对象做Mock吗?</div>2021-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/24/9c/e32fe600.jpg" width="30px"><span>下弦の月</span> 👍（4） 💬（4）<div>是否可以这么理解？
有个待测的组件A，内部依赖组建B,会执行B.callFunc(); 
同时，B还依赖于组建C,会执行 C.callMethod();

对A做单元测试的时候，我们需要隔离对B的依赖。Stub 做的事情是模拟一个B对象，设置好模拟B对象的 callFunc() 这个方法的输入与输出即可。

而Mock，除了上述的安排好输入与输出之外，还要对B.callFunc() 这个方法本身的行为做校验。比如verify(C,atLeast(1)).callMethod(any());

总结下来就是：如果只是准备一个被模拟对象的输入输出，就是Stub；如果要检查被模拟对象内部的行为，就是Mock。</div>2021-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/bd/6c/a988846d.jpg" width="30px"><span>asusual</span> 👍（3） 💬（1）<div>以前写测试基本都写了verify。现在看来郑大的观点非常准确~

过度使用 verify，在写代码的时候，你会有一种成就感。但是，一旦涉及代码修改，整个人就不好了。因为实现细节被 verify 锁定死，一旦修改代码，这些 verify 就很容易造成测试无法通过。</div>2021-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/52/c0/791d0f5e.jpg" width="30px"><span>MHT</span> 👍（0） 💬（0）<div>请教一下老师:假如我需要对A方法做单测，A方法调用B方法，B方法又会调用C方法，其中C的行为是不可控的，我在做mock的时候，是要mock B还是C呢？</div>2023-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（0）<div>Moco 主要模拟服务器，那突然想到 http 调用第三方服务器，都是在一个封装调用类里，那直接用 mock 框架，mock 这个类是不是也可以完成同样的事情</div>2023-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/6d/3e570bb8.jpg" width="30px"><span>一打七</span> 👍（0） 💬（2）<div>老师好，【测试应该测试的是接口行为，而不是内部实现】这句怎么理解？测试不就是测试业务的实现逻辑吗？这里怎么又说不是</div>2023-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>使用 Mock 框架，少用 verify。--记下来</div>2022-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/86/8e52afb8.jpg" width="30px"><span>花花大脸猫</span> 👍（0） 💬（1）<div>如何确定verify多写了，过度依赖，这有没有一个标准，如果我一个void返回的方法，需要处理单元测试，里面有几个依赖对象，那对于整个流程来说，我写单元测试肯定是需要verify调用到它们的时候入参是不是合法的，调用了几次，是不是这样的顺序调用，那这样势必要有多个verify？这块有点疑惑希望老师解答下</div>2022-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/83/27fd9c50.jpg" width="30px"><span>ownraul</span> 👍（0） 💬（0）<div>之前的代码中用了一个 RestTemplate 的mock 来模拟第三方的返回, 不好地方在于一旦使用了之后全部的  restTemplate 都被模拟, 用 Moco 直接模拟返回结果是个更加优雅的方式了, 只要把第三方的 url 都解耦开, 用本地不同的端口进行模拟就好</div>2022-01-03</li><br/>
</ul>