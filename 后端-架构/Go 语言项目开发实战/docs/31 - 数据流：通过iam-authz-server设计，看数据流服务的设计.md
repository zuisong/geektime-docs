你好，我是孔令飞。

在 [28讲](https://time.geekbang.org/column/article/401190) 和 [29讲](https://time.geekbang.org/column/article/402206) ，我介绍了IAM的控制流服务iam-apiserver的设计和实现。这一讲，我们再来看下IAM数据流服务iam-authz-server的设计和实现。

因为iam-authz-server是数据流服务，对性能要求较高，所以采用了一些机制来最大化API接口的性能。另外，为了提高开发效率，避免重复造轮子，iam-authz-server和iam-apiserver共享了大部分的功能代码。接下来，我们就来看下，iam-authz-server是如何跟iam-apiserver共享代码的，以及iam-authz-server是如何保证API接口性能的。

## iam-authz-server的功能介绍

iam-authz-server目前的唯一功能，是通过提供 `/v1/authz` RESTful API接口完成资源授权。 `/v1/authz` 接口是通过[github.com/ory/ladon](https://github.com/ory/ladon)来完成资源授权的。

因为iam-authz-server承载了数据流的请求，需要确保API接口具有较高的性能。为了保证API接口的性能，iam-authz-server在设计上使用了大量的缓存技术。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/64/53/c93b8110.jpg" width="30px"><span>daz2yy</span> 👍（8） 💬（1）<div>老师，请问下，数据流和控制流这个怎么来理解呢，是从什么角度来定义的服务类型的？</div>2021-08-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKhuGLVRYZibOTfMumk53Wn8Q0Rkg0o6DzTicbibCq42lWQoZ8lFeQvicaXuZa7dYsr9URMrtpXMVDDww/132" width="30px"><span>hello</span> 👍（5） 💬（2）<div>老师，咨询您一个问题，使用GiN做WEB服务，微服务间通过gRPC通讯，如何选择配置注册中心，老师能否推荐几款比较流行开源的配置注册中心。</div>2021-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（4） 💬（1）<div>本地channel缓冲和redis缓存对于性能的提高效果会很明显，设计的比较好。但同时，这样的设计会导致多存储数据同步的问题。比如，如果服务突然宕机，本地缓冲中的数据就可能丢失。不知道老师有没有什么好的办法解决？</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/96/82/8ac1e909.jpg" width="30px"><span>Jarvis</span> 👍（3） 💬（1）<div>更新缓存时每次都 List 全部密钥&#47;策略，数据量会不会太大了？ Pub 时带上变化的策略&#47;密钥 id, 只更新该 id  的内容是不是好一点？</div>2022-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（2） 💬（1）<div>总结：
iam-authz-server 在数据流上工作，负责授权工作，对性能要求高。
authz也需要对请求进行认证工作，authz 的认证采用 cache 方式实现 jwt token 认证，即密钥已经缓存在内存中，通过同样的加密方案，确认token的合法性。
authz的认证工作主要交给了 landon 来完成。iam-apiserver 存储的授权策略符合landon的语法规范，iam-authz-server 接收的授权请求，也符合landon的语法规范。landon 通过接口的方式，暴露了manager、auditLogger、metric 等相关的接口。比如，我们需要为landon提供用户的 policy 列表，是否允许授权，由 landon 来做决策。
缓存设计</div>2021-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/11/d7e08b5b.jpg" width="30px"><span>dll</span> 👍（1） 💬（1）<div>每次从apiserver触发reload() 都是全量的拉去 s.cli.GetPolicies()，这样应该可能会产生性能问题吧 假如当Policies数量特别大的时候</div>2022-10-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJKObzsYVibibyibmTVKBmoGPqS0WQC16EY4p1agGDCpv5okKpjzicLtHafBVa7TCwh9HaRxTx9qQ1Qkg/132" width="30px"><span>陈先生</span> 👍（1） 💬（1）<div>如果iam-authz-server挂了，是不是有audit log丢失的可能性？</div>2021-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（1） 💬（1）<div>在实际应用中，请求&#47;v1&#47;authz接口的参数体是网关根据用户实际请求的某个具体业务的api的参数、请求方法、path等，并根据提前定制的规则自动构造出来的吧，这样理解对吗</div>2021-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/49/c4/c5ddbe2b.jpg" width="30px"><span>岑惠韬</span> 👍（0） 💬（1）<div>老师请问Load的Start函数第二个协程的作用是什么呢？是主要起解耦作用吗？假如让PubSubLoop直接操作requeue切片，让reloadLoop每秒清空切片，仅考虑当前用法的话是不是也是能跑的？还是会有什么逻辑上的问题？</div>2022-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/5e/b79e6d5d.jpg" width="30px"><span>꧁子华宝宝萌萌哒꧂</span> 👍（0） 💬（1）<div>preparedAuthzServer.Run 为啥需要一个 stopChan 来阻塞不让退出？

按我的理解这个 stopChan 没有写，这个进程永远就退不了， 

直接 return s.genericAPIServer.Run() 不可以吗？</div>2022-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1e/4c/10174727.jpg" width="30px"><span>xinHAOr</span> 👍（0） 💬（1）<div>func (r *Analytics) Start() 里面为什么同步执行了Stop？刚启动完就停止了吗</div>2022-04-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7orjLiard5WYicG0WaRjk01ycCDtAZadtf2sWzg0c7vXl7oqIwic0QvzlE3lr3fgMZibqXSwAibV4Qu0YSeeMlibUMSg/132" width="30px"><span>Geek_226b1b</span> 👍（0） 💬（3）<div>老师，请问为什么用Ristretto缓存数据，不直接用Redis缓存数据呢？在用Redis缓存的基础上，讲一下MySQL与Redis的数据一致性相关的缓存读写策略会不会更好一点？把所有数据都简单缓存到一个缓存包&#47;Redis里，没有淘汰机制是不是不太好？</div>2022-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/f0/eb/24a8be29.jpg" width="30px"><span>RunDouble</span> 👍（0） 💬（1）<div>太强调授权相关的东西，并不是很好的 demo。</div>2022-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（2） 💬（0）<div>详细介绍了iam-authz-server的设计与实现。
需要结合代码和跑起来的程序反复揣摩。</div>2021-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/78/35/63a49c0a.jpg" width="30px"><span>Will</span> 👍（1） 💬（0）<div>孔老师。Reload这里
c.secrets.Clear()
for key, val := range secrets {
	c.secrets.Set(key, val, 1)
}
这里clear.另一个请求如果授权的话。还没有跑到set的方法。可能会有问题。虽然可能是毫秒级别的。
可能是为了教学演示，如果是生产使用的话，是不是要设计成增量合理些。</div>2023-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/67/73/50edc703.jpg" width="30px"><span>Rocky</span> 👍（0） 💬（0）<div>func startPubSubLoop() {
	cacheStore := storage.RedisCluster{}
	cacheStore.Connect()
	&#47;&#47; On message, synchronize
	for {
		err := cacheStore.StartPubSubHandler(RedisPubSubChannel, func(v interface{}) {
			handleRedisEvent(v, nil, nil)
		})
		if err != nil {
			if !errors.Is(err, storage.ErrRedisIsDown) {
				log.Errorf(&quot;Connection to Redis failed, reconnect in 10s: %s&quot;, err.Error())
			}

			time.Sleep(10 * time.Second)
			log.Warnf(&quot;Reconnecting: %s&quot;, err.Error())
		}
	}
}这个函数在load.go文件中，想问问这个函数退出循环的条件在哪呢？</div>2024-09-12</li><br/><li><img src="" width="30px"><span>Geek_7a540f</span> 👍（0） 💬（0）<div>老师，我看了封装redis的那段代码，不太理解尝试重新连接的作用。我们一开始通过写好配置，创建对应的client。如果当前redis连接不上，重试也没用。过了一段时间redis能够连接了，使用原来的client也能连上(说到底配置还是没变)</div>2024-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/a9/66/2df6b3fe.jpg" width="30px"><span>滴滴答答</span> 👍（0） 💬（0）<div>缓存一致性那里是怎么做到前面文章提到的如果 redis down掉或者网络不稳定的问题的？redis的 pub&#47;sub 是有可能有数据丢失的问题吧？</div>2024-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d3/40/0067d6db.jpg" width="30px"><span>AKA三皮</span> 👍（0） 💬（1）<div>您文章中说的，api server 对于secret和policy的改动，会pub事件到redis，给auth server 订阅，这块代码中没有实现吧？ 我代码翻了一遍，并没有找到</div>2023-06-24</li><br/>
</ul>