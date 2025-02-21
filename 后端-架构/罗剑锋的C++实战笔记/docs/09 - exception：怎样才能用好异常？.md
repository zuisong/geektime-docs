你好，我是Chrono。

上节课，我建议尽量不用裸指针、new和delete，因为它们很危险，容易导致严重错误。这就引出了一个问题，如何正确且优雅地处理运行时的错误。

实际上，想要达成这个目标，还真不是件简单的事情。

程序在运行的时候不可能“一帆风顺”，总会遇到这样那样的内外部故障，而我们写程序的人就要尽量考虑周全，准备各种“预案”，让程序即使遇到问题也能够妥善处理，保证“健壮性”。

C++处理错误的标准方案是“异常”（exception）。虽然它已经在Java、C#、Python等语言中得到了广泛的认可和应用，但在C++里却存在诸多争议。

你也可能在其他地方听到过一种说法：“**现代C++里应该使用异常**。”但这之后呢？应该怎么去用异常呢？

所以，今天我就和你好好聊聊“异常那些事”，说一说为什么要有异常，该怎么用好异常，有哪些要注意的地方。

## 为什么要有异常？

很多人认为，C++里的“异常”非常可怕，一旦发生异常就是“了不得的大事”，这其实是因为没有理解异常的真正含义。

实际上，你可以按照它的字面意思，把它理解成“**异于正常**”，就是正常流程之外发生的一些特殊情况、严重错误。一旦遇到这样的错误，程序就会跳出正常流程，甚至很难继续执行下去。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/b4/63/59bb487d.jpg" width="30px"><span>eletarior</span> 👍（51） 💬（1）<div>初识编程时，对异常处理的误解还是挺大的，可能是因为异常处理总是在教材的最后几页，觉得很难，然后就草草的误解了。之前有一份工作领导特意提到了正确地进行异常处理。后来认真学了下，接触到C++11后，才真正用起来。
异常的好处是不言自明的，加强程序的健壮性，避免大量if else形式的代码处理。坏处也是有的，比如某个函数是否抛异常，写的人不好确定，要关注具体逻辑；而用这个函数的人也不确定，可能还需要借助注释来说明这个函数会抛出了怎样的异常。而抛异常就要try 和catch处理，不处理程序就会崩溃，接口的“客户”可能会不乐意处理。
用异常时，我更多的将某个函数声明为 noexcept ,比如构造函数，而明确要抛异常的函数则声明为noexcept(false)。
而在代码里处处使用 try catch也是不明智的，需要根据具体的场景和业务来辨别。而有一点是需要特别注意的避免在catch里写真实的业务代码，不应该在里写改变整个程序的流程的代码。如果程序崩溃了，就让它崩溃吧。
</div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（20） 💬（4）<div>异常是个很重要的东西。
涉及磁盘操作的最好使用异常+调用栈，
涉及业务逻辑的最好利用日志+调用栈，
涉及指针和内存分配的还是用日志+调用栈吧，这种coredump一般是内存泄露和内存不够引起的。</div>2020-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/67/01/1497fe0a.jpg" width="30px"><span>Coder Wu</span> 👍（18） 💬（4）<div>个人感觉如果是封装功能库给其他人使用，可以考虑用异常，能方便传递错误信息给外部。如果是写业务逻辑的话，只是涉及到自身功能的错误，还是多用错误码的方式，并且配合日志，方便后续问题的跟踪。</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/93/df/5500fc5b.jpg" width="30px"><span>_smile滴水C</span> 👍（5） 💬（1）<div>老师我使用过python的try，能跳过数组越界错误，假设是用户代码，跳过并无大碍，避免直接崩溃，C++的try有跟python类似的用法吗？</div>2020-08-09</li><br/><li><img src="" width="30px"><span>Geek_6a1d96</span> 👍（4） 💬（1）<div>底层功能库采用错误码，业务逻辑部分采用观察者模型抛异常，谁注册成观察者谁处理异常。不管是log,显示在ui,或者用数据库记录异常，重启重连操作，把他们注册成观察者，就能很方便的跨类，跨dll完成异常处理。</div>2023-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6c/ea/e03fec22.jpg" width="30px"><span>泰伦卢</span> 👍（4） 💬（1）<div>禁用异常典型的有google和美国国防部或者移动端，google是因为历史包袱，以前编译器对异常支持的不太好，所以都使用的错误码方式，近些年来沿用了之前得方式，不好两种错误处理方式都穿插到代码里，国防部是因为异常处理在catch异常时候程序运行速度受影响，移动端主要是因为异常处理的程序体积会大20-30%，而我们真的那么在意程序体积吗，我们普通人使用异常简直不能再香，只是用之前需要搞明白异常处理的各种注意事项</div>2020-05-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ7mAt63VrbLZPHpeZxSc4IlBYswQSnaAB5wGePaGFDehgiaNfIxI1SJ5yIHIlmVk8hsw0RaoaSCPA/132" width="30px"><span>Stephen</span> 👍（3） 💬（1）<div>老师,&quot;通过引入一个“中间层”来获得更多的可读性、安全性和灵活性&quot;这句话中可读性和灵活性我可以理解,这是函数比较容易理解的特性,安全性怎么讲呢?请老师不惜赐教</div>2020-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/19/17245c59.jpg" width="30px"><span>Eglinux</span> 👍（3） 💬（4）<div>class my_exception : public std::runtime_error
{
public:
    using this_type     = my_exception;
    using super_type    = std::runtime_error;
public:
    my_exception(const char* msg):
        super_type(msg)
    {}

    my_exception() = default;
   ~my_exception() = default;
private:
    int code = 0;
};

