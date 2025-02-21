你好，我是李玥。

继续上节课的内容，这节课我们一起来实现这个RPC框架的通信和序列化部分。如何实现高性能的异步通信、如何来将结构化的数据序列化成字节流，用于网络传输或者存储到文件中，这两部分内容，我在进阶篇中都有在专门的课程分别讲解过。

网络传输和序列化这两部分的功能相对来说是非常通用并且独立的，在设计的时候，只要能做到比较好的抽象，这两部的实现，它的通用性是非常强的。不仅可以用于我们这个例子中的RPC框架中，同样可以直接拿去用于实现消息队列，或者其他需要互相通信的分布式系统中。

我们在实现这两部分的时候，会尽量以开发一个高性能的生产级系统这样的质量要求来设计和实现，但是为了避免代码过于繁杂影响你理解主干流程，我也会做适当的简化，简化的部分我会尽量给出提示。

## 如何设计一个通用的高性能序列化实现？

我们先来实现序列化和反序列化部分，因为后面讲到的部分会用到序列化和反序列化。

首先我们需要设计一个可扩展的，通用的序列化接口，为了方便使用，我们直接使用静态类的方式来定义这个接口（严格来说这并不是一个接口）。

```
public class SerializeSupport {
    public static  <E> E parse(byte [] buffer) {
        // ...
    }
    public static <E> byte [] serialize(E  entry) {
        // ...
    }
}
```

上面的parse方法用于反序列化，serialize方法用于序列化。如果你对Java语言不是特别的熟悉，可能会看不懂`<E>`是什么意思，这是Java语言泛型机制，你可以先忽略它。看一下如何来使用这个类就明白了：
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/03/10/26f9f762.jpg" width="30px"><span>Switch</span> 👍（5） 💬（2）<div>使用fastjson实现，改动代码见：https:&#47;&#47;gist.github.com&#47;Switch-vov&#47;8cb76aabd1e1addcdbec205cc06d9023</div>2019-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/1b/f62722ca.jpg" width="30px"><span>A9</span> 👍（5） 💬（1）<div>老师的课程很多地方让人茅塞顿开，感觉从高中毕业之后就再也没有过这种抽丝剥茧学习知识的感觉了。感谢带来这么好的课程</div>2019-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/1b/f62722ca.jpg" width="30px"><span>A9</span> 👍（2） 💬（1）<div>使用JSON字符串进行序列化，String的序列化保持原样。MetaData和RpcRequest修改了size parse serialize函数  https:&#47;&#47;gist.github.com&#47;WangYangA9&#47;210ca898525832cba8ddd57ae1ae3d13</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/88/23/a0966b4d.jpg" width="30px"><span>Tim Zhang</span> 👍（1） 💬（1）<div>有一点不是很理解，为啥typeMap不可以是(type, serializer)，通过type获取序列化实现类一步操作，现在看源码是通过type拿到class，再class拿到serializer</div>2019-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/cf/b0d6fe74.jpg" width="30px"><span>L.</span> 👍（0） 💬（2）<div>小白问一下，send方法的返回值是怎么到completableFuture对象里的，我没看到赋值操作啊，求解。。。</div>2020-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5f/73/bb3dc468.jpg" width="30px"><span>拒绝</span> 👍（0） 💬（1）<div>有点不理解，Server启动时，向NameService注册接口时，序列化对象是MetadataSerializer？</div>2019-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/69/187b9968.jpg" width="30px"><span>南山</span> 👍（0） 💬（1）<div>动手动手，一定要动手，netty不熟，看起来吃力，但也收获满满，每明白一点都是进步～～～</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/41/87/46d7e1c2.jpg" width="30px"><span>Better me</span> 👍（0） 💬（2）<div>ResponseInvocation 这个类是相当于一个回调类的形式吧。“就是根据响应头中的 requestId，去在途请求 inFlightRequest 中查找对应的 ResponseFuture，设置返回值并结束这个 ResponseFuture 就可以了。”这里的设置返回值是指code码形式吗？这里的作用是还需要在返回给服务端确认收到吗？老师有空看看</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（27） 💬（2）<div>今日得到
关键字:背压机制(back pressure)
当客户端同步请求服务端时，客户端需要等待服务端处理完请求并返回响应，在此期间，客户端需要等待，这是一种天然背压机制

那换成异步请求呢？
客户端异步请求服务端时，不会等待服务端处理请求，这样就丧失了同步请求的那种天然背压。
如果服务器处理请求的速度慢于客户端发送请求的速度，就会导致InFlightRequest(在途请求，即还未被服务端处理或响应的请求)越来越多，如果这些在途请求保存在内存中，就可能导致内存飙升，进而引发频繁FGC，之前线上遇到过几次FGC的案例【在公众号:每天晒白牙 中分享过一个vertx-redis-client客户端的案例 https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;fWsy26VeUvb8yPKON3OTmA，后面也遇到rpc框架中也出现类似的问题】都是因为这些在途请求保存在一个无界队列中，请求得不到处理，导致内存占用过高。

