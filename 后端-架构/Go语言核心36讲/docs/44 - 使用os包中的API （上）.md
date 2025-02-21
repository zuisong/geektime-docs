我们今天要讲的是`os`代码包中的API。这个代码包可以让我们拥有操控计算机操作系统的能力。

## 前导内容：os包中的API

这个代码包提供的都是平台不相关的API。那么说，什么叫平台不相关的API呢？

它的意思是：这些API基于（或者说抽象自）操作系统，为我们使用操作系统的功能提供高层次的支持，但是，它们并不依赖于具体的操作系统。

不论是Linux、macOS、Windows，还是FreeBSD、OpenBSD、Plan9，`os`代码包都可以为之提供统一的使用接口。这使得我们可以用同样的方式，来操纵不同的操作系统，并得到相似的结果。

`os`包中的API主要可以帮助我们使用操作系统中的文件系统、权限系统、环境变量、系统进程以及系统信号。

其中，操纵文件系统的API最为丰富。我们不但可以利用这些API创建和删除文件以及目录，还可以获取到它们的各种信息、修改它们的内容、改变它们的访问权限，等等。

说到这里，就不得不提及一个非常常用的数据类型：`os.File`。

从字面上来看，`os.File`类型代表了操作系统中的文件。但实际上，它可以代表的远不止于此。或许你已经知道，对于类Unix的操作系统（包括Linux、macOS、FreeBSD等），其中的一切都可以被看做是文件。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/2d/36/d3c8d272.jpg" width="30px"><span>HF</span> 👍（8） 💬（1）<div>老师，高级语言的标准库实现方式有哪些？用到的系统服务是封装系统调用还是用系统库函数</div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（7） 💬（1）<div>郝林老师能简单说一下demo87.go 中的 ：reflect.TypeOf((*io.ReadWriteSeeker)(nil)).Elem() 运作流程吗？ 感觉这种写法还挺特别的。
</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>郝林老师，demo87.go 样例中好像少了这一段 关闭文件的代码：

defer file3.Close()</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/48/97/520f3511.jpg" width="30px"><span>Walking In The Air</span> 👍（30） 💬（0）<div>最希望老师把net包内极相关的包讲解一下，这部分用的最频繁，但是总有一种似懂非懂的感觉，只是知道是这样用，不知道为什么，对底层知识不清晰，没有一个轮廓</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7c/e5/3dca2495.jpg" width="30px"><span>上山的o牛</span> 👍（2） 💬（0）<div>同求net包讲解</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ac/95/9b3e3859.jpg" width="30px"><span>Timo</span> 👍（0） 💬（0）<div>打卡</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/b2/1f914527.jpg" width="30px"><span>海盗船长</span> 👍（0） 💬（0）<div>打卡</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（0） 💬（0）<div>打卡</div>2019-03-13</li><br/>
</ul>