你好，我是吴咏炜。

有一个我之前没讲、但挺有意思的话题是 `new` 和 `delete` 行为的定制。这件事情我很久很久以前就做过 \[1]，没往专栏里写的最主要原因是，这实际是 C++98 就有的高级技巧，不属于现代 C++。不过，在目前续写的内容里，我就不再拘泥必须新了，既然这是 C++ 里现在仍然需要的技巧，那就还是介绍一下。何况，这部分在现代 C++ 里还是有点新内容的。

## 最常用的分配和释放函数

在[第 1 讲](https://time.geekbang.org/column/article/169225)，我提到过，当我们使用 `new` 和 `delete` 来创建和销毁对象时，实际发生的事情还是比较多的（如果忘了的话，可以去复习一下）。其中，分配内存和释放内存的操作是通过 `operator new` 和 `operator delete` 函数完成的。在最简单的 `new` 和 `delete` 形式里，我们使用的是以下两个函数：

```cpp
void* operator new(size_t size);
void operator delete(void* ptr) noexcept;
```

`operator new` 和 `operator delete` 函数通常就被称为分配函数（allocation function）和释放函数（deallocation function）。

需要注意 `operator new` 是可能抛出异常的，而 `operator delete` 则不会抛出异常，被标为 noexcept。这和我们通常不允许在析构函数中抛出异常是完全一致的。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/21/7e/fb725950.jpg" width="30px"><span>罗 乾 林</span> 👍（11） 💬（5）<div>前一个相同，后一个不同（除开POD）。数组会在头部存放对象的大小，这样才能依次找到数组中的每个对象地址，调用析构函数</div>2022-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/27/a6/32e9479b.jpg" width="30px"><span>tang_ming_wu</span> 👍（1） 💬（1）<div>new Obj返回的是调用构造函数初始化完成的对象指针；
operator new 返回的只是一块足够容纳这个对象大小的空白的内存空间。
不知道我的理解准不准确。</div>2022-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ca/e3/447aff89.jpg" width="30px"><span>记事本</span> 👍（0） 💬（1）<div>看不懂 怎么整？</div>2022-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/df/77acb793.jpg" width="30px"><span>禾桃</span> 👍（0） 💬（1）<div>麻烦问下，

new Obj 对应的表达式是 auto ptr = new Obj;
operator new对应的表达式是？</div>2022-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/f4/a1/51e99a88.jpg" width="30px"><span>高伸</span> 👍（0） 💬（1）<div>吴老师有个问题想请教下，在查阅gcc4.9中stl源码时，发现allocator申请内存时直接调用::operator new，为什么没有如以前一样采用二级缓存pool_allocator的方式呢</div>2022-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/33/e7/145be2f9.jpg" width="30px"><span>怪兽</span> 👍（0） 💬（1）<div>在&quot;不分配内存的布置分配和释放函数&quot;小节里，老师有提到&quot;另外注意，跟大部分其他分配函数和释放函数不同，这个函数是不能被用户提供的版本替换的&quot;。这里说的&quot;这个函数&quot;是指这两个函数吗？
inline void* operator new(size_t, void* ptr) noexcept
{ return ptr; }

inline void operator delete(void*, void*) noexcept
{}</div>2022-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/49/4a488f4c.jpg" width="30px"><span>农民园丁</span> 👍（0） 💬（1）<div>居然还有31，太值了！</div>2022-02-24</li><br/>
</ul>