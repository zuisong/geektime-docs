你好，我是蒋德钧。今天这节课，我们来聊聊Redis的执行模型。

所谓的执行模型，就是指Redis运行时使用的进程、子进程和线程的个数，以及它们各自负责的工作任务。

你在实际使用Redis的时候，可能经常会听到类似“Redis是单线程”“Redis的主IO线程”，“Redis包含多线程”等不同说法。我也听到不少同学提出困惑和疑问：**Redis到底是不是一个单线程的程序？**

其实，彻底理解这个问题，有助于指导我们保持Redis高性能、低延迟的特性。如果说Redis就是单线程程序，那么，我们就需要避免所有容易引起线程阻塞的操作；而如果说Redis不只是单线程，还有其他线程在工作，那么，我们就需要了解多线程各自负责什么任务，负责请求解析和数据读写的线程有几个，有哪些操作是后台线程在完成，而不会影响请求解析和数据读写的。

所以，今天这节课，我就从Redis server启动后运行的进程开始，带你一边学习Redis源码中子进程和线程的创建方式，一边掌握Redis server运行时涉及到的进程、子进程和线程情况。

下面，我们先来看Redis server启动时的进程运行。

## 从shell命令执行到Redis进程创建

我们在启动Redis实例时，可以在shell命令行环境中，执行redis-server这个可执行文件，如下所示：
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（31） 💬（4）<div>1、很多人认为 Redis 是单线程，这个描述是不准确的。准确来说 Redis 只有在处理「客户端请求」时，是单线程的。但整个 Redis Server 并不是单线程的，还有后台线程在辅助处理一些工作

2、Redis 选择单线程处理请求，是因为 Redis 操作的是「内存」，加上设计了「高效」的数据结构，所以操作速度极快，利用 IO 多路复用机制，单线程依旧可以有非常高的性能

3、但如果一个请求发生耗时，单线程的缺点就暴露出来了，后面的请求都要「排队」等待，所以 Redis 在启动时会启动一些「后台线程」来辅助工作，目的是把耗时的操作，放到后台处理，避免主线程操作耗时影响整体性能

4、例如关闭 fd、AOF 刷盘、释放 key 的内存，这些耗时操作，都可以放到后台线程中处理，对主逻辑没有任何影响

5、后台线程处理这些任务，就相当于一个消费者，生产者（主线程）把耗时任务丢到队列中（链表），消费者不停轮询这个队列，拿出任务就去执行对应的方法即可：

- BIO_CLOSE_FILE：close(fd)
- BIO_AOF_FSYNC：fsync(fd)
- BIO_LAZY_FREE：free(obj) &#47; free(dict) &#47; free(skiplist)

课后题：Redis 后台任务使用 bio_job 结构体来描述，该结构体用了三个指针变量来表示任务参数，如果我们创建的任务，所需要的参数大于 3 个，你有什么应对方法来传参么？

最直接的方法就是，把参数换成数组类型，这样就可以传递任意数量参数了。因为这里 Redis 的后台任务都比较简单，最多 3 个参数就足够满足需求，所以 job 直接写死了 3 个参数变量，这样做的好处是维护起来简单直接。</div>2021-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（10） 💬（0）<div>感谢老师的文章，发现老师前面的问题都是为了这章节埋下伏笔的，一样首先回答老师的提问：有什么应对方法来传参么？
答：
    最好的方式就是使用指针数组，因为指针数组本身就是一个个指针，可以通过index的顺序标记参数的含义类型，通过index就能快速获取不同的参数对应的指针（这个方案在最新的Redis代码中也有体现）

