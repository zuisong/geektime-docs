你好，我是王昊天。

在多年的电脑使用经历中，你肯定经历过这种画面：

下载了官方软件却没有正版授权，于是千辛万苦找到一个破解软件，但是在运行破解软件时不断被杀毒软件拦截，一怒之下你把杀毒软件关闭了，随着破解软件的成功消息弹出，你露出了满意的微笑……

3天后你的电脑由于病毒感染无法开机了。

这是一种很典型的场景——为了某些临时性的操作破坏了权限边界，进而导致安全问题的发生。其实，**除了临时性的操作，还有很多权限安全问题是长期性的**，可能是配置原因、也可能是代码原因，接下来就让我们来一起探究。

## 权限不合理

**权限不合理简单来说，是不合理的权限赋予、权限处理以及权限管理过程**。这里所说的权限，指的是终端角色的一种属性。那么什么是终端角色呢？你可以理解为，用户就是一个终端角色。

与权限相关的赋予、处理以及管理过程，我们主要通过权限管理来统一实现。权限管理就是能够赋予终端执行某种特殊操作的权利，比如在某些运维场景下，运维人员能够获得系统维护的权限，这其中就包括重启服务器权限——我们都知道服务器重启可不是常规操作权限。

**接下来我们以运行时权限过高为例，来看几种典型的攻击场景。**

应用软件在执行某些操作时可能会获取过高的权限，这就可能会破坏我们之前课程中提到的最小权限原则，如果因为这种原因导致了提权漏洞的发生，就可能会放大其他安全风险，导致严重后果。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>可以讲讲最近log4j的漏洞吗？为了不打乱课程计划，可以以加餐的形式来讲，</div>2021-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/7e/73/a5d76036.jpg" width="30px"><span>DoHer4S</span> 👍（0） 💬（2）<div>老师您好，在MiTuan中执行您上边的代码，返回 400 Bad Request 错误；
尝试在 URL 中访问路径 `&#47;cgi-bin` 返回404；
请问是哪里出问题呢？</div>2021-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/18/e6367c6f.jpg" width="30px"><span>空间探索</span> 👍（0） 💬（2）<div>MiTuan 上对应这个CVE 的靶机 返回的信息是 
&lt;html&gt;
&lt;head&gt;&lt;title&gt;400 Bad Request&lt;&#47;title&gt;&lt;&#47;head&gt;
&lt;body&gt;
&lt;center&gt;&lt;h1&gt;400 Bad Request&lt;&#47;h1&gt;&lt;&#47;center&gt;
&lt;hr&gt;&lt;center&gt;openresty&#47;1.17.8.2&lt;&#47;center&gt;
&lt;&#47;body&gt;
&lt;&#47;html&gt;

感觉靶机不对吧</div>2021-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9a/e7/310b4a12.jpg" width="30px"><span>波动星球</span> 👍（0） 💬（1）<div>CVE-2021-42013 Mituan中 搜不到 </div>2021-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b3/c5/38439724.jpg" width="30px"><span>南瓜不胡闹</span> 👍（0） 💬（0）<div>42013验证成功，在mituan上的那个靶场有flag可以获取提交么</div>2022-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b3/c5/38439724.jpg" width="30px"><span>南瓜不胡闹</span> 👍（0） 💬（0）<div>测试为什么返回的是408报错呢

HTTP&#47;1.1 408 Request Timeout
Date: Sat, 08 Oct 2022 10:49:48 GMT
Server: Apache&#47;2.4.50 (Unix)
Content-Length: 221
Connection: close
Content-Type: text&#47;html; charset=iso-8859-1

&lt;!DOCTYPE HTML PUBLIC &quot;-&#47;&#47;IETF&#47;&#47;DTD HTML 2.0&#47;&#47;EN&quot;&gt;
&lt;html&gt;&lt;head&gt;
&lt;title&gt;408 Request Timeout&lt;&#47;title&gt;
&lt;&#47;head&gt;&lt;body&gt;
&lt;h1&gt;Request Timeout&lt;&#47;h1&gt;
&lt;p&gt;Server timeout waiting for the HTTP request from the client.&lt;&#47;p&gt;
&lt;&#47;body&gt;&lt;&#47;html&gt;</div>2022-10-08</li><br/>
</ul>