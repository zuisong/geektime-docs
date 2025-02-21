你好，我是陈航。今天，我们来聊一聊Flutter应用的工程架构这个话题。

在软件开发中，我们不仅要在代码实现中遵守常见的设计模式，更需要在架构设计中遵从基本的设计原则。而在这其中，DRY（即Don’t Repeat Yourself）原则可以算是最重要的一个。

通俗来讲，DRY原则就是“不要重复”。这是一个很朴素的概念，因为即使是最初级的开发者，在写了一段时间代码后，也会不自觉地把一些常用的重复代码抽取出来，放到公用的函数、类或是独立的组件库中，从而实现代码复用。

在软件开发中，我们通常从架构设计中就要考虑如何去管理重复性（即代码复用），即如何将功能进行分治，将大问题分解为多个较为独立的小问题。而在这其中，组件化和平台化就是客户端开发中最流行的分治手段。

所以今天，我们就一起来学习一下这两类分治复用方案的中心思想，这样我们在设计Flutter应用的架构时也就能做到有章可循了。

## 组件化

组件化又叫模块化，即基于可重用的目的，将一个大型软件系统（App）按照关注点分离的方式，拆分成多个独立的组件或模块。每个独立的组件都是一个单独的系统，可以单独维护、升级甚至直接替换，也可以依赖于别的独立组件，只要组件提供的功能不发生变化，就不会影响其他组件和软件系统的整体功能。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/89/e3/aa57d3b2.jpg" width="30px"><span>小水滴</span> 👍（2） 💬（1）<div>请问有没有好的方式检测组件之间循环依赖或者层级依赖错误呢，这样可以在开发阶段来规避团队错误的使用方式</div>2019-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/23/74/e0b9807f.jpg" width="30px"><span>小米</span> 👍（0） 💬（1）<div>老师，关于架构这一讲，有没有demo可以参考一下？</div>2019-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/56/83/7cefd6b7.jpg" width="30px"><span>白</span> 👍（0） 💬（2）<div>请问 我目前所做 架构设计稍有不同  第一层是各个模块儿页面 -&gt;各个独立的UI组件(选项卡，slider，bottomSheet,轮播图等等...)-&gt;业务逻辑（provider中做逻辑处理然后通知页面）-&gt;基础能力模块(网络，加解密，数据存储等...)  ，这种方式会有什么隐患或者不足么？</div>2019-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/56/83/7cefd6b7.jpg" width="30px"><span>白</span> 👍（0） 💬（1）<div>我在做的App静态资源类主要包括image,color ,icon font ,svg,animation，多语言词条以及一些静态的.json文件，目前我的做法是会写一个脚本去扫描对应的路径生成一个对应的索引类
ex:
class AnimationAssets {
 static const String clock = &#39;assets&#47;animations&#47;xx.json&#39;;
 static const String gold = &#39;assets&#47;animations&#47;xx.json&#39;;
}</div>2019-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（2） 💬（0）<div>Dart 目前没有特别好用的图形工具可以用来分析依赖，你可以用 flutter pub deps 来打印工程的完整依赖树，配合简单的字符串扫描脚本，检查下是否存在依赖关系特别深，或是循环依赖的情况</div>2023-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/2a/7e/6d2e703b.jpg" width="30px"><span>小何</span> 👍（1） 💬（0）<div>感觉都是组件化和平台化结合的啊，平台化里面也在用组件化吧</div>2021-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/a1/9530ce70.jpg" width="30px"><span>陈士玉</span> 👍（0） 💬（0）<div>关于平台化的讲解深受启发，过去的工作中在组件化的基础上有下意识的运用平台化的一些思想（比如单向依赖），但是没有系统的思考过。非常有收获。</div>2023-11-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/lTPkR3OBWyffM5zl84FYoJI8cXhibA72T1LATMwwiaia6TjVqHMLElZcSyqibyQiceic6loVvovGzicj7gRtxTIJcRzAQ/132" width="30px"><span>bily</span> 👍（0） 💬（0）<div>和我目前设计的架构思想几乎一致</div>2020-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/89/a7/82827b76.jpg" width="30px"><span>outman</span> 👍（0） 💬（0）<div>请教一下，能不能将fluttet这个控件做成组件，比如一个Button ，然后在原生页面使用这个flutter做的button ？</div>2020-05-21</li><br/>
</ul>