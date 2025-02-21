你好，我是景霄。

我想你对Python中的with语句一定不陌生，在专栏里它也曾多次出现，尤其是在文件的输入输出操作中，不过我想，大部分人可能习惯了它的使用，却并不知道隐藏在其背后的“秘密”。

那么，究竟with语句要怎么用，与之相关的上下文管理器（context manager）是什么，它们之间又有着怎样的联系呢？这节课，我就带你一起揭开它们的神秘面纱。

## 什么是上下文管理器？

在任何一门编程语言中，文件的输入输出、数据库的连接断开等，都是很常见的资源管理操作。但资源都是有限的，在写程序时，我们必须保证这些资源在使用过后得到释放，不然就容易造成资源泄露，轻者使得系统处理缓慢，重则会使系统崩溃。

光说这些概念，你可能体会不到这一点，我们可以看看下面的例子：

```
for x in range(10000000): 
    f = open('test.txt', 'w')
    f.write('hello') 
```

这里我们一共打开了10000000个文件，但是用完以后都没有关闭它们，如果你运行该段代码，便会报错：

```
OSError: [Errno 23] Too many open files in system: 'test.txt'
```

这就是一个典型的资源泄露的例子。因为程序中同时打开了太多的文件，占据了太多的资源，造成系统崩溃。

为了解决这个问题，不同的编程语言都引入了不同的机制。而在Python中，对应的解决方式便是上下文管理器（context manager）。上下文管理器，能够帮助你自动分配并且释放资源，其中最典型的应用便是with语句。所以，上面代码的正确写法应该如下所示：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/a5/67/bf286335.jpg" width="30px"><span>AllenGFLiu</span> 👍（28） 💬（2）<div>第一次有教程提到这个上下文管理器，学习。
对知识的学习就是需要从多角度重复去看，在这个过程中查遗补缺，才能保持不断进步。</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（10） 💬（2）<div>是不是只有程序出了with代码块，管理的对象才会析构，也就是释放资源？</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6b/e1/90d63f3e.jpg" width="30px"><span>fly1024</span> 👍（3） 💬（1）<div>有个疑问: 对于file和Lock这两个使用with用法，python会自动调用对应释放资源的函数(close和release)，这两个释放资源的函数也是定义__exit函数里的吗？希望老师解答一下。</div>2019-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/4e/ff0702fc.jpg" width="30px"><span>火锅小王子</span> 👍（2） 💬（1）<div>现在才学这个专栏 感觉落后了好多同学 想问下老师一个问题 这里讲到了上下文管理器 可不可以分析下async with异步上下文的逻辑和用法 ？一直不是很明白这个点 😀</div>2019-11-02</li><br/><li><img src="" width="30px"><span>Geek_d848f7</span> 👍（1） 💬（1）<div>还是不怎么清楚基于生成器的上下文管理器的运行过程</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/44/3e3040ac.jpg" width="30px"><span>程序员人生</span> 👍（0） 💬（1）<div>老师，最后一段代码执行后报这个错：
TypeError: file_manager() missing 1 required positional argument: &#39;mode&#39;

