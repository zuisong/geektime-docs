你好，我是卢誉声。

在日常工作中，我们经常会碰到有关异步编程的问题。但由于绝大多数异步计算都跟I/O有关，因此在很多现代编程语言中，都支持异步编程，并提供相关的工具。

不过在C++20以前，异步编程从未在C++语言层面得到支持，标准库的支持更是无从说起。我们往往需要借助其他库或者操作系统相关的编程接口，来实现C++中的异步编程，特别是异步I/O。比如libuv、MFC，它们都提供了对消息循环和异步编程的支持。

接下来的三节课，我们主要讨论C++ coroutines。这节课里，为了让你更好地理解C++ coroutines，我们有必要先弄清楚同步与异步、并发与并行的概念以及它们之间的区别。同时，我还会跟你一起，通过传统C++解决方案实现异步I/O编程，亲身体验一下这种实现的复杂度。这样后面学习C++ coroutines的时候，你更容易体会到它的优势以及解决了哪些棘手问题（课程配套代码，点击[这里](https://github.com/samblg/cpp20-plus-indepth)即可获取）。

好了，我们话不多说，先从基本概念开始讲起。

## 同步与异步

同步与异步的概念比较容易理解。所谓“同步”，指的是多个相关事务必须串行执行，后续事务需要等待前一事务完成后再进行。

我们日常使用的iostream，本质上就是一种同步I/O，在发起I/O任务后当前线程就会一直阻塞等待，直到当前任务完成后才会继续后续任务，同时不会处理其他的任务。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ8aLz0tWdsZuMiaNUAd0dicSD9M6A77seMGFdHgvsQwOzN8ztYPiaJSo53DcbjQWUQpw4pf4rI2f7vg/132" width="30px"><span>Geek_7c0961</span> 👍（2） 💬（1）<div>同步, 异步, 阻塞, 非阻塞 这四个概念还是有必要区分清楚. 详见 https:&#47;&#47;www.cnblogs.com&#47;lixinjie&#47;p&#47;a-post-about-io-clearly.html</div>2023-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/50/a9/40a58c67.jpg" width="30px"><span>王子面</span> 👍（0） 💬（1）<div>&quot;static void count(int32_t maxValue)&quot;声明为静态的原因是什么？</div>2023-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/50/a9/40a58c67.jpg" width="30px"><span>王子面</span> 👍（0） 💬（1）<div>“绝大多数异步计算都跟 I&#47;O”的根本原因是什么？能不能举一两个跟I&#47;O无关的异步计算的例子？</div>2023-10-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKcGxibqN07pL59UYmlK2deeuiaZj0ze2Bk8dCEu8c0xGnYpFtGnOxRfSn2gWIDvP1LgWNwqALUafLg/132" width="30px"><span>Geek_6778f9</span> 👍（0） 💬（1）<div>“接着，我们在 main 函数中创建了三个异步任务，给每个任务分别创建对应的目录。这三个任务会同时启动并独立执行。我们在这些线程对象上调用 join，让主线程等待这三个线程结束。”


老师，这里主线程需要等待子线程执行结束，我理解这是同步编程，为什么是异步？</div>2023-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师两个问题：
Q1：子线程之间可以用future和promise传递数据吗？
Q2：结构化异常是什么意思？</div>2023-01-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ8aLz0tWdsZuMiaNUAd0dicSD9M6A77seMGFdHgvsQwOzN8ztYPiaJSo53DcbjQWUQpw4pf4rI2f7vg/132" width="30px"><span>Geek_7c0961</span> 👍（2） 💬（0）<div>github 上面的星最多的线程池实现, 可以收藏.
https:&#47;&#47;github.com&#47;progschj&#47;ThreadPool&#47;blob&#47;master&#47;ThreadPool.h
</div>2023-02-07</li><br/>
</ul>