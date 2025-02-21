在性能分析的人眼里，性能瓶颈就是性能瓶颈。无论这个性能瓶颈出现在代码层、操作系统层、数据库层还是其他层，最终的目的只有一个结果：解决掉！

有人可能会觉得这种说法过于霸道。

事实上，我要强调的性能分析能力，是一套分析逻辑。在这一套分析逻辑中，不管是操作系统、代码还是数据库等，所涉及到的都只是基础知识。如果一个人都掌握这些内容，那确实不现实，但如果是对一个性能团队的要求，我觉得一点也不高。

在性能测试和性能分析的项目中，没有压力发起，就不会有性能瓶颈，也就谈不上性能分析了。所以每个问题的前提，都是要有压力。

但不是所有的压力场景都合理，再加上即使压力场景不合理，也能压出性能瓶颈，这就会产生一种错觉：似乎一个错误的压力场景也是有效的。

我是在介入一个项目时，首先会看场景是否有效。如果无效，我就不会下手去调了，因为即使优化好了，可能也给不出生产环境应该如何配置的结论，那工作就白做了。

所以要先调场景。

我经常会把一个性能测试项目里的工作分成两大阶段：

### 整理阶段

在这个阶段中，要把之前项目中做错的内容纠正过来。不止有技术里的纠正，还有从上到下沟通上的纠正。

### 调优阶段

这才真是干活的阶段。

在这个案例中，同样，我还是要表达一个分析的思路。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/20/1d/0c1a184c.jpg" width="30px"><span>罗辑思维</span> 👍（13） 💬（3）<div>分享下自己学习体会：
为什么缓存可以加速I&#47;O的访问速度？
老师说的缓存应该有两个：操作系统的缓存和PostgreSQL的缓存。它俩作用都是为了把经常访问的数据（也就是热点数据），提前读入到内存中。这样，下次访问时就可以直接从内存读取数据，而不需要经过硬盘，从而加速I&#47;O 的访问速度。

因为没接触过PostgreSQL,在做思考题时找了些资料，下面是延伸的学习。
PostgreSQL缓存跟操作系统的缓存有啥联系？

1.在访问数据时，数据会先加载到操作系统缓存，然后再加载到shared_buffers，这个加载过程可能是一些查询，也可以使用pg_prewarm预热缓存。
2.当然也可能同时存在操作系统和shared_buffers两份一样的缓存（双缓存）。
3.查找到的时候会先在shared_buffers查找是否有缓存，如果没有再到操作系统缓存查找，最后再从磁盘获取。
4.操作系统缓存使用简单的LRU（移除最近最久未使用的缓存），而PostgreSQL采用的优化的时钟扫描，即缓存使用频率高的会被保存，低的被移除。

PostgreSQL缓存读顺序share_buffers -&gt; 操作系统缓存 -&gt; 硬盘。那么也可能是操作系统缓存不足，而不定是share_buffers。通过文章中vmstat命令看到cache有260G，free值也很稳定，所以应该检查PostgreSQL的缓存。（老师执行vmstat是不是埋了个伏笔）。

参考资料
https:&#47;&#47;www.cnblogs.com&#47;zhangfx01&#47;p&#47;postgresql_shared_buffer.html
https:&#47;&#47;blog.csdn.net&#47;kwame211&#47;article&#47;details&#47;78665999</div>2020-03-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJlkFFx4N8ice8UcQRu3AMP0QAXdib17lyFI8G6QLje9iaumOXhsNq50PyLowAwg0umho89o1amN2UGQ/132" width="30px"><span>Geek_7cf52a</span> 👍（3） 💬（1）<div>bi 是指每秒读磁盘的块数。所以要先看一下，一块有多大。

[root@7dgroup1 ~]# tune2fs -l &#47;dev&#47;vda1 | grep &quot;Block size&quot;
Block size: 4096
[root@7dgroup1 ~]#

(300000∗1024)&#47;1024&#47;1024≈293M

=====================================================
=====================================================
上面为原文
这里指的是块。但是老师这样算也错了吧，一块是4096byte,那300000块的大小应该是300000*4096&#47;1024&#47;1024=1172M</div>2020-07-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJ6G2xZvNRmhyXBjmGbI5G8icGCCMPupr6yxZ1IcURwp7GTRHcpWGWpg9A0fLlyicmVdDwzqZqwiaOQ/132" width="30px"><span>jy</span> 👍（2） 💬（5）<div>bi 是指每秒读磁盘的块数。所以要先看一下，一块有多大。

[root@7dgroup1 ~]# tune2fs -l &#47;dev&#47;vda1 | grep &quot;Block size&quot;
Block size:               4096
[root@7dgroup1 ~]#

(300000∗1024)&#47;1024&#47;1024≈293M

=====================================================
=====================================================
上面为原文

问题一：
老师，这里是不是有问题？
bi表示从块设备读入数据的总量（即读磁盘）（kb&#47;s），而不是每秒读磁盘的块数
其实，这样算就可以了：300000&#47;1024≈293M


