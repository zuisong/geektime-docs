你好，我是李玥。

Apache Kafka是一个高性能的消息队列，在众多消息队列产品中，Kafka的性能绝对是处于第一梯队的。我曾经在一台配置比较好的服务器上，对Kafka做过极限的性能压测，Kafka单个节点的极限处理能力接近每秒钟2000万条消息，吞吐量达到每秒钟600MB。

你可能会问，Kafka是如何做到这么高的性能的？

我们在专栏“进阶篇”的前几节课，讲的知识点一直围绕着同一个主题：怎么开发一个高性能的网络应用程序。其中提到了像全异步化的线程模型、高性能的异步网络传输、自定义的私有传输协议和序列化、反序列化等等，这些方法和优化技巧，你都可以在Kafka的源代码中找到对应的实现。

在性能优化方面，除了这些通用的性能优化手段之外，Kafka还有哪些“独门绝技”呢？

这节课，我来为你一一揭晓这些绝技。

## 使用批量消息提升服务端处理能力

我们知道，批量处理是一种非常有效的提升系统吞吐量的方法。在Kafka内部，消息都是以“批”为单位处理的。一批消息从发送端到接收端，是如何在Kafka中流转的呢？

我们先来看发送端，也就是Producer这一端。

在Kafka的客户端SDK（软件开发工具包）中，Kafka的Producer只提供了单条发送的send()方法，并没有提供任何批量发送的接口。原因是，Kafka根本就没有提供单条发送的功能，是的，你没有看错，虽然它提供的API每次只能发送一条消息，但实际上，Kafka的客户端SDK在实现消息发送逻辑的时候，采用了异步批量发送的机制。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/57/f6/2c7ac1ad.jpg" width="30px"><span>Peter</span> 👍（66） 💬（3）<div>老师您好，请教个问题：在NIO中创建缓冲区时，可以创建直接缓冲区，即ByteBuffer.allocateDirect(capacity)这里的直接缓冲区是不是就是零拷贝技术？</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/14/17/8763dced.jpg" width="30px"><span>微微一笑</span> 👍（42） 💬（6）<div>老师好，有些疑问希望老师解答下：
①rocketMq有consumeQueue，存储着offset，然后通过offset去commitlog找到对应的Message。通过看rocketmq的开发文档，通过offset去查询消息属于【随机读】，offset不是存储着消息在磁盘中的位置吗？为什么属于随机读呢？
②rocketMq的某个topic下指定的消息队列数，指的是consumeQueue的数量吗？
③性能上，顺序读优于随机读。rocketMq的实现上，在消费者与commitlog之间设计了consumeQueue的数据结构，导致不能顺序读，只能随机读。我的疑惑是，rocketMq为什么不像kafka那样设计，通过顺序读取消息，然后再根据topic、tag平均分配给不同的消费者实例,，这样消息积压的时候，直接增加消费者实例就可以了，不需要增加consumeQueue，这样也可以去除consumeQueue的存在呀？我在想consumeQueue存在的意义是什么呢？
哈哈，我的理解可能有些问题，希望老师指点迷津~</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（25） 💬（1）<div>谢谢老师，今天讲到的点，我会在课下去读源码并写出文章</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/8c/373d4027.jpg" width="30px"><span>龍蝦</span> 👍（17） 💬（3）<div>Kafka Producer 调用同步 send() 成功返回，其实没法保证消息已经成功发送到 Kafka 服务器？</div>2019-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/c4/6f97daea.jpg" width="30px"><span>长期规划</span> 👍（14） 💬（9）<div>老师，如果Pagecahe在刷入磁盘前系统崩溃了，那数据就丢了吧？这样说来，即使写了文件，也不代表持久化了</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（13） 💬（8）<div>1、老师有个疑问，kafka在发送时，都会在客户端进行攒一波，然后过一定的时间，或者达到一定的大小发送出去，批量发送的时候，是把一批同一个topic下的分区的消息进行批量发送么？还是不管是属于同一分区的消息都进行批量发送，broker端是不会对批消息进行拆分成每一条，那这样消费端消费到的消息不是有可能有不是订阅的分区么？
2、学习到现在，有个感想，很多事情看似很简单，但是实际再做的时候都没那么简单，很多都得持之以恒，多思考、多实践、多动手，不然的话很多都是看懂，真正在使用的时候还是不知道如何下手。把很多小事、简单的事情做好本身就不是个简单的事情，目前有个想法打算把开源rocketmq读完，代码上写上注释和理解。
3、老师我一直有个疑惑点，如何才能当上架构师了，一方面硬核实力技术过硬，有整体的大局观，老师能否以你自身的经历给我们解惑下了</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/31/a7/7b0fc84d.jpg" width="30px"><span>正本·清源</span> 👍（10） 💬（1）<div>班长确实知识扎实，其实全是大学本科课本的知识在不同技术上的组合。好在这些专业课我没有逃课，哈哈</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/bc/6d/f6f0a442.jpg" width="30px"><span>汤小高</span> 👍（9） 💬（1）<div>老师，如果消息是先写入page cache，再由操作系统写入磁盘的话，如果刚刚写入page cache，操作系统还没来得及写入磁盘，主机宕机了，那岂不是会丢数据？ 那这样卡夫卡服务本身岂不是也会存在丢数据的情况？ Kafka broker是在写入page cache就给producer 回复ack 还是操作系统将page cache写入磁盘后，如果是后者，就能保证不丢数据</div>2020-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（9） 💬（1）<div>   老师的课程学到现在开始越来越费力了：一堂课学完笔记量已经直线上升了；对于今天的课程读完后有些困惑之处烦劳老师可以指点迷津：
    1.客户端发送者的发送给服务器端的时候：其实是写入一个Packge或者说一个log包，然后服务器端处理完这个包之后，作为一个批处理，处理完成后给客户端的消费者消费者解包之后依次获得处理结果；是这样么。
    2.关于PageCache：刘超老师的课程中曾经提及其实消息队列主要运作在缓存层，常驻缓存就是为了节约查询时间；老师早先在开课的时候提过不同的消息队列其实特性不同，Kafka擅长或者说充分利用的是PageCache，其它如RockeMQ呢？我们如何扬长避短
    主要是基于以下两方面：一方面是-其实现在大量的服务器是在云端的，无论是Amaze云、腾讯云、阿里云其实共同的特性都是CPU和IO稳定性或者使用率并非真实会引发一些看似极高的是使用率真实情况却并非有那么高，另外一方面-其实任何消息队列的推出都是基于当下，如果想基于当下的消息队列做些二次开发或者特性改进需要做些什么或者准备些什么呢?操作系统、计算机组成原理，还有什么？望老师能提点1、2.
     跟着老师学到现在发现确实学好这门课可能比老师最初说的要求还要高：老师的课程跟到现在，觉得自己已经在最初的目标的路上了，谢谢老师的提点；期待老师的后续课程。</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ed/4c/8674b6ad.jpg" width="30px"><span>timmy21</span> 👍（7） 💬（2）<div>老师，我有两个疑问想请教一下：1. 我们平常打开文件写入数据是顺序写吗？2. 还有如何进行随机写？是seek到某个位置开始写？但这样的话文件数据不是会被覆盖吗？</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/b1/5c63be67.jpg" width="30px"><span>易水寒</span> 👍（6） 💬（4）<div>老师好，我有个问题一直不明白，一个文件的数据应该是分散存储在磁盘上的吧（一般不太可能会是数据的位置都是连续的），读完整个文件的数据，怎么着也是需要移动磁头的吧（假如是机械盘），那么顺序读，所谓的顺序的含义是指什么？</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9c/9b/eec0d41f.jpg" width="30px"><span>康师傅</span> 👍（6） 💬（1）<div>请教一下
