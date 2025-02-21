你好，我是郑晔！

上一讲我们讲了 Spring 对轻量级开发的支持。不同于传统的开发方式，Spring 希望可以做到开发不依赖于应用服务器。为了达成这个目标，Spring 提供了各种支持，能够让你在部署到容器之前完成所有代码的基础验证工作。在核心业务部分，只要我们能够不过分依赖于 Spring 的种种特性，测试就和普通的单元测试差别不大。

不过在真实世界的软件开发中，我们总要与其它的外部组件集成。一旦牵扯到集成，测试的难度就上来了。不过正如前面所说，Spring 要尽可能让你在不依赖于容器的情况下进行测试。Spring 的做法就是提供一套自己的方案，替代掉对于容器的依赖。

这一讲，我们就来看看采用 Spring 的项目如何做集成测试。

## 数据库的测试

今天数据库几乎成了所有商业项目的标配，所以，Spring 也提供了对于数据库测试很好的支持。我们之前说过，一个好的测试要有可重复性，这句话放到数据库上就是要保证测试之前的数据库和测试之后的数据库是一样的。怎么做到这一点呢？

### 测试配置

通常有两种做法，一种是采用嵌入式内存数据库，也就是在测试执行之后，内存中的数据一次丢掉。另一种做法就是采用真实的数据库，为了保证测试前后数据库是一致的，我们会采用事务回滚的方式，并不把数据真正地提交进数据库里。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/87/8ed5880a.jpg" width="30px"><span>大碗</span> 👍（6） 💬（1）<div>如果业务逻辑里面有发布消息到MQ的逻辑，在集成测试里面也是要部署一个mq_test来测试吗，有没有什么好方法</div>2021-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/e6/47742988.jpg" width="30px"><span>webmin</span> 👍（4） 💬（2）<div>H2本身支持设定为模拟oracle,mysql等数据库(url中加上MODE=Oracle)，可以支持特定DB常用的函数和机制，到是准备测试用的初始化数据是比较考验耐心和毅力，后期如果调整schema，需要对测试用到的SQL逐一调整也一项体力活。</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/84/0b8e2d25.jpg" width="30px"><span>邓志国</span> 👍（3） 💬（1）<div>引入cucumber后，实际上是启动了web服务，通过http来测试，这样更加真实。不知道mockmvc有没有什么坑，毕竟它稍微假了一点</div>2021-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/95/4544d905.jpg" width="30px"><span>sylan215</span> 👍（3） 💬（0）<div>之前没有了解过嵌入式内存数据库，这次学习了，回头也了解下。

我们目前做数据库相关的测试，就用的独立的测试数据库的做法，当然，我们是逻辑验证为主，所以可以保证一致性。

如果不能使用单独测试数据库的话（业务关联逻辑较强的时候），我们会考虑使用测试数据回滚的方式来做，就是会有独立的数据准备的接口，然后有独立的数据清洗的接口，这样做的困难点，就是保证数据一致性的问题，比较测试逻辑本身也可能存在 bug。

最后说的 Web 接口测试，没有特别明白为啥不使用真实的 Web 环境，如果是为了测试分离，倒是可以理解，其他的好像影响不大。</div>2021-09-16</li><br/><li><img src="" width="30px"><span>byemoto</span> 👍（2） 💬（0）<div>老师, 对于Go语言来说是否也有类似的测试工具推荐使用呢?</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/33/acacb6ac.jpg" width="30px"><span>砖用冰西瓜</span> 👍（1） 💬（0）<div>“不能为了测试的需要而修改代码”说的是不是实现细节？如果遗留系统的一些函数之前写的是不可测的，那我把它改成可测试的，算是“为了测试的需要而修改代码”吗？</div>2022-08-15</li><br/><li><img src="" width="30px"><span>Geek_8206f4</span> 👍（0） 💬（0）<div>请问带有security或者oauth授权的接口该如何进行测试呢
</div>2022-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>采用轻量级的测试手段，保证代码的正确性--记下来</div>2022-06-12</li><br/>
</ul>