了解了如何使用共享内存和信号量集合之后，今天我们来解析一下，内核里面都做了什么。

不知道你有没有注意到，咱们讲消息队列、共享内存、信号量的机制的时候，我们其实能够从中看到一些统一的规律：**它们在使用之前都要生成key，然后通过key得到唯一的id，并且都是通过xxxget函数。**

在内核里面，这三种进程间通信机制是使用统一的机制管理起来的，都叫ipcxxx。

为了维护这三种进程间通信进制，在内核里面，我们声明了一个有三项的数组。

我们通过这段代码，来具体看一看。

```
struct ipc_namespace {
......
	struct ipc_ids	ids[3];
......
}

#define IPC_SEM_IDS	0
#define IPC_MSG_IDS	1
#define IPC_SHM_IDS	2

#define sem_ids(ns)	((ns)->ids[IPC_SEM_IDS])
#define msg_ids(ns)	((ns)->ids[IPC_MSG_IDS])
#define shm_ids(ns)	((ns)->ids[IPC_SHM_IDS])
```

根据代码中的定义，第0项用于信号量，第1项用于消息队列，第2项用于共享内存，分别可以通过sem\_ids、msg\_ids、shm\_ids来访问。

这段代码里面有ns，全称叫namespace。可能不容易理解，你现在可以将它认为是将一台Linux服务器逻辑的隔离为多台Linux服务器的机制，它背后的原理是一个相当大的话题，我们需要在容器那一章详细讲述。现在，你就可以简单的认为没有namespace，整个Linux在一个namespace下面，那这些ids也是整个Linux只有一份。

接下来，我们再来看struct ipc\_ids里面保存了什么。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/11/e7/044a9a6c.jpg" width="30px"><span>book尾汁</span> 👍（7） 💬（1）<div>补充下该查了下file是VFS框架的一个基本概念，一切皆文件指的就是这个,f,然后在这个file下面会有各种各样的实现,比如设备是文件 sock是文件 pipe是文件 共享内存也是文件,file结构体里面都是一些通用的属性,而private_data里面是一些各个披着文件外衣的各种结构体的一个独特的东西,因此这里会有两个file,vm_file就是这个外壳,其private_data里就是共享内存的相关数据</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/11/e7/044a9a6c.jpg" width="30px"><span>book尾汁</span> 👍（5） 💬（3）<div>共享内存:
创建共享内存,通过shmget系统调用来创建一个共享内存,主要是通过key来创建一个struct kern_ipc_perm,信号量 队列和共享内存的结构都是一样的,可以通过强制类型转换来转化成任意一个类型.然后接下来去填充这个结构,然后将一个文件与共享内存关联,内存映射有两种方式一种是匿名映射 一种是映射到一个文件,物理内存是不能共享的,文件可以跨进程共享,所以要映射到文件.但这里的文件是一个特殊的文件系统内存文件系统上的文件,这个内存文件系统也会在系统初始化的时候注册 挂载, 该文件也有目录项和inode以及其fs_operation,然后会将新创建的共享内存对象加入到shm_ids基数上,并将其加到当前进程的sysvshm队列中.

