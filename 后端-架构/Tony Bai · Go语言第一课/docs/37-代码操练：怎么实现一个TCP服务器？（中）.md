你好，我是Tony Bai。

上一讲中，我们讲解了解决Go语言学习“最后一公里”的实用思路，那就是“理解问题” -&gt; “技术预研与储备” -&gt; “设计与实现”的三角循环，并且我们也完成了“理解问题”和“技术预研与储备”这两个环节，按照“三角循环”中的思路，这一讲我们应该针对实际问题进行一轮设计与实现了。

今天，我们的目标是实现一个基于TCP的自定义应用层协议的通信服务端，要完成这一目标，我们需要建立协议的抽象、实现协议的打包与解包、服务端的组装、验证与优化等工作。一步一步来，我们先在程序世界建立一个对上一讲中自定义应用层协议的抽象。

## 建立对协议的抽象

程序是对现实世界的抽象。对于现实世界的自定义应用协议规范，我们需要在程序世界建立起对这份协议的抽象。在进行抽象之前，我们先建立这次实现要用的源码项目tcp-server-demo1，建立的步骤如下：

```plain
$mkdir tcp-server-demo1
$cd tcp-server-demo1
$go mod init github.com/bigwhite/tcp-server-demo1
go: creating new go.mod: module github.com/bigwhite/tcp-server-demo1
```
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/96/0cf9f3c7.jpg" width="30px"><span>Aeins</span> 👍（7） 💬（1）<div>几点疑问

1. 协议处理程序保证使用相同的字节序的情况下，有必要一定用大端序吗，改成小端序，也能成功。

2. TCP 保证顺序交付的，不指定字节序，顺序处理数据流可以吗。这时会有字节序问题吗，如果协议栈都使用同一种字节序呢。（我认为字节序和程序使用的字节序有关，如果每个程序都使用同一种字节序，那应该就不存在字节序问题了，比如本程序，收发都用相同的字节序处理，不知道这个结论对不对）

3. 协议头和协议体，分两次写入的，会不会有并发安全问题，为什么？这里应该没做到上节课说的，一次写入一个“业务包”吧。

4. 多次运行 client，错误偶发。有时 io.ReadFull 读不满数据，有时读取的数据长度不对，会是哪些原因导致的呢？</div>2022-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b5/e6/c67f12bd.jpg" width="30px"><span>左耳朵东</span> 👍（4） 💬（2）<div>client 代码中的 done chan 好像没必要吧，去掉它也能正常退出</div>2022-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/71/26/773e6dcb.jpg" width="30px"><span>枫</span> 👍（3） 💬（2）<div>&#47;&#47;
select {
		case &lt;-quit:
			done &lt;- struct{}{}
			return
		default:
}
老师，client中读取服务端返回响应的这个goroutine中，这段select的作用不是很理解，如果没有从quit中收到值就会一直轮询，但是从quit中收到值又会return，那下面的代码不是一直都没有机会执行了吗</div>2022-07-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKfYfHAvhZmsKiauxPAt9T2D7ntiaZrP8mial07CAdWiaCEJMawZwficjL3PFvZl35WM7D6ibcYf6miaERJQ/132" width="30px"><span>晚枫</span> 👍（2） 💬（2）<div>为什么totalLen指定了字节序，payload不需要指定吗？</div>2022-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（2） 💬（1）<div>还是老师实现的代码优雅，我们项目的这块代码是刚开始学 Go 时实现的，只能说可以用。但对比老师的实现，我觉得我们的代码可以好好优化一下了。</div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/51/d4/ca703443.jpg" width="30px"><span>张尘</span> 👍（1） 💬（1）<div>白老师好, 本节课受益颇多, 有点疑问, 还望有时间能够帮忙解答下:
frameCodec.Decode返回值是自定义数据结构FramePayload
packet.Decode的入参是[]byte
client&#47;server 代码中直接将FramePayload当做[]byte使用

