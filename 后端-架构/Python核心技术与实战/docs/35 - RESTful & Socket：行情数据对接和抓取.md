你好，我是景霄。

上一节课，我们介绍了交易所的交易模式，数字货币交易所RESTful接口的常见概念，以及如何调用RESTful接口进行订单操作。众所周知，买卖操作的前提，是你需要已知市场的最新情况。这节课里，我将介绍交易系统底层另一个最重要的部分，行情数据的对接和抓取。

行情数据，最重要的是实时性和有效性。市场的情况瞬息万变，合适的买卖时间窗口可能只有几秒。在高频交易里，合适的买卖机会甚至在毫秒级别。要知道，一次从北京发往美国的网络请求，即使是光速传播，都需要几百毫秒的延迟。更别提用Python这种解释型语言，建立HTTP连接导致的时间消耗。

经过上节课的学习，你对交易应该有了基本的了解，这也是我们今天学习的基础。接下来，我们先从交易所撮合模式讲起，然后介绍行情数据有哪些；之后，我将带你基于Websocket的行情数据来抓取模块。

## 行情数据

回顾上一节我们提到的，交易所是一个买方、卖方之间的公开撮合平台。买卖方把需要/可提供的商品数量和愿意出/接受的价格提交给交易所，交易所按照公平原则进行撮合交易。

那么撮合交易是怎么进行的呢？假设你是一个人肉比特币交易所，大量的交易订单往你这里汇总，你应该如何选择才能让交易公平呢？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJOlibibPFEWOib8ib7RtfAtxND5FUqCxxoeTuLAbBI9ic23xuwdXT4IyiaWq3Fic9RgEAYI0lBTbEp2rcg/132" width="30px"><span>Jingxiao</span> 👍（58） 💬（0）<div>思考题答案：
Websocket 可能丢包。TCP 协议保证了所有的包按顺序抵达（即使是乱序抵达，在前面的包收到之前，TCP 协议下的底层程序也会讲先到达的靠后的包缓存，直到前面的包抵达，才送给上层的应用程序），但是并不能保证不可恢复的错误发生的时候，包不会丢失。这种情况发生的时候，就会出现 Orderbook 中一个或多个（价格，数量）信息没得到及时更新。这种错误越积攒越多的情况下，就会导致本地的 Orderbook 充满垃圾信息，变得完全不可靠。因此一个很好的做法是，可以设置一个时间间隔，通过 RESTFul 或者其他方式重新抓一下 Orderbook 的 Snapshot，然后和本地的 Orderbook 进行比对，纠正错误。</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bc/29/022905e6.jpg" width="30px"><span>SCAR</span> 👍（47） 💬（1）<div>思考题：
1. websocket基于tcp的，虽然协议上有纠错，重传和等待的机制，但一些特殊的情况还是可能会有丢包的情况，比如同时有超过服务器负载的客户端在请求数据。
2.如果丢包的情况发生时，类似开大会会场人人都发微信图片，看着WiFi信号满格，却发不出去，差不多一样的道理爬虫也是收不到数据的。
3.查了下websocket的WebSocketApp的函数，有个参数on_error，是websocket发生错误的时候触发的，那么我们可以编写这个对应的回调函数来让服务器重发或者其他有效的处理。</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（6） 💬（1）<div>websocket资料
https:&#47;&#47;pypi.org&#47;project&#47;websocket_client&#47;</div>2019-07-29</li><br/><li><img src="" width="30px"><span>Geek_adeba6</span> 👍（4） 💬（1）<div>想请问是否可以使用STOMP协议与Gemini这样的交易平台通信, 像消息队列rabbitmq 有 stomp的plugins</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/84/55/1e40bd61.jpg" width="30px"><span>shiziwen</span> 👍（3） 💬（1）<div>请问文章中，接口获取的数据中，bids和ask是什么意思呢？</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/90/6d/f0dd5cb3.jpg" width="30px"><span>Merlin</span> 👍（3） 💬（1）<div>对于web socket的编程，可以用asyncio，我觉得用asyncio来开发web socket更为方便</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fd/91/65ff3154.jpg" width="30px"><span>_stuView</span> 👍（1） 💬（2）<div>我之前看到Linux公众号讲python并不是一个解释型语言，而是一个运行在虚拟机上的语言https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;Yqwk_eXO1t5N2cjRz_u0sw</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（45） 💬（1）<div>websocket包的安装使用如下命令:

pip -m install websocket_client安装。

pip -m install websocket会安装另外一个完全不同的包</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/b3/a74a7125.jpg" width="30px"><span>tux</span> 👍（16） 💬（0）<div>干布球和tt 的提示，解决了报错。
import websocket     #pip install websocket-client
import _thread as thread

