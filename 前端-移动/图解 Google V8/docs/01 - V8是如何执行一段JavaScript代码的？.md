你好，我是李兵。

今天是我们整个课程的第一讲，我会从一个高层的宏观视角来解释什么是V8，以及V8又是怎么执行一段JavaScript代码的。在这个过程中，我会引入一些核心概念，诸如JIT、作用域、词法环境、执行上下文等，理解了这些概念，能够帮助你更好地理解V8是如何工作的，同时也能帮助你写出更加高效的JavaScript代码。

由于本节的目的是对V8做一个宏观的、全面的介绍，其目的是让你对V8的执行流程有个整体上的认识，所以涉及到的概念会比较多，如果你对其中一些概念不太理解也没有关系，在后面的章节中我会展开了详细地介绍。

## 什么是V8？

首先我们来看看什么是V8。

V8是一个由Google开发的开源JavaScript引擎，目前用在Chrome浏览器和Node.js中，其核心功能是执行易于人类理解的JavaScript代码。

![](https://static001.geekbang.org/resource/image/ca/4d/ca2cf22c8b2b322022666a3183db1b4d.jpg?wh=1142%2A222 "V8执行JavaScript")

那么V8又是怎么执行JavaScript代码的呢？

其主要核心流程分为编译和执行两步。首先需要将JavaScript代码转换为低级中间代码或者机器能够理解的机器代码，然后再执行转换后的代码并输出执行结果。

![](https://static001.geekbang.org/resource/image/b7/bf/b77593de2fc7754d146e1218c45ef2bf.jpg?wh=1142%2A393 "转换为中间代码")

你可以把V8看成是一个虚构出来的计算机，也称为虚拟机，虚拟机通过模拟实际计算机的各种功能来实现代码的执行，如模拟实际计算机的CPU、堆栈、寄存器等，虚拟机还具有它自己的一套指令系统。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/d8/6f/22e5ec55.jpg" width="30px"><span>零维</span> 👍（44） 💬（3）<div>想知道如何安装v8的同学可以参考这个链接：https:&#47;&#47;gist.github.com&#47;kevincennis&#47;0cd2138c78a07412ef21</div>2020-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/88/2e/db17801a.jpg" width="30px"><span>灰的更高</span> 👍（51） 💬（1）<div>老师，我有一个疑问。因为我看过了网上很多的关于v8编译的文章包括《WebKit技术内幕》这本书写道v8和javascriptcore的最重要的区别就是，v8不再将AST转成字节码或者是中间代码，而是直接转为本地代码，但在您的课程里面，好像很重要的一点就是AST转成了字节码文件，请老师能够答疑以下，谢谢</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（42） 💬（1）<div>著名的还有JVM以及luajit，包括oracle最新的graalVM都已经采用了JIT技术。</div>2020-03-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/EJZoM46wR6QqTeibhPZsO5wJTeUia4RndGicWfDZLw153WibjsnJXqEtGZICxAa8icb36pDkficTic3FViaySd1z9HmQBw/132" width="30px"><span>翰弟</span> 👍（29） 💬（1）<div>老师 全局执行上下文和全局作用域啥关系呢 </div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/0c/01fa3539.jpg" width="30px"><span>花生</span> 👍（17） 💬（2）<div>可以使用 jsvu 来安装 js 引擎

1. 全局安装 jsvu： npm install jsvu -g

2. 将~&#47;.jsvu路径添加到系统环境变量中：export PATH=&quot;${HOME}&#47;.jsvu:${PATH}&quot;

3. 可以直接通过命令参数指定： jsvu --os=mac64 --engines=v8-debug。</div>2020-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/72/18/d9e2fcf9.jpg" width="30px"><span>我来人间一趟</span> 👍（13） 💬（9）<div>老师 我有一点疑惑 就是解释器编译出的字节码 v8可以直接执行字节码 但是v8不过是模拟计算机执行嘛 最后都是要靠计算机的cpu和其他基础设施执行呀 如果这样的话 v8执行字节码是不是也会将字节码编译成机器吗执行呢？</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5d/74/2762a847.jpg" width="30px"><span>流乔</span> 👍（9） 💬（2）<div>请问老师，我想使用D8这个工具，我该如何操作？要下载源码编译吗？</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/31/bc/c4f31fa5.jpg" width="30px"><span>杨越</span> 👍（7） 💬（1）<div>d8在哪用呢，在控制台上用不了</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/61/68462a07.jpg" width="30px"><span>无名</span> 👍（6） 💬（3）<div>D8这个工具怎么编译在Mac下？或者是有现成的吗？</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/dc/19/c058bcbf.jpg" width="30px"><span>流浪地球</span> 👍（6） 💬（3）<div>请问老师是否可以把v8的源码构建环境搭建，构建和相关命令执行的知识做下介绍。</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/04/69/9236c63d.jpg" width="30px"><span>elias4ty</span> 👍（5） 💬（1）<div>解释器执行字节码，不也是要将字节码转换成二进制代码让 CPU 执行吗？这和编译器有啥区别</div>2020-05-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/EJZoM46wR6QqTeibhPZsO5wJTeUia4RndGicWfDZLw153WibjsnJXqEtGZICxAa8icb36pDkficTic3FViaySd1z9HmQBw/132" width="30px"><span>翰弟</span> 👍（5） 💬（1）<div>前文说解释器生成字节码？ 解释器不是执行字节码么</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/29/92/076e0f61.jpg" width="30px"><span>Silence</span> 👍（5） 💬（1）<div>java 的虚拟机也用到了 JIT</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/00/89/90d77632.jpg" width="30px"><span>廖彬</span> 👍（4） 💬（1）<div>我们把这种混合使用编译器和解释器的技术称为JIT，这个说法严格意义上来说不对吧。比如说早期V8并没有使用解释器技术，而使用了baseline的full codegen与crankshaft结合，这个也可以算是JIT。</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d8/6f/22e5ec55.jpg" width="30px"><span>零维</span> 👍（3） 💬（1）<div>老师，请问一下：解释和编译js代码的这个功能是属于V8的功能还是浏览器提供给v8的功能呢？
我产生这个疑问是因为《你不知道的js》这本书种讲述执行一段代码时分为了engine、compiler、scope manager三个名词。我认为engine是指的 v8，所以才产生了这个疑问。</div>2020-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/22/b8c596b6.jpg" width="30px"><span>风</span> 👍（3） 💬（3）<div>老师，v8是如何确定某段优化后的代码失效的？反优化是做了什么呢？</div>2020-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2c/07/636a47cd.jpg" width="30px"><span>慢慢来的比较快</span> 👍（3） 💬（1）<div>解释器把代码解释成字节码并执行吗？</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b9/5e/a8f6f7db.jpg" width="30px"><span>Ming</span> 👍（2） 💬（2）<div>JIT（Just In Time）技术在检测到热点代码之后，对中间代码优化编译成机器码，这时对于不同的 CPU，执行二进制指令表现会有差异吗？</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/ce/d9e00eb5.jpg" width="30px"><span>undefined</span> 👍（2） 💬（1）<div>JIT
---------------------
PHP -&gt; https:&#47;&#47;wiki.php.net&#47;rfc&#47;jit
HotSpot
Dalvik -&gt; https:&#47;&#47;android-developers.googleblog.com&#47;2010&#47;05&#47;dalvik-jit.html
Dart VM
PyPy
Ruby 2.6+
…</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6d/4f/e3158018.jpg" width="30px"><span>开心水牛</span> 👍（2） 💬（1）<div>PHP也是哦</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c5/01/9cd12725.jpg" width="30px"><span>孔宇飞</span> 👍（1） 💬（1）<div>请问一下老师，解释器执行中间代码和二进制文件交给CPU执行有什么区别？</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a9/64/819fccec.jpg" width="30px"><span>蔡孟泳</span> 👍（1） 💬（1）<div>在将代码编译为二进制代码后，如果该段代码之后数据结构格式变了会进行反优化，请问反优化的具体流程是什么样的？</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/29/92/076e0f61.jpg" width="30px"><span>Silence</span> 👍（1） 💬（1）<div>解释执行最后通过解释器输出的结果也是二进制吗？</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/b0/cabe4fa8.jpg" width="30px"><span>邦邦</span> 👍（0） 💬（1）<div>混合编译执行和解释执行 就是JIT？</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/b0/cabe4fa8.jpg" width="30px"><span>邦邦</span> 👍（0） 💬（4）<div>各种优化得到的运行高效是以花费更多的内存为代价的吧？</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（0） 💬（1）<div>使用了brew instal v8 安装了v8环境。 发现老师文中用的 d8 --print-scopes test.js 的命令是没有的。

只有一部分命令。 V8 version 8.0.426.27。是v8的版本不同导致的吗？谢谢。

今日收获：
V8执行JavaScript代码的过程，这块正好和上一个专栏中V8内容衔接起来了。</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ba/6b/517a286a.jpg" width="30px"><span>安辰</span> 👍（0） 💬（2）<div>遇到奇怪的问题
Warning: &quot;unknown&quot; flag --print-ast.</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/82/a4/a92c6eca.jpg" width="30px"><span>墨灵</span> 👍（0） 💬（1）<div>第一次听说d8，长见识了。</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/ce/d9e00eb5.jpg" width="30px"><span>undefined</span> 👍（0） 💬（4）<div>Warning: unknown flag --print-ast.
Try --help for options

是编译选项的问题？</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7f/14/ebe97682.jpg" width="30px"><span>小余GUNDAM</span> 👍（0） 💬（1）<div>请老师 回复下 在 node中 如何实现 d8指令 重现文章中的效果</div>2020-03-19</li><br/>
</ul>