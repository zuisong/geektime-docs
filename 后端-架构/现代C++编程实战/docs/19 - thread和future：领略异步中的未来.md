你好，我是吴咏炜。

编译期的烧脑我们先告个段落，今天我们开始讲一个全新的话题——并发（concurrency）。

## 为什么要使用并发编程？

在本世纪初之前，大部分开发人员不常需要关心并发编程；用到的时候，也多半只是在单处理器上执行一些后台任务而已。只有少数为昂贵的工作站或服务器进行开发的程序员，才会需要为并发性能而烦恼。原因无他，程序员们享受着摩尔定律带来的免费性能提升，而高速的 Intel 单 CPU 是性价比最高的系统架构，可到了 2003 年左右，大家骤然发现，“免费午餐”已经结束了 \[1]。主频的提升停滞了：在 2001 年，Intel 已经有了主频 2.0 GHz 的 CPU，而 18 年后，我现在正在使用的电脑，主频也仍然只是 2.5 GHz，虽然从单核变成了四核。服务器、台式机、笔记本、移动设备的处理器都转向了多核，计算要求则从单线程变成了多线程甚至异构——不仅要使用 CPU，还得使用 GPU。

如果你不熟悉进程和线程的话，我们就先来简单介绍一下它们的关系。我们编译完执行的 C++ 程序，那在操作系统看来就是一个进程了。而每个进程里可以有一个或多个线程：

- 每个进程有自己的独立地址空间，不与其他进程分享；一个进程里可以有多个线程，彼此共享同一个地址空间。
- 堆内存、文件、套接字等资源都归进程管理，同一个进程里的多个线程可以共享使用。每个进程占用的内存和其他资源，会在进程退出或被杀死时返回给操作系统。
- 并发应用开发可以用多进程或多线程的方式。多线程由于可以共享资源，效率较高；反之，多进程（默认）不共享地址空间和资源，开发较为麻烦，在需要共享数据时效率也较低。但多进程安全性较好，在某一个进程出问题时，其他进程一般不受影响；而在多线程的情况下，一个线程执行了非法操作会导致整个进程退出。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/35/3c/9800b0ba.jpg" width="30px"><span>李公子胜治</span> 👍（26） 💬（1）<div>作者大大，你好，我在effective modern c++这本书上面看到，作者告诫我们平时写代码时，首先基于任务而不是线程，但是如果我们使用async时，实际上async还是为我们创建了一个新线程，还是没有体会到async比thread的优越性，难道仅仅是可以调用get()，获取async后的执行结果吗？</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cf/db/9693d08f.jpg" width="30px"><span>YouCompleteMe</span> 👍（10） 💬（2）<div>当时看&lt;The C++ Programming&gt;下册关于多线程的时候，还写了一些demo，现在看到future&#47;async这些类，一点想不起来怎么用的-_-</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/31/43/2f70125c.jpg" width="30px"><span>风临</span> 👍（9） 💬（1）<div>老师教得很棒，学之前一头雾水，学之后醍醐灌顶，真是很享受。其实网上的教程很多，但是鱼龙混杂，自身没有经验的话，很难去分清多种方法的优劣，很可能片面甚至误导。所以跟着老师说真的很安心，因为质量很高，既全面又能让人看清楚趋势和方向</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（6） 💬（1）<div>future执行get函数的时候，如果此时还没生成结果，是否get就阻塞了，直到有返回值为止呢？</div>2020-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/33/a2/6c0ffc15.jpg" width="30px"><span>皮皮侠</span> 👍（3） 💬（1）<div>模板部分终于看完了，玩过lamda和一些traits。跟着老师学了好多新东西，新思维，尤其是对编译期计算。对一些以前模糊的理论有了新的认识。这几篇以后肯定要回头继续把玩的。另外，我想老师花了这么多心血来写一些14、17、20的新特性，应该是希望让C++既能写出性能高的代码，也易于使用，简练，更适合上层业务逻辑，用心良苦。
蟹蟹老师的分享；）</div>2020-02-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/33/e7/145be2f9.jpg" width="30px"><span>怪兽</span> 👍（2） 💬（1）<div>老师你好，想请问下shared_future，原文说“要么调用 future 的 share 方法来生成一个 shared_future，结果就可以在多个线程里用了——当然，每个 shared_future 上仍然还是只能调用一次 get 函数”。
意思是，async 返回的 future 作为共享资源被多个线程使用时，每个线程通过 future 的 share 方法获取到 shared_future，然后每个线程就可以调用get函数了，是这样吗？
另外，我在 MSVC 下测试，async 返回的 future，future.share() 得到 shared_future，shared_future 多次调用它的 get 方法也没有问题.</div>2022-11-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Cwkic25ndkExxY3HvVjAaYKVzFRicv2X6TE2sjdqTBBmqeh7X8crIQe3SHPichvcayOCqI3PJ88yVuMNlD8VvkE3A/132" width="30px"><span>even</span> 👍（2） 💬（2）<div>吴老师的课适合几度回味，多看几次，跟着敲代码，试着运行，慢慢的领会C++新特性，希望以后能够用上</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/76/60/8ea658a9.jpg" width="30px"><span>西加加</span> 👍（1） 💬（3）<div>看到作者推荐，买了一本 《c++ concurrency in action》 ，33.79美刀，肉痛。慢慢读完它。</div>2020-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0e/b6/37b19725.jpg" width="30px"><span>王大为</span> 👍（1） 💬（3）<div>最近用google的cpplint工具扫描了我的代码，但cpplint报告说不允许包含c++11的thread头文件，请问这个是出于什么目的呢？