frameCodec.Decode为什么要返回自定义数据结构FramePayload而不是[]byte呢? 是因为FramePayload的结构可能改变吗? FramePayload可能不是[]byte吗? FramePayload可能包含Packet之外的其它数据吗?
可是如果FramePayload的结构改变, 那client&#47;server 的代码中直接将FramePayload当做[]byte的用法不是就有问题了吗?</div>2022-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/0a/23/c26f4e50.jpg" width="30px"><span>Sunrise</span> 👍（1） 💬（1）<div>有个小疑问：
func (p *myFrameCodec) Encode(w io.Writer, framePayload FramePayload) error { 
  var f = framePayload
  ...
}
var f = framePayload 这个地方有必要重新定义一个 f 吗，直接使用 framePayload 会有什么问题？</div>2022-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/49/4a488f4c.jpg" width="30px"><span>农民园丁</span> 👍（1） 💬（1）<div>请问老师，framePayload, err := frameCodec.Decode(c)
以上代码中&quot;c&quot;是net.Conn 类型，
而frameCodec.Decode(io.Reader)的输入参数是io.Reader,
这两个为什么可以不一样？</div>2022-11-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/5JKZO1Ziax3Ky03noshpVNyEvZw0pUwjLcHrHRo1XNPKXdmCE88homb6ltA15CdVRnjzjgGs3Ex42CaDbeYzNuQ/132" width="30px"><span>Geek_25f93f</span> 👍（1） 💬（1）<div>老师，单元测试的代码是不是有点问题，就判断条件是if err == nil</div>2022-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0a/da/dcf8f2b1.jpg" width="30px"><span>qiutian</span> 👍（1） 💬（2）<div>
&#47;&#47; tcp-server-demo1&#47;packet&#47;packet.go

func Encode(p Packet) ([]byte, error) {
  var commandID uint8
  var pktBody []byte
  var err error

  switch t := p.(type) {
  case *Submit:
    commandID = CommandSubmit
    pktBody, err = p.Encode()
    if err != nil {
      return nil, err
    }
  case *SubmitAck:
    commandID = CommandSubmitAck
    pktBody, err = p.Encode()
    if err != nil {
      return nil, err
    }
  default:
    return nil, fmt.Errorf(&quot;unknown type [%s]&quot;, t)
  }
  return bytes.Join([][]byte{[]byte{commandID}, pktBody}, nil), nil
}
老师，这段代码的最后的 return bytes.Join(), nil这个在什么情况下回运行到呢?不是很理解</div>2022-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（1） 💬（1）<div>老师，Conn 和 ConnAck 要实现的话，请问从业务中来讲，一般会需要发送一些什么 Payload 呢？我看这里的例子没有他们也可以正常运行整个流程，是类似 需要认证的系统中的登录账号和密码 的这种内容吗？</div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/92/b609f7e3.jpg" width="30px"><span>骨汤鸡蛋面</span> 👍（1） 💬（2）<div>老师，一些rpc框架学习 http2 的stream概念，在connection与协议之间加了一个stream层， 这块主要抽象了啥，很想听一下老师的看法。 </div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/44/d5/ca522e83.jpg" width="30px"><span>爱吃胡萝卜</span> 👍（0） 💬（1）<div>老师这节课学完了，主要还是有一下几点困惑，烦请解答
1.关于大端小端小问题
网络字节是不是都是大端
而本地的的比如磁盘这种 默认的是小端

2. 关于命名规范
go语言通过大小写区分public和internel权限
那么这里我怎么通过命名去区分该类型具体是变量，还是结构体接口类型呢
有什么具体规范没有，因为之前接触的语言都是通过大小写区分变量和结构体固有次一问
我看代码里很多参数 都是以短字符命名，我接触到语言命名都是尽可能长，以做到望文知义，
以短字符命名这个符合go的编码规范吗

3. const 类型推断

const (
	CommonConn  = iota + 0x01
	CommonSumbit
)

const (
	CommonConnAck  = iota + 0x81
	CommonSumbitAck
)

编译器是如何识别它的具体类型的，因为这个字段最终会被encode所以有次一问 万一编译器识别成int型那编码就是失败了
我把它简单重构了一下

const (
	CommonConn uint8 = iota + 0x01
	CommonSumbit
)

