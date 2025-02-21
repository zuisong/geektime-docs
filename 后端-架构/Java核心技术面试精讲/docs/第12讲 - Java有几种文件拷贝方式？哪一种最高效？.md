我在专栏上一讲提到，NIO不止是多路复用，NIO 2也不只是异步IO，今天我们来看看Java IO体系中，其他不可忽略的部分。

今天我要问你的问题是，Java有几种文件拷贝方式？哪一种最高效？

## 典型回答

Java有多种比较典型的文件拷贝实现方式，比如：

利用java.io类库，直接为源文件构建一个FileInputStream读取，然后再为目标文件构建一个FileOutputStream，完成写入工作。

```
public static void copyFileByStream(File source, File dest) throws
        IOException {
    try (InputStream is = new FileInputStream(source);
         OutputStream os = new FileOutputStream(dest);){
        byte[] buffer = new byte[1024];
        int length;
        while ((length = is.read(buffer)) > 0) {
            os.write(buffer, 0, length);
        }
    }
 }

```

或者，利用java.nio类库提供的transferTo或transferFrom方法实现。

```
public static void copyFileByChannel(File source, File dest) throws
        IOException {
    try (FileChannel sourceChannel = new FileInputStream(source)
            .getChannel();
         FileChannel targetChannel = new FileOutputStream(dest).getChannel
                 ();){
        for (long count = sourceChannel.size() ;count>0 ;) {
            long transferred = sourceChannel.transferTo(
                    sourceChannel.position(), count, targetChannel);            sourceChannel.position(sourceChannel.position() + transferred);
            count -= transferred;
        }
    }
 }

```

当然，Java标准类库本身已经提供了几种Files.copy的实现。

对于Copy的效率，这个其实与操作系统和配置等情况相关，总体上来说，NIO transferTo/From的方式**可能更快**，因为它更能利用现代操作系统底层机制，避免不必要拷贝和上下文切换。

## 考点分析

今天这个问题，从面试的角度来看，确实是一个面试考察的点，针对我上面的典型回答，面试官还可能会从实践角度，或者IO底层实现机制等方面进一步提问。这一讲的内容从面试题出发，主要还是为了让你进一步加深对Java IO类库设计和实现的了解。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/36/2d61e080.jpg" width="30px"><span>行者</span> 👍（133） 💬（4）<div>可以利用NIO分散-scatter机制来写入不同buffer。
Code:
ByteBuffer header = ByteBuffer.allocate(128);
ByteBuffer body   = ByteBuffer.allocate(1024);
ByteBuffer[] bufferArray = {header, body};
channel.read(bufferArray);
注意:该方法适用于请求头长度固定。</div>2018-05-31</li><br/><li><img src="" width="30px"><span>13576788017</span> 👍（128） 💬（20）<div>杨老师，想问一下，一般要几年java经验才能达到看懂你文章的地步？？我将近一年经验。。我发现我好几篇都看不懂。。底层完全不懂。。是我太菜了吗。。</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/86/0de33451.jpg" width="30px"><span>乘风破浪</span> 👍（54） 💬（1）<div>零拷贝是不是可以理解为内核态空间与磁盘之间的数据传输，不需要再经过用户态空间？</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/95/96/0020bd67.jpg" width="30px"><span>夏洛克的救赎</span> 👍（21） 💬（1）<div>请问老师您有参与jdk的开发吗</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/ab/867fa111.jpg" width="30px"><span>CC</span> 👍（18） 💬（1）<div>我Nio从没接触过，很难受，两年开发的</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/36/6c/7d5b797e.jpg" width="30px"><span>vash_ace</span> 👍（17） 💬（3）<div>其实在初始化 DirectByteBuffer对象时，如果当前堆外内存的条件很苛刻时，会主动调用 System.gc()强制执行FGC。所以一般建议在使用netty时开启XX:+DisableExplicitGC</div>2018-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/24/7d43d807.jpg" width="30px"><span>mongo</span> 👍（15） 💬（1）<div>杨老师，我也想请教，目前为止您的其他文章都理解的很好，到了上次专栏的NIO我理解的不是很好，今天的这篇可以说懵圈了。到了这一步想突破，应该往哪个方向？我自己感觉是因为基于这两个底层原理的上层应用使用的时候观察的不够深入，对原理反应的现象没有深刻感受，就是所谓还没有摸清楚人家长什么样。所以接下来我会认真在使用基于这些原理实现的上层应用过程中不断深挖和观察，比如认真学习dubbo框架（底层使用到了netty，netty的底层使用了NIO）来帮助我理解NIO。在这个过程中促进对dubbo的掌握，以此良性循环。不知道方向对不对？老师的学习方法是什么？请老师指点避坑。学习方法不对的话时间成本太可怕。</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9f/3f/f4666faa.jpg" width="30px"><span>老陈板</span> 👍（9） 💬（1）<div>本篇文章有恍然大悟的感觉，前面段时间有一家面试问了个这样的问题，我们发现服务器内存使用得特别高，但是堆内存也比较稳定，这种场景是你你会怎么排查？这里就涉及到堆外内存相关的问题！以前不知道有NMT这个工具，然后当时没答好，导致工资少了好多，早点读这篇文章多好。另外注意，sysyem.gc不一定会立即触发fgc，有个权值</div>2019-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/59/bb/caf2b06c.jpg" width="30px"><span>皮蛋</span> 👍（9） 💬（1）<div>杨老师，想问下如果想学操作系统的知识，阅读什么书比较适合，初学者</div>2018-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9b/2f/b7a3625e.jpg" width="30px"><span>Len</span> 👍（9） 💬（1）<div>请教老师:
1. 经常看到 Java 进程的 RES 大小远超过设置的 Xmx，可以认为这就是 Direct Memory 的原因吗？如果是的话，可以简单的用堆实际占用的大小减去 RES 就是 Direct Memory 的大小吗？

