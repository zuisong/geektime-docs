你好，我是蒋德钧。

字符串在我们平时的应用开发中十分常见，比如我们要记录用户信息、商品信息、状态信息等等，这些都会用到字符串。

而对于Redis来说，键值对中的键是字符串，值有时也是字符串。我们在Redis中写入一条用户信息，记录了用户姓名、性别、所在城市等，这些都是字符串，如下所示：

```
SET user:id:100 {“name”: “zhangsan”, “gender”: “M”,“city”:"beijing"}
```

此外，Redis实例和客户端交互的命令和数据，也都是用字符串表示的。

那么，既然字符串的使用如此广泛和关键，就使得我们在实现字符串时，需要尽量满足以下三个要求：

- 能支持丰富且高效的字符串操作，比如字符串追加、拷贝、比较、获取长度等；
- 能保存任意的二进制数据，比如图片等；
- 能尽可能地节省内存开销。

其实，如果你开发过C语言程序，你应该就知道，在C语言中可以使用**char\*字符数组**来实现字符串。同时，C语言标准库string.h中也定义了多种字符串的操作函数，比如字符串比较函数strcmp、字符串长度计算函数strlen、字符串追加函数strcat等，这样就便于开发者直接调用这些函数来完成字符串操作。

所以这样看起来，**Redis好像完全可以复用C语言中对字符串的实现呀？**

但实际上，我们在使用C语言字符串时，经常需要手动检查和分配字符串空间，而这就会增加代码开发的工作量。而且，图片等数据还无法用字符串保存，也就限制了应用范围。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/44/cf/a0315a85.jpg" width="30px"><span>lzh2nix</span> 👍（18） 💬（2）<div>个人觉得这里使用__attribute__ ((__packed__))除了节省内存空间之外，还有一个很精妙的设计就是在packed之后可以通过以下的方式来获取flags字段

	unsigned char flags = s[-1];
    
    switch(flags&amp;SDS_TYPE_MASK) {
        case SDS_TYPE_5:
            return SDS_TYPE_5_LEN(flags);
        case SDS_TYPE_8:
            return SDS_HDR(8,s)-&gt;len;
        case SDS_TYPE_16:
            return SDS_HDR(16,s)-&gt;len;
        case SDS_TYPE_32:
            return SDS_HDR(32,s)-&gt;len;
        case SDS_TYPE_64:
            return SDS_HDR(64,s)-&gt;len;
    }

从而更进一步的得到struct的具体类型，如果是非1字节对齐的话，这里就不能这样操作。而sds中通过原始的char* 定位到sds的Header是设计的的**灵魂**</div>2021-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/cf/a0315a85.jpg" width="30px"><span>lzh2nix</span> 👍（2） 💬（1）<div>&quot;这两个元数据占用的内存空间在 sdshdr16、sdshdr32、sdshdr64 类型中，则分别是 2 字节、4 字节和 8 字节&quot;

这里的描述是是否有问题， sdshdr16中len， alloc这两个元数据占用的空间应该是4字节，其他两个类推。
struct __attribute__((__packed__))sdshdr16 {
        uint16_t len; &#47;*2字节*&#47;
        uint16_t alloc; &#47;* 2字节*&#47;
        unsigned char flags; &#47;* 1字节 *&#47;
        char buf[];
    };</div>2021-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（105） 💬（15）<div>char* 的不足：
- 操作效率低：获取长度需遍历，O(N)复杂度
- 二进制不安全：无法存储包含 \0 的数据

SDS 的优势：
- 操作效率高：获取长度无需遍历，O(1)复杂度
- 二进制安全：因单独记录长度字段，所以可存储包含 \0 的数据
- 兼容 C 字符串函数，可直接使用字符串 API

另外 Redis 在操作 SDS 时，为了避免频繁操作字符串时，每次「申请、释放」内存的开销，还做了这些优化：
- 内存预分配：SDS 扩容，会多申请一些内存（小于 1MB 翻倍扩容，大于 1MB 按 1MB 扩容）
- 多余内存不释放：SDS 缩容，不释放多余的内存，下次使用可直接复用这些内存

这种策略，是以多占一些内存的方式，换取「追加」操作的速度。

这个内存预分配策略，详细逻辑可以看 sds.c 的 sdsMakeRoomFor 函数。

