你好，我是蔡元楠。

今天我要与你分享的主题是“如何测试Beam Pipeline”。

在上一讲中，我们结合了第7讲的内容，一起学习了在Beam的世界中我们该怎么设计好对应的设计模式。而在今天这一讲中，我想要讲讲在日常开发中经常会被忽略的，但是又非常重要的一个开发环节——测试。

你知道，我们设计好的Beam数据流水线通常都会被放在分布式环境下执行，具体每一步的Transform都会被分配到任意的机器上面执行。如果我们在运行数据流水线时发现结果出错了，那么想要定位到具体的机器，再到上面去做调试是不现实的。

当然还有另一种方法，读取一些样本数据集，再运行整个数据流水线去验证哪一步逻辑出错了。但这是一项非常耗时耗力的工作。即便我们可以把样本数据集定义得非常小，从而缩短运行数据流水线运行所需的时间。但是万一我们所写的是多步骤数据流水线的话，就不知道到底在哪一步出错了，我们必须把每一步的中间结果输出出来进行调试。

基于以上种种的原因，在我们正式将数据流水线放在分布式环境上面运行之前，先完整地测试好整个数据流水线逻辑，就变得尤为重要了。

为了解决这些问题，Beam提供了一套完整的测试SDK。让我们可以在开发数据流水线的同时，能够实现对一个Transform逻辑的单元测试，也可以对整个数据流水线端到端（End-to-End）地测试。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/b0/77e5f8c8.jpg" width="30px"><span>李孟聊AI</span> 👍（0） 💬（1）<div>Beam 有类似sparksql的api吗？</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（7） 💬（0）<div>我期望是基于spark或flink讲解的重实践思想，轻知识，这个可以自己下去学</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（2） 💬（0）<div>看来我得先去学学Java了，不会java，看不太懂。</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/21/eb/bb2e7a3b.jpg" width="30px"><span>Ming</span> 👍（2） 💬（0）<div>我觉得测试的话，相对麻烦的地方还是在工程脚手架的设计上。
显然代码本身要抽象封装好，确保测试能覆盖生产代码，而不是生产代码的“拷贝”。
但有些在代码之外的问题让我挺好奇的：
如何保证测试数据的格式和生产数据的格式同步？
流处理的测试怎么模拟时间？
团队是如何在流程上确保pipeline必须经过测试才能运行的，是通过CI&#47;CD来自动执行pipeline？还是往往通过人力把关？
</div>2019-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/a0/f4/7e122a67.jpg" width="30px"><span>之渊</span> 👍（0） 💬（0）<div>我觉得挺好的，对于我们新手来说很友好。
谁都是从新手过来的，感谢大佬对新手的支持。
代码示例：
https:&#47;&#47;gitee.com&#47;oumin12345&#47;daimademojihe&#47;tree&#47;master&#47;cloudx&#47;bigdata&#47;src&#47;main&#47;java&#47;test&#47;beam</div>2020-08-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqEacia8yO1dR5Tal9B7w8PzTRrViajlAvDph96OqcuBGe29icbXOibhibGmaBcO7BfpVia0Y8ksZwsuAYQ/132" width="30px"><span>杰洛特</span> 👍（0） 💬（1）<div>TestClass 里的这个 PCollection&lt;String&gt; output = input.apply(ParDo.of(new EvenNumberFn())); 里面的泛型是不是写错了？偶数是 Integer 吧？</div>2019-11-14</li><br/>
</ul>