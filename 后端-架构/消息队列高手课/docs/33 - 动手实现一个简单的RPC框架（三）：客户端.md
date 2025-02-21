你好，我是李玥。

上节课我们已经一起实现了这个RPC框架中的两个基础组件：序列化和网络传输部分，这节课我们继续来实现这个RPC框架的客户端部分。

在《[31 | 动手实现一个简单的RPC框架（一）：原理和程序的结构](https://time.geekbang.org/column/article/144320)》这节课中我们提到过，在RPC框架中，最关键的就是理解“桩”的实现原理，桩是RPC框架在客户端的服务代理，它和远程服务具有相同的方法签名，或者说是实现了相同的接口，客户端在调用RPC框架提供的服务时，实际调用的就是“桩”提供的方法，在桩的实现方法中，它会发请求到服务端获取调用结果并返回给调用方。

**在RPC框架的客户端中，最关键的部分，也就是如何来生成和实现这个桩。**

## 如何来动态地生成桩？

RPC框架中的这种桩的设计，它其实采用了一种设计模式：“代理模式”。代理模式给某一个对象提供一个代理对象，并由代理对象控制对原对象的引用，被代理的那个对象称为委托对象。

在RPC框架中，代理对象都是由RPC框架的客户端来提供的，也就是我们一直说的“桩”，委托对象就是在服务端，真正实现业务逻辑的服务类的实例。

![](https://static001.geekbang.org/resource/image/6c/48/6ca3f88f1a6c06513d5adfe976efcc48.jpg?wh=4266%2A768)

我们最常用Spring框架，它的核心IOC（依赖注入）和AOP（面向切面）机制，就是这种代理模式的一个实现。我们在日常开发的过程中，可以利用这种代理模式，在调用流程中动态地注入一些非侵入式业务逻辑。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/04/71/853b2292.jpg" width="30px"><span>Gred</span> 👍（31） 💬（4）<div>1.改用CGLib动态代理，增加多接口多方法支持。
2.增加Object序列化类以及默认序列化类，增加对多入参的序列化支持。
借花献佛了，麻烦老师指导下
https:&#47;&#47;github.com&#47;Gred01&#47;simple-rpc-framework</div>2019-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/03/10/26f9f762.jpg" width="30px"><span>Switch</span> 👍（5） 💬（1）<div>基本类型暂未实现，
https:&#47;&#47;github.com&#47;Switch-vov&#47;simple-rpc-framework&#47;tree&#47;feature-stub</div>2019-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/a0/9555c97d.jpg" width="30px"><span>wzzJike</span> 👍（3） 💬（1）<div>java的很多框架使用的都是jdk的动态代理吧，能获取到代理类，调用方法，参数信息</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/99/c4302030.jpg" width="30px"><span>Khirye</span> 👍（1） 💬（3）<div>老师，我想请教一个问题。您的文章中写道：“那能不能用一个第三方来创建这个实现类呢？也是不行的，即使用一个第三方类来创建实现，那依赖关系就变成了：调用方依赖第三方类，第三方类依赖实现类，调用方还是间接依赖实现类，还是没有解耦”，那么请问SPI跟“一个第三方来创建实现类”这个行为本质上有什么区别呢。我的理解是SPI本质上也是“创建”了一个类。还望老师解惑🙏

</div>2019-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/1b/f62722ca.jpg" width="30px"><span>A9</span> 👍（5） 💬（0）<div>解除参数和返回值的限制，意味着序列化模块要支持任意类，这就需要实现一套通用的序列化协议或在serialize模块中实现用到的所有类型。假设依旧使用自定义协议，并且用到的所有类型均实现了序列化接口。需要进行如下修改：
  1.DynamicStubFactory#createStub的Method处理，使用getMethods获取method数组，for循环处理method而不是直接去数组下标0
  2.把DynamicStubFactory的类代码模板进行拆分，分为类模板和方法模板，先生成所有method的代码，再以此生成整个类的代码
  3.定义一个新的协议结构用来存放函数的参数，用此类型代替RpcRequest的serializedArguments变量，并修改RpcRequest的序列化相关函数
  4.修改RpcRequestHandler#handle:52行内根据rpcRequest去取得实际method的函数，获取任意参数个数和类型的对应函数
</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（2） 💬（0）<div>明确的知道自己的问题后再补开发语言那块的漏、、、课程拉了3节：看来一个人的精力还是有限，完全不拉的跟了30节后面还是拉下了课程，动手这块只能利用双休日再争取补上一点了。。。</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（1） 💬（0）<div>案例篇太精彩了</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/05/06/f5979d65.jpg" width="30px"><span>亚洲舞王.尼古拉斯赵四</span> 👍（1） 💬（0）<div>嘻嘻，开心，成功支持任意数目方法，任意返回值类型，接口成功调用并正确工作，其实这个作业就是一个循环遍历的过程，然后将每个方法的返回值，方法名替换的过程</div>2019-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>棒👍🏻</div>2023-01-11</li><br/>
</ul>