课后题：SDS 字符串在 Redis 内部模块实现中也被广泛使用，你能在 Redis server 和客户端的实现中，找到使用 SDS 字符串的地方么？

1、Redis 中所有 key 的类型就是 SDS（详见 db.c 的 dbAdd 函数）

2、Redis Server 在读取 Client 发来的请求时，会先读到一个缓冲区中，这个缓冲区也是 SDS（详见 server.h 中 struct client 的 querybuf 字段）

3、写操作追加到 AOF 时，也会先写到 AOF 缓冲区，这个缓冲区也是 SDS （详见 server.h 中 struct client 的 aof_buf 字段）
</div>2021-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（13） 💬（3）<div>课后题：使用 SDS 字符串的地方？

1. server.h 文件中的 `redisObject` 对象，key 和 value 都是对象，key （键对象）都是 SDS 简单动态字符串对象
2. cluter.c 的 clusterGenNodesDescription 函数中。这个函数代表以 csv 格式记录当前节点已知所有节点的信息。
3. client.h 的 clusterLink 结构体中。clusterLink 包含了与其他节点进行通讯所需的全部信息，用 SDS 来存储输出缓冲区和输入缓冲区。
4. server.h 的 client 结构体中。缓冲区 querybuf、pending_querybuf 用的 sds 数据结构。
5. networking.c 中的 catClientInfoString 函数。获取客户端的各项信息，将它们储存到 sds 值 s 里面，并返回。
6. sentinel.c 中的 sentinelGetMasterByName 函数。根据名字查找主服务器，而参数名字会先转化为 SDS 后再去找主服务器。
7. server.h 中的结构体 redisServer，aof_buf 缓存区用的 是 sds。
8. slowlog.h 中的结构体 slowlogEntry，用来记录慢查询日志，其他 client 的名字和 ip 地址用的是 sds。

还有很多地方用到了，这里就不一一列举了，感兴趣的同学加我好友交流：passjava。

----------------------------------

详细说明：

（1）Redis 使用对象来表示数据库中的键和值，每次创建一个键值对时，都会创建两个对象：一个键对象，一个值对象。而键对象都是 SDS 简单动态字符串对象，值对象可以字符串对象、列表对象、哈希对象、集合对象或者有序集合对象。

对象的数据结构：

server.h 文件中的 `redisObject` 结构体定义如下：

```c
typedef struct redisObject {
    &#47;&#47; 类型
    unsigned type:4;
    &#47;&#47; 编码
    unsigned encoding:4;
    &#47;&#47; 对象最后一次被访问的时间
    unsigned lru:LRU_BITS; &#47;* LRU time (relative to global lru_clock) or
                            * LFU data (least significant 8 bits frequency
                            * and most significant 16 bits access time). *&#47;
    &#47;&#47; 引用计数
    int refcount;
    &#47;&#47; 指向实际值的指针
    void *ptr;
} robj;
```

再来看添加键值对的操作，在文件 db.c&#47;

```C
void dbAdd(redisDb *db, robj *key, robj *val)
```

第一个参数代表要添加到哪个数据库（Redis 默认会创建 16 个数据库，第二个代表键对象，第三个参数代表值对象。

dbAdd 函数会被很多 Redis 命令调用，比如 sadd 命令。

（Redis sadd 命令将一个或多个成员元素加入到集合中，已经存在于集合的成员元素将被忽略。

假如集合 key 不存在，则创建一个只包含添加的元素作成员的集合。

当集合 key 不是集合类型时，返回一个错误。2）

类似这样的命令：myset 就是一个字符串。
```SH
redis 127.0.0.1:6379&gt; SADD myset &quot;hello&quot;
```

（2）集群中也会用到，代码路径： cluter.c&#47;clusterGenNodesDescription

所有节点的信息（包括当前节点自身）被保存到一个 sds 里面，以 csv 格式返回。

（3）cluster.h 的 clusterLink 结构体中。clusterLink 包含了与其他节点进行通讯所需的全部信息

```C
&#47;&#47; 输出缓冲区，保存着等待发送给其他节点的消息（message）。
sds sndbuf;                 &#47;* Packet send buffer *&#47;

&#47;&#47; 输入缓冲区，保存着从其他节点接收到的消息。
sds rcvbuf;     
```

