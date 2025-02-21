你好，我是姚秋辰。

在上节课中，我们通过一系列谓词和过滤器的组合为三个微服务模块配置了路由规则，这套方案足以应对大部分线上业务的需求，但在可扩展性方面还不够完美。为什么这么说呢？因为这些路由规则是以yml文件或者Java代码配置在项目中的静态规则。随着项目启动，这些路由规则会被加载到应用上下文并生效。但在程序运行期，如果我们想要改变这些预定义的路由规则，或者创建新的路由规则，似乎只有提交改动到Gateway组件-&gt;编译项目-&gt;重新部署这一条路子。

那么，如果我们希望不重新部署网关，就能更改路由规则，可以有哪些途径呢？

有一种“临时性”的方案，是借助Gateway网关的actuator endpoiont进行CRUD。Gateway组件内定义了一套内置的actuator endpoints，当满足下面两个条件时，我们就可以借助actuator提供的能力对路由表进行修改了。

- 项目中存在spring-boot-starter-actuator依赖项；
- Gateway组件的actuator endpoint已对外开放。  
  为了满足上面这两个条件，我已经将配置项添加到了Gateway模块中，并且在application.yml文件中的management节点下，对外开放了所有actuator端点。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/9d/35/e026cf65.jpg" width="30px"><span>Ever</span> 👍（10） 💬（6）<div>没明白为啥不直接在nacos上用spring.cloud.gateway.routes配置项配置路由，明明本身就支持动态刷新，哪里需要画蛇添足自定义监听配置和刷新路由。
RefreshRoutesEvent 事件会触发路由刷新，这一步本身就比较耗CPU（可以自己抓个火焰图），这里在forEach里还不停触发是否合理（放在循环外面不是更好）。</div>2022-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/bd/ba3530ff.jpg" width="30px"><span>theodore</span> 👍（4） 💬（1）<div>我们的路由是自己实现的前后端分离的服务，增删改查都在上面操作 没有依靠nacos config</div>2022-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师四个问题啊：
Q1：Gateway内置的actuator endpoint是Gateway独有的？还是具有通用性？比如其他的组件(e.g,nacos)也可以加入actuator endpoint?
Q2：DynamicRoutesListener是观察者模式吗？
Q3：DynamicRoutesLoader是把Nacos中的文件“routes-config.json”读取过来吗？（相当于跨进程或跨机器传输文件）
Q4：在middleware下面的Gateway这个module本身是个独立的服务，它不同于Gateway组件，对吗？ 如果是这样，GatewayService是定义在Gateway这个服务中的，GatewayService要把路由信息更新到Gateway组件的上下文中，是通过跨进程或跨机器通信，对吗？</div>2022-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1e/cf/97cd8be1.jpg" width="30px"><span>so long</span> 👍（0） 💬（4）<div> 请教老师一个问题：publisher.publishEvent(new RefreshRoutesEvent(this));这行代码是必须的吗？我自己测试的时候执行该行代码后就卡主不会往下执行了，然后我注释掉该行代码，也可以实现路由的动态刷新。</div>2022-03-01</li><br/><li><img src="" width="30px"><span>Geek_bf202a</span> 👍（0） 💬（1）<div> publisher.publishEvent(new RefreshRoutesEvent(this));
这行代码会导致gateway项目起不来，卡住，怎么解决呢？</div>2023-10-12</li><br/><li><img src="" width="30px"><span>Geek_bf202a</span> 👍（0） 💬（0）<div> publisher.publishEvent(new RefreshRoutesEvent(this));  </div>2023-10-12</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83epUm0LibVnFOia7CN1fj91UyicicIOxib8POPG2dkVIN5IuJJlOQqwJAH4koEEUMoujZKBqzfZIrVmA5wA/132" width="30px"><span>安静的美男子</span> 👍（0） 💬（0）<div>看起来没有支持路由删除的场景，updateRoutes 实现的只支持新增、修改，不支持删除呀，如果删除了路由会不起效</div>2023-04-25</li><br/>
</ul>