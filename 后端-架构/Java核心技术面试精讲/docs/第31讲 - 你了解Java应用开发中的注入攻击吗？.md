安全是软件开发领域永远的主题之一，随着新技术浪潮的兴起，安全的重要性愈发凸显出来，对于金融等行业，甚至可以说安全是企业的生命线。不论是移动设备、普通PC、小型机，还是大规模分布式系统，以及各种主流操作系统，Java作为软件开发的基础平台之一，可以说是无处不在，自然也就成为安全攻击的首要目标之一。

今天我要问你的问题是，你了解Java应用开发中的注入攻击吗？

## 典型回答

注入式（Inject）攻击是一类非常常见的攻击方式，其基本特征是程序允许攻击者将不可信的动态内容注入到程序中，并将其执行，这就可能完全改变最初预计的执行过程，产生恶意效果。

下面是几种主要的注入式攻击途径，原则上提供动态执行能力的语言特性，都需要提防发生注入攻击的可能。

首先，就是最常见的SQL注入攻击。一个典型的场景就是Web系统的用户登录功能，根据用户输入的用户名和密码，我们需要去后端数据库核实信息。

假设应用逻辑是，后端程序利用界面输入动态生成类似下面的SQL，然后让JDBC执行。

```
Select * from use_info where username = “input_usr_name” and password = “input_pwd”
```

但是，如果我输入的input\_pwd是类似下面的文本，

```
“ or “”=”
```

那么，拼接出的SQL字符串就变成了下面的条件，OR的存在导致输入什么名字都是复合条件的。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="" width="30px"><span>羊羊羊</span> 👍（19） 💬（1）<div>也不是很懂，根据自己的理解讲一下，部分可能是错误的。中间人攻击原理大概是用户在正常上网的时候，同网段的恶意用户对其进行欺骗。恶意用户向局域网广播:我是路由器，然后正常用户(电脑无防御)收到以后认为恶意用户就是路由器，然后向恶意用户发送数据包，恶意用户可以截获数据包，再向路由器发送正常用户的数据包，路由器将返回的数据包在给恶意用户，恶意用户在给正常用户，恶意用户就形成了中间人的效果，可以向返回的数据包注入html代码，达到劫持用户网站的效果，不过现在大部分的网站都是https且双向认证，比较难获取到用户发送数据包中的账号密码。</div>2018-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（12） 💬（1）<div>每次使用开源组件，经常关注使用版本修复的问题列表，其中的安全修复值得重点关注</div>2019-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/78/54005251.jpg" width="30px"><span>鸡肉饭饭</span> 👍（8） 💬（3）<div>杨老师，您好，被一个安全问题困扰许久。就是开发者是否能够通过一定的手段修改jdk中的String类，并将修改后的String类进行替换，对于这个问题，应当从哪里开始寻找答案？谢谢</div>2018-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/14/40/a6306dd3.jpg" width="30px"><span>王建</span> 👍（11） 💬（0）<div>中间人攻击最容易理解的可能就是fiddler吧，他可以截获request重新组织request的数据，有个专业的攻击工具叫burp。</div>2018-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（10） 💬（0）<div>PreparedStatement又是如何防范sql注入的呢？
preparedStatement = &quot;SELECT * FROM users WHERE name = ?&quot;;
preparedStatement.setString(1, userName);