（4）Redis 会维护每个 Client 的状态，Client 发送的请求，会被缓存到 querybuf 中。</div>2021-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/cf/a0315a85.jpg" width="30px"><span>lzh2nix</span> 👍（12） 💬（0）<div>个人觉得sds有一个很优秀的设计是对外和char*保持一致，在sds外面可以像使用char*一样来使用sds，但是使用sds相关函数操作的时候又可以发挥sds的特性(通过偏移量来找到sds的header)。

我们可以看到在sdsnewlen中返回的是char*

sds sdsnewlen(const void *init, size_t initlen) {
    sds s;
    sh = s_malloc(hdrlen+initlen+1);
    s = (char*)sh+hdrlen;
    return s;
}
这样的实际对外面的使用着来说就很友好很友好的。</div>2021-08-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLgsx7Jic0oLzyKcEtk675vnicehGIQGqZiaedh9fdaQjKv6ZJsWviclFakKJicabC2ibV3bibm3gIic5hvtA/132" width="30px"><span>frankylee</span> 👍（6） 💬（4）<div>既然这篇是讲解SDS的,那按道理来说   SDS内存空间分配策略,以及空间释放册罗 这块就应该讲清楚,但是通篇读下来好像并没提到这块,读完下面的精选留言部分读者可能仍然云里雾里</div>2021-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/cf/851dab01.jpg" width="30px"><span>Milittle</span> 👍（4） 💬（0）<div>设计着实牛逼：
1. 使用sds这个字符数组保存所有8 16 32 64的结构体。
2. 结构体中的len alloc 对应不同类型占不同字节数，flags始终是相同的，后面char buf[]就是真实的字符串。
3. SDS_HDR 这个宏定义，一键让sds回到指针初始的地方，对变量进行设置。
4. 一开始纳闷在取flags的时候，直接使用s[-1],不会数据越界么，但是你仔细瞧一瞧，发现这个s指向的位置，刚好是char buf[]这里，-1 的位置刚好是flags。害，还是发现c牛逼。一个指针掌控的死死的。

望赐教
</div>2021-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（2） 💬（0）<div>Redis设计sds的意图：
    1、满足存储传输二进制的条件（避免\0歧义）
    2、高效操作字符串（通过len和alloc,快速获取字符长度大小以及跳转到字符串末尾）
    3、紧凑型内存设计（按照字符串类型，len和alloc使用不同的类型节约内存，并且关闭内存对齐来达到内存高效利用，在redis中除了sds，intset和ziplist也有类似的目底）
    4、避免频繁的内存分配，除了sds部分类型存在预留空间，sds设计了sdsfree和sdsclear两种字符串清理函数，其中sdsclear，只是修改len为0以及buf为&#39;\0&#39;，并不会实际释放内存，避免下次使用带来的内存开销（老师可能忘记提及了）


此外sds的使用几乎可以贯穿整个redis，在server.h文件中以redisServer 和 client 为例子（client既可以是普通客户端，也可以是slave）

client:
    1、querybuf（查询缓冲区使用sds，RESP的协议数据）
    2、pending_querybuf（易主时候的等待同步缓冲区）
    等等


redisServer：
    1、aof_buf（aof缓冲区）
    等等</div>2021-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/10/65fe5b06.jpg" width="30px"><span>J²</span> 👍（1） 💬（0）<div>&#47;&#47;将源字符串中的每个字符逐一赋值到目标字符串中，直到遇到结束字符 
