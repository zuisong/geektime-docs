前不久，有同学问我，`String.indexOf`方法和自己实现的`indexOf`方法在字节码层面上差不多，为什么执行效率却有天壤之别呢？今天我们就来看一看。

```
public int indexOf(String str) {
    if (coder() == str.coder()) {
        return isLatin1() ? StringLatin1.indexOf(value, str.value)
                          : StringUTF16.indexOf(value, str.value);
    }
    if (coder() == LATIN1) {  // str.coder == UTF16
        return -1;
    }
    return StringUTF16.indexOfLatin1(value, str.value);
}
```

为了解答这个问题，我们来读一下`String.indexOf`方法的源代码（上面的代码截取自Java 10.0.2）。

> 在Java 9之前，字符串是用char数组来存储的，主要为了支持非英文字符。然而，大多数Java程序中的字符串都是由Latin1字符组成的。也就是说每个字符仅需占据一个字节，而使用char数组的存储方式将极大地浪费内存空间。
> 
> Java 9引入了Compact Strings\[1]的概念，当字符串仅包含Latin1字符时，使用一个字节代表一个字符的编码格式，使得内存使用效率大大提高。

假设我们调用`String.indexOf`方法的调用者以及参数均为只包含Latin1字符的字符串，那么该方法的关键在于对`StringLatin1.indexOf`方法的调用。

下面我列举了`StringLatin1.indexOf`方法的源代码。你会发现，它并没有使用特别高明的算法，唯一值得注意的便是方法声明前的`@HotSpotIntrinsicCandidate`注解。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/2e/9b/84370b68.jpg" width="30px"><span>^_^</span> 👍（18） 💬（1）<div>我个人觉得老师讲的非常好，这些东西更像是讲解一个系统似的，让我们更懂他们的运行机制，推算出我们系统每个类、方法和属性在jvm上的运作模式。这课程真的对于我们java开发的真的是太有帮助了，不想某某些课程占着实践经验的名义混。感谢老师辛苦啦！</div>2018-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（17） 💬（2）<div>赞，之前学习了深入理解计算机原理这门课，再联系这一节就知道intrinsic想做什么了。
JVM 自身不是跨平台的，Windows，Linux都有各自的安装包，也就是JVM帮我们做了不同操作系统及底层体系结构的兼容；但是针对每一个具体的CPU，其自身提供的指令，寄存器，以及SIMD等优化机制并没有得到利用，而intrinsic的产生正是为了利用这些。
个人理解，有不对之处，请老师和各位同学指出。</div>2019-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bf/0a/98e116e0.jpg" width="30px"><span>Geek_09d838</span> 👍（6） 💬（1）<div>我觉得有些功能你要先知道，再去考虑能否会用到这些功能。</div>2018-09-10</li><br/><li><img src="" width="30px"><span>Scott</span> 👍（5） 💬（1）<div>我还是看得蛮过瘾的，周一三五早上起来第一件事就是看更新，的确可能不是很实用，但是对于对虚拟机感兴趣的同学来讲，是满足了好奇心</div>2018-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ef/84/a0ffbd8b.jpg" width="30px"><span>白三岁</span> 👍（3） 💬（1）<div>我看了下java8中没有找到这个注解。调用从源码复制出来的方法和直接调用源码的方法没有性能上的差别。是java8没有加入这种优化吗</div>2018-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9b/2f/b7a3625e.jpg" width="30px"><span>Len</span> 👍（3） 💬（1）<div>我觉得老师讲的非常好，尤其是上两讲讲方法内联，结合老师讲的，在课后我又恶补了一下 IR 方面的知识，收获很大。
尽管目前我的工作不会直接用到这方面的知识，但我相信这些底层机制、原理性的知识点，对成长为一名优秀的工程师是必备的。</div>2018-09-10</li><br/><li><img src="" width="30px"><span>ahern88</span> 👍（3） 💬（3）<div>我觉得这份虚拟机教程写的知识有点偏，不够实用，大家觉得呢</div>2018-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/af/d29273e2.jpg" width="30px"><span>饭粒</span> 👍（2） 💬（2）<div>文中说 @HotSpotIntrinsicCandidate 如果不是 HotSpot 的虚拟机就退化使用 JDK 源码的方式。但如果某个 @HotSpotIntrinsicCandidate 注解的方法 X86_64 有指令可以优化，但其他架构体系比如 AMD64 没有相应的指令或者指令不同这个过程是怎样的？</div>2019-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/ba/d738255c.jpg" width="30px"><span>JZ</span> 👍（0） 💬（1）<div>Java8中并没有看到相应的注解，如String类的indexOf方法，Java8中没有类似的优化？</div>2018-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/e3/abb7bfe3.jpg" width="30px"><span>bradsun</span> 👍（0） 💬（1）<div>这个为什么不都是独立的形式。而且只有少部分是独立的。谢谢</div>2018-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（11） 💬（5）<div>嗯，JVM的重要性自不必言，学好是进阶的台阶，否则就是屏障。不知道运行原理和机制，怎么理解OOM？怎么优化性能？怎么分析和定位一些奇怪的问题？

老师讲的相当好了，只是知识储备不够的话，学习曲线是比较陡峭的，比如IR图，那个是第一次听，来龙去脉都不清楚自然会懵逼。还好大部分都能听明白和吸收，只是以后面试能判断出面试官的水平。

