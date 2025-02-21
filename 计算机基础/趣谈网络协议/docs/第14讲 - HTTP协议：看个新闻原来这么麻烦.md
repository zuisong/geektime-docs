前面讲述完**传输层**，接下来开始讲**应用层**的协议。从哪里开始讲呢，就从咱们最常用的HTTP协议开始。

HTTP协议，几乎是每个人上网用的第一个协议，同时也是很容易被人忽略的协议。

既然说看新闻，咱们就先登录 [http://www.163.com](http://www.163.com) 。

[http://www.163.com](http://www.163.com) 是个URL，叫作**统一资源定位符**。之所以叫统一，是因为它是有格式的。HTTP称为协议，www.163.com是一个域名，表示互联网上的一个位置。有的URL会有更详细的位置标识，例如 [http://www.163.com/index.html](http://www.163.com/index.html) 。正是因为这个东西是统一的，所以当你把这样一个字符串输入到浏览器的框里的时候，浏览器才知道如何进行统一处理。

## HTTP请求的准备

浏览器会将www.163.com这个域名发送给DNS服务器，让它解析为IP地址。有关DNS的过程，其实非常复杂，这个在后面专门介绍DNS的时候，我会详细描述，这里我们先不管，反正它会被解析成为IP地址。那接下来是发送HTTP请求吗？

不是的，HTTP是基于TCP协议的，当然是要先建立TCP连接了，怎么建立呢？还记得第11节讲过的三次握手吗？

目前使用的HTTP协议大部分都是1.1。在1.1的协议里面，默认是开启了Keep-Alive的，这样建立的TCP连接，就可以在多次请求中复用。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="" width="30px"><span>起风了001</span> 👍（75） 💬（7）<div>以前一直不是很确定Keep-Alive的作用, 今天结合tcp的知识, 终于是彻底搞清楚了. 其实就是浏览器访问服务端之后, 一个http请求的底层是tcp连接, tcp连接要经过三次握手之后,开始传输数据, 而且因为http设置了keep-alive,所以单次http请求完成之后这条tcp连接并不会断开, 而是可以让下一次http请求直接使用.当然keep-alive肯定也有timeout, 超时关闭.</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/68/006ba72c.jpg" width="30px"><span>Untitled</span> 👍（33） 💬（1）<div>QUIC说是基于UDP，无连接的，但是老师又说到是面向连接的，看的晕乎乎的。。</div>2018-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/25/348b4d76.jpg" width="30px"><span>墨萧</span> 👍（26） 💬（2）<div>每次http都要经过TCP的三次握手四次挥手吗</div>2018-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/af/00/9b49f42b.jpg" width="30px"><span>skye</span> 👍（18） 💬（4）<div>“一前一后，前面 stream 2 的帧没有收到，后面 stream 1 的帧也会因此阻塞。”这个和队首阻塞的区别是啥，不太明白？</div>2018-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0f/c0/e6151cce.jpg" width="30px"><span>花仙子</span> 👍（13） 💬（2）<div>UDP不用保持连接状态，不用建立更多socket，是不是就说服务端只能凭借客户端的源端口号来判定是客户端哪个应用发送的，是吗？</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/0d/3dc5683a.jpg" width="30px"><span>柯察金</span> 👍（11） 💬（4）<div>怎么说呢，感觉听了跟看书效果一样的，比较晦涩。因为平时接触比较多的就是 tcp http ，结果听了感觉对实际开发好像帮助不大，因为都是一个个知识点的感觉，像准备考试。希望能结合实际应用场景，讲解。</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a7/92/d4ce2462.jpg" width="30px"><span>传说中的风一样</span> 👍（8） 💬（2）<div>cache control部分讲错了，max–age不是这么用的</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d6/39/6b45878d.jpg" width="30px"><span>意无尽</span> 👍（6） 💬（1）<div>哇，竟然坚持到这里了（虽然一半都还不到），虽然前面也有很多不懂。基本上从第二章开时候每一节都会花费一两个小时去理解，但是花费确实值啊，让我一个网络小白慢慢了解了网络的各个方面，感觉像是打开了另一个奇妙的世界！相当赞，后期还要刷第二遍！学完这个必须继续购买趣谈Linux操作系统！感谢刘超老师！</div>2020-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/72/67/aa52812a.jpg" width="30px"><span>stark</span> 👍（6） 💬（1）<div>有个地方不是很明白，就是里面说的流数据，比如，我在实际的应用里怎么查看下这些数据什么，比如像top这样的，怎么查看呢？</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5f/dc/d16e0923.jpg" width="30px"><span>heliang</span> 👍（4） 💬（1）<div>http2.0 并行传输同一个请求不同stream的时候，如果“”前面 stream 2 的帧没有收到，后面 stream1也会阻塞&quot;，是阻塞在tcp重组上吗

</div>2019-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/e8/94365887.jpg" width="30px"><span>ieo</span> 👍（2） 💬（3）<div>有两个问题，麻烦老师回答下：1:一个页面请求了同一域名下的两个地址，如果没有用keep-alive，三次握手会进行两次吗？如果有了这个设置，就会进行一次吗？
2:一个请求发到服务器后，服务器给客户端返回内容时，还要和客户端三次握手吗？如果还需要握手的话，为啥不能用客户端和服务器建立的tcp连接呢？</div>2019-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a5/40/ad00a484.jpg" width="30px"><span>- -</span> 👍（2） 💬（1）<div>“当其中一个数据包遇到问题，TCP 连接需要等待这个包完成重传之后才能继续进行。虽然 HTTP 2.0 通过多个 stream，使得逻辑上一个 TCP 连接上的并行内容，进行多路数据的传输，然而这中间并没有关联的数据。一前一后，前面 stream 2 的帧没有收到，后面 stream 1 的帧也会因此阻塞。” 请问这一段怎么理解？感觉和前面所述“http2.0的乱序传输支持”是不是有些矛盾？</div>2019-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b6/97/93e82345.jpg" width="30px"><span>陆培尔</span> 👍（2） 💬（4）<div>QUIC协议自定义了连接机制、重传机制和滑动窗口协议，感觉这些都是原来tcp干的活，那为啥QUIC是属于应用层协议而不是传输层呢？应该把QUIC协议加入内核的网络栈而不是做在chrome这样的用户态应用程序里面吧</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/82/a3ea8076.jpg" width="30px"><span>tim</span> 👍（2） 💬（1）<div>有个问题：
文中指出tcp采样不准确。 序列号可以发送一致的。

但是之前讲的序列号是根据时间来增长的，除非你过去非常长的时间，不然是不可能重复的。

这个问题不知是我理解序列号的增长策略有问题还是文中作者的推断有问题🤨</div>2018-10-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/LWicoUend7QOH6pyXGJyJicAzm5T4TUD8TaicSCHVPJp7sbIicpeArcicZiaMGcQ7uUDWjGZYgVnUqNGFFDVe9h0EV4w/132" width="30px"><span>Geek_f7658e</span> 👍（1） 💬（1）<div>刘老师，您好！请问steam是什么？一个在tcp上的应用层程序？</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/57/83f3a377.jpg" width="30px"><span>LiBloom</span> 👍（1） 💬（1）<div>请问：http协议有这么多 0.9、1、1.1、2、3 ，浏览器是怎么选择使用哪个协议跟服务器通信的呢？我看1.1开始有了协议协商，那1.1之前浏览器是有一个默认的协议吗？</div>2019-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/99/3873b659.jpg" width="30px"><span>Hulk</span> 👍（1） 💬（1）<div>你好，Accept-Charset是针对字符的编码？如果请求的是文件，那二进制的编码是？</div>2018-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/75/16/4dd77397.jpg" width="30px"><span>a</span> 👍（0） 💬（1）<div>关于post和put方法和我理解的完全不一样.老师说的put是修改数据,post是创建数据.但我一直理解的是post是修改局部数据,put是创建和修改幂等数据,难道我一直都理解错了?</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c1/0e/2b987d54.jpg" width="30px"><span>蜉蝣</span> 👍（0） 💬（1）<div>老师，如你所说：“而 QUIC 以一个 64 位的随机数作为 ID 来标识，即使 IP 或者端口发生变化，只要 ID 不变，就不需要重新建立连接。”

那我是不是可以认为，QUIC 的安全性比 TCP 低。</div>2019-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/0c/ada45f25.jpg" width="30px"><span>憎爱不关心</span> 👍（0） 💬（1）<div>看完这一篇 不敢看新闻了。。。</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（1）<div>如果要传输银行卡等敏感信息  使用TCP+SSL协议吗？</div>2019-06-05</li><br/><li><img src="" width="30px"><span>Geek_f6f02b</span> 👍（0） 💬（1）<div>HTTP 2.0 虽然大大增加了并发性，但还是有问题的。因为 HTTP 2.0 也是基于 TCP 协议的，TCP 协议在处理包时是有严格顺序的。当其中一个数据包遇到问题，TCP 连接需要等待这个包完成重传之后才能继续进行。这里指的严格顺序是否是因为受到接受方同时最多接受字节限制导致要顺序，也就是说在接受方限制字符内是无须顺序的，可以先发的后接收，后发的先接收，是吗？</div>2019-04-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJGOSxM1GIHX9Y2JIe7vGQ87rK8xpo5F03KmiaGyXeKnozZsicHeSZrbSlzUVhTOdDlXCkTrcYNIVJg/132" width="30px"><span>ferry</span> 👍（0） 💬（1）<div>我感觉QUIC是TCP和UDP长处的结合体，但是既然TCP协议下的数据也是流的形式，为什么TCP协议不采用offset的方式来标记数据，而要采用序号来标记呢？</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c0/2a/86ca523d.jpg" width="30px"><span>shaohsiung</span> 👍（0） 💬（2）<div>keepalive和pipeline有什么区别？</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4a/8a/c1069412.jpg" width="30px"><span>makermade</span> 👍（0） 💬（1）<div>超哥。服务器存在大量time_wait的连接，是网络问题，还是web应用问题？</div>2018-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b0/3a/b942f384.jpg" width="30px"><span>我那么圆</span> 👍（146） 💬（11）<div>http1.0的队首阻塞

对于同一个tcp连接，所有的http1.0请求放入队列中，只有前一个请求的响应收到了，然后才能发送下一个请求。

可见，http1.0的队首组塞发生在客户端。

3 http1.1的队首阻塞

对于同一个tcp连接，http1.1允许一次发送多个http1.1请求，也就是说，不必等前一个响应收到，就可以发送下一个请求，这样就解决了http1.0的客户端的队首阻塞。但是，http1.1规定，服务器端的响应的发送要根据请求被接收的顺序排队，也就是说，先接收到的请求的响应也要先发送。这样造成的问题是，如果最先收到的请求的处理时间长的话，响应生成也慢，就会阻塞已经生成了的响应的发送。也会造成队首阻塞。

可见，http1.1的队首阻塞发生在服务器端。

4 http2是怎样解决队首阻塞的

http2无论在客户端还是在服务器端都不需要排队，在同一个tcp连接上，有多个stream，由各个stream发送和接收http请求，各个steam相互独立，互不阻塞。

只要tcp没有人在用那么就可以发送已经生成的requst或者reponse的数据，在两端都不用等，从而彻底解决了http协议层面的队首阻塞问题。</div>2019-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7f/27/03007a5e.jpg" width="30px"><span>月饼</span> 👍（94） 💬（19）<div>既然quic这么牛逼了干嘛还要tcp？</div>2018-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/28/1e307312.jpg" width="30px"><span>鲍勃</span> 👍（41） 💬（13）<div>我是做底层的，传输层还是基本能hold住，现在有点扛不住了😂</div>2018-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/a1/43d83698.jpg" width="30px"><span>云学</span> 👍（35） 💬（2）<div>http2.0的多路复用和4g协议的多harq并发类似，quick的关键改进是把Ack的含义给提纯净了，表达的含义是收到了包，而不是tcp的＂期望包＂</div>2018-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/90/6828af58.jpg" width="30px"><span>偷代码的bug农</span> 👍（27） 💬（2）<div>一窍不通，云里雾里</div>2018-07-13</li><br/>
</ul>