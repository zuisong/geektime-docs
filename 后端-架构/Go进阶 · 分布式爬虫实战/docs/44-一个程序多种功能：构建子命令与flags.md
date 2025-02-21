你好，我是郑建勋。

之前，我们介绍了Worker的开发以及代码的测试，但之前的程序其实还是单机执行的。接下来让我们打开分布式开发的大门，一起看看如何开发Master服务，实现任务的调度与故障容错。

考虑到Worker和Master有许多可以共用的代码，并且关系紧密，所以我们可以将Worker与Master放到同一个代码仓库里。

## Cobra实现命令行工具

代码放置在同一个仓库后，我们遇到了一个新的问题。代码中只有一个main函数，该如何构建两个程序呢？其实，我们可以参考Linux中的一些命令行工具，或者Go这个二进制文件的处理方式。例如，执行go fmt代表执行代码格式化程序，执行go doc代表执行文档注释程序。

在本项目中，我们使用 [github.com/spf13/cobra](http://xn--github-hz8ig3bo82im51b.com/spf13/cobra) 库提供的能力构建命令行应用程序。命令行应用程序通常接受各种输入作为参数，这些参数也被称为子命令，例如go fmt中的fmt和go doc中的doc。同时，命令行应用程序也提供了一些选项或运行参数来控制程序的不同行为，这些选项通常被称为flags。

### Cobra实例代码

怎么用Cobra来实现命令行工具呢？我们先来看一个简单的例子。在下面这个例子中，cmdPrint、cmdEcho、cmdTimes 表示我们将向程序加入的3个子命令。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep075ibtmxMf3eOYlBJ96CE9TEelLUwePaLqp8M75gWHEcM3za0voylA0oe9y3NiaboPB891rypRt7w/132" width="30px"><span>shuff1e</span> 👍（5） 💬（1）<div>这是想到哪讲到哪么？课程大纲上44节不是讲微服务框架与协议的么？怎么又忽然来讲cobra？pflag？这种基础的工具放在前面讲会不会更好一些？</div>2023-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9c/fb/7fe6df5b.jpg" width="30px"><span>陈卧虫</span> 👍（1） 💬（0）<div>正好在写一个命令行工具，今天就用上了，但是遇到了一个问题，我需要实现交互式的，能多次用户输入，但是cobra好像只能在启动时指定参数，无法在运行中输入向Yes 或No这样的参数，有其它的方案吗（除了直接读取标准输入，我现在就这么做的）</div>2023-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/6d/3e570bb8.jpg" width="30px"><span>一打七</span> 👍（0） 💬（0）<div>为什么有时候是一个杠有时候是两个，有什么区别吗？-t=3    --http=:8081</div>2024-01-14</li><br/>
</ul>