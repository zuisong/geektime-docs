你好，我是程远。

上一讲，我们讲了Memory Cgroup是如何控制一个容器的内存的。我们已经知道了，如果容器使用的物理内存超过了Memory Cgroup里的memory.limit\_in\_bytes值，那么容器中的进程会被OOM Killer杀死。

不过在一些容器的使用场景中，比如容器里的应用有很多文件读写，你会发现整个容器的内存使用量已经很接近Memory Cgroup的上限值了，但是在容器中我们接着再申请内存，还是可以申请出来，并且没有发生OOM。

这是怎么回事呢？今天这一讲我就来聊聊这个问题。

## 问题再现

我们可以用这里的[代码](https://github.com/chengyli/training/tree/main/memory/page_cache)做个容器镜像，然后用下面的这个脚本启动容器，并且设置容器Memory Cgroup里的内存上限值是100MB（104857600bytes）。

```shell
#!/bin/bash

docker stop page_cache;docker rm page_cache

if [ ! -f ./test.file ]
then
	dd if=/dev/zero of=./test.file bs=4096 count=30000
	echo "Please run start_container.sh again "
	exit 0
fi
echo 3 > /proc/sys/vm/drop_caches
sleep 10

docker run -d --init --name page_cache -v $(pwd):/mnt registry/page_cache_test:v1
CONTAINER_ID=$(sudo docker ps --format "{{.ID}}\t{{.Names}}" | grep -i page_cache | awk '{print $1}')

echo $CONTAINER_ID
CGROUP_CONTAINER_PATH=$(find /sys/fs/cgroup/memory/ -name "*$CONTAINER_ID*")
echo 104857600 > $CGROUP_CONTAINER_PATH/memory.limit_in_bytes
cat $CGROUP_CONTAINER_PATH/memory.limit_in_bytes
```
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（74） 💬（6）<div>Momory Cgroup 应该包括了对内核内存的限制，老师给出的例子情况比较简单，基本没有使用 slab，可以试下在容器中打开海量小文件，内核内存 inode、dentry 等会被计算在内。

内存使用量计算公式（memory.kmem.usage_in_bytes 表示该 memcg 内核内存使用量）：
memory.usage_in_bytes = memory.stat[rss] + memory.stat[cache] + memory.kmem.usage_in_bytes

另外，Memory Cgroup OOM 不是真正依据内存使用量 memory.usage_in_bytes，而是依据 working set（使用量减去非活跃 file-backed 内存），working set 计算公式：
working_set = memory.usage_in_bytes - total_inactive_file</div>2020-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bf/aa/32a6449c.jpg" width="30px"><span>蒋悦</span> 👍（12） 💬（1）<div>您好，问一个操作系统相关的问题。根据我的理解，操作系统为了性能会在刷盘前将内容放在page cache中（如果可以申请的话），后续合适的时间刷盘。如果是这样的话，在一定条件下，可能还没刷盘，这个内存就需要释放给rss使用。这时必然就会先刷盘。这样会导致 系统 malloc 的停顿，对吗？如果是这样的话，另外一个问题就是 linux 是如何保证 磁盘的数据的 crash safe 的呢？</div>2020-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/cd/3aff5d57.jpg" width="30px"><span>Alery</span> 👍（9） 💬（3）<div>首先，很感谢老师，从您这几节关于容器的文章学到了很多知识点，感觉自己以前了解的容器都是些皮毛，在学习的过程中发现容器的很多的问题都需要深入了解操作系统或者linux内核相关的知识，这块知识是我比较缺失的，除了继续打卡老师的文章，空闲时间还想系统的学习一下操作系统及内核相关的知识，老师可以推荐几本讲操作系统或者linux内核相关的书籍吗？</div>2020-12-05</li><br/><li><img src="" width="30px"><span>Geek3340</span> 👍（6） 💬（2）<div>page_cache是不是会被很多进程共享呢，比如同一个文件需要被多个进程读写，这样的话，page_cache会不会无法被释放呢？

另外，老师能不能讲解下，这里面的page_cache和free中的cache、buffer、shared还有buffer cache的区别呢？</div>2020-12-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/icV5dx2hqJOiaQ2S8Lh1z448lQjTZllkd6wWib21rTKq5uicIcDTr5LIYsauFEudnFWefI2xGnvXrcLNfaFrKYMuew/132" width="30px"><span>缝合怪天下无敌</span> 👍（5） 💬（1）<div>请问老师：这边结合了课程内容以及评论中的一些补充想在确认一下以下几个问题：
1 Memory Cgroup OOM 的依据是working set吗？还是说rss，working set都会进行判断
2 这边看到有评论的大佬给了对于memory.usage_in_bytes 以及working_set ，但是对这两个间的关系有一些疑惑，想请问一下老师是否可以理解为working_set = memory.stat[rss] + memory.kmem.usage_in_bytes+常用的page cache 这样？</div>2021-02-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/icV5dx2hqJOiaQ2S8Lh1z448lQjTZllkd6wWib21rTKq5uicIcDTr5LIYsauFEudnFWefI2xGnvXrcLNfaFrKYMuew/132" width="30px"><span>缝合怪天下无敌</span> 👍（2） 💬（3）<div>老师，这边在请教两个问题，
1 cgroup底下的memory.stat文件中inactive_file 是否在oom时能回收，因为这边看到代码里描述workset = memory.usage-inactive_file这个值获得的，而这边看到在评论区里有大佬提到Memory Cgroup OOM会以working set为标准
2 在查看某个容器的时候发现container_memory_working_set_bytes远小于container_memory_rss指标，原因是因为inactive_file的值非常大，因此这个时候内存监控的时候用container_memory_working_set_bytes似乎看不出来是否马上就要oom这样，因此比较困惑如果想要监控内存的使用率判断oom该使用哪个指标？
下面是查看cgroup的情况：
cat &#47;sys&#47;fs&#47;cgroup&#47;memory&#47;memory.stat 
....
rss 2666110976
...
inactive_anon 0
active_anon 172163072
inactive_file 2489147392
active_file 7667712
....
total_cache 2596864
total_rss 2666110976
total_rss_huge 276824064</div>2021-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/15/4d/bbfda6b7.jpg" width="30px"><span>笃定</span> 👍（2） 💬（1）<div>老师，如果新程序申请的内存大小是大于之前进程的page cache内存大小的；是不是就会发生oom？</div>2021-03-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIz9dKN1C8rKQoaVtmEGdzObhlia6zAfTsPYOm4ibz39VjTbu7Aia1LyeedHR26b6nxUtcCufpichcYgw/132" width="30px"><span>上邪忘川</span> 👍（2） 💬（1）<div>看了这篇文章，对于linux内存的机制和free的使用有了很大的认识</div>2020-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/dc/19/c058bcbf.jpg" width="30px"><span>流浪地球</span> 👍（2） 💬（1）<div>请问文中提到rss包括共享内存的大小，那pss呢，pss和rss的区别不是 是否包括共享内存的大小码？</div>2020-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/02/33/b4bb0b9c.jpg" width="30px"><span>仲玄</span> 👍（0） 💬（1）<div>老师,  page cache 如果都被回收了, 会不会没办法使用page cache 导致磁盘很慢?</div>2021-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/e0/7b/ab5cec6d.jpg" width="30px"><span>Q～Q</span> 👍（0） 💬（1）<div>请问老师： 容器内file-backed过大导致容器oom这个案例有遇到过吗 我现在遇到过一个现象 容器内由于读取的是宿主机的proc&#47;meminfo 导致cache没办法回收 </div>2021-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2a/ff/a9d72102.jpg" width="30px"><span>BertGeek</span> 👍（0） 💬（1）<div>docker容器内存资源限制有了新的认知</div>2021-07-01</li><br/><li><img src="" width="30px"><span>13549804879</span> 👍（0） 💬（1）<div>老师，我看过一些liunx的书，看了很容易就忘记了。如何能做到与实践想结合，或者用代码演示kernel的代码。这样可能会容易理解。请问有什么相关的案例书籍推荐。</div>2021-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/de/94/4c1e96dd.jpg" width="30px"><span>alpha</span> 👍（0） 💬（2）<div>老师，你好 最近我们在迁移docker时发现当应用第一次去使用到swap的内存时，应用会有几秒的响应延迟？这个问题如何解决？</div>2021-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/6c/7c/5ea0190c.jpg" width="30px"><span>刘浩</span> 👍（3） 💬（1）<div>我遇见过会因为page cache高OOM的··如果我运行一个定期清cache的就不会OOM，所以容器的cache高真的不会被杀进程吗</div>2022-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/45/c6/28dfdbc9.jpg" width="30px"><span>*</span> 👍（1） 💬（0）<div>好像pss比rss更接近真实使用的物理内存</div>2022-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3d/0e/92176eaa.jpg" width="30px"><span>左氧佛沙星人</span> 👍（1） 💬（0）<div>老师好，一般active&#47;inactive_anon  是指什么呢？看了很多资料都说的很模糊</div>2021-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e2/5a/f898300f.jpg" width="30px"><span>寒焰</span> 👍（0） 💬（1）<div>老师，看了你的文章很有收获，我最近遇到了个问题，想请教下您，就是容器内部的RSS占用的不是很高，不到1个G，但是memory.usage_in_bytes 这个内核内存，使用量一直在增长，当增长到3G左右，（我们pod的memory limit为4G），就会oom，我想请教下这个内核内存是干什么的，以及如何限制它的增长。</div>2024-03-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJrDXfgDow28Xxxrj0n3MSlH3gqzdwfYPgPM82G8tpDNjIE5Uib1Emt80kYXoCEwSOk0m2T3EWp4pw/132" width="30px"><span>Geek_yhg</span> 👍（0） 💬（1）<div>有什么办法限制物理机的page cache大小</div>2024-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/78/ab/3e793aee.jpg" width="30px"><span>frost晨随</span> 👍（0） 💬（0）<div>如果只看rss值 会漏掉shmget那部分共享内存</div>2023-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/78/ab/3e793aee.jpg" width="30px"><span>frost晨随</span> 👍（0） 💬（0）<div>这里面有个很重要的坑没提：
top里 进程的rss是包括了使用到的共享内存的，比如通过ipcs shmget获得的共享内存；
然后cgroup里的memory.stat文件的rss是不包括共享内存的，它被粗暴地合并到了cache。</div>2023-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/7c/69/7f96a023.jpg" width="30px"><span>pathfinder</span> 👍（0） 💬（0）<div>请教老师，有个疑问，为什么pagecache会占这么内存呢？内核有dirty page的writeback机制，当脏页达到一定数量或者脏页驻留超过一定时间就会回刷，脏页回刷机制没起作用，还是大部分都是clean page？</div>2022-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b4/00/bfc101ee.jpg" width="30px"><span>Tendrun</span> 👍（0） 💬（0）<div>想到一个问题，能否针对某个进程触发 page cache的回收呢， 这样就能基于用户侧进程的重要程度控制释放那一个应用的cache了</div>2022-04-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eq30mvo0eATZ3Yfm5POktwic3NJSRkiagtJt1vaxyvCS22PJRm8xrulXqaLJRWQWb6zNI4zL0G2QkCA/132" width="30px"><span>heyhd9475</span> 👍（0） 💬（0）<div>老师你好。想请教一下rss里面代码段部分是不是应该属于pagecache里面，因为我看前面统计容器内存时先做了是否是匿名页的判断。在我的认知里pagecache里的页都是映射页（swapcache不知道算不算），rss里的页包含映射页和匿名页</div>2021-10-11</li><br/>
</ul>