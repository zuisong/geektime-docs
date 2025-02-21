你好，我是郑建勋。

这节课，让我们将Worker节点变为一个支持GRPC与HTTP协议访问的服务，让它最终可以被Master服务和外部服务直接访问。在Worker节点上线之后，我们还要将Worker节点注册到服务注册中心。

## GRPC与Protocol buffers

一般要在微服务中进行远程通信，会选择 [GRPC](https://grpc.io/) 或RESTful风格的协议。我们之前就提到过，GRPC的好处包括：

- 使用了HTTP/2传输协议来传输序列化后的二进制信息，让传输速度更快；
- 可以为不同的语言生成对应的Client库，让外部访问非常便利；
- 使用 Protocol Buffers 定义API的行为，提供了强大的序列化与反序列化能力；
- 支持双向的流式传输（Bi-directional streaming）。

GRPC默认使用 Protocol buffers 协议来定义接口，它有如下特点：

- 它提供了与语言、框架无关的序列化与反序列化的能力；
- 它序列化生成的字节数组比JSON更小，同时序列化与反序列化的速度也比JSON更快；
- 有良好的向后和向前兼容性。

Protocol buffers 将接口语言定义在以 .proto为后缀的文件中，之后 proto 编译器结合特定语言的运行库生成特定的SDK。这个SDK文件有助于我们在Client端访问，也有助于我们生成GRPC Server。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep075ibtmxMf3eOYlBJ96CE9TEelLUwePaLqp8M75gWHEcM3za0voylA0oe9y3NiaboPB891rypRt7w/132" width="30px"><span>shuff1e</span> 👍（0） 💬（1）<div>mux := runtime.NewServeMux()
看起来是HandleHTTP没指定路由？name是从body取，还是从query参数取，也没指定？</div>2022-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/7d/cae6b979.jpg" width="30px"><span>出云</span> 👍（1） 💬（2）<div>回答一下结尾问题：按文中的写法其实不会出现只返回“Hello”的情况。检查了下代码仓库v3.0.0版本。hello.proto文件中hello方法的option注解少了body字段。按这种写法生成proto文件再次运行，才复现了文末说的问题，所以问题就是出在少了一行`body:  &quot;*&quot;`。

（另外，给protoc安装grpc-gateway的两个插件后，生成的hello.pb.micro.go文件中的NewGreeterEndpoints()函数中返回的api.Endpoint对象会多一个不存在的Body字段，需要删掉才能正常编译。）</div>2023-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/7d/cae6b979.jpg" width="30px"><span>出云</span> 👍（0） 💬（0）<div>产生多余Body字段的原因也找到了。是因为按文中给的包路径安装不到最新的protoc-gen-micro插件。根据go-micro的官方repo，该插件目前的包路径是` github.com&#47;go-micro&#47;generator&#47;cmd&#47;protoc-gen-micro@latest `。 去$GOPATH&#47;bin 把旧的可执行文件删了，执行`go install 新路径`，再重新生成pb文件即可解决问题。 </div>2023-03-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/qCv5IcP1lkO2jicrTic9KicycZXZ7WylG49GZHJCibuFQfBlJMsCpVHARuaLxIB23f3enRL4ls6EOr9wxu40K0Hl8Q/132" width="30px"><span>tcyi</span> 👍（0） 💬（0）<div>google&#47;api&#47;annotations.proto 报错，按照老师提供的方法 不能成功，win10环境
</div>2023-02-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKgz63XQKh9eI5vEicMY27siaoAPubmWr33XNBYic1rvFX0bFNUF6obpKpEEZgzcAtNX1nQiartf8icvdQ/132" width="30px"><span>viclilei</span> 👍（0） 💬（1）<div>docker etcd error</div>2023-01-11</li><br/>
</ul>