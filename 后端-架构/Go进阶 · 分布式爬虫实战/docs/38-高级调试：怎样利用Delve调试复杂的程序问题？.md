你好，我是郑建勋。

工欲善其事，必先利其器。这节课，我们来看看怎么合理地使用调试器让开发事半功倍。调试器能够控制应用程序的执行，它可以让程序在特定的位置暂停并观察当前的状态，还能够控制单步执行代码和指令，以便观察程序的执行分支。

当我们谈到调试器，一些有经验的开发可能会想到GDB，不过在Go语言中，我们一般会选择使用Delve（dlv）。这不仅因为Delve比 GDB 更了解 Go 运行时、数据结构和表达式，还因为Go中栈扩容等特性会让[GDB得到错误的结果](https://go.dev/doc/gdb)。所以这节课，我们就主要来看看如何利用Delve完成Go程序的调试。

## Delve的内部架构

我们先来看看[Delve](https://github.com/go-delve/delve)的内部架构。Delve本身也是用Go语言实现的，它的内部可以分为3层。

- UI Layer

UI layer 为用户交互层，用于接收用户的输入，解析用户输入的指令。例如打印变量信息时用户需要在交互层输入print a。

- Symbolic Layer

Symbolic Layer用于解析用户的输入。例如对于print a这个打印指令，变量a可能是结构体、int等多种类型，Symbolic Layer负责将变量a转化为实际的内存地址和它对应的字节大小，最后通过Target Layer层读取内存数据。同时，Symbolic Layer也会把从Target Layer中读取到的数据解析为对应的结构、行号等信息。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/9c/fb/7fe6df5b.jpg" width="30px"><span>陈卧虫</span> 👍（1） 💬（3）<div>如果在远程容器中开发，如何用goland 连接远程容器中的dlv呢</div>2023-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fc/4f/0a452c94.jpg" width="30px"><span>大毛</span> 👍（0） 💬（0）<div>不建议将 Delve 用在线上环境中，因为断点会阻塞程序的运行，如果你的断点打在了核心位置上，这个断点会阻塞线上环境中所有协程的运行。

最近正在思考当爬虫被阻塞后要如何定位问题，使用 dlv attach 似乎是一个不错的选择</div>2024-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/6d/3e570bb8.jpg" width="30px"><span>一打七</span> 👍（0） 💬（1）<div>Goland远程调试时，dlv attach怎么用？这才是更多的场景</div>2024-01-12</li><br/>
</ul>