本篇文章确实让我赞叹，老师刚好通过本篇文章，联合前面几篇文章的问题，一气呵成的给出解答，那么我这边就借老师的气场补充一下我自己的理解和认识：

    1、Redis是一个多进程多线程的程序：
        通过这篇文章也能很清晰的认识到，在Redis中不但有fork的方式创建进程，也有通过pthread_create的方式创建线程，二者都能起到异步执行任务的效果

    2、fork是一个沉重的方案：
        除了以守护进程的方式启动时候会进行fork，bgsave也会进行fork。但是fork比thread的代价大的多，fork出来的子进程会复制一份父进程的虚拟地址表（虚拟内存技术，子进程复制父进程的地址表，复用原有的地址空间，当某个地址上的数据涉及修改的时候才会把数据复制一份到自己的地址空间）从而也可能会导致出现写时复制等内存高损耗的开销。

    3、Thread需要解决并发问题：
        多线程虽然资源开销没有fork那么沉重，但是由于多线程的地址空间都属于同一个进程（线程属于进程），那么必然要解决并发问题。然而Redis的设计很巧妙，无论是bioInit的bioProcessBackgroundJobs使用分type的方式让每给线程依次执行列表上的任务，还是initThreadedIO（老师本篇没提到）使用信号量的方式控制线程的协调，都能避开内存共享带来的并发问题，从而即享受了多线程的优势，又避免了多线程的劣势。

读完本篇文章，非常建议大家去阅读一下《深入理解计算机系统》的 【第8章-异常控制流】 和 【第9章-虚拟内存】</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（10） 💬（0）<div>今天这节课收获满满，以前看源码的时候，没注意过daemonize()方法，因为不是做C语言的，因此只是想着后台启动，没想到原始是这么启动起来的。

回答下问题，其实这个问题Redis的作者在源码中已经注释了
struct bio_job {
    time_t time; &#47;* Time at which the job was created. *&#47;
    &#47;* Job specific arguments pointers. If we need to pass more than three
     * arguments we can just pass a pointer to a structure or alike. *&#47;
    void *arg1, *arg2, *arg3;
};
void*代表任意类型的指针，因此当参数多于三个时，可以传递数组或者结构。</div>2021-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/cf/851dab01.jpg" width="30px"><span>Milittle</span> 👍（4） 💬（0）<div>这节课我学到了什么：
1. 第一、redis不是单线程的，而是一个主线程，处理IO，另外有三个线程分别处理关闭fd、异步AOF刷盘、延迟释放。
2. 我们从bio文件中可以看到函数之间的配合。

回答一下课后题目：
可以看到最新版的代码，redis开发人员已经把这个重构了：
bio_job里面包含了fd（给关闭文件和异步刷盘用的），lazy_free_fn、free_args给延迟释放用的，一个是函数，一个是函数所需要用的参数。
备注：结合老师讲的源码版本和自己结合最新的版本看，你会在这个过程里面学到不少，有一些时候问题，就被解决了，你也可以从中学习到一些。</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/89/52/b96c272d.jpg" width="30px"><span>🤐</span> 👍（0） 💬（0）<div>想起了我自己为私有化设计的定时任务调度。</div>2022-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/5d/35/b1eb964a.jpg" width="30px"><span>🐟🐙🐬🐆🦌🦍🐑🦃</span> 👍（0） 💬（1）<div>bio_pending[type] 的++ 和 -- 不是原子的吧，一个消费线程--，提交任务在++,看着也没加锁，？？？？</div>2022-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/6a/be36c108.jpg" width="30px"><span>ikel</span> 👍（0） 💬（0）<div>pthread_attr_setstacksize 函数，来重新设置线程栈大小，这样做的目的是什么呢
对内存操作单线程我觉得是为了避免锁操作的资源开销吧</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（2）<div>后台线程有3个，后台进程有几个的？</div>2021-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6c/b5/32374f93.jpg" width="30px"><span>可怜大灰狼</span> 👍（0） 💬（0）<div>如果所需要参数大于3个，我想可以把多个参数都封装到一个list或者dict中，然后占用arg1向实际业务方法传，只不过实际业务方法代码需要从list或dict再拆解出参数。</div>2021-08-21</li><br/>
</ul>