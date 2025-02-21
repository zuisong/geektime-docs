你好，我是蒋德钧。

在前面的课程中，我们主要学习了Redis服务器端的机制和关键技术，很少涉及到客户端的问题。但是，Redis采用的是典型的client-server（服务器端-客户端）架构，客户端会发送请求给服务器端，服务器端会返回响应给客户端。

如果要对Redis客户端进行二次开发（比如增加新的命令），我们就需要了解请求和响应涉及的命令、数据在客户端和服务器之间传输时，是如何编码的。否则，我们在客户端新增的命令就无法被服务器端识别和处理。

Redis使用RESP（REdis Serialization Protocol）协议定义了客户端和服务器端交互的命令、数据的编码格式。在Redis 2.0版本中，RESP协议正式成为客户端和服务器端的标准通信协议。从Redis 2.0 到Redis 5.0，RESP协议都称为RESP 2协议，从Redis 6.0开始，Redis就采用RESP 3协议了。不过，6.0版本是在今年5月刚推出的，所以，目前我们广泛使用的还是RESP 2协议。

这节课，我就向你重点介绍下RESP 2协议的规范要求，以及RESP 3相对RESP 2的改进之处。

首先，我们先来看下客户端和服务器端交互的内容包括哪些，毕竟，交互内容不同，编码形式也不一样。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/cf/81/96f656ef.jpg" width="30px"><span>杨逸林</span> 👍（10） 💬（2）<div>语音中有一个和文本内容不符合的地方，就是那个“正常的 0 字符”。语音是正常的空字符，文本就是前面引号的部分，是哪个对的呢，还是都对的？</div>2020-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/38/4c9cfdf4.jpg" width="30px"><span>谢小路</span> 👍（3） 💬（1）<div>RESP 也可以通过抓包的方式来具体查看格式，使用 tcpdump 进行抓包得到的文件，使用 wireshark 进行查看，也比较直观。</div>2020-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（125） 💬（3）<div>key为mylist，使用LPUSH写入是1、2、3.3、4、hello，执行LRANGE mylist 0 4命令时，实例返回给客户端的编码结果是怎样的？

测试结果如下，写入命令：

127.0.0.1:6479&gt; LPUSH mylist 1 2 3.3 4 hello
(integer) 5
127.0.0.1:6479&gt; LRANGE mylist 0 4
1) &quot;hello&quot;
2) &quot;4&quot;
3) &quot;3.3&quot;
4) &quot;2&quot;
5) &quot;1&quot;

使用telnet发送命令，观察结果：

Trying 127.0.0.1...
Connected to localhost.
Escape character is &#39;^]&#39;.

LRANGE mylist 0 4
*5
$5
hello
$1
4
$3
3.3
$1
2
$1
1

Redis设计的RESP 2协议非常简单、易读，优点是对于客户端的开发和生态建设非常友好。但缺点是纯文本，其中还包含很多冗余的回车换行符，相比于二进制协议，这会造成流量的浪费。但作者依旧这么做的原因是Redis是内存数据库，操作逻辑都在内存中进行，速度非常快，性能瓶颈不在于网络流量上，所以设计放在了更加简单、易理解、易实现的层面上。

Redis 6.0重新设计RESP 3，比较重要的原因就是RESP 2的语义能力不足，例如LRANGE&#47;SMEMBERS&#47;HGETALL都返回一个数组，客户端需要根据发送的命令类型，解析响应再封装成合适的对象供业务使用。而RESP 3在响应中就可以明确标识出数组、集合、哈希表，无需再做转换。另外RESP 2没有布尔类型和浮点类型，例如EXISTS返回的是0或1，Sorted Set中返回的score是字符串，这些都需要客户端自己转换处理。而RESP 3增加了布尔、浮点类型，客户端直接可以拿到明确的类型。

另外，由于TCP协议是面向数据流的，在使用时如何对协议进行解析和拆分，也是分为不同方法的。常见的方式有4种：

1、固定长度拆分：发送方以固定长度进行发送，接收方按固定长度截取拆分。例如发送方每次发送数据都是5个字节的长度，接收方每次都按5个字节拆分截取数据内容。

2、特殊字符拆分：发送方在消息尾部设置一个特殊字符，接收方遇到这个特殊字符就做拆分处理。HTTP协议就是这么做的，以\r\n为分隔符解析协议。

3、长度+消息拆分：发送方在每个消息最前面加一个长度字段，接收方先读取到长度字段，再向后读取指定长度即是数据内容。Redis采用的就是这种。

4、消息本身包含格式：发送方在消息中就设置了开始和结束标识，接收方根据这个标识截取出中间的数据。例如&lt;start&gt;msg data&lt;end&gt;。

如果我们在设计一个通信协议时，可以作为参考，根据自己的场景进行选择。</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（3） 💬（0）<div>文中最后的小结完美总结了本篇的主要内容。这篇可以先看小结内容，然后再通读全文，这样整体脉络会比较清晰。
另外文中的一张总结图很棒，一图胜千言。
</div>2021-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（1） 💬（0）<div>在 macOS 上默认似乎是没有 telnet 的，放狗搜索，似乎是可以安装一个 telnet，也可以使用 ssh 或者 nc 工具。

