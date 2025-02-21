你好，我是卢誉声。

上一讲我们聊到开发者为了业务逻辑划分和代码复用，需要模块化代码。但随着现代C++编程语言的演进，现代C++项目的规模越来越大，即便是最佳实践方法，在不牺牲编译性能的情况下，也没有完全解决**符号可见性**和**符号名称隔离**的问题。

如果从技术的本质来探究“模块”这个概念，其实**模块主要解决的就是符号的可见性问题**。而控制符号可见性的灵活程度和粒度，决定了一门编程语言能否很好地支持现代化、标准化和模块化的程序开发。一般，模块技术需要实现以下几个必要特性。

- 每个模块使用模块名称进行标识。
- 模块可以不断划分为更多的子模块，便于大规模代码组织。
- 模块内部符号仅对模块内部可见，对模块外部不可见。
- 模块可以定义外部接口，外部接口中的符号对模块外部可见。
- 模块可以相互引用，并调用被引用模块的外部接口（也就是符号）。

我们在[上一讲](https://time.geekbang.org/column/article/623274)中仔细讲解了include头文件机制，虽然它在一定程度上解决了同一组件内相同符号定义冲突的符号可见性问题，但头文件代码这种技术方式实现非常“低级”，仍无法避免两个编译单元的重复符号的符号名称隔离问题。我们迫切需要一种更加现代的、为未来编程场景提供完备支持的解决方案。

而今天的主角——C++ Modules，在满足上述特性的基础上，针对C++的特性将提供一种解决符号隔离问题的全新思路。我们一起进入今天的学习，看看如何使用C++ Modules解决旧世界的问题？
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/29/3b/b0/eb382271.jpg" width="30px"><span>Ak</span> 👍（6） 💬（1）<div>怎么感觉C++越来越像Java和python😅</div>2023-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/9a/63dc81a2.jpg" width="30px"><span>Geek1185</span> 👍（2） 💬（1）<div>C++发展的过程中一直要兼容前面的用法，感觉越来越复杂了</div>2023-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/f9/39492855.jpg" width="30px"><span>阿阳</span> 👍（1） 💬（1）<div>前端开发中，JavaScript的模块化方案发展多年了，历史中也出现了各种模块化方案，浏览器现在支持es module方案。感觉js的模块化探索走在前列。现在不太理解编译型语言的模块化和js这种解释型语言的模块化，有什么异同？</div>2023-02-11</li><br/><li><img src="" width="30px"><span>常振华</span> 👍（0） 💬（1）<div>我觉得不好用，花里胡哨的。C++最大的问题是库太少了，不像python和java那样想写个啥到处都是现成的库。用Modules的话，就只需要.cpp不需要.h了？</div>2023-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/37/f5/12d6641f.jpg" width="30px"><span>亘古谣</span> 👍（0） 💬（1）<div>我下载了源代码看了， 发现.ixx 和 .cpp里面的内容一样的。 我的理解.ixx不是向外提供的接口文件么， 怎么和实现文件一样？</div>2023-03-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ8aLz0tWdsZuMiaNUAd0dicSD9M6A77seMGFdHgvsQwOzN8ztYPiaJSo53DcbjQWUQpw4pf4rI2f7vg/132" width="30px"><span>Geek_7c0961</span> 👍（0） 💬（1）<div>mac os 上的 clang 对c++20支持十分有限,不知道在环境配置上面有啥好的建议么?</div>2023-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/41/0d/99312186.jpg" width="30px"><span>小龚小龚 马到成功 🔥</span> 👍（0） 💬（1）<div>不会考虑用户的心智负担吗？</div>2023-01-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoZ5NZbtUUJV426Bs5xflO20BjapfRZSwtHkLqPlVuDqcAyrotkWVky74EMEbAbsMc85ZxxCs1nPw/132" width="30px"><span>xuyong</span> 👍（0） 💬（1）<div>有点复杂了啊</div>2023-01-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJV27QOK57cdpdh3E4hbArCOlccdtjCyWooF9fhjeSKAMo9SN1v9RODkrZUZD4RejjbdsqU2FIeMA/132" width="30px"><span>西钾钾</span> 👍（0） 💬（1）<div>helloworld.cpp 是需要需改为 helloworld.cppm 吗？</div>2023-01-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJV27QOK57cdpdh3E4hbArCOlccdtjCyWooF9fhjeSKAMo9SN1v9RODkrZUZD4RejjbdsqU2FIeMA/132" width="30px"><span>西钾钾</span> 👍（0） 💬（2）<div>建议搞一个代码仓库</div>2023-01-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/FhibmYQUzY7ibPac8Id5PwbibqCbvj5rWibeQhEyvYguc9pvPNUciaQydicrUjJKkhhp1s2AgfP7LRTZA8zqaa82yC8g/132" width="30px"><span>tanatang</span> 👍（0） 💬（1）<div>“同时，如果模块 A 通过 import 导入了模块 B 的符号，然后模块 B 通过 import 导入了模块 C 的符号，模块 A 中是无法直接使用模块 C 的符号的。毕竟模块系统就是为了严格规范符号可见性。”
这个得要求 是在 *.cpp中import其它模块，如果在 *.h中导入了其它模块， 当.h被其它文件include的时候，就不是这样了。对吧？</div>2023-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师两个问题：
Q1：怎么知道C++版本？
我现在正在调试一个安卓上的C++程序，在看专栏的时候，想在这份安卓代码上测试文章中的内容。文章中的内容是C++20版本，我怎么知道这个安卓代码是否支持C++20？（安卓代码的IDE是AS3.5）
Q2：所有被调用的代码都属于同一个线程吗？
安卓代码，上层是Java，通过JNI调用native层的c++代码。 Java层的Class A中创建一个线程P1，该线程的while循环中，会调用其他的Java类代码，也会调用JNI代码，JNI代码再调用native层的c++代码。那么所有被调用的代码，包括Java代码（其他类）、JNI代码、C++代码，都属于线程P1，对吗？</div>2023-01-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoZ5NZbtUUJV426Bs5xflO20BjapfRZSwtHkLqPlVuDqcAyrotkWVky74EMEbAbsMc85ZxxCs1nPw/132" width="30px"><span>xuyong</span> 👍（0） 💬（0）<div>太复杂</div>2023-01-21</li><br/>
</ul>