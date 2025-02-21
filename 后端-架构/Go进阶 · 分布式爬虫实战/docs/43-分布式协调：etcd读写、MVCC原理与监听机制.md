你好，我是郑建勋。

这节课，我们重点来看看etcd的读写流程，以及它的两个重要特性：MVCC原理和监听机制。

## 写的完整流程

我们先来看看etcd怎么完整地写入请求。

![图片](https://static001.geekbang.org/resource/image/b4/bb/b4bfe7313049f3cb46d846d977cf75bb.jpg?wh=1920x846)

1. 客户端通过GRPC协议访问etcd-server服务端。
2. 如果是一个写请求，会访问etcd-server注册的Put方法。要注意的是，在访问etcd-server时，会进行一些检查，例如DB配额（Quota）的检查。此外，如果客户端访问的节点不是Leader节点，这个节点会将请求转移到Leader中。
3. etcd-server会调用raft-node模块的Propose方法进行限速、鉴权等判断，之后raft-node模块调用etcd-raft模块完成数据的封装。
4. 接着，etcd-raft模块会将封装后的数据返回给raft-node模块。
5. raft-node模块调用storage存储模块，将本次操作对应的Entry记录存储到WAL日志文件当中。
6. raft-node模块将当前Entry广播给集群中的其他节点，snap模块还会在适当时候保存当前数据的快照。
7. 当Leader最终收到了半数以上节点的确认时，该Entry的状态会变为committed ，这时etcd-raft模块会将Commit Index返回上游，供etcd-server模块执行。后面我们还会看到，etcd-server实现了MVCC机制，维护了某一个Key过去所有的版本记录。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（3） 💬（1）<div>思考题：
一 treeIndex 的结构为什么是 B 树而不是哈希表或者是二叉树？
不使用【hash表】的原因：
1. hash表不支持范围查询；
2. hash表可能有hash碰撞的问题(Hash_fn(k1) = Hash_fn(key2),还需要使用其他方法进行进一步处理(如:拉链法)；
3. hash表不支持排序；
4. hash表不支持key的前缀索引,prefix=xxx,想必是用不了;

不使用【二叉树】的原因:
1. 二叉树造成树的层次太高,查找的时候，可能造成磁盘IO的次数较多,性能不好.

二 如果这个时候节点崩溃了，如何保证数据不丢失呢？
应该是通过WAL进行保障，先写日志在提交.

这样看，很多思路与MySQL相似.</div>2023-01-17</li><br/><li><img src="" width="30px"><span>Geek_c3c15b</span> 👍（0） 💬（2）<div>怎么又是一整篇理论知识，实战课的重点不是实战吗？极客时间已经有etcd的专栏了</div>2023-02-22</li><br/>
</ul>