现在共享内存其实还只是内核中的一个结构体,我们只有共享内存的id,要想使用共享内存还要通过id来将其映射到使用者的用户态的进程空间中,通过shmat系统调用可以做到这一点,该系统调用的主要工作如下:
1 通过共享内存的ip在 shm_ids基数树上找到该共享内存的结构体,然后取出内存文件系统里file并将其赋值给新创建的struct shm_file_data-&gt;file,这里我们已经有了可以共享的文件&quot;file&quot;,然后在用户进程虚拟空间的mmap映射区分配一个vm_area struct来做文件映射就可以了,将vm_area_struct里的vm_file的private_data指向shm_file_data,为什么不能直接用file呢?private_data貌似只有共享内存才有用,不太理解,可能因为vm_file有其独特的file_operation的问题吧,两个file&#39;虽然可以是同一类结构体,但差异还是很大.在创建vm_file的过程中应该可以找到答案,略过,映射内存时还会将vm_area的vm_ops先指向shmem_vm_ops,然后在指向shm_vm_ops, 将shm_file_data的vm_ops指向shmem_vm_ops即内存文件系统的文件的vm_ops,到这里就完成了.后面进程读或写数据时,如果对应的页表项没有建立会触发缺页异常,跟之前的缺页异常流程差不多,最终会调用内存文件系统的缺页异常函数来分配对应的物理页,并建立页表项.</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/2e/93812642.jpg" width="30px"><span>Amark</span> 👍（2） 💬（1）<div>老师有没有什么通俗易懂的资料，您将的太专业了</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7a/e3/145adba9.jpg" width="30px"><span>不一样的烟火</span> 👍（0） 💬（1）<div>听完了 快点更新😁</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a6/43/cb6ab349.jpg" width="30px"><span>Spring</span> 👍（20） 💬（1）<div>文章一遍看不懂但底下总结的图很好，终于明白了为什么需要两个file。file1是shmem内存文件系统里的文件，file2是进程虚拟内存里映射的文件，所以file1是属于共享内存的，file2是属于某个进程的。</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fe/34/67c1ed1e.jpg" width="30px"><span>小橙子</span> 👍（12） 💬（1）<div>工作了几年 ，业务代码写多了，框架与API调来调去的，遇到很多疑难杂症，还是不明所以。
回过头再看下 操作系统真是核心，很多人说操作系统就是功夫里面的易筋经，内功章法。学习了操作系统，再看很多其他的技术，感觉更自然，理解的更深刻了。一直想读内核代码，但是啃起来很费劲，这个专栏一直再看，越看越喜欢，很多篇章都会反复的看。相信看完专栏后，再去看一些深入理解linux内核，会清晰很多。</div>2019-11-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eov38ZkwCyNoBdr5drgX0cp2eOGCv7ibkhUIqCvcnFk8FyUIS6K4gHXIXh0fu7TB67jaictdDlic4OwQ/132" width="30px"><span>珠闪闪</span> 👍（7） 💬（1）<div>文章两遍读下来蒙蒙的，最后对着总结图把共享内存的创建和在用户态映射的流程理顺了。关键就是因为共享内存刚开始申请的物理内存无法在进程中共享，所以先要把物理内存的shmid_kernel对应到shmem文件系统的一个文件，这样shmem中的文件可以再进程中共享；然后在shmat函数时，相当于将shm映射到shmem的file2，先映射到shmem文件系统的文件file1，然后再通过file1的mmap函数完成shm_file_data和vm_area_struct的ops设置。这样内存映射完毕后，并没有真的分配物理内存，当访问内存会触发缺页异常。然后vm_area_struct的vm_ops的shm_fault会调用shm_file_data的vm_ops的shmem_fault。最后在page cache中找一个空闲页，或者创建一个空闲页。</div>2020-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fd/08/c039f840.jpg" width="30px"><span>小鳄鱼</span> 👍（1） 💬（0）<div>为了统一操作入口：一切皆文件。构建了各种各样的“文件系统”。共享内存文件系统，硬盘文件系统（ext4等），设备文件系统，相信还有各种各样的文件系统！虽然感觉复杂了，但是实际的场景本来就不简单。反而统一入口之后，“上层建筑”的开发人员不再需要关系底层的具体实现，从而实现并行开发，独立维护。</div>2022-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/b8/94/d20583ef.jpg" width="30px"><span>NeverSeeYouAgainBUG</span> 👍（0） 💬（0）<div>哎呀超哥，深入浅出啊深入浅出啊。关键在 浅出，要好好总结，</div>2022-06-12</li><br/><li><img src="" width="30px"><span>Geek_2b44d4</span> 👍（0） 💬（0）<div>这个page cache 跟swap的选择时机是怎样的？</div>2022-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8d/3b/42d9c669.jpg" width="30px"><span>艾瑞克小霸王</span> 👍（0） 💬（0）<div>对于 sem_ids、msg_ids、shm_ids 各有一棵基数树
---------------------------------------------------
应该是共享一个树吧？</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/fe/f2ce12cd.jpg" width="30px"><span>Leosocy</span> 👍（0） 💬（0）<div>seq 和 next_id 用于一起生成 ipc 唯一的 id，因为信号量，共享内存，消息队列，它们三个的 id 也不能重复

这句话不太明白，不同的ipc_ids不是有不同的idr吗？为什么要保证他们三个id不重复？</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/90/8f/9c691a5f.jpg" width="30px"><span>奔跑的码仔</span> 👍（0） 💬（0）<div>将本节所讲的共享内存实现流程与文件内存映那节所讲的流程对比着梳理一下，感觉明朗了好多</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1c/6f/3ea2a599.jpg" width="30px"><span>嘉木</span> 👍（0） 💬（0）<div>C的面向对象居然这么巧妙</div>2019-08-13</li><br/>
</ul>