你好，我是郑晔。

这一讲是我们整个专栏的第一节课。我在开篇词里说过，很多程序员之所以不写测试，一个重要的原因是不会写测试。所以，我们不玩虚的，第一节课直接带你上手实战。

我们要实现的是一个 ToDo 的应用，选择一个新项目开始，我们没有历史负担，对于学习如何写测试来说，是最容易的。整个实战分为了上下两节课，在这节课里，我们先来实现业务的核心部分，下一节课，我们把完整的应用实现出来。

这个 ToDo 应用本身非常简单，实现功能并不是我们这两节课的重点。一方面，你会看到如何解决问题的过程，比如，如何分解任务、如何设计测试场景、如何把测试场景转换为一个测试用例等等；另一方面，你也会看到，我是如何运用这些解决问题的过程一点点把问题解决掉，在整个开发的过程中如何写测试、写代码。

当你在实际工作中面对更复杂的问题时，这里面的代码对你的帮助可能不大，但这些解决问题的思路却会在工作中实际帮助到你。如果你订阅过我的前几个专栏，这算是一个完整的实战练习。

## 项目前的准备

在正式开始之前，我们一块来看下这个 ToDo 应用都有哪些具体需求（注：接下来的代码我会用Java来写，如果你没有购买过我的其他课程也没有关系，极客时间有免费试读额度，欢迎你点击文章里的超链接进行学习）。
<div><strong>精选留言（25）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/95/4544d905.jpg" width="30px"><span>sylan215</span> 👍（15） 💬（3）<div>这个例子比较简单，挺适合刚开始入门测试的人，但是同时，也可能会让开发觉得，这么简单的逻辑，一看就知道对不对、有没有问题了，何必还要用自动化测试进行覆盖呢？

一方面，这确实只是个例子，但是也不能因为简单，就不写用例，因为所有的代码都不可预知的在后面发生改变，那么作为后续的回归用例，也是一样有用的；

另一方面，需要关注 mock 的使用，实际业务场景很复杂，函数之间相互调用逻辑更是很常见，所以会经常用到 mock，但是 mock 也不可避免的会让我们规避了集成测试的测试点，所以怎么选取合适的 mock 点，并预知 mock 的风险，也是要了解的。

再补充，就算自己写了测试用例，也不要完全的依赖测试来发现所有的问题，代码思维、设计风格、编码习惯，这些预防问题发生的手段，才是最有效的。

以上，期待后续的精彩内容。</div>2021-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/4a/e1/2a498473.jpg" width="30px"><span>李威</span> 👍（6） 💬（1）<div>文中是从sevice层入手写第一个测试，可否以整洁架构图中最内层的entity入手写第一个测试，代码实现也是按先实现内层，再逐步实现外层的代码？</div>2021-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/bd/6c/a988846d.jpg" width="30px"><span>asusual</span> 👍（4） 💬（1）<div>相比Junit,Spock框架测试起来要省事很多~</div>2021-08-22</li><br/><li><img src="" width="30px"><span>Geek_3b1096</span> 👍（3） 💬（1）<div>谢谢老师一步一步的说明添加TodoItem字段: content -&gt; done -&gt; index</div>2021-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/f7/0b/403fbeba.jpg" width="30px"><span>小凯</span> 👍（3） 💬（1）<div>项目运行不起来 能贴一下具体的gradle版本信息吗？</div>2021-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/67/3a/0dd9ea02.jpg" width="30px"><span>Summer  空城</span> 👍（3） 💬（1）<div>List list(final boolean all);  这个接口不符合单一职责原则吧</div>2021-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/03/50/abb7bfe3.jpg" width="30px"><span>Geek_jct58r</span> 👍（2） 💬（2）<div>我在实现例如 TodoItemService 之前, 通常都会先测试它的 输入和输出, 两个类被测试完成后, 我才去开始用测试实现TodoItemService. 但看了您的实现手法, 一个测试集就已经能够覆盖到了输入输出.感觉您这样更简单些. 不知道我想的对不对, 还是应该一个模块对应一个测试集呢?</div>2021-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/29/ab/59a6e437.jpg" width="30px"><span>Kevin</span> 👍（1） 💬（1）<div>老师好，我是从10x程序员开始关注老师的课程，目前该课程已经学习完毕，受益匪浅。然后就开始继续学习软件设计之美，目前还在学习中。后来又看到代码之丑的ToDo项目，当时就在想也要参与一下。然后就思考怎么样才能写得出彩，第一点想到的就是要实践一下tdd。现在看到程序员的测试课这门课程，果然是英雄所见略同，哈哈哈！

因为我刚换了一个工作，主要会用C++来开发。所以这里先立个flag，使用C++来实践这个课程，采用tdd来实现这个ToDo的小项目。到时把GitHub工程发出来，请老师点评。