想要避免上面的情况，需要我们主动引入背压机制，即在服务端处理不过来的情况要限制客户端的请求速率，具体的做法应该有很多，我列举几个
1.把无界队列换成有界队列，队列满了就不让添加了
2.在往队列中添加请求的时候获取许可，服务端处理完请求释放许可，如果许可没了就阻塞客户端的请求或返回异常
——每天晒白牙
</div>2019-10-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIE3Vw0icEQic96rOykFD2bUo6KotVx53gvtG0CDe8tUKC3pNXxIQYMuyPyrgL06Zn32UWtEXTIVWMw/132" width="30px"><span>Geek_fd81b3</span> 👍（2） 💬（0）<div>纸上得来终觉浅，绝知此事要躬行，真是良心课程，赞。</div>2020-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/05/06/f5979d65.jpg" width="30px"><span>亚洲舞王.尼古拉斯赵四</span> 👍（2） 💬（0）<div>想用json的方式，搞一个泛型的CommonSerializer&lt;T&gt;出来，序列化好说，但是在进行解析成对象的时候，发现我通过泛型无法拿到原本的Class，😂，想了半天方法用反射去搞，但是觉得这样不好，查了一下发现一般这种情况是通过传入一个你想要解析的最终类型的Class对象，但是又要求不该接口，这样我就不能传进去一个Class，无奈，只能针对每个类型实现一下Serializer接口</div>2019-11-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7H0jIVKP3icqA4LmA1jXicHRz3zticVGE7gTRA5WDwmcLmLiay6S7PnKwhiaN5LNia3f5SIeglU6O7ByibOibnAiaMjjQgA/132" width="30px"><span>知也无涯</span> 👍（1） 💬（1）<div>removeTimeoutFutures, 这个方法名起得不太好~  根本没有移除 future, 只是把 semaphore 释放了</div>2021-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/a2/fa41c8a8.jpg" width="30px"><span>书中迷梦</span> 👍（1） 💬（0）<div>requestId要保持唯一性，不然消息就乱了！！而且不用保持全局唯一性，只要保证在单个服务中唯一就好</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/0d/3dc5683a.jpg" width="30px"><span>柯察金</span> 👍（0） 💬（0）<div>这个课不错。很多其他讲 rpc 的课，理论一大堆，不如老师这几讲的内容</div>2024-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ff/d0/402be1e9.jpg" width="30px"><span>VIC</span> 👍（0） 💬（0）<div>老师代码，github地址发下</div>2022-10-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKiauonyMORA2s43W7mogGDH4WYjW0gBJtYmUa9icTB6aMPGqibicEKlLoQmLKLWEctwHzthbTZkKR20w/132" width="30px"><span>Spring4J</span> 👍（0） 💬（0）<div>请教个问题：
CommandEncoder中，byteBuf.writeInt(Integer.BYTES + command.getHeader().length() + command.getPayload().length);
CommandDecoder中，int length = byteBuf.readInt() - LENGTH_FIELD_LENGTH(4字节);
我没搞懂编码时第一个四字节有啥用；
我在编码中把这四字节取消掉，然后解码时也取消掉(int length = byteBuf.readInt())是没有问题的
</div>2022-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9d/81/d748b7eb.jpg" width="30px"><span>千锤百炼领悟之极限</span> 👍（0） 💬（0）<div>private final Semaphore semaphore = new Semaphore(10);
相当于设置一个令牌桶，最多有10个令牌，如果使用完则需要归还才能继续发送数据，是一个限流的作用。</div>2021-09-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/STqKg1kLgvRuduQfo0R2E2osYBian7XrQAjSWmOwL9nyZVhq7vyLPnlGcgvguFV4aV7ToWLFiauEMKy96KWHKBVg/132" width="30px"><span>离境”</span> 👍（0） 💬（0）<div>想问下可以使用netty的SO_BACKLOG来实现背压机制吗</div>2021-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/6d/8b417c84.jpg" width="30px"><span>Wheat Liu</span> 👍（0） 💬（0）<div>感觉跟rocket mq的代码结构差不多，也是用的netty</div>2021-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（0） 💬（0）<div>最后的RPC实战这几节课，真的是绝，看了何晓峰老师的RPC实战，然后在结合李老师的这个简易的RPC架构实现，简直完美，这个背压机制，其实就是限流，利用信号量进行限流，之前看过信号量Semaphore的源码，一直没在代码中用过，这算是一个很好的应用了，当然限流还可以用令牌桶和漏桶算法等实现，这里想信号量其实就是个计数器</div>2021-05-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7H0jIVKP3icqA4LmA1jXicHRz3zticVGE7gTRA5WDwmcLmLiay6S7PnKwhiaN5LNia3f5SIeglU6O7ByibOibnAiaMjjQgA/132" width="30px"><span>知也无涯</span> 👍（0） 💬（0）<div>com.github.liyue2008.rpc.transport.InFlightRequests#remove 的实现只是把 Map 中的元素移除了, 并没有像文稿中一样 &quot;设置返回值并结束这个 ResponseFuture&quot;</div>2021-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（0）<div>异常关流；
超时关流；
背压限流。</div>2020-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/34/eb/d00aedb0.jpg" width="30px"><span>lecy_L</span> 👍（0） 💬（0）<div>准点研读了一遍，受益匪浅。明天利用空闲时间尝试完成思考题。</div>2019-10-08</li><br/>
</ul>