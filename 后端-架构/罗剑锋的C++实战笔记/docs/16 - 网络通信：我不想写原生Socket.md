你好，我是Chrono。

在上一节课，我讲了JSON、MessagePack和ProtoBuffer这三种数据交换格式。现在，我们手里有了这些跨语言、跨平台的通用数据，该怎么与外部通信交换呢？

你肯定首先想到的就是Socket网络编程，使用TCP/IP协议栈收发数据，这样不仅可以在本地的进程间通信，也可以在主机、机房之间异地通信。

大方向上这是没错的，但你也肯定知道，原生的Socket API非常底层，要考虑很多细节，比如TIME\_WAIT、CLOSE\_WAIT、REUSEADDR等，如果再加上异步就更复杂了。

虽然你可能看过、学过不少这方面的资料，对如何处理这些问题“胸有成竹”，但无论如何，像Socket建连/断连、协议格式解析、网络参数调整等，都要自己动手做，想要“凭空”写出一个健壮可靠的网络应用程序还是相当麻烦的。

所以，今天我就来谈谈C++里的几个好用的网络通信库：libcurl、cpr和ZMQ，让你摆脱使用原生Socket编程的烦恼。

## libcurl：高可移植、功能丰富的通信库

第一个要说的库是libcurl，它来源于著名的[curl项目](https://curl.haxx.se/)，也是curl的底层核心。

libcurl经过了多年的开发和实际项目的验证，非常稳定可靠，拥有上百万的用户，其中不乏Apple、Facebook、Google、Netflix等大公司。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/72/52/8e81daf1.jpg" width="30px"><span>屈肖东</span> 👍（21） 💬（1）<div>老师什么时候可以推荐几个值得读的比较通用的开源代码，因为很多开源代码虽然很好，但是太过复杂庞大，很难阅读。或者写一篇针对如何更好的阅读源码的文章。毕竟读代码应该是学习写代码最好的方式</div>2020-06-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTICBNZjA9hW65x6g9b2iaicKUJW5gxFxtgPXH9Cqp6eyFfY1sD2hVY4dZrY5pmoK2r1KZEiaaIKocdZQ/132" width="30px"><span>赖阿甘</span> 👍（16） 💬（3）<div>说实在在看文章之前，我还不知道ZMQ这个网络通信库，哈哈。老师怎么没提到libevent、libev、asio、muduo等网络通信库，是否这些库的接口比较原始，不好用，还望解答</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/46/3a/35d9cc02.jpg" width="30px"><span>Seven</span> 👍（8） 💬（1）<div>我也知道别人的东西好，但是老师也用，会不会这样的依赖，而让我们进步缓慢，怎么看这个问题。如何破？</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/79/0f083d7d.jpg" width="30px"><span>编程国学</span> 👍（8） 💬（4）<div>军工行业，用户强调实时，一般采用udp，目前我们采用qt 自己的库，有没有好的建议</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7f/a3/23540579.jpg" width="30px"><span>robonix</span> 👍（5） 💬（1）<div>疑惑同楼上～ ASIO 据说要加到c++ 20了，应该介绍呀？</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0a/83/f916f903.jpg" width="30px"><span>风</span> 👍（4） 💬（1）<div>请教罗老师，如何看待Go语言在网络编程上的发展势头～</div>2020-06-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ7mAt63VrbLZPHpeZxSc4IlBYswQSnaAB5wGePaGFDehgiaNfIxI1SJ5yIHIlmVk8hsw0RaoaSCPA/132" width="30px"><span>Stephen</span> 👍（3） 💬（2）<div>确实感觉nanomsg更新的很慢,而且资料,影响力都不如zeromq.请教老师一个事情,如果想要学习这一块,是选择ZMQ还是nanomsg呢,我最近在看zmq作者写的一本书《ZeroMQ:云时代极速消息通信库》.但同事说,zmq已经过时了,应该学习nanomsg,给我搞的很无语,老师怎么看?</div>2021-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/63/1b/83ac7733.jpg" width="30px"><span>忧天小鸡</span> 👍（2） 💬（1）<div>有流媒体udp特别适合的库吗？刚接触c++，对编译什么的还不熟</div>2021-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/6c/87/1ec1ed1a.jpg" width="30px"><span>章北海</span> 👍（1） 💬（1）<div>老师好，最近项目中用到了Windows平台的libcurl，https通信的时候一般通过系统的证书验证服务器的证书，有两种编译方式:一种是支持win sspi的，这种情况编译的libcurl不用手动加载系统证书就可以发起https请求，但是不同的Windows系统上可能运行不了一样的程序;另一种是编译支持openssl的版本，但是Windows平台openssl有点特殊，要手动指定ca证书文件。我目前用的是后者，有个疑惑:curl根证书可以从官网手动下载，但是如何预防证书过期呢？证书过期了就访问不了https了吧，一般在项目中我们如何处理根证书的过期问题？谢谢！</div>2023-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/3f/1f529b26.jpg" width="30px"><span>henry</span> 👍（1） 💬（1）<div>请问下罗老师，ZMQ的pub&#47;sub, push&#47;pull模式和redis相比有哪些优势？

如果多个进程之间要 pub，push 不同的业务类型数据，需要在一些进程中开多个端口，管理上有点麻烦，如果加一个Broker的中间层，又有点类似redis用法的意思</div>2020-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/ee/33ef689b.jpg" width="30px"><span>土土人</span> 👍（1） 💬（1）<div>ASIO使用起来极其别扭</div>2020-06-12</li><br/><li><img src="" width="30px"><span>TC128</span> 👍（1） 💬（1）<div>HP-Socket有人用吗？</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/54/87/3b1f9de4.jpg" width="30px"><span>Confidant.</span> 👍（1） 💬（4）<div>老师，zmq的代码有一个lamda用&amp;捕获的错误，你的都可以编过吗？</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/39/85/c6110f83.jpg" width="30px"><span>黄骏</span> 👍（1） 💬（1）<div>之前用过zmq，他的创始人也非常传奇</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b4/63/59bb487d.jpg" width="30px"><span>eletarior</span> 👍（1） 💬（1）<div>涨知识了，之前http通信一直使用的原生 libcurl，看起来现在可以转cpr了，不是不知道这个库的存在，只是没人推荐不敢换而已。另外ZMQ，这个库看起来可以解决手写TCP&#47;IP通信的问题，后面会试试。
网络编程最大的坑其实是不懂网络协议，以及联调的问题，感觉不是库能解决的。但是库能解决底层封装，避免重复造轮子的痛苦。
</div>2020-06-11</li><br/><li><img src="" width="30px"><span>飞飞</span> 👍（0） 💬（1）<div>能不能用ZMQ写服务？用其他库来写客户端？如果可以的话，ZMQ的几种模式要怎么配置？</div>2024-06-07</li><br/><li><img src="" width="30px"><span>Geek_e76697</span> 👍（0） 💬（1）<div>老师您好，编译cpr.cpp时报了下面的错误，这是什么原因呀，是cpr没装好嘛？
&#47;usr&#47;local&#47;include&#47;cpr&#47;cprtypes.h:34:44: error: expected ‘)’ before ‘str’
     explicit StringHolder(std::string_view str) : str_(str) {}
                                            ^~~
&#47;usr&#47;local&#47;include&#47;cpr&#47;cprtypes.h:123:26: error: expected ‘)’ before ‘url’
     Url(std::string_view url) : StringHolder&lt;Url&gt;(url) {}
                          ^~~
In file included from &#47;usr&#47;local&#47;include&#47;cpr&#47;util.h:8:0,
                 from &#47;usr&#47;local&#47;include&#47;cpr&#47;ssl_options.h:11,
                 from &#47;usr&#47;local&#47;include&#47;cpr&#47;response.h:15,
                 from &#47;usr&#47;local&#47;include&#47;cpr&#47;async_wrapper.h:8,
                 from &#47;usr&#47;local&#47;include&#47;cpr&#47;async.h:4,
                 from &#47;usr&#47;local&#47;include&#47;cpr&#47;api.h:10,
                 from &#47;usr&#47;local&#47;include&#47;cpr&#47;cpr.h:4,
                 from cpr.cpp:13:
&#47;usr&#47;local&#47;include&#47;cpr&#47;callback.h:105:10: error: ‘optional’ in namespace ‘std’ does not name a template type
     std::optional&lt;std::reference_wrapper&lt;ProgressCallback&gt;&gt; user_cb;
</div>2023-03-09</li><br/><li><img src="" width="30px"><span>Geek_859342</span> 👍（0） 💬（1）<div>准备入门C++服务端的话，老师可以推荐一些可以快速上手的开源项目吗~想还是先从原生socket开始写
之前一直都是用的其他语言写的后端，看到C++的socket封装感觉蛮头大的，但面试偏偏很容易问到…</div>2023-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/dc/e6/ea4b2c10.jpg" width="30px"><span>........</span> 👍（0） 💬（1）<div>想咨询一下，就是 zeromq 是 GPL-3.0 协议的，在项目中使用是否存在风险呢？</div>2022-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/5a/f1/67a3e8c6.jpg" width="30px"><span>旭日东升</span> 👍（0） 💬（1）<div>cocoyaxi
看到过这个go风格的c++协程库，很方便的创建http server， 并且实现http client。
老师这个库怎么样？</div>2022-04-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKiboeh23vhCNruZ7odUjROiac6N9fx0VWAE6zBNRxJIJFZspSUTQdgu9ajg4F0fAZgdk1vBsicnib3QQ/132" width="30px"><span>在水一方</span> 👍（0） 💬（2）<div>老师，ZMQ库有没有windows版的安装包？</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/16/ea/c7caf466.jpg" width="30px"><span>ydq</span> 👍（0） 💬（1）<div>老师。make_sock接口的定义在哪里呢？
ydqun@ydqhost zmq % cat 02.cpp                                                                                                  [1]
&#47;*************************************************************************
        &gt; File Name: 02.cpp
        &gt; Author:
        &gt; Mail:
        &gt; Created Time: Thu 04 Nov 2021 02:30:06 PM CST
 ************************************************************************&#47;
#include &lt;iostream&gt;
#include &lt;zmq.hpp&gt;

using namespace std;

int main() {
    const auto addr = &quot;ipc:&#47;&#47;&#47;dev&#47;shm&#47;zmq.sock&quot;s;  &#47;&#47;通信地址

    auto recviver = [=]()
    {
        auto sock = make_sock(ZMQ_PULL);

        sock.bind(addr);
        assert(sock.connected());

        zmq::message_t msg;
        sock.recv(&amp;msg);

        string s = {msg.data&lt;char&gt;(), msg.size()};
        cout &lt;&lt; s &lt;&lt; endl;
    };

    auto sender = [=]()
    {
        auto sock = make_sock(ZMQ_PUSH);

        sock.connect(addr);
        assert(sock.connected());

        string s = &quot;hello zmq&quot;;
        sock.send(s.data(), s.size());
    };

    sender();

    recviver();

    return 0;
}



ydqun@ydqhost zmq % g++ 02.cpp   -lzmq                                                                                          [0]
02.cpp: In lambda function:
02.cpp:17:21: error: ‘make_sock’ was not declared in this scope
   17 |         auto sock = make_sock(ZMQ_PULL);
      |                     ^~~~~~~~~
02.cpp: In lambda function:
02.cpp:31:21: error: ‘make_sock’ was not declared in this scope
   31 |         auto sock = make_sock(ZMQ_PUSH);
</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/28/1e307312.jpg" width="30px"><span>鲍勃</span> 👍（0） 💬（1）<div>感谢老师的指点，我参考官方文档已经找到和解决丢消息的问题了。这里想请教下老师另外一个关于ZMQ问题：有个关于ZMQ Security的库CurveZMQ，不知道老师是否了解过呢？</div>2021-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/28/1e307312.jpg" width="30px"><span>鲍勃</span> 👍（0） 💬（5）<div>使用czmq 4.1的时候遇到了比较棘手的问题：请问如何才能保证pub-sub（整个消息流框架是dealer-router-pub-sub）的消息不丢失呢，好像比较新的库都不支持可持续化的durapub&#47;sub了。</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3c/51/c324a7de.jpg" width="30px"><span>凌云</span> 👍（0） 💬（1）<div>罗老师，请教一下，支持多语言的库，比如zmq，源码是分别使用不同语言都实现了一遍这个库么？</div>2021-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/4b/22/10df9727.jpg" width="30px"><span>Why not.</span> 👍（0） 💬（3）<div>老师 您好 想问一下 cpr可以发送put方式请求吗</div>2021-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ed/6c/6fb35017.jpg" width="30px"><span>群书</span> 👍（0） 💬（1）<div>最近用asio做服务器，压力测试好久结果宕机在asio的内存分配中， asio默认开启了小内存分配优化 这个问题一直无法解决，堆栈信息是为一个函数对象分配内存时宕机了，调用的接口是async_write_some回调函数是传入的闭包</div>2020-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ed/6c/6fb35017.jpg" width="30px"><span>群书</span> 👍（0） 💬（1）<div>老师好 我最近遇到一个asio宕机的问题 在调用async_write_some的时候宕机在asio内存分配代码里，asio默认开启了一个小内存分配优化的特性，这个问题不是必现，服务器压力测试很久才可能出现一次</div>2020-12-30</li><br/><li><img src="" width="30px"><span>JY</span> 👍（0） 💬（1）<div>实践得真知。老师每篇文章点出来的东西，都是好东西啊，哈哈，太好用了。</div>2020-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/80/f4/564209ea.jpg" width="30px"><span>纳兰容若</span> 👍（0） 💬（1）<div>老师您好
我自己下载安装cpr，在编译项目中的cpr.cpp，使用注释中的
g++ cpr.cpp -std=c++14 -lcpr -lpthread -lcurl -o a.out
发现：&#47;usr&#47;bin&#47;ld: cannot find -lcurl
我把-lcurl选项去掉也能编译运行成功，请问老师-lcurl是必须的么，这里面-lcurl起到了什么作用
</div>2020-10-30</li><br/>
</ul>