2.可以认为 Direct Memory 不论在什么情况下都不会引起 Full GC，Direct Memory 的回收只是在 Full GC (或调用 System.gc())的时候顺带着回收下，是吗？</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/92/99530cee.jpg" width="30px"><span>灰飞灰猪不会灰飞.烟灭</span> 👍（6） 💬（1）<div>老师，带缓冲区的io流比nio哪一个性能更好？</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/92/99530cee.jpg" width="30px"><span>灰飞灰猪不会灰飞.烟灭</span> 👍（4） 💬（2）<div>杨老师 我刚刚做个项目，上传文件到文件服务器，文件大概10M，经常上传失败。假如我上传的文件改成1M，就没这问题了。不知道什么原因，能提供个思路吗？谢谢</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e3/57/e5de0216.jpg" width="30px"><span>Cui</span> 👍（4） 💬（1）<div>Direct Buffer 生命周期内内存地址都不会再发生更改，进而内核可以安全地对其进行访问—这里能提高性能的原因 是因为内存地址不变，没有锁争用吗？能否详细解答下？</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/76/12203657.jpg" width="30px"><span>罗飞</span> 👍（3） 💬（4）<div>零拷贝，是DMA 数据传输，完全由硬件实现的，内核只是起到控制设置作用，不要误人子弟好么</div>2019-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/03/a2/ceb37046.jpg" width="30px"><span>crazyone</span> 👍（2） 💬（1）<div>杨老师，Nio transfer 不一定快的场景是否有案例场景说明下？ 还有你说MappedByteBuffer本质上也是一个Direct  Buffer ,那它设计的目的和意义是什么？</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（1） 💬（2）<div>再问个问题，在Java 8中，对Byte Buffer有这样的描述，a byte buffer is either or non-direct。
我有点晕乎了，在代码调试中isDirect是False 。</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（1） 💬（1）<div>杨老师，问个问题，Byte Buffer对象什么时候被垃圾回收？</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/8d/7db04ad3.jpg" width="30px"><span>I am a psycho</span> 👍（1） 💬（1）<div>杨老师，我看1.8的源码中，files.copy共重载了4个方法，其中有三个调用的都是bio，有一个是您讲的native调用，而没有nio的transferTo。请问这是jdk9变成nio的吗？</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/27/c8/3addd7b7.jpg" width="30px"><span>沈老师</span> 👍（1） 💬（2）<div>上面有两张说明普通copy和nio下的transfer，我理解大致意思就是后者省去了切换到用户态的开销，但想问一下前者为什么要设计这样的切换呢?是不是和你copy的数据类型有关?还望详释，谢谢！</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/eb/af/b893c7e2.jpg" width="30px"><span>jacky</span> 👍（0） 💬（1）<div>杨老师，如果显示调用system.gc会不会导致堆空间充足，但fullgc频繁的现象呢？导致应用经常停顿？</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2b/9e/821c75f9.jpg" width="30px"><span>闭门造车</span> 👍（16） 💬（8）<div>你好，我查看jdk8中的源码，看到您说的关于Files.copy其中两种是依靠transferto实现的，但是我翻看源码觉得跟您的理解不同，特来求证，源码如下:    public static long copy(Path source, OutputStream out) throws IOException {
        Objects.requireNonNull(out);
        try (InputStream in = newInputStream(source)) {
            return copy(in, out);
        }
    }
        private static long copy(InputStream source, OutputStream sink)
        throws IOException
    {
        long nread = 0L;
        byte[] buf = new byte[BUFFER_SIZE];
        int n;
        while ((n = source.read(buf)) &gt; 0) {
            sink.write(buf, 0, n);
            nread += n;
        }
        return nread;
    }</div>2018-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0f/4f/c75c4889.jpg" width="30px"><span>石头狮子</span> 👍（10） 💬（0）<div>若使用非 directbuffer 操作相关 api 的话，jdk 会将其复制为 ditrctbuff。并且在线程内部缓存该directbuffer。jdk 对这个缓存的大小并没有限制。
