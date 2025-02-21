在上一讲里，我们在本机的最小化环境了做了两个HTTP协议的实验，使用Wireshark抓包，弄清楚了HTTP协议基本工作流程，也就是“请求-应答”“一发一收”的模式。

可以看到，HTTP的工作模式是非常简单的，由于TCP/IP协议负责底层的具体传输工作，HTTP协议基本上不用在这方面操心太多。单从这一点上来看，所谓的“超文本传输协议”其实并不怎么管“传输”的事情，有点“名不副实”。

那么HTTP协议的核心部分是什么呢？

答案就是它传输的报文内容。

HTTP协议在规范文档里详细定义了报文的格式，规定了组成部分，解析规则，还有处理策略，所以可以在TCP/IP层之上实现更灵活丰富的功能，例如连接控制，缓存管理、数据编码、内容协商等等。

## 报文结构

你也许对TCP/UDP的报文格式有所了解，拿TCP报文来举例，它在实际要传输的数据之前附加了一个20字节的头部数据，存储TCP协议必须的额外信息，例如发送方的端口号、接收方的端口号、包序号、标志位等等。

有了这个附加的TCP头，数据包才能够正确传输，到了目的地后把头部去掉，就可以拿到真正的数据。

![](https://static001.geekbang.org/resource/image/17/95/174bb72bad50127ac84427a72327f095.png?wh=3000%2A1681)

HTTP协议也是与TCP/UDP类似，同样也需要在实际传输的数据前附加一些头数据，不过与TCP/UDP不同的是，它是一个“**纯文本**”的协议，所以头数据都是ASCII码的文本，可以很容易地用肉眼阅读，不用借助程序解析也能够看懂。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（153） 💬（6）<div>1:如果拼 HTTP 报文的时候，在头字段后多加了一个 CRLF，导致出现了一个空行，会发生什么？
在header 下面第一个空行以后都会被当作body 体

2:讲头字段时说“:”后的空格可以有多个，那为什么绝大多数情况下都只使用一个空格呢？
头部多一个空格就会多一个传输的字节，去掉无用的信息，保证传输的头部字节数尽量小</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ab/e1/079ee6e3.jpg" width="30px"><span>壹笙☞漂泊</span> 👍（47） 💬（1）<div>答题：
1、头字段后多了一个CRLF，会被当做body处理
2、节省资源
总结：
HTTP协议的请求报文和相应报文的结构基本相同：
    1、起始行（start line）：描述请求或响应的基本信息
    2、头部字段集合（header）：使用key-value形式更详细的说明报文
    3、消息正文（entity）：实际传输的数据，它不一定是纯文本，可以是图片、视频等二进制数据

HTTP协议必须有header，可以没有body。而且header之后必须要有一个空行，也就是  “CRLF”，十六进制的“0D0A”

请求行（请求报文里的起始行）：
    描述了客户端想要如何操作服务器端的资源
起始行由三部分构成：
    1、请求方法：标识对资源的操作：GET&#47;POST&#47;PUT
    2、请求目标：通常是一个URI，标记了请求方法要操作的资源
    3、版本号：标识报文使用的HTTP协议版本
以上三部分，通常使用空格分隔，最后用CRLF换行

状态行：（响应报文里的起始行）：
    服务器响应的状态
状态行也是由三部分构成：
    1、版本号：标识报文使用的HTTP协议版本
    2、状态码：三位数，用代码形式标识处理的结果，比如200是成功，500是服务器错误
    3、原因：作为数字状态码补充，是更详细的解释文字，帮助人理解原因
以上三部分，通常也使用空格分隔，最后用CRLF换行

头部字段：
请求行或状态行再加上头部字段集合就构成了HTTP报文里完整的请求头或响应头。

头部字段是key-value的形式，用“:”分隔，最后用CRLF换行标识字段结束

头字段，不仅可以使用标准的Host等已有开头，也可以任意添加自定义头

注意：
    1.字段名不区分大小写，例如“Host&quot;也可以写成“host”,但首字母大写的可读性更好;
    2.字段名里不允许出现空格，可以使用连字符“一”，但不能使用下划线“”。例    如，“test-name”是合法的字段名，而“test name&quot;&quot;test_ name&#39; 是不正确的字段名;
    3.字段名后面必须紧接着“:”，不能有空格，而“:” 后的字段值前可以有多个空格;
    4.字段的顺序是没有意义的，可以任意排列不影响语义; 
    5.字段原则上不能重复，除非这个字段本身的语义允许，例如Set-Cookie。

常用头字段

基本分为四类：
    1.通用字段:在请求头和响应头里都可以出现;
    2.请求字段:仅能出现在请求头里，进一步说明请求信息或者额外的附加条件;
    3.响应字段:仅能出现在响应头里，补充说明响应报文的信息;
    4.实体字段:它实际上属于通用字段，但专门描述body的额外信息。

Host：请求字段，只能出现在请求头。是必须出现的字段
User-Agent：是请求字段，只能出现在请求头里。
Date：是通用字段，通常出现在响应头，标识HTTP报文创建的时间，客户端可以使用这个时间再搭配其他字段决定缓存策略
Server字段是响应字段，只能出现在响应头里。告诉客户端当前正在提供Web服务的软件名称和版本号。
Content-Length：标识报文里body的长度。</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/2e/c6/1ebf8edd.jpg" width="30px"><span>Mèow</span> 👍（30） 💬（1）<div>请问Host虽然是规定必须的，但是不加的话也没问题吗？我看掘金的主页就没有host，而是用的几个私有字段
:authority: juejin.cn
:method: GET
:path: &#47;
:scheme: https</div>2021-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/72/2d35f80c.jpg" width="30px"><span>xing.org1^</span> 👍（25） 💬（5）<div>老师，请问为什么请求头太大会占用服务器资源呢？</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/78/2828195b.jpg" width="30px"><span>隰有荷</span> 👍（14） 💬（1）<div>为啥老师懂的这么多！唉，何时能学成你的一半水平，我也就满意了😂</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/81/51/4999f121.jpg" width="30px"><span>qzmone</span> 👍（11） 💬（2）<div>我也不是很理解这个host字段，比如一个网站的域名解析后的IP是负载均衡的IP，负载均衡后面对应的是web主机集群，那么这个host是什么，浏览器怎么知道虚拟主机的真实IP呢</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/d8/c0/8d07d9b7.jpg" width="30px"><span>10</span> 👍（10） 💬（4）<div>我也遇到了前面2个同学提到的遗失对主机的连接的问题，但老师您的回答貌似没解决问题，我再确认一下，在浏览器可以顺利访问www.chrono.com的情况下：

1. Win+R打开Telnet后，输入 “open www.chrono.com 80”，点击回车，然后界面显示“正在连接open www.chrono.com 80”
2. 上一步漫长的等待后，界面显示“按任意键继续”
3. 我按了空格，界面上新增一行“遗失对主机的连接”

另外老师您说的“按Ctrl+]键，然后回车”我在上面1步和第3步都试过 每次都显示“无效指令”

