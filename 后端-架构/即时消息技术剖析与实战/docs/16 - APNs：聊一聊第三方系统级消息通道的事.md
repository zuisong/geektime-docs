你好，我是袁武林。

前面几节课里，我讲到在即时消息场景下，我们会依赖服务端推送技术来提升消息到达的实时性，以及通过各种手段来保证消息收发通道的可用性，从而让消息能尽量实时、稳定地给到接收人。

但在实际情况中，出于各种原因，App与服务端的长连接会经常断开。比如，用户彻底关闭了App，或者App切换到后台一段时间后，手机操作系统为了节省资源，会杀掉进程或者禁止进程的网络功能。在这些情况下，消息接收方就没有办法通过App和IM服务端的长连接来进行消息接收了。

那有没有办法，能让消息在App被关闭或者网络功能被限制的情况下，也能发送到接收人的设备呢？答案是：有。

现在手机常用的iOS和Android系统，都提供了标准的系统级下发通道，这个通道是系统提供商维护的与设备的公共长连接，可以保证在App关闭的情况下，也能通过手机的通知栏来下发消息给对应的接收人设备。而且，当用户点击这些通知时，还能重新唤醒我们的App，不仅能提升消息的到达率，还增加了用户的活跃度。

## 第三方系统下发通道

常见的第三方系统下发通道，有iOS端的APNs，以及Android端的GCM和厂商系统通道。

- iOS端的APNs（Apple Push Notification service，苹果推送通知服务），是独立于应用之外，依托系统常驻进程来维护和苹果服务器的公共长连接，负责全局的系统推送服务。
- 在Android端上，有Google的GCM（Google Cloud Message，Google云消息传递）。但GCM由于某些技术原因（如NAT超时太长、暴露的5228端口连通性差等）和某些非技术原因（需要和Google服务器建立连接），Android端的GCM在国内被大部分手机厂商定制化后直接去掉，并替换成了各自的系统通道。目前国内Android的系统级下发通道基本都是厂商通道，目前已知的有5家：小米、华为、vivo、OPPO、魅族。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/e6/87197b10.jpg" width="30px"><span>GeekAmI</span> 👍（6） 💬（1）<div>“一般情况下，我们的 IM 服务端可以在每次启动 App 时，都去请求 APNs 服务器进行注册，来获取 DeviceToken。” 
老师，这句话不太理解，到底是App去APNs获取DeviceToken，还是IM服务端获取呢？</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f9/24/c920101e.jpg" width="30px"><span>冬</span> 👍（2） 💬（1）<div>老师，Apple除了静默推送，还有更可靠的Voip 推送哦</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/5c/39/6b542136.jpg" width="30px"><span>谢炳辉</span> 👍（2） 💬（1）<div>怎么理解
因此在没有 WiFi 和移动网络的场景下，我们只要有手机信号就能推送
不是有信号就有网络了吗</div>2019-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/6c/0c2a26c7.jpg" width="30px"><span>clip</span> 👍（2） 💬（4）<div>“DeviceToken 是 APNs 用于区分识别不同 iOS 设备同一个 App 的唯一标识”
是“不同 iOS 设备不同 App”吗？</div>2019-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/e6/87197b10.jpg" width="30px"><span>GeekAmI</span> 👍（1） 💬（1）<div>静默推送是不是可以这样搞？
静默推送-&gt;唤起app-&gt;重新建立长连接通道-&gt;服务端通道长连接通道下达消息。</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（1） 💬（2）<div>请问如果发送方使用小米的推送服务，那么非小米手机怎样接收到消息呢？竞争品牌可能不允许在手机里安装小米的拉取软件。</div>2019-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/8f/551b5624.jpg" width="30px"><span>小可</span> 👍（1） 💬（1）<div>app后台自动升级(如果设置自动更新升级)</div>2019-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/be/b7/638b5d30.jpg" width="30px"><span>白泗小林</span> 👍（0） 💬（1）<div>apns 的消息去重一般怎么做的？</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/73/a3/2b077607.jpg" width="30px"><span>Michael</span> 👍（0） 💬（2）<div>每台iPhone设备的的deviceToken都不一样，IM服务器给APNs推送消息数据需要带上deviceToken,但是IM Server是如何获取到设备的deviceToken的呢？</div>2019-10-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKsBRgibKxD2M0ibmgPqfcoaZOxmUrwCCGlex8xehyYeeTOEN2ibtQ5S6t30LoOKFvMR5KDm5gnU99PQ/132" width="30px"><span>Michael</span> 👍（0） 💬（1）<div>思考题：可以唤起app，重新建立长连接。</div>2019-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（2） 💬（0）<div>推必达产品还没做出来 凉了应该，域名也不能访问了chinaupa.com</div>2022-09-19</li><br/><li><img src="" width="30px"><span>Geek_23ac9c</span> 👍（0） 💬（0）<div>老师，我想请问一下，每次接受到APNs推送后都会唤醒app，但是如何知道将json格式的消息转发给被唤醒的app的哪个页面或者方法进行处理呢？</div>2025-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/5d/c35b117c.jpg" width="30px"><span>薛建辉</span> 👍（0） 💬（0）<div>老师你好，我实际工作中遇到一个问题，如何提高自建长连接的在线推送成功率。

原本国内线上单次推送成功率在70%左右，我将业务心跳从30秒改成5秒之后，线上环境成功率提升到90%，内测环境成功率达到98%，将近10%的差距。请老师给些下一步改造建议。

我想到的下一步改造措施是：从原本单次推送，改成5秒内多次重推的方式。请问老师是否靠谱？

另外，请教下老师你是怎么提高自建长连接推送成功率的？</div>2022-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/a9/5b/791d0f5e.jpg" width="30px"><span>不卷怎么搞钱</span> 👍（0） 💬（1）<div>老师，我想问下，DeviceToken存的话怎么存好点呢？因为当大批量发push的时候，可能要查几百万的DeviceToken去发push，对于循环查mysql来说，肯定是没那么友好，reids的话也不合适，因为可能有的用户每天就只会收到一条push，redis的成本也高。</div>2022-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a3/e2/5cb4f43f.jpg" width="30px"><span>laolinshi</span> 👍（0） 💬（0）<div>老师，想问个问题，每次调用APNS通道时需要传人deviceToken, 假如一次需要推送几千万的用户，那传人APNS接口的deviceToken就会达到几千万这个量级？</div>2022-03-28</li><br/><li><img src="" width="30px"><span>Geek_fa166f</span> 👍（0） 💬（0）<div>请教下老师：海外APP推送，使用什么第三方的服务比较好呢（包含IOS以及安卓）?</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/25/a384ee7a.jpg" width="30px"><span>李进</span> 👍（0） 💬（0）<div>之前做过IPad的mdm，有用到APNS，应该是静默推送。</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/83/69/77256c74.jpg" width="30px"><span>空白</span> 👍（0） 💬（0）<div>请教下 统一推送联盟不会出统一的sdk嘛？目前和第三方厂商了解到 并没有提供，对于开发者接入的成本还是很大</div>2020-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/02/d1/36285394.jpg" width="30px"><span>🐌🐌🐌</span> 👍（0） 💬（1）<div>im中app端如何实现在线电话和在线视频，现在流行一般采用何种技术实现，在线视频和电话在服务端说一般做录音存储文件吗？</div>2020-03-16</li><br/>
</ul>