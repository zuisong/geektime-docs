你好，我是徐文浩。

在解读完GFS的论文之后，相信你现在对“分布式系统”已经有了初步的了解。本质上，GFS是对上千台服务器、上万块硬盘的硬件做了一个封装，让GFS的使用者可以把GFS当成一块硬盘来使用。

通过GFS客户端，无论你是要读还是写海量的数据，你都不需要去操心这些数据最终要存储到哪一台服务器或者哪一块硬盘上。你也不需要担心哪一台服务器的网线可能松了，哪一块硬盘可能坏了，这些问题都由GFS这个“分布式系统”去考虑解决了。

不过，GFS仅仅是解决了数据存储和读写的问题。要知道，只是把数据读出来和写回去，只能做做数据备份，这可解决不了什么具体、有意义的问题。所幸，在GFS这个分布式文件系统之上，谷歌又在2004年发表了MapReduce的论文，也就是一个分布式计算的框架。

那么，我们今天就一起来看看，MapReduce到底是要解决什么样的问题。而要解决这些问题的系统，又应该要怎么设计。

当你仔细了解MapReduce的框架之后，你会发现MapReduce的设计哲学和Unix是一样的，叫做**“Do one thing, and do it well”**，也就是每个模块只做一件事情，但是把这件事情彻底做好。

在学完这两讲之后，你不仅应该了解什么是MapReduce，MapReduce是怎么设计的。更重要的是理解如何对系统进行抽象并做出合理的设计。在未来你自己进行系统设计的时候，为各个模块划分好职责和边界，把“Do one thing, and do it well”落到实处。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（0） 💬（4）<div>徐老师好，晚上试着读了下MapReduce的论文，比GFS的论文要简单很多。
问题一，如何按照域名统计访问频率？只需要把原来Map函数的输出从List&lt;URL, “”&gt;，变成List&lt;domainName(URL), “”&gt;。
问题二，如何按照访问人数对统计结构排序？假如还是统计URL的访问情况，Map函数的输出为List&lt;URL, USER_ID&gt;，Reduce函数对USER_ID去重，获得每个URL的访问人数。Reduce程序存在k个，不同的URL通过哈希取模的方式，也就是hash(URL) % k，分配给不同的Reduce排序。通常我们不是关心所有数据的排行情况，而是前N名的排行情况，假设N等于10000。所以每个Reduce函数只排前10000名，然后通过另一个MapReduce程序，将k个Reduce的排行结果汇总，得到全局的前10000名排行结果。</div>2021-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（10） 💬（1）<div>第二个问题，URL 访问统计结果要按访问的人数多少从高到底排序。为了减少Reduce 函数去重的时候，用户数据量比较大的问题。可以通过两次map reduce操作来减少这个数据量。

1. map以(URL+UserId, 1) 作为输出,表示某个url被某个user访问过一次，reduce输出则是 (URL+UserId, 1)，通过这个过程来去重用户量过大的问题。
2. 输入是过程1的结果，map的输出是（URL，1），reduce的输出则是（URL，sum())表示该url被访问的人数。按照访问的人数多少从高到底排序，输出URL即可。

