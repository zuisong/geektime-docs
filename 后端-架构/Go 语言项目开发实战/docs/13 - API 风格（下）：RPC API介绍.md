你好，我是孔令飞。这一讲，我们继续来看下如何设计应用的API风格。

上一讲，我介绍了REST API风格，这一讲我来介绍下另外一种常用的API风格，RPC。在Go项目开发中，如果业务对性能要求比较高，并且需要提供给多种编程语言调用，这时候就可以考虑使用RPC API接口。RPC在Go项目开发中用得也非常多，需要我们认真掌握。

## RPC介绍

根据维基百科的定义，RPC（Remote Procedure Call），即远程过程调用，是一个计算机通信协议。该协议允许运行于一台计算机的程序调用另一台计算机的子程序，而程序员不用额外地为这个交互作用编程。

通俗来讲，就是服务端实现了一个函数，客户端使用RPC框架提供的接口，像调用本地函数一样调用这个函数，并获取返回值。RPC屏蔽了底层的网络通信细节，使得开发人员无需关注网络编程的细节，可以将更多的时间和精力放在业务逻辑本身的实现上，从而提高开发效率。

RPC的调用过程如下图所示：

![](https://static001.geekbang.org/resource/image/98/1d/984yy094616b9b24193b22a1f2f2271d.png?wh=2521x1671)

RPC调用具体流程如下：

1. Client通过本地调用，调用Client Stub。
2. Client Stub将参数打包（也叫Marshalling）成一个消息，然后发送这个消息。
3. Client所在的OS将消息发送给Server。
4. Server端接收到消息后，将消息传递给Server Stub。
5. Server Stub将消息解包（也叫 Unmarshalling）得到参数。
6. Server Stub调用服务端的子程序（函数），处理完后，将最终结果按照相反的步骤返回给 Client。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（70） 💬（1）<div>假定希望用RPC作为内部API的通讯，同时也想对外提供RESTful API，又不想写两套，可以使用gRPC Gateway 插件，在生成RPC的同时也生成RESTful web  server。</div>2021-06-24</li><br/><li><img src="" width="30px"><span>Geek_e7af5e</span> 👍（43） 💬（4）<div>这里提供一些更新说明（刚踩过的坑）
github.com&#47;golang&#47;protobuf&#47;protoc-gen-go和google.golang.org&#47;protobuf&#47;cmd&#47;protoc-gen-go是不同的。区别在于前者是旧版本（操作类似于作者大大的），后者是google接管后的新版本，他们之间的API是不同的，也就是说用于生成的命令，以及生成的文件都是不一样的。因为目前的gRPC-go源码中的example用的是后者的生成方式，所以这里提供后者说明：
1. 首先需要安装两个库：
go install google.golang.org&#47;protobuf&#47;cmd&#47;protoc-gen-go
go install google.golang.org&#47;grpc&#47;cmd&#47;protoc-gen-go-grpc
2. 然后.proto文件保持一致，输入两个生成代码命令：
protoc -I. --go_out=$GOPATH&#47;src helloworld.proto
protoc -I. --go-grpc_out=$GOPATH&#47;src helloworld.proto
3. 上述两个命令会生成两个文件：
helloworld.pb.go      helloworld_grpc.pb.go
这两个文件分别生成message和service的代码，合起来就是老版本的代码

这是排查了两小时的坑，希望大家注意！</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/15/9b/9ce9f374.jpg" width="30px"><span>柠柠</span> 👍（16） 💬（1）<div>RPC 与 RESTful 共通逻辑抽象出来 Service 层，RPC server 和 RESTful server 初始化or 启动时时都需要指定 service，真正提供服务的是 Service 层</div>2021-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/68/d4/c9b5d3f9.jpg" width="30px"><span>💎A</span> 👍（10） 💬（1）<div>https:&#47;&#47;www.bookstack.cn&#47;read&#47;API-design-guide&#47;API-design-guide-04-%E6%A0%87%E5%87%86%E6%96%B9%E6%B3%95.md  我又来做贡献了</div>2021-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3e/89/77829168.jpg" width="30px"><span>fliyu</span> 👍（6） 💬（1）<div>想方便调用grpc，可以使用grpcurl和grpcui，基于反射的方式使用</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/9a/52/93416b65.jpg" width="30px"><span>不明真相的群众</span> 👍（6） 💬（1）<div>你有一个 gRPC 服务，但是却希望该服务同时也能提供 RESTful API 接口，这该如何实现？
---------------------------
在封装一层？</div>2021-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ed/0a/18201290.jpg" width="30px"><span>Juniper</span> 👍（4） 💬（2）<div>查了下文档，optional是protoco 3.12版本加入的，如果参数设置成optional，执行时必须要带--experimental_allow_proto3_optional。但是我是3.15.8版本，执行时没有加上--experimental_allow_proto3_optional也没有报错</div>2021-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/f1/ce10759d.jpg" width="30px"><span>wei 丶</span> 👍（4） 💬（2）<div>老师有个疑问
protoc --go_out=. *.proto
protoc --go_out=plugins=grpc:. *.proto
这俩有啥啥区别  😵</div>2021-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/59/d0f326e7.jpg" width="30px"><span>张名哲</span> 👍（4） 💬（1）<div>老师，文章中有四种模式，平时用的最多的是哪一种模式？</div>2021-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a9/93/2a26fe6e.jpg" width="30px"><span>learner2021</span> 👍（3） 💬（4）<div>哪里设置错误了？
[going@dev server]$ pwd
&#47;home&#47;going&#47;workspace&#47;golang&#47;src&#47;github.com&#47;marmotedu&#47;gopractise-demo&#47;apistyle&#47;greeter&#47;server
[going@dev server]$ go run main.go
main.go:8:2: no required module provides package github.com&#47;marmotedu&#47;gopractise-demo&#47;apistyle&#47;greeter&#47;helloworld: go.mod file not found in current directory or any parent directory; see &#39;go help modules&#39;
main.go:9:2: no required module provides package google.golang.org&#47;grpc: go.mod file not found in current directory or any parent directory; see &#39;go help modules&#39;</div>2021-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/97/39/1f5c6350.jpg" width="30px"><span>朱元彬🗿</span> 👍（2） 💬（1）<div>生产环境中，使用服务提供者的接口，如果遇到接口更新的情况，要怎么跟服务提供者沟通更新协议呢？</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/14/e2/f6f1627c.jpg" width="30px"><span>顺势而为</span> 👍（2） 💬（1）<div>建议作者的命令行，多点pwd，方便我们定位</div>2022-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/34/84/27ecfcab.jpg" width="30px"><span>江湖夜雨十年灯</span> 👍（2） 💬（2）<div>老师，我的proto文件是这样写的，go_package用的是我本地项目的目录：
option go_package = &quot;whw_scripts_stroage&#47;a_grpc_tests&#47;helloworld&quot;;
在helloworld目录中执行下面命令：
sudo protoc -I. --go_out=. .&#47;helloworld.proto 
但是最后在helloworld目录中，与helloworld.proto文件同一个级别生成的不是helloworld.pb.go，而是：whw_scripts_stroage&#47;a_grpc_tests&#47;helloworld.pb.go
请问为什么生成的是目录加go文件呢？



</div>2021-10-22</li><br/><li><img src="" width="30px"><span>andox</span> 👍（2） 💬（1）<div>grpc有推荐的服务治理方案吗</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/14/e2/f6f1627c.jpg" width="30px"><span>顺势而为</span> 👍（1） 💬（2）<div>对protoc为什么生成.pb.go的函数，不是很理解。</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/96/3a/e06f8367.jpg" width="30px"><span>HiNeNi</span> 👍（1） 💬（1）<div>请问老师怎么看待tars？什么情况下用tars会比用grpc好一点？</div>2022-06-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/rSzzqGwHcvhwPejiaPsCY9XBX7ib7zTxJ6cUDORdhGIakX8dTPVsz6ibud5ec1FeWQGTseF2TPRECCjky5JMlHvDg/132" width="30px"><span>Struggle~honor</span> 👍（1） 💬（1）<div>老师，看代码是使用了grpc中的invoke函数，指定URL，请问这个是怎样用的呢</div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b5/e6/c67f12bd.jpg" width="30px"><span>左耳朵东</span> 👍（1） 💬（1）<div>为什么我执行这个命令的时候 protoc --go_out=plugins=grpc:. helloworld.proto 报错：
--go_out: protoc-gen-go: plugins are not supported; use &#39;protoc --go-grpc_out=...&#39; to generate gRPC</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/64/272dc1b7.jpg" width="30px"><span>圆滚滚</span> 👍（1） 💬（2）<div>protoc-gen-go: program not found or is not executable
Please specify a program using absolute path or make sure the program is available in your PATH system variable
--go_out: protoc-gen-go: Plugin failed with status code </div>2021-12-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/rSzzqGwHcvhwPejiaPsCY9XBX7ib7zTxJ6cUDORdhGIakX8dTPVsz6ibud5ec1FeWQGTseF2TPRECCjky5JMlHvDg/132" width="30px"><span>Struggle~honor</span> 👍（1） 💬（1）<div>老师，请问grpc数据结构中的 1 2 3 4 这些定义分别代表什么意思呢</div>2021-12-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJkOj8VUxLjDKp6jRWJrABnnsg7U1sMSkM8FO6ULPwrqNpicZvTQ7kwctmu38iaJYHybXrmbusd8trg/132" width="30px"><span>yss</span> 👍（1） 💬（2）<div>不知道老师有没有跨语言，跨处理器平台做 gRPC 开发的经验。

开发机是 windows + x86 
目标机是 Linux + arm

希望实现 golang 与 QT 的 gRPC 通讯。并想在开发机直接构建完成后到目标机执行。这个思路对于 c++ 程序是不是不可行，编译还是必须在对应的平台？</div>2021-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（1） 💬（1）<div>以前用过Thrift，当时选用它的原因是与gRPC相比支持的编程语言比较多。不知道现在两者哪个更强一些？</div>2021-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/37/92/961ba560.jpg" width="30px"><span>授人以🐟，不如授人以渔</span> 👍（1） 💬（2）<div>孔老师，请问：「在描述 Protocol Buffer 时，谈到的第一个特征相对于 JSON&#47;XML “节省了大量的 IO 操作”，这一点不理解！」我的理解是这样的：JSON&#47;XML，或者是 Protobuf 都是需要转化为二进制数据，但后者数据量小。正因为数据量小，减少了底层网络数据传输的 IO。我可以这样理解吗？</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（1） 💬（2）<div>一文搞懂rpc，这个周末写一下demo。周日晚上再来打卡。</div>2021-08-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoeNMibYsgHBsbhIwf9YR4Shy6psfqiblneVHA5CYrBRoqJwkw1ZUbVAPRGAfFfWjia7MZlDZzddeE2w/132" width="30px"><span>wfatec</span> 👍（1） 💬（2）<div>我这里遇到个问题，我在&#47;workspace&#47;greeter&#47;helloworld&#47;下新建了一个helloworld.proto文件，并cd到当前目录执行：
protoc --go_out=plugins=grpc:$GOPATH&#47;src helloworld.proto
之后，helloworld.pb.go 并不会在当前目录生成，查看:$GOPATH&#47;src之后，发现多了个 home 文件夹，最终发现，helloworld.pb.go 生成的位置是$GOPATH&#47;src&#47;home&#47;username&#47;workspace&#47;greeter&#47;helloworld&#47;helloworld.pb.go下，请问这个是为什么呢？</div>2021-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a7/b2/274a4192.jpg" width="30px"><span>漂泊的小飘</span> 👍（1） 💬（1）<div>老师，有两个问题请教下：
1，能否讲下四种模式的应用场景？
2，一般生成的文件需要放进git里面吗</div>2021-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/fc/0e887697.jpg" width="30px"><span>kkgo</span> 👍（1） 💬（1）<div>老师有对比过grpc和rpcx之间的性能，稳定性方面不? 看官方说明rpcx性能是grpc的2倍</div>2021-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e2/c7/3e1d396e.jpg" width="30px"><span>oneWalker</span> 👍（0） 💬（1）<div>为何我用protoc自动生成的文件和作者的完全不一样：
自动生成的代码如链接：【腾讯文档】13  API 风格（下）RPC API介绍-protobuf自动生成文件
https:&#47;&#47;docs.qq.com&#47;doc&#47;DS3Nmc1dqRmFkSVZT
</div>2021-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/c1/84/c4ddaddd.jpg" width="30px"><span>Star°时光℡</span> 👍（0） 💬（3）<div>protoc -I. --go_out=plugins=grpc:$GOPATH&#47;src helloworld.proto
执行命令后无任何输出，也没有产生helloworld.pb.go文件</div>2021-06-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJl2cs8X08aK8GiaUYcH0V2L7QJ14Y1YCfjT42Ta3CwnJEczVvwsAOA1InCNg5PqUuCCTEda287PYg/132" width="30px"><span>Bradford</span> 👍（3） 💬（0）<div>postman现在也支持grpc啦</div>2022-04-20</li><br/>
</ul>