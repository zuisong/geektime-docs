你好，我是于航。

在这门课的第三个模块“C 工程实战篇”中，我带你学习了在大型工程实战中应用 C 语言时需要掌握的很多必备技巧。而这次的答疑加餐，我从这个模块的课后思考题中精选了同学们讨论比较多，也比较有代表性的三个问题，来对它们进行详细分析。接下来，就请跟随我的脚步，一起来看看吧。

## **问题一**

我在 [14 讲](https://time.geekbang.org/column/article/478213) 的“使用条件变量”一节中为你留下了这样一个问题：

在下面的代码中，为什么我们要在 while 语句，而不是 if 语句中使用 cnd\_wait 呢？

```c++
// ...
while (done == 0) { 
  cnd_wait(&cond, &mutex);
}
// ...
```

对于这个问题，评论区的一些同学给出了不错的回答。比如 @liu\_liu 同学就指出了其中的一个原因：

> 当阻塞的线程被重新调度运行时，done 的值可能被改变了，不是预期值。

还有 @ZR2021 同学也提到了与此相关的另一个重要因素：

> 使用 while 是防止广播通知方式的虚假唤醒，需要用户进一步判断。

这里，我就在同学们的回答基础上，对这个问题做一个总结。

首先需要知道的是，使用 while 或 if 语句的主要目的，在于判断线程是否满足“可以进入阻塞状态”的基本条件。比如，在上述代码中，当全局变量 done 的值为 0 时，表明当前线程需要优先等待其他线程完成某项任务后，才能够继续执行。但在现实情况中，“等待线程”的执行恢复往往会在各种非正常情况下发生。通常来说，这些情况可以被总结为三类。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/4a/eb91b1f8.jpg" width="30px"><span>ALPHA</span> 👍（3） 💬（1）<div>老师好，问一哈c语言有类似于协程的特性吗</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a9/12/e041e7b2.jpg" width="30px"><span>Ping</span> 👍（2） 💬（1）<div>多谢老师</div>2022-02-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKwGurTWOiaZ2O2oCdxK9kbF4PcwGg0ALqsWhNq87hWvwPy8ZU9cxRzmcGOgdIeJkTOoKfbxgEKqrg/132" width="30px"><span>ZR2021</span> 👍（0） 💬（0）<div>666</div>2022-02-21</li><br/>
</ul>