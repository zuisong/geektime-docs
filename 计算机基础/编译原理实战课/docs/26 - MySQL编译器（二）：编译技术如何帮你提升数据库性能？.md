你好，我是宫文学。今天这一讲，我们继续来探究MySQL编译器。

通过上一讲的学习，你已经了解了MySQL编译器是怎么做词法和语法分析的了。那么在做完语法分析以后，MySQL编译器又继续做了哪些处理，才能成功地执行这个SQL语句呢？

所以今天，我就带你来探索一下MySQL的实现机制，我会把重点放在SQL的语义分析和优化机制上。当你学完以后，你就能真正理解以下这些问题了：

- 高级语言的编译器具有语义分析功能，那么MySQL编译器也会做语义分析吗？它有没有引用消解问题？有没有作用域？有没有类型检查？
- MySQL有没有类似高级语言的那种优化功能呢？

好，让我们开始今天的探究吧。不过，在讨论MySQL的编译过程之前，我想先带你了解一下MySQL会用到的一些重要的数据结构，因为你在解读代码的过程中经常会见到它们。

## 认识MySQL编译器的一些重要的数据结构

**第一组数据结构**，是下图中的几个重要的类或结构体，包括线程、保存编译上下文信息的LEX，以及保存编译结果SELECT\_LEX\_UNIT和SELECT\_LEX。

![](https://static001.geekbang.org/resource/image/cc/b7/ccd4a2dcae0c974b0b5254c51440f9b7.jpg?wh=2284%2A1215)

图1：MySQL编译器的中的几个重要的类和结构体

**首先是THD，也就是线程对象。**对于每一个客户端的连接，MySQL编译器都会启动一个线程来处理它的查询请求。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/c6/958212b5.jpg" width="30px"><span>sugar</span> 👍（3） 💬（1）<div>浏览器中的html+css 作为ui界面样式，也是一种实用很广泛的dsl。特别是css3 、或一些预处理css工具所衍生出的css方言都会带有表达式计算 甚至自定义函数的能力。</div>2020-08-03</li><br/><li><img src="" width="30px"><span>myrfy</span> 👍（1） 💬（1）<div>正则表达式，sed、awk等文本编辑用的命令行工具。</div>2020-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a6/60/0eac2751.jpg" width="30px"><span>52rock</span> 👍（0） 💬（0）<div>了解引用消解是怎么回事了</div>2020-08-29</li><br/>
</ul>