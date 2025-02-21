你好，我是Chrono。

今天我要与你分享的话题是“海纳百川：HTTP的实体数据”。

这一讲是“进阶篇”的第一讲，从今天开始，我会用连续的8讲的篇幅来详细解析HTTP协议里的各种头字段，包括定义、功能、使用方式、注意事项等等。学完了这些课程，你就可以完全掌握HTTP协议。

在前面的“基础篇”里我们了解了HTTP报文的结构，知道一个HTTP报文是由“header+body”组成的。但那时我们主要研究的是header，没有涉及到body。所以，“进阶篇”的第一讲就从HTTP的body谈起。

## 数据类型与编码

在TCP/IP协议栈里，传输数据基本上都是“header+body”的格式。但TCP、UDP因为是传输层的协议，它们不会关心body数据是什么，只要把数据发送到对方就算是完成了任务。

而HTTP协议则不同，它是应用层的协议，数据到达之后工作只能说是完成了一半，还必须要告诉上层应用这是什么数据才行，否则上层应用就会“不知所措”。

你可以设想一下，假如HTTP没有告知数据类型的功能，服务器把“一大坨”数据发给了浏览器，浏览器看到的是一个“黑盒子”，这时候该怎么办呢？

当然，它可以“猜”。因为很多数据都是有固定格式的，所以通过检查数据的前几个字节也许就能知道这是个GIF图片、或者是个MP3音乐文件，但这种方式无疑十分低效，而且有很大几率会检查不出来文件类型。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/11/26838646.jpg" width="30px"><span>彧豪</span> 👍（99） 💬（2）<div>上周五和服务端做上传图片的时候遇到过这个content-type的问题，上传图片时候我这边需要设置content-type:&quot;image&#47;jpg&quot;，然后传完了，我在预览的时候获取图片的地址，此时比如通过a标签的方式打开新标签预览该图片时才能成功预览，不然如果使用上传的js-sdk设置的默认类型：content-type:&quot;octet-stream&quot;，那么浏览器就不认识这个图片了，转而会下载这个文件(图片)，所以我是不是可以理解为content-type这字段在请求头，和响应头里都能使用？或者上传文件这个业务又不同于一般的请求操作呢？</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/c8/980776fc.jpg" width="30px"><span>走马</span> 👍（41） 💬（4）<div>accept 表达的是你想要的
而你发送 post请求时，你发送的数据是给服务器的，这时候就需要像 服务器会用 content-type 标明它给你的数据类型一样，你也需要用 content- 来表明你给别人的数据的一些属性</div>2019-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/78/2828195b.jpg" width="30px"><span>隰有荷</span> 👍（37） 💬（1）<div>用post方法请求接口时，在客户端语言的设置上不能使用Accept-Language吗？为什么一定是Contenr-Language呢？是不是Accept-Language只用于get方式时，表明客户端需要的的语言呢？</div>2019-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/05/06/f5979d65.jpg" width="30px"><span>亚洲舞王.尼古拉斯赵四</span> 👍（37） 💬（6）<div>1.含义是：我这个请求最希望服务器给我返回的编码方式是gzip和deflate，他们俩在我这是最优的地位，我不接受br的编码方式，如果还有其他的编码方式的话对我来说权重0.5。服务器可能的响应头是
HTTP&#47;1.1 200 OK
Content-Encoding: gzip

2.请求头可能是
POST &#47;serv&#47;v1&#47;user&#47;auth HTTP&#47;1.1
Content-Type: application&#47;json
Accept-Language: zh-CN, zh
Accept-Charset: gbk, utf-8
3.MIME类比快递的话就是你要快递的物品（衣服，食物等），Encoding就是快递你这个物品的包装方式，如果是衣服可能就随意一点一个袋子，如果是食物担心腐烂给你放个冰袋进去
不知道回答的对不对，请老师指正</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（28） 💬（2）<div>现在很多小文件 比如图片 都往云存上放了 千万指定正确content-type 一旦指定错 批量修改太麻烦 而且会影响终端的解析</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/99/5d603697.jpg" width="30px"><span>MJ</span> 👍（24） 💬（1）<div>老师，每一个并发连接，都需要新建tcp三次握手吗？还是一次tcp握手后，可以并发多个连接？</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/df/6e/267bd6ee.jpg" width="30px"><span>1900</span> 👍（20） 💬（1）<div>“所以后来就出现了 Unicode 和 UTF-8，把世界上所有的语言都容纳在一种编码方案里，UTF-8 也成为了互联网上的标准字符集。”