在查找资料时，看到了：
import websocket
try:
    import thread
except ImportError:
    import _thread as thread
</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/7d/c7e8cd34.jpg" width="30px"><span>干布球</span> 👍（8） 💬（1）<div>第二段代码少了个import time，python3里面thread用import _thread，不知是不是这样？</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/44/3d/35d6670d.jpg" width="30px"><span>Claywoow</span> 👍（7） 💬（1）<div>老师，请教个问题，为什么我把这两个类分成两个模块来测试的时候，程序会进入无响应的状态，好像一直在运行，这会是什么原因呢？</div>2019-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bc/29/022905e6.jpg" width="30px"><span>SCAR</span> 👍（7） 💬（3）<div>尝试回答下Destroy的问题：
查看WebsocketApp函数：
on_message: callable object which is called when received data.
 on_message has 2 arguments.
 The 1st argument is this class object.
 The 2nd argument is utf-8 string which we get from the server.
你如果直接on_message = self.on_message，那么会缺少第一个参数，因为class Crawler类里on_message(self,message)是缺少如最上面老师例子def on_message(ws, message)里的ws的。所以
on_message = lambda ws, message: self.on_message(message)是通过lambda补上第一个参数ws。</div>2019-07-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（4） 💬（0）<div>实测on_message = self.on_message没有问题，源码中_callback中只是对回调函数做了类型判断，self.on_message是和method，所以直接将返回data给了形参message，执行接受数据的处理</div>2019-08-03</li><br/><li><img src="" width="30px"><span>Geek_688e7c</span> 👍（3） 💬（2）<div>按照老师的代码来都没有反应，是不是Url失效了？ 我直接在浏览器里访问Url是说无法访问。
出现程序运行没有报错但是没有任何输出和结果的情况，是不是就是服务端出了问题呢</div>2022-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/a5/43aa0c27.jpg" width="30px"><span>TKbook</span> 👍（3） 💬（2）<div>因此，应该你注意到了，它的第一个参数是 self，这里如果直接写成 on_message = self.on_message 将会出错。
为了避免这个问题，我们需要将函数再次包装一下。这里我使用了前面学过的匿名函数，来传递中间状态，注意我们只需要 message，因此传入 message 即可。
这段没看懂，老师或者哪位大神能解释一下？</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/46/15/0f215f66.jpg" width="30px"><span>BinyGo</span> 👍（2） 💬（0）<div>    理解：on_message = lambda ws, message: self.on_message(message)
    我们先来看一个lambda的函数写法：
    g = lambda x, y=2, z=3: x + y + z
    g(1, z=4, y=5)  # 输出结果是10
    这个表达式也可以写成
    def g(x, y=2, z=3):
        return x + y + z


    那么再来理解老师的写法，也就好理解多了

    websocket原本的on_message被我们修改为匿名函数，
    也就是当websocket回调的时候，本来是带2个参数ws和message去找on_message函数的，变成了去找我们写的匿名函数
    on_message(ws, message)，改成匿名函数：anonymous(ws, message)，也对应了lambda ws, message 因此这里参数必须一致
    def anonymous(ws, message):  # 这里函数名称随意，因为是匿名函数，只是来理解lambda的写法
        self.on_message(message) #这里再让程序去执行我们需要的代码。绕了一个圈

    为了验证这个逻辑流程，下面2行代码参数名改一下，做一个输出，执行老师的代码大概就20多秒就有打印采集的数据，验证成功
    self.ws = websocket.WebSocketApp(&#39;wss:&#47;&#47;api.gemini.com&#47;v1&#47;marketdata&#47;{}&#39;.format(symbol),
                                     on_message=lambda gg, mmm: self.on_message(mmm))
    def on_message(self, mmm):
        print(mmm)
    最后不知道有没更优美的写法呢？？？</div>2021-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/51/86/b5fd8dd8.jpg" width="30px"><span>建强</span> 👍（2） 💬（4）<div>网络编程没有经验，想问下老师，我用的是Python3，用ws = websocket.WebSocketApp(&quot;ws:&#47;&#47;echo.websocket.org&#47;&quot;,
                              on_message = on_message,
                              on_open = on_open)是报错的，错误信息：AttributeError: module &#39;websocket&#39; has no attribute &#39;WebSocketApp&#39;，这是什么原因？</div>2020-02-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKxqOFPRvW2d6WEC705zuSSvxBOBxibBib4XQxBGAGPOx2bRGqhsSeQkUNa0Z11OJoKbuGsNaMR4GNg/132" width="30px"><span>hel793</span> 👍（1） 💬（0）<div>Latency is 2630.9838048 ms</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/29/d6816ebf.jpg" width="30px"><span>小侠龙旋风</span> 👍（1） 💬（0）<div>最近在复习js的相关知识，js中socket.io库封装了websocket，同时也包含了其他连接方式，比如ajax。socket.on(event_name, callback)中的内置事件名有10种。https:&#47;&#47;socket.io&#47;docs&#47;client-api&#47;</div>2019-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/29/d6816ebf.jpg" width="30px"><span>小侠龙旋风</span> 👍（1） 💬（0）<div>会丢包，在on_error(ws, error)回调函数中做处理</div>2019-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第35讲打卡~</div>2024-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/58/8d/bc69cde1.jpg" width="30px"><span>浩克</span> 👍（0） 💬（0）<div>我之前看到Linux公众号讲python并不是一个解释型语言，而是一个运行在虚拟机上的语言https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;Yqwk_eXO1t5N2cjRz_u0sw；
