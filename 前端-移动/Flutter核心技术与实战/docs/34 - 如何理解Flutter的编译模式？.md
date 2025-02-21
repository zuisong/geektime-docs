你好，我是陈航。今天，我们来聊聊Flutter的编译模式吧。

在开发移动应用程序时，一个App的完整生命周期包括开发、测试和上线3个阶段。在每个阶段，开发者的关注点都不一样。

比如，在开发阶段，我们希望调试尽可能方便、快速，尽可能多地提供错误上下文信息；在测试阶段，我们希望覆盖范围尽可能全面，能够具备不同配置切换能力，可以测试和验证还没有对外发布的新功能；而在发布阶段，我们则希望能够去除一切测试代码，精简调试信息，使运行速度尽可能快，代码足够安全。

这就要求开发者在构建移动应用时，不仅要在工程内提前准备多份配置环境，还要利用编译器提供的编译选项，打包出符合不同阶段优化需求的App。

对于Flutter来说，它既支持常见的Debug、Release等工程物理层面的编译模式，也支持在工程内提供多种配置环境入口。今天，我们就来学习一下Flutter提供的编译模式，以及如何在App中引用开发环境和生产环境，使得我们在不破坏任何生产环境代码的情况下，能够测试处于开发期的新功能。

## Flutter的编译模式

Flutter支持3种运行模式，包括Debug、Release和Profile。在编译时，这三种模式是完全独立的。首先，我们先来看看这3种模式的具体含义吧。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/af/bf/06fa89fb.jpg" width="30px"><span>渐醒AINY</span> 👍（8） 💬（1）<div>老师讲的很棒，帮助了我很多，我的一个Flutter项目也制作完成，并上架发布了</div>2019-10-18</li><br/><li><img src="" width="30px"><span>Geek_082580</span> 👍（3） 💬（2）<div>对于一个 flutter module 工程， 即需要嵌入到已有 Android 项目，又需要单独运行调试，在这两种状态下需要不同的配置，比如不同的 plugin，请问老师有什么好的办法吗？</div>2019-09-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqUP1oawANUYOmFic40JrcRC4AVp0qVvuoibUFYkKDJtJNP6qXKnibB0nQ9kQibqCiakHkGoYXZbLTcibUw/132" width="30px"><span>liyuan</span> 👍（2） 💬（1）<div>仅仅通过-t能配置的参数还是太弱了，如果有dev，qa，uat，prod等多个环境，每个环境的app应用名称&#47;图标可能有差别，同时希望手机上多个环境的app共存

android可以用build flavor实现，ios应该怎么做比较好？</div>2019-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/81/45/9aa91b75.jpg" width="30px"><span>矮个子先生😝</span> 👍（1） 💬（2）<div>看到过另外一种判断方法:bool.fromEnvironment(&#39;dart.vm.product&#39;)</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4b/0a/4bb137d9.jpg" width="30px"><span>hz</span> 👍（1） 💬（2）<div>var config = AppConfig.of(context); 获取配置的时候需要context作为参数，在build方法里面就可以方便获得配置。在其他地方没有context作为参数的时候，需要获取配置应该怎么获取</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/37/aa04f997.jpg" width="30px"><span>和小胖</span> 👍（0） 💬（1）<div>思考题：老师我的理解是直接再 new 一个 AppConfig 出来传入不同的参数不就好了吗？只是相当于我们有多种开发的 config，有几种就配置几个 AppConfig 可以吗？</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f5/d4/5a0a2f8d.jpg" width="30px"><span>火腿</span> 👍（3） 💬（0）<div>配置信息可以写到json或其它格式的本地文件里， 启动时读取配置信息。 或者把配置文件放到远程，可以实现动态加载样式或模块，本地有默认的配置， 以防网络不可用。 </div>2019-12-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/MxIKVrOfvGrWibezibHJ376rHJOAtiaVyKtX9j5hZNdY9z1GH6tPJdgu66oE1fuBvc3Jnz9dhwd046xBXQYjia0H2g/132" width="30px"><span>。。。。。。</span> 👍（0） 💬（1）<div>InheritedWidget 麻烦问一下如何能脱离了context 来使用呢？</div>2020-05-16</li><br/>
</ul>