我的理解是：顺序写是针对某个分区而言的，那么如果单个节点上的topic数量很多，或者分区数很多，从整体来看应该还是会有很多的随机IO，因为会切换写不同的文件，这种情况下整体性能是不是就不高了？
这种场景下，除了增加节点，将分区分布到多个节点上，是否还有其他有效提升性能的办法？</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（5） 💬（1）<div>应用程序在写入文件的时候，操作系统会先把数据写入到内存中的 PageCache，然后再一批一批地写到磁盘上。读取文件的时候，也是从 PageCache 中来读取数据，这时候会出现两种可能情况。

客户端读取消息是，有个位置信息，这个信息在信息写入时，只在pagecache里出现还没有落盘时，位置信息就已经有了吗？这个位置信息怎么来的，原理又是什么？</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/30/fc095d86.jpg" width="30px"><span>摩云神雕</span> 👍（4） 💬（1）<div>请教下老师，调用send()方法发送一条消息后，无论是同步还是异步发送，这条消息都会缓存到我本地的内存吗？ 然后在合适的时间组成一批，一次发给Broker（kafka服务端）吗？ 发送时机是客户端可配的吗？ </div>2019-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c8/34/fb871b2c.jpg" width="30px"><span>海罗沃德</span> 👍（4） 💬（1）<div>Kafka既然是批量處理消息，那麼是怎麼實現Kafka的實時數據流計算呢？</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bd/da/3d76ea74.jpg" width="30px"><span>看不到de颜色</span> 👍（3） 💬（1）<div>有一点疑惑还请老师解答一下。kafka为了保证消息丢失，客户端在发送消息时有三种acks可供选择。那如果kafka消息客户端都采用异步批量发送，那这三种参数还有意义吗？</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/14/f1532dec.jpg" width="30px"><span>鲁班大师</span> 👍（2） 💬（1）<div>老师，我理解只要使用了nio就自动使用了零拷贝</div>2020-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/4f/ff1ac464.jpg" width="30px"><span>又双叒叕是一年啊</span> 👍（2） 💬（1）<div>老师请教一下，课程最后说： 这种从文件读出数据后再通过网络发送出去的场景，并且这个过程中你不需要对这些数据进行处理，那一定要使用这个零拷贝的方法，可以有效地提升性能。
可是我理解 kafka消费则消费过程是需要读取数据的内存处理完成后再回复消费成功消息的。为什么还能用到零拷贝技术呢？</div>2019-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c5/b2/5b339c64.jpg" width="30px"><span>K-Li</span> 👍（2） 💬（1）<div>老师，我知道kafka是攒一波消息后进行批处理的，那么在consumer消费到一条消息后如果处理失败需要commit offset为上一条消息来重新消费的话是这么做到下一次来的就是刚刚处理失败的那条数据而不是&quot;一批&quot;里的下一条？</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（2） 💬（1）<div>尝试回答微微一笑的问题，老师有空帮忙看下哦
老师好，有些疑问希望老师解答下：
①rocketMq有consumeQueue，存储着offset，然后通过offset去commitlog找到对应的Message。通过看rocketmq的开发文档，通过offset去查询消息属于【随机读】，offset不是存储着消息在磁盘中的位置吗？为什么属于随机读呢？
②rocketMq的某个topic下指定的消息队列数，指的是consumeQueue的数量吗？
③性能上，顺序读优于随机读。rocketMq的实现上，在消费者与commitlog之间设计了consumeQueue的数据结构，导致不能顺序读，只能随机读。我的疑惑是，rocketMq为什么不像kafka那样设计，通过顺序读取消息，然后再根据topic、tag平均分配给不同的消费者实例,，这样消息积压的时候，直接增加消费者实例就可以了，不需要增加consumeQueue，这样也可以去除consumeQueue的存在呀？我在想consumeQueue存在的意义是什么呢？
哈哈，我的理解可能有些问题，希望老师指点迷津~
①顺序读写是从头开始进行读写，比随机读比，不需要进行数据的位置定位只要从头开始进行读写，随机读需要进行数据位置的定位，如果能知道位置，通过位置进行随机读也会很快，rocketmq就是这样来优化io的随机读，快速读数据不一定是顺序读，也可以根据位置的随机读。
②rocketmq是messageQueue的数量，老师我有个好奇点rocketmq内部为什么要分读写队列，还有messageQueue内部没有存放消息，而是由消息message存放queueId和topic，消费者在消费的时候应该会有个consumerQueue才对，但是我在rocketmq代码里没有找到。
③rocketmq在内部用到consumeQueue，因为consumeQueue内部无需存放真正的消息，只要存储消息在commitLog的offset的位置、消息的storeSize，每次要消费的时候只要拿到位置和大小，就可以读到消息，并且无需每次根据topic和tag进行平均分配。</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（2） 💬（1）<div>只说了它的优点，其实它的缺点也很明显。把确定也顺便解释解释。</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a9/36/d054c979.jpg" width="30px"><span>G.S.K</span> 👍（1） 💬（1）<div>有个疑问请教老师，虽然kafka进程是顺序读写，假如主机上还部署了其他进程比如一个进程A。进程A随机读写磁盘，移动磁头，会不会影响kafka进程呢？会不会kafka进程在顺序写，但是进程切换到进程A运行，进程A把磁头给移动走了。</div>2020-07-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKUcSLVV6ia3dibe7qvTu8Vic1PVs2EibxoUdx930MC7j2Q9A6s4eibMDZlcicMFY0D0icd3RrDorMChu0zw/132" width="30px"><span>Tesla</span> 👍（1） 💬（1）<div>老师好，请问kafka是怎么实现的顺序存储呢？是操作系统log文件本身就是顺序存储的吗</div>2020-03-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKUcSLVV6ia3dibe7qvTu8Vic1PVs2EibxoUdx930MC7j2Q9A6s4eibMDZlcicMFY0D0icd3RrDorMChu0zw/132" width="30px"><span>Tesla</span> 👍（1） 💬（1）<div>老师好，请问一下，kafka利用pageCache减少IO。这样消费端是不是要知道Broker保存到pageCache中的对象的内存地址呢？而它们又是两个不同的进程，内存地址是怎么传递的呢？</div>2019-10-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKUcSLVV6ia3dibe7qvTu8Vic1PVs2EibxoUdx930MC7j2Q9A6s4eibMDZlcicMFY0D0icd3RrDorMChu0zw/132" width="30px"><span>Tesla</span> 👍（1） 💬（1）<div>老师好，请问一下kafka使用顺序读写的方式，应该是在有正式数据写入之前，先在硬件上开辟一段连续的存储空间吧？等到有数据了再依次写入存储空间，就像列表需要指定对象类型和列表长度一样。那kafka是如何确定这段空间的大小呢？</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/e2/1fad12eb.jpg" width="30px"><span>张洪阆</span> 👍（1） 💬（1）<div>如果没攒够数据量是否就一直不发呢，有没有超时机制？</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（1） 💬（1）<div>构建批消息和解开批消息分别在发送端和消费端的客户端完成，不仅减轻了 Broker 的压力，最重要的是减少了 Broker 处理请求的次数，提升了总体的处理能力。

