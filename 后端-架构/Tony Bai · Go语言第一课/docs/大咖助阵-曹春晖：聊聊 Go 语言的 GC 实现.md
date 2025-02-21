> 作者注：本文只作了解，不建议作为面试题考察。

你好，我是曹春晖，是《Go 语言高级编程》的作者之一。

今天我想跟你分享一下 Go 语言内存方面的话题，聊一聊Go语言中的垃圾回收（GC）机制的实现，希望你能从中有所收获。

## 武林秘籍救不了段错误

![图片](https://static001.geekbang.org/resource/image/5f/c8/5f4574358998f372abcab606df8803c8.png?wh=500x300 "包教包会包分配")

在各种流传甚广的 C 语言葵花宝典里，一般都有这么一条神秘的规则，不能返回局部变量：

```plain
int * func(void) {
    int num = 1234;
    /* ... */
    return &num;
}
```

duang!

当函数返回后，函数的栈帧（stack frame）就会被销毁，引用了被销毁位置的内存，轻则数据错乱，重则 segmentation fault。

可以说，即使经过了八十一难，终于成为了 C 语言绝世高手，我们还是逃不过复杂的堆上对象引用关系导致的 dangling pointer：

![图片](https://static001.geekbang.org/resource/image/8c/73/8c834c68ab195cc01200a84fc942bc73.gif?wh=984x616 "当 B 被 free 掉之后")

你看，在这张图中，当 B 被 free 掉之后，应用程序依然可能会使用指向 B 的指针，这就是比较典型的 dangling pointer 问题，堆上的对象依赖关系可能会非常复杂。所以，我们要正确地写出 free 逻辑，还得先把对象图给画出来。

不过，依赖人去处理复杂的对象内存管理的问题是不科学、不合理的。C 和 C++ 程序员已经被折磨了数十年，我们不应该再重蹈覆辙了，于是，后来的很多编程语言就用上垃圾回收（GC）机制。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/a8/b0/6f87ab08.jpg" width="30px"><span>Tony Bai</span> 👍（9） 💬（0）<div>曹老师把GC原理讲得好通透！👍 </div>2022-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/50/82/32a2bf86.jpg" width="30px"><span>叶剑峰</span> 👍（2） 💬（0）<div>膜拜曹大</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/92/b609f7e3.jpg" width="30px"><span>骨汤鸡蛋面</span> 👍（1） 💬（4）<div>大佬，go 在变量赋值时调用 write barrier，可以多补充些细节嘛？</div>2022-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/1e/0a/159b2129.jpg" width="30px"><span>lufofire</span> 👍（0） 💬（0）<div>牛逼</div>2024-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/67/30/57856788.jpg" width="30px"><span>Niku</span> 👍（0） 💬（0）<div>曹神TQL</div>2023-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/8c/f9/e1dab0ca.jpg" width="30px"><span>怎么睡才能做这种梦</span> 👍（0） 💬（0）<div>看不懂噢</div>2023-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/96/dd/1620a744.jpg" width="30px"><span>simple_孙</span> 👍（0） 💬（1）<div>PauseNs数组中的数字是啥意思呢</div>2022-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/16/3e/5965e58b.jpg" width="30px"><span>风</span> 👍（0） 💬（0）<div>曹大yyds</div>2022-02-26</li><br/>
</ul>