这句话最后有点问题吧？Unicode才是字符集，应该是“遵循UTF-8字符编码方式的Unicode字符集也成为了互联网上的标准字符集”，是么？</div>2019-07-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTImeO3D5b56u2oHuQ13e58OmLexGVjYt6NTn1W4XjALJUrx7vh0FE2OVZvpxiczt8SibZM6TTFp2ASA/132" width="30px"><span>BellenHsin</span> 👍（12） 💬（2）<div>这篇写的不错</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fc/d7/b102034a.jpg" width="30px"><span>do it</span> 👍（9） 💬（1）<div>1、试着解释一下这个请求头“Accept-Encoding: gzip, deflate;q=1.0, *;q=0.5, br;q=0”，再模拟一下服务器的响应头。
  ：最好使用gzip,deflate压缩格式，我不接受br压缩，如果都没有的话就选择其他格式

2、假设你要使用 POST 方法向服务器提交一些 JSON 格式的数据，里面包含有中文，请求头应该是什么样子的呢？
      content-type: application&#47;json, charset=gbk
      content-language:zh-cn, zh

3、试着用快递发货收货比喻一下 MIME、Encoding 等概念。
     物品的种类（水果、衣服）就是MIME，包装方式就是Encoding</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（5） 💬（1）<div>做web开发有两个问题，估计许多人都遇到过，一个是乱码问题，这个是字符集设置不一致导致的具体哪里设置的不一致通常需要观察所有需要数据转换的地方，一般是客户端和服务器端不一致了。另外，就是文件上传，这个格式一定要设置对，否则就会感到莫名其妙。
我想请教老师两个问题：
1：看到说浏览器最多会有六个连接并发执行，为什么是六个，不会是因为六六大顺吧？
2：文件上传的速度和文件的大小密切相关，文件上传的大小限制都是有哪些限制或控制？之前，这是老早了，发现有些框架默认只能是2g</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（5） 💬（1）<div>老师好!有个问题,之前遇到过一个发送ajax请求。前端忘记在content-type里面指定，application&#47;json。后端接受数据失败。具体表现不太记得了好像都是null。后来前端加了content-type就好了。accept比较好理解就是发起请求放想要接受的内容。content-type是服务器，是响应类型的话。客户端在发送请求时压根就不知道啊，也不应该由客户端来设置。
所以我想问的是，accept相关的都是请求头里面的数据
content-type相关的都是响应头里的数据么?
至于我前面正确的写法应该是在accept里面设置json类型。错写了content-type。框架做了兼容处理(在服务端看起来content-type起作用了)?
谢谢老师</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（4） 💬（1）<div>老师好!那accept是不是有两个语意
1.客户端希望接受(支持)的数据类型
2.我发送的数据就是这个类型的。请用这些方式解析?
问题:accept指定text。实际传的数据是一个json这样的后台会用text解析。然后拿不到数据是么?在请求头里加content -type这些字段会起作用么?</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/0b/73628618.jpg" width="30px"><span>兔嘟嘟</span> 👍（3） 💬（2）<div>罗老师，我不是很能理解accept-language这类字段的意义，因为我们开发前后端肯定是有一套接口文档的，里面约定了各种开发细节，前后端应该使用什么编码什么语言，为何还要在报文里去提accept-language？
总不能前端写好了，发送一个报文给后端，后端程序员慢慢看里面的字段，再开始后端的编程吧？</div>2021-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c7/5f/2028aae5.jpg" width="30px"><span>搏未来</span> 👍（3） 💬（1）<div>Accept表示客户端能接受什么，Content-*表示提供的具体信息，由于客户端与服务端都可以提供信息，所以Content-*是可以在两端都可以用的。</div>2021-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/18/b3/848ffa10.jpg" width="30px"><span>Jinlee</span> 👍（3） 💬（2）<div>1. 含义：服务器，你返回的数据编码方式最好是gzip或者deflate，实在不行返回其他的编码方式也行，但是，我不接受br类型的数据编码方式

