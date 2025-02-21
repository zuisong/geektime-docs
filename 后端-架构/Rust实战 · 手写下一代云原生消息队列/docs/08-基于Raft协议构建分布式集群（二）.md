> 本课程为精品小课，不标配音频

你好，我是文强。

这节课我们继续完善基于 Raft 协议开发的分布式集群，我们会完成存储层和网络层这两部分的开发。接上节课的内容，我们首先来看一下 RaftMachineStorage 的实现逻辑。

## Raft 存储层：RaftMachineStorage

从代码上看，RaftMachineStorage 的作用是**使用 RocksDB 来持久化存储 Raft 运行数据**。由于 RaftMachineStorage 的代码较多，这里我就不把全部代码贴出来了，建议你先去看一下文件[《RaftMachineStorage》](https://github.com/robustmq/robustmq-geek/blob/main/src/placement-center/src/storage/raft.rs)中的代码。

下面这张图是 RaftMachineStorage 的功能列表。

![图片](https://static001.geekbang.org/resource/image/fe/4a/fe0d4abcfdecb8d609b444e96aa2484a.png?wh=1084x1364)

从函数名称中可以知道，RaftMachineStorage 的功能就是对 Entry、HardState、ConfState、First Index、Last Idnex、Uncommit Index、Snapshot 等数据进行读写。

因为 RocksDB 是 KV 存储模型，因此我们需要先定义保存数据的 Key。来看下面这段代码：

```plain
// 存储未过期的第一个Entry的Index
pub fn key_name_by_first_index() -> String {
    return "/raft/first_index".to_string();
}


// 存储最新的一个 Entry 的Index
pub fn key_name_by_last_index() -> String {
    return "/raft/last_index".to_string();
}


// 保存 Raft 元数据 HardState
pub fn key_name_by_hard_state() -> String {
    return "/raft/hard_state".to_string();
}


// 保存 Raft 元数据 ConfState
pub fn key_name_by_conf_state() -> String {
    return "/raft/conf_state".to_string();
}


// 根据Entry的 Index 保存Entry 信息
pub fn key_name_by_entry(idx: u64) -> String {
    return format!("/raft/entry/{}", idx);
}


// 保存未正常 commit 的index列表
pub fn key_name_uncommit() -> String {
    return "/raft/uncommit_index".to_string();
}


// 保存快照信息
pub fn key_name_snapshot() -> String {
    return "/raft/snapshot".to_string();
}


```
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/c8/33/2d4c464b.jpg" width="30px"><span>zhuxiufenghust</span> 👍（0） 💬（0）<div>create_snapshot调用的read_all有点疑问，rocksdb存储的都是kv格式数据，entry、last_index等数据存储没有什么区别，那read_all是如何做到只读取到entry的</div>2024-12-20</li><br/>
</ul>