如果数据量少的话，bash也可以，`cat $input | awk &#39;{print $1&quot; &quot;$2}&#39; | sort | uniq -c | awk &#39;{print $1}&#39; | sort | uniq -c `</div>2021-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/e6/47742988.jpg" width="30px"><span>webmin</span> 👍（6） 💬（0）<div>看到MapReduce我就会不自主的映射为递归，Map是递的过程，一路向下进行切分，Reduce是归触底向上一路进行收集。
思考题：
第二个问题与网上流传的在单机上2GB内存排序10GB大小文件的题目类似，需要通过分桶缩小每次处理的大小，按Count数划分区间，每个区间一个文件，然后再对每一个区间进行排序，最后把文件按区间顺序连在一起。这种处理过程好似快排算法，用快排来划分区间每次把数据落地进文件。</div>2021-10-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（2） 💬（2）<div>请问老师，如果所有map出来数据依然很大，在清洗的过程中的排序是磁盘操作么，是map输出到gfs然后清洗进程从gfs拷贝到磁盘么？如果数据过于大，是不是清洗也需要多台机器呢，他们之间如何沟通呢</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/60/be0a8805.jpg" width="30px"><span>陈迪</span> 👍（2） 💬（0）<div>尝试回答下思考题：
1. 按域名统计：partition函数嵌一个获取domain的方法，论文中有描述
2. 统计结果排序：看上去写两个MapReduce Job比较清楚。第一个就是统计数量，第二个专门做排序。主要是利用shuffle之后，reduce任务会对本机的全局&lt;key, lists&gt;按key排序。</div>2021-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（2） 💬（2）<div>想到个有些复杂的方法：

第一轮：map输出&lt;URL+USER_ID, &#39;&#39;&gt;，reduce时对value计数，可以得出每个url被每个用户访问了多少次&lt;URL+USER_ID, visitsByUser&gt;

第二轮：map的时候只取key中的URL部分，输出&lt;URL, visitsByUser&gt;，reduce时对value计数得到访问人数，把value相加得到访问频次，输出&lt;URL, [visits, totalVisits]&gt;

第三轮：map的时候把访问人数visits作为key，输出&lt;visits, [URL, totalVisits]&gt;。如果shuffle是按照key的大小shuffle的话，reduce原样输出应该就是排好序的结果了。 </div>2021-10-02</li><br/><li><img src="" width="30px"><span>Geek_980ded</span> 👍（0） 💬（0）<div>MapReduce过程可以理解成一群人统计选票的过程，假设有候选人A和候选人B，首先从选票箱里拿出所有的选票，分给所有初统人员，每个初统人员拿其中一摞，只要统计这一小部分中A的选票数是多少，B的选票数多少，然后把这个结果交给汇总人员。两个汇总人员分别负责合计A和B的选票。</div>2023-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/91/3bd41811.jpg" width="30px"><span>Pluto</span> 👍（0） 💬（0）<div>第二个问题： 
第一轮： map的输出是 &lt;url + user, &#39;&#39;&gt;, reduce去重得到 &lt;url + user, &#39;&#39;&gt; 

第二轮： map不做处理， 输出 &lt;url, user&gt;， reduced得到 &lt;url, sum&gt; （sum 就是把 的value 相加即可）

第三轮:   map输入 &lt;url, sum&gt;， 输出 &lt;sum, url&gt;,（数目应该是大大降低了，边界是所有url都被访问一次）,key 如果是排序的，用单一的Reduce即可</div>2022-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/99/4bdadfd3.jpg" width="30px"><span>Chloe</span> 👍（0） 💬（0）<div>对课后思考题，我的第一感觉是要把问题划分为小的模块，然后逐个解决。正好翻出了Design Pattern的书，看看5.10节，再回来讲感想。</div>2022-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（0） 💬（0）<div>现在很多人说hadoop已经快凉了～</div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/92/7b/8c7e3e61.jpg" width="30px"><span>Monroe  He</span> 👍（0） 💬（0）<div>问题2是否可以通过两个mapreduce实现：
mapreduce1: map函数  key(URL+userID): value(&#39;1&#39;)  -&gt; reduce函数去重之后的 key(URL+userID): value(&#39;1&#39;)
mapreduce2: map直接使用mapreduce1的输出， reduce 函数计数 key(URL):value(sum())</div>2021-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（0） 💬（0）<div>老师确实把mapreduce拆解的非常合理，这种合理不是简单的应用层的去拆；纵观数据系统这么多年真正合理的都是简单方便；SQL的特点就是简练-这是为何至今四十余年依然未曾衰老。</div>2021-10-02</li><br/>
</ul>