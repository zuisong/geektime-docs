前面我们通过两篇文章详细介绍了 Medooze 的实现逻辑，我相信你现在已经对 Medooze 有了非常深刻的认知。通过对Medooze实现原理和架构的了解，我们可以知道Medooze支持的功能非常多，如录制回放、推流、SFU 等，其中最主要的功能是 SFU 的实现。

实际上，**我们要实现的多方音视频会议就是由 SFU 来实现的，或者你可以认为Medooz实现的 SFU 就是一个最简单的音视频会议系统**。Medooze 提供的 SFU Demo 的地址为：[https://github.com/medooze/sfu](https://github.com/medooze/sfu) 。

由于 SFU 是一个 Node.js 项目，所以在环境部署、源码分析的时候，需要你有 JavaScript 基础，也需要掌握 NPM 和 Node 的常用命令，比如 npm install 等。接下来，我们主要从以下几方面向你介绍一下多方音视频会议（SFU）项目：

- 搭建多方音视频会议系统，让你感受一下多方通信；
- 分析多方音视频会议实现的架构；
- 分析 Medooze API 的具体使用；
- 分析多方音视频会议的入会流程。

## 多方音视频会议环境的搭建

多方音视频会议（SFU）项目是纯 Node.js 实现的，可以说在目前所有的操作系统上都可以运行。然而，由于该系统依赖 medooze-media-server 项目，而该项目仅支持 macOS X 和 Linux 两种操作系统，所以 SFU 项目也只能在 macOS X 和 Linux 这两种操作系统下运行了。
<div><strong>精选留言（25）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1f/05/94/e55abef3.jpg" width="30px"><span>Her later</span> 👍（2） 💬（1）<div>大佬 您好 ： 
offer 和 answer 都是客户端自己创建的 ，那RTCPeerConnection  怎么知道要把流推到自己的中转服务器呢 。
服务器的配置信息是怎么得到的呢 ，是否offer和answer发送到信令服务器后 ，信令服务器对其进行了封装？ </div>2021-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/72/18/a0b03020.jpg" width="30px"><span>张昌海185</span> 👍（2） 💬（1）<div>老师好，有个问题搞不清楚，就是sfu模式中多人通话，接收着怎么判断收到的媒体数据，是哪一个用户发出的呢？</div>2020-11-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/xaL9uxibkT3AKspw9bPYXnsibQJztSjY1vxiceovK5UUHA3AsCCJEfJtR1fOzHxADz13OR8rktgQxIiaO1YOXsByiaQ/132" width="30px"><span>陈龙</span> 👍（1） 💬（4）<div>老师，centOS 6.5 npm install 失败
make: *** [Release&#47;obj.target&#47;medooze-media-server&#47;src&#47;media-server_wrap.o] Error 1
make: *** Waiting for unfinished jobs....
..&#47;media-server&#47;src&#47;RTPTransport.cpp: In member function ‘int RTPTransport::SetLocalCryptoSDES(const char*, const uint8_t*, uint32_t)’:
..&#47;media-server&#47;src&#47;RTPTransport.cpp:219:22: warning: comparison between signed and unsigned integer expressions [-Wsign-compare]
  if (len!=policy.rtp.cipher_key_len)
                      ^
..&#47;media-server&#47;src&#47;RTPTransport.cpp: In member function ‘int RTPTransport::SetRemoteCryptoSDES(const char*, const uint8_t*, uint32_t)’:
..&#47;media-server&#47;src&#47;RTPTransport.cpp:363:22: warning: comparison between signed and unsigned integer expressions [-Wsign-compare]
  if (len!=policy.rtp.cipher_key_len)
                      ^
make: Leaving directory `&#47;home&#47;chenlong&#47;sfu-master&#47;node_modules&#47;medooze-media-server&#47;build&#39;
gyp ERR! build error 
gyp ERR! stack Error: `make` failed with exit code: 2
gyp ERR! stack     at ChildProcess.onExit (&#47;home&#47;chenlong&#47;node-v12.16.1-linux-x64&#47;lib&#47;node_modules&#47;npm&#47;node_modules&#47;node-gyp&#47;lib&#47;build.js:194:23)
gyp ERR! stack     at ChildProcess.emit (events.js:311:20)
gyp ERR! stack     at Process.ChildProcess._handle.onexit (internal&#47;child_process.js:275:12)
gyp ERR! System Linux 3.10.5-3.el6.x86_64
gyp ERR! command &quot;&#47;home&#47;chenlong&#47;node-v12.16.1-linux-x64&#47;bin&#47;node&quot; &quot;&#47;home&#47;chenlong&#47;node-v12.16.1-linux-x64&#47;lib&#47;node_modules&#47;npm&#47;node_modules&#47;node-gyp&#47;bin&#47;node-gyp.js&quot; &quot;rebuild&quot; &quot;--jobs=max&quot;
gyp ERR! cwd &#47;home&#47;chenlong&#47;sfu-master&#47;node_modules&#47;medooze-media-server
gyp ERR! node -v v12.16.1
gyp ERR! node-gyp -v v5.0.5
gyp ERR! not ok 
npm ERR! code ELIFECYCLE
npm ERR! errno 1
npm ERR! medooze-media-server@0.27.2 install: `test -f build&#47;Release&#47;medooze-media-server.node || (node-gyp configure &amp;&amp; node-gyp rebuild --jobs=max)`
npm ERR! Exit status 1
npm ERR! 
npm ERR! Failed at the medooze-media-server@0.27.2 install script.

</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f7/88/da243c77.jpg" width="30px"><span>大魔王</span> 👍（1） 💬（1）<div>老师,这个和之前的medooze-server-node 区别是什么啊</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/70/68/0fc42e2d.jpg" width="30px"><span>No</span> 👍（1） 💬（5）<div>&#47;src&#47;media-server_wrap.cxx: At global scope:
..&#47;src&#47;media-server_wrap.cxx:909:7: error: ‘Handle’ in namespace ‘v8’ does not name a template type
   v8::Handle&lt;v8::Value&gt; err;
       ^
..&#47;src&#47;media-server_wrap.cxx: In member function ‘virtual void OverloadErrorHandler::error(int, const char*)’:
..&#47;src&#47;media-server_wrap.cxx:904:5: error: ‘err’ was not declared in this scope
     err = v8::Exception::Error(SWIGV8_STRING_NEW(msg));
老师，我 npm install 的时候报错了。 这是nodejs 版本问题吗？

我的版本 
 node -v v12.13.0
 node-gyp -v v5.0.5
系统是 Ubuntu 16.04  </div>2019-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/0c/a2/14c30983.jpg" width="30px"><span>阿良</span> 👍（0） 💬（2）<div>老师你好，我搭建medooze之后，服务顺利跑起来了，但是只能看到自己的图像，而没法看到其他人的。我调试发现他们的video的id编码不一致，想往这方面调试，但是在评论区没看到小伙伴有这样的问题，所以想跟老师请教下，我遇到的这个问题有可能是什么引起的？如有可能，能否提供测试可以正常使用的demo，感谢~</div>2021-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/98/ee/43bb6c11.jpg" width="30px"><span>会飞的猪</span> 👍（0） 💬（1）<div>老师，用medooze录制的mp4视频不能播放，您有遇到过吗？
const recorder = MediaServer.createRecorder (ts +&quot;.mp4&quot;,{
			refresh : 1000,
			timeShift : 6000,
			disableHints : true,
			waitForIntra: true
		});
		recorder.record(incomingStream);</div>2020-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/87/9e/e18f55ec.jpg" width="30px"><span>张一画</span> 👍（0） 💬（1）<div>老师 我有一些不太理解 这一课里面的HTTPS证书为什么是自己生成 我记得您之前说必须是权威机构发布的证书</div>2020-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/72/a8/c24a66a1.jpg" width="30px"><span>Geek_sky</span> 👍（0） 💬（3）<div>老师，我这边连接的时候遇到这个问题：
VM479:1 Uncaught DOMException: Failed to execute &#39;createEncodedVideoStreams&#39; on &#39;RTCRtpSender&#39;: Encoded video streams not requested at PC initialization
    at eval (eval at ws.onopen (https:&#47;&#47;192.168.50.150:8084&#47;js&#47;sfu.js:264:36), &lt;anonymous&gt;:1:8)
    at WebSocket.ws.onopen (https:&#47;&#47;192.168.50.150:8084&#47;js&#47;sfu.js:264:36)
我换了createEncodedStreams，也不行。这是什么问题？chrome是不是需要设置什么？</div>2020-09-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3giaicn2VaDJicDD7WnaT9mB5VbaF6J7aQszN4W9BVmSWmKoVFxTuN7iaDDgrKhlFp49k1iacvjMYSH3eejVbaH0Vhw/132" width="30px"><span>sam</span> 👍（0） 💬（2）<div>跑起来后到页面加入房间，点ready后页面刷新一下还是弹窗让加入房间是什么情况，貌似也找不到log</div>2020-07-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/WgRsoJMxcTMcDkRlR59jCDLux2JDdtz1G8Ophe3a7EnhP8lqOdFw8F7sURXkRTYXibzVicozrQ8HFYj578myJ0CA/132" width="30px"><span>行所当行</span> 👍（0） 💬（8）<div>老师你好，在客户端的chrome打开index.html，提示: Your browser does not support insertable streams，chrome版本83.0.4103.61(正式版本)(64位)，这个是浏览器版本问题吗？</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/87/fa/403e82ea.jpg" width="30px"><span>dayu</span> 👍（0） 💬（1）<div>老师，可以基于medooze开发安卓版的视频会议么？</div>2020-05-08</li><br/><li><img src="" width="30px"><span>pyg</span> 👍（0） 💬（2）<div>老师我在本地运行了sfu服务，打开了两个Chrome窗口，但是互相看不见对方。哪些原因会导致这样呢？</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/db/25/47fd129d.jpg" width="30px"><span>檸檬稻</span> 👍（0） 💬（3）<div>最后卡在，
我的版本
 node 12.15.0&#47;10.13.0
 npm 6.4.1
系统是 Ubuntu 18.04 &#47;Ubuntu 14.04
这些都试了，openSSL 两个版本也试了1.1.1与1.0.2d最后卡在 node运行不起来
internal&#47;modules&#47;cjs&#47;loader.js:717                                                                                      
  return process.dlopen(module, path.toNamespacedPath(filename));                                                       
                 ^                                                                                                      
                                                                                                                        
Error: &#47;root&#47;sfu&#47;node_modules&#47;medooze-media-server&#47;build&#47;Release&#47;medooze-media-server.node: undefined symbol: HMAC_CTX_i
nit                                                                                                                     
    at Object.Module._extensions..node (internal&#47;modules&#47;cjs&#47;loader.js:717:18)                                          
    at Module.load (internal&#47;modules&#47;cjs&#47;loader.js:598:32)                                                              
    at tryModuleLoad (internal&#47;modules&#47;cjs&#47;loader.js:537:12)                                                            
    at Function.Module._load (internal&#47;modules&#47;cjs&#47;loader.js:529:3)                                                     
    at Module.require (internal&#47;modules&#47;cjs&#47;loader.js:636:17)                                                           
    at require (internal&#47;modules&#47;cjs&#47;helpers.js:20:18)                                                                  
    at Object.&lt;anonymous&gt; (&#47;root&#47;sfu&#47;node_modules&#47;medooze-media-server&#47;lib&#47;Native.js:10:19)                             
    at Module._compile (internal&#47;modules&#47;cjs&#47;loader.js:688:30)                                             </div>2020-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7b/d0/e39b1875.jpg" width="30px"><span>ralph</span> 👍（0） 💬（1）<div>老师，能不能提高一个视频通信的例子，音频的看完，还是没想明白视频怎么弄.....</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/24/dbc4d29d.jpg" width="30px"><span>颜广杰</span> 👍（0） 💬（3）<div>安装过程有报错，然后运行之后报错。root@iZwz9isydglfcdgnqd84a4Z:&#47;home&#47;sfu# node index.js 47.112.45.177
&#47;home&#47;sfu&#47;lib&#47;Room.js:59
                this.activeSpeakerDetector = MediaServer.createActiveSpeakerDetector();
                                                         ^

TypeError: MediaServer.createActiveSpeakerDetector is not a function
    at new Room (&#47;home&#47;sfu&#47;lib&#47;Room.js:59:44)
    at WebSocketServer.ws.on (&#47;home&#47;sfu&#47;index.js:116:10)
    at WebSocketServer.emit (events.js:198:13)
    at WebSocketServer.handleUpgrade (&#47;home&#47;sfu&#47;node_modules&#47;websocket&#47;lib&#47;WebSocketServer.js:213:14)
    at Server.emit (events.js:198:13)
    at onParserExecuteCommon (_http_server.js:555:14)
    at onParserExecute (_http_server.js:501:3)

</div>2019-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/24/dbc4d29d.jpg" width="30px"><span>颜广杰</span> 👍（0） 💬（1）<div>..&#47;external&#47;mp4v2&#47;lib&#47;src&#47;itmf&#47;type.cpp:258:1: warning: missing initializer for member ‘mp4v2::impl::Enum&lt;mp4v2::impl::itmf::ContentRating, (mp4v2::impl::itmf::ContentRating)255&gt;::Entry::formal’ [-Wmissing-field-initializers]
..&#47;external&#47;mp4v2&#47;lib&#47;src&#47;itmf&#47;type.cpp:290:5: warning: missing initializer for member ‘mp4v2::impl::itmf::{anonymous}::ImageHeader::data’ [-Wmissing-field-initializers]
     };

..&#47;media-server&#47;src&#47;stunmessage.cpp: In static member function ‘static STUNMessage* STUNMessage::Parse(uint8_t*, uint32_t)’:
..&#47;media-server&#47;src&#47;stunmessage.cpp:106:8: warning: variable ‘posMessageIntegrity’ set but not used [-Wunused-but-set-variable]
  DWORD posMessageIntegrity = 0;
        ^~~~~~~~~~~~~~~~~~~

&#47;root&#47;.node-gyp&#47;10.18.0&#47;include&#47;node&#47;openssl&#47;ssl.h:1895:45: note: declared here
 DEPRECATEDIN_1_1_0(__owur const SSL_METHOD *DTLSv1_method(void)) &#47;* DTLSv1.0 *&#47;
                                             ^
&#47;root&#47;.node-gyp&#47;10.18.0&#47;include&#47;node&#47;openssl&#47;.&#47;.&#47;archs&#47;linux-x86_64&#47;asm&#47;include&#47;openssl&#47;opensslconf.h:124:37: note: in definition of macro ‘DECLARE_DEPRECATED’
系统是 阿里云 Ubuntu 18.04
node v10.18.0
npm 6.4.1
老师，尝试了好几次，报了好多错。</div>2019-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/ac/c84fa0c3.jpg" width="30px"><span>Hadooper</span> 👍（0） 💬（3）<div>不管用ubuntu18还是centos7，用12的nodejs怎么编译都失败，完全没办法</div>2019-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/ce/a8c8b5e8.jpg" width="30px"><span>Jason</span> 👍（0） 💬（1）<div> 老师好，咱们搭建的medooze的demo能承担多少用户的负载？另外，sfu架构图有个别单词拼写错误，白璧微瑕^^</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/35/5e/7a584fed.jpg" width="30px"><span>accessory</span> 👍（0） 💬（2）<div>&#47;home&#47;toney&#47;source&#47;sfu&#47;lib&#47;Room.js:59
		this.activeSpeakerDetector = MediaServer.createActiveSpeakerDetector();
		                                         ^

TypeError: MediaServer.createActiveSpeakerDetector is not a function
    at new Room (&#47;home&#47;toney&#47;source&#47;sfu&#47;lib&#47;Room.js:59:44)
    at WebSocketServer.ws.on (&#47;home&#47;toney&#47;source&#47;sfu&#47;index.js:116:10)
    at WebSocketServer.emit (events.js:198:13)
    at WebSocketServer.handleUpgrade (&#47;home&#47;toney&#47;source&#47;sfu&#47;node_modules&#47;websocket&#47;lib&#47;WebSocketServer.js:213:14)
    at Server.emit (events.js:198:13)
    at onParserExecuteCommon (_http_server.js:553:14)
    at onParserExecute (_http_server.js:499:3)

按照课程中搭建了服务，使用浏览器访问服务，输入 roomid，name，点击 ready 按钮，sfu 就 crash 了，请问老师改如何解决</div>2019-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1a/e2/f88bf28f.jpg" width="30px"><span>frank</span> 👍（0） 💬（1）<div>不懂nodejs，大致看了下，应该是participant.on(&#39;stream&#39; 这边，但是stream怎么触发就不知道了</div>2019-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/60/20c6a3f2.jpg" width="30px"><span>expecting</span> 👍（1） 💬（0）<div>sfu.js里的有些方法已经废弃，需要更新才能跑起来
createEncodedVideoStreams --&gt; createEncodedStreams
forceEncodedVideoInsertableStreams --&gt; encodedInsertableStreams
readableStream --&gt; readable
writableStream --&gt; writable</div>2022-02-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLYibV8EBAIuJ2eO8KcElQmIbKWHBL96XodCgoKjmjcE9evmm6TzwvpdT9RLvdkDeea5ZoEPoibydibQ/132" width="30px"><span>夏天的水獭</span> 👍（0） 💬（0）<div>思考题答案是文章中所说的“这关键的一步是，当新参会人一切准备就绪后，服务端要发送广播消息（update） 通知所有已经在会中的其他人，有新用户进来了，需要重新进行媒体协商。只有重新媒体协商之后，其他参会人才能看到新入会人的音视频流。”的吗？</div>2024-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e5/e3/06aa87b5.jpg" width="30px"><span>强者之风</span> 👍（0） 💬（0）<div>李老师我确认一下，sfu demo，是不是npm install 就可以了， 不需要另外编译medooze-server-node，sfu依赖有medooze-server-node,npm install 会自动编译。</div>2022-01-25</li><br/><li><img src="" width="30px"><span>Geek_f6186b</span> 👍（0） 💬（0）<div>老师，您好，请问下为什么登录不上去了呢？？我按照您的要求都搭建成功了。可是就登录不上去哇，</div>2021-10-26</li><br/>
</ul>