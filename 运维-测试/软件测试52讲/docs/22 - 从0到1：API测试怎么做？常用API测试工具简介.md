你好，我是茹炳晟，我今天分享的主题是“从0到1：API测试怎么做？常用API测试工具简介”。

在第11篇文章[《互联网产品的测试策略应该如何设计？》](https://time.geekbang.org/column/article/11462)中，我介绍过当今互联网产品的测试策略往往会采用菱形结构，即重量级 API 测试，轻量级 GUI 测试，轻量级单元测试，由此可见API测试在现今测试中的重要性不言而喻。

这篇文章是API自动化测试系列的第一篇文章，我会先为你打好API测试的基础。所以，我会先从0到1设计一个API测试用例，通过这个测试用例，你可以体会到最基本的API测试是如何进行的，并介绍几款常用的API测试工具。

## API测试的基本步骤

通常来讲，无论采用什么API测试工具，API测试的基本步骤主要包括以下三大步骤：

1. 准备测试数据（这是可选步骤，不一定所有API测试都需要这一步）；
2. 通过API测试工具，发起对被测API的request；
3. 验证返回结果的response。

对API的测试往往是使用API测试工具，比如常见的命令行工具cURL、图形界面工具Postman或者SoapUI、API性能测试的JMeter等。

为了让你更好地理解API测试具体是怎么做的，并掌握常见API测试工具的使用，我会以基于主流Spring Boot框架开发的简单Restful API为例，分别介绍如何使用cURL和Postman对其进行最基本的功能测试，目的是让你对API测试有一个基本的感性认识。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/95/4544d905.jpg" width="30px"><span>sylan215</span> 👍（29） 💬（2）<div>1. 这么一对比的话，Postman 完胜 cURL，实际情况也是 Postman 的使用更加的广泛，特别是开发相互之间做接口对接时，Postman 可以很方便的甩锅。

2. Postman 的 Pre-request Script 功能，可以支持变量的传入，应该也可以解决 API 调用的时序问题，比如前一个接口的返回值作为当前接口的入参。

3. Postman 如果设置了多个 Workspace，并且有 Collections 在不同 Workspace 之间分享的话，貌似还是同一份，从一个 Workspace 删除后，另一个 Workspace 也会被同步删除，有点坑，千万注意，还好的就是 Postman 的 web 版提供了 Trash 可以恢复不小心错删的内容，前段时间刚刚踩过这个坑，请关注。

4. 如果是简单的 URL 测试，我觉得使用 Python 的 requests 库做下分层设计，应该也是比较简单的，而且会更加灵活，也更适合做为日常的回归执行，这样也可以解决茹老师提到的时序问题和异步调用问题了。

以上，欢迎沟通交流，公众号「sylan215」</div>2018-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d0/5d/9f9d73fe.jpg" width="30px"><span>文大头</span> 👍（18） 💬（2）<div>说到异步，我现在的项目刚好有个场景，我使用jmeter压API，需要调用异步API创建一个东西，然后后台线程进行一系列操作后，更新这个东西的状态，我前端要等到他的状态变化后，再做下一步操作。具体做法是jmeter发起了创建操作后，循环执行一个查询状态操作，等到发现状态正常后再进行后续操作，或者状态异常&#47;超时后报错。有意思的是，如果后端数据库是个集群，这样测试，还能经常发现数据库集群的node间数据不同步的问题。</div>2018-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/78/87/66f6f2da.jpg" width="30px"><span>大QA</span> 👍（10） 💬（1）<div>小白请教个问题，Postman 可以批量执行(run)，为什么还需要newman ？是为了持续集成吗？</div>2018-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4c/b0/f22017b0.jpg" width="30px"><span>楚耳</span> 👍（10） 💬（1）<div>老师能深入讲解下Mock这个东西嘛，我看你好几篇文章都提到这个东西。还有这篇API 测试感觉完全没尽兴，现在公司都是自己用python 写代码测试API ，能讲讲自己开发一套api 测试框架的相关设计吗</div>2018-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/1f/7fac8712.jpg" width="30px"><span>DON    G</span> 👍（5） 💬（1）<div>异步api测试这块不太理解，我们现在基本都是用ajax实现异步请求，接口测试的时候就按照普通的接口进行测试，验证返回值，并没有对异步调用业务逻辑测试～ 🤔</div>2018-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c0/95/694658fd.jpg" width="30px"><span>桃夭夭</span> 👍（1） 💬（1）<div>老师，这个API测试也可以用testng来实现吧，是不是接口测试和API测试基本上算是同一个东西？</div>2019-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d6/54/3127cab2.jpg" width="30px"><span>赵明月</span> 👍（1） 💬（1）<div>postman预处理部分，是使用JS来产生请求报文中的字段取值，比如md5计算sign之类，在计算签名时候，把一大段JS实现的md5方法贴进预处理部分，进而调用，感觉很low啊，求教老师一般怎么写。</div>2018-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cb/4f/5bcf31f7.jpg" width="30px"><span>five years</span> 👍（0） 💬（1）<div>哈哈，终于等到api啦</div>2018-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/1f/7fac8712.jpg" width="30px"><span>DON    G</span> 👍（0） 💬（1）<div>异步调用返回成功的时候，前提都是基于数据库操作成功的吧，为什么还要再去验证数据库中的值呢？</div>2018-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f0/47/cc3c862d.jpg" width="30px"><span>Geek_558041</span> 👍（0） 💬（1）<div>这个是基本的接口测试，但是实际工作中，为了防止接口被刷通常都有验签功能，这一步怎么根据不同签名自动化.此外，测试环境基本依赖mock,包括各种正常场景和异常数据，mock是自己开发的吗？因为要支持不同的协议调用。如果使用mock，测试环境自动化似乎没有入参参数化的必要？请教老师</div>2018-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4c/b0/f22017b0.jpg" width="30px"><span>楚耳</span> 👍（0） 💬（1）<div>这么说wget 命令也算一个工具了</div>2018-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/ad/6e3e9e15.jpg" width="30px"><span>产品助理</span> 👍（0） 💬（1）<div>一直以来，仅对postman最基本的发送请求功能有所了解。通过今天的分享才知道，原来postman有如此多的功能，工具还是要多研究。

api依赖测试的场景例如接口1需要下单，接口2基于目标订单查询信息。相互依赖后场景变得复杂，测试成本变高，期待后续分享了解业界问题成熟解决方案。</div>2018-08-17</li><br/><li><img src="" width="30px"><span>豆豆</span> 👍（22） 💬（0）<div>这课的展现效果不好，有种茶壶煮饺子的感觉</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0b/35/2c56c29c.jpg" width="30px"><span>arthur</span> 👍（11） 💬（0）<div>我们的项目中也有异步API调用的情况，作为开发，他们也需要知道操作什么时候完成，然后做出后续操作。这边的异步，开发都会在数据库的一张表插入运行信息，完成后做出相应修改。所以测试的时候，也是通过查数据库来判断异步是否完成。</div>2018-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/9d/38/a67f8d3c.jpg" width="30px"><span>zyl</span> 👍（5） 💬（0）<div>摘要：
API测试的基本步骤：
1.	准备测试数据（可选）
2.	通过API测试工具发起对被测API的request
3.	验证返回的response

Postman是目前使用最广泛的http请求模拟工具之一，常被用于Web Service API的测试，具体操作如下：
1.	发起API调用
2.	添加结果验证
3.	保存测试用例
4.	基于Postman的测试代码生成

如何应对复杂场景的API测试？
场景1：被测业务是由多个API调用协作完成
通过API调用和结果解析的代码化就可以灵活处理上述场景。通过抓包的方式获取单个操作触发的API调用序列。
场景2：API测试过程中的第三方依赖
启用mock server来代替真实API就能实现
场景3：异步API的测试
异步API指的是调用后立即返回，但是任务没有完成，需要后续去查询或者回调的API.
异步API的测试主要分为两部分：
1.	测试异步调用是否成功
2.	测试异步调用的业务逻辑处理是否正确。
</div>2020-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dc/33/a68c6b26.jpg" width="30px"><span>捷后愚生</span> 👍（3） 💬（0）<div>学习到了，api测试，其实就是我们平时所说的接口测试。
如何应对复杂场景的 API 测试？这部分总结得非常好，可以直接拿来应对面试啊 ！

接触了python+ requests、python+httprunner，这两个都是比较容易上手的。
其实接口测试时也会用到PO思想，这篇文章没有介绍，不知道后面老师会不会提到。</div>2020-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c0/bc/c49e1eaa.jpg" width="30px"><span>静静张</span> 👍（3） 💬（2）<div>老师，这里的异步是多线程的意思吗？</div>2018-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/1f/d3/6a108d88.jpg" width="30px"><span>Gavin</span> 👍（2） 💬（0）<div>最近也学习接口测试，不过是基于Jmeter这款工具。
之前我理解的接口测试就是对照接口文档，填写对应的请求，参数，通过断言验证返回结果。
不过对于不规范的接口文档，自己通过Fiddler抓包查看时不确定哪些请求有用，哪些请求没什么用。
而且对于那种订单提交需要传很多参数时，看着有点懵。
简单接口参数，一些常用的可能通过变量获取使用，但那种提交需要很多参数的，不知道如何下手了。</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/ed/2a964aa4.jpg" width="30px"><span>Geek_269o5s</span> 👍（2） 💬（0）<div>长期来看还是使用测试框架进行API测试会更加合适，特别是很多公司还有非HTTP协议的情况下（如thirft、dubbo、hsf等）</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/c3/d41e8c79.jpg" width="30px"><span>不将就</span> 👍（2） 💬（0）<div>星主，您好，请问接口测试都要做数据库检查吗？</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/11/831cec7d.jpg" width="30px"><span>小寞子。(≥3≤)</span> 👍（2） 💬（0）<div>不知道有没有听过lisa，CA。 我们在用这个做中间件测试。 测试各种API。 包含了消息队列。 SOAP。 各种不同的call。。 要自己建立stub来连接中间件之后做自动化测试。。。。 也是遇到了很多挑战。</div>2019-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/29/b3133c45.jpg" width="30px"><span>芭蕉桑</span> 👍（2） 💬（2）<div>老师，我负责测试的一款APP最近完成了API测试的基本框架和测试代码，已经在迭代中试用了。但手工测试的用例编写数量和人力投入并没有减少。想请教一下老师，API测试如何运用才能有效地减少手工测试的人力投入呢？辛苦老师解答一下。</div>2018-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e5/d5/5bca3e9d.jpg" width="30px"><span>family</span> 👍（2） 💬（0）<div>能讲一下sdk的自动化测试么？</div>2018-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/39/a4c2154b.jpg" width="30px"><span>小昭</span> 👍（1） 💬（0）<div>之前做过接口测试，也用过postman，对这节课内容理解相对容易。
cURL之前没用过，现在下载了，研究一下。
接口测试还是要重点关注三个复杂场景的API测试。</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/de/32/8561a320.jpg" width="30px"><span>学无止境，唯乐学习</span> 👍（1） 💬（0）<div>时序API调用，最常见在场景自动化，或则登录接口，场景自动化我之前应用了方法调用方法的方法，可以按照一个场景对应一个测试用例。登录的话，testNG框架有对应的注解BeforeSuite（在test suite中的所有test运行之前运行，只运行一次）然后缓存获取的token，可以再BeforeSuite注解的方法里，查询缓存在Redis里的token，有的话执行登录方法，无执行登录方法</div>2020-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e1/8f/46c8b66f.jpg" width="30px"><span>Geek_guzhenhua</span> 👍（1） 💬（0）<div>接口测试的用例应该如何设计，如果参数很多，是否需要按照功能测试的用例设计方法，组合起来的参数的接口测试用例会很多。希望老师解答一下</div>2019-10-11</li><br/><li><img src="" width="30px"><span>豆豆</span> 👍（1） 💬（0）<div>这种课应该录制成视频，只是看图说话，没有演绎的过程理解起来很费劲。</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（1） 💬（0）<div>1、老师为什么不用interface test，而用API test
2、Python 中的requests 您感觉如何？</div>2018-10-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIGzSM6be2xCNS00kQYHDgXO3icOoOSsvnz3FiaCov5Kgs6oaXkBicLbicuEerJjiaNPWxB0FTVmdur3kg/132" width="30px"><span>Xiye</span> 👍（1） 💬（0）<div>我目前的项目就有涉及到异步API测试，我们的Agent端产品是提供lib库，客户需要集成我们的li库到他们的产品。我们需要测试这些库公开的API函数。我们的某些API的参数就是callback回调函数，这些回调函数主要是处理网络传输，当时也是花了好长时间理解原理。我目前的做法就是自己写相应代码实现网络传输，构造正确的Response数据，错误Response数据，非正常的网络状态等看我们API处理结果。</div>2018-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/28/db/0112a8bb.jpg" width="30px"><span>明月天涯</span> 👍（0） 💬（0）<div>老师 jmeter用来做接口测试怎么样</div>2024-05-31</li><br/>
</ul>