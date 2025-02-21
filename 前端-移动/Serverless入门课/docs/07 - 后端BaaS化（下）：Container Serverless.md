你好，我是秦粤。上节课，我重点给你讲了业务逻辑的拆和合，拆的话可以借助DDD的方法论，也可以用动态网络的思想让微服务自然演进；合的话，我们可以用代码编排，也可以用事件流来驱动。另外，我们还了解了微服务拆解后会带来的安全信任问题，这可以通过微服务的跨域认证JWT方案解决。我们还了解了后端应用要支持快速迭代或发布，可以参考微服务搭建灰度发布流水线，也就是发布管道。其实我们在使用FaaS过程中遇到的很多问题，都可以借助或参考微服务的解决方案。

现在我们再回顾一下BaaS化后的“待办任务”Web服务，我们已经将后端拆解为用户微服务和待办任务微服务，前端用户访问我们的FaaS服务，登录后获取到JWT，通过数据接口+JWT安全地访问我们的微服务。而且我们的FaaS和微服务都具备了快速迭代的能力。

![](https://static001.geekbang.org/resource/image/c8/15/c8ee82521e5c965d8955afe8c210b615.jpg?wh=1534%2A1150 "BaaS化后的“待办任务”Web服务")

到这里，我要指出我之前rule-faas.js的一个Bug，如果你之前亲自动手做过实验的话，估计也有发现。这个Bug的直接表现是用户初次请求数据时，如果触发了冷启动，返回的待办任务列表就会为空。

究其原因，是因为冷启动时连接数据库会有延时，这直接导致了第一个请求返回的待办任务列表还未同步到消息队列的数据。要解决这个bug，我们可以用之前讲过的预热FaaS或预留实例的方式，但你也要知道，FaaS函数扩容时，新启动的函数副本也会出现同样的问题。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（6） 💬（1）<div>在完成课后作业时,将docker镜像部署到了本地,阿里云ECI,阿里云k8s,一切都很美好.
但是部署到阿里云serverless k8s的时候,遇到了一个坑,给大家分享一下.

现象: 无法打开todolist页面.
      但是控制面板上看pod和容器组状态正常,无重启记录.

排查过程:
1. 使用golang服务制作了一个镜像,端口号也使用3001,部署的服务可以正常访问.
   (说明操作流程和相关配置无问题)
2. 在控制面板上看,对应的pod运行状态健康,遂在index.js底部添加日志.
   发现初始化的日志出来了,说明服务确实是跑起来了.
3. 由于控制面板上无法执行kubectl exec -it 操作进入容器.
   顾开启了一个实例,安装了kubectl客户端,登录容器.
   [由于创建serverless k8s集群时未开通API Server 公网连接端点,所以只能在VPC网络中访问k8s API]
4. 进入容器后,发现curl http:&#47;&#47;localhost:3001提示连接拒绝.
   使用netstat命令提示命令不存在.
   在容器内直接使用apt-get update ; apt-get install net-tools 由于网络问题,长时间安装不成功.
5. 修改dockerfile,在制作镜像时执行安装操作.
6. 重新推送镜像,部署服务,进入容器.
   发现3001端口果真未监听.
   但是netstat -antple中,显示连接了一个阿里云的otsIP地址处于SEND_SYNC阶段.怀疑是网络问题.
   结果ping baidu.com果真是ping不通.
7. 尝试还原index.js中监听服务的代码
   直接使用: app.listen(PORT, () =&gt; console.log(`Example app listening at http:&#47;&#47;localhost:${PORT}`))
   不再放在client.getRow函数中.
8. 重新推送镜像,部署服务,进入容器.
   发现可以正常访问todolist主页,只是没有数据.
9. 猜测是 serverless k8s 默认无法访问公网,需要NAT网关才可以访问公网.
   提交工单,得到证实.
   需要在创建服务时,添加一个注解,在创建pod时绑定一个eip.
   照着工单中的方法,重新还原index.js后部署了一遍,果真可以正常访问todolist首页,且历史记录也有了.

就一个简单的服务不可用,排查起来是相当的麻烦.还要不走弯路.

对[suke]同学留言中的一句话很赞同:
&quot;如果想完全hold住serverless 真是的类似全栈这样的工程师来做&quot;
</div>2020-05-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ZkcKFzQ3qaIWpHjfOib9yU1LicthmiawfmkNhiakDdTUbTtCcworSZsxpiaib4sygOoc32duoUdQcI3Y1EmgcbicTzAyA/132" width="30px"><span>Geek_a5c054</span> 👍（1） 💬（6）<div>用docker后台运行的时候显示了容器id之后直接就退出了，没在后台运行，
然后，使用docker run -it或者在文件根目录使用npm start的时候显示cannot find module uuid是为什么呀</div>2020-07-04</li><br/><li><img src="" width="30px"><span>suke</span> 👍（1） 💬（3）<div>老师我觉得，专栏看到这里，如果想完全hold住serverless 真是的类似全栈这样的工程师来做，如果只是让偏前端的工程师开发页面以及简单的业业务逻辑，在真正开发 以及调试的阶段，很难去完全cover ，但是如果把前端页面以外的工作交给后端工程师，实现起来一个是拆分的太细，想想本来一个很简单的列表查询 我不仅要写业务逻辑的查询 我还要把基础的数据查询接口封装到有状态的服务，开发、维护起来很麻烦，后期维护起来排查问题难度都很大，调用链条还变长，怎么看我都觉得serverless有点舍近求远，不知道老师觉得我这个想法有什么问题</div>2020-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/48/15/8db238ac.jpg" width="30px"><span>神仙朱</span> 👍（0） 💬（1）<div>学到这里的确有些吃力了，学完baas我觉得还是不太明白怎么回事。
现在baas是在faas来做，那么肯定最好是无状态的。
正常来说baas应该在哪里做呢。
就是，如果我现在要写一个应用，后端的接口要连数据库，我要怎么做给前端提供接口，难道还是一样直接部署到服务器？</div>2020-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/62/24/07e2507c.jpg" width="30px"><span>托尼斯威特</span> 👍（0） 💬（3）<div>没有aliyunConfig 文件, 代码没法运行. 
看用到aliyunConfig的地方, 读了endpoint, AK&#47;KS, instanceName, tableName, primaryKey.

是不是意味着要想跑这个代码, 我们得自己去见一个tablestore的表格? instanceName填什么? 


</div>2020-07-06</li><br/><li><img src="" width="30px"><span>suke</span> 👍（0） 💬（1）<div>老师，这篇文章我看了好几遍，类似java这样的后端服务baas化，冷启动即使是docker容器化启动也是省略不了正常的启动过程的，也就是说无论你从裸机上启动还是docker化启动，时长都差不多呀，这样还是改变不了启动时间很长的问题；另外一种把db服务包装成restful接口，其实这种方式还是需要有状态服务一直存在的，同时，这种方式对于事务问题的解决又带来了新的问题，所以我个人感觉serverless目前局限性很大</div>2020-06-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/EcYNib1bnDf5dz6JcrE8AoyZYMdqic2VNmbBtCcVZTO9EoDZZxqlQDEqQKo6klCCmklOtN9m0dTd2AOXqSneJYLw/132" width="30px"><span>博弈</span> 👍（0） 💬（1）<div>老师，registry.cn-shanghai.aliyuncs.com&#47;jike-serverless&#47;nodejs，这个基础镜像不能拉取，获取不到latest的版本，肿么破</div>2020-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/a8/dfe4cade.jpg" width="30px"><span>电光火石</span> 👍（0） 💬（1）<div>老师，请问一下，Fass和Bass是不是都可以使用Docker来启动？但是因为Bass会连接数据库，启动时间较长，所以偏向于用Docker启动，而Fass层做服务编排，而且都会提供一项“函数初始化入口”的选项，启动时间会很短，所以是否Docker启动没有那么明显？谢谢了！</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（0） 💬（1）<div>即便是用了docker，遇到需要编译的npm包，直接复制node_modules目录也可能会因为宿主系统和镜像系统的差异而导致问题吧</div>2020-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（0） 💬（3）<div>课后作业:

1. 由于镜像中有aliyunConfig,所以不建议将镜像公开.(即不要推送到默认的 https:&#47;&#47;hub.docker.com&#47;)

2. 我是在template.yml文件中添加了一行`Initializer: index.initializer`实现了作业1:部署的 rule-faas 函数添加初始化入口

3. 使用阿里云ECI部署时,需要申请弹性公网EIP.
   注意: 这里需要指定端口号3001访问服务, 默认的80端口是无法访问到服务的!!!
   与本地调试一样,某些操作会触发容器重启.

4. 本地调试时,使用get方法访问`http:&#47;&#47;localhost:3001&#47;api&#47;rule`可以正常获取结果.
   但是完成&#47;删除(使用put&#47;delete方法)时,会提示403&quot;用户得到授权，但是访问是被禁止的。&quot;
   docker反馈的日志如下:
   ```
   &#47;home&#47;myhome&#47;myapp&#47;node_modules&#47;tablestore&#47;lib&#47;request.js:66
            throw err;
            ^
Error [ERR_HTTP_HEADERS_SENT]: Cannot set headers after they are sent to the client
    at ServerResponse.setHeader (_http_outgoing.js:470:11)
    at ServerResponse.header (&#47;home&#47;myhome&#47;myapp&#47;node_modules&#47;express&#47;lib&#47;response.js:771:10)
    at ServerResponse.send (&#47;home&#47;myhome&#47;myapp&#47;node_modules&#47;express&#47;lib&#47;response.js:170:12)
    at ServerResponse.json (&#47;home&#47;myhome&#47;myapp&#47;node_modules&#47;express&#47;lib&#47;response.js:267:15)
    at Response.&lt;anonymous&gt; (&#47;home&#47;myhome&#47;myapp&#47;index.js:151:16)
    at Request.&lt;anonymous&gt; (&#47;home&#47;myhome&#47;myapp&#47;node_modules&#47;tablestore&#47;lib&#47;request.js:162:18)
    at Request.callListeners (&#47;home&#47;myhome&#47;myapp&#47;node_modules&#47;tablestore&#47;lib&#47;sequential_executor.js:113:20)
    at Request.emit (&#47;home&#47;myhome&#47;myapp&#47;node_modules&#47;tablestore&#47;lib&#47;sequential_executor.js:81:10)
    at Request.emit (&#47;home&#47;myhome&#47;myapp&#47;node_modules&#47;tablestore&#47;lib&#47;request.js:189:14)
    at Request.transition (&#47;home&#47;myhome&#47;myapp&#47;node_modules&#47;tablestore&#47;lib&#47;request.js:57:10)
   ```
   由于不太懂node.js,所以也不知道如何解决.
   之前部署到阿里云FC时是没有遇到过该问题的.
</div>2020-05-01</li><br/><li><img src="" width="30px"><span>北冥神功</span> 👍（0） 💬（1）<div>我感觉谷歌的Cloud Run冷启动要比faas这种快，在腾讯部署的go服务冷启动要2s，cloud run只需要几百毫秒。cloud run是基于knative，不知道是不是因为是容器所以快？</div>2020-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>利用实时监控，去控制扩缩容,
向文中说的，云上有什么服务可以实时监控 一些指标进行扩缩容呢？ 现在基本上都是根据并发数来进行扩缩容的</div>2020-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>这个把服务 docker  化，不就没有办法使用 FaaS 服务了？ FaaS 有么有哪个地方可以结合 容器化服务一起使用的？</div>2020-05-01</li><br/>
</ul>