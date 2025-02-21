你好，我是戴铭。

在 iOS 开发中，我们可以使用 Runtime 接口动态地调用 Objective-C 方法，但是却无法动态调用 C 的函数。那么，我们怎么才能动态地调用 C 语言函数呢？

C 语言编译后，在可执行文件里会有原函数名信息，我们可以通过函数名字符串来找到函数的地址。现在，我们只要能够通过函数名找到函数地址，就能够实现动态地去调用C 语言函数。

而在动态链接器中，有一个接口 dlsym() 可以通过函数名字符串拿到函数地址，如果所有 C 函数的参数类型和数量都一样，而且返回类型也一样，那么我们使用 dlsym() 就能实现动态地调用 C 函数。

但是，在实际项目中，函数的参数定义不可能都一样，返回类型也不会都是 void 或者 int类型。所以， dlsym()这条路走不通。那么，还有什么办法可以实现动态地调用 C 函数呢？

## 如何动态地调用C函数？

要想动态地调用 C 函数，你需要先了解函数底层是怎么调用的。

高级编程语言的函数在调用时，需要约定好参数的传递顺序、传递方式，栈维护的方式，名字修饰。这种函数调用者和被调用者对函数如何调用的约定，就叫作调用惯例（Calling Convention）。高级语言编译时，会生成遵循调用惯例的代码。

不同 CPU 架构的调用惯例不一样，比如64位机器的寄存器多些、传递参数快些，所以参数传递会优先采用寄存器传递，当参数数量超出寄存器数量后才会使用栈传递。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epzwbJGbUmgEC77J6QY6A5pLPdPbw7sqk4DcsHK8qPw7OiaiaMD7pjzb8uHlkY5uLZRibWVvPDDAgM5A/132" width="30px"><span>mersa</span> 👍（2） 💬（1）<div>这个库可以用在线上审核么</div>2019-05-30</li><br/><li><img src="" width="30px"><span>Alex</span> 👍（1） 💬（1）<div>能用libffi hook c函数嘛？</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/0b/4346a253.jpg" width="30px"><span>Ant</span> 👍（0） 💬（1）<div>为啥少了编译过程也能调用</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9e/28/d7ac85bd.jpg" width="30px"><span>幻想vs梦想</span> 👍（5） 💬（0）<div>首先,为啥要调用c函数,什么场景下我们需要去调用c函数,调用c函数有哪些好处或作用,有点不太懂.</div>2020-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e7/bb/18eb89fd.jpg" width="30px"><span>开发小能手</span> 👍（3） 💬（1）<div>&#47;&#47; 有一个问题想要请教老师, 可能与当前文章没有太大的关联.
&#47;&#47; 在女神(念茜)的博客(iOS安全攻防（二十二）：static和被裁的符号表)中提到
&#47;**
 如果函数属性为 static ，那么编译时该函数符号就会被解析为local符号。
 在发布release程序时（用Xcode打包编译二进制）默认会strip裁掉这些函数符号，无疑给逆向者加大了工作难度。
 *&#47;

&#47;&#47; 但是根据我的测试发现, 实际上并不是女神说的那样.在 iOS 项目中, 一个 C 函数即使是不添加 static 关键字, 在 release 的时候, 也没有具体的符号表.
&#47;&#47; 这是因为现在的 Xcode （编译器）做了优化了么?

@implementation CoderPerson


&#47;&#47; 发现, 即使是不加 static, 在 release 的时候这个函数符号也没有
&#47;&#47;  static int coder_func() {
int coder_func() {
    int a = 10;
    int b = 20;
    int c = a+b;
    return c;
}

- (void)coder_method {
    int d = coder_func();
    NSLog(@&quot;%d&quot;, d);
}

@end


一摸一样的代码、如果放到终端项目中的话，确实是要加上static才会在release的时候被裁减。 感觉是项目的参数配置导致的、但是一直没有找到。


</div>2019-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/dc/d9/129f569f.jpg" width="30px"><span>forping</span> 👍（1） 💬（0）<div>struct BlockDescriptor
{
    unsigned long reserved;
    unsigned long size;
    void *rest[1];
};

struct Block
{
    void *isa;
    int flags;
    int reserved;
    void *invoke;
    struct BlockDescriptor *descriptor;
};

static void *BlockImpl(id block)
{
    return ((__bridge struct Block *)block)-&gt;invoke;
}

void testFFIBlockCall(){
    
    int(^block)(void) = ^{
        NSLog(@&quot;1&quot;);
        return 2;
    };
    
    
    ffi_cif cif;
    ffi_type *argumentTypes[] = {};
    
    ffi_prep_cif(&amp;cif, FFI_DEFAULT_ABI, 0, &amp;ffi_type_sint32, argumentTypes);
    
    void *arguments[] = {};
    
    IMP imp = BlockImpl(block);
    
    int retValue;
    
    ffi_call(&amp;cif, imp, &amp;retValue, arguments);
    NSLog(@&quot;ffi_call: %d&quot;, retValue);
    
}</div>2021-01-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3B5MoC4DfBt00nnVshEBFHHkNVgbcBrXsd3SxFicdN3XX5ILOe7GJxKvtJKCY53xNCuxSV8ABxNulbhkibm1lXIw/132" width="30px"><span>林峰峰</span> 👍（1） 💬（0）<div>想问下实际应用中，这种动态调用用到了那些方面？</div>2019-06-17</li><br/><li><img src="" width="30px"><span>Space</span> 👍（0） 💬（0）<div>如何hook C函数？没头绪~</div>2021-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/32/f1/54575096.jpg" width="30px"><span>Master</span> 👍（0） 💬（0）<div>没太看明白，好像被调用的函数都是被编译过的啊？</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2f/99/918e9b2a.jpg" width="30px"><span>三刀流剑客</span> 👍（0） 💬（0）<div>可以用libffi动态替换系统+load方法吗</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/35/19/4f9dc4b5.jpg" width="30px"><span>帅气潇洒的豆子</span> 👍（0） 💬（1）<div>没有汇编基础，看起来好痛苦。</div>2019-05-30</li><br/>
</ul>