请问老师，这一句是什么语法？没看懂
my_exception(const char* msg):
        super_type(msg)
    {}

列表初始化吗？但是 super_type 不是成员变量呀</div>2020-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/97/fc/0ca13c5c.jpg" width="30px"><span>xGdl</span> 👍（2） 💬（1）<div>两try-catch当函数体还是挺丑的吧</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/4a/40a2ba79.jpg" width="30px"><span>reverse</span> 👍（2） 💬（1）<div>老师，在下说一下我在工作写代码三四年的时间内的一些感受 ，在下主要用的是nodejs java  ， node这块我觉得在es6之后可以结合promise async 函数 再配合try catch 写出简洁的的函数，java 要求的比较严格  ，它的编译器会强制要求你加上 try catch 尤其是对 io操作 来说 ，实际上node的io操作也需要如此，综上所述，偏向于业务逻辑的错误码需要自己合理的定义范围自己意义，涉及到硬件磁盘的需要强制性的捕获异常，设计大于编程，函数规格大于功能本身</div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/de/3d/b74ee1af.jpg" width="30px"><span>禾众</span> 👍（1） 💬（3）<div>老师如果代码中没有写过异常处理逻辑，那么类的构造析构函数还有必要写noexcept吗？如果也需要的话，代码中到处都要加noexcept就太累赘了。</div>2020-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f3/ea/2b2adda5.jpg" width="30px"><span>EncodedStar</span> 👍（1） 💬（1）<div>异常不要乱用，乱用容易把bug隐藏起来，出现假象，让你看起来程序跑的很稳定。</div>2020-05-26</li><br/><li><img src="" width="30px"><span>java2c++</span> 👍（1） 💬（1）<div>用途1:捕获到异常后可以记录到日志文件中，很容易找到出问题的地方以及出问题的原因，比coredump分析容易多了。用途2:代码分支处理，一个经典的案例就是入参需要string转int，可以转换就走正常逻辑，不可以转换出现异常就直接返回错误原因给上游</div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/df/7a/1176bc21.jpg" width="30px"><span>Yarco</span> 👍（0） 💬（1）<div>这... 我的困扰在于当你调用一个API时，你怎么知道它是用错误码还是异常来做错误处理的？
（当然如果文档有写或者看源码是另一个回事... 似乎光凭声明看不出来）
我记得似乎 java 里方法定义的时候会写 throws？
====
    private static void setZero(int[] a,int index) throws ArrayIndexOutOfBoundsException {
        a[index] = 0;
    }
====
似乎清楚一点
</div>2023-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/b3/7b/95adaf84.jpg" width="30px"><span>学习者</span> 👍（0） 💬（1）<div>打卡</div>2023-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6b/0d/74aeb985.jpg" width="30px"><span>睡着的海豚</span> 👍（0） 💬（1）<div>异常的好处是能捕获错误，让程序继续运行不至于崩溃；坏处是同时隐藏了错误，程序的根本错误没有被解决，始终是个隐患</div>2023-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1c/95/d25d96d7.jpg" width="30px"><span>游子</span> 👍（0） 💬（1）<div>请问一下罗老师，在try代码块中主动throw一个异常，用catch(const exception&amp;)捕获不到，用catch(...)可以捕获到，是什么原因呢？</div>2022-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/e9/cf/c345a5ac.jpg" width="30px"><span>张杨</span> 👍（0） 💬（1）<div>目前而言，公司的大框架一直在用错误码进行处理</div>2022-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/e9/b7/8445f7de.jpg" width="30px"><span>辣个少年</span> 👍（0） 💬（1）<div>实现机制可以展开讲讲吗</div>2022-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8b/19/a15d060d.jpg" width="30px"><span>silverhawk</span> 👍（0） 💬（2）<div>之前有在网络连接时候用try catch，其实导致了不必要的overhead. 另外不知道笔者用过Golang没，对漫天飞舞的err ！=nil怎么看，函数默认都可以返回错误与信息两者，然后层层处理，这个虽然繁琐，但是是不是也少了不少坑而且性能更佳？</div>2020-05-31</li><br/>
</ul>