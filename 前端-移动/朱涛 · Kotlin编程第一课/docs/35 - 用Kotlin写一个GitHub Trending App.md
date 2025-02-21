你好，我是朱涛。

这节课，我们一起来用Kotlin和Jetpack写一个简单的Android应用。为了便于理解，这个应用的功能会尽量简单，即使你对Android不是特别熟悉，跟着课程的引导，你也能轻松完成。

## 准备工作

在之前的课程中，我们的实战项目都是基于JVM的，并没有涉及过Android相关的配置。因此，如果你的电脑没有Android开发的环境的话，那么可能需要做一些额外的配置。当然，在你已有Java环境的前提下，想要配置Android开发环境并不麻烦，你可以去搜索一些相关的[Android开发环境配置](https://www.google.com/search?q=Android%20%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE)的教程。

那么，要进行Android开发，我们可以使用IntelliJ，也可以使用Android Studio，后者针对Android开发做了很多定制化，也是免费的，这里我也建议你去下载Android Studio。

当配置好所有的环境以后，我们就可以像创建Kotlin工程一样，来创建一个新的Android工程了。

![图片](https://static001.geekbang.org/resource/image/f9/00/f9f6b73c7a09bac3ae5b3e15ff997000.gif?wh=900x650)

然后，当你创建好工程以后，就可以尝试运行代码了，这时候你大概率会看到一个Hello World的初始界面。

接下来，我们就正式进入开发吧。

## MVVM架构

Android应用的架构，在过去的这些年里一直都在变化。最开始的Android其实没有什么明确的架构，大家习惯于把所有代码都往Activity里放，直到后来才开始有了MVC、MVP以及MVVM。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/49/04/152ecd3f.jpg" width="30px"><span>百里路海</span> 👍（6） 💬（1）<div>实体层中的密封类定义中，Loading为什么用 object 而不是 data class，之前也在其他地方看过这种用法，没理解是有什么特别含义还是二者皆可混用，还请解惑。</div>2022-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a4/ee/cffd8ee6.jpg" width="30px"><span>魏全运</span> 👍（4） 💬（1）<div>MVVM+Clean架构的组合使得原先在VM里的数据处理逻辑转移到了usecase，这样VM的逻辑更加精简且清晰，并且由于clean架构的引入，数据层的代码将更加可测。但是，clean架构的缺点也很明显：代码臃肿、结构复杂。实际项目中很少会使用clean架构来实现一个业务模块。</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b3/d5/93b704b6.jpg" width="30px"><span>sunlight</span> 👍（2） 💬（1）<div>还有其他这么好的Android课程推荐么，这门课程收获很多。最近没东西看了。。</div>2022-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5a/75/4e0d7419.jpg" width="30px"><span>飓风</span> 👍（2） 💬（1）<div>usecase的好处感觉可以单元测试，一般我都是省去了直接在viewmodel单独定义一个suspend方法用来做单元测试，不知道还有没有其他好的方案可以对viewmodel做单元测试</div>2022-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b3/d5/93b704b6.jpg" width="30px"><span>sunlight</span> 👍（2） 💬（3）<div>想请教下老师，一般view中对应一个viewModel还是多个viewModel，这个有统一标准吗</div>2022-05-05</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（2） 💬（2）<div>MVVM和Clean架构的融合，相对于原来逻辑都在Activity里，实现了较好的分层，单元测试也容易多了。相对于MVP架构，MVVM架构避免了presenter和view里面来回穿梭的调用，简化了逻辑，而且得到谷歌较好的支持。MVVM架构在Android系统中的问题是，Andorid应用多是UI重度型应用，UI中的逻辑太多，分层解决的主要是非UI部分的代码，对于UI部分的分层，方法论层面就没有系统的支持，实践中的自动化测试也很不方便。Jetpack Compose在一定程度上，提供了UI模块化的解决方案，但是自动化测试也远比非UI的单元测试要复杂。这方面我不太熟，期待老师将来的精彩讲解。
</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/e5/e1/a5064f88.jpg" width="30px"><span>Geek_Adr</span> 👍（1） 💬（1）<div>我理解 解决复杂问题通用方法就是拆分或者说是分层，不管是MVVM或是Clean都是分层方法的一种，如何选择主要看复杂度。MVP或MVVM 可以理解为UI交互与业务逻辑 对等复杂度的分法，MVVM与Clean混合架构更重业务逻辑轻UI交互的分法，所以优点：应用在复杂业务场景合适，缺点：分层本身就需要理解，带来额外复杂度。HelloWorld 直写就好</div>2022-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/4a/5a/14eb7973.jpg" width="30px"><span>杨小妞</span> 👍（1） 💬（1）<div>个人理解：对于数据处理不是很复杂的场景，UseCase一般用得很少，直接在vm完成数据请求处理然后就抛出去了。
有一个设想，对于UI很复杂的页面，将其粗略拆分成上、中、下三个Delegate（包含UI+业务），这样Activity任务处理就能减轻不少。</div>2022-04-13</li><br/><li><img src="" width="30px"><span>Geek_12f95b</span> 👍（0） 💬（1）<div>老师，问下你这个架构图 用啥软件画的呀</div>2022-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c6/78/9b1e4b15.jpg" width="30px"><span>ZircoN</span> 👍（0） 💬（1）<div>usecase google推荐是封装复杂逻辑或者逻辑复用时使用，正常情况如上面例子是可以去掉这一层的。</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/61/54/31a8d7e6.jpg" width="30px"><span>anmi</span> 👍（0） 💬（0）<div>试着拉了一下github代码，编译后没法正常用，因为api似乎已经停止维护了</div>2024-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6d/2f/ed8db646.jpg" width="30px"><span>Fred</span> 👍（0） 💬（0）<div>try { Success(RetrofitClient.service.repos()) } catch (e: Exception) { Log.e(TAG, e.message, e) Error(e) }  这个地方有更优的写法吗? 每一处都要写这个try ... catch 不太好</div>2023-07-12</li><br/><li><img src="" width="30px"><span>Kevin</span> 👍（0） 💬（1）<div>这个实战项目能给出git地址查看代码吗</div>2022-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/01/2885812b.jpg" width="30px"><span>Michael</span> 👍（0） 💬（0）<div>如果这个 NULL 对应到我们的实体类的字段是 Int，Boolean，另一个对象 时，就需要写多个 NullXXXAdapter 么？</div>2022-07-04</li><br/>
</ul>