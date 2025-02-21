IPC这块的内容比较多，为了让你能够更好地理解，我分成了三节来讲。前面我们解析完了共享内存的内核机制后，今天我们来看最后一部分，信号量的内核机制。

首先，我们需要创建一个信号量，调用的是系统调用semget。代码如下：

```
SYSCALL_DEFINE3(semget, key_t, key, int, nsems, int, semflg)
{
	struct ipc_namespace *ns;
	static const struct ipc_ops sem_ops = {
		.getnew = newary,
		.associate = sem_security,
		.more_checks = sem_more_checks,
	};
	struct ipc_params sem_params;
	ns = current->nsproxy->ipc_ns;
	sem_params.key = key;
	sem_params.flg = semflg;
	sem_params.u.nsems = nsems;
	return ipcget(ns, &sem_ids(ns), &sem_ops, &sem_params);
}
```

我们解析过了共享内存，再看信号量，就顺畅很多了。这里同样调用了抽象的ipcget，参数分别为信号量对应的sem\_ids、对应的操作sem\_ops以及对应的参数sem\_params。

ipcget的代码我们已经解析过了。如果key设置为IPC\_PRIVATE则永远创建新的；如果不是的话，就会调用ipcget\_public。

在ipcget\_public中，我们能会按照key，去查找struct kern\_ipc\_perm。如果没有找到，那就看看是否设置了IPC\_CREAT。如果设置了，就创建一个新的。如果找到了，就将对应的id返回。

我们这里重点看，如何按照参数sem\_ops，创建新的信号量会调用newary。

```
static int newary(struct ipc_namespace *ns, struct ipc_params *params)
{
	int retval;
	struct sem_array *sma;
	key_t key = params->key;
	int nsems = params->u.nsems;
	int semflg = params->flg;
	int i;
......
	sma = sem_alloc(nsems);
......
	sma->sem_perm.mode = (semflg & S_IRWXUGO);
	sma->sem_perm.key = key;
	sma->sem_perm.security = NULL;
......
	for (i = 0; i < nsems; i++) {
		INIT_LIST_HEAD(&sma->sems[i].pending_alter);
		INIT_LIST_HEAD(&sma->sems[i].pending_const);
		spin_lock_init(&sma->sems[i].lock);
	}
	sma->complex_count = 0;
	sma->use_global_lock = USE_GLOBAL_LOCK_HYSTERESIS;
	INIT_LIST_HEAD(&sma->pending_alter);
	INIT_LIST_HEAD(&sma->pending_const);
	INIT_LIST_HEAD(&sma->list_id);
	sma->sem_nsems = nsems;
	sma->sem_ctime = get_seconds();
	retval = ipc_addid(&sem_ids(ns), &sma->sem_perm, ns->sc_semmni);
......
	ns->used_sems += nsems;
......
	return sma->sem_perm.id;
}
```

newary函数的第一步，通过kvmalloc在直接映射区分配一个struct sem\_array结构。这个结构是用来描述信号量的，这个结构最开始就是上面说的struct kern\_ipc\_perm结构。接下来就是填充这个struct sem\_array结构，例如key、权限等。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/bf/aa/abb7bfe3.jpg" width="30px"><span>免费的人</span> 👍（4） 💬（3）<div>消息队列的内核实现好像没讲过？</div>2019-07-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ASWNK7fz2Wo2nzcbxhOsgeOUibSdtGo9icibf7WmXoTLB5lCyeiaC1ibVRVmtNp4P6ocvViaD6Z5LLXTyibgyNBc1pa9A/132" width="30px"><span>Geek_835e66</span> 👍（2） 💬（2）<div>请问消息队列的内容在哪里？</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d2/f1/c071cffa.jpg" width="30px"><span>一只特立独行的猪</span> 👍（1） 💬（1）<div>我们来看进程 2。我们调用 semop，将 semaphore1 的三个信号量的值，分别减 3、加 2 和加 1，从而信号量的值变为 1、7、1   ???</div>2020-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/c2/adba355c.jpg" width="30px"><span>王之刚</span> 👍（0） 💬（1）<div>请问一下老师，在应用程序开发中，像信号量 共享内存这些内核资源怎么样防止泄漏呢？比如有进程a和b用共享内存共享数据，共享内存资源由教程a申请和维护，但由于异常情况导致教程异常退出导致共享内存资源没有释放，导致了申请的共享内存没有释放。这种情况一般怎么处理呢？Linux内核是否有相关资源保护吗？谢谢了</div>2019-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/fd/035f4c94.jpg" width="30px"><span>欢乐小熊</span> 👍（16） 💬（0）<div>终于把共享内存和信号量集合的知识串联在一起了, 其中的操作的确有些复杂

