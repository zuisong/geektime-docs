你好，我是宫文学。

前面两讲中，我介绍了Sea of Nodes类型的HIR，以及基于HIR的各种分析处理，这可以看做是编译器的中端。

可编译器最终还是要生成机器码的。那么，这个过程是怎么实现的呢？与硬件架构相关的LIR是什么样子的呢？指令选择是怎么做的呢？

这一讲，我就带你了解Graal编译器的后端功能，回答以上这些问题，破除你对后端处理过程的神秘感。

首先，我们来直观地了解一下后端处理的流程。

## 后端的处理流程

在[第14讲](https://time.geekbang.org/column/article/256914)中，我们在运行Java示例程序的时候（比如`atLeastTen()`方法），使用了“`-Dgraal.Dump=:5`”的选项，这个选项会dump出整个编译过程最详细的信息。

对于HIR的处理过程，程序会通过网络端口，dump到IdealGraphVisualizer里面。而后端的处理过程，缺省则会dump到工作目录下的一个“`graal_dumps`”子目录下。你可以用文本编辑器打开查看里面的信息。

```
//至少返回10
public int atLeastTen(int a){
    if (a < 10)
        return 10;
    else
        return a;    
}
```

不过，你还可以再偷懒一下，使用一个图形工具[c1visualizer](http://lafo.ssw.uni-linz.ac.at/c1visualizer/)来查看。

补充：c1visualizer原本是用于查看Hopspot的C1编译器（也就是客户端编译器）的LIR的工具，这也就是说，Graal的LIR和C1的是一样的。另外，该工具不能用太高版本的JDK运行，我用的是JDK1.8。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1c/68/fd/0a64b003.jpg" width="30px"><span>智昂张智恩震😱</span> 👍（4） 💬（1）<div>请问和JVM握手就是插入safe point的过程吗？具体的握手是在做什么？</div>2020-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/85/70/8f05f04b.jpg" width="30px"><span>手抓饼熊</span> 👍（3） 💬（1）<div>老师能否再开个专栏专门将graal的？这2门课讲的太好了，广度也非常好，如果再挑一个深度讲讲就很完美了，现在市面上对jit，编译优化和后端讲解的很少。</div>2020-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0a/83/f916f903.jpg" width="30px"><span>风</span> 👍（0） 💬（1）<div>一些c工具链支持习语识别，能够识别源代码中的特定模式，并从源代码直接生成对应cpu的汇编代码，这类优化属于哪一环节？</div>2020-12-24</li><br/>
</ul>