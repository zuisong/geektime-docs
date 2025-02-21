你好，我是Chrono。

在[第26讲](https://time.geekbang.org/column/article/110354)里，我介绍了TLS 1.2的握手过程，在Client Hello和Server Hello里用到了ECDHE算法做密钥交换，参数完全公开，但却能够防止黑客攻击，算出只有通信双方才能知道的秘密Pre-Master。

这是TLS握手的关键步骤，也让很多同学不太理解，“为什么数据都是不保密的，但中间人却无法破解呢？”

解答这个问题必须要涉及密码学，我原本觉得有点太深了，不想展开细讲，但后来发现大家都对这个很关心，有点“打破砂锅问到底”的精神。所以，这次我就试着从底层来解释一下。不过你要有点心理准备，这不是那么好懂的。

先从ECDHE算法的名字说起。ECDHE就是“短暂-椭圆曲线-迪菲-赫尔曼”算法（ephemeral Elliptic Curve Diffie–Hellman），里面的关键字是“短暂”“椭圆曲线”和“迪菲-赫尔曼”，我先来讲“迪菲-赫尔曼”，也就是DH算法。

## 离散对数

DH算法是一种非对称加密算法，只能用于密钥交换，它的数学基础是“**离散对数**”（Discrete logarithm）。

那么，什么是离散对数呢？

上中学的时候我们都学过初等代数，知道指数和对数，指数就是幂运算，对数是指数的逆运算，是已知底数和真数（幂结果），反推出指数。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（12） 💬（2）<div>DH算法只能用于密钥的交换，没有原文、摘要这些参数，无法生成数字签名。</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（9） 💬（2）<div>回答一下思考题：我觉得原因是,根据DH算法的原理，只能算出一个新的值出来用于交换密钥，而数字签名是需要解密数字证书得到数字签名，从而判断数字证书是否真实有效。DH是基于现有数据算出一个新值，公钥私钥算出的结果并不相同，RSA是对数据进行加解密。</div>2019-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（2） 💬（1）<div>学习了，数学就是计算机的力量源泉。</div>2023-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/8b/9080f1fa.jpg" width="30px"><span>猫头鹰波波</span> 👍（2） 💬（1）<div>老师，为什么ECDHE更难破解么，是因为离散的点选取更具备随机性吗</div>2020-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8b/fa/90126961.jpg" width="30px"><span>fxs007</span> 👍（2） 💬（1）<div>刚才看了下RSA验证签名的过程(https:&#47;&#47;crypto.stackexchange.com&#47;questions&#47;12768&#47;why-hash-the-message-before-signing-it-with-rsa)，我觉得DH算法本身是可以用来验证数字签名。比如双方已经完成了DH秘钥交换过程，
签名方发送 text + DH-enc(sha256(text))，其中DH-enc(sha256(text))是对text进行hash算法然后DH加密
验证方 用DH-dec解密签名，然后和sha256(text)比较，相等就说明验证通过
只是DH一般用在双方确定身份以前，验证没有身份的签名并没有什么意义。</div>2020-02-08</li><br/><li><img src="" width="30px"><span>Geek_78044b</span> 👍（1） 💬（1）<div>老师你好，有个疑问。握手过程中的第三个参数，pre-master为何要用用那么复杂的算法去避免破解呢？

我的理解是，第三个随机数是通过服务端的公钥加密后传输的，传递到服务端后，用服务端的私钥才能解密出来这个随机数。

黑客没有服务端的私钥，完全不可能破解pre-master的啊，为何要那么复杂的加密算法去生成这个pre-master？？？</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/92/7a/0c2317ab.jpg" width="30px"><span>江湖骗子</span> 👍（0） 💬（1）<div>ECDHE握手中有4个数，ClientRandom，ServerRandom，ClientParam，ServerParam，分别对应DH算法中的P，G，A，B，请问老师我的理解对吗？但是DH中P和G不是要求为质数吗？</div>2023-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e7/20/70a95f94.jpg" width="30px"><span>潮汐</span> 👍（0） 💬（2）<div>老师好，二刷完成了，对课程内容有更深的学习！
这里的思考题，我的看法是，从非对称加密算法来说DH是可以对消息做签名的，只是在连接密钥交换阶段没有这个必要，另外DH算法的公私钥是一次一密，也是不符合数字签名中解签的公钥从证书获取保持不变的场景？</div>2023-02-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83errj9iaMOHaUFf2XkdkMFU7kNnOiarW6bU8yggOzkJj4ncoqHXiaFwc8nosCdeSvfdeMfBpoVibO724ow/132" width="30px"><span>Geek_91cf3b</span> 👍（0） 💬（1）<div>老师，PFS报文能解密码？</div>2022-07-12</li><br/><li><img src="" width="30px"><span>GeekCoder</span> 👍（0） 💬（1）<div>也就是说DH算法中，也是有私钥的(私密部分)，而外部并不知道私钥。</div>2022-05-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIuTjCibv0afd7SSdLicfNk0f7KO5ga9VMleD1hc2DtQfianK20ht06SekClKV7M8UXLRHqQLm9hJ3ow/132" width="30px"><span>Jasmine</span> 👍（0） 💬（1）<div>老师，等式B ^ a = (G ^ b ) ^ a = (G ^ a) ^ b = A ^ b左右两边就算忽略mod17值也不相等啊，为什么说经过运算都等于8呢？实际应用计算的底数超级大，给定了算法，数字运算的结果还是固定的呀，哪怕差0.00001那pre-master也不相同啊。困惑ing</div>2021-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/5e/40/dee7906c.jpg" width="30px"><span>张欣</span> 👍（0） 💬（2）<div>老师，不知道我理解的对不对：
根据文中以及之前tls文章的讲解，DH算法的主要目的就生成不可逆操作的公钥和私钥，然后再次执行算法生成两端相同的pre-master。这里面生成的公钥和私钥是可以拿来再次对文件摘要进行签名和验证，但是DH算法本身并没有这个作用。假设参数可以是文件摘要，就算算法能够算出，之后拿到证书的人也破解不开，根本没有意义。</div>2021-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/2b/b32f1d66.jpg" width="30px"><span>Ball</span> 👍（0） 💬（1）<div>原理完全没看懂，得花点时间消化一下了。</div>2021-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/32/75/abbc6810.jpg" width="30px"><span>久念</span> 👍（0） 💬（1）<div>老师好，”国家级别的计算能力是有可能算出私钥的“ -- 如果私钥是可以被算出来的，那 Root CA 对应的私钥也有可能被破解，这样的话 黑客是不是就可以随意的颁发证书</div>2020-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（0） 💬（1）<div>因为DH算法，由公钥反向计算私钥是非常难的。</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/43/1aa8708a.jpg" width="30px"><span>子杨</span> 👍（0） 💬（1）<div>对证书这块还是有点晕。证书应该只是用来证明站点的身份的吧？使用证书颁发机构的公钥对证书中的 hash 值进行解密，同时对 data 做 hash，如果相等就说明身份可信。</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/44/d3d67640.jpg" width="30px"><span>Hills录</span> 👍（0） 💬（2）<div>DHE不能用于数字签名，是因为无法使用公钥验证私钥有效性</div>2020-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e5/ac/6c87d5ee.jpg" width="30px"><span>mark</span> 👍（0） 💬（1）<div>DH算法是选择一个数字作为私钥，hash好像不可逆，如果类似hash这样的算法，生成一个整数，是不是就可以用DH算法加密文本了。</div>2019-10-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erbY9UsqHZhhVoI69yXNibBBg0TRdUVsKLMg2UZ1R3NJxXdMicqceI5yhdKZ5Ad6CJYO0XpFHlJzIYQ/132" width="30px"><span>饭团</span> 👍（0） 💬（3）<div>老师问题是不是是因为DH算法是动态的！即2个参数是相辅相成的，而数字签名中，公钥是不变的！</div>2019-10-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erbY9UsqHZhhVoI69yXNibBBg0TRdUVsKLMg2UZ1R3NJxXdMicqceI5yhdKZ5Ad6CJYO0XpFHlJzIYQ/132" width="30px"><span>饭团</span> 👍（0） 💬（2）<div>真棒老师，估计好多同学都不知道您更新了！谢谢您了！</div>2019-10-11</li><br/>
</ul>