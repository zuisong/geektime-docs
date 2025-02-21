你好，我是朱涛。在过去的几十讲里，我们把Kotlin的基础语法和核心难点协程，都全面学习了一遍，从原理到实战，从协程的核心挂起函数、launch等，到探究它们的源码定义，可以说我们已经基本掌握了Kotlin的核心知识点与特性，你也应该可以在工作中使用Kotlin来解决实际问题了。如果你发现自己对这些知识的掌握还有不少漏洞，也别着急，可以再回头复习一下相应部分的内容，或者在留言区提问，我会给你解答。

那么，从这节课起，我会带你来看看Kotlin在实践场景中，应用得最普遍、最广泛的领域，**Android**。我们一起来学习下如何结合所学的Kotlin知识，来高效开发Android应用。

今天这节课，我们先来聊聊Kotlin和Android的关系，让你对Android的现状与未来的发展方向有一个清晰的认识。

虽然Kotlin是面向多个平台的（如JVM、Native、JS等），不过我们在讨论Kotlin的同时，难免也会讨论下Android。甚至，很多开发者都是因为Android才开始接触Kotlin的。

说起Kotlin与Android，就不得不提它俩对应的公司JetBrains和Google。早在2013年之前，这两家公司就有过合作。最开始的时候，Android开发者的开发工具还是Eclipse，Google是在JetBrains的IntelliJ的基础上，进行改造以后，才有了后来的Android Studio。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="" width="30px"><span>Paul Shan</span> 👍（3） 💬（1）<div>我参与开发的项目已经全面拥抱Compose，过程中遇到很多问题，例如多行的Textview想在右边显示一个垂直的滑动条，我仔细找了一下，没找到解决方案，只能用AndroidView+xml+android:scrollbars=&quot;vertical&quot;,老师如果知道解决方案，望不吝赐教。我还遇到一个情况，MutableState按照谷歌的文档，里面值改变（value指向新的对象）的时候，会recompose。但是在实际的某些UI响应中改变值却没有recompose，导致状态没有更新。这个问题困扰了我很久，一度让我认为Compose还没有成熟到可以解决复杂的UI问题，后来发现把MutableState里面的对象拆成简单类型（例如整型，字符串）可以解决问题。这种写法破坏了类的内聚性，但是Compose还有bug的情况下不得不做出妥协。

Compose 遇到的最大问题就是思路的转变，原来的view类都是一个个有状态的对象，对象之间有复杂的继承关系，把他们全转成函数，我没有找到通用的方法，只能特事特办。例如，我遇到一个树状的UI，里面的view是父子结构，最终转化成Compose的时候用了递归函数。老师如果有机会的话可否在多讲一些Kotlin函数式编程的内容，个人觉得Kotlin函数式编程是Android开发人员将来不得不掌握的内容，函数式编程本身又是一个很大的的课题，值得大书特书。
</div>2022-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cc/f3/5e4b0315.jpg" width="30px"><span>追梦小乐</span> 👍（2） 💬（1）<div>老师，Compose 在国内应用的广吗？！</div>2022-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/47/b0/8c301d00.jpg" width="30px"><span>H.ZWei</span> 👍（2） 💬（2）<div>老师能对讲讲鸿蒙的看法吗，前几天在官网的文档看到，华为好像也在慢慢抛弃Java，在鸿蒙3.0上重点更新Js的环境，据说3.0开始会不兼容Android应用，未来在国内是不是会大量挤压Android的空间。</div>2022-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c6/78/9b1e4b15.jpg" width="30px"><span>ZircoN</span> 👍（0） 💬（1）<div>卡顿检测框架 LeakCanary -&gt; 内存泄露检测框架 LeakCanary</div>2022-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/91/d0/35bc62b1.jpg" width="30px"><span>无咎</span> 👍（1） 💬（0）<div>好久不写Android应用，最近想写了，发现涉及到Kotlin的代码越来越多了，虽然看了基本语法，还是没有把握，所以只好来学习课程了。
与其被动裹挟，不如主动拥抱变化，认真学习，积极实践。
当然转换思路，切换语言和库也是有成本的，但也是值得的，有些常见问题甚至没有现成方案，也没什么好怕的，耐心逐步解决。</div>2022-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ed/c5/036cb044.jpg" width="30px"><span>墨水</span> 👍（0） 💬（0）<div>我是脑子一热自己的应用上了kotlin，由于理解的不到位狠狠的被kotlin虐了一把</div>2023-06-16</li><br/>
</ul>