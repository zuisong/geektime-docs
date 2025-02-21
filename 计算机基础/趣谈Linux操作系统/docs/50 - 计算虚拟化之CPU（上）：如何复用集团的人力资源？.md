上一节，我们讲了一下虚拟化的基本原理，以及qemu、kvm之间的关系。这一节，我们就来看一下，用户态的qemu和内核态的kvm如何一起协作，来创建虚拟机，实现CPU和内存虚拟化。

这里是上一节我们讲的qemu启动时候的命令。

```
qemu-system-x86_64 -enable-kvm -name ubuntutest  -m 2048 -hda ubuntutest.qcow2 -vnc :19 -net nic,model=virtio -nettap,ifname=tap0,script=no,downscript=no
```

接下来，我们在[这里下载](https://www.qemu.org/)qemu的代码。qemu的main函数在vl.c下面。这是一个非常非常长的函数，我们来慢慢地解析它。

## 1.初始化所有的Module

第一步，初始化所有的Module，调用下面的函数。

```
module_call_init(MODULE_INIT_QOM);
```

上一节我们讲过，qemu作为中间人其实挺累的，对上面的虚拟机需要模拟各种各样的外部设备。当虚拟机真的要使用物理资源的时候，对下面的物理机上的资源要进行请求，所以它的工作模式有点儿类似操作系统对接驱动。驱动要符合一定的格式，才能算操作系统的一个模块。同理，qemu为了模拟各种各样的设备，也需要管理各种各样的模块，这些模块也需要符合一定的格式。

定义一个qemu模块会调用type\_init。例如，kvm的模块要在accel/kvm/kvm-all.c文件里面实现。在这个文件里面，有一行下面的代码：

```
type_init(kvm_type_init);

#define type_init(function) module_init(function, MODULE_INIT_QOM)

#define module_init(function, type)                                         \
static void __attribute__((constructor)) do_qemu_init_ ## function(void)    \
{                                                                           \
    register_module_init(function, type);                                   \
}

void register_module_init(void (*fn)(void), module_init_type type)
{
    ModuleEntry *e;
    ModuleTypeList *l;

    e = g_malloc0(sizeof(*e));
    e->init = fn;
    e->type = type;

    l = find_type(type);

    QTAILQ_INSERT_TAIL(l, e, node);
}
```

从代码里面的定义我们可以看出来，type\_init后面的参数是一个函数，调用type\_init就相当于调用module\_init，在这里函数就是kvm\_type\_init，类型就是MODULE\_INIT\_QOM。是不是感觉和驱动有点儿像？
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/f9/caf27bd3.jpg" width="30px"><span>大王叫我来巡山</span> 👍（27） 💬（1）<div>感觉设计这个软件的真厉害，怪不得我们自己做的业务系统自己都信不过，差距实在是太远，国内很多大公司在分享技术的时候也就是个PPT，根本不敢把代码放出来给大家看，也没有把实际用的效果展示给大家，只是给别人的感觉很牛逼而已。我感觉我从事这个工作这么久，真没遇到过这种大神</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/25/4b/4cbd001e.jpg" width="30px"><span>佳俊</span> 👍（8） 💬（1）<div>看了很久都没有搞明白一个type_init 宏定义出来的函数是怎么被调用的，直到发现在module_init 里面一个这个属性的定义__attribute__((constructor))，才明白是GNU C 里面的一个特性，在main函数调用前系统会自动先调用这个函数。</div>2020-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e3/ad/a47728fd.jpg" width="30px"><span>泡泡</span> 👍（1） 💬（2）<div>请问代码是用的哪个内核版本</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/c9/d3439ca4.jpg" width="30px"><span>why</span> 👍（12） 💬（0）<div>解析 qemu 的执行步骤

1. 初始化所有模块

模块的信息(包括名称, 模块类型初始化函数等), 存在 TypeInfo 中, 通过调用 type_init, 将这些信息统一以 ModelEntry 的格式存储到 ModelTypeList 中. 

module_call_init() 会调用 ModelTypeList 中所有模块的初始化函数,  从 ModelEntry 里存储的 TypeInfo 信息生成 TypeImpl(类似于 class 文件), 这个 TypeImpl 会存储到 qemu 的一个全局 hash 表中.  

2. 解析命令行参数

命令行参数比较多. 

其中 -machine 参数用于指定计算机体系结构. 另外 网卡&#47;硬盘的配置要分表从 Host&#47;Guest 较多进行设置.

3. 初始化 machine

会在 qemu 的全局 hash 表中注册对应计算机体系结构的 TypeImpl 信息. 然后会调用所有 TypeImpl 的初始化方法 class_init 生成对应的 Class. 最后会得到一个 MachineClass. 然后调用 TypeImple 中的 instance_init 方法生成 MachineClass 的一个实例. </div>2020-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/4d/97/1d99a0a3.jpg" width="30px"><span>柒城</span> 👍（3） 💬（0）<div>老师，之后会不会开个专门讲虚拟化的专栏啊？吧QEMU和KVM好好讲讲</div>2021-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/2c/f8451d77.jpg" width="30px"><span>石维康</span> 👍（3） 💬（0）<div>请问老师pc_machine_type_##suffix所对应的TypeImpl的instance_init是在哪初始化的？也就是从代码里如何体现从MachineClass生成MachineState？</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5e/aa/b29ee77d.jpg" width="30px"><span>RobinDevNotes</span> 👍（2） 💬（0）<div>期望老师出一个讲openstack的专栏</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5e/aa/b29ee77d.jpg" width="30px"><span>RobinDevNotes</span> 👍（1） 💬（0）<div>openstack是调用libvirt，libevirtd再调用kvm吗？</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b2/e0/bf56878a.jpg" width="30px"><span>kkxue</span> 👍（0） 💬（0）<div>nova通过libvirt驱动，将配置数据转化成XML格式的文件，用于创建虚拟机。</div>2022-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/90/8f/9c691a5f.jpg" width="30px"><span>奔跑的码仔</span> 👍（0） 💬（0）<div>请问，qemu使用的是哪个版本？</div>2019-10-23</li><br/>
</ul>