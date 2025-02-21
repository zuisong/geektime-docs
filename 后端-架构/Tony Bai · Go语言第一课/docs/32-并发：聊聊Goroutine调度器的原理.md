你好，我是Tony Bai。

上一讲我们学习了并发的基本概念和Go的并发方案，也就是Goroutine的一些基本使用和注意事项。对于大多数Gopher来说，这些内容作为Go并发入门已经是足够了。

但毕竟Go没有采用基于线程的并发模型，可能很多Gopher都好奇Go运行时究竟是如何将一个个Goroutine调度到CPU上执行的。当然，Goroutine的调度本来是Go语言核心开发团队才应该关注的事情，大多数Gopher们无需关心。但就我个人的学习和实践经验而言，我觉得了解Goroutine的调度模型和原理，能够帮助我们编写出更高质量的Go代码。

因此，在这一讲中，我想和你一起简单探究一下Goroutine调度器的原理和演化历史。

## Goroutine调度器

提到“调度”，我们首先想到的就是操作系统对进程、线程的调度。操作系统调度器会将系统中的多个线程按照一定算法调度到物理CPU上去运行。

前面我们也提到，传统的编程语言，比如C、C++等的并发实现，多是基于线程模型的，也就是应用程序负责创建线程（一般通过libpthread等库函数调用实现），操作系统负责调度线程。当然，我们也说过，这种传统支持并发的方式有很多不足。为了解决这些问题，Go语言中的并发实现，使用了Goroutine，代替了操作系统的线程，也不再依靠操作系统调度。
<div><strong>精选留言（29）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_cca544</span> 👍（51） 💬（1）<div>go1.13的话加上runtime.GOMAXPROCS(1) main goroutine在创建 deadloop goroutine 之后就无法继续得到调度
但如果是go1.14之后的话即使加上runtime.GOMAXPROCS(1) main goroutine在创建 deadloop goroutine 之后还是可以得到调度，应该是因为增加了对非协作的抢占式调度的支持</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（33） 💬（1）<div>大白老师这篇算是让我重新对Go的G、P、M模型有了一个新的认识。感谢。不过还是有几处疑惑的地方：

1. 怎么理解文中的：“集中状态存储”和“数据局部性较差”，能再进一步解释一下么？

2. 编译器在每个函数或方法的入口处加上了一段额外的代码 (runtime.morestack_noctxt)，括号中的：runtime.morestack_noctxt 这是一个文件么？

3. 怎么理解“协作式”、“非协作式”呢？看了文章还是没太明白。

4. 关于挂起，百度的说法大概是：“暂时被淘汰出内存的进程。”，这里该怎么理解呢？

5. 为什么 M有时必须要与 G 一起挂起？M 不是可以不保存 G的状态的吗？M不能直接去绑定别的p吗？为什么要频繁的挂起呢？

PS：老师的文档链接好评，最原始的出处标准的很明确。</div>2022-01-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ8ic8eLTo5rnqIMJicUfpkVBrOUJAW4fANicKIbHdC54O9SOdwSoeK6o8icibaUbh7ZUXAkGF9zwHqo0Q/132" width="30px"><span>ivhong</span> 👍（20） 💬（1）<div>谢谢大白老师，能把这么晦涩的原理讲的这么清楚。我反复看了很多遍，做了如下总结，不知道是不是合理，希望老师闲暇之余给予指正，🙏。
在文中提及的GPM，以及GPM之前的相互配合，完成了go的并发功能。

G：可以看作关键字go 后面跟着的可执行代码块（即goroutine），当然包含这个代码块的一些本身的信息（比如栈信息、状态等等一些必要的属性）。另外存在一个G的全局队列，只要是需要执行的 goroutine 都会被放倒这个全局队列里。

