你好，我是郝林，今天我们继续分享使用os包中的API。

我们在上一篇文章中。从“`os.File`类型都实现了哪些`io`包中的接口”这一问题出发，介绍了一系列的相关内容。今天我们继续围绕这一知识点进行扩展。

## 知识扩展

### 问题1：可应用于`File`值的操作模式都有哪些？

针对`File`值的操作模式主要有只读模式、只写模式和读写模式。

这些模式分别由常量`os.O_RDONLY`、`os.O_WRONLY`和`os.O_RDWR`代表。在我们新建或打开一个文件的时候，必须把这三个模式中的一个设定为此文件的操作模式。

除此之外，我们还可以为这里的文件设置额外的操作模式，可选项如下所示。

- `os.O_APPEND`：当向文件中写入内容时，把新内容追加到现有内容的后边。
- `os.O_CREATE`：当给定路径上的文件不存在时，创建一个新文件。
- `os.O_EXCL`：需要与`os.O_CREATE`一同使用，表示在给定的路径上不能有已存在的文件。
- `os.O_SYNC`：在打开的文件之上实施同步I/O。它会保证读写的内容总会与硬盘上的数据保持同步。
- `os.O_TRUNC`：如果文件已存在，并且是常规的文件，那么就先清空其中已经存在的任何内容。

对于以上操作模式的使用，`os.Create`函数和`os.Open`函数都是现成的例子。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/89/fc2aad72.jpg" width="30px"><span>心静梵音</span> 👍（2） 💬（1）<div>郝大大，咱们os&#47;exec和os&#47;signal包还会讲嘛？我看咱们的课程介绍上列了，是不是在其他讲讲过了？
</div>2018-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5c/f6/56d77359.jpg" width="30px"><span>SamuraiDeng</span> 👍（1） 💬（1）<div>权限，看的不是很懂，但是，我感觉跟Linux给文件加权限应该是一个出处</div>2021-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/80/b5/f59d92f1.jpg" width="30px"><span>Cloud</span> 👍（9） 💬（0）<div>func Syscall</div>2018-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/86/fb/4add1a52.jpg" width="30px"><span>兵戈</span> 👍（5） 💬（0）<div>思考题：怎样通过os包中的 API 创建和操纵一个系统进程？
个人思路如下：
1. os 包及其子包 os&#47;exec 提供了创建进程的方法
2. os&#47;proc.go 提供了不少获取进程属性的方法</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/c9/a7c77746.jpg" width="30px"><span>冰激凌的眼泪</span> 👍（5） 💬（0）<div>操作模式，限定了可以通过*File执行的操作
权限模式，对应操作系统上的文件权限</div>2018-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/17/96/a10524f5.jpg" width="30px"><span>蓬蒿</span> 👍（1） 💬（0）<div>怎样创建系统进程？通过cmd的api可以运行系统命令，其底层是系统调用fork和execv家族函数</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（0） 💬（0）<div>打卡</div>2019-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b7/f9/75bae002.jpg" width="30px"><span>manky</span> 👍（0） 💬（0）<div>跟linux文件访问规则差不多</div>2018-11-23</li><br/>
</ul>