你好，我是俊达。

之前在评论区有同学留言问是否能加一讲源代码调试的内容。考虑到这个专栏中有相当多的篇幅是讲MySQL和InnoDB的内部实现机制，而我自己在整理这些内部原理时，也参考了大量的MySQL源码，有时也会用GDB来调试跟踪代码的执行，因此在这一讲中，我们就来聊聊MySQL源码分析和GDB在源码分析中的一些使用场景。

这里我们只讨论MySQL的源码分析，不涉及到怎么修改MySQL源码来实现一些定制化的功能。

## MySQL源码介绍

这一讲中，我们就以当前8.0系列中最新的Release版本8.0.40为例，下载代码并解压。我们先简单看一下MySQL源码文件的组织（只是为了看结构，下面的输出中，把很多内容删减掉了）。

```plain
# tree -d -L 2
...
├── include
├── mysys
├── plugin
│   ├── auth
│   ├── clone
...
│   ├── group_replication
...
│   ├── semisync
│   └── x
......
├── sql
│   ├── auth
│   ├── binlog
│   ├── changestreams
│   ├── conn_handler
│   ├── containers
│   ├── daemon_proxy_keyring
│   ├── dd
│   ├── examples
│   ├── gis
│   ├── histograms
│   ├── iterators
│   ├── join_optimizer
│   ├── locks
│   ├── memory
│   ├── partitioning
│   ├── protobuf
│   ├── raii
│   ├── range_optimizer
│   ├── server_component
│   └── xa
├── sql-common
│   └── oci
├── storage
......
│   ├── innobase
│   └── temptable
└── vio
```
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/29/3c/48/38f84bbc.jpg" width="30px"><span>小猪猪猪蛋</span> 👍（1） 💬（1）<div>讲的非常详细，一步一步跟下来 受益匪浅！ 谢谢老师</div>2024-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5b/4f/e9092c74.jpg" width="30px"><span>hDEC2突变</span> 👍（0） 💬（1）<div>进入某个线程用thread n ，info threads显示当前的所有线程，正在运行的前面有*号
老师，有个问题，就是p thread_id和info threads里面的线程id都不对应，我想知道某个函数运行的时候调用的哪个线程，如何确定？</div>2025-01-27</li><br/>
</ul>