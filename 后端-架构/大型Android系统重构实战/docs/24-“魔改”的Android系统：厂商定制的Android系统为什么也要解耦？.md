你好，我是黄俊彬。

上节课，我们了解了Android系统开发的基础框架、编译环境、开发工具等基础知识。这节课，让我们聚焦在架构设计层面，看看定制系统里最容易出现哪些架构耦合问题，这些问题又会给整机产品埋下哪些隐患。

想要分析架构层面的耦合问题，自然要先弄清楚规范的Android系统架构长什么样，就让我们从这里开始今天的内容吧！

## Android系统架构

做过Android系统定制开发的同学，一定会接触到AOSP。[AOSP](https://source.android.com/)，全称是Android Open Source Project，中文译为“Android 开放源代码项目”。厂商每年会基于Google开放的最新代码进行适配定制，开发属于自己的OS版本。

首先，我们根据Android的架构图来看看Android系统架构的设计。

![](https://static001.geekbang.org/resource/image/57/2a/57127fe2f0a68534fb104467d983842a.jpg?wh=3104x3083 "图片来自Google官网介绍 https://source.android.com/docs/core/architecture")

对照架构图，我们从上到下来看。在应用框架层上面应该还有一层，就是诸多的应用。

这些应用可以分为2类：一类是系统应用，拥有高的系统权限，可以调用系统提供的高权限接口，例如打电话、短信、设置等应用；另外一类就是非系统应用，与第三方应用一样，例如定制一些便签、运动健康、视频播放等应用。

接下来的第一层就是应用框架层，**应用框架最常被应用开发者使用，对应用提供标准的API来调用系统的能力，从而实现相关的业务功能。**我们在代码编译时，通常会依赖Android SDK的android.jar空包，保证能通过编译。但需要注意的是android.jar具体的实现都在框架层中，实际运行时调用的都是系统中的类。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_e0fb72</span> 👍（0） 💬（1）<div>应用与框架，框架与框架之间的解耦希望能提供些具体的思路和案例，谢谢</div>2023-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：“android.jar 空包”，空包是什么意思？另外，平时开发中，没有注意到引入了android.jar这个包啊，不管是具体类代码，还是gradle文件中，并没有import这个包。那这个包是怎么导入的？默认导入的吗？
Q2：文中的系统架构图，和最常见的安卓系统架构图，是不同的，HAL之上的分层不同，为什么？是不同的描述方法吗？（留言不能贴图，不过相信老师知道我说的“最常见的安卓系统架构图”是什么）
Q3：合规性问题，安卓APP开发完成后，要做合规性方面的工作吗？</div>2023-04-05</li><br/>
</ul>