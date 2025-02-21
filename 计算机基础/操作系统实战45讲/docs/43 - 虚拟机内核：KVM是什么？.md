你好，我是LMOS。

上节课，我们理解了Linux里要如何实现系统API。可是随着云计算、大数据和分布式技术的演进，我们需要在一台服务器上虚拟化出更多虚拟机，还要让这些虚拟机能够弹性伸缩，实现跨主机的迁移。

而虚拟化技术正是这些能力的基石。这一节课，就让我们一起探索一下，亚马逊、阿里、腾讯等知名公司用到的云虚拟主机，看看其中的核心技术——KVM虚拟化技术。

## 理解虚拟化的定义

什么是虚拟化？在我看来，虚拟化的本质是一种资源管理的技术，它可以通过各种技术手段把计算机的实体资源（如：CPU、RAM、存储、网络、I/O等等）进行**转换和抽象**，让这些资源可以重新分割、排列与组合，实现**最大化使用物理资源的目的**。

## 虚拟化的核心思想

学习了前面的课程我们发现，操作系统的设计很高明，已经帮我们实现了单机的资源配置需求，具体就是在一台物理机上把CPU、内存资源抽象成进程，把磁盘等资源抽象出存储、文件、I/O等特性，方便之后的资源调度和管理工作。

但随着时间的推移，我们做个统计就会发现，其实现在的PC机平常可能只有50%的时间处于工作状态，剩下的一半时间都是在闲置资源，甚至要被迫切换回低功耗状态。这显然是对资源的严重浪费，那么我们如何解决资源复用的问题呢？
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（12） 💬（4）<div>以我所在的腾讯云为例。
腾讯云服务器 CVM 支持用户自定义一切资源：CPU、内存、硬盘、网络、安全等，并可以在需求发生变化时轻松地调整它们，还支持随时扩容，迁移，运维等管理功能。
一个成熟的IAAS平台搭建起来不容易啊，要考虑的事情太多了。</div>2021-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（3） 💬（2）<div>装虚拟机出现过ghost系统（如win系统ghost版），在VM虚拟机上面识别不了，需要装原版官网下载的非ghost版本才安装成功，以及AMD的cpu装苹果系统也没成功，故认为开发虚拟机系统（如VM），需要对厂家的cpu指令以及各系统的启动流程有一定的了解。如此才好“欺骗”，虚拟机安装系统失败的很大部分原因是没找对原版系统，也就是修改过的系统启动流程和虚拟机表中的流程不完全一致，识别不了。
故，认为开发虚拟机可以单独做一个启动表（允许修改），还有就是扫描表，就是在安装系统前对要装的系统进行扫描，识别不了的东西也显示出来，方便用户网上查询和修改参数，而不是猜。还有就是文件格式的识别需要改进，iso或者dmg都能识别最好，这样覆盖的厂家更多！
还可以设计一种网络虚拟机，就是虚拟机装在A电脑上，但是用户在B电脑上，用户的操作通过平台翻译成标准信息输出，然后传送到A电脑上，这样就不用考虑用户在B电脑（手机）用的是什么系统，硬件性能如何。只要他能联网就行，这样可以在A电脑上允许多个用户分时间操作，更能利用好资源。</div>2021-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（8） 💬（1）<div>二、下半部分
5、在调用ioctl时
SYSCALL_DEFINE3(ioctl, unsigned int, fd, unsigned int, cmd, unsigned long, arg)
-&gt;vfs_ioctl，会用到vfs_ioctl.unlocked_ioctl也就是kvm_vm_ioctl

kvm_vm_ioctl-&gt;kvm_vm_ioctl_create_vcpu
-&gt;kvm_arch_vcpu_precreate
-&gt;kvm_vcpu_init
-&gt;kvm_arch_vcpu_create
-&gt;kvm_get_kvm
-&gt;create_vcpu_fd，生成设备文件inode
-&gt;kvm_arch_vcpu_postcreate

其中，kvm_arch_vcpu_create
-&gt;kvm_mmu_create
-&gt;vcpu-&gt;arch.user_fpu = kmem_cache_zalloc(x86_fpu_cache, GFP_KERNEL_ACCOUNT);
-&gt;kvm_pmu_init(vcpu);
-&gt;kvm_hv_vcpu_init(vcpu);
-&gt;kvm_x86_ops.vcpu_create(vcpu);
-&gt;kvm_vcpu_mtrr_init(vcpu);
-&gt;vcpu_load(vcpu);
-&gt;kvm_vcpu_reset(vcpu, false);
-&gt;kvm_init_mmu(vcpu, false);  &#47;&#47;包括init_kvm_tdp_mmu和init_kvm_softmmu两种虚拟化方式

