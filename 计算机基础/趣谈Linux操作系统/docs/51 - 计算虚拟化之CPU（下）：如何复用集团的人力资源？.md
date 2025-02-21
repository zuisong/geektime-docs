上一节qemu初始化的main函数，我们解析了一个开头，得到了表示体系结构的MachineClass以及MachineState。

## 4.初始化块设备

我们接着回到main函数，接下来初始化的是块设备，调用的是configure\_blockdev。这里我们需要重点关注上面参数中的硬盘，不过我们放在存储虚拟化那一节再解析。

```
configure_blockdev(&bdo_queue, machine_class, snapshot);
```

## 5.初始化计算虚拟化的加速模式

接下来初始化的是计算虚拟化的加速模式，也即要不要使用KVM。根据参数中的配置是启用KVM。这里调用的是configure\_accelerator。

```
configure_accelerator(current_machine, argv[0]);

void configure_accelerator(MachineState *ms, const char *progname)
{
    const char *accel;
    char **accel_list, **tmp;
    int ret;
    bool accel_initialised = false;
    bool init_failed = false;
    AccelClass *acc = NULL;

    accel = qemu_opt_get(qemu_get_machine_opts(), "accel");
    accel = "kvm";
    accel_list = g_strsplit(accel, ":", 0);

    for (tmp = accel_list; !accel_initialised && tmp && *tmp; tmp++) {
        acc = accel_find(*tmp);
        ret = accel_init_machine(acc, ms);
    }
}

static AccelClass *accel_find(const char *opt_name)
{
    char *class_name = g_strdup_printf(ACCEL_CLASS_NAME("%s"), opt_name);
    AccelClass *ac = ACCEL_CLASS(object_class_by_name(class_name));
    g_free(class_name);
    return ac;
}

static int accel_init_machine(AccelClass *acc, MachineState *ms)
{
    ObjectClass *oc = OBJECT_CLASS(acc);
    const char *cname = object_class_get_name(oc);
    AccelState *accel = ACCEL(object_new(cname));
    int ret;
    ms->accelerator = accel;
    *(acc->allowed) = true;
    ret = acc->init_machine(ms);
    return ret;
}
```

在configure\_accelerator中，我们看命令行参数里面的accel，发现是kvm，则调用accel\_find根据名字，得到相应的纸面上的class，并初始化为Class类。

MachineClass是计算机体系结构的Class类，同理，AccelClass就是加速器的Class类，然后调用accel\_init\_machine，通过object\_new，将AccelClass这个Class类实例化为AccelState，类似对于体系结构的实例是MachineState。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/58/9f/abb7bfe3.jpg" width="30px"><span>小龙的城堡</span> 👍（5） 💬（1）<div>深入内核以后，发现一切都是那么简洁，美妙？</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/04/2b/68d6ac0d.jpg" width="30px"><span>whiledoing</span> 👍（4） 💬（1）<div>老师，想问一下：在虚拟机中创建的线程，是如何进行调度的？又是如何映射到vCPU执行的呢？</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（4） 💬（1）<div>老师，那在虚拟机里面创建的多个核其实是假的是码？即使创建4个核的虚拟机，那么对应到kvm里面其实也是一个线程，也就是从虚拟机os这个层面它是无法真正利用多核的。其实它虚拟机os利用多核也没有意义。只要保证宿主os能正常利用多核就足够了，不知道这样理解是否正确？</div>2019-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d0/d6/f335954b.jpg" width="30px"><span>一笔一画</span> 👍（1） 💬（1）<div>.unlocked_ioctl = kvm_dev_ioctl,
    .compat_ioctl   = kvm_dev_ioctl,
请问下这两个ioctl有什么区别？在什么时候会调到</div>2019-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/c9/d3439ca4.jpg" width="30px"><span>why</span> 👍（7） 💬（0）<div>CPU 虚拟化

初始化表示体系结构的 MachineClass 之后, qemu main 函数将继续初始化块设备, 初始化 KVM, 初始化网络设备以及 CPU 和 内存的虚拟化.

初始化 KVM

以类似的方式创建 AccelClass 和 AccelState. 接着调用 AccelState 中的 kvm_init 继续初始化.

打开 &#47;dev&#47;kvm 字符设备文件以调用 KVM 的接口. 通过 ioctl 系统调用进入内核态.

在内核态中, 调用 kvm_dev_ioctl_create_vm 创建虚拟机. 

先创建 struct kvm 表示虚拟机, 其中存储 vcpu, mm_struct 等信息. 

再创建 fd, file_operations 设为 kvm_vm_fops

完成 kvm 内核数据结构的创建

CPU 虚拟化

调用 MachineClass 的 init 函数. 里面调用 pc_cpus_init 和 pc_memory_init 分别进行 vcpu 和内存的虚拟化.

从 qemu 参数解析得到 CPU 类型, 得到对应虚拟化 CPU 的定义. 调用定义中的初始化函数, 会设置 realize 函数 x86_cpu_realizefn, 在 x86_cpu_realizefn 会为一个 vcpu 创建一个线程. 该线程执行 qemu_kvm_cpu_thread_fn 函数. 

qemu_kvm_cpu_thread_fn 先初始化 vcpu, 创建一个 struct file, file_operation 指向 kvm_vcpu_fops. 然后在 vmx_create_cpu 创建标识 vcpu 的结构 vcpu_vmx. vcpu_vmx 包含 guest_msrs, loaded_vmcs 等.  vmcs 存储 vcpu 状态, 物理 cpu 状态等信息. 对 vmcs 有两个操作 VM_Entry 进入 guest 状态, vm_exit 进入宿主机状态.

qemu_kvm_cpu_thread_fn 接着执行无限循环调用 kvm_cpu_exec. 在 kvm_cpu_exec 进入 vm_entry, 执行 kvm_vcpu_ioctl(KVM_RUN) , 进行无限循环进入 guest 运行或处理信号. 进入 guest 执行的步骤为 save host reg -&gt; load guest reg -&gt; 进入&#47;恢复 guest 模式运行, 退出时 save guest reg -&gt; load host reg. </div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/64/37/3446d585.jpg" width="30px"><span>陈 皮。</span> 👍（1） 💬（0）<div>老师，请问是不是虚拟机的CPU本质就是一个线程，物理机的CPU调度到这个线程就等于调度到对应的VCPU？</div>2019-09-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/uG2kliaKAroGkNaXSwFNEmVz8xM6srw7OEHBMSBbPibuXQMctibLyuQEpRVmOth8sdojb3u5VUEjWm2D2lzRGuMDA/132" width="30px"><span>Geek_ae11ce</span> 👍（0） 💬（0）<div>讲这一块，在函数中跳来跳去的时候最好把代码再贴一下，交代两句。否则很容易衔接不上。</div>2024-07-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/uG2kliaKAroGkNaXSwFNEmVz8xM6srw7OEHBMSBbPibuXQMctibLyuQEpRVmOth8sdojb3u5VUEjWm2D2lzRGuMDA/132" width="30px"><span>Geek_ae11ce</span> 👍（0） 💬（0）<div>切换到kvm_init_vcpu那段，最好能再贴函数一下代码。上下翻来翻去特别费劲且不易于理解。</div>2023-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/97/7d/791d0f5e.jpg" width="30px"><span>蚂蚁吃大象</span> 👍（0） 💬（0）<div>超哥，请问openvswitch结合dpdk跑在宿主机上时，qemu~kvm的虚拟机使用virtio虚拟网卡支持对称rss？想跑fstack程序。</div>2020-10-25</li><br/>
</ul>