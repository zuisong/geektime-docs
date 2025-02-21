你好，我是吴咏炜。

今天是我们未来篇的最后一讲，也是这个专栏正文内容的最后一篇了。我们讨论 C++20 里的又一个非常重要的新功能——协程 Coroutines。

## 什么是协程？

协程是一个很早就被提出的编程概念。根据高德纳的描述，协程的概念在 1958 年就被提出了。不过，它在主流编程语言中得到的支持不那么好，因而你很可能对它并不熟悉吧。

如果查阅维基百科，你可以看到下面这样的定义 \[1]：

> 协程是计算机程序的⼀类组件，推⼴了协作式多任务的⼦程序，允许执⾏被挂起与被恢复。相对⼦例程⽽⾔，协程更为⼀般和灵活……

等学完了这一讲，也许你可以明白这段话的意思。但对不了解协程的人来说，估计只能吐槽一句了，这是什么鬼？

![](https://static001.geekbang.org/resource/image/4d/f9/4d4fb4a1c16edb1087d934cd1bb7eef9.png?wh=1142%2A293 "图片源自网络")

很遗憾，在 C++ 里的标准协程有点小复杂。我们还是从……Python 开始。

```python
def fibonacci():
    a = 0
    b = 1
    while True:
        yield b
        a, b = b, a + b
```

即使你没学过 Python，上面这个生成斐波那契数列的代码应该也不难理解。唯一看起来让人会觉得有点奇怪的应该就是那个 `yield` 了。这种写法在 Python 里叫做“生成器”（generator），返回的是一个可迭代的对象，每次迭代就能得到一个 yield 出来的结果。这就是一种很常见的协程形式了。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/1c/47/53c48284.jpg" width="30px"><span>吴咏炜</span> 👍（2） 💬（0）<div>参考资料 [3] 的 cppcoro 目前看起来已经不再维护了，跟新版编译器的兼容性问题一直无人解决。目前比较好的复刻在下面这个链接：

https:&#47;&#47;github.com&#47;andreasbuhr&#47;cppcoro</div>2022-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/2c/92c7ce3b.jpg" width="30px"><span>易轻尘</span> 👍（7） 💬（3）<div>个人对协程的理解，可能不太准确：
不可以混淆线程和协程两个概念。计算机看到的是线程，调度的也是线程。一个线程中可以有很多个协程，这些协程的执行顺序由程序员自己来调度。比较明显的好处是，1. 同一个线程中的协程不需要考虑数据的竞争问题，因为这些协程的执行顺序是固定的；2. 协程能够很方便的保存执行状态，使复杂状态机的实现变得简单；</div>2020-06-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqAEFC6klazFO4gurkagZqjPb4BCv1VbnqHiaA0WVX9uINI7Jd9BBh3rJN2ljRFqicZxLjpHodIicPUw/132" width="30px"><span>Fireplusplus</span> 👍（4） 💬（1）<div>无栈协程的内存布局可以明白函数D调用结束后，应该是通过编译器处理后的方式返回到协程C的堆上空间，协程c挂起之后堆仍然是保留的，但是一个有栈协程的内存布局应该是什么样子的，协程挂起之后不是要出栈才能回到调用者的栈桢吗？</div>2021-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/9c/ffc2a5d9.jpg" width="30px"><span>谦谦君子</span> 👍（2） 💬（1）<div>老师， 图左边“调用X的参数”在“返回Y的地址”下面， 而右边“调用X的参数”在“返回Y的地址”上面， 是画错了么， 还是协成里面就是跟栈上函数调用是反的呢？</div>2020-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/db/86/51ec4c41.jpg" width="30px"><span>李云龙</span> 👍（1） 💬（1）<div>老师下面的这个函数体内没有写co_return，为什么函数的返回值就可以写uint64_resumable ? 
uint64_resumable fibonacci()
{
  uint64_t a = 0;
  uint64_t b = 1;
  while (true) {
    co_yield b;
    auto tmp = a;
    a = b;
    b += tmp;
  }
}</div>2023-11-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep2gRIticwS6CiatsCiaU4QRjAODKibQevrhSciatrmd90lNIZFxywE9yyZgAxKTmWiaBSH4zZUcRIV46qQ/132" width="30px"><span>englefly</span> 👍（1） 💬（1）<div>吴老师，请教两个问题：
1。coroutine的能力是不是比线程弱？我们可以用线程的 mutex+condition-variable 或 primise+future 模拟coroutine。但coroutine究竟哪些方面弱于线程呢？
2。coroutine的底层实现究竟是什么？它有cpu的上下文切换吗？还是所有coroutine都运行在同一个线程里，coroutine只是fibonacci c++实现那样的一种代码组织形式？
谢谢</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/cb/7e/dd9258dd.jpg" width="30px"><span>Gallen</span> 👍（1） 💬（2）<div>您好，吴老师，之前在2018年cpp开发者大会上听过您讲string view和range，还巧妙的使用|管道符进行函数间对象传递，能否有幸添加一下您的微信？谢谢</div>2020-02-20</li><br/><li><img src="" width="30px"><span>晚风·和煦</span> 👍（1） 💬（1）<div>老师，map&lt;int, int&gt;().swap(map1);
这个语句为什么不能达到真正释放map1内存的效果呢？必须得用malloc_trim</div>2020-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/63/84/f45c4af9.jpg" width="30px"><span>Vackine</span> 👍（1） 💬（1）<div>感觉跟python里面的async的新的标准库好像，是真的有性能上的提升么，还是只是编程魔法？</div>2020-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fd/1d/76bec892.jpg" width="30px"><span>梅侯</span> 👍（0） 💬（1）<div>在上面的函数 D 的执行过程中，协程是不可以挂起的——如果控制回到 B 继续，B 可能会使用目前已经被 D 使用的栈空间！

请教一下老师，在D的执行过程中，协程能挂起吗？应该是D返回后，协程才能挂起吧？老师能详细解说一下吗？谢谢</div>2025-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/6d/fa3ab44d.jpg" width="30px"><span>徐</span> 👍（0） 💬（1）<div>很早了解过协程的概念，说是用户级线程，在用户态调度，避免线程的内核态切换，性能更高；
后来在一个 C++ 服务框架上也使用过，再后来切到 Go，用起了 goroutine；
简单来说，协程用起来是真爽，避免了恶心的异步 IO 的 callback 写法，自我感觉也算是理解并熟练使用协程了。

直到看了 C++ 20 的协程，完了惊掉下巴玩脑袋问号，这什么玩意儿，这是协程吗？
查各种资料和书，都跟以前理解的不一样，特别是看到有人所谓的用几行代码实现协程，那更是不知所以。

最后终于在这里解开了我的疑惑，原来以前理解和使用的协程，和 C++ 20 里的协程，一个是有栈协程，一个是无栈协程，有巨大差异，为啥在那些讲现代 C++ 的书里，都不提这个点，这个很关键呐，真是困扰我很久。</div>2023-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4a/27/2702206d.jpg" width="30px"><span>百年</span> 👍（0） 💬（1）<div>老师结课有一年多了，什么时候开个C++与python联合编程的课啊。</div>2021-06-11</li><br/>
</ul>