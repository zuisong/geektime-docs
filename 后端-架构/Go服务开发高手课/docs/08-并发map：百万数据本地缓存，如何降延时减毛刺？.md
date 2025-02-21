你好，我是徐逸。

在上节课的内容中，我们一起学习了锁和无锁编程技术，还使用分段锁和map类型，实现了一个缓存结构。不过，值得留意的是，其实 Go 语言的 sync 包已经提供了一种并发安全的 Map 类型。

今天，我就以大规模数据缓存的数据结构设计要点为例，带你掌握sync.Map类型以及针对map的GC优化技巧。

假如我们现在需要实现一个key-value类型的本地缓存，且缓存的key特别多，达到百万甚至千万级别，那么我们该怎么设计，才能在并发环境下高性能、安全地访问这个缓存呢？

针对大规模数据缓存的场景，我们在数据结构设计上要考虑的技术点有两个。

1. 如何实现并发安全的map类型。
2. 如何减少甚至避免因大规模数据缓存导致的GC开销。

## 并发map选择

实际上，大规模且有读写操作的数据缓存，咱们可以考虑的map类型有两种，一个是分段锁实现的map类型，另一个是sync包提供的Map类型。

那么我们到底该选择哪个呢？

在选型之前，我们需要先掌握sync.Map类型的基础知识和原理。

sync.Map是 Go 语言sync包中提供的一个内置的并发安全的map类型。它在设计上考虑了高并发场景，尽量避免加锁操作从而提升读写性能。

sync.Map该如何使用呢？下面我给了一段简单的代码，这段代码使用了sync.Map提供的Store、Load和Delete方法，分别用于写、读和删除操作。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/CBKaSBa3Hsj6XicVHHYk34pFCmnicRg9141ic8IJicb09hRQgia2Y2gyftYroRfficJEZOYZthghI6oianycmzJvmC6wQ/132" width="30px"><span>Geek_e73ba0</span> 👍（1） 💬（1）<div>cache.Set(&quot;my-unique-key&quot;, []byte(&quot;value&quot;)) 这里的key是&quot;my-unique-key&quot;，不就是字符串吗？按照之前的说法，字符串底层数据结构中有指向数组的指针，是不符合条件的，这不是自相矛盾吗？还好我有deepseek和GPT 03-mini，通过它俩得知，用户侧接口的抽象：Set(key string, value []byte) 只是 API 接口，实际存储时：

将 key 转换为 uint64 哈希值（无指针）

将 key 和 value 序列化为二进制存入 entries（无指针结构）

最终存储结构无指针：核心存储结构 map[uint64]uint32 和 []byte 均不含指针，GC 完全忽略。适用场景与限制
1. 最佳适用场景
海量小对象缓存（如缓存会话数据、配置项）

高吞吐量场景（需要极低 GC 开销）

键值无需遍历（bigcache 不支持遍历操作）

2. 主要限制
内存不可回收：entries 数组采用预分配+环形缓冲区设计，旧数据会被新数据覆盖，但无法主动释放内存。

无持久化能力：纯内存缓存，进程退出后数据丢失。

总结
bigcache 通过以下设计实现 GC 优化：

哈希值映射：将字符串键转换为无指针的 uint64。

连续内存存储：键值数据以二进制形式存储在 []byte 数组中，避免指针。

无指针哈希表：map[uint64]uint32 的键值均为基本类型，GC 不会扫描。

用户代码中看似使用了带指针的字符串键，但通过内部转换，最终存储结构完全不含指针，完美契合 Go 的 GC 优化机制。</div>2025-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/00/f0/fe94061e.jpg" width="30px"><span>假装在养🐷</span> 👍（0） 💬（1）<div>老师，这句话的具体含义能解释一下吗
read 存储了部分写入 Map 的内容，用来加速读操作。而 dirty 存储了全量内容，需要加锁才能读写数据。 </div>2024-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/19/fe/d31344db.jpg" width="30px"><span>lJ</span> 👍（0） 💬（1）<div>1. 只支持 []byte 类型的数据存储，不支持复杂的数据结构，需要自行序列化和反序列化数据，增加了开发复杂度。
2. 使用环形缓冲区存储数据，数据写入时是连续分配的，但删除时只标记为无效，不回收空间。导致内存利用率降低。</div>2024-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/7e/01/1660e1e8.jpg" width="30px"><span>快叫我小白</span> 👍（0） 💬（1）<div>runtime.GC 这个函数为何在函数内外都调用一次呀？而且测试函数似乎没产生需要回收的临时结构体，我们调用GC函数仅仅是为了观察垃圾回收的扫描时间吗？</div>2024-12-25</li><br/>
</ul>