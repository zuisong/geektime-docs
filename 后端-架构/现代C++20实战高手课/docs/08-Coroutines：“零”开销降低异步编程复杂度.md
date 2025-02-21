你好，我是卢誉声。

在上一讲中，我们看到在传统的C++异步方案中，想要实现高效易用的异步方案是非常困难的。好消息是从C++20开始，提供了一个全新的解决异步问题（特别是异步I/O）的方案——那就是协程。

协程提供了泛化的协作式多任务模型，在并发计算和高性能I/O领域有着广泛的应用，相较于多线程或多进程运行时来说，可以实现几乎“零”开销的代码调度。虽说如此，协程并不是一个新概念，早在1958年Melvin E. Conway就提出这一概念，早期的C++也支持基于协程的任务模型编程。

但是，早期C++对协程的支持简陋且不可移植。与此同时，协程在设计上相较于规范函数调用来说更加泛化，因此针对C++的标准化协程方案很难得到一致认可。经过几十年的探索和努力，C++20及其后续演进中终于回归了标准化协程（C++ coroutines）。

由于以往的协程都被编写在非常底层的实现上，因此常见的应用系统上很少使用它。

但这次标准化让它重回大众视野，也启发了我们用另一种思维模式来解决高性能计算问题——通过协程，就能在几乎零性能开销的情况下，大幅降低异步编程复杂度。甚至可以说，**标准化协程促使C++20成长为全新的编程模型**，让我们用现代C++解决工程问题时更加游刃有余。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/29/5c/c9/f1b053f2.jpg" width="30px"><span>Family mission</span> 👍（1） 💬（1）<div>作者你好，感觉你讲的这节内容干货满满，请解释下这个代码块的含义
template
struct promise;
template
struct Generator : std::coroutine_handle&gt; { using promise_type = promise;};
using promise_type = promise&lt;T&gt;;这个代码块的含义么，可以理解成是将模版类赋值给这个promise_type么</div>2023-11-07</li><br/><li><img src="" width="30px"><span>常振华</span> 👍（0） 💬（1）<div>说实话，从这些代码来看，我认为比传统的异步编程更复杂了，而且是复杂太多了。
学到这里，我觉得concept是个好东西，相比原来的模板元编程，可读性友好了很多，其它的，就是把简单的事情复杂化。</div>2023-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/73/f7d3a996.jpg" width="30px"><span>！null</span> 👍（0） 💬（1）<div>CountGenerator doCount() {
    for (int32_t i = 0; i &lt; 3; ++i) {
        co_yield i;
    }
}
这个返回值是在哪里return的呢？</div>2023-08-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIm5rlbJ4HdXLbxmflvW0FW4rTyLcDzHLGDJUJic9W3f1KibWY7mAj9dxUIEVlxDyjwRXEX54KXEn5g/132" width="30px"><span>sea520</span> 👍（0） 💬（1）<div>生成器在执行代码的时候，调用者也会在执行自己的代码吗，还是调用者暂停执行？
调用者是通过自己不断循环来获取生成器的返回值，还调用者怎么去做自己的事情，感觉不太能体现异步编程。异步编程是生成器有数据后通知调用者，而不是一直循环去检查是否数据完成吧</div>2023-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/27/a6/32e9479b.jpg" width="30px"><span>tang_ming_wu</span> 👍（0） 💬（1）<div>个人觉得，作为普通开发者，当前只需要了解无栈协程的基本原理即可。最后使用的，应该还是标准库需要提供的易用接口。</div>2023-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/50/cb/01422311.jpg" width="30px"><span>momo</span> 👍（0） 💬（1）<div>请教老师一个问题：
我们知道协程实现有 有栈协程和无栈协程，C++ 选用了无栈协程是基于什么考虑？</div>2023-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：局部变量的声明周期是什么？
Q2：用“exposition only”标识出来的ptr怎么跟编译器有关？
文中说“用“exposition only”标识出来的部分，就是 coroutine_handle 的内部存储内容，这部分只是为了说明标准做的示例，实际不同编译器可以根据自己的需求定义这里的实现”。 我的理解是：ptr应该是coder设置的具体内容，应该和编译器无关。
Q3：协程可以用来做长耗时的运算吗？</div>2023-02-02</li><br/>
</ul>