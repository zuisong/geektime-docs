你好，我是郑晔！

经过了基础篇的介绍，相信你已经对在日常开发中测试应该做到什么程度有了一个初步的认识。有了基础固然好，但对于很多人来说，面对常见的场景还是不知道如何下手。在接下来的应用篇中，我们就用一些开发中常见的场景，给你具体介绍一下怎么样把我们学到的知识应用起来。

在后端开发中，最常见的一种情况就是开发一个 REST 服务，将数据写到数据库里面，也就是传说中的 CRUD 操作。这一讲，我们就把前面已经写好的 [ToDo 应用](https://time.geekbang.org/column/article/404301)扩展一下，让它变成一个 REST 服务。

## 扩展前的准备

具体动手写任何代码之前，我们先要搞清楚我们要把这个应用改造成什么样子。把 ToDo 应用扩展为一个 REST 服务也就是说，原来本地的操作现在要以 REST 服务的方式提供了。另外，在这次改造里面，我们还会把原来基于文件的 Repository 改写成基于数据库的 Repository，这样，就和大多数人在实际的项目中遇到的情况是类似的了。

有人可能会想，既然是 REST 服务，那是不是要考虑多用户之类的场景。你可以暂时把它理解成一个本地运行的服务（也就是说只有你一个人在使用），所以我们可以不考虑多用户的情况。这样做可以让我们把注意力更多放在测试本身上，而增加更多的能力是需求实现的事情，你可以在后面拿这个项目练手时，做更多的尝试。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/d2/f8/d5006178.jpg" width="30px"><span>闻人</span> 👍（2） 💬（3）<div>文中外部对象转为内部对象的实现有必要放到单独的类里吗，减少两个对象的依赖</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/7d/dd852b04.jpg" width="30px"><span>chon</span> 👍（1） 💬（1）<div>集成restful的例子写的挺好的，如何处理dubbo的呢？后续章节能否给个完整的例子？谢谢</div>2021-09-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELEVMHiad4wERgib6x90kI81JZhzIvQeXMju6WohePAlfjWD3gHibapVNX88G4R29Ujcbiap1Bfz0Efmg/132" width="30px"><span>不二先生</span> 👍（1） 💬（1）<div>郑老师，你好：
有一个问题想请教下。
MockMVC 创建的模拟网络环境可以连接到数据库？这个数据库是本地的吗？</div>2021-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f3/06/8da1bf0c.jpg" width="30px"><span>Fredo</span> 👍（1） 💬（1）<div>老师你好 ，更新了一下ToDo项目 build无法通过了，task migrateToDev 这里是不还有漏了啥没上传的</div>2021-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/87/8ed5880a.jpg" width="30px"><span>大碗</span> 👍（1） 💬（1）<div>有几个问题请教下老师：
1, 参数校验的逻辑在core层也有，算不算重复？现在写在的api里，能否移动到request的构造函数里面判断，然后抛出全局异常再返回BadRequest？实际业务一个add有好几个字段要check，写起来api的函数就好长了
2，测试接口的时候，构造request的使用的字符串json，为什么不用new对象再用工具toJsonString，手打json字符串容易出错
3，测试的数据库用了mysql的一个test库，不用h2是基于什么考虑呢</div>2021-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d4/ee/92b9bd3d.jpg" width="30px"><span>深云</span> 👍（0） 💬（1）<div>final TodoParameter parameter = TodoParameter.of(request.getContent());这种方式，不会导致TodoParameter依赖于外部request的content吗，是不是在api层设计一个converter专门用于处理这个转换比较好</div>2025-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/95/4544d905.jpg" width="30px"><span>sylan215</span> 👍（4） 💬（0）<div>本节是一个实例验证把一个应用扩展为 REST 服务（自查下具体的意思）。

因为是基于 Java 语言的，所以里面提到很多 Java 的工具，这部分不会，所以不是特别懂，但是大概意思是知道的，几个关键点：

1、接口服务要遵循 RESTful 规范（统一规范对测试来说也意义重大）；

2、接口如果涉及对数据的操作，测试完之后尽量要进行清场操作，避免垃圾数据残留（数据构造也是测试的一大难点）；

3、本次演示还是遵循接口测试的原则，不涉及接口实现的覆盖；</div>2021-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（0）<div>集成测试回滚数据，保证测试的可重复性。--记下来
Springboot很方便</div>2022-06-11</li><br/><li><img src="" width="30px"><span>Geek_3b1096</span> 👍（1） 💬（0）<div>...而不仅仅是围绕着前端需求去做... 期待老师推出API设计课</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/6d/3e570bb8.jpg" width="30px"><span>一打七</span> 👍（0） 💬（0）<div>没有理解为什么用构造函数的方式进行注入，老师能解答一下吗？谢谢</div>2023-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/4b/53/f797f031.jpg" width="30px"><span>无道win</span> 👍（0） 💬（0）<div>如果数据库使用的mybatias有没有类似 @DataJpaTest的注解？</div>2022-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c4/ad/79b8a12c.jpg" width="30px"><span>一步</span> 👍（0） 💬（0）<div>mockmvc全流程测试，特别耗时的问题该从哪些方面优化，提高测试速度，特别是环境构建速度。</div>2022-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/86/8e52afb8.jpg" width="30px"><span>花花大脸猫</span> 👍（0） 💬（0）<div>老师，如果单元测试需要依赖spring容器的运行时环境才能支撑，那如果后续我开发一个项目但是并没有用到问题提到的那些部分，应该如何处理？我认为单元测试应该不依赖任何组件的，直接可以运行。</div>2022-04-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/rvQxUmekECjyZu1RwbUguBWpBcQuKywQPtiaxNVFJSib07QMZnNUr8MnRF3RYEsn6MhgGFJibwlrVomibEicYMiaia7ZQ/132" width="30px"><span>Geek_a8ce05</span> 👍（0） 💬（1）<div>原来是面向java的测试课，php溜了溜了</div>2022-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/4c/01/72203f00.jpg" width="30px"><span>sidabw</span> 👍（0） 💬（0）<div>great!
</div>2022-02-23</li><br/>
</ul>