while((*dest++ = *src++) != &#39;\0&#39; )
这里少了个分号，应该是while((*dest++ = *src++) != &#39;\0&#39; );</div>2022-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/6a/be36c108.jpg" width="30px"><span>ikel</span> 👍（1） 💬（0）<div>5年前看redis源码，当时把sds结构用到了项目中来处理字符串，也没出过啥幺蛾子，只可惜后来没有再继续看源码了</div>2021-08-31</li><br/><li><img src="" width="30px"><span>Geek4452</span> 👍（1） 💬（4）<div>和c++ string一样？std string也能满足上述的需求啊，为啥不直接用</div>2021-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/c5/4d/3e75e5f1.jpg" width="30px"><span>命运女神在微笑</span> 👍（1） 💬（0）<div>sdshdr5结构会被使用，if (type == SDS_TYPE_5 &amp;&amp; initlen == 0)，当长度小于sdshdr8且不为空的时候就会被使用，具体的解释可以看这个issue  https:&#47;&#47;github.com&#47;redis&#47;redis&#47;issues&#47;7581，</div>2021-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c7/f8/6b311ad9.jpg" width="30px"><span>BrightLoong</span> 👍（1） 💬（0）<div>mac版本过高，5.0.8编译因为debug.c文件报错的问题，我这边参照最新版本的源文件修改了下，现在可以编译成功了，有需要可以自己下载替换
链接: https:&#47;&#47;pan.baidu.com&#47;s&#47;1dKC9n2a9CmaQCkxn2OuZPw 提取码: 6d6v</div>2021-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/27/b4/df65c0f7.jpg" width="30px"><span>| ~浑蛋~</span> 👍（0） 💬（0）<div>两个宏 SDS_HDR_VAR 和 SDS_HDR 是用于在SDS（Simple Dynamic String）数据结构中从字符串指针获取其对应的SDS头部指针。SDS头部包含了字符串的元数据，如长度和剩余空间。具体来说，这两个宏的功能如下：

SDS_HDR_VAR(T, s):
这个宏定义了一个变量 sh，它是指向SDS头部的指针。
T 是一个类型标识符，用于选择不同的SDS头部结构（例如，sdshdr8, sdshdr16, sdshdr32, sdshdr64 等）。
s 是指向字符串数据的指针。
宏的实现通过将字符串指针 s 减去相应的SDS头部结构的大小来计算头部的起始地址，并将其转换为相应类型的指针。
#define SDS_HDR_VAR(T, s) struct sdshdr##T *sh = (void*)((s) - (sizeof(struct sdshdr##T)));
这个宏的作用是声明并初始化一个指向SDS头部的指针变量 sh。


SDS_HDR(T, s):
这个宏直接返回一个指向SDS头部的指针。
T 和 s 的含义与 SDS_HDR_VAR 中相同。
宏的实现方式与 SDS_HDR_VAR 类似，通过将字符串指针 s 减去相应的SDS头部结构的大小来计算头部的起始地址，并将其转换为相应类型的指针。
#define SDS_HDR(T, s) ((struct sdshdr##T *)((s) - (sizeof(struct sdshdr##T))))
这个宏的作用是返回一个指向SDS头部的指针，而不声明变量。</div>2024-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/b8/bc/5f4c9cb2.jpg" width="30px"><span>掂过碌蔗</span> 👍（0） 💬（0）<div>字节对齐的介绍：https:&#47;&#47;zhuanlan.zhihu.com&#47;p&#47;30007037</div>2023-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/c3/fd/8a2a69f2.jpg" width="30px"><span>ly</span> 👍（0） 💬（0）<div>请问一下，sds采用的紧凑模型会不会和内存对齐矛盾呢，换句话说就是紧凑模型会不会产生大量碎片造成性能下降</div>2022-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/07/22dd76bf.jpg" width="30px"><span>kobe</span> 👍（0） 💬（1）<div>uint8_t 是 8 位无符号整型，会占用 1 字节的内存空间。当字符串类型是 sdshdr8 时，它能表示的字符数组长度（包括数组最后一位\0）不会超过 256 字节（2 的 8 次方等于 256）。这里的字符数组长度应该是256 而不是256字节吧？</div>2022-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/89/52/b96c272d.jpg" width="30px"><span>🤐</span> 👍（0） 💬（0）<div>省内存感觉出来了 对于一开始就用JAVA的人来说 就觉得c的这个字符串设计很奇怪 读长度居然是on</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8f/41/307555ff.jpg" width="30px"><span>伊诺</span> 👍（0） 💬（2）<div>打扰一下，SDS 不通过字符串中的“\0”字符判断字符串结束，但是源码里面老师说最后会拼接上&quot;\o&quot;字符。</div>2022-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/26/3b/c71c197a.jpg" width="30px"><span>Young</span> 👍（0） 💬（0）<div>回头看了一下Redis核心技术与实战的第11节“万金油的string...”，可能之前讲原理讲的比较浅一点吧、在计算内存占用的时候，都是按最大分配的？看了这一节、会更好理解</div>2022-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f7/ad/4fd4d867.jpg" width="30px"><span>数学汤家凤</span> 👍（0） 💬（1）<div>说到结构体！就不得不提到一道经典题目
typedef struct {
    char*  a; &#47;&#47; 8 个字节
    short  b; &#47;&#47; 2 个字节
	double c; &#47;&#47; 8 个字节
	char   d; &#47;&#47; 1 个字节
	float  e; &#47;&#47; 4 个字节
	char   f; &#47;&#47; 1 个字节
	long   g; &#47;&#47; 8 个字节
	int    h; &#47;&#47; 4 个字节
} A;
问：该结构体占多少字节。并优化该结构体使得该结构体所占空间最小</div>2022-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/2f/0a5e0751.jpg" width="30px"><span>再见理想</span> 👍（0） 💬（0）<div>根据字符串的大小，通过flag为len和alloc设置不同的数据类型，内存的合理利用</div>2022-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/2f/0a5e0751.jpg" width="30px"><span>再见理想</span> 👍（0） 💬（1）<div>Sds简单动态字符串
可以存储二进制数据，图片数据
通过len直接获取字符串长度，而不是通过查找&#47;0
预分配内存，防止字符串操作的频繁申请内存，将字符串操作变为安全操作。防止边界溢出。</div>2022-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/2b/1e059a0f.jpg" width="30px"><span>nul</span> 👍（0） 💬（1）<div>优化方案：
1. 引入元数据
2. 编译优化
优化了啥：
1. 二进制安全问题
2. 操作效率问题
3. 内存资源优化</div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/08/c3/bf4fe285.jpg" width="30px"><span>白菜</span> 👍（0） 💬（0）<div>有个疑问希望老师能解答：
Redis 字符串类型最大长度应该是 512M，sdshdr32 结构 的 len 和 alloc 刚好能够存储 512M 的长度，那么什么情况下才可能用到 sdshdr64 呢？</div>2021-12-23</li><br/><li><img src="" width="30px"><span>Geek_4f06ca</span> 👍（0） 💬（0）<div>在一次set操作中，key 在dbAdd的时候会调用sds copy = sdsdup(key-&gt;ptr) 生成sds ，但是value 没有没有看到转成sds的操作，在tryObjectEncoding 会对小于44字节的进行编码，但是大于44的情况并没有转成sds ，为什么值不转sds？有谁能解答下吗？
</div>2021-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/09/07/44625105.jpg" width="30px"><span>Alba</span> 👍（0） 💬（0）<div>写一下自己看代码的疑惑和解决。
1. sdsnewlen 函数返回的是 sds 类型，也就是 char * 类型，而sdsnewlen 函数内部申请了sdshdr 加上 字符串的内存大小。这里利用了指针偏移。
2. 使用__attribute__((packed)) 确实能够实现内存紧凑，但是我们日常普遍用的都是结构体内存对齐。结构体内存对齐的意义在于防止访问一个数据时内存访问两次，相当于用空间换时间。那 redis 放弃了结构体内存对齐，对影响内存访问的效率吗？目前看的代码还很少，猜想是对 sdshdr 里的字段访问的比较少，所以不会影响内存访问的效率。如果工作中对内存优化需求不是很强烈，还是没必要使用内存紧凑的。
3. 结构体末端0长度数组相比指针的好处。一、方便申请和释放。如果用指针，就需要先申请结构体的内存，再申请指针指向字符串的内存；先释放指针指向字符串的内存，再释放结构体的内存。而用数组，只申请和释放结构体的内存就可以了。二、数组长度为 0 的时候不占用内存大小，而使用指针，指针本身就占用一个字长。</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/33/b17c8fb7.jpg" width="30px"><span>熊猫№.47</span> 👍（0） 💬（0）<div>Strings类型：一个String类型的value最大可以存储512M

Lists类型：list的元素个数最多为2^32-1个，也就是4294967295个。

Sets类型：元素个数最多为2^32-1个，也就是4294967295个。

Hashes类型：键值对个数最多为2^32-1个，也就是4294967295个。

Sorted sets类型：跟Sets类型相似。</div>2021-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/5e/81/82709d6e.jpg" width="30px"><span>码小呆</span> 👍（0） 💬（2）<div>__attribute__ ((__packed__)) 是这么做到紧凑型内存布局的呢，还有作者大大，有没有啥工具能更好的看redis源码呢，谢谢</div>2021-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/8c/a7/3a696385.jpg" width="30px"><span>.</span> 👍（0） 💬（1）<div>为什么\0就不符合redis存储二进制数据的要求呢？</div>2021-08-01</li><br/>
</ul>