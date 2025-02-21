你好，我是程远。今天我们聊一聊容器文件Quota。

上一讲，我们学习了容器文件系统OverlayFS，这个OverlayFS有两层，分别是lowerdir和upperdir。lowerdir里是容器镜像中的文件，对于容器来说是只读的；upperdir存放的是容器对文件系统里的所有改动，它是可读写的。

从宿主机的角度看，upperdir就是一个目录，如果容器不断往容器文件系统中写入数据，实际上就是往宿主机的磁盘上写数据，这些数据也就存在于宿主机的磁盘目录中。

当然对于容器来说，如果有大量的写操作是不建议写入容器文件系统的，一般是需要给容器挂载一个volume，用来满足大量的文件读写。

但是不能避免的是，用户在容器中运行的程序有错误，或者进行了错误的配置。

比如说，我们把log写在了容器文件系统上，并且没有做log rotation，那么时间一久，就会导致宿主机上的磁盘被写满。这样影响的就不止是容器本身了，而是整个宿主机了。

那对于这样的问题，我们该怎么解决呢？

## 问题再现

我们可以自己先启动一个容器，一起试试不断地往容器文件系统中写入数据，看看是一个什么样的情况。

用Docker启动一个容器后，我们看到容器的根目录(/)也就是容器文件系统OverlayFS，它的大小是160G，已经使用了100G。其实这个大小也是宿主机上的磁盘空间和使用情况。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（21） 💬（3）<div>容器 quota 的局限性：容器通常采用 overlay2 driver，仅支持在宿主文件系统 xfs 上开启 quota 功能。意味着 overlay over ext4 不支持 quota 功能，而实际生产环境上 ext4 的使用远多于 xfs。</div>2020-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/9d/104bb8ea.jpg" width="30px"><span>Geek2014</span> 👍（13） 💬（2）<div>上篇的评论中提到：“我们在2019年初就不用docker了。”
这篇中，老师提到了containerd，是说你们已经用containerd替换了docker吗？有机会对containerd和docker之间的使用对比做个介绍吗？</div>2020-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/86/4ff2a872.jpg" width="30px"><span>Sun</span> 👍（12） 💬（2）<div>老师，我觉得可以补充下 现在k8s 1.14 开始，默认开启 LocalStorageCapacityIsolation， 可以通过限制resources.limits.ephemeral-storage 和resources.requests.ephemeral-storage 来保护宿主机 rootfs了。</div>2020-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/7c/bb/635a2710.jpg" width="30px"><span>徐少文</span> 👍（4） 💬（1）<div>老师，CGroup子系统中没有对硬盘使用量进行限制的功能模块吗？除了通过文件系统的quota去限制还有其他的方法吗？</div>2021-07-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（4） 💬（2）<div>老师能说下你们应用容器Quota的场景么。对于无状态服务一般就是日志会写文件了，离线任务比如机器学习的模型也不敢给人家限制呀😂
</div>2020-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/93/38/71615300.jpg" width="30px"><span>DayDayUp</span> 👍（1） 💬（1）<div>老师讲的太好了，不知道面试贵司会不会有机会呢？老师在eBay哪个team啊？应届生要吗？？？</div>2021-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/c2/77a413a7.jpg" width="30px"><span>Action</span> 👍（1） 💬（1）<div>老师 为什么overlayFS 并不是docker_id 呢？
[root@localhost overlay2]# docker inspect 5440662c8db
[
    {
        &quot;Id&quot;: &quot;5440662c8db65d5d9ab522e0be1a3911584c492527fcde334c3fdec090cd3857&quot;,

        &quot;Image&quot;: &quot;sha256:300e315adb2f96afe5f0b2780b87f28ae95231fe3bdd1e16b9ba606307728f55&quot;,
  
        &quot;GraphDriver&quot;: {
            &quot;Data&quot;: {
                &quot;LowerDir&quot;: &quot;&#47;home&#47;data&#47;docker&#47;overlay2&#47;4146b7c314a97b46695a59ccdc323709eda7177b3e91ed30d3f4f9326a061584-init&#47;diff:&#47;home&#47;data&#47;docker&#47;overlay2&#47;dc1e8c89044058319c4e0b6917603f3ed8972cd155bfced0c7c0c2509ddaae14&#47;diff&quot;,
                &quot;MergedDir&quot;: &quot;&#47;home&#47;data&#47;docker&#47;overlay2&#47;4146b7c314a97b46695a59ccdc323709eda7177b3e91ed30d3f4f9326a061584&#47;merged&quot;,
                &quot;UpperDir&quot;: &quot;&#47;home&#47;data&#47;docker&#47;overlay2&#47;4146b7c314a97b46695a59ccdc323709eda7177b3e91ed30d3f4f9326a061584&#47;diff&quot;,
                &quot;WorkDir&quot;: &quot;&#47;home&#47;data&#47;docker&#47;overlay2&#47;4146b7c314a97b46695a59ccdc323709eda7177b3e91ed30d3f4f9326a061584&#47;work&quot;
            },
            &quot;Name&quot;: &quot;overlay2&quot;
        },

    }
]
</div>2020-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/f5/e3f5bd8d.jpg" width="30px"><span>宝仔</span> 👍（1） 💬（1）<div>这个是一定要基于xfs文件系统吗？如果是ext4文件系统呢？</div>2020-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/81/60/71ed6ac7.jpg" width="30px"><span>谢哈哈</span> 👍（6） 💬（0）<div>可以通过xfs_quota -x -c &quot;report -pbih &quot; 目录名称查询projectid</div>2020-12-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIz9dKN1C8rKQoaVtmEGdzObhlia6zAfTsPYOm4ibz39VjTbu7Aia1LyeedHR26b6nxUtcCufpichcYgw/132" width="30px"><span>上邪忘川</span> 👍（3） 💬（0）<div>[root@localhost ~]# xfs_quota -x -c &#39;report -h &#47;tmp&#47;xfs_prjquota&#39;
Project quota on &#47; (&#47;dev&#47;mapper&#47;centos-root)
                        Blocks              
Project ID   Used   Soft   Hard Warn&#47;Grace   
---------- --------------------------------- 
#0           3.2G      0      0  00 [------]
#2             8K   100M   100M  00 [------]
#3           100M   100M   100M  00 [------]
#101          10M      0    10M  00 [------]
</div>2020-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6c/95/bb237f51.jpg" width="30px"><span>李梦嘉</span> 👍（0） 💬（0）<div>老师好，通过xfs quota设置了容器容量后，怎么扩容呢？
</div>2024-07-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKzqiaZnBw2myRWY802u48Rw3W2zDtKoFQ6vN63m4FdyjibM21FfaOYe8MbMpemUdxXJeQH6fRdVbZA/132" width="30px"><span>kissingers</span> 👍（0） 💬（1）<div>k8s 中readonlyrootfs 也是同样的场景吧</div>2021-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（0） 💬（0）<div>之前工作中就经常因为es错误日志把宿主机的磁盘撑满。但还从未往这个方向想，还可以限制某个项目的磁盘使用量。😂</div>2021-01-03</li><br/>
</ul>