之前遇到缓存的 directbuffer 过多，导致oom的情况。后续 jdk 版本加入了对该缓存的限制。
额外一点是尽量不要使用堆内的 bytebuffer 操作 channel 类 api。</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/29/629d9bb0.jpg" width="30px"><span>天王</span> 👍（7） 💬（0）<div>12 java java有几种文件拷贝方式，1 利用Java.io，FileInputStream和FileOutputStream， 2 nio的transferTo和transferFrom，2比1快的原因，是操作系统分用户态和内核态，先在内核态把文件拷贝到内存，再从内核态拷贝到用户态，多了拷贝的过程和上下文切换，3 拷贝的底层实现 操作系统分内核空间和用户空间，操作系统内核和硬盘驱动等在内核空间，用户态在用户空间，文件读取是先从内核态读取磁盘数据到内核缓存中，再切换到用户态，从内核态空间读取到用户态缓存，nio的transferTo不会经用户态，直接在内核态做相应处理 4 Java Java.nio.files.Files.copy，java标准类库提供的copy方法transferTo，底层是调用了InputStream.transferTo，底层调用了用户态的拷贝方法，5 提高拷贝方法 利用缓存，尽量减少io次数，减少内核态到用户态的切换，减少切换开销，减少不必要的转换过程，比如编解码，序列化和反序列化，6 Buffer NIO为每个数据类型提供了各自的Buffer，ByteBuffer，IntBuffer，FloatBuffer，7 DirectBuffer，java提供了堆内和堆外Buffer(DirectBiffer)，MappedByteBuffer，将文件大小直接映射为内存区域，程序访问时直接访问，省去了用户态和内核态的空间转换，java尽量对DirectBuffer仅做本地操作，生命周期内的内存地址不修改，内核可以安全访问，可以更高效，同时减少了堆内对象的维护工作。</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/94/a3/c8bcb28b.jpg" width="30px"><span>美国的华莱士</span> 👍（6） 💬（4）<div>国外的这遍文章写的还不错，偏基础的可以参考下：
https:&#47;&#47;www.journaldev.com&#47;861&#47;java-copy-file</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/39/ac/d185d0e5.jpg" width="30px"><span>Quincy</span> 👍（3） 💬（1）<div>老师，我想问下，transferto是怎么实现的零拷贝，而避免了用户态和内核态之间转换的开销</div>2018-08-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKzqI6QDsTCeYhrBsLo5YFQ0NMMbKKU5JD1xvnlBHcxc7GomeRaoHF1ic3gC6c355PgVjBOica6ibO4g/132" width="30px"><span>玲玲爱学习</span> 👍（2） 💬（1）<div>堆外缓存是否与内核缓存是同一个东西？</div>2018-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（1） 💬（0）<div>https:&#47;&#47;shawn-xu.medium.com&#47;its-all-about-buffers-zero-copy-mmap-and-java-nio-50f2a1bfc05c
可以对照这篇文章看看，说明了write,read; sendfile; mmap等系统调用的过程</div>2020-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/66/39eeb3f9.jpg" width="30px"><span>Cain</span> 👍（1） 💬（1）<div>老师，可以举例说明nio比io慢的场景吗？</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/53/e8/137a75f5.jpg" width="30px"><span>linco_001</span> 👍（1） 💬（0）<div>按照老师的说法，上下文切换可以理解成用户态和内核态之间的切换。这样理解对吗？</div>2019-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（1） 💬（0）<div>有同感，Java IO这块学起来坡度明显陡峭了，上午看各种IO就有点不在状态，估计更偏向操作系统层面了吧！
不过我又回头看了漫画编程上关于Java IO的文章，感觉轻松自在很多，理解同步，异步，阻塞，非阻塞，各种IO的特点丝毫不费劲，估计是漫画和更通俗的原因吧！
老师，讲文件拷贝最快的方式有数据依据吗？还是就是推论？感觉不是很确定，需要依据具体情况来定？</div>2018-12-15</li><br/>
</ul>