如果一定要回答 Python 是不是解释型语言，那么答案是它是部分编译型语言。它和 Java 类似，不会像 C++ 一样编译到机器语言，而是编译成字节码来提高执行速度。https:&#47;&#47;stackoverflow.com&#47;questions&#47;6889747&#47;is-python-interpreted-or-compiled-or-both</div>2024-02-20</li><br/><li><img src="" width="30px"><span>肖肖</span> 👍（0） 💬（0）<div>并发执行websocket连接，都能连接成功，但都立马断了，只会连接一个，是什么原因呢</div>2022-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/89/23/e71f180b.jpg" width="30px"><span>Geek_fc975d</span> 👍（0） 💬（1）<div>我安装了websocket_Client了，但是发现这个函数run_foreve总是提示找不到对应函数，请问大家有遇到相同问题的吗？</div>2022-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/b9/4c/8c9edc85.jpg" width="30px"><span>小庞</span> 👍（0） 💬（0）<div>sha384是非对称算法？难道不是计算消息认证码的吗？解决不可否认性和完整性的</div>2021-11-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/a8PMLmCTCBa40j7JIy3d8LsdbW5hne7lkk9KOGQuiaeVk4cn06KWwlP3ic69BsQLpNFtRTjRdUM2ySDBAv1MOFfA/132" width="30px"><span>Ilovek8s</span> 👍（0） 💬（0）<div>http2最怕包头阻塞</div>2021-07-01</li><br/><li><img src="" width="30px"><span>Geek_a16bbc</span> 👍（0） 💬（0）<div>還是不能理解為何需要用lambda才能把self傳進去？
lambda ws, message: self.on_message(message))
ws 和self有什麼關係？</div>2020-10-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIiaeebUYxl7e1b8DhQGz7v6uibGcytfL8iaTke1S6NwSVxicOy5iaLGbRn2aZtxZy8vVnF6j3fjtxDEbQ/132" width="30px"><span>daowuli_chihai</span> 👍（0） 💬（0）<div>下面代码 【import thread】报错，python3要不要改成【import _thread】


import websocket
import thread

# 在接收到服务器发送消息时调用
def on_message(ws, message):
    print(&#39;Received: &#39; + message)

# 在和服务器建立完成连接时调用   
def on_open(ws):
    # 线程运行函数
    def gao():
        # 往服务器依次发送0-4，每次发送完休息0.01秒
        for i in range(5):
            time.sleep(0.01)
            msg=&quot;{0}&quot;.format(i)
            ws.send(msg)
            print(&#39;Sent: &#39; + msg)
        # 休息1秒用于接收服务器回复的消息
        time.sleep(1)
        
        # 关闭Websocket的连接
        ws.close()
        print(&quot;Websocket closed&quot;)
    
    # 在另一个线程运行gao()函数
    thread.start_new_thread(gao, ())


if __name__ == &quot;__main__&quot;:
    ws = websocket.WebSocketApp(&quot;ws:&#47;&#47;echo.websocket.org&#47;&quot;,
                              on_message = on_message,
                              on_open = on_open)
    
    ws.run_forever()

#### 输出 #####
Sent: 0
Sent: 1
Received: 0
Sent: 2
Received: 1
Sent: 3
Received: 2
Sent: 4
Received: 3
Received: 4
Websocket closed</div>2020-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/84/55/1e40bd61.jpg" width="30px"><span>shiziwen</span> 👍（0） 💬（0）<div>想问一个业务逻辑的问题，想获取一段时间内的订单，用来测试自己的交易所逻辑，应该使用哪个接口呢？orderbook和tick data的概念还没有理解透。
Gemini的账户没有注册成功，所以调试遇到了些问题。</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/41/ba/ae028565.jpg" width="30px"><span>YqY</span> 👍（0） 💬（1）<div>请问抓取 orderbook 信息的脚本在第50和51行转换成字典的意义何在？没怎么看明白，请老师解答下</div>2020-02-22</li><br/>
</ul>