模拟服务器响应头：
HTTP&#47;1.1 200 OK
Content-Encoding: gzip 

2. 请求头：
POST &#47; HTTP&#47;1.1
Content-type:text&#47;json; chartset=GBK, utf-8

3. 收发快递比喻：
MIME type就是要发收的具体物品，如文件、生鲜、衣物等。Encoding就是快递的包装方式，如果是文件呢，那我就用专用文件袋给你寄过去；如果是生鲜，那我就给你套个保鲜泡沫寄过去；如果是衣物，那我就给你个一般的快递包装寄过去。

参考其他优秀同学的答案😬

</div>2020-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/44/a7/171c1e86.jpg" width="30px"><span>啦啦啦</span> 👍（3） 💬（1）<div>不错不错，靠谱这篇，天天看这些参数一直不知道具体意思，今天老师讲了以后理解了</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/94/82/d0a417ba.jpg" width="30px"><span>蓝配鸡</span> 👍（2） 💬（1）<div>试着解释一下这个请求头“Accept-Encoding: gzip, deflate;q=1.0, *;q=0.5, br;q=0”，再模拟一下服务器的响应头。
我希望用GZIP或者deflate压缩算法，实在不行给我其他的算法也行，但千万别给我br压缩过的数据，我这边可不会这个算法！

假设你要使用 POST 方法向服务器提交一些 JSON 格式的数据，里面包含有中文，请求头应该是什么样子的呢？
content-type: zh-CN, zh, charset=utf-8, application&#47;json

试着用快递发货收货比喻一下 MIME、Encoding 等概念。
比如说我想在某宝上买乐高，
MIME 确定了我购买的乐高种类，是成品呢， 还是零散的需要自己拼装。
Encoding好比这个乐高的包装方式，某宝可以选择把所有的乐高零件全都放在一个包装里， 也可以分模块把零件放在不同的包装里。 我也可以主动告诉某宝我想要哪一种包装方式。</div>2019-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/62/05/30ae6faf.jpg" width="30px"><span>aNught</span> 👍（2） 💬（1）<div>老师，您好，如果我accep-encoding填写了gzip，那服务端发来的报文是是gzip压缩过的吗，我需要解压才行是吗？</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（2） 💬（1）<div>content-type 千万不能填错 否则其他终端解析会存在问题</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（2） 💬（1）<div>1.服务器优先按照gzip和deflate压缩，否则用其他压缩算法，但是不用brotli算法</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fa/5d/735fdc76.jpg" width="30px"><span>╭(╯ε╰)╮</span> 👍（1） 💬（1）<div>我有6个问题

1 新版的http协议支持服务器向客户端推送消息，是吗，这样的话，如果客户端不支持Conyent-头里给的类型，有什么方式或机制告知服务端呢，难不成紧跟着再回发一个请求带上Accept-吗？

2 http是无状态的 是不是意味着正经的做法，每次请求，客户端都要带上Accept-,服务器不能缓存并根据客户端之前请求的Accept-来返回Content-?如果服务器做选择时的算法没做好，意味着这是一个潜在的性能瓶颈？

3 客户端里要是无脑把市面上已知的所有类型都带到Accept-里，服务器从这么多类型里选择，会不会浪费计算资源，甚至没实现好的话，会造成ddos攻击

4 html里的&lt;head lang=&gt;&lt;meta charset=&gt;标签和http头里的Content-是怎么协作的，他俩冲突时客户端应该怎么处理？

