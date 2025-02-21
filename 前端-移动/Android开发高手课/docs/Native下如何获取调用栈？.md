你好，我是simsun，曾在微信从事Android开发，也是开源爱好者、Rust语言“铁粉”。应绍文邀请，很高兴可以在“高手课”里和你分享一些编译方面的底层知识。

当我们在调试Native崩溃或者在做profiling的时候是十分依赖backtrace的，高质量的backtrace可以大大减少我们修复崩溃的时间。但你是否了解系统是如何生成backtrace的呢？今天我们就来探索一下backtrace背后的故事。

下面是一个常见的Native崩溃。通常崩溃本身并没有任何backtrace信息，可以直接获得的就是当前寄存器的值，但显然backtrace才是能够帮助我们修复Bug的关键。

```
pid: 4637, tid: 4637, name: crasher  >>> crasher <<<
signal 6 (SIGABRT), code -6 (SI_TKILL), fault addr --------
Abort message: 'some_file.c:123: some_function: assertion "false" failed'
    r0  00000000  r1  0000121d  r2  00000006  r3  00000008
    r4  0000121d  r5  0000121d  r6  ffb44a1c  r7  0000010c
    r8  00000000  r9  00000000  r10 00000000  r11 00000000
    ip  ffb44c20  sp  ffb44a08  lr  eace2b0b  pc  eace2b16
backtrace:
    #00 pc 0001cb16  /system/lib/libc.so (abort+57)
    #01 pc 0001cd8f  /system/lib/libc.so (__assert2+22)
    #02 pc 00001531  /system/bin/crasher (do_action+764)
    #03 pc 00002301  /system/bin/crasher (main+68)
    #04 pc 0008a809  /system/lib/libc.so (__libc_init+48)
    #05 pc 00001097  /system/bin/crasher (_start_main+38)
```

在阅读后面的内容之前，你可以先给自己2分钟时间，思考一下系统是如何生成backtrace的呢？我们通常把生成backtrace的过程叫作unwind，unwind看似和我们平时开发并没有什么关系，但其实很多功能都是依赖unwind的。举个例子，比如你要绘制火焰图或者是在崩溃发生时得到backtrace，都需要依赖unwind。

## 书本中的unwind

**1. 函数调用过程**

如果你在大学时期修过汇编原理这门课程，相信你会对下面的内容还有印象。下图就是一个非常标准的函数调用的过程。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/jfwxv44zewuyr7WEsOvTowFicSIFBwHJnUQzibhUuYHSIibcAAicUzehWia7y5uUiaEG9A1DgltOKsL6IMwSZIzRCgTQ/132" width="30px"><span>Geek_Yasin28</span> 👍（3） 💬（1）<div>请问这里的方法可以用于获取非崩溃情况下其他线程的native堆栈吗？
对于卡顿的分析，除了Simpleperf ，如果想或许线上的native执行情况，是否只能对指定的函数进行GOTHOOK?</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/82/6e/f552d036.jpg" width="30px"><span>山鬼</span> 👍（3） 💬（1）<div>春节依然继续学习。之前老师讲崩溃优化的时候尝试对native的崩溃进行了捕获，使用的系统提供的uwind工具，当时觉得比较难得在于打印出对应的java堆栈。现在对uwind的原理又了解了一下，但感觉这篇教程的信息量少了些。</div>2019-02-03</li><br/>
</ul>