你好，我是李玥。

上节课我们一起学习了如何来构建这个RPC框架中最关键的部分，也就是：在客户端，如何根据用户注册的服务接口来动态生成桩的方法。在这里，除了和语言特性相关的一些动态编译小技巧之外，你更应该掌握的是其中动态代理这种设计思想，它的使用场景以及实现方法。

这节课我们一起来实现这个框架的最后一部分：服务端。对于我们这个RPC框架来说，服务端可以分为两个部分：注册中心和RPC服务。其中，注册中心的作用是帮助客户端来寻址，找到对应RPC服务的物理地址，RPC服务用于接收客户端桩的请求，调用业务服务的方法，并返回结果。

## 注册中心是如何实现的？

我们先来看看注册中心是如何实现的。一般来说，一个完整的注册中心也是分为客户端和服务端两部分的，客户端给调用方提供API，并实现与服务端的通信；服务端提供真正的业务功能，记录每个RPC服务发来的注册信息，并保存到它的元数据中。当有客户端来查询服务地址的时候，它会从元数据中获取服务地址，返回给客户端。

由于注册中心并不是这个RPC框架的重点内容，所以在这里，我们只实现了一个单机版的注册中心，它只有客户端没有服务端，所有的客户端依靠读写同一个元数据文件来实现元数据共享。所以，我们这个注册中心只能支持单机运行，并不支持跨服务器调用。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4b/4d/0239bc19.jpg" width="30px"><span>益军</span> 👍（12） 💬（1）<div>您好哈，提个疑问:
服务端业务方法不应该在channelRead0中执行，会导致netty ioEvent线程阻塞，应该异步提交到业务线程池执行
workers.execute(() -&gt; {
    Command response = handler.handle(request);
    if (null != response) {
        channelHandlerContext.writeAndFlush(response).addListener((ChannelFutureListener) channelFuture -&gt; {
            if (!channelFuture.isSuccess()) {
                logger.warn(&quot;Write response failed!&quot;, channelFuture.cause());
                channelHandlerContext.channel().close();
            }
        });
    } else {
        logger.warn(&quot;Response is null!&quot;);
    }
});
 Command response = handler.handle(request);</div>2019-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/04/71/853b2292.jpg" width="30px"><span>Gred</span> 👍（8） 💬（2）<div>来交作业啦【https:&#47;&#47;github.com&#47;Gred01&#47;simple-rpc-framework&#47;tree&#47;nameservice】，其实本应该在周五就写好了，现在写的demo支持mysql和oracle，初始化sql在rpc-netty底下init-sql.md。</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/7f/a7df049a.jpg" width="30px"><span>Standly</span> 👍（3） 💬（1）<div>请教下老师，如果要实现一个可供生产环境大规模集群使用的注册中心，JDBC协议是不是就不太合适了？这种情况下一个注册中心要满足哪些要求呢？个人盲猜：可多台部署、基于tcp协议最好也是netty实现、彼此之间要保证数据一致性（好像也不用强一致），不知道理解对不对</div>2019-11-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKlwpFM3tkeG15YqyJTYWkfqkdmro9POq6SicYm57TaEFDOUZCXjoe0Z0Iz6UibGQqic3icJRsHdFzibtw/132" width="30px"><span>zero</span> 👍（2） 💬（1）<div>如果服务端挂掉了，怎么通知NameService呢？</div>2019-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/69/187b9968.jpg" width="30px"><span>南山</span> 👍（2） 💬（2）<div>抓耳挠腮了两天，还没开始动手，不知道怎么下手～</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/aa/b1/c834aab5.jpg" width="30px"><span>张小勋</span> 👍（0） 💬（1）<div>老师 你好~ 本人是net的 最近刚下了 git 的代码 去看了下~有些写法java和net 还是有区别的  问几个问题 希望老师能够作答一下
首先：helloServiceapi 项目中 建了一个接口   这个接口在服务端去实现   客户端也用到了~ 问下这个接口 在正常的使用中 都是服务端定义好  去给客户端 去使用的么  
第二点：就是在服务端  服务端启动的时候  这个demo 中 是自己去实例化了HelloServiceImpl对象  如果在生产环境中 是不是启动的时候 通过反射 去实例化 那些特定的对外提供的服务  HelloService这样的接口 是不是也要做下标识  是这个思路么
最后 给自己立下个flag  这个月 自己会去 用netcore+netty+zookeeper 去实现一个RPC  多谢老师 </div>2019-11-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/jDG4trQm3t6licZym9TayWRib15Z3auNv4ictblMvkHxzYqOwuD3HibGs8ktGBrPefDic5ZYH85lg9CroynSMlJxcpw/132" width="30px"><span>kim118000</span> 👍（0） 💬（3）<div>Method method = serviceProvider.getClass().getMethod(rpcRequest.getMethodName(), String.class);
每次请求都用反射获取method，有没有性能损耗，是不是存起来，请问老师这部分生产级别怎么处理的？</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ac/62/37912d51.jpg" width="30px"><span>东方奇骥</span> 👍（5） 💬（1）<div>这里注册中心信息是保存在本地文件中，如果保存在数据库，就要用数据库锁，或者zookeeper、redis的分布式锁。感谢老师，工作三年了，没写过框架，这个专栏收获不小！实战篇就超值了。</div>2020-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/05/06/f5979d65.jpg" width="30px"><span>亚洲舞王.尼古拉斯赵四</span> 👍（3） 💬（0）<div>看过了这四节rpc的课程之后，再去看了看中KafkaClient及实现的源码，和本篇讲述思想都是相似的，玥哥厉害！还是思想重要，同时觉得期末测试中的状态转换图也是中间件的基本中的基本，重要中的重要的点，KafkaClient这个接口中很多方法都是基于状态字段来给予的返回。（为什么提起状态转换图我就想到了线程的状态转换~~☺️</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d8/d6/47da34bf.jpg" width="30px"><span>任鹏斌</span> 👍（3） 💬（0）<div>代码拿下来刚消化了一部分，慢慢消化，希望能做一些扩展，一转眼课程要结束了，老师辛苦！</div>2019-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（1） 💬（1）<div>动手要欠账了：大致明白了RPC整个过程需要什么了，啃几遍梳理一下-看看各个是怎么实现的啃明白再去思考Go怎么实现。。。</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/95/2f/d88950a1.jpg" width="30px"><span>颜如玉</span> 👍（0） 💬（0）<div>Method method = serviceProvider.getClass().getMethod(rpcRequest.getMethodName(), String.class);注册中心不是只返回物理地址嘛，怎么还能调用服务端呢</div>2024-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/69/af/ceb4450c.jpg" width="30px"><span>Asha</span> 👍（0） 💬（1）<div>老师，有个问题，不知道还能不能到达你那，我们在进阶篇中讲到了应用层协议，其实就是半包处理，为什么在rpc这里没有这部分的处理</div>2021-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5a/5e/a897cb0d.jpg" width="30px"><span>grey927</span> 👍（0） 💬（0）<div>老师，单例模式的实现，如果用Effective Java中推荐的枚举单例是否会更好一些。</div>2020-05-12</li><br/>
</ul>