我尝试使用 ssh 被拒绝了，然后使用 nc 连上了阿里云的 Redis 实例。

```
#&gt; nc -v r-2zede1d2b3b2b312pd.redis.rds.aliyuncs.com 6379
Connection to r-2zede0d1b1b2b564pd.redis.rds.aliyuncs.com port 6379 [tcp&#47;*] succeeded!
```

连接之后，是没有命令提示符的。直接 hello world，需要输入密码

```
get hello
-NOAUTH Authentication required.
auth myPassword
+OK
get hello
$5
world
```

然后看一下专栏中提到的例子

```
LRANGE mylist 0 4
*5
$5
hello
$1
4
$3
3.3
$1
2
$1
1
set testkey testvalue
+OK
get testkey
$9
testvalue
hset testhash a 1 b 2 c 3
:3
put testkey2 testvalue
-ERR unknown command `put`, with args beginning with: `testkey2`, `testvalue`,
```

可以看到 mylist 中的值都是使用长字符串类型（RESP Bulk String）来回复的，还能看到 以“:”开头的简单字符串类型（RESP Simple Strings），用“+”号开头的整数类型（RESP Integer）和用“-”号开头的错误类型（RESP Errors）

用“*”号开头的数组编码类型（RESP Arrays）没有看到具体的例子。

最后，关于 Hash 类型的 testhash 和 Sorted Set 类型的 testzset 的例子

```
hset testhash a 1 b 2 c 3
:0
hgetall testhash
*6
$1
a
$1
1
$1
b
$1
2
$1
c
$1
3
zadd testzset 1 &quot;a&quot;
:1
zadd testzset 2 &quot;b&quot;
:1
zadd testzset 3 &quot;c&quot;
:1
zrange testzset 0 3 withscores
*6
$1
a
$1
1
$1
b
$1
2
$1
c
$1
3
```</div>2021-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（1） 💬（0）<div>用旧的客户端连接6没看到返回合适有变化，2和3的兼容是服务端做的嘛？</div>2021-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/6a/26/09c1221e.jpg" width="30px"><span>GJXAIOU</span> 👍（0） 💬（0）<div>MAC  ARM 验证示例：
```shell
brew install telnet
```
然后使用 telnet
```shell
telnet 127.0.0.1 6379
```
然后可以执行 Redis 命令（和 telnet 同窗口就行）：
```shell
GET key 
$3
112
SET KEY 123
+OK
GET KEY
$3
123
```
```</div>2024-08-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ7Fd19uVrF8RmRg9ibNdHXEdFV7V8LypzrTZtWQibP8PaWjM054SghI8QJeIZaOQNsdY5zib5Yh2JwQ/132" width="30px"><span>Geek_LIAO</span> 👍（0） 💬（0）<div>lpush mylist 1 2 3.3 4 hello
:5                                                                                                                                

lrange mylist 0 4
*5
$5
hello
$1
4
$3
3.3
$1
2
$1
1</div>2023-02-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ7Fd19uVrF8RmRg9ibNdHXEdFV7V8LypzrTZtWQibP8PaWjM054SghI8QJeIZaOQNsdY5zib5Yh2JwQ/132" width="30px"><span>Geek_LIAO</span> 👍（0） 💬（0）<div>在 telnet 中，向 Redis 实例发送用 RESP 2 协议编写的命令操作，为什么报错？

*2\r\n$3\r\nGET\r\n$7\r\ntestkey\r\n

-ERR Protocol error: invalid multibulk length</div>2023-02-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ7Fd19uVrF8RmRg9ibNdHXEdFV7V8LypzrTZtWQibP8PaWjM054SghI8QJeIZaOQNsdY5zib5Yh2JwQ/132" width="30px"><span>Geek_LIAO</span> 👍（0） 💬（0）<div>字符串长度达到多长时不使用简单字符串类型，而使用长字符串类型进行编码呢？</div>2023-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2e/7e/ebc28e10.jpg" width="30px"><span>NULL</span> 👍（0） 💬（0）<div>Redis Serialization Protocol (RESP) Specifications
https:&#47;&#47;github.com&#47;redis&#47;redis-specifications&#47;tree&#47;master&#47;protocol</div>2022-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9e/d8/49a2626e.jpg" width="30px"><span>少</span> 👍（0） 💬（0）<div>Redis6 默认也是支持RESP2的</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/89/f0/3e90365b.jpg" width="30px"><span>L-an</span> 👍（0） 💬（0）<div>老师，HSET testhash a 1 b 2 c 3  这个命令是不是有问题呢？
长字符串类型返回长度之后应该有换行吧，应该是： $9\r\ntestvalue\r\n</div>2021-08-24</li><br/><li><img src="" width="30px"><span>dfuru</span> 👍（0） 💬（0）<div>*5\r\n:1\r\n:2\r\n,3.3\r\n:4\r\n$5\r\nhello\r\n</div>2020-11-05</li><br/>
</ul>