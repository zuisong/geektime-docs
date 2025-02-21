你好，我是宫文学。这一讲，我们继续来研究Graal编译器，重点来了解一下它的IR的设计。

在上一讲中，我们发现Graal在执行过程中，创建了一个图的数据结构，这个数据结构就是Graal的IR。之后的很多处理和优化算法，都是基于这个IR的。可以说，这个IR是Graal编译器的核心特性之一。

**那么，为什么这个IR采用的是图结构？它有什么特点和优点？编译器的优化算法又是如何基于这个IR来运行的呢？**

今天，我就带你一起来攻破以上这些问题。在揭晓问题答案的过程中，你对真实编译器中IR的设计和优化处理过程，也就能获得直观的认识了。

## 基于图的IR

IR对于编译器非常重要，因为它填补了高级语言和机器语言在语义上的巨大差别。比如说，你在高级语言中是使用一个数组，而翻译成最高效的x86机器码，是用间接寻址的方式，去访问一块连续的内存。所以IR的设计必须有利于实现这种转换，并且还要有利于运行优化算法，使得生成的代码更加高效。

在上一讲中，通过跟踪Graal编译器的执行过程，我们会发现它在一开始，就把字节码翻译成了一种新的IR，这个IR是用图的结构来表示的。那这个图长什么样子呢？非常幸运的是，我们可以用工具来直观地看到它的结构。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKdzXiawss5gGiax48CJGAJpha4pJksPia7J7HsiatYwjBA9w1bkrDicXfQz1SthaG3w1KJ2ibOxpia5wfbQ/132" width="30px"><span>chris</span> 👍（1） 💬（1）<div>老师会讲一下从字节码到graal ir的生成过程吗？</div>2020-07-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/jsMMDDzhbsTzhicsGZiaeV0PWSnAS0fBlb1r6CsuB32vr3hRwV9UubmfHQx45v7jtaXajPlQ8kQ17b3zpQzHmqVw/132" width="30px"><span>fy</span> 👍（0） 💬（1）<div>太硬核了</div>2021-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/36/ac0ff6a7.jpg" width="30px"><span>wusiration</span> 👍（0） 💬（1）<div>指令排序以及缓存优化，这两种优化方法需要分析出代码控制依赖和数据依赖的关系。</div>2020-07-04</li><br/>
</ul>