这样的他，一批消息在多个消费端的情况下，这批消息这能落到一个消费端的吧？</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1c/6f/3ea2a599.jpg" width="30px"><span>嘉木</span> 👍（1） 💬（1）<div>如果你遇到这种从文件读出数据后再通过网络发送出去的场景，并且这个过程中你不需要对这些数据进行处理，那一定要使用这个零拷贝的方法，可以有效地提升性能。

这个sendfile是不是从一个fd到另外一个fd的复制都是可以用的？</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/9b/46/ad3194bd.jpg" width="30px"><span>jack</span> 👍（1） 💬（1）<div>老师，关于kafka有几个问题期待您的解答：
1、消费者是线程不安全的，多线程使用消费者，官方提供了两个方法，一是一个线程一个消费者，但是这样总的线程数受到分区数量的影响；二是一个线程或者几个线程把数据都消费到，然后将数据交给真正处理数据的线程池处理。想问您实际开发中哪种使用的更频繁，更多呢？
2、消费者在poll时，总是处于while(true)循环中，那么逻辑处理就都放在循环中？如果想在循环外使用数据该怎么做呢？
3、消费者为了保证“至少一次”处理，是否应该更多的采用手动提交offset？</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3a/82/1ff83a38.jpg" width="30px"><span>牛牛</span> 👍（0） 💬（1）<div>老师、想请教下 RocketMQ的queue
1. 生产者和消费者都有自己的Queue吗 ？还是生产者的Queue就是消费这的Queue呢 ？
   如果各自有独立的Queue、这两者之间有什么联系没 ？
2. ReadQueue 和 WriteQueue 的作用是什么呢 ？这两个Queue都是针对某个topic而言还是针对Producer和Consumer而言呢 ？ReadQueue和WriteQueue的数量可以不一致么 ？
3. 真正存储消息的地方是Queue、而Broker只是负责消息的路由？Broker的slave和master上包含相同的数据信息、对吗？

有点儿乱了、希望老师或者路过的同学指点下 ^.^、先多谢啦~~~</div>2019-09-02</li><br/>
</ul>