查询“ SELECT * FROM users where where name =？” 将被发送到数据库，数据库会对其进行编译，然后将替换setString中的userName。 如果数据库看到非法值，它将引发错误。 因此，&#39;or&#39;1&#39;=&#39;1将被视为一个完整的字符串，而不是包含运算符or和=的语句, 也就是数据库将其视为值为 &quot;&#39; or &#39;1&#39;=&#39;1&quot;的字符（虽然是个奇怪的字符串）。
总结就一句话，占位符只能存储给定类型的值，而不能存储任意SQL片段（你写片段，我也把你看成是整体，即该类型的特别输入，比如上面的&quot;&#39; or &#39;1&#39;=&#39;1&quot;就被看成是一个特别的String）
https:&#47;&#47;stackoverflow.com&#47;questions&#47;4333015&#47;does-the-preparedstatement-avoid-sql-injection
https:&#47;&#47;en.wikipedia.org&#47;wiki&#47;SQL_injection</div>2021-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/c9/f44cb7f3.jpg" width="30px"><span>爪哇夜未眠</span> 👍（10） 💬（0）<div>期待杨晓峰老师直播！</div>2018-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/39/04/a8817ecf.jpg" width="30px"><span>会网络的老鼠</span> 👍（4） 💬（0）<div>或者通过明文传输、存储，这些都存在暴露安全隐患的可能。
朗读者将 明文 读成 文明
难道只有我注意到么？
</div>2018-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cf/49/af338c0f.jpg" width="30px"><span>wei</span> 👍（3） 💬（1）<div>String你懂双亲委派就知道，自己定义String是用不了的。</div>2019-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d1/15/7d47de48.jpg" width="30px"><span>咖啡猫口里的咖啡猫🐱</span> 👍（2） 💬（0）<div>我来回答，，鸡肉饭饭的，，，数据存在immutable,mutable,两种，java没有原生immutable支持，string如果是new就是相对意义的immutable,java基本类型和string是有高效缓存池范围，OK?</div>2018-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（1） 💬（0）<div>中间人攻击，现在https如果被中间人代理了，一般程序要检查https证书是否合法，Android就是在本地保存一份合法https证书去检查线上https是否合法，缺点就是每次https证书到期之前要升级一次客户端，还有就是抓包调试的时候需要去掉https证书检查，才能正常运行抓包。</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/50/6e/8bd276a5.jpg" width="30px"><span>匿名</span> 👍（1） 💬（0）<div>感谢老师！
</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/a7/674c1864.jpg" width="30px"><span>William</span> 👍（1） 💬（1）<div>类加载器本身也可以对代码之间进行隔离，例如，应用无法获取启动类加载器（Bootstrap Class-Loader）对象实例，不同的类加载器也可以起到容器的作用，隔离模块之间不必要的可见性等。

所以上面这段话没理解，  启动器加载器不是顶级父类加载器么？ 按照“双亲委派机制”不是从父加载器看是否能够加载对象么？ 怎么还无法回去对象实例了呢？</div>2019-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fd/fd/1e3d14ee.jpg" width="30px"><span>王宁</span> 👍（1） 💬（0）<div>纠结String的同学可以试一下，String应该是加载不了的。</div>2018-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/60/c5/69286d58.jpg" width="30px"><span>樱小路依然</span> 👍（0） 💬（0）<div>您好老师，我这几天突然发现半年之前开发中碰到的一个问题，有一个接口是接收信息存储数据库的，然后这个过程比较长，可能要几十秒，但是我在开发时，调用这个接口的是一个linux py脚本定时器，其中限制是5s超时。之后我经常发现服务跑了一段时间就挂了，需要重启，经过检查发现是由于大量的close_wait导致。
由于py脚本超时5s断开时，向服务发送fin，然后服务回了一个ack进入close_wait状态，但是此时并没有执行完方法，然而等方法执行完对py端发送fin时，py端已经不识别了，长时间的定时任务导致大量close_wait从而使tomcat容器假死。
请问这也算是一种攻击方式吗？我在网上查找解决方案，但是大部分是说服务方需要关闭httpclient，我使用的是springboot的@RequestMapping，好像没有类似解决的参数。</div>2022-02-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep424XzsecvviatRKB5JCDibJlvlEVhQLicY5FXueucRk3s1XtwWMUV3nfug7RI22EjRyHnIEWR4taJQ/132" width="30px"><span>paxos</span> 👍（0） 💬（0）<div>可以加新内容了，log4j JNDI 注入</div>2021-12-19</li><br/><li><img src="" width="30px"><span>地表十进制</span> 👍（0） 💬（0）<div>sql注入攻击是开发中需要避免的</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/53/9b/d0a21378.jpg" width="30px"><span>时代先锋</span> 👍（0） 💬（0）<div>不错</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/53/9b/d0a21378.jpg" width="30px"><span>时代先锋</span> 👍（0） 💬（0）<div>网络安全值得重视。</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f0/3e/f9f021bf.jpg" width="30px"><span>Geeker</span> 👍（0） 💬（0）<div>感谢老师！</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4b/26/3bea96f9.jpg" width="30px"><span>Victory</span> 👍（0） 💬（0）<div>这一讲看的完了，昨天面试的时候有问道注入攻击</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/4b/4fb10188.jpg" width="30px"><span>我奋斗去了</span> 👍（0） 💬（0）<div>终于可以见到杨老师真人了 😄</div>2018-07-18</li><br/>
</ul>