问题二：查询Block size的目的是？我看这个4096和iostat图中r&#47;s列的值差不多，
而r&#47;s表示每秒完成读IO设备的次数</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/3e/82202cc8.jpg" width="30px"><span>月亮和六便士</span> 👍（2） 💬（1）<div>老师假如一条SQL语句执行100毫秒，我们一般觉得需要去优化SQL语句，但是也可能是等到磁盘读取消耗了大部分时间，我们如何区分这种情况？</div>2020-04-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Ce5DHQHpoeWBDMtibPAO9QKfRgRz9RvA3jgibMfJnyIXmOgZulVW02NYtn6ibF2fGNMQZ7z6LopHrknqB6MAzP1pw/132" width="30px"><span>rainbowzhouj</span> 👍（2） 💬（1）<div>CPU的处理速度与磁盘的处理速度不同，Buffer能起到协调和缓冲的作用，增加Buffer增加了缓冲的空间，故磁盘I&#47;O的压力就会减少。</div>2020-04-05</li><br/><li><img src="" width="30px"><span>Geek_6a9aeb</span> 👍（1） 💬（1）<div>原文:这个 bi 挺高，能达到 30 万以上。那这个值说明了什么呢？我们来算一算。
bi 是指每秒读磁盘的块数。 
-------------------------------------------
老师这里，30万是指有30万块数，还是30万kb的数据， 如果是kb那没有必要查一块是多大的呀？</div>2021-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/83/69/a9201594.jpg" width="30px"><span>。。。</span> 👍（1） 💬（1）<div>继续打卡</div>2020-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/06/ac/55fba20b.jpg" width="30px"><span>qtracer</span> 👍（0） 💬（1）<div>（1）为什么加大 buffer 可以减少磁盘 I&#47;O 的压力？
buffer可以缓存和合并来自文件系统的写请求，当积累足够多刷盘的时候，可以顺序写，提高写效率。
（2）为什么说 TPS 趋势要在预期之内？
TPS趋势不在预期内，无法准确判断瓶颈在什么时候出现的，不利于进一步分析。</div>2024-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/02/e0/5e11188d.jpg" width="30px"><span>坚持半途而废</span> 👍（0） 💬（1）<div>一块是4096个字节，读每秒到了300000次
为啥是：
（300000*1024）&#47;1024&#47;1024？
不应该是：
（300000*4096）&#47;1024？</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/02/e0/5e11188d.jpg" width="30px"><span>坚持半途而废</span> 👍（0） 💬（1）<div>确实没有看明白，怎么等于300M的</div>2021-11-05</li><br/><li><img src="" width="30px"><span>Geek_6a9aeb</span> 👍（0） 💬（1）<div>老师，看了一下午太困惑了，后面一下子就写到优化的动作，看 shared_buffers 最后一下子是20g, 没看到调优前这些值是多大的？ 难道调优前是特别小吗？</div>2021-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/de/d4/b83c4185.jpg" width="30px"><span>David.cui</span> 👍（0） 💬（1）<div>老师，我遇到一个国产数据库的的压测场景。数据库+Loadrunner。loadrunner录制好了脚本，通过增加用户数来增加压力。刚开始通过增加用户把数据库的CPU压满了，TPS还可以。
后来数据库做了一个调优，TPS一下就高出来很多，但是CPU再也上不去了，基本上就维持在30-40%左右。我怀疑是数据库测使用了类似于结果集缓存的技术，只是给Loadrunner返回结果，至于结果的准确性就无从知道了。但是怎么去确认呢？</div>2020-12-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Ce5DHQHpoeWBDMtibPAO9QKfRgRz9RvA3jgibMfJnyIXmOgZulVW02NYtn6ibF2fGNMQZ7z6LopHrknqB6MAzP1pw/132" width="30px"><span>rainbowzhouj</span> 👍（0） 💬（1）<div>第一个问题，为什么加大 Buffer 可以减少磁盘 I&#47;O 的压力？
</div>2020-04-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Ce5DHQHpoeWBDMtibPAO9QKfRgRz9RvA3jgibMfJnyIXmOgZulVW02NYtn6ibF2fGNMQZ7z6LopHrknqB6MAzP1pw/132" width="30px"><span>rainbowzhouj</span> 👍（0） 💬（1）<div>高老师，您好，以下是我对两个问题的思考：

第二个问题，为什么说 TPS 趋势要在预期之内？
此问题类比测试人员设计测试用例，每条用例你要知道它对应的预期结果是什么。若执行后，预期结果与实际结果一致，那么就通过；反之，异常则需要提Bug，分析定位问题的原因，然后解决。</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/43/35/04f1ad16.jpg" width="30px"><span>你比昨天快乐🌻</span> 👍（0） 💬（1）<div>酣畅淋漓，看完了，有种跃跃欲试的感觉，难道是幻想，哈哈</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1b/ab/a5f88914.jpg" width="30px"><span>kubxy</span> 👍（0） 💬（3）<div>老师，在分析过程中，对数据量的计算是否不准确？
磁盘的块大小为4096B，那么30万个磁盘块的数据量应该是：
300,000 * 4096B &#47; 1024 &#47; 1024 = 1172M</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/3e/82202cc8.jpg" width="30px"><span>月亮和六便士</span> 👍（0） 💬（1）<div>老师，1jmeter  tps是150  2jmeter  tps是200能说明什么？ 在场景对比中增加jmeter数量我怎么觉得是压力不够呢，怎么能说明server哪个节点有瓶颈</div>2020-03-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ibaGFsFicWRKlUjhGsw4ibm9eGLQHrmlwxia1W28yqDUNbao2YD1icAQ07ux3mDZviaZACicsicoibrCndCV1kStN3PuPYw/132" width="30px"><span>Geek_65c0a2</span> 👍（0） 💬（1）<div>刚开始分析时使用vmstat，发现bi高。
如果这时看top命令的话，iowait应该也高吧？</div>2020-03-04</li><br/>
</ul>