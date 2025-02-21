你好，我是卢誉声，Autodesk 数据平台和计算平台资深软件工程师，也是《移动平台深度神经网络实战》和《分布式实时处理系统：原理架构与实现》的作者，主要从事C/C++、JavaScript开发工作和平台架构方面的研发工作，对SWIG也有比较深的研究。很高兴受极客时间邀请来做本次分享，今天，我们就来聊一聊SWIG这个话题。

我们都知道，Python 是一门易于上手并实验友好的胶水语言。现在有很多机器学习开发或研究人员，都选择Python作为主力编程语言；流行的机器学习框架也都会提供Python语言的支持作为调用接口和工具。因此，相较于学习成本更高的C++来说，把Python作为进入机器学习世界的首选编程语言，就再合适不过了。

不过，像TensorFlow或PyTorch这样的机器学习框架的核心，是使用Python编写的吗？

显然不是。这里面的原因比较多，但最为显著的一个原因就是“性能”。通过C++编写的机器学习框架内核，加上编译器的优化能力，为系统提供了接近于机器码执行的效率。这种得天独厚的优势，让C++在机器学习的核心领域站稳了脚跟。我们前面所说的TensorFlow和PyTorch的核心，便都是使用C/C++开发的。其中，TensorFlow的内核，就是由高度优化的C++代码和CUDA编写而成。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKUB29SpDkCxZlePjLomc02r6MFGDPWH7XiaTsG1cWrW6fIvicF2dv359nL87aGVOE7umVl1Yu0Itjg/132" width="30px"><span>gutentag</span> 👍（10） 💬（1）<div>对于单文件而言，用SWIG还是boost.python&#47;py++感觉都好理解和实践，请问对于依赖关系复杂的大型C++项目（比如OpenCV, OpenSceneGraph之类的）的python binding有没有比较完整的最佳实践呢？
C++编译的动态库python无法直接调用，C++项目的python binding本身等价于把本身编译时用到的所有的头文件中需要暴露的接口都extern成C的呢？对于头文件的相互各种include一般是人工处理还是SWIG本身可以解决呢？除了头文件暴露以外，还有别的工作吗？
任何C项目直接生成的动态链接库python都能直接import吗？请问有例外吗？
谢谢</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（6） 💬（1）<div>极客时间的C++课程快来了，期待一下，补一补我的C++。</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（5） 💬（0）<div>类似于jni啊</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f4/af/a33008a0.jpg" width="30px"><span>Ethan</span> 👍（4） 💬（0）<div>c++大法</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4f/36/7e532812.jpg" width="30px"><span>Felix</span> 👍（2） 💬（0）<div>老师，实际使用中遇到个问题，想请教下您：
假如有这么一个C++函数：ErrCode GetTpError(std::string&amp; errMsg);
用于获取错误信息，想要在python中调用，利用swig编译OK，但调用后没有得到 errMsg字符串，原因是python的字符串类型是immutable，不知道我这样理解对吗？还有这个函数要怎么转换，才能在python中调用呢？</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/44/47/8ef492fc.jpg" width="30px"><span>-.----..</span> 👍（2） 💬（1）<div>
感觉SWIG更灵活，比ctypes和py4j更方便，但是Python调用.so文件好像很挑gcc版本，不同版本gcc编译的.so文件，Python调用时有时候会报</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/51/de/990fd4f2.jpg" width="30px"><span>好好先生</span> 👍（1） 💬（0）<div>加油！</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f5/9f/1509d389.jpg" width="30px"><span>栾~龟虽寿！</span> 👍（1） 💬（0）<div>如何看python源代码，比如list.sort的实现</div>2019-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/51/9b/ccea47d9.jpg" width="30px"><span>安迪密恩</span> 👍（0） 💬（0）<div>这份加餐有点突兀，是为什么呢？</div>2024-07-04</li><br/>
</ul>