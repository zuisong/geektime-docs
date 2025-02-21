你好，我是蒋德钧。这节课，我们一起来看看Redis是如何在源码中实现哨兵机制的。

我们知道，Redis主从复制是保证Redis可用性的一个重要手段。而一旦Redis主节点发生故障，哨兵机制就会执行故障切换。这个故障切换过程实现起来其实比较复杂，涉及了哨兵Leader选举、新主节点选举和故障切换等关键操作。但同时，这个故障切换过程又是我们在实现高可用系统时经常要面对的开发需求。

所以从这节课开始，我就来给你逐一介绍下，Redis哨兵机制及其实现故障切换的关键技术设计与实现。通过这部分内容的学习，你既可以了解在故障切换过程中，起到重要作用的Raft协议是如何实现的，而且你还可以掌握在故障切换时，主节点、从节点和客户端相互之间如何完成切换通知的。

不过，在开始了解故障切换的关键技术之前，今天我们会先来了解哨兵实例本身的初始化和基本运行过程，这是因为从源码的角度来看，哨兵实例和常规Redis实例的实现都是在一套源码中的，它们共享了一些执行流程。所以了解这部分内容，也可以帮助我们更加清楚地掌握哨兵实例的实现机制。

好，下面我们就先来看下哨兵实例的初始化过程。

## 哨兵实例的初始化

因为哨兵实例是属于运行在一种特殊模式下的Redis server，而我在[第8讲](https://time.geekbang.org/column/article/406556)中，已经给你介绍过了Redis server启动后的入口函数main的整体执行过程。其实，这个过程就包含了哨兵实例的初始化操作。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（16） 💬（0）<div>1、哨兵和 Redis 实例是一套代码，只不过哨兵会根据启动参数（redis-sentinel 或 redis-server --sentinel），设置当前实例为哨兵模式（server.sentinel_mode = 1），然后初始化哨兵相关数据

2、哨兵模式的实例，只能执行一部分命令（ping、sentinel、subscribe、unsubscribe、psubscribe、punsubscribe、publish、info、role、client、shutdown、auth），其中 sentinel、publish、info、role 都是针对哨兵专门实现的

3、之后哨兵会初始化各种属性，例如哨兵实例 ID、用于故障切换的当前纪元、监听的主节点、正在执行的脚本数量、与其他哨兵实例发送的 IP 和端口号等信息

4、启动哨兵后，会检查配置文件是否可写（不可写直接退出，哨兵需把监控的实例信息写入配置文件）、是否配置了哨兵 ID（没配置随机生成一个）

5、最后哨兵会在监控的 master 实例的 PubSub（+monitor 频道）发布一条消息，表示哨兵开始监控 Redis 实例

6、哨兵后续会通过 PubSub 的方式，与主从库、其它哨兵实例进行通信

课后题：哨兵实例本身是有配置文件 sentinel.conf 的，那么在哨兵实例的初始化过程中，解析这个配置文件的函数在哪？

Redis 启动时，会在 main 函数中调用 loadServerConfig 加载配置文件，loadServerConfig 函数会读取配置文件中的内容，然后调用 loadServerConfigFromString 函数解析具体的配置项。

loadServerConfigFromString 函数中，其中有一个分支，对哨兵模式进行了判断，如果是哨兵模式，则调用 sentinelHandleConfiguration 函数解析哨兵配置项。

所以，函数调用链为 main -&gt; loadServerConfig（读出配置文件内容） -&gt; loadServerConfigFromString（解析配置项） -&gt; sentinelHandleConfiguration（解析哨兵配置项）。</div>2021-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（3） 💬（0）<div>回答老师的问题：sentinel.conf 是在哪读取的？
    答:redis应该是实现了一套通用的配置文件读取方法loadServerConfig，可以解析文件，也可以直接解析字符串

主要步骤如下所示：
    1、哨兵启动的两种方式都显示，配置文件会根据参数传入，而解析后应该是赋值给configfile
        redis-sentinel sentinel.conf[文件路径]
        redis-server sentinel.conf[文件路径] —sentinel

    2、在loadServerConfig方法上方有一个判断，当前模式如果是哨兵，那么如果发现没有配置文件就会直接退出。
        if (server.sentinel_mode &amp;&amp; configfile &amp;&amp; *configfile == &#39;-&#39;) {
            serverLog(LL_WARNING,
                &quot;Sentinel config from STDIN not allowed.&quot;);
            serverLog(LL_WARNING,
                &quot;Sentinel needs config file on disk to save state.  Exiting...&quot;);
            exit(1);
        }

    3、基于前两个步骤，最终调用loadServerConfig，而入参configfile就是哨兵的配置文件了，方法签名如下：
        void loadServerConfig(char *filename, char *options)

    4、最终调用loadServerConfig去解析配置文件
     文件开启代码如下：
        &#47;&#47;将读取出来的内容转换为sds动态字符
        sds config = sdsempty();
        char buf[CONFIG_MAX_LINE+1];
        if (filename) {
        FILE *fp;

        if (filename[0] == &#39;-&#39; &amp;&amp; filename[1] == &#39;\0&#39;) {
            fp = stdin;
        } else {
            &#47;&#47;读取文件
            if ((fp = fopen(filename,&quot;r&quot;)) == NULL) {
                serverLog(LL_WARNING,
                    &quot;Fatal error, can&#39;t open config file &#39;%s&#39;&quot;, filename);
                exit(1);
            }
        }
        while(fgets(buf,CONFIG_MAX_LINE+1,fp) != NULL)
            config = sdscat(config,buf);
        if (fp != stdin) fclose(fp);
    }
        

    5、调用loadServerConfigFromString去解析读取出来的文件字符串
        调用路径 loadServerConfig -&gt; loadServerConfigFromString</div>2021-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/cf/851dab01.jpg" width="30px"><span>Milittle</span> 👍（2） 💬（0）<div>在main函数中：loadServerConfig这个函数用来load sentinel.conf。
loadSentinelConfigFromQueue 在哨兵模式下的特殊load函数。</div>2021-09-23</li><br/>
</ul>