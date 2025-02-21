你好，我是蒋德钧。从这节课开始，我们就来到了课程的第二个模块，在这个模块里，我会带你了解和学习与Redis实例运行相关方面的知识，包括Redis server的启动过程、基于事件驱动框架的网络通信机制以及Redis线程执行模型。今天，我们先来学习下Redis server的启动过程。

我们知道，main函数是Redis整个运行程序的入口，并且Redis实例在运行时，也会从这个main函数开始执行。同时，由于Redis是典型的Client-Server架构，一旦Redis实例开始运行，Redis server也就会启动，而main函数其实也会负责Redis server的启动运行。

> 我在[第1讲](https://time.geekbang.org/column/article/399866)给你介绍过Redis源码的整体架构。其中，Redis运行的基本控制逻辑是在[server.c](https://github.com/redis/redis/tree/5.0/src/server.c)文件中完成的，而main函数就是在server.c中。

你平常在设计或实现一个网络服务器程序时，可能会遇到一个问题，那就是服务器启动时，应该做哪些操作、有没有一个典型的参考实现。所以今天这节课，我就从main函数开始，给你介绍下Redis server是如何在main函数中启动并完成初始化的。通过这节课内容的学习，你可以掌握Redis针对以下三个问题的实现思路：
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（36） 💬（6）<div>Redis 启动流程，主要的工作有：

1、初始化前置操作（设置时区、随机种子）

2、初始化 Server 的各种默认配置（server.c 的 initServerConfig 函数），默认配置见 server.h 中的 CONFIG_DEFAULT_XXX，比较典型的配置有：

- 默认端口
- 定时任务频率
- 数据库数量
- AOF 刷盘策略
- 淘汰策略
- 数据结构转换阈值
- 主从复制参数

3、加载配置启动参数，覆盖默认配置（config.c 的 loadServerConfig 函数）：

- 解析命令行参数
- 解析配置文件

3、初始化 Server（server.c 的 initServer 函数），例如会初始化：

- 共享对象池
- 客户端链表
- 从库链表
- 监听端口
- 全局哈希表
- LRU 池
- 注册定时任务函数
- 注册监听请求函数

4、启动事件循环（ae.c 的 aeMain 函数）

- 处理请求
- 处理定时任务

这里补充一下，初始化 Server 完成后，Redis 还会启动 3 类后台线程（server.c 的 InitServerLast 函数），协助主线程工作（异步释放 fd、AOF 每秒刷盘、lazyfree）。

课后题：Redis 源码的 main 函数在调用 initServer 函数之前，会执行如下的代码片段，你知道这个代码片段的作用是什么吗？

int main(int argc, char **argv) {
	...
	server.supervised = redisIsSupervised(server.supervised_mode);
	int background = server.daemonize &amp;&amp; !server.supervised;
	if (background) daemonize();
	...
}

Redis 可以配置以守护进程的方式启动（配置文件 daemonize = yes），也可以把 Redis 托管给 upstart 或 systemd 来启动 &#47; 停止（supervised = upstart|systemd|auto）。</div>2021-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（11） 💬（2）<div>感谢老师的文章，先回答老师提出的问题：文章中代码片段的作用是？根据关键词我找到代码位于，main函数中loadServerConfig之后执行的，那么这块代码主要任务和顺序如下所示：
    1、此时redis的config是已经初始化完成的
    2、执行redisIsSupervised其目底主要是判断当redis进程是否运行中
    3、判断daemonize是否开启（如果启动设置了daemonize参数那么这里参数已经被填充）
    4、之前并没有存活的redis实例，并且开启了daemonize配置，那么执行daemonize函数挂起后台运行

这里需要解释一下，执行daemonize()函数的时候本质是fork()进程，并不是大多文章说的那样是守护线程，父亲fork成功后是直接退出（在前端的效果就是，启动命令任务完成但是ps是有一个redis的进程），剩余的任务是交给fork出的子进程完成的（可以参考《深入理解操作系统》 第8章-异常控制流-进程中的内容）

读完这篇文章后，我个人尝试画出整个redis启动的时序图，发现整个思路就很清晰了，建议同样阅读文章的同学可以尝试画一下，我总结一下我读完文章后的理解：
    1、redis的整体启动流程是按照 【初始化默认配置】-&gt;【解析启动命令】-&gt;【初始化server】-&gt;【初始化并启动事件驱动框架】 进行
    2、整个运行中的redis，其实就是一个永不停歇的while循环，位于aeMain中（运行中的事件驱动框架）
    3、在事件驱动框架中有两个钩子函数 beforeSleep 和 aftersleep，在每次while循环中都会触发这两个函数，后面用来实现事件触发的效果

此外我发现了一个细节点：我在近期版本的redis6的分支上，发现在启动事件驱动框架之前（执行aeMain之前）会执行一个redisSetCpuAffinity函数，其效果有点类似于绑核的效果，那么是否可以认为从redis6开始其实不需要运维帮忙绑核redis自身就能做到绑核的效果呢？</div>2021-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/ee/46/7d65ae37.jpg" width="30px"><span>木几丶</span> 👍（3） 💬（1）<div>简易版启动流程：
初始化默认配置-&gt;解析启动参数和配置文件覆盖默认配置-&gt;初始化server-&gt;启动事件驱动框架</div>2021-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/72/e7bc6ff1.jpg" width="30px"><span>零点999</span> 👍（1） 💬（0）<div>mac环境下使用clion软件debug redis源码的配置过程：
https:&#47;&#47;www.toutiao.com&#47;article&#47;7214017532637004346&#47;?log_from=bc6912dd0e87f_1679699758013</div>2023-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/cf/a0315a85.jpg" width="30px"><span>lzh2nix</span> 👍（1） 💬（0）<div>在这一讲中大部分逻辑都是在initSerer中完成，所以对initSerer函数的理解也是重中之重。
initSerer(void initServer(void))
 \
  1.  server 结构体的初始化
  2.  sharedObject 创建(createSharedObjects())
  3.  创建事件驱动框架(aeCreateEventLoop())
  4.  监听tcp端口(listenToPort())
  5.  监听unix socket(anetUixServer())
  6.  redis DB 初始化
  7.  系统状态设置(staat&#47;cron&#47;aof&#47;rdb 等状态)
  8.  将timer事件添加到eventLoop中(aeCreateTimeEvent(...serverCron))
  9.  接受tcp连接事件添加到eventLoop中(aeCreateFileEvent(...acceptTcpEVent))
  10. 接受到unix socket连接的事件添加到eventLoop中(aeCreateFileEvent(acceptUnixHandler))	
  11. server中cluster 相关配置的初始化
  12. replicationScriptCacheInit()&#47;scriptingInit()&#47;scriptingInit()&#47;latencyMonitorInit()
</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/72/e7bc6ff1.jpg" width="30px"><span>零点999</span> 👍（0） 💬（0）<div>server.supervised = redisIsSupervised(server.supervised_mode);int background = server.daemonize &amp;&amp; !server.supervised;if (background) daemonize();...}
Redis 可以配置以守护进程的方式启动（配置文件 daemonize = yes）</div>2023-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/cf/5e2ce2bc.jpg" width="30px"><span>瞭望站在风口的猪</span> 👍（0） 💬（1）<div>老师好，我发现有一处逻辑错了，是先检查RBD再检查AOF吧

if (strstr(argv[0],&quot;redis-check-rdb&quot;) != NULL)
        redis_check_rdb_main(argc,argv,NULL);
    else if (strstr(argv[0],&quot;redis-check-aof&quot;) != NULL)
        redis_check_aof_main(argc,argv);</div>2022-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/cf/a0315a85.jpg" width="30px"><span>lzh2nix</span> 👍（0） 💬（0）<div>在这一讲中大部分逻辑都是在initSerer中完成，所以对initSerer函数的理解也是重中之重。
initSerer(void initServer(void))
 \
  1.  server 结构体的初始化
  2.  sharedObject 创建(createSharedObjects())
  3.  创建事件驱动框架(aeCreateEventLoop())
  4.  监听tcp端口(listenToPort())
  5.  监听unix socket(anetUixServer())
  6.  redis DB 初始化
  7.  系统状态设置(staat&#47;cron&#47;aof&#47;rdb 等状态)
  8.  将timer事件添加到eventLoop中(aeCreateTimeEvent(...serverCron))
  9.  接受tcp连接事件添加到eventLoop中(aeCreateFileEvent(...acceptTcpEVent))
  10. 接受到unix socket连接的事件添加到eventLoop中(aeCreateFileEvent(acceptUnixHandler))	
  11. server中cluster 相关配置的初始化
  12. replicationScriptCacheInit()&#47;scriptingInit()&#47;scriptingInit()&#47;latencyMonitorInit()</div>2021-08-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKGYB743jGRasUxqpkrBLgbRoLVwVP4MgePOWDMjrBDBGtn0us1vvUDzPIJPfibIbytSrEqUq8ib5Qw/132" width="30px"><span>haha</span> 👍（0） 💬（1）<div>老师的这些图是用什么软件画的啊</div>2021-08-21</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLm8skz4F7FGGBTXWUMia6qVEc00BddeXapicv5FkAx62GmOnUNEcE4scSR60AmappQoNdIQhccKsBA/132" width="30px"><span>末日，成欢</span> 👍（0） 💬（3）<div>起始处设置随机种子是为了做什么？</div>2021-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（6）<div>请问老师，Redis server 会先读取 AOF；而如果没有 AOF，则再读取 RDB。为什么不先读rdb，再读aof呢？</div>2021-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6c/b5/32374f93.jpg" width="30px"><span>可怜大灰狼</span> 👍（0） 💬（0）<div>先判断是否upstart或者systemd托管。再判断是否需要守护进程，内部还是fork+setsid</div>2021-08-12</li><br/>
</ul>