cpplint. py --verbose=5 my_cpp_file
output : &lt;thread&gt; is an unapproved c++11 header

我看了一下cpplint脚本，里面确实对mutex thread chrono等头文件做了限制。</div>2020-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/3f/7d/f624fa69.jpg" width="30px"><span>当初莫相识</span> 👍（0） 💬（1）<div>每次看线程都有新的收获，也有新的疑问。scoped_thread在析构函数时join，析构函数会等join完毕后销毁thread成员变量，对吗？
  scoped_thread th{work, ref(cv),
                   ref(result)};
  &#47;&#47; 干一些其他事
  cout &lt;&lt; &quot;I am waiting now\n&quot;;
  unique_lock lock{cv_mut};
  cv.wait(lock);
  cout &lt;&lt; &quot;Answer: &quot; &lt;&lt; result
       &lt;&lt; &#39;\n&#39;;
}
main()函数里，我理解为scoped_thread直到｝才会执行析构启动线程，而cv.wait又一直在阻塞，所以不会运行到｝。虽然知道程序能得到预期结果，但逻辑上不理解，希望老师能解答我的困惑</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（1）<div>老师，你好，关于条件变量应该如何退出呢？
比如说:
void f()
{
    while(m_isRun)
    { 
       std::unique_lock&lt;std::mutex&gt; dataLock(m_mtx);
       while(m_list.empty())
       {
           m_cond. wait(dataLock);
        }
        ……
    }
}
线程函数如上面所写，这个线程如何安全退出呢？</div>2020-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（0） 💬（2）<div>老师，异步的例子都是基于async的。那如果不用这个特性，在cpp98上应该只有下面这个方法了吧
1. Callback
2.多线程+Callback

但是这两个都有个问题，callback也是会阻塞的。如果有A B C D四个流程，B C D分别依赖于前一个的输出，这种callback就会调用栈太深，容易爆栈。

最近对异步编程模式产生了些疑问，应该怎么解决？