共享内存若想实现进程之间的同步读写, 则需要配合信号量共同使用
- **共享内存**
  - **共享内存的创建**
    - 开辟共享内存区域, 使用 shmid_kernel 描述
    - 通过 kvmalloc 在内核的直接映射区分配一个 shmid_kernel 结构体
    - 将内存映射到文件
      - 这个文件并非磁盘文件, **而是通过内存文件系统 shmem 创建的内存文件**
      - 这么做的原因是因为**文件可以跨进程共享**
      - 将这个 shmid_kernel 挂载到共享内存基树上, 返回对应的 id
  - **共享内存的映射**
    - 通过 id 在共享内存基树上找到对应的共享内存描述 shmid_kernel
    - 创建一个 shm_file_data 指向共享内存的内存文件
    - 创建一个 file 指向 shm_file_data
    - 在用户空间找一块内存区域, 将这个 file 映射到用户地址空间
      - 通过文件映射之后, 便可以在用户空间操作这块内存了
- **信号量集合**
  - 信号量集合的创建
    - 创建 sem_array 结构体, 用于描述信号量
    - 将这个 sem_array 信号量添加到基树上, 返回对应的 id
  - 信号量集合的初始化
    - SETALL: 为所有信号量集合赋值
    - SETVAL: 为指定信号量赋值
  - 操作信号量集合
    - 调用 **perform_atomic_semop** 尝试从操作队列中读取执行
    - 若执行成功, 则说明无需等待
      - 调用 do_smart_update, 看看这次操作能够激活等待队列中的哪些进程
      - 调用 **wake_up_q** 唤醒因为信号量阻塞的进程
    - 若需要等待
      - 根据是操作信号量还是信号集合, 将其挂载到对应的 pending_alter 中
      - 执行 looper 等待, 直到 timeout 或者被 wake_up_q 唤醒
        - 若未设置 timeout, 则让出 CPU 资源
</div>2019-07-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（11） 💬（1）<div>思考问题总结了个图：
https:&#47;&#47;user-images.githubusercontent.com&#47;12036324&#47;67062221-431e6f80-f195-11e9-9dd1-4353ebbc730c.png

https:&#47;&#47;github.com&#47;helios741&#47;myblog&#47;issues&#47;60
</div>2019-10-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoVRER40LhyAhBK6YgPYibRzWARkc3efUquib4j9BPru4y8FfvXK2sBPbXej9314pZdfdcxb07RcjZw/132" width="30px"><span>酷酷的嵩</span> 👍（1） 💬（0）<div>在 perform_atomic_semop 函数中，对于计算和修改是如何确保原子性的？</div>2022-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（1） 💬（1）<div>老师，有没有打算讲一下POSIX IPC呢？</div>2019-07-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLMDBq7lqg9ZasC4f21R0axKJRVCBImPKlQF8yOicLLXIsNgsZxsVyN1mbvFOL6eVPluTNgJofwZeA/132" width="30px"><span>Run</span> 👍（0） 💬（2）<div>第一次看到这个的时候月薪8k</div>2021-12-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/NyFOEueITjaGLpakMEuWAqVQjo1uDIXlpDdpCxXGfaWiaXzibLQ3WgOFCe8D9FvCmyjsGT7jDsLUbkt8jt2aVs9g/132" width="30px"><span>geek</span> 👍（0） 💬（1）<div>一个进程已经等待在心信号量上时，如果另一个进程释放了此信号量，原先等待的进程如何知道该提前退出了？按文中的代码，是要一直等到超时，如果没超时，就会一直等下去。</div>2021-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/9c/1e/fdce4a6b.jpg" width="30px"><span>小怪盗kid</span> 👍（0） 💬（0）<div>老师有两个问题:1.共享内存的创建，是不是只要创建就是在内存中存在，与创建共享内存的进程无关吧，即使该进程异常退出，也不会影响创建好的共享内存？2.某个进程获取信号量，但是这个进程也是异常退出了，信号量没有释放，这个恢复工作由内核完成，还是其他进程需要判断undo结构进行恢复？</div>2021-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（0） 💬（2）<div>schedule_timeout调用完后，会让出cpu，过一段时间还会回来。这个过一段时间是多长时间啊？是说超时之后返回来吗，还是被其它信号打断睡眠之后回来？</div>2019-07-04</li><br/>
</ul>