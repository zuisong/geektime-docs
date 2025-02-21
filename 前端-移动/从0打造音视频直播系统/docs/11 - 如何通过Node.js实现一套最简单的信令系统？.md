通过前面几篇文章的讲解，我想现在你应该已经对 WebRTC 有了一个清楚的认知了。接下来的章节咱们就使用 WebRTC 逐步实现一套真实可用的 1 对 1 实时直播系统吧。

WebRTC 1.0 规范对 WebRTC 要实现的功能、API 等相关信息做了大量的约束，比如规范中定义了如何采集音视频数据、如何录制以及如何传输等。甚至更细的，还定义了都有哪些 API，以及这些API 的作用是什么。但这些约束只针对于客户端，并没有对服务端做任何限制。

那WebRTC规范中为什么不对服务器也做约束呢？其实，这样做有以下三点好处。

- **第一点，可以集中精力将 WebRTC 库做好**。WebRTC的愿景是使浏览器能够方便地处理音视频相关的应用，规范中不限制服务端的事儿，可以使它更聚焦。
- **第二点，让用户更好地对接业务**。你也清楚，信令服务器一般都与公司的业务有着密切的关系，每家公司的业务都各有特色，让它们按照自已的业务去实现信令服务器会更符合它们的要求。
- **第三点，能得到更多公司的支持**。WebRTC扩展了浏览器的基础设施及能力，而不涉及到具体的业务或产品，这样会更容易得到像苹果、微软这种大公司的支持，否则这些大公司之间就会产生抗衡。

