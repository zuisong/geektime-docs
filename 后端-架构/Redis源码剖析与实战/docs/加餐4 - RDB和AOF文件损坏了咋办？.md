你好，我是蒋德钧。今天的加餐课程，我来和你聊聊Redis对损坏的RDB和AOF文件的处理方法。

我们知道，Redis为了提升可靠性，可以使用AOF记录操作日志，或者使用RDB保存数据库镜像。AOF文件的记录和RDB文件的保存都涉及写盘操作，但是，如果在写盘过程中发生了错误，就会导致AOF或RDB文件不完整。而Redis使用不完整的AOF或RDB文件，是无法恢复数据库的。那么在这种情况下，我们该怎么处理呢？

实际上，Redis为了应对这个问题，就专门实现了针对AOF和RDB文件的完整性检测工具，也就是redis-check-aof和redis-check-rdb两个命令。今天这节课，我就来给你介绍下这两个命令的实现以及它们的作用。学完这节课后，如果你再遇到无法使用AOF或RDB文件恢复Redis数据库时，你就可以试试这两个命令。

接下来，我们先来看下AOF文件的检测和修复。

## AOF文件检测与修复

要想掌握AOF文件的检测和修复，我们首先需要了解下，AOF文件的内容格式是怎样的。

### AOF文件的内容格式

AOF文件记录的是Redis server运行时收到的操作命令。当Redis server往AOF文件中写入命令时，它会按照RESP 2协议的格式来记录每一条命令。当然，如果你使用了Redis 6.0版本，那么Redis会采用RESP 3协议。我在第一季的时候，曾经给你介绍过Redis客户端和server之间进行交互的[RESP 2协议](https://time.geekbang.org/column/article/298504)，你可以再去回顾下。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（8） 💬（0）<div>1、RDB 和 AOF 文件在写盘故障时，可能发生损坏不完整的情况，那使用其恢复数据就会出现问题，所以 Redis 提供了 2 个命令来检测文件是否有错误

2、要想检测出文件错误，那说明 RDB 和 AOF 必定是按照某种固定格式写入的，检测是否完整只需要按照其格式规则，发现不符即认为文件不完整

3、redis-check-rdb 命令检测 RDB，因为 RDB 有明确的文件头、数据部分、文件尾，读取文件发现不完整即报错

4、redis-check-aof 命令检测 AOF，AOF 按照 RESP 协议写入，按照这个协议可以读取每个命令参数个数、参数字符串长度，如果不符合协议格式，则说明不完整。但这个命令提供了 --fix 命令，可以修复 AOF 文件，实现原理是：把不完整的命令和后续部分，直接从 AOF 中删除

课后题：redis_check_aof_main 函数是检测 AOF 文件的入口函数，但是它还会调用检测 RDB 文件的入口函数 redis_check_rdb_main，它的作用是什么？

Redis 在 4.0 版本支持了「混合持久化」，即在 AOF rewrite 期间，先以 RDB 格式写入到 AOF 文件中，再把后续命令追加到 AOF 中，这样 AOF rewrite 后的文件既包括了 RDB 格式，又包含 AOF 格式（目的是为了让 AOF 体积更小），所以 redis_check_rdb_main 在检测 AOF 文件时，RDB 和 AOF 文件格式都需要检测。</div>2021-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/7e/5a/da39f489.jpg" width="30px"><span>Ethan New</span> 👍（0） 💬（0）<div>redis 4.0后提供了aof rewrite的功能，重写后的aof文件既有RDB格式的数据也有AOF格式的命令，redis_check_aof_main调用redis_check_rdb_main就是为了检测文件中RDB格式的数据。</div>2021-10-05</li><br/>
</ul>