P：可以看作逻辑上的“任务处理器”，go有多个这个处理器，具体的数量由runtime.GOMAXPROCS(1)指定，它有下面的指责：
    1. 它有自己G队列。当他发现自己的队列为空时，可以去全局G队列里获取等待执行的goroutine，甚至可以去其他的P的队列里抢用goroutine。他把拿过来的goroutine放到自己的队列里
    2. 他可以找到一个空闲的M与自己绑定，用来运行自己队列中的goroutine，如果没有空闲的M，则创建一个M来绑定
    3. 被P绑定的M，可以自己主动的与P解绑，当P发现自己的M被解绑，就执行2
    4. 如果自己队列中没有goroutine，也无法从“外面”获取goroutine，则与M解绑（解绑M时，是按什么逻辑选择挂起M或者释放M呢？）

M：物理的处理器，具体执行goroutine的系统线程，所有goroutine都是在M中执行的，它被P创建，与P绑定后可执行P队列中的goroutine，在执行goroutine会处理3中情况保证并发是顺利的（不会发生“饿死”，资源分配不平等的情况）
    1. 当G长时间运行时，可以被Go暂停执行而被移出M（是不是放到全局G队列呢？），等待下次运行（即抢占式调度）。
    2. 如果G发生了channel 等待或者 网络I&#47;O请求，则把G放到某个等待队列中，M继续执行下一goroutine，当G等待的结果返回时，会唤醒“G”，并把它放入到全局G的队列中，等待P的获取（这里不知道理解的对不对？）。
    3. 如果G产生了系统调用，则M与P解绑，然后M和它正执行的G被操作系统“挂起”等待操作系统的中断返回（对于操作系统而言，M和G是一回事；而对于GO来说，G只有能在M中运行，只有运行才触发发系统调用）。

</div>2022-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/d8/39/acb7e16e.jpg" width="30px"><span>麦芒极客</span> 👍（18） 💬（1）<div>老师您好，G遇到网络IO阻塞时，真正的线程即M不应该也阻塞吗？</div>2022-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/ce/fd45714f.jpg" width="30px"><span>bearlu</span> 👍（6） 💬（2）<div>老师，想学习goroutine调度器，演进的关键版本，依次是go的什么发行版？还有什么相关资料书籍？谢谢老师</div>2022-01-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/7hOJBKZVrJD8ayZoYnq0ECFsoWf9yx6eyq3JU8p1449A6cKEp5rSpicJRg5vH3HZgq5YwbpGicBvyARFutcPLGgw/132" width="30px"><span>Mr_D</span> 👍（4） 💬（1）<div>请问G的可重用具体指什么呢？是针对已经运行结束的G留下的内存空间，进行相关数据的重填么</div>2022-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/b7/30/c1e4f5b5.jpg" width="30px"><span>微微超级丹💫</span> 👍（3） 💬（1）<div>请问常规文件是不支持监听的（pollable）是什么意思呀？</div>2022-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/64/8a/bc8cb43c.jpg" width="30px"><span>路边的猪</span> 👍（3） 💬（1）<div>第一种，因为网络io导致阻塞的处理方式这里。我想问，网络io势必会引起系统调用，比如最基础的建立tcp连接这些，那这块儿是咋区分系统调用和网络io的呢？</div>2022-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（3） 💬（2）<div>思考题：
是不是不管怎么处理，main goroutine  都会被调度？</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0c/46/dfe32cf4.jpg" width="30px"><span>多选参数</span> 👍（2） 💬（1）<div>有几个问题想问老师： 
1. 文章中提到的 Go 运行时这块更多是指哪些内容？Go 调度器应该也是 Go 运行时中的部分内容吧？就是 Go 开源的源代码吗？
2. 有关 Go 运行时比较好的资料推荐吗？比如 Go 运行时的架构、Go 运行时是怎么和用户编写的代码合在一起的，因为我理解的 Go 运行时不像 JVM 那样，Go 是编译性的，也就是说会将用户编写的代码和 Go 运行时代码一起编译成二进制，然后运行是从 Go 运行时开始的，然后在从用户逻辑的代码开始。

