我们前面讲了，如果项目组之间需要紧密合作，那就需要共享内存，这样就像把两个项目组放在一个会议室一起沟通，会非常高效。这一节，我们就来详细讲讲这个进程之间共享内存的机制。

有了这个机制，两个进程可以像访问自己内存中的变量一样，访问共享内存的变量。但是同时问题也来了，当两个进程共享内存了，就会存在同时读写的问题，就需要对于共享的内存进行保护，就需要信号量这样的同步协调机制。这些也都是我们这节需要探讨的问题。下面我们就一一来看。

共享内存和信号量也是System V系列的进程间通信机制，所以很多地方和我们讲过的消息队列有点儿像。为了将共享内存和信号量结合起来使用，我这里定义了一个share.h头文件，里面放了一些共享内存和信号量在每个进程都需要的函数。

```
#include <stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/types.h>
#include <sys/sem.h>
#include <string.h>

#define MAX_NUM 128

struct shm_data {
  int data[MAX_NUM];
  int datalength;
};

union semun {
  int val; 
  struct semid_ds *buf; 
  unsigned short int *array; 
  struct seminfo *__buf; 
}; 

int get_shmid(){
  int shmid;
  key_t key;
  
  if((key = ftok("/root/sharememory/sharememorykey", 1024)) < 0){
      perror("ftok error");
          return -1;
  }
  
  shmid = shmget(key, sizeof(struct shm_data), IPC_CREAT|0777);
  return shmid;
}

int get_semaphoreid(){
  int semid;
  key_t key;
  
  if((key = ftok("/root/sharememory/semaphorekey", 1024)) < 0){
      perror("ftok error");
          return -1;
  }
  
  semid = semget(key, 1, IPC_CREAT|0777);
  return semid;
}

int semaphore_init (int semid) {
  union semun argument; 
  unsigned short values[1]; 
  values[0] = 1; 
  argument.array = values; 
  return semctl (semid, 0, SETALL, argument); 
}

int semaphore_p (int semid) {
  struct sembuf operations[1]; 
  operations[0].sem_num = 0; 
  operations[0].sem_op = -1; 
  operations[0].sem_flg = SEM_UNDO; 
  return semop (semid, operations, 1); 
}

int semaphore_v (int semid) {
  struct sembuf operations[1]; 
  operations[0].sem_num = 0; 
  operations[0].sem_op = 1; 
  operations[0].sem_flg = SEM_UNDO; 
  return semop (semid, operations, 1); 
} 
```

## 共享内存

我们先来看里面对于共享内存的操作。

首先，创建之前，我们要有一个key来唯一标识这个共享内存。这个key可以根据文件系统上的一个文件的inode随机生成。

然后，我们需要创建一个共享内存，就像创建一个消息队列差不多，都是使用xxxget来创建。其中，创建共享内存使用的是下面这个函数：

```
int shmget(key_t key, size_t size, int shmflag);
```

其中，key就是前面生成的那个key，shmflag如果为IPC\_CREAT，就表示新创建，还可以指定读写权限0777。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/2e/93812642.jpg" width="30px"><span>Amark</span> 👍（16） 💬（1）<div>请教一个问题，CPU调度是以进程为单位的吗，还是以线程?</div>2019-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（13） 💬（1）<div>System V IPC具有很好的移植性，但缺点也比较明显，不能接口自成一套，难以使用现有的fd操作函数。建议对比讲一下比较流行的POSIX IPC。</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1e/3a/5b21c01c.jpg" width="30px"><span>nightmare</span> 👍（4） 💬（1）<div>信号量大于1的情况，可以让进程不操作共享变量，比如操作不同的变量，比如对一批数据做操作，然后做完之后给消费端读取</div>2019-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（1） 💬（2）<div>信号量大于 1 的情况下，应该如何使用？
可以让多个进程同时访问一个共享内存。</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/ce/a8c8b5e8.jpg" width="30px"><span>Jason</span> 👍（0） 💬（2）<div>老师好，ftok提示我的机器里没有“&#47;root&#47;sharememory&#47;semaphorekey”这个文件，我随便新建一个文件可以吗？</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/50/39/14adb0f0.jpg" width="30px"><span>trllllllll</span> 👍（0） 💬（1）<div>老师，share.h 里面 include 了两次 ipc.h。</div>2019-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/2e/93812642.jpg" width="30px"><span>Amark</span> 👍（0） 💬（1）<div>如果线程是掉用的到基本单位，那么进程的共享资源呢?</div>2019-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/4f/6a/0a6b437e.jpg" width="30px"><span>有风</span> 👍（2） 💬（0）<div>信号量大于1，可以用于限流。如线程或进程的个数，访问请求的个数等。</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0b/d4/39763233.jpg" width="30px"><span>Tianz</span> 👍（2） 💬（0）<div>超哥，现在是不是推荐使用 POSIX 系列的 IPC 呢？</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8d/3b/42d9c669.jpg" width="30px"><span>艾瑞克小霸王</span> 👍（1） 💬（0）<div>信号量和锁的区别就是 信号量可以控制资源数量（&gt;1）, 而锁是 互斥排他的？</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/ce/a8c8b5e8.jpg" width="30px"><span>Jason</span> 👍（1） 💬（0）<div>这篇看的很明白，嘿嘿。</div>2019-08-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI4Gr57Aia5McdvyQco8hKpaibeeYUhQcMtaFhNtHESSF7MPq5OdQBQpCBYicl7Libt6MjWKNJvmGwODA/132" width="30px"><span>Geek_93a721</span> 👍（0） 💬（0）<div>如果大于1时，应该使用三个信号量，一个表示任务这种资源，一个表示空间这种资源，第三个将其置为1用于互斥访问。</div>2020-09-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（0） 💬（0）<div>信号量大于1的时候应该就不能控制写操作了。应该是控制读操作的进程数量。</div>2019-10-15</li><br/>
</ul>