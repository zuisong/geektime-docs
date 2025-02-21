你好，我是鸟窝。

哈希表（Hash Table）这个数据结构，我们已经非常熟悉了。它实现的就是key-value之间的映射关系，主要提供的方法包括Add、Lookup、Delete等。因为这种数据结构是一个基础的数据结构，每个key都会有一个唯一的索引值，通过索引可以很快地找到对应的值，所以使用哈希表进行数据的插入和读取都是很快的。Go语言本身就内建了这样一个数据结构，也就是**map数据类型**。

今天呢，我们就先来学习Go语言内建的这个map类型，了解它的基本使用方法和使用陷阱，然后再学习如何实现线程安全的map类型，最后我还会给你介绍Go标准库中线程安全的sync.Map类型。学完了这节课，你可以学会几种可以并发访问的map类型。

## map的基本使用方法

Go内建的map类型如下：

```
map[K]V
```

其中，**key类型的K必须是可比较的**（comparable），也就是可以通过 == 和 !=操作符进行比较；value的值和类型无所谓，可以是任意的类型，或者为nil。

在Go语言中，bool、整数、浮点数、复数、字符串、指针、Channel、接口都是可比较的，包含可比较元素的struct和数组，这俩也是可比较的，而slice、map、函数值都是不可比较的。
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/c1/0e/2b987d54.jpg" width="30px"><span>蜉蝣</span> 👍（9） 💬（3）<div>老师好，我看到 read 中 key 被删除会有两个状态：nil 和 expunged。我会有些不明白，要么都用 nil 或者都用 expunged，这样会不会更好一些？</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/0f/f6/609ded9f.jpg" width="30px"><span>tingting</span> 👍（1） 💬（1）<div>想问一下老师，以下这种情况会有data race吗？
m:=make(map[string]int)
Goroutine A: 不停地覆盖m指向新的map值
Goroutine B: 不停地读m里面的某个key</div>2022-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/02/ff/e21a97c1.jpg" width="30px"><span>叶小彬</span> 👍（0） 💬（1）<div>老师，我看了sync.Map 源码，有两点不是很懂
1、设计read和dirty的想法是什么
因为sync.Map里，read结构本身就是atomic.Value，增加和修改有Store方法，本身就可以防止幻读，脏读的问题，如果是为了delete的逻辑（我发现atomic.Value里是没有delete方法的），那完全可以写一个加锁逻辑的delete，个人感觉dirty的没什么用
2、源码里的逻辑是，当read 的miss次数大于等于dirty的长度的时候，就将dirty转成read，这个是什么设计想法</div>2021-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cf/cc/8de5007b.jpg" width="30px"><span>徐改</span> 👍（0） 💬（1）<div>还是不太明白为什么在创建dirty的时候，要将read中未删除的entry拷贝给dirty.
sync.map一个优秀的地方是当我们访问read的时候不需要上锁，访问dirty的时候需要加锁。在Load()方法中，我们每次都是先访问read，如果read中没有的话才访问dirty。那么对于dirty来说，dirty中的数据可能read没有，或者read有。read中有的数据，dirty有；read中没有的数据，dirty可能会有。而我们的程序每次都是先访问read，如果read没有后续才会访问dirty，那这样的话创建dirty的时候，感觉可以不用将read中的entry一个一个拷贝到dirty中，因为我们访问是先访问read的。</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/59/d3/696b1702.jpg" width="30px"><span>校歌</span> 👍（0） 💬（1）<div>老师，发现有个地方不严谨，”map不可比较”。我写了个小程序，提示map只可以跟nil比较，而不是不能比较。（可能有点扣字眼了）
.&#47;main.go:11:12: invalid operation: resMap == resMap (map can only be compared to nil)</div>2021-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/fd/47/499339d1.jpg" width="30px"><span>新味道</span> 👍（0） 💬（1）<div>新加的元素需要放入到 dirty 中，如果 dirty 为 nil，那么需要从 read 字段中复制出来一个 dirty 对象。

---
为什么需要从 read 字段中复制出来一个 dirty 对象？
</div>2020-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（3）<div>应该着重说明一下为什么有expunged这种状态,这点比较迷惑。我能理解expunged的entry代表read中存在而dirty中不存在。但为什么在read向dirty复制时，需要将nil的entry变为expunged？</div>2020-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/47/d217c45f.jpg" width="30px"><span>Panmax</span> 👍（0） 💬（1）<div>文章中写到「所以，这里我们就超前一把，我带你直接体验这个即将要发布的泛型方案。」

是我对泛型的理解有什么误会吗，下文中并没有看到使用泛型的地方������。</div>2020-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ab/a9/590d6f02.jpg" width="30px"><span>Junes</span> 👍（32） 💬（5）<div>1. 双检查主要是针对高并发的场景：
第一次先用CAS快速尝试，失败后进行加锁，然后进行第二次CAS检查，再进行修改；
在高并发的情况下，存在多个goroutine在修改同一个Key，第一次CAS都失败了，在竞争锁；如果不进行第二次CAS检查就直接修改，这个Key就会被多次修改；