老师有空的时候麻烦解答下，谢谢老师～</div>2022-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（2） 💬（1）<div>老师讲的太好了，干货慢慢，老师已经把流程和原理讲清楚了，
原理下的 更底层细节 得自己再研究学习。
</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/8c/f9/e1dab0ca.jpg" width="30px"><span>怎么睡才能做这种梦</span> 👍（1） 💬（2）<div>老师，我想问一下，Go语言有了GPM模型，还有线程池存在的必要吗？
还是说可能存在特殊情况，比如说当有系统调用发生阻塞的情况下，线程池才有作用，因为只有系统调用发生阻塞才可能创建线程。或者说自定义的线程池补充了GPM模型的哪些缺点呢？</div>2023-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/64/8a/bc8cb43c.jpg" width="30px"><span>路边的猪</span> 👍（1） 💬（1）<div>抢占式调度这里，比如 go func(){ for {}}
这种情况 协程内确实没有其他的函数调用 是一个死循环，但是这个func() 本身不就是个函数吗，为啥不能在这个函数开头插入检测代码呢？</div>2023-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/96/fb0d8a65.jpg" width="30px"><span>李亮</span> 👍（1） 💬（1）<div>抢占是什么意思？G被抢占是指本来停止运行G，换成另外一个G吗？</div>2022-10-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoGLuQGiaBftJglfdCicBnCWw8tZKkbEJoU3lpgI10mAzaYgS0QLicG02GMH9zSzFD2KFQ0SHc6PuMUA/132" width="30px"><span>Geek_1d2661</span> 👍（1） 💬（1）<div>1.用1.13是实现了抢占式调度 但是那个是通过函数埋点的  这里的不是函数 所以不会运行吧
2.使用函数调度应该可以吧</div>2022-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/eb/2e/90fea784.jpg" width="30px"><span>柒</span> 👍（1） 💬（2）<div>Goroutine 传递问题：M 经常在 M 之间传递“可运行”的 Goroutine？为啥会有传递呀？ 就算是上下文切换，只会挂起一个G，M切换到执行另一个G，它不会从一个M传递到另一个M嘛。</div>2022-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/2e/ca/469f7266.jpg" width="30px"><span>菠萝吹雪—Code</span> 👍（1） 💬（1）<div>打卡</div>2022-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（1） 💬（1）<div>思考题
1.在一个拥有多核处理器的主机上，使用 Go 1.13.x 版本运行这个示例代码，你在命令行终端上是否能看到“I got scheduled!”输出呢？也就是 main goroutine 在创建 deadloop goroutine 之后是否能继续得到调度呢？
答：不会得到调度，首先 Go 是在 1.2 版本增加的抢占式调度，1.13.x版本还不支持，因为deadloop goroutine 是死循环，所以这个G会永远占用分配的P和M

2.我们通过什么方法可以让上面示例中的 main goroutine，在创建 deadloop goroutine 之后无法继续得到调度？
两个必要条件
①go的版本要在1.2之前，因为1.2之前不支持抢占式调度，可以确保G可以占用分配给它的P和M
②设置GOMAXPROCS=1
</div>2022-07-19</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/wgMMrp1hvSB3E30KqZvMsj3KQdAI3T1uQM77LT7hZ65nVSjPGRg3AbUOyiahnssA6AIT5PAkyHFmlTBzUH9gdyQ/132" width="30px"><span>pythonbug</span> 👍（1） 💬（1）<div>“如果一个 G 任务运行 10ms，...... 那么等到这个 G 下一次调用函数或方法时，...... 等待下一次被调度。”
老师好，有个问题，某个goroutine运行超过10ms了，为啥不直接抢占，等待下一次是什么意思呢？那么这次是直接运行完吗，既然这次都运行完了，又怎么会有下一次呢。。。这段不大理解，有点懵了。。。</div>2022-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/96/dd/1620a744.jpg" width="30px"><span>simple_孙</span> 👍（1） 💬（1）<div>每个P是不是跟Java中的线程一样都有一个就绪队列和等待队列呢</div>2022-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/d7/5315f6ce.jpg" width="30px"><span>不负青春不负己🤘</span> 👍（1） 💬（1）<div>mark</div>2022-02-02</li><br/><li><img src="" width="30px"><span>Geek_0b92d9</span> 👍（1） 💬（1）<div>老师好。关于调度的顺序，想请教下。

