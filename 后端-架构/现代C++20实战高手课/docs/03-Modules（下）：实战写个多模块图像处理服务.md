你好，我是卢誉声。

通过前面的学习，我们掌握了模块的基本概念。这节课，我们会一起学习，怎样使用C++ Modules来组织实际的项目代码。相信你在动手实战后，就能进一步理解应该如何使用C++ Modules和namespace来解决现实问题。

掌握了基本概念和使用要点之后，我们也会站在语言设计者的角度，整体讨论一下C++ Modules能解决什么问题，不能解决什么问题。

好，话不多说，我们马上进入今天的学习。课程配套代码，点击[这里](https://github.com/samblg/cpp20-plus-indepth)获取。

## 面向图像的对象存储系统

要写的实例是一个常见的面向图像的对象存储系统，核心功能是将图片存储在本地空间，用户通过HTTP请求获取相应的图片，而这个系统的特点是用户除了可以获取原始图片，还可以通过参数获取经过处理的图片，比如图像缩放、图像压缩等。

想实现这样的功能，需要哪些模块呢？

我们画一张系统的模块架构图，可以清晰地看到系统模块以及模块内部分区的依赖关系。

![](https://static001.geekbang.org/resource/image/3e/15/3e344cfb7e5cef10a7defef271b44415.jpg?wh=2900x2311)

首先我们需要创建项目，项目包括5个子模块，分别是app、cache、command、image、network，其中app是业务应用模块，cache是本地缓存模块，command是命令行解析模块，image是图像处理模块，network是网络服务模块，每个模块分别创建对应的目录存储模块内的源代码。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/86/07/aefa4e8b.jpg" width="30px"><span>wilby</span> 👍（2） 💬（2）<div>怎么编译这个项目呢？在macOS下没试出来怎么编译</div>2023-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/54/a9b1d9f1.jpg" width="30px"><span>bruceyk</span> 👍（0） 💬（1）<div>老师，请问clang哪个版本能完美支持20所有特性呢？</div>2024-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/e4/a8/bb6e00ba.jpg" width="30px"><span>Cedric</span> 👍（0） 💬（1）<div>代码中是否存在bug，使用function和vector，map容器的代码编译会报重定义错误注释掉相关代码就可以编译通过了，我的环境是ubuntu22.04，g++13.0.1，不确定是否是对于module的支持的问题还是使用上的问题</div>2023-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/1f/29/c7a69190.jpg" width="30px"><span>浩浩</span> 👍（0） 💬（1）<div>请教老师：
1）文中：“现阶段的 Modules 暂时无法解决各编译器之间 ABI” ，C&#47;C++现今有解决这个问题的方案吗？
2）文中：“二进制库分发的问题”，具体是指二进制库在不同体系结构设备上无法通用吗？
</div>2023-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/dc/53/938b775e.jpg" width="30px"><span>Coding Fatty</span> 👍（0） 💬（1）<div>ips 表示什么含义?</div>2023-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：cpp文件中怎么会有变量声明？
命令行模块的代码中，argument.cpp中怎么声明了一些字段？：private: std::string _flag; std::string _name;  这些不是应该在.h文件中声明吗？ Cpp文件是类的实现文件啊。
Q2：用了module以后就不再有头文件了吗？
文中有一句“新的 C++ Modules 方法，本质上抛弃了“头文件”这种 C&#47;C++ 中的重要组成部分”。采用module以后，不再是“.h + .cpp”这种方式，而时只有.cpp一个文件，对吗？
Q3：C80、CA0表示什么？
文中“STL 内存布局问题”部分，图中有“C80、CA0”等内容，是表示CPU类型吗？</div>2023-01-20</li><br/>
</ul>