尤其高并发的情况下，阻塞的时候线程不被调度，这不就相当于cpu会飙升。</div>2020-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/32/8d/91cd624b.jpg" width="30px"><span>幻境之桥</span> 👍（0） 💬（2）<div>std::async 有个比较大的坑，如果把返回的 future 绑定到变量 ， 调用 std::sync 的线程仍然会阻塞到里面的任务执行完，即使绑定了，在出绑的变量出作用域时析构时会阻塞
很多时候只是想单纯的异步运行一下，不阻塞当前的线程，这种情况使用 std::sync 就会掉坑里了</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/cd/02/26993bee.jpg" width="30px"><span>HaHa</span> 👍（0） 💬（1）<div>请问使用async时是每次都要启动一个线程吗，那大量使用会频繁创建线程？</div>2020-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/76/60/8ea658a9.jpg" width="30px"><span>西加加</span> 👍（0） 💬（1）<div>最近写了一些多线程程序练手，突然想到有了 feature 这一套东西，是不是应该完全抛弃之前的条件变量同步那一套呢？尝试写一个基于cpp17特性的线程池，想到上面的问题。望解答。</div>2020-05-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJe0esddRVdG689MicU5zMibMtkyLpYkX4MtiamKP8eFf7KUoMlfU7ficrciakyVS06jHVdskYT67JKtdg/132" width="30px"><span>湖海散人</span> 👍（0） 💬（1）<div>请教老师几个问题：
1. sleep_for函数中的参数数字后面的&quot;ms&quot;, &quot;s&quot;是C++的什么特性呀，我用C++11编译不过，用C++17正常
2. 对于async，future的用法，是怎么拿到另一个线程的返回值的？ 是future内部使用了管道？这个async和future和python里面的协程很像</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0f/53/92a50f01.jpg" width="30px"><span>徐洲更</span> 👍（0） 💬（1）<div>在系列完结以后才开始阅读。最初买专栏以为自己能看懂，结果直接懵逼了。现在终于写了一些c++代码，才发现这系列都是浓缩的精华，每次读都有新收获啊</div>2020-03-26</li><br/><li><img src="" width="30px"><span>晚风·和煦</span> 👍（0） 💬（3）<div>老师，线程的虚拟内存大小都一样大吗？😂</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c9/e3/28c16afa.jpg" width="30px"><span>三味</span> 👍（0） 💬（1）<div>普大喜奔！
🍾🍾🎉🎉🎊🎊
模板章节终于结束了！
其实我还没学够呢（真心）

其实死锁这玩意太容易出现了。描述一个比较经典的场景，A,B两个线程，a,b两个资源，两个线程都要用两个资源。
A线程先用资源a，锁住资源a；
B线程先用资源b，锁住资源b；
A线程还需要资源b，但是不能放开资源a，因为没用完；
B线程还需要资源a，但是也不能放开资源b，因为没用完；
A线程占着a不放还想用b，B线程占着b不放还想用a；
A说，你先给我用b，我用完b，我肯定ab一起放；
B说，为啥你不给我用a，我用完a，我肯定ab一起放；
任务管理器说：你们都死吧。</div>2020-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（0） 💬（1）<div>烧脑的编译期内容终于结束了。每天在工作之余烧一会儿，还没烧透呢，就结束了。是该庆幸还是该解脱呢？

感觉编译期编程就是C++中的理论物理，需要纸和笔，然后适应一大堆符号。

feature只能使用一次，是为了避免多次使用带来的循环获取锁从而导致死锁么？


读书的时候先学的就是C++，并且为其微妙的语义而着迷，可以工作中很少用到它。接触future, promise, async是从Python和JavaScript开始的。虽然这三种语言互补相同，可是在异步或者并发上，用的关键词竟然都是一样的，真是聪明的脑袋都是类似的，愚笨的脑袋各有不同啊。

这个巧合也许因为Python和JavaScript底层都是用c&#47;c++实现的？</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/13/0b203112.jpg" width="30px"><span>道隐</span> 👍（0） 💬（0）<div>第一个例子WSL上实测始终是A B, VS2015上体现出随机。感觉WSL是个伪多线程的环境</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/83/25/10dac87c.jpg" width="30px"><span>舍得</span> 👍（0） 💬（0）<div>nice</div>2020-01-08</li><br/>
</ul>