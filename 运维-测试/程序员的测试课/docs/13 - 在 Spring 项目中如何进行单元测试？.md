你好，我是郑晔！

上一讲，我们将 ToDo 应用从命令行扩展为了 REST 服务。在这个应用里，我们用到了 Spring 这个在 Java 世界中广泛使用的框架。大多数人对于 Spring 这个框架的认知都停留在如何使用它完成各种功能特性上，而 Spring 更大的价值其实在对于开发效率的巨大提升上，其中就包含了对测试的支持。

在接下来的两讲，我们就把注意力从一个具体的项目上挪开，放到 Spring 框架本身，看看它对开发效率提升的支持。

## 轻量级开发的 Spring

很多人对于 Spring 的理解是从依赖注入容器开始的，但是，Spring 真正对行业的影响却是从它对原有开发模式的颠覆开始。

在 21 世纪初的时候，Java 世界的主流开发方式是 J2EE，也就是 Java 的企业版。在那个时候，企业版代表软件开发的最高水准。在这个企业版的构想中，所有的复杂都应该隐藏起来，写代码的程序员不需要知道各种细节，需要的东西拿过来用就好了。

这种想法本身是没有问题的，时至今日，很多平台和框架也是这么想的。到了具体的做法上，J2EE 提供了一个应用服务器，我把这些复杂性都放在这个应用服务器里实现，你写好的程序部署到这个应用服务器上就万事大吉了。但正是因为应用服务器的存在，使用 J2EE 进行开发变成了一件无比复杂的事情。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/84/0b8e2d25.jpg" width="30px"><span>邓志国</span> 👍（16） 💬（2）<div>构造函数不写autowire也能依赖注入</div>2021-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/13/71/887f0c83.jpg" width="30px"><span>蔡奎</span> 👍（6） 💬（1）<div>老师,spring 应用中依赖太多，每次启动都需要几分钟，如何保证测试。为了减少启动时间，步子都会迈大了，导致一些逻辑都不会写测试。最后就放弃测试。</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（5） 💬（5）<div>一直错误使用字段注入，所以感觉单元测试非常难</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e8/fc/4d84560f.jpg" width="30px"><span>我的康康</span> 👍（5） 💬（1）<div>老师，那平常开发过程中，也是不推荐用基于字段注入 而是推荐用基于构造方法注入吗？</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/af/c3/b213e913.jpg" width="30px"><span>null</span> 👍（2） 💬（2）<div>一些场景不适合使用构造器注入的呢？比如循环依赖。</div>2021-12-24</li><br/><li><img src="" width="30px"><span>Geek_3b1096</span> 👍（1） 💬（1）<div>ApplicationContext用起来简单，之后会避免</div>2021-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/95/4544d905.jpg" width="30px"><span>sylan215</span> 👍（2） 💬（0）<div>有幸在 Java1.5 的时代就接触了 Java，那时候 Java 的三个方向是 J2EE、J2SE、J2ME，后面 Spring 横空出世时，我就没有了解了，不过挺老师这么一说，真的是个转折点了。

至于框架对测试的支持，我也有过体会，比如 Python 里面的 Django 框架对测试的支持就是特别好，我当时学习的一个教程，就是一边讲代码，一边写测试，毫无违和感。

当然，老师也说了，不要过度依赖某些特性，所以怎么把框架特性，适度合理的进行利用，也是一个技术活。</div>2021-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/86/8e52afb8.jpg" width="30px"><span>花花大脸猫</span> 👍（1） 💬（1）<div>因为字段注入的问题，导致mock对象很难，后续全部调整成了构造器注入，另外我的观念是尽量单元测试不需要springboot的运行时环境依赖，这样会使得单元测试不纯粹，还需要依赖外部组件启动玩成才能运行</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/6d/3e570bb8.jpg" width="30px"><span>一打七</span> 👍（0） 💬（0）<div>推荐用基于构造方法注入，老师能举个mock参数的例子吗？</div>2023-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cb/93/124d8cd8.jpg" width="30px"><span>努力努力再努力</span> 👍（0） 💬（0）<div>老师，像是有一些 handler 类，只是单纯处理下数据就可以销毁实例了，这种并不打算交给容器管理，但是方法内可能又会使用到 spring 容器管理的 bean，例如某个 service，这种如果不使用 context 获取的话，可以怎么处理呢？</div>2022-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>平时同事，还有我自己都是基于字段注入的</div>2022-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>业务代码不要过度依赖于框架。--记下来</div>2022-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/df/bf/f90caa79.jpg" width="30px"><span>椿</span> 👍（0） 💬（0）<div>@MockBean 可以设置 Bean 的行为吗？</div>2022-06-07</li><br/>
</ul>