6、启动虚拟机，还是文件操作
static struct file_operations kvm_vcpu_fops = {
    .release        = kvm_vcpu_release,
    .unlocked_ioctl = kvm_vcpu_ioctl,
    .mmap           = kvm_vcpu_mmap,
    .llseek     = noop_llseek,
    KVM_COMPAT(kvm_vcpu_compat_ioctl),
};

7、在调用ioctl时KVM_RUN
SYSCALL_DEFINE3(ioctl, unsigned int, fd, unsigned int, cmd, unsigned long, arg)
-&gt;vfs_ioctl，会用到vfs_ioctl.unlocked_ioctl也就是kvm_vcpu_ioctl

kvm_vcpu_ioctl-&gt;
case KVM_RUN: 
  kvm_arch_vcpu_ioctl_run

其中，kvm_arch_vcpu_ioctl_run-&gt;vcpu_run-&gt;vcpu_enter_guest

8、IO同样有虚拟化和半虚拟化两种，一个处理函数为kvm_fast_pio，另一个为kvm_emulate_instruction</div>2021-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（6） 💬（1）<div>一、上半部分
1、内核模块初始化
module_init(vmx_init)-&gt;kvm_init
module_init(svm_init)-&gt;kvm_init

其中，kvm_init
-&gt;kvm_arch_init
-&gt;kvm_irqfd_init
-&gt;kvm_arch_hardware_setup
-&gt;misc_register(&amp;kvm_dev)

2、从数据结构角度，又可以看到了设备皆为文件的思想
static struct miscdevice kvm_dev = {
    KVM_MINOR,
    &quot;kvm&quot;,
    &amp;kvm_chardev_ops,
};

static struct file_operations kvm_chardev_ops = {
    .unlocked_ioctl = kvm_dev_ioctl,
    .llseek     = noop_llseek,
    KVM_COMPAT(kvm_dev_ioctl),
};

通过misc_register，实现了操作的绑定。

3、通过上面的数据结构，我们就可以找到创建虚拟机的方法，并生成控制文件
kvm_dev.kvm_chardev_ops.kvm_dev_ioctl

ioctl系统调用KVM_CREATE_VM，效果也是一样的：
SYSCALL_DEFINE3(ioctl, unsigned int, fd, unsigned int, cmd, unsigned long, arg)
-&gt;vfs_ioctl，会用到vfs_ioctl.unlocked_ioctl也就是kvm_dev_ioctl

-&gt;case KVM_CREATE_VM:
-&gt;        r = kvm_dev_ioctl_create_vm(arg);
-&gt;file = anon_inode_getfile(&quot;kvm-vm&quot;, &amp;kvm_vm_fops, kvm, O_RDWR);

其中，kvm_dev_ioctl_create_vm
-&gt;kvm_create_vm
-&gt;-&gt;kvm_arch_init_vm
-&gt;-&gt;hardware_enable_all
-&gt;-&gt;kvm_arch_post_init_vm
-&gt;-&gt;list_add(&amp;kvm-&gt;vm_list, &amp;vm_list);

4、生成虚拟CPU套路很相似，仍是文件操作
static struct file_operations kvm_vm_fops = {
    .release        = kvm_vm_release,
    .unlocked_ioctl = kvm_vm_ioctl,
    .llseek     = noop_llseek,
    KVM_COMPAT(kvm_vm_compat_ioctl),
};
创建虚拟机时，anon_inode_getfile(&quot;kvm-vm&quot;, &amp;kvm_vm_fops, kvm, O_RDWR)，实际上就把文件和kvm_vm_fops绑定了起来。</div>2021-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f4/48/2242bed9.jpg" width="30px"><span>吴建平</span> 👍（0） 💬（1）<div>文中用到的kvm的源码，是linux的么，哪个版本的，或者去哪里可以下载到对应源码
</div>2022-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（0） 💬（1）<div>老师，JVM 属于软虚拟还是硬虚拟？</div>2022-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（1）<div>秀啊</div>2022-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/66/11/f7408e3e.jpg" width="30px"><span>云师兄</span> 👍（0） 💬（1）<div>软硬结合才是虚拟化的关键啊！</div>2021-09-08</li><br/><li><img src="" width="30px"><span>springXu</span> 👍（0） 💬（1）<div>这课的例子和内容相当精彩，还是意犹未尽呀。由于虚拟化知识欠缺了，想问还有后续不？</div>2021-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/09/5c/b5d79d20.jpg" width="30px"><span>李亮亮</span> 👍（0） 💬（0）<div>哥，你太强了。什么都懂。</div>2024-08-29</li><br/>
</ul>