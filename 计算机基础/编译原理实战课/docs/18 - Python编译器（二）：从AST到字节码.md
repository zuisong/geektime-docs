你好，我是宫文学。

今天这一讲，我们继续来研究Python的编译器，一起来看看它是如何做语义分析的，以及是如何生成字节码的。学完这一讲以后，你就能回答出下面几个问题了：

- **像Python这样的动态语言，在语义分析阶段都要做什么事情呢，跟Java这样的静态类型语言有什么不同？**
- **Python的字节码有什么特点？生成字节码的过程跟Java有什么不同？**

好了，让我们开始吧。首先，我们来了解一下从AST到生成字节码的整个过程。

## 编译过程

Python编译器把词法分析和语法分析叫做“**解析（Parse）**”，并且放在Parser目录下。而从AST到生成字节码的过程，才叫做“**编译（Compile）**”。当然，这里编译的含义是比较狭义的。你要注意，不仅是Python编译器，其他编译器也是这样来使用这两个词汇，包括我们已经研究过的Java编译器，你要熟悉这两个词汇的用法，以便阅读英文文献。

Python的编译工作的主干代码是在Python/compile.c中，它主要完成5项工作。

**第一步，检查**[**future语句**](https://docs.python.org/3/reference/simple_stmts.html#future-statements)。future语句是Python的一个特性，让你可以提前使用未来版本的特性，提前适应语法和语义上的改变。这显然会影响到编译器如何工作。比如，对于“8/7”，用不同版本的语义去处理，得到的结果是不一样的。有的会得到整数“1”，有的会得到浮点数“1.14285…”，编译器内部实际上是调用了不同的除法函数。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/54/ad/6ee2b7cb.jpg" width="30px"><span>Jacob.C</span> 👍（5） 💬（0）<div>答题：因为python变量的语义设计是“定义-使用”，不存在先使用再定义的情况，所以不用担心这种情况下的消解错误</div>2020-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/11/fa/e0dcc1bf.jpg" width="30px"><span>榕</span> 👍（0） 💬（0）<div>思考题：我的理解是Python在添加符号的时候已经通过标志位对符号做了标记，所以后面做引用消解可通过标志位区分。</div>2021-07-23</li><br/>
</ul>