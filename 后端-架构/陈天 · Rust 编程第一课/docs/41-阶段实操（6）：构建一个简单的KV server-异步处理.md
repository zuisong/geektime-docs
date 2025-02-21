你好，我是陈天。

到目前为止，我们已经一起完成了一个相对完善的 KV server。还记得是怎么一步步构建这个服务的么？

基础篇学完，我们搭好了KV server 的基础功能（[21讲](https://time.geekbang.org/column/article/425001)、[22讲](https://time.geekbang.org/column/article/425005)），构造了客户端和服务器间交互的 protobuf，然后设计了 CommandService trait 和 Storage trait，分别处理客户端命令和存储。

在进阶篇掌握了trait的实战使用技巧之后，（[26讲](https://time.geekbang.org/column/article/429666)）我们进一步构造了 Service 数据结构，接收 CommandRequest，根据其类型调用相应的 CommandService 处理，并做合适的事件通知，最后返回 CommandResponse。

**但所有这一切都发生在同步的世界**：不管数据是怎么获得的，数据已经在那里，我们需要做的就是把一种数据类型转换成另一种数据类型的运算而已。

之后我们涉足网络的世界。（[36讲](https://time.geekbang.org/column/article/446948)）为 KV server 构造了自己的 frame：一个包含长度和是否压缩的信息的 4 字节的头，以及实际的 payload；还设计了一个 FrameCoder 来对 frame 进行封包和拆包，这为接下来构造网络接口打下了坚实的基础。考虑到网络安全，（[37讲](https://time.geekbang.org/column/article/446949)）我们提供了 TLS 的支持。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（4） 💬（2）<div>前两节感觉理解有些吃力了，今天的实操突然又让我觉得好像也没那么难了。老师实操阶段的代码真是赏心悦目。我要动手好好理解一下。</div>2021-12-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/vHujib2CCrUYNBaia32eIwTyJoAcl27vASZ9KGjSdnH1dJhD7CrSUicBib19Tf8nDibWaHjzIsvIfdqcXX6vGrH8bicw/132" width="30px"><span>罗同学</span> 👍（0） 💬（2）<div>利用异步io 重构后 process ,性能会不会有一定提升呢?</div>2021-12-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epWuRmpg9jWibtRH3mO9I0Sc9Y86fJpiaJDdLia39eib89R1raTkxMg9AOkjb0OTRkmXiaialJgHC5ve59g/132" width="30px"><span>Geek_64affe</span> 👍（4） 💬（1）<div>尝试回答第一个问题：因为当poll返回的是Pending，会直接返回出去，如果使用局部变量，每次进到poll里面都会被重置，导致逻辑错误</div>2022-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/82/54/b9cd3674.jpg" width="30px"><span>小可爱(`へ´*)ノ</span> 👍（0） 💬（0）<div>坚持✊</div>2023-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6e/72/f8e5b97e.jpg" width="30px"><span>啦啦啦啦啦啦啦</span> 👍（0） 💬（0）<div>为方便在 sink 和 stream 中对 stream 操作？因为是异步环境中使用，使用局部变量时会丢失数据吧</div>2022-02-26</li><br/>
</ul>