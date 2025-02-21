你好，我是何辉。首先祝你新年快乐。

今天是我们深入研究Dubbo源码的第五篇，Compiler 编译。

在“[点点直连](https://time.geekbang.org/column/article/613319)”中，我们实现了一套万能管控平台来修复数据，其中就有通过市场上的 Groovy 插件编译 Java 源代码来生成类信息。

而上一讲“[Wrapper 机制](https://time.geekbang.org/column/article/620918)”中，在实现自定义代理的时候，我们也使用了 JavaCompiler 来编译源代码，只不过编译的时候，借助了磁盘上的 class 文件才得以生成类信息。

掌握了这两种动态编译方式，相信你在动态编译这块已经有了一定的基础，如果你还是觉得有点胆怯，今天我们上点难度，再学习 2 种 Compiler 方式，帮助你在底层框架开发层面拥有更强大的技术支撑。

## Javassist 编译

还是以上一讲的自定义代理为例。这张图你应该还有印象，我们尝试通过添加一层代理的方式，把各种 if…else 的硬编码逻辑转变为动态生成：

![图片](https://static001.geekbang.org/resource/image/b9/fa/b91da4e352be6f6246763e738f5356fa.jpg?wh=5052x1791)

在实现自定义代理的过程中，我们采用的是最纯粹的字符串拼接的方式，拼接出了动态的源代码，虽然实用，但是写起来也费劲。

有没有通过 set 或 get 操作就能实现创建类的简单方式，来改造图中的代理实现过程呢？

我们在脑内检索一番，平常都是直接将编写好的代码交给 Javac 编译器去编译的，现在要通过某种工具简单的进行 set 或 get 动态创建一个类，怎么办呢，突然灵光一闪，在上一讲“Wrapper 机制的原理”代码流程中，我们看到了一段 makeClass 的样例代码，难道 Dubbo 已经有了类似的先进操作么？
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1d/85/d2/045c63fb.jpg" width="30px"><span>王建新</span> 👍（0） 💬（1）<div>上一节和这一节讲的完全不搭边呀，最主要的核心关联没说上，ASM语法代码写了那么多看那干啥。。。</div>2023-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/09/1e/fc5144ff.jpg" width="30px"><span>王轲</span> 👍（0） 💬（1）<div>`...用 0表示，方法中的第一个参数用1 表示...` 这里看起来显示有误，应该是`...用 $0表示，方法中的第一个参数用$1 表示...`</div>2023-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/da/9a/ed524797.jpg" width="30px"><span>斯瓦辛武Roy</span> 👍（0） 💬（1）<div>老师春节好，请教个问题，再看官方文档的时候https:&#47;&#47;cn.dubbo.apache.org&#47;zh&#47;docsv2.7&#47;user&#47;references&#47;telnet&#47;
用了这个命令trace XxxService: 跟踪 1 次服务任意方法的调用情况
我调用自己本地的dubbo服务，但这个命令没有反应，请教一下老师这个是什么原因</div>2023-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/80/93/dde3d5f0.jpg" width="30px"><span>熊悟空的凶</span> 👍（0） 💬（1）<div>老师，新年好</div>2023-01-23</li><br/>
</ul>