应该写成这样把，
with file_manager(&#39;test.txt&#39;,&#39;w&#39;) as f:
    f.write(&#39;hello world2&#39;)</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/e2/fc6260fb.jpg" width="30px"><span>ajodfaj</span> 👍（16） 💬（1）<div>with tf.Session() as sess</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/2d/af86d73f.jpg" width="30px"><span>enjoylearning</span> 👍（15） 💬（0）<div>主要用于数据库连接</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ba/3c/2b642c9a.jpg" width="30px"><span>new</span> 👍（13） 💬（0）<div>打开文件时用最方便</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/6d/c20f2d5a.jpg" width="30px"><span>LJK</span> 👍（8） 💬（2）<div>老师好，请问基于类的上下文，“__enter__“方法什么时候返回self呢？DBConnectionManager的例子中可以说明一下为什么是返回self不是返回self.connection么？</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/19/37/e0a9bf99.jpg" width="30px"><span>Geek_59f23e</span> 👍（4） 💬（1）<div>UnboundLocalError: local variable &#39;f&#39; referenced before assignment
最后一个例子有报错哦，基于生成器的上下文管理器那儿，提示说finally语句里的f变量没有先声明。</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/59/21/d2efde18.jpg" width="30px"><span>布凡</span> 👍（2） 💬（0）<div>这里with 的用法和C#中的using 一样，表示资源变量在一个块中有效，块结束后自动回收资源</div>2020-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ae/89/81404170.jpg" width="30px"><span>Carl</span> 👍（2） 💬（2）<div>为什么平时使用 with open() as f 时可以畅通无阻呢?
是因为open这个函数在源码里就用@contextmanager装饰了吗?</div>2019-10-21</li><br/><li><img src="" width="30px"><span>瞳梦</span> 👍（2） 💬（0）<div>请问数据库的那个例子，__enter__()中返回self.connection是不是更符合实际应用中的情况。 </div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/e2/1fad12eb.jpg" width="30px"><span>张洪阆</span> 👍（1） 💬（0）<div>with限制了对象的作用域，相当于是个临时对象</div>2019-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/41/83/a6263932.jpg" width="30px"><span>倾</span> 👍（1） 💬（0）<div>只是在文件操作时使用，今天第一次学习到还能这么用。</div>2019-07-15</li><br/><li><img src="" width="30px"><span>E79991</span> 👍（0） 💬（0）<div>with open 这里，Open函数又没有实现 close ，怎么自动执行 file.close的呢 ？</div>2024-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第29讲打卡~</div>2024-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/df/06/72f90828.jpg" width="30px"><span>01</span> 👍（0） 💬（0）<div>  yield f  
这里用生成器的意义是啥呢？</div>2021-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/32/7440d47d.jpg" width="30px"><span>王位庆</span> 👍（0） 💬（0）<div>最近正好看with语句，然后看课程学习了一下。基本了解了原理</div>2020-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0e/d9/e61ce097.jpg" width="30px"><span>郭纯</span> 👍（0） 💬（0）<div>我的理解在 __enter__ 和 __exit__ 魔术方法内定义资源初始化和资源释放的逻辑.也就是两个回调钩子. 当使用 with 的时候会在代码块内创建上下文.在上下文开始的时候执行 __enter__ 钩子函数. 在上下文销毁之前执行__exit__ 钩子函数. 提供了类似生命周期的机制.</div>2020-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（0）<div>这一节学到了with 的上下文管理器，之前都是f.close(  )  </div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/be/30/1154657e.jpg" width="30px"><span>风含叶</span> 👍（0） 💬（0）<div>1. 主要是 io 操作，包含 文件打开关闭、网络请求</div>2019-12-15</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（0） 💬（0）<div>内存管理Python已经实现，with语句是管理其他类型资源的简便方法。</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/bc/cb39ed38.jpg" width="30px"><span>自由民</span> 👍（0） 💬（0）<div>没用过，以前在c&#47;c++里都是自己释放资源的。最多在类的析构函数里释放，但是这样还是有可能会资源泄露的。</div>2019-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/5b/08/b0b0db05.jpg" width="30px"><span>丁丁历险记</span> 👍（0） 💬（0）<div>超喜欢py 这总把啰哩巴嗦的实现简化的套路。</div>2019-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（0） 💬（0）<div>“__enter__()返回FileManager 对象赋给变量f”这里应该写错了，应该是返回资源self.file给变量f</div>2019-09-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI9TONIzolbQaRAubeRv37J4zfwRicsOPe8T6LpAgfLxusiaiaibAWmTwNRxb3OeChNbc0kIgtlhoIEWw/132" width="30px"><span>温若</span> 👍（0） 💬（0）<div>some_lock = threading.Lock()
with somelock:
    ...

这个第二行是不是 with some_lock ? </div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a4/c0/c6880c07.jpg" width="30px"><span>magician</span> 👍（0） 💬（0）<div>DBClient用了什么python package?</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/29/d6816ebf.jpg" width="30px"><span>小侠龙旋风</span> 👍（0） 💬（0）<div>老师，您好，threading.Lock()案例能否写得详细一点</div>2019-07-21</li><br/>
</ul>