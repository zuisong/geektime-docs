你好，我是唯鹿。

接着上篇[练习手记](https://time.geekbang.org/column/article/83742)，今天练习6～8、12、17、19这六期内容（主要针对有课后Sample练习的），相比1～5期轻松了很多。

[**Chapter06**](https://github.com/AndroidAdvanceWithGeektime/Chapter06)

> 该项目展示了使用PLT Hook技术来获取Atrace的日志，可以学习到systrace的一些底层机制。

没有什么问题，项目直接可以运行起来。运行项目后点击开启Atrace日志，然后就可以在Logcat日志中查看到捕获的日志，如下：

```
11:40:07.031 8537-8552/com.dodola.atrace I/HOOOOOOOOK: ========= install systrace hoook =========
11:40:07.034 8537-8537/com.dodola.atrace I/HOOOOOOOOK: ========= B|8537|Record View#draw()
11:40:07.034 8537-8552/com.dodola.atrace I/HOOOOOOOOK: ========= B|8537|DrawFrame
11:40:07.035 8537-8552/com.dodola.atrace I/HOOOOOOOOK: ========= B|8537|syncFrameState
    ========= B|8537|prepareTree
    ========= E
    ========= E
    ========= B|8537|eglBeginFrame
    ========= E
    ========= B|8537|computeOrdering
    ========= E
    ========= B|8537|flush drawing commands
    ========= E
11:40:07.036 8537-8552/com.dodola.atrace I/HOOOOOOOOK: ========= B|8537|eglSwapBuffersWithDamageKHR
    ========= B|8537|setSurfaceDamage
    ========= E
11:40:07.042 8537-8552/com.dodola.atrace I/HOOOOOOOOK: ========= B|8537|queueBuffer
    ========= E
11:40:07.043 8537-8552/com.dodola.atrace I/HOOOOOOOOK: ========= B|8537|dequeueBuffer
    ========= E
    ========= E
    ========= E
```

通过B|事件和E|事件是成对出现的，这样就可以计算出应用执行每个事件使用的时间。那么上面的Log中View的draw()方法显示使用了9ms。

这里实现方法是使用了[Profilo](https://github.com/facebookincubator/profilo)的PLT Hook来hook libc.so的`write`与`__write_chk`方法。libc是C的基础库函数，为什么要hook这些方法，需要我们补充C、Linux相关知识。

同理[Chapter06-plus](https://github.com/AndroidAdvanceWithGeektime/Chapter06-plus)展示了如何使用 PLT Hook技术来获取线程创建的堆栈，README有详细的实现步骤介绍，我就不赘述了。

[**Chapter07**](https://github.com/AndroidAdvanceWithGeektime/Chapter07)

> 这个Sample是学习如何给代码加入Trace Tag，大家可以将这个代码运用到自己的项目中，然后利用systrace查看结果。这就是所谓的systrace + 函数插桩。