2. 真正删除key的操作是在数据从read往dirty迁移的过程中（往dirty写数据时，发现dirty没有数据，就会触发迁移），只迁移没有被标记为删除的KV</div>2020-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（14） 💬（1）<div>看到本文的标题,就让我想到之前看过的一篇文章:
[踩了 Golang sync.Map 的一个坑](https:&#47;&#47;gocn.vip&#47;topics&#47;10860)

就是老师文章代码中的一行注释的由来:
`这一行长坤在1.15中实现的时候忘记加上了，导致在特殊的场景下有些key总是没有被回收`

当时我是好好把系统的sync.Map代码看了一下.
虽然才短短384行代码,但还是花了不少功夫.

另外,推荐一个 欧长坤 未完工的开源电子书 [Go 语言原本](https:&#47;&#47;github.com&#47;golang-design&#47;under-the-hood).
</div>2020-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2e/7e/ebc28e10.jpg" width="30px"><span>NULL</span> 👍（9） 💬（2）<div>感觉有两个地方写的有点模糊，导致对后面的内容有些不明所以_(:з」∠)_
1是 “通过冗余的两个数据结构（只读的 read 字段、可以 dirty）”，可以 dirty 是笔误吗
2是 “动态调整。miss 次数多了之后”，miss是什么？

查了下其他资料，dirty指 将最新写入的数据则存在 dirty 字段上
misses 字段用来统计 read 被穿透的次数（被穿透指需要读 dirty 的情况）
这样理解起来好多了_(:з」∠)_</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/61/93/3191eafa.jpg" width="30px"><span>TT</span> 👍（5） 💬（0）<div> 1. 为什么说 read 是并发读写安全的？
 2. read 为什么可以更新 key 对应的 value？dirty 中会同步更新吗？
 3. map 的 misses 是什么？干嘛用的？
 4. 什么时候 misses 会变化？
 5. readOnly 的 amended 是什么？
 6. 什么时候会改变 amended？
 7. 定义 expunged 是干什么用的？标记清除到底是怎么标记的？又是怎么清除的？

自己写了一篇总结 http:&#47;&#47;zero-tt.fun&#47;go&#47;sync-map&#47; ，希望可以和大家讨论</div>2021-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/85/2b/5c489bc1.jpg" width="30px"><span>阿梅</span> 👍（1） 💬（0）<div>map并发读写不只是panic，而是直接宕机， 也就是无法通过recover捕获后继续执行程序</div>2023-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（0）<div>concurrent-map，新知识点get，项目中用起来。</div>2022-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/34/67/06a7f9be.jpg" width="30px"><span>while (1)等;</span> 👍（0） 💬（0）<div>老师好！
type RWMap struct { &#47;&#47; 一个读写锁保护的线程安全的map
    sync.RWMutex &#47;&#47; 读写锁保护下面的map字段
    m map[int]int
}
&#47;&#47; 新建一个RWMap
func NewRWMap(n int) *RWMap {
    return &amp;RWMap{
        m: make(map[int]int, n),
    }
}
这里初始化map的时候为什么用的是&amp;RWMap</div>2021-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2a/e6/c788257f.jpg" width="30px"><span>geek_arong2048</span> 👍（0） 💬（0）<div>Map并发安全优化：
1、读写锁
2、CAS、Atomic原子操作
3、分段锁</div>2021-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b8/3c/1a294619.jpg" width="30px"><span>Panda</span> 👍（0） 💬（0）<div>map 很常用  有两个问题 

 1 无序 可以用 第三方 ordermap 解决  
2. 并发问题   可以加锁 或者分片
PS:  官方的 sync.map  不太常用</div>2021-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/17/11/a63acc6a.jpg" width="30px"><span>( ･᷄ὢ･᷅ )</span> 👍（0） 💬（0）<div>作业：
1.为了防止在第一次检查后加锁前并发运行的其他Store操作对其进行了增加。即把dirty复制给read.m、
2.真正删除是在在readonly中没有查询到数据且amended标记为true 的时候进行了删除</div>2020-12-27</li><br/><li><img src="" width="30px"><span>Geek_194084</span> 👍（0） 💬（0）<div>大佬，函数的返回值应该可以比较把</div>2020-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/dd/7d/5d3ab033.jpg" width="30px"><span>不求闻达</span> 👍（0） 💬（0）<div>map</div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c4/f3/92f654f1.jpg" width="30px"><span>Bug? Feature!</span> 👍（0） 💬（0）<div>没有竞争，就没有伤害！
为啥要再次加锁？
为了安全，我知道java就有重排序啥的</div>2020-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/6e/76b4aa3d.jpg" width="30px"><span>橙子888</span> 👍（0） 💬（0）<div>看完打卡。</div>2020-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（0） 💬（1）<div>分片索引值计算也消耗一部分时间的吧？
</div>2020-10-30</li><br/>
</ul>