当然，这样做也带来了一些坏处，最明显的一个就是增加了学习 WebRTC 的成本，因为你在学习WebRTC的时候，必须**自己去实现信令服务器**，否则你就没办法让 WebRTC 运转起来，这确实增加了不少学习成本。
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoicwtj6x3l7NEcODqsXHjUTjzbl99pesNbydQUSfR6IywcKKyyaY9AIhBS0bCz3R8icMRIploDdUQA/132" width="30px"><span>花果山の酸梅汤</span> 👍（7） 💬（1）<div>client代码运行于浏览器渲染引擎中的V8引擎，server代码运行于Node.js的JS运行时的V8引擎部分。一个面向渲染一个面向提供后台服务。</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/cf/8b/2b4ef30f.jpg" width="30px"><span>天天</span> 👍（2） 💬（1）<div>老师，您在介绍node. js的Reactor模式时和我以往理解的有点出入。您说道有个线程池的概念，我的理解应该是没有的喔(虽然我们可以使用worker来创建）还请提点一下我呦，推我篇文章也行😁谢谢啦</div>2019-12-11</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJaCVXshyiclaBQpxvIWQknKdEeicJ6vv69ZsjPmlIa69Ba32kXe10Djk4kBjiap4j6yuicTA1xaptFfA/132" width="30px"><span>jike</span> 👍（2） 💬（2）<div>不懂 node 的小白
客户端运行报错 404  http:&#47;&#47;127.0.0.1:8000&#47;socket.io&#47;?EIO=3&amp;transport=polling&amp;t=MvPeDk4；
服务端运行没有任何输出 浏览器也访问不了</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/02/87/047259c9.jpg" width="30px"><span>Ethan</span> 👍（2） 💬（1）<div>客户端一定要引入socket. io吗？可以直接用 websocket api吗</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/c5/4f/0a1c7334.jpg" width="30px"><span>人生在事</span> 👍（1） 💬（3）<div>李老师，文章实例里客户端都没有指明连哪个端口，服务端怎么监听的啊？</div>2020-11-04</li><br/><li><img src="" width="30px"><span>宇宙之王</span> 👍（1） 💬（1）<div>老师好，有个问题不明白，socket = io.connect(); 没指定端口也能连接通吗？第一次接触node，废了半天劲，这章源码和课程不太一致，运行不了，安装各种node模块又把server.js 做了如下修改 暂时去掉了https和log4j，已部署到服务器测试，大家有调不通的先试试这个，有问题互相多沟通
&#39;use strict&#39;

var http = require(&#39;http&#39;);
var https = require(&#39;https&#39;);
var fs = require(&#39;fs&#39;);
var socketIo = require(&#39;socket.io&#39;);

var express = require(&#39;express&#39;);
var serveIndex = require(&#39;serve-index&#39;);

var USERCOUNT = 4;

var app = express();
app.use(serveIndex(&#39;.&#47;public&#39;));
app.use(express.static(&#39;.&#47;public&#39;));

&#47;&#47;http server
var http_server = http.createServer(app);
var io = socketIo.listen(http_server);

io.sockets.on(&#39;connection&#39;, (socket)=&gt; {

	socket.on(&#39;message&#39;, (room, data)=&gt;{
	    console.log(&#39;message, room: &#39; + room + &quot;, data, type:&quot; + data);
		socket.to(room).emit(&#39;message&#39;,room, data+&#39;from server!&#39;);
	});

	socket.on(&#39;join&#39;, (room)=&gt;{
		socket.join(room);
		var myRoom = io.sockets.adapter.rooms[room]; 
		var users = (myRoom)? Object.keys(myRoom.sockets).length : 0;
		console.log(&#39;the user number of room (&#39; + room + &#39;) is: &#39; + users);

		if(users &lt; USERCOUNT){
			socket.emit(&#39;joined&#39;, room, socket.id); &#47;&#47;发给除自己之外的房间内的所有人
			if(users &gt; 1){
				socket.to(room).emit(&#39;otherjoin&#39;, room, socket.id);
			}
		
		}else{
			socket.leave(room);	
			socket.emit(&#39;full&#39;, room, socket.id);
		}
	});

	socket.on(&#39;leave&#39;, (room)=&gt;{

		socket.leave(room);

		var myRoom = io.sockets.adapter.rooms[room]; 
		var users = (myRoom)? Object.keys(myRoom.sockets).length : 0;
		console.log(&#39;the user number of room is: &#39; + users);

		socket.to(room).emit(&#39;bye&#39;, room, socket.id);
		socket.emit(&#39;leaved&#39;, room, socket.id);
	});

});

http_server.listen(8080, &#39;0.0.0.0&#39;);



</div>2020-09-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eolBabicK5OTVJJJlUA4wwRtwCohCb75ahtbiaopsicnG3HRQTBOVEUrRY1KYCRZH78cDweQllh0Jzeg/132" width="30px"><span>like_wind</span> 👍（1） 💬（1）<div>没太理解老师说的这个房间的概念，文中提到的“房间概念”是指客户端和服务端的一个连接就是一个房间吗？还是说这个房间指的是业务上的某一个房间，比如说某直播平台的一个直播间?</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/97/d2/daaed7d8.jpg" width="30px"><span>dahaowenge</span> 👍（1） 💬（3）<div>node serves.js     Error: ENOENT: no such file or directory, open &#39;.&#47;cert&#47;1557605_www.learningrtc.cn.key&#39;</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/ce/a8c8b5e8.jpg" width="30px"><span>Jason</span> 👍（1） 💬（1）<div>老师好，问一下， 这套简单的信令系统，已经实现了交换各端sdp信息的功能了吗？</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（1） 💬（1）<div>两个不同的 V8 引擎上，你知道它们的对应关系吗
一个是nodejs服务端的V8，一个是浏览器中客户端的V8。</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/c5/4f/0a1c7334.jpg" width="30px"><span>人生在事</span> 👍（0） 💬（1）<div>&lt;script src=&#39;&#47;socket.io&#47;socket.io.js&#39;&gt;&lt;&#47;script&gt;这段代码没看到，李老师。第一次接触nodejs和socket.io.js，不太明白，希望指导一下
</div>2020-11-04</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJoNVHqRL5iatEoMgfFAaGFZxD8ic6CicxKI9Facp4bzAkNMAfaduSENlPOafs6dOGawibhNv3V9lVowQ/132" width="30px"><span>SherwinFeng</span> 👍（0） 💬（2）<div>老师，我运行了github上的demo，遇到了一个问题：
client端不能显示发送出去的消息
已尝试的排查：
①查看了日志发现client发送的消息服务器端已经接收到了，并且显示了消息内容（这里自己修改了demo中的debug信息，以便记录消息内容，原demo只能显示data.type）
②F12调试时发现client.js中的监听“message”事件没有执行
这是什么原因造成呢？</div>2020-01-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Cyuxk6Ej9B5G9icGd2h9OiclVzDNYLvYUME62sUk2UMcvfVINEvNYHBWyJUicfiahG86xgYmbdeVNQ3eRZr6yNdGcw/132" width="30px"><span>Geek_r2sfwe</span> 👍（0） 💬（2）<div>老师你好，我下载了您的代码，更改了cert，但是报了一个错误，我不知道怎么解决
 node server.js 
&#47;root&#47;node_modules&#47;streamroller&#47;lib&#47;RollingFileWriteStream.js:133
  async _shouldRoll() {
        ^^^^^^^^^^^

SyntaxError: Unexpected identifier
    at createScript (vm.js:56:10)
    at Object.runInThisContext (vm.js:97:10)
    at Module._compile (module.js:549:28)
    at Object.Module._extensions..js (module.js:586:10)
    at Module.load (module.js:494:32)
    at tryModuleLoad (module.js:453:12)
    at Function.Module._load (module.js:445:3)
    at Module.require (module.js:504:17)
    at require (internal&#47;module.js:20:19)
    at Object.&lt;anonymous&gt; (&#47;root&#47;node_modules&#47;streamroller&#47;lib&#47;index.js:2:27)

是我的环境有问题么</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/1a/389eab84.jpg" width="30px"><span>而立斋</span> 👍（0） 💬（2）<div>跑起来报啦个错误，页面显示Cannot GET </div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/97/d2/daaed7d8.jpg" width="30px"><span>dahaowenge</span> 👍（0） 💬（1）<div>老师，用的是官方demo，但是运行node server.js时，报错  Error: Cannot find module &#39;log4js&#39;</div>2019-10-10</li><br/><li><img src="" width="30px"><span>Geek_leo长沙</span> 👍（0） 💬（2）<div>老师，要做多短在线音视频的话是不是就得考虑mesh,router,mix这三种架构呢。</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/45/6c/3393668d.jpg" width="30px"><span>小狂</span> 👍（0） 💬（1）<div>老师,是否能发一下这节的代码</div>2019-08-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/sIfDHQxDV6iaanrd8PcdVWZnke6nJmqBOLMx0iazR1yNN3FI6ib7PtXCfzicWcuEwSIqzfqiaFMf7PMYNPiaRibiaFHgcw/132" width="30px"><span>hao11111205</span> 👍（0） 💬（1）<div>老师，启动服务，报错，什么原因？
hao@hao-Aspire-4820TG:~$ node server.js
&#47;home&#47;hao&#47;node_modules&#47;debug&#47;src&#47;node.js:165
	const (namespace: name, useColors) = this;
	                ^

SyntaxError: Unexpected token :
    at exports.runInThisContext (vm.js:53:16)
    at Module._compile (module.js:374:25)
    at Object.Module._extensions..js (module.js:417:10)
    at Module.load (module.js:344:32)
    at Function.Module._load (module.js:301:12)
    at Module.require (module.js:354:17)
    at require (internal&#47;module.js:12:17)
    at Object.&lt;anonymous&gt; (&#47;home&#47;hao&#47;node_modules&#47;debug&#47;src&#47;index.js:9:19)
    at Module._compile (module.js:410:26)
    at Object.Module._extensions..js (module.js:417:10)
</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a8/54/06da255b.jpg" width="30px"><span>Beast-Of-Prey</span> 👍（0） 💬（2）<div>老师 http:&#47;&#47;file&#47;socket.io&#47;?EIO=3&amp;transport=polling&amp;t=MnpuVBE net::ERR_NAME_NOT_RESOLVED 这个错误是什么原因导致的？我百度了 说是浏览器设置了代理，但是我检查我的浏览器，没有进行设置啊。</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a8/54/06da255b.jpg" width="30px"><span>Beast-Of-Prey</span> 👍（0） 💬（1）<div>老师  我按步骤安装了 socket.io 但是 我本地 html 加载 socket.io.js文件的时候 提示2 个错误，1、文件未发现ERR_FILE_NOT_FOUND，2、io 未定义 io is not defined。</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a8/54/06da255b.jpg" width="30px"><span>Beast-Of-Prey</span> 👍（0） 💬（1）<div>读了好几遍 </div>2019-08-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIDMOwpv5uMgy4HhoS0VPczxfXQldueafaaq2hznQx51nxZung0kYWukicNP3a3MFrhguVrjBwlwAg/132" width="30px"><span>彭刚</span> 👍（0） 💬（1）<div>期待更新 每篇文章都能看好几次 都是精华</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/fd/59/7f653e69.jpg" width="30px"><span>no ne</span> 👍（2） 💬（0）<div>最新的版本的socket.io会有不兼容问题(如服务器代码里的socketIo.listen(https_server)会报错)</div>2021-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/63/1b/83ac7733.jpg" width="30px"><span>忧天小鸡</span> 👍（1） 💬（0）<div>这client对不懂前端的人来说，完全跑不起来</div>2022-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3c/58/81307481.jpg" width="30px"><span>bohao</span> 👍（1） 💬（1）<div>新版本的 socket.io 代码需要修改下，比如 io.sockets.adapter.rooms[room] 是个 Map&lt;String, Set&lt;String&gt;&gt;</div>2021-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/b7/d2/2cab8598.jpg" width="30px"><span>里脊</span> 👍（0） 💬（0）<div>这节课就是实现了一个 socket 服务器吗？怎么交换 webrtc 信息没有说🤔</div>2025-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/92/44/8a803da1.jpg" width="30px"><span>小明</span> 👍（0） 💬（0）<div>请问这个课程还在维护吗？这节课的代码好像不能运行。
server.js 服务端运行后，然后打开index.html，点击‘connect&#39;没有任何的打印，没有’join‘这些变化</div>2024-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/14/57cb7926.jpg" width="30px"><span>ShawnWu</span> 👍（0） 💬（1）<div>server能用node跑起来，但是client没有监听任何websockt地址，应该咋样建联呢，没搞清楚怎么跑起来客户端</div>2023-11-30</li><br/>
</ul>