浏览器安全主要划分为三大块内容：页面安全、系统安全和网络安全。前面我们用四篇文章介绍了页面安全和系统安全，也聊了浏览器和Web开发者是如何应对各种类型的攻击，本文是我们专栏的最后一篇，我们就接着来聊聊网络安全协议HTTPS。

我们先从HTTP的明文传输的特性讲起，在上一个模块的三篇文章中我们分析过，起初设计HTTP协议的目的很单纯，就是为了传输超文本文件，那时候也没有太强的加密传输的数据需求，所以HTTP一直保持着明文传输数据的特征。但这样的话，在传输过程中的每一个环节，数据都有可能被窃取或者篡改，这也意味着你和服务器之间还可能有个中间人，你们在通信过程中的一切内容都在中间人的掌握中，如下图：

![](https://static001.geekbang.org/resource/image/11/e2/118ced11537bd1e257f8df09380f33e2.png?wh=1142%2A508)

中间人攻击

从上图可以看出，我们使用HTTP传输的内容很容易被中间人窃取、伪造和篡改，通常我们把这种攻击方式称为**中间人攻击**。

具体来讲，在将HTTP数据提交给TCP层之后，数据会经过用户电脑、WiFi路由器、运营商和目标服务器，在这中间的每个环节中，数据都有可能被窃取或篡改。比如用户电脑被黑客安装了恶意软件，那么恶意软件就能抓取和篡改所发出的HTTP请求的内容。或者用户一不小心连接上了WiFi钓鱼路由器，那么数据也都能被黑客抓取或篡改。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/1e/71/54ff7b4e.jpg" width="30px"><span>3Spiders</span> 👍（163） 💬（14）<div>我有一个地方不是很理解。CA的公钥，浏览器是怎么拿到的。是浏览器第一次请求服务器的时候，CA机构给浏览器的吗？求大神或者老师解答</div>2019-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（76） 💬（9）<div>1. 首先是tcp的三次握手建立连接
2. client发送random1+支持的加密算法集合（clientHello）
3. server收到信息，返回选择一个加密算法+random2（serverHello）+ 证书+ 确认
4. clent验证证书有效性，并用random1+random2生成pre-master通过服务器公钥加密 发送给server
5. server收到premaster，根据约定的加密算法对random1+random2+premaster（解密）生成master-secret，然后发送预定成功
6. client收到生成同样的master-secert，对称加密秘钥传输完毕

今日总结
浏览器安全主要包括页面安全、系统安全、传输安全三个部分。https主要保证传输过程的安全，从防止中间人窃取修改伪造的角度循序渐进的介绍了https的实现过程。 
1. 对称加密传输（协商秘钥的过程容易被窃取）
2. 非对称加密传输（服务端用私钥加密的内容，可以通过它的公钥进行解密）
3. 非对称加密交换秘钥、对称加密传输内容（DNS劫持 如何保证服务器是可信的）
4. 引入CA权威机构保证服务器可信性。
数字证书的申请过程：服务器生成一对公钥和私钥，私钥自己保存，通过公钥+企业+网站信息去CA机构申请证书。CA机构通过全方位的验证给这个网站颁发证书，证书内容包括企业信息、证书有效期、证书编号，以及自己私钥加密上述信息的摘要、网站的公钥。服务器就获得了CA的认证。
浏览器认证证书过程：浏览器从服务器拿到网站的证书，通过CA的公钥解密证书信息的摘要跟使用摘要算法计算企业信息等的摘要对比，如果一致则证明证书有效。如果证书CA是可靠的呢，通过给CA颁发证书的根CA验证，通常操作系统中包括顶级CA证书（它们自己给自己签名称为自签名证书，我们自己生成证书也是自签名证书 只是它不是操作系统内置的）</div>2019-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0b/2f/6efc3051.jpg" width="30px"><span>GY</span> 👍（34） 💬（2）<div>问了很多次，一直没有回复，想请问下老师，专栏中一直说的主线程和渲染引擎线程、js引擎线程之间有什么关系，渲染引擎和js引擎互斥，两个引擎是都运行在主线程中吗，这个主线程到底是什么啊？</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/94/82/d0a417ba.jpg" width="30px"><span>蓝配鸡</span> 👍（26） 💬（1）<div>HTTPS握手过程：
1. 建立TCP链接
2. 获取服务器证书并检查证实真实性
3. 通过证书里服务器的公钥发送自己的公钥以及协商对称加密需要的信息给服务器. 
4. 服务器返回协商结果
5. 双方生成对称密钥
6. 开始通信

第二步证明了服务器就是服务器， 其实已经可以愉快的沟通了（通过非对称加密）， 后面交换对称加密信息的步骤其实可以算是优化吧？ 我记得是TLS1.2才引入的？ 

有个问题：
根证书是信任的根源， 老师说它是被系统内核管理的并且自签名，那如果系统内核被黑了岂不是黑客就可以作假了？ 根证书是不是就是一个躺在内核中（用户无法访问到）的文件？ 有没有什么机制或者技术去发现根证书是假的？ 还是说等到用户出现损失之后系统级别的更新来去除对这个根CA的信任？


给李兵老师：
不知不觉最后一节了， 本人由于工作原因对前端以及chrome需要加深理解。 老师的专栏每天上下班的时候都会听，反复的听。
不管是内容，还是文字结构梳理，都不难发现老师花了大量的精力和时间去思考如何讲透某一个知识点。 
老师对知识的颗粒度把握的很好， 既不是泛泛而谈， 又不会太细以至于难以理解。 使得我对前端，以及chrome产生了浓厚的兴趣！ 虽然现在整个前端， 或者chrome浏览器对我来说可能还是打着码的， 但相比之前， 我相信我已经看到一个大致的轮廓了， 今后一定会更花时间在前端领域中， 把这些码去掉，成为前端大神！ 
表达能力可能有限...总而言之， 谢谢老师🙏！虽然这是最后一篇了， 但是如果老师想做几篇加餐，我想同学们也是很欢迎的 😂
</div>2019-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1e/71/54ff7b4e.jpg" width="30px"><span>3Spiders</span> 👍（12） 💬（1）<div>这篇文章是我看过最好的https总结的文章，拆解很到位。</div>2019-10-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/7WkTI1IicbKvsPJng5vQh5qlrf1smbfl2zb7icHZfzcAk1k4lr8w8IDEAdrqq1NHW5XZMPXiaa1h7Jn1LGOWOCkIA/132" width="30px"><span>早起不吃虫</span> 👍（9） 💬（4）<div>老师好，您前面说随机数加密算法是公开透明的，后面又说利用 client-random 和 service-random 计算出来 pre-master，然后利用公钥对 pre-master 加密，并向服务器发送加密后的数据，。   。这样的话，premaster不是也是可以计算出来了吗，有必要用公钥加密吗？</div>2019-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/1f/f7be5246.jpg" width="30px"><span>大前端洞见</span> 👍（8） 💬（3）<div>&gt;虽然浏览器端可以使用公钥来加密，但是服务器端只能采用私钥来加密，私钥加密只有公钥能解密，但黑客也是可以获取得到公钥的，这样就不能保证服务器端数据的安全了。

老师，这里不是很明白。浏览器使用公钥加密，服务器端不是用私钥解密吗？怎么你这里说“服务器端只能采用私钥来加密”呢？</div>2019-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b9/5e/a8f6f7db.jpg" width="30px"><span>Ming</span> 👍（5） 💬（1）<div>请问老师：

（1）非对称加密部分，当浏览器的公钥给了服务器，服务器不就可以给浏览器安全传输数据了吗？
（2）混合加密部分，“浏览器保存公钥，并利用 client-random 和 service-random 计算出来 pre-master”，经揣摩，pre-master是生成对称加密密钥的重要且唯一安全的参数，但是在浏览器端，计算出来的pre-master是安全的吗？因为考虑到client-random 和 service-random是可以被拦截的，是否pre-master可以在传输前就被知晓了？
（3）混合加密方式有个漏洞，这种情况是服务器向浏览器发送公钥过程中被伪装篡改，导致浏览器不是与真正的“对话人”即服务器进行对话，因而出现了数字证书对公钥的身份进行公证。</div>2019-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/bb/5e5c37c1.jpg" width="30px"><span>Angus</span> 👍（2） 💬（1）<div>这是我在极客时间认真看完并总结的第一篇专栏，并且在最后将自己的网站升级了HTTPS。整体来说受益匪浅，后续还会反复查阅的，感谢！</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/65/4d/92b6a180.jpg" width="30px"><span>填</span> 👍（2） 💬（1）<div>期待大佬以后有机会继续发布这么高质量的系列，很感谢这段时间的输出</div>2019-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5e/05/0d8a5b8e.jpg" width="30px"><span>郝仁杰</span> 👍（1） 💬（4）<div>老师您好：

浏览器单向认证可以验证服务证书是否为CA所颁发，但如何验证是访问的URL是对应的服务下发的？如果有中间代理劫持，如何判别和预防？</div>2019-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3b/71/b7094a80.jpg" width="30px"><span>Sunsmile</span> 👍（0） 💬（1）<div>感谢，全都是精华</div>2019-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ed/d1/7f9e8ec7.jpg" width="30px"><span>Tourbillon</span> 👍（0） 💬（1）<div>非常感谢李斌老师的答疑解惑，收获很多，给力！！！</div>2019-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b9/0d/ae745ec0.jpg" width="30px"><span>刹那</span> 👍（0） 💬（1）<div>谢谢老师这么精彩的系列，超棒。
我这里还有一个疑问，之前自己琢磨的时候，记得是对称加密这一步中。是这么理解的。
1、客户端用自己的对称密钥A，并告诉服务端，服务端接收到客户端的数据时用这个A解密。
2、服务端用另一个对称密钥B，并告诉客户端，客户端接收到的数据用这对称密钥B解密。
仔细想想又觉得这样子没必要，不存在更安全的说法，是不是我理解错了</div>2019-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/80/88/6601b81a.jpg" width="30px"><span>(-o-)／</span> 👍（0） 💬（1）<div>感谢</div>2019-10-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJS0jwYKhjm1hq96go05J4R7XDd5FFXXaoyIfX9TgoI3mLURAu2ET72SvYGM2iaET7IV3WDvMibAVfw/132" width="30px"><span>tokey</span> 👍（0） 💬（1）<div>老师加餐环节还是在这个专栏下么？后续还会有其他课程安排么</div>2019-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/af/b3/3486dea2.jpg" width="30px"><span>gigot</span> 👍（10） 💬（4）<div>感谢老师的干货输出，终于看完了，收获非常大。
看到很多同学对 client-random 和 service-random 生成 pre-master 比较迷惑，这里交换信息采用的是 ECDHE 算法，其实是浏览器生成了一对非对称秘钥，其中私钥c，公钥即 client-random 发给服务器；而服务器也同理生成非对称秘钥，其中私钥s，公钥即 service-random 发给浏览器。然后根据离散对数和椭圆曲线的数学基础，可以得出 pre-Master = f(c, service-random, client-random) = f(s, service-random, client-random)。即根据不同私钥得出相同的秘钥。而离散对数是非常难逆推破解的（计算量非常大），而形成保密</div>2019-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/c7/02/8346ebf6.jpg" width="30px"><span>Chris</span> 👍（6） 💬（1）<div>老师，
为什么要在ssl四次建立连接步骤中，生成三次随机数，我觉得最后一次的用服务器公钥加密的随机数pre-master就可以保证安全了啊。</div>2020-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ad/d9/6b4c397b.jpg" width="30px"><span>长草</span> 👍（4） 💬（1）<div>老师你好，原文中“首先浏览器读取证书中相关的明文信息，采用 CA 签名时相同的 Hash 函数来计算并得到信息摘要 A”，请问浏览器如何知道 CA 所用的是何种 HASH 函数。</div>2020-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/8c/ce36a2d0.jpg" width="30px"><span>爱看书的蜗牛</span> 👍（3） 💬（3）<div>数字证书解决了DNS劫持的问题吗？并没有啊</div>2020-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c7/cc/fc9232f6.jpg" width="30px"><span>影相随</span> 👍（2） 💬（3）<div>我有一个疑问，就是数字证书虽然不可以伪造，但是可不可以被劫持，比如中间人劫持了服务器返回的数字证书，然后把劫持到数字证书返回给浏览器，那浏览器拿到的数字证书依然可以验证通过呢？</div>2021-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/39/08/09055b47.jpg" width="30px"><span>淡</span> 👍（2） 💬（8）<div>今天又读了两遍，收获很多，同时又产生了3个疑问：
1.“浏览器如何验证证书”这一节中提到“然后再利用对应 CA 的公钥解密签名数据，得到信息摘要 B”，这一步中CA的公钥怎么拿到的？我理解的浏览器收到的数字证书包含的公钥是服务器的公钥，这里公钥是不是要在验证过证书合法后才能得到CA的公钥？
2.文章说验证数字证书的CA是否合法的时候，当前的数字证书包含了完整的CA链？如果没有，当CA是个层级比较低的CA的时候（假设中间有3层），怎么判断中间CA是否是合法的？
3.“通常情况下，操作系统中会内置信任的顶级 CA 的证书信息（包含公钥），如果这个 CA 链中没有找到浏览器内置的顶级的 CA，证书也会被判定非法”，请问这里是操作系统内置证书还是浏览器内置证书？</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/a1/7d/64ed0fdd.jpg" width="30px"><span>电单车</span> 👍（1） 💬（0）<div>过年花了好几天时间一口气看完了，简直停不下来，写的真好，感谢</div>2022-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/e7/d9/e426b92c.jpg" width="30px"><span>xxh</span> 👍（0） 💬（1）<div>从技术上来说CA证书是完全可以被伪造的</div>2023-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/ce/ae/97261da0.jpg" width="30px"><span>hpw123</span> 👍（0） 💬（0）<div>不懂就问，非对称加密既然是用公钥加密的，那服务端传给浏览器的加密套件有什么用呢</div>2022-07-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erXRaa98A3zjLDkOibUJV1254aQ4EYFTbSLJuEvD0nXicMNA8pLoxOfHf5kPTbGLXNicg8CPFH3Tn0mA/132" width="30px"><span>Geek_115bc8</span> 👍（0） 💬（1）<div>首先 CA 使用 Hash 函数来计算极客时间提交的明文信息，并得出信息摘要；然后 CA 再使用它的私钥对信息摘要进行加密，加密后的密文就是 CA 颁给极客时间的数字签名。

这个数字签名。这个CA使用《谁的》私钥啊？？？？</div>2022-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/b5/6c/18c5b2ed.jpg" width="30px"><span>一七</span> 👍（0） 💬（0）<div>浏览器也需要向服务器证明自己的身份吧</div>2022-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/d3/df/34fd4ebf.jpg" width="30px"><span>维他命</span> 👍（0） 💬（0）<div>有一个地方有点疑惑，就是第二版只使用非对称加密的方式进行通信，文中提到这种方式的弊端的第二点是无法保证服务器发送给浏览器的数据安全，黑客虽然可以获取公钥，从而对服务器发送给浏览器的数据进行截取并解密，但是没办法进行篡改，因为黑客并没有服务器的私钥，那么为什么说无法保证服务器发送给浏览器的数据安全呢，仅仅是因为可能被窃听？</div>2022-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/be/71/b9da2c1a.jpg" width="30px"><span>alone</span> 👍（0） 💬（0）<div>Https = http + 加密 + 证书 + 完整性保护。完整性保护是不是没有讲(数据摘要)</div>2022-03-08</li><br/>
</ul>