懂JVM我感觉就好像了解地球是圆的以及围绕太阳公转一样，好像平时生活上也没什么用，不过如果想要征服星辰大海，以及迷失方向时还是挺有用的。

嗯，总之，老师讲的非常好，毕竟只是一个专栏的入门教程，已经如此深入了，相当有用，这也是我付费了第一个专栏，由于老师讲的好，我在极客时间又订阅的好多，现在已看不过来了，不过这个专栏我一直没断，每天必听必看，感觉学到不少知识。

嗯，今天讲解的 intrinsic ，我感觉也听明白了，总结一下：
1:intrinsic-可认为也是一种hotspot虚拟机，为提高JVM性能的优化机制或技巧

2:使用注解的方式来和Java代码结合

3:本质上适配出对应系统体系架构，然后直接使用和系统体系架构强关联的高效指令来执行对应的功能

4:针对不同的类具体的高效指令亦不同

疑问❓
1:intrinsic 是只有hotspot虚拟机支持吗？

2:系统的体系架构适配是唯一的吗？主要是x86_64？按照这个思路是不是可以有多个类似的注视，针对多种的系统体系架构来优化呢？毕竟计算机系统的体系架构是有限的</div>2018-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/e3/abb7bfe3.jpg" width="30px"><span>bradsun</span> 👍（2） 💬（0）<div>不好意思，昨天没写清楚。就是intrinsic，只有少部分可以直接被解释器应用，而大部分只能被编译器应用。为什么不都可以被解释器调用，这样解释执行的时候不会更高效吗</div>2018-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/a6/9f/3c60fffd.jpg" width="30px"><span>青阳</span> 👍（0） 💬（0）<div>intrinsic就是有些功能硬件已经实现了，不用软件编程的方式实现了</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/01/1c/d638d46e.jpg" width="30px"><span>宋世通</span> 👍（0） 💬（0）<div>打开了新世界的大门</div>2021-08-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/hQ01GRPRFNTfBWX1Gmz0cqXZxbyJqHmORNJuE8yIqCbg1fXjvaWOGoatVo3Pbib5ZHCEqYFhSHhCVA8zr2Q2WuA/132" width="30px"><span>Geek_03a866</span> 👍（0） 💬（0）<div>将编码、即时编译器、cpu指令体系架构、并发unsafe、natuve jni  之间的过渡讲深入和清楚了，水平真高</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/c5/29/4848464f.jpg" width="30px"><span>兰芳林</span> 👍（0） 💬（0）<div>厉害，受教</div>2020-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（0） 💬（0）<div>这篇大概讲的就是说，有很多@HotSpotIntrinsicCandidate注解的方法。我们叫他intrinsic，这些方法特别之处就是基于CPU啥的指令高效运行。
这时候就会有一个问题，会不会换个构架的硬件或者说不支持对应的指令集，这些东西就玩不转了，有时候遇到一些需求比如说打印，有的机器打印标签不支持重定位，打着打着就会出现偏差，有对应的指令但是硬件不支持。</div>2020-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fc/04/d83a555e.jpg" width="30px"><span>Kevin⚡️Zhou</span> 👍（0） 💬（0）<div>这门课我觉得可以先囫囵吞枣的看过去, 以后开发中遇到了具体的疑问在来回顾, 对于经验不是很长的工程师来说, 想一次性全部吃透是很难得</div>2020-07-30</li><br/><li><img src="" width="30px"><span>伍春林</span> 👍（0） 💬（0）<div>老师好，文中提到绝大部分intrinsic方法都是在及时编译的时候被替换的，那是不是意味着如果没有触发及时编译的话，intrinsic方法的高效实现就体现不了呢？</div>2020-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/de/e28c01e1.jpg" width="30px"><span>剑八</span> 👍（0） 💬（0）<div>intrinsic，就是利用CPU底层指令高效完成目标事情。
如：String的indexOf
可以利用CPU指令直接将byte数组存入底层寄存器由CPU指令进行比较并返回相应的index。</div>2020-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/66/e9/814d057a.jpg" width="30px"><span>小陈</span> 👍（0） 💬（0）<div>这节不错，讲了很多底层知识</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/30/c9b568c3.jpg" width="30px"><span>NullPointer</span> 👍（0） 💬（0）<div>这些东西听着挺过瘾的，虽然大部分时间用不上。但是理解原理，在你查找疑难问题的时候却是有奇效</div>2019-09-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ABjAPveWxOuBs3ibbCaBicX7OSibic3prycYG9vOicGHMEv8Vws5o3epykBSFHkbysnaKeMqQaJufINNUncGhmAEomg/132" width="30px"><span>雪人</span> 👍（0） 💬（0）<div>这些东西，尽管现在可能看起来不会都懂，但留着以后无论什么时候再看，都会有或多或少的收获，而这个收获，对以后的前进之路，是有非常大的帮助，感谢老师，希望老师有空能再出一份专栏吧</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/c4/270db3ad.jpg" width="30px"><span>ZoQ-tans</span> 👍（0） 💬（0）<div>第三部分，利用工具进行调优，非常期待，其实像PrintCompile这类参数也是十分实用的</div>2018-09-12</li><br/>
</ul>