你好，我是孔令飞。接下来的两讲，我们来看下如何设计和实现一个优秀的Go SDK。

后端服务通过API接口对外提供应用的功能，但是用户直接调用API接口，需要编写API接口调用的逻辑，并且需要构造入参和解析返回的数据包，使用起来效率低，而且有一定的开发工作量。

在实际的项目开发中，通常会提供对开发者更友好的SDK包，供客户端调用。很多大型服务在发布时都会伴随着SDK的发布，例如腾讯云很多产品都提供了SDK：

![图片](https://static001.geekbang.org/resource/image/e1/fa/e1bb8eb03c2f26f546710e95751c17fa.png?wh=1920x747)

既然SDK如此重要，那么如何设计一个优秀的Go SDK呢？这一讲我就来详细介绍一下。

## 什么是SDK？

首先，我们来看下什么是SDK。

对于SDK（Software Development Kit，软件开发工具包），不同场景下有不同的解释。但是对于一个Go后端服务来说，SDK通常是指**封装了Go后端服务API接口的软件包**，里面通常包含了跟软件相关的库、文档、使用示例、封装好的API接口和工具。

调用SDK跟调用本地函数没有太大的区别，所以可以极大地提升开发者的开发效率和体验。SDK可以由服务提供者提供，也可以由其他组织或个人提供。为了鼓励开发者使用其系统或语言，SDK通常都是免费提供的。

通常，服务提供者会提供不同语言的SDK，比如针对Python开发者会提供Python版的SDK，针对Go开发者会提供Go版的SDK。一些比较专业的团队还会有SDK自动生成工具，可以根据API接口定义，自动生成不同语言的SDK。例如，Protocol Buffers的编译工具protoc，就可以基于Protobuf文件生成C++、Python、Java、JavaScript、PHP等语言版本的SDK。阿里云、腾讯云这些一线大厂，也可以基于API定义，生成不同编程语言的SDK。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/25/06/13/e4f9f79b.jpg" width="30px"><span>你赖东东不错嘛</span> 👍（8） 💬（1）<div>Q1:构建Request时将API版本作为可选参数传入</div>2021-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（6） 💬（2）<div>老师讲的太好了，
请教老师一个问题：
sdk中 日志应该如何设计比较好，
我看 阿里云是 默认了一个实现，用的标准log。
这样好吗， 如果用户使用的是  zap，那是不是得分文件，用同一个文件会不会冲突。
感觉都不优雅</div>2021-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3e/89/77829168.jpg" width="30px"><span>fliyu</span> 👍（4） 💬（1）<div>openapi-generator是个非常不错的项目：https:&#47;&#47;github.com&#47;openapitools&#47;openapi-generator，支持生成几十种客户端语言，安装简单，使用简单，生成的代码质量高，还有特别详细的markdown使用文档，超级推荐</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（2） 💬（1）<div>总结：
SDK的命名规范、目录结构、以及各个云厂商的逻辑架构。
云厂商的SDK的实现分为两层：API层和基础层。
API 层实现一个Client对象，每个方法对应了一个API接口
基础层：主要负责，请求的Marshall、Unmarshal、签名等功能。
API 层的 Client 通过匿名的方式继承了基础层的 Client。</div>2021-12-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKotsBr2icbYNYlRSlicGUD1H7lulSTQUAiclsEz9gnG5kCW9qeDwdYtlRMXic3V6sj9UrfKLPJnQojag/132" width="30px"><span>ppd0705</span> 👍（2） 💬（1）<div>云厂商python版本sdk感觉代码质量ucloud最好</div>2021-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9b/e5/bd0be5c3.jpg" width="30px"><span>⁶₆⁶₆⁶₆</span> 👍（2） 💬（1）<div>你讲义里面提供的客户端调用示例执行失败了，也就是你https:&#47;&#47;github.com&#47;marmotedu&#47;medu-sdk-go里面提供的那个示例代码，错误提示如下，提示找不到对应的包，但是明明已经拉下来了呀，没看出原因，希望大佬能解答下。

[root@dev sdk]# go mod init sdk
go: creating new go.mod: module sdk
go: to add module requirements and sums:
        go mod tidy
[root@dev sdk]# go mod tidy
go: finding module for package github.com&#47;marmotedu&#47;medu-sdk-go&#47;services&#47;iam
go: finding module for package github.com&#47;marmotedu&#47;medu-sdk-go&#47;sdk
go: finding module for package github.com&#47;ory&#47;ladon
go: found github.com&#47;marmotedu&#47;medu-sdk-go&#47;sdk in github.com&#47;marmotedu&#47;medu-sdk-go v1.0.0
go: found github.com&#47;ory&#47;ladon in github.com&#47;ory&#47;ladon v1.2.0
go: finding module for package github.com&#47;marmotedu&#47;medu-sdk-go&#47;services&#47;iam
sdk imports
        github.com&#47;marmotedu&#47;medu-sdk-go&#47;services&#47;iam: module github.com&#47;marmotedu&#47;medu-sdk-go@latest found (v1.0.0), but does not contain package github.com&#47;marmotedu&#47;medu-sdk-go&#47;services&#47;iam
[root@dev sdk]#
[root@dev sdk]# ll &#47;root&#47;workspace&#47;golang&#47;pkg&#47;mod&#47;github.com&#47;marmotedu&#47;
total 8
dr-xr-xr-x  6 root root  185 Sep 16 01:16 api@v1.0.1
dr-xr-xr-x  3 root root  138 Sep 25 17:48 component-base@v0.0.2
dr-xr-xr-x  3 root root  138 Sep 22 22:43 component-base@v1.0.0
dr-xr-xr-x  3 root root  138 Sep 16 01:16 component-base@v1.0.1
dr-xr-xr-x  2 root root 4096 Sep 22 22:43 errors@v0.0.1
dr-xr-xr-x  2 root root 4096 Sep 16 01:16 errors@v1.0.2
dr-xr-xr-x 18 root root  257 Sep 15 22:57 gopractise-demo@v0.0.1
dr-xr-xr-x  5 root root  261 Sep 16 01:16 log@v0.0.1
dr-xr-xr-x  8 root root  233 Sep 16 01:18 marmotedu-sdk-go@v1.0.2-0.20210528170801-2c91b80cb4cf
dr-xr-xr-x  5 root root  112 Sep 25 17:48 medu-sdk-go@v1.0.0
[root@dev sdk]#
</div>2021-09-25</li><br/><li><img src="" width="30px"><span>Geek_d71d64</span> 👍（0） 💬（1）<div>sdk的api和前端网页的api如何区分开来呢？</div>2022-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/6b/af7c7745.jpg" width="30px"><span>tiny🌾</span> 👍（0） 💬（1）<div>前端比如安卓的sdk也是这个设计思路吗</div>2022-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/0a/e4/c576d62b.jpg" width="30px"><span>阿波罗尼斯圆</span> 👍（0） 💬（2）<div>doc.go是干啥的</div>2022-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（2） 💬（0）<div>sdk为服务使用方提供了方便的同时，也为服务提供方省去很多不必要的沟通培训成本。
文中介绍了go sdk的目录结构，架构和云厂商常用的设计实现方案。</div>2021-08-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/iaxgvyIjNFomptQ9qBk4iaakYOS1XojYHDp48TXt1kX9DxTkKuR2UXGTyhG1liahib6E4BLF12ia6mic2pF0t4ECeZIQ/132" width="30px"><span>Joeforfun</span> 👍（1） 💬（8）<div>很赞，准备给没有go-sdk的某云厂商写个简单的demo</div>2021-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/20/ca/2b0f69bc.jpg" width="30px"><span>SmartsYoung</span> 👍（0） 💬（0）<div>doSend 方法中 err = sign(req)  这个函数调用没有看懂，SignFunc 是 func(*http.Request) error 的别名，但这个函数只定义，并没有实现啊，这样调用的目的是什么呢？</div>2024-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/9e/f8/f9f06e3e.jpg" width="30px"><span>@噜咪啦</span> 👍（0） 💬（0）<div>func (v1 SignatureV1) Sign(serviceName string, r *http.Request, body io.ReadSeeker) http.Header {
  tokenString := auth.Sign(v1.Credentials.SecretID, v1.Credentials.SecretKey, &quot;medu-sdk-go&quot;, serviceName+&quot;.marmotedu.com&quot;)
  r.Header.Set(&quot;Authorization&quot;, fmt.Sprintf(&quot;Bearer %s&quot;, tokenString))
  return r.Header

}
我的理解，这段是签发token的代码吗，为什么SDK里会有这个代码啊，不应该在服务端签发token吗</div>2023-09-24</li><br/>
</ul>