const (
	CommonConnAck uint8 = iota + 0x81
	CommonSumbitAck
)</div>2023-11-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erZCyXaP2gbxwFHxvtnyaaF2Pyy5KkSMsk9kh7SJl8icp1CD6wicb6VJibiblGibbpDo6IuHrdST6AnWQg/132" width="30px"><span>Geek_1cc6d1</span> 👍（0） 💬（1）<div>怎么根据totalLength拆包的？</div>2023-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2d/df/4949b250.jpg" width="30px"><span>Six Days</span> 👍（0） 💬（1）<div>frame encode 的方法将数据编码与发送耦合在一起，在外界调用的时候无法直观的感受到消息发送，建议可以做下合理拆分，对体验消息发送与接收更容易理解</div>2023-03-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erwcUXd1YciaE2VmCRZUjbm0hscIAwvXJOQtibK2aor2DrmxxPszsfecZ11dibniakRSkMYrhp8ibsHWoA/132" width="30px"><span>zhu见见</span> 👍（0） 💬（1）<div>done 这个chan的意义是啥呢？为了让startClient 晚于内部的go func 执行完吗？</div>2023-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/56/4e/9291fac0.jpg" width="30px"><span>Jay</span> 👍（0） 💬（1）<div>func (p *myFrameCodec) Encode(w io.Writer, framePayload FramePayload) error { 
var f = framePayload 
var totalLen int32 = int32(len(framePayload)) + 4 
...
}
以上方法的第二行处有个疑问：

为什么要额外创建一个方法参数 framePayload 的拷贝 f 呢？直接使用 framePayload 传入 w.Write() 方法会有什么问题吗？</div>2022-09-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/x3gOkI2Dl1Gb3WRic44roicJMILgHfdFRic8nfR7oh0asf0KONEj7U2or6YHMmCcyibskvVE5Pjypz2ALGwBXRyMPA/132" width="30px"><span>中年编程人员</span> 👍（0） 💬（1）<div>老师你好，frame中，var totalLen int32 = int32(len(framePayload)) + 4；这个totalLen为啥要加4呢？？</div>2022-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/62/6f/8fb1a57b.jpg" width="30px"><span>南方虚心竹</span> 👍（0） 💬（1）<div>frame.go:  

func (p *myFrameCodec) Decode(r io.Reader) (FramePayload, error) {
    ...
    buf := make([]byte, totalLen-4)   &#47;&#47; 这行在运行的时候在跑的时候会panic 
   ...
}
&#47;&#47; panic: runtime error: makeslice: len out of range
打印出来是一个很大的负数

大概率会panic，小概率会pass，感觉是多线程下出现的问题

求老师解答一下
</div>2022-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/62/6f/8fb1a57b.jpg" width="30px"><span>南方虚心竹</span> 👍（0） 💬（1）<div>packet.go 中 Submit 映射的Decode方法 
第二行中使用 s.ID = string(pktBody[:8])  写法在运行client的时候和会出现 
panic: runtime error: makeslice: len out of range
修改为老师git当中的s.ID = string(pktBody[0:8]) 后可以正常运行。（我的环境是MacOS12-intelCPU）

想请教下老师这里的 pktBody[:8] 和 pktBody[0:8] 不是等价的吗？

&#47;&#47; 附上文章中的代码
func (s *Submit) Decode(pktBody []byte) error { 
    s.ID = string(pktBody[:8]) 
    s.Payload = pktBody[8:] 
    return nil
}</div>2022-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/23/5c74e9b7.jpg" width="30px"><span>$侯</span> 👍（0） 💬（3）<div>请问 data := []byte{0x0, 0x0, 0x0, 0x9, &#39;h&#39;, &#39;e&#39;, &#39;l&#39;, &#39;l&#39;, &#39;o&#39;} 中的0x0, 0x0, 0x0, 0x9代表的是什么意思</div>2022-04-26</li><br/><li><img src="" width="30px"><span>酒醒何处</span> 👍（0） 💬（1）<div>CommandConnAck = iota + 0x80 &#47;&#47; 0x81，连接请求的响应包
这儿应该是：
CommandConnAck = iota + 0x81 &#47;&#47; 0x81，连接请求的响应包</div>2022-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/49/4e/8798cd01.jpg" width="30px"><span>顷</span> 👍（0） 💬（1）<div>老师，Makefile的相关知识考虑在加餐要说下吗</div>2022-03-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ge7uhlEVxicQT73YuomDPrVKI8UmhqxKWrhtO5GMNlFjrHWfd3HAjgaSribR4Pzorw8yalYGYqJI4VPvUyPzicSKg/132" width="30px"><span>陈东</span> 👍（0） 💬（2）<div>老师能加餐一节单元测试吗？查很多资料，没有学到测试的入门。谢谢。</div>2022-01-27</li><br/>
</ul>