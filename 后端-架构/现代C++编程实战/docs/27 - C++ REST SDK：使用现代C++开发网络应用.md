你好，我是吴咏炜。

在实战篇，我们最后要讲解的一个库是 C++ REST SDK（也写作 cpprestsdk）\[1]，一个支持 HTTP 协议 \[2]、主要用于 RESTful \[3] 接口开发的 C++ 库。

## 初识 C++ REST SDK

向你提一个问题，你认为用多少行代码可以写出一个类似于 curl \[4] 的 HTTP 客户端？

使用 C++ REST SDK 的话，答案是，只需要五十多行有效代码（即使是适配到我们目前的窄小的手机屏幕上）。请看：

```c++
#include <iostream>
#ifdef _WIN32
#include <fcntl.h>
#include <io.h>
#endif
#include <cpprest/http_client.h>

using namespace utility;
using namespace web::http;
using namespace web::http::client;
using std::cerr;
using std::endl;

#ifdef _WIN32
#define tcout std::wcout
#else
#define tcout std::cout
#endif

auto get_headers(http_response resp)
{
  auto headers = resp.to_string();
  auto end =
    headers.find(U("\r\n\r\n"));
  if (end != string_t::npos) {
    headers.resize(end + 4);
  };
  return headers;
}

auto get_request(string_t uri)
{
  http_client client{uri};
  // 用 GET 方式发起一个客户端请求
  auto request =
    client.request(methods::GET)
      .then([](http_response resp) {
        if (resp.status_code() !=
            status_codes::OK) {
          // 不 OK，显示当前响应信息
          auto headers =
            get_headers(resp);
          tcout << headers;
        }
        // 进一步取出完整响应
        return resp
          .extract_string();
      })
      .then([](string_t str) {
        // 输出到终端
        tcout << str;
      });
  return request;
}

#ifdef _WIN32
int wmain(int argc, wchar_t* argv[])
#else
int main(int argc, char* argv[])
#endif
{
#ifdef _WIN32
  _setmode(_fileno(stdout),
           _O_WTEXT);
#endif

  if (argc != 2) {
    cerr << "A URL is needed\n";
    return 1;
  }

  // 等待请求及其关联处理全部完成
  try {
    auto request =
      get_request(argv[1]);
    request.wait();
  }
  // 处理请求过程中产生的异常
  catch (const std::exception& e) {
    cerr << "Error exception: "
         << e.what() << endl;
    return 1;
  }
}
```
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/32/8d/91cd624b.jpg" width="30px"><span>幻境之桥</span> 👍（94） 💬（2）<div>吴老师要是可以把所有的内容都使用 cmake 来构建，以后参考起来可以更方便啊</div>2020-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/64/52a5863b.jpg" width="30px"><span>大土豆</span> 👍（8） 💬（1）<div>老师，您认为现在这种前后端分离的架构，服务端不输出页面，纯粹只输出json的情况下，为什么C++在Http Rest API的服务端还没有广泛的应用？目前大多数还是Java(spring)或者PHP，C++基本没份额</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/ca/2a7cc193.jpg" width="30px"><span>阿鼎</span> 👍（4） 💬（1）<div>项目用vs2010，而目前可选的restful库大多是c++11的。请问老师，通过何种手段，可以使用c11库？</div>2020-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/80/d958b445.jpg" width="30px"><span>心情难以平静</span> 👍（2） 💬（1）<div>coroutine现在有好多轮子。希望标准实现快点到来。据说里面的坑较多，希望有人能先帮忙踩一踩。</div>2020-02-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKiboeh23vhCNruZ7odUjROiac6N9fx0VWAE6zBNRxJIJFZspSUTQdgu9ajg4F0fAZgdk1vBsicnib3QQ/132" width="30px"><span>在水一方</span> 👍（1） 💬（1）<div>支持长链接吗？</div>2022-02-22</li><br/><li><img src="" width="30px"><span>Geek_c18718</span> 👍（1） 💬（1）<div>吴老师，运行结果为A URL is needed，我应该去哪输入URL；完整的输入输出调用函数应该是什么样的呢？</div>2021-06-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoUlR8EWYGknKf3CG3n1gFhFKtPoticmN6AqJbbmLVibWvberBFIq3pHCHiakTI5juHVqrSnBz9lL6TQ/132" width="30px"><span>Geek_611a57</span> 👍（1） 💬（1）<div>在准备搭建一个HTTP网关，有两个问题请教：
1. 异步流例子里哪里体现异步？看着好像是要等所有task都完成才返回？异步的需求是发送之后不等，有结果返回时候回调。
2. 跟libcurl相比，哪个更适合应用于HTTP网关？</div>2021-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/7c/f8f38ad0.jpg" width="30px"><span>可爱的小奶狗</span> 👍（1） 💬（1）<div>g++ -std=c++17 -pthread test.cpp -lcpprest -lcrypto -lssl -lboost_thread -lboost_chrono -lboost_system
老师，这段手工在linux上编译test.cpp的命令，你咋知道要链接这些库呢？纯靠经验还是根据github上cpprestsdk这个项目release下的cmakelists.txt推断出出来的。</div>2020-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/ed/1c662e93.jpg" width="30px"><span>莫珣</span> 👍（1） 💬（2）<div>cpprest这个库在linux下编译起来真是太麻烦了，今天折腾了大半天竟然没有编译出来。github上给出的编译步骤过于简单。</div>2020-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/d5/5d6b3d34.jpg" width="30px"><span>hey</span> 👍（1） 💬（1）<div>支持https吗 </div>2020-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f2/21/00600713.jpg" width="30px"><span>小侠</span> 👍（0） 💬（1）<div>现在（2024.12）有没有支持C++20协程的高效稳定的网络库？</div>2024-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/20/07/80337e76.jpg" width="30px"><span>江湖中人</span> 👍（0） 💬（1）<div>老师，我想把老项目里自定义消息体TCP传输的方式都改成RPC接口方式，不知道可行不，您有什么建议吗？</div>2022-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/65/94/829f321f.jpg" width="30px"><span>天亮了</span> 👍（0） 💬（2）<div>cpprest 微软自己都不推荐在新项目使用了。参见 github README. </div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/1b/be/525e05ae.jpg" width="30px"><span>NiceBlueChai</span> 👍（0） 💬（1）<div>用crow只用10行不到可能</div>2021-12-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKsI6VdljHFtMx4cgEPpqhXiaIYQicqGcal8sIoBYQZn7tYQyPLH1FuOVP8SaYPghPIsqSa1DWjRT2A/132" width="30px"><span>Geek_227a72</span> 👍（0） 💬（1）<div>运行第一个例子后出现：A URL is needed   段错误（核心已转储）   是什么原因呢？</div>2021-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/43/c5/288c59ab.jpg" width="30px"><span>造梦师</span> 👍（0） 💬（1）<div>  initialize_with_threads 设置多少比较合理，或者说根据哪些条件设置</div>2020-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/af/0e/ac955022.jpg" width="30px"><span>申学晋</span> 👍（0） 💬（3）<div>只用过cpprest开发客户端，在windows下字符串处理还是有点麻烦。最近想开发WebSocket服务器，不知道是否能用？</div>2020-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（0） 💬（2）<div>我觉得纯从网路编程上来说，比起直接用EPOLL，然后加上一堆线程、队列、锁、条件变量啥的方便多了，隐藏了事件和循环，还是方便多了。
和JAVASCRIPT中的PROMISE已经非常像了。</div>2020-02-03</li><br/>
</ul>