5 世面上的服务器做选择的时候普遍做法是什么，有一套约定俗称的方法吗，还是各自实现？比如nginx,spring-mvc,python -m http.server他们分别怎么实现的，有文档吗？

6 国内总是有一些骗子公司，把chrome浏览器打个zip压缩包来骗国家科研经费说是独立自主研发的。我很愤慨，想自己从玩具开始从零实现一个浏览器，有借鉴的手册或项目吗，难道是啃rfc？操作系统这方面感觉就很多，我所知道的有LFS项目，很多大牛根据linux早期版本的魔改，甚至极客时间也有专栏《操作系统实战45讲》</div>2022-12-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erwIgbTd3oy4GzkdCUBmz8lHGIIWBwoSIfibgQzwDlQuvTrLlqwTh7p99NBJIsu98ziaYoroQCSENwA/132" width="30px"><span>Celine</span> 👍（1） 💬（2）<div>1，接收的编码格式最好是GUN zip 和deflate ,不接受br,如果还有其他格式。我勉为其难也接受一下吧，权重是0.5；http响应头应该是  Http 1.1 200 Ok  Conten-Encoding: gzip
2,Content-Type:Application&#47;json
   Content-Language: cn-zh
   Content-charset: gbk, utf-8

    
   </div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9d/9a/4cf0e500.jpg" width="30px"><span>芒果</span> 👍（1） 💬（1）<div>给老师点赞，大牛就是大牛</div>2020-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/26/7e/823c083e.jpg" width="30px"><span>Wr</span> 👍（1） 💬（1）<div>1. 客户端最想接受的编码格式是gzip，deflate，权重是1，不接受br格式，如果还有其他格式，权重是0.5
2. accept-chartset：utf-8，
    accept-langue：zh-cn，
3. mime可以看作快递物品的类型，encoding可以看作打包物品的方法</div>2020-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/94/82/d0a417ba.jpg" width="30px"><span>蓝配鸡</span> 👍（1） 💬（1）<div>有个问题：
浏览器是依据什么来设置 accept 头字段的呢？还是说浏览器只是把所有可以accept的类型列出来？</div>2019-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/24/5d/65e61dcb.jpg" width="30px"><span>学无涯</span> 👍（1） 💬（1）<div>老师，是否可以这样理解：
get请求下，请求使用Accept-*字段，响应使用Content-*；post的话，请求相应就都需要用Content-*字段</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/44/a7/171c1e86.jpg" width="30px"><span>啦啦啦</span> 👍（1） 💬（1）<div>二刷</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/22/89/73397ccb.jpg" width="30px"><span>响雨</span> 👍（1） 💬（2）<div>Content-type: application&#47;json; charset=utf-8
Accept-language: zh-CN
python中的requests模块发送url请求，post时一定要在header中加上Content-type，不然会报错。
老师，我在mime中放了1G的MP4视频，为什么只有声音没有画面啊。
</div>2019-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/31/7e/ce1cf9b2.jpg" width="30px"><span>聂成阳</span> 👍（1） 💬（2）<div>老师，我访问极客时间https:&#47;&#47;account.geekbang.org&#47;dashboard&#47;user它的请求头是这样的：
POST &#47;account&#47;user HTTP&#47;1.1
Host: account.geekbang.org
Connection: keep-alive
Content-Length: 2
Accept: application&#47;json, text&#47;plain, *&#47;*
Origin: https:&#47;&#47;account.geekbang.org
User-Agent: Mozilla&#47;5.0 (Windows NT 10.0; Win64; x64) AppleWebKit&#47;537.36 (KHTML, like Gecko) Chrome&#47;75.0.3770.100 Safari&#47;537.36
Content-Type: application&#47;json
Referer: https:&#47;&#47;account.geekbang.org&#47;dashboard&#47;buy
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
为啥post也使用accept-*呢？</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/44/a7/171c1e86.jpg" width="30px"><span>啦啦啦</span> 👍（1） 💬（1）<div>今天凌晨买的课程，然后现在一口气看完了</div>2019-07-02</li><br/>
</ul>