不过时间周期可能会比较长，我尽量努力。</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/59/21/d2efde18.jpg" width="30px"><span>布凡</span> 👍（0） 💬（1）<div>老师，java 新手，课程中的思路我都能理解，但是如果自己手动实践还是有一些问题，可以考虑出一个java开发环境安装的视频吗？</div>2022-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/87/92/9ac4c335.jpg" width="30px"><span>🌿</span> 👍（0） 💬（1）<div>关于应用服务的设计，老师哪个专栏或文章里面有详细说明？</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/87/92/9ac4c335.jpg" width="30px"><span>🌿</span> 👍（0） 💬（3）<div>老师，例子中，TodoItemService目前为止包含了TodoItem所有相关业务操作方法，但有些资料推荐将这些业务方法提取到单独Service里面，请问这2种方式各有什么优点，在实际开发中这2种方式各在什么情况下使用？</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/6c/0f0cf9eb.jpg" width="30px"><span>树懒先生</span> 👍（0） 💬（1）<div>so, Service实现就在Service层。</div>2021-09-10</li><br/><li><img src="" width="30px"><span>爪哇咿</span> 👍（6） 💬（3）<div>我有个疑问，是否有必要为了满足单测的可测性让原本没有返回值的函数有返回值</div>2021-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/37/92/961ba560.jpg" width="30px"><span>授人以🐟，不如授人以渔</span> 👍（2） 💬（0）<div>在工作中，我一般做测试的代码是那些看起来很容易做测试的部分，实际上其底层逻辑依然是：对我有能力做测试的代码做测试，很大部分代码都是没有能力做测试的，也就是说写出的代码是不具备可测试性的。另外，我会做大量的接口测试，实际上是一种集成测试或系统测试。</div>2022-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（0）<div>细化测试场景，编写可测试的代码。--记下来</div>2022-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/7d/dd852b04.jpg" width="30px"><span>chon</span> 👍（1） 💬（0）<div>老师，我用jacoco的maven plugin，运行后发现代码覆盖率为0，这部分的测试代码已写。同样写了不用mockito的测试代码，这个就能看到测试覆盖率不为0。网上说因为mockito也用了字节码增强，导致冲突。请问这个怎么解决？</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/cd/8d552516.jpg" width="30px"><span>Gojustforfun</span> 👍（1） 💬（2）<div>should_mark_todo_item_as_done测试用例中
1)  actural.isDone是在哪实现的？TodoItem中没有这个方法。是使用注解实现的吗？
2） Optional&lt;TodoItem&gt; todoItem = service.markTodoItemDone(1)中1应该是TodoIndexParameter类型
3)  Java特性用的有点多，其他语言背景看的有点困难。运行时异常，Optional。希望老师能照顾一下，多解释一下或者提示一下其他语言对应的特性，谢谢</div>2021-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e6/d5/20c2fb6b.jpg" width="30px"><span>天空提提</span> 👍（0） 💬（0）<div>为什么索引超出范围不直接抛出异常呢？</div>2023-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（0）<div>在实际工作中，自己都是先写Repository层和内容实现，再写 Service 层实现，然后再直接集成测试 Service 层。并且都是先写好内容代码，再想着写测试 case</div>2023-04-28</li><br/><li><img src="" width="30px"><span>Geek_a6ed5f</span> 👍（0） 💬（1）<div>github的地址是哪里？</div>2022-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/33/acacb6ac.jpg" width="30px"><span>砖用冰西瓜</span> 👍（0） 💬（0）<div>我不是写 Java 的程序猿，有个问题，Java 是强类型，函数的参数的类型定义好了，在调用的时候如果用了 null，应该是不用单元测试也会报错吧？还需要在单元测试里面再验证一遍吗？</div>2022-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/93/33/2d4de22e.jpg" width="30px"><span>大鹏</span> 👍（0） 💬（0）<div>   @Test
    void should_not_list_without_item() {
        when(repository.findAll()).thenReturn(ImmutableList.of());

        List&lt;TodoItem&gt; items = service.list(true);
        &#47;&#47; assertThat(items).hasSize(0);  &#47;&#47; 这一行性能有问题, 替换成下面的更好
        assertThat(items).isEmpty();
    }</div>2022-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/b6/abdebdeb.jpg" width="30px"><span>Michael</span> 👍（0） 💬（0）<div>老师好，我一直有个问题比较困惑，我们在做单元测试的时候需要mock数据，比如说我下面这个例子：

```
public interface OrderService {
    Order create(Order order)
}

@Test
public void should_create_order() {
        Order mockOrder = mockOrder();
        OrderService subject = new OrderServiceImpl(orderRepository);
        when(orderRepository.save(any())).thenReturn(mockOrder);

        Order createdOrder = subject.create(mockOrder);
        这里对状态的测试好像没什么意义，因为createdOrder就是mockOrder, 而mockOrder是我们给的
    }
```
在这个例子中，OrderService接收一个Order entity的参数，通过orderRepository.save(order)持久化Order，然后return createdOrder，我的问题是：
1. 这个测试好像没什么用，因为你的返回值createdOrder其实就是测试里的mockOrder?
2. 这个OrderService.create(Order order)的设计是不是不对，我们是不是应该设计成OrderService.create(OrderDTO orderDto)，这样的话我们就不需要每次都得在调用方做DTO-&gt;entity的convert
3. 每次有xxxRepository.save()这样的调用我就感觉整个测试没什么意义，因为你的返回值很可能就是 return xxxRepository.save(xxx), 这种方法可能只能用行为测试，做不了状态测试。</div>2022-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/20/c8/b16eb6ed.jpg" width="30px"><span>程同学</span> 👍（0） 💬（0）<div>不懂Java，只懂JS。有咩有适合前端的测试课程</div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b6/e6/db12908c.jpg" width="30px"><span>微笑</span> 👍（0） 💬（0）<div>当代码技术负债太高，实际开发业务时根本没那么多时间写测试
最多就是关键逻辑，或者必要测试才会写
大多数都是接口集成测试。

适合新项项目、项目质量要求高</div>2022-01-21</li><br/>
</ul>