func main() {
	runtime.GOMAXPROCS(1)

	&#47;&#47; 启动 4 个协程
	var i int
	for i = 0; i &lt; 4; i++ {
		go func(i int) {
			fmt.Printf(&quot;hello %d \n&quot;, i)
		}(i)
	}

	fmt.Println(&quot;hello main&quot;)

	time.Sleep(1 * time.Second)
}
&#47;&#47;输出的是 3,0,1,2

如果我在每个子协程打印前，加上 time.Sleep(10 * time.Millisecond) ，完整代码如下：
func main() {
	runtime.GOMAXPROCS(1)

	&#47;&#47; 启动 4 个协程
	var i int
	for i = 0; i &lt; 4; i++ {
		go func(i int) {
			time.Sleep(10 * time.Millisecond)
			fmt.Printf(&quot;hello %d \n&quot;, i)
		}(i)
	}

	fmt.Println(&quot;hello main&quot;)

	time.Sleep(1 * time.Second)
}
&#47;&#47;又输出 0,3,2,1
</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f1/de/3ebcbb3f.jpg" width="30px"><span>DullBird</span> 👍（1） 💬（1）<div>小结上面一句：之前的那个挂起的 M 将再次进入挂起状态。   最后是不是运行状态吧？</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f1/10/cdb35cd1.jpg" width="30px"><span>stronger</span> 👍（0） 💬（1）<div>goroutine在进行系统调用的时候，会在内核态运行吗？</div>2024-07-01</li><br/><li><img src="" width="30px"><span>Geek_73c432</span> 👍（0） 💬（1）<div>老师，怎么理解
基于协作的“抢占式”调度
非协作的抢占式调度
这两个表达？

个人认为，在调度策略中， &quot;协作式&quot; 和 &quot;抢占式&quot; 是两种截然不同的策略。从文中没看出来哪里体现了”协作“啊</div>2024-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（0） 💬（2）<div>思考题：
1、可以定时 1 秒间隔地不断看到“I got scheduled!”输出；
2、main 函数中，go deadloop() 语句前添加 runtime.GOMAXPROCS(1)，即可使 main goroutine 在创建 deadloop goroutine 之后无法继续得到调度。

PS：基于 go1.17.6 windows&#47;amd64 版本测试，我这测试结果与留言中 Geek_cca544 同学的结论不一样，请问老师问题 2 哪个答案是对的呢？</div>2022-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f1/10/cdb35cd1.jpg" width="30px"><span>stronger</span> 👍（0） 💬（0）<div>系统调用下的调度，gorountine 会运行在内核态吗？</div>2024-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/cc/70/64045bc0.jpg" width="30px"><span>人言有力</span> 👍（0） 💬（0）<div>本节讲述了go语言并发调度器的基本原理，从G-M到G-P-M模型，从非抢占式到协作抢占到信号抢占的演进。我们现在用到的还是G-P-M模型，其中G是goroutine保存调用栈，P是逻辑处理器，保存一个G的运行队列，数量由GOMAXPROCS控制，而M是真实调度器，和系统线程绑定。
调度过程就是启动goroutine后会绑定一个P队列，P队列和M调度器绑定进行CPU执行。
抢占过程就是会有一个专门的G0作为调度G，常规情况就是执行各自时间片之后，常规的G会被设置为可抢占，下个调度被移除队列重新入队；IO情况下G会进入等待，而M会和运行P的下个G；如果是系统调用，则M和G都会阻塞，然后P会尝试绑定空闲M或新建M，导致线程数增加，需要注意。

思考题：由于是多核，是可以被调度的，除非GOMAXPROCS=1</div>2024-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>gpm模型还是有性能问题吧？ m应该要尽量绑核，阻塞调用，应该用其它线程去处理，尽量不要占用当前m。</div>2022-10-02</li><br/>
</ul>