请问我是哪一步出的问题呢</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/8c/e3/b9e926f9.jpg" width="30px"><span>面罩</span> 👍（8） 💬（7）<div>说一下老师所说的 telnet 怎么用：
1. win + r，输入 telnet，确定后就打开了
2. 在界面中输入 open www.chrono.com 80，并回车
3. 接下来会显示 “正在连接 www.chrono.com....”，就已经表示连接上了
4. 接下来先 ctrl + ]，然后再 enter，即可进入黑乎乎的编辑页面
5. 在编辑页面输入老师给的请求信息（我是手敲的，我复制过去貌似直接发请求了，应该是复制的格式不对，导致失败了）
6. 输入请求信息后，连续点击两次 enter，即可发送请求</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/3b/af/2e3618a8.jpg" width="30px"><span>文華</span> 👍（8） 💬（1）<div>使用Telnet遇到问题的同学请注意，“Escape Character is &#39;Ctrl+]&#39;&quot;这提示的意思是已经连接到了服务器，按Ctrl+]就结束连接退出了，所以看到提示时直接将HTTP请求内容贴上去，再按回车加入空行，就能得到响应了。</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（8） 💬（1）<div>支持老师原声。赞一个</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（7） 💬（9）<div>老师，不是通过ip+port+资源路径确定的吗，咋又通过header中的host来找呢，不懂。</div>2019-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（7） 💬（1）<div>老师讲到了 Host，可以顺便讲一下 Host 攻击吗？</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/f3/7fcc98e6.jpg" width="30px"><span>高翔Gilbert</span> 👍（5） 💬（2）<div>为什么不找人读呢？听起来好吃力</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fa/07/1d50f530.jpg" width="30px"><span>Osborne</span> 👍（4） 💬（1）<div>hosts的实验终于成了，问题有2：host太容易失效了，用vpn的、代理的都容易干扰hosts，360安全卫士貌似也影响。二是其中表述“右键粘贴文本”这句话容易误导把界面的粘贴功能带过来的剪贴板内容都粘过来，而俩个一起粘贴是有问题的。且表现会很诡异。几个问题交织到一起的时候，就更糟了。多种可能组合，让你简直觉得鬼打墙，而telnet本身在windows的cmd下还有诡异的现象，光标位置乱跳。一个小小的实操，废了我2小时时间。极客时间编辑该反省下自己了。</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/11/b9/abb7bfe3.jpg" width="30px"><span>小桶</span> 👍（4） 💬（1）<div>对window一直显示正在连接的问题，我的解决方案是直接使用telnet www.chrono.com 80，而不是使用open www.chrono.com 80</div>2019-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/96/e3/dd40ec58.jpg" width="30px"><span>火车日记</span> 👍（3） 💬（1）<div>老师有个点是不是漏讲了，头部字段content_type，和body的数据格式</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a6/b6/27412d76.jpg" width="30px"><span>sc</span> 👍（3） 💬（1）<div>2. 讲头字段时说“:”后的空格可以有多个，那为什么绝大多数情况下都只使用一个空格呢？
请问老师，空格可以一个都不加吧，telnet测试也可以正确返回，为什么还要使用一个空格</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（3） 💬（1）<div>文中说 http 的头部不能使用下划线，感觉是有问题的，就拿 nginx 来说吧，虽然nginx 默认是忽略下划线的头部的，但是可以设置 underscores_in_headers on;  来获取下划线的头部

对于常用的 web application 服务器，下划线的头部好像是可以直接获取到的，不用配置什么

老师你说的不能使用下划线是  RFC规范吗？</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/67/2b/3a53ca86.jpg" width="30px"><span>Vera</span> 👍（2） 💬（1）<div>1.新手实操之后理解了下，多了个CRLF相当于在请求行输入后直接退出连接，最终发送请求失败。
2.测试过多的空格发送后，发现会导致content-length增加。增加冗余的数据大小，所以不建议多写空格</div>2021-02-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/5kv7IqibneNnMLqtWZQR5f1et8lJmoxiaU43Ttzz3zqW7QzBqMkib8GCtImKsms7PPbWmTB51xRnZQAnRPfA1wVaw/132" width="30px"><span>Geek_63bb29</span> 👍（2） 💬（1）<div>老师，如何理解“纯文本协议”啊，http报文不是都要加上tcp、ip、mac头，然后二进制流发出去吗？http是纯文本协议，http2是二进制协议，仅看这个特性的话，他两的不同是不是在于，应用层接受到二进制数据以后，http需要将其转换成字符，然后才能确定报文类型，但是http2不要转换前就能确定报文类型，可以这样理解吗？烦请老师指点呀~</div>2020-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/6b/a98162a1.jpg" width="30px"><span>winner_0715</span> 👍（2） 💬（1）<div>空行和CRLF不是同一个东西吧</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/c8/8627f5c1.jpg" width="30px"><span>右耳朵猫咪</span> 👍（2） 💬（2）<div>请问token是不是放在请求头里？</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/de/18/b2635f3c.jpg" width="30px"><span>李彬</span> 👍（2） 💬（4）<div>老师，这个telnet每次编辑模式输入
GET &#47;09-1 HTTP&#47;1.1 Host: www.chrono.com或GET &#47; HTTP&#47;1.1 Host: www.chrono.com，按回车都没有发起请求，按一次回车会提示“无效指令”，按两次回车就进入一个完全空白的页面，只能ctrl+z终止，会提示“遗失对主机的连接”，并且报&quot;HTTP&#47;1.1 400 Bad Request(text&#47;html)&quot;，结果现在wireshark只能捕获&quot; open www.chrono.com 80&quot;这个连接动作的tcp三次握手,然后就自动断开连接了</div>2019-06-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7JkdLdZXNYZeopVSxeI8ml4MptQMCWI7oIHaJpfYuYjlV9Efic7x19lWickckLQzmTuFlgCVmVicZ9A/132" width="30px"><span>Geek_0e3b40</span> 👍（1） 💬（1）<div>关于打开telnet的步骤总结：
1. win+R，输入cmd
2. 输入telnet www.chrono.com 80
3. 到这一步应该在一个全黑的界面，输入ctrl+]
4. 回车
5. 到这里又到全黑的界面，但这里可以输入http报文了</div>2022-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/52/66/3e4d4846.jpg" width="30px"><span>includestdio.h</span> 👍（1） 💬（2）<div>1.第一个CRLF后均为body
2.节省资源</div>2021-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/8f/ec/c30b45d4.jpg" width="30px"><span>Geek_Maggie</span> 👍（1） 💬（1）<div>如果拼 HTTP 报文的时候，在头字段后多加了一个 CRLF，导致出现了一个空行，会发生什么？
第一个空行以后都会被当作body来处理

讲头字段时说“:”后的空格可以有多个，那为什么绝大多数情况下都只使用一个空格呢？
多个空格就会多传输字节，去掉无用的信息，保证传输的头部字节数尽量小。</div>2021-03-08</li><br/><li><img src="" width="30px"><span>牛</span> 👍（1） 💬（1）<div>telnet小白留言：
MacOS系统使用telnet发送Get请求时有个坑，在执行oepn www.chrono.com 80命令，连接上了服务器之后，已经直接进入了编辑模式，无需使用提示的快捷键切换模式了。

</div>2021-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/99/44378317.jpg" width="30px"><span>李皮皮皮皮皮</span> 👍（1） 💬（1）<div>大头儿子的比喻太赞了，这下一辈子都忘不了了</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/3f/684f858e.jpg" width="30px"><span>勇敢黄瓜</span> 👍（1） 💬（1）<div>1. 如果拼 HTTP 报文的时候，在头字段后多加了一个 CRLF，导致出现了一个空行，会发生什么？
这样会导致server解析报文时，到空行出判断为头部字段已结束，将此空行后面的部分解析为body；如果此空行在Host头前，那么报文会解析错误；如果空行在Host头后，那么报文可以解析，但服务端处理会异常；


2. 讲头字段时说“:”后的空格可以有多个，那为什么绝大多数情况下都只使用一个空格呢？
数据的传输总是为了在更短的时间传输更多的数据，使用多个空格造成网络资源浪费，所以只使用一个空格。</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9d/5d/3fdead91.jpg" width="30px"><span>レイン小雨</span> 👍（1） 💬（2）<div>老师我请教您一个问题，就是最近做了个ReactNative的项目，里面的网络请求使用的是新一代的浏览器Fetch请求，导致我们在开发的过程中无法在Chrome的开发者工具中查看网络请求，因为它不是一个XHR，我就很迷惑Fetch是处在什么位置，它是特殊的http吗？</div>2019-06-29</li><br/>
</ul>