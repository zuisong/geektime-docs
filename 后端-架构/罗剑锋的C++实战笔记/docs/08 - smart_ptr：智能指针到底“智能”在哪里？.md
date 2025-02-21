你好，我是Chrono。

上节课在讲const的时候，说到const可以修饰指针，不过今天我要告诉你：请忘记这种用法，在现代C++中，绝对不要再使用“裸指针（naked pointer）”了，而是应该使用“智能指针（smart pointer）”。

你肯定或多或少听说过、用过智能指针，也可能看过实现源码，那么，你心里有没有一种疑惑，智能指针到底“智能”在哪里？难道它就是解决一切问题的“灵丹妙药”吗？

学完了今天的这节课，我想你就会有个明确的答案了。

## 什么是智能指针？

所谓的“智能指针”，当然是相对于“不智能指针”，也就是“裸指针”而言的。

所以，我们就先来看看裸指针，它有时候也被称为原始指针，或者直接简称为指针。

指针是源自C语言的概念，本质上是一个内存地址索引，代表了一小片内存区域（也可能会很大），能够直接读写内存。

因为它完全映射了计算机硬件，所以操作效率高，是C/C++高效的根源。当然，这也是引起无数麻烦的根源。访问无效数据、指针越界，或者内存分配后没有及时释放，就会导致运行错误、内存泄漏、资源丢失等一系列严重的问题。

其他的编程语言，比如Java、Go就没有这方面的顾虑，因为它们内置了一个“垃圾回收”机制，会检测不再使用的内存，自动释放资源，让程序员不必为此费心。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/19/17245c59.jpg" width="30px"><span>Eglinux</span> 👍（53） 💬（3）<div>C++ 这么小众吗？讲得这么好，如果写成书，完全可以看成另外一本 effective C++ 了，为什么才 3000 多订阅人数？</div>2020-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9c/62/f625b2bb.jpg" width="30px"><span>酸葡萄</span> 👍（30） 💬（1）<div>老师，您好，什么时候用weak_ptr,什么时候用shared_ptr？</div>2020-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b4/63/59bb487d.jpg" width="30px"><span>eletarior</span> 👍（20） 💬（2）<div>默认用的比较多的是unique_ptr ，相反的shared_ptr倒是用的不多，因为担心文中提到的循环引用，资源消耗，线程安全等问题。大部分时候，unique_ptr是能完全取代裸指针的。如果是存粹的标准C++代码，使用智能指针确实很舒服，把它们当成一个普通的类型看就行了。但是，同时，作为C++程序员我们又不得不和裸指针打交道，不论是Linux还是Windows，我们不可避免的要使用它们的系统api，于是就不得不使用get将智能指针转成裸指针。而这条指针所指向的内存在系统api里也许是不应该随意析构掉的，因为在系统内部可能还得继续使用这段内存，那么在这种场景下，智能指针的特性就可能帮倒忙，难受了😫。针对这种问题，我想到的就是延长这个智能指针的生命周期，或者直接使用release将裸指针释放出来，可是这样一来，delete就少不了要使用了😔
</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/47/b0/f44aef75.jpg" width="30px"><span>颓废人才</span> 👍（13） 💬（2）<div>罗老师您好，还有一个问题，常用的C++ reference 我看到一个 cplusplus.com和cppreference.com, 但是网上有一些不好评价，觉得这两个网站都有问题，罗老师这边一般参考的哪些文档网站，可以推荐下么。非常感谢。</div>2020-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/df/77acb793.jpg" width="30px"><span>禾桃</span> 👍（11） 💬（1）<div>“因为 shared_ptr 具有完整的“值语义”（即可以拷贝赋值）”

一直都觉得值语义这三个字比较难理解。想请教下这个概念到底是想说明什么问题，这个“值”该怎么理解？</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6c/83/48e528cb.jpg" width="30px"><span>Luke</span> 👍（6） 💬（1）<div>使用智能指针可以自动析构“资源”，隐含了指针管理的细节，从而提高了代码的安全性和易用性，但是这是否同时意味着效率下降？在极致追求执行速度的系统中，是否需要避免使用智能指针，依赖程序员自己管理裸指针的new和delete呢？</div>2020-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/28/f6/7fa61d68.jpg" width="30px"><span>郭郭</span> 👍（6） 💬（1）<div>老师，关于unique_ptr，如auto ptr = ptr1，那ptr1就应该被置空啦。不需要显示的调用std::move</div>2020-05-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLZqsT4YGrnaBtCgetwQiaK8nt2qXr5z56a9j2ricUiadibsPNqYqiawaygHicq3frt1jPVaoT78gh2f7Uw/132" width="30px"><span>Geek_王</span> 👍（5） 💬（3）<div>罗老师能把文中提到的血泪教训详细说一下吗？什么问题？怎么解决的？</div>2020-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/67/05/a0315f44.jpg" width="30px"><span>The Answer</span> 👍（5） 💬（4）<div>老师，shared_ptr 本身是线程安全的，但是如何理解它所管理的对象不是线程安全的呢？</div>2020-07-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/E73UicmpgFiaZW4SOTGaxoIk9PWue54neNcfsicz7HOxJUucep4jSMyeMMruLNcIlxsE330qOFMacaEQ9Vz4zXJyg/132" width="30px"><span>Mari</span> 👍（4） 💬（1）<div>罗老师，问个问题：shared_ptr作为函数参数时，什么情况传值，什么情况传引用？</div>2022-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fb/61/c84a45be.jpg" width="30px"><span>Geek_3nl94i</span> 👍（4） 💬（3）<div>讲的很好很实用，不过只有30讲，有点少呀</div>2020-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/99/27/15d2c4f5.jpg" width="30px"><span>Zivon</span> 👍（4） 💬（1）<div>罗老师，今天尝试使用智能指针改写双向链表的时候感觉实现很麻烦啊，请问在实现这种基本数据结构的时候需要使用智能指针吗</div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/47/b0/f44aef75.jpg" width="30px"><span>颓废人才</span> 👍（3） 💬（1）<div>老师您好，请问智能指针的释放和内存管理的结合怎么使用例如以前我们写的智能指针的简单用法：
Template&lt;class T&gt;
class AutoPtr
{
private:
    T* m_ptr
public:
    AutoPtr(T* ptr):m_ptr(ptr)   {}
    ~AutoPtr()                          {if(ptr) ptr-&gt;release()}          &#47;&#47;析构函数里去回收对象内存
}
那现在使用stl的智能指针能否做到这步。
还有能否介绍下实际项目开发中的一些使用场景和使用小技巧。</div>2020-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/99/27/15d2c4f5.jpg" width="30px"><span>Zivon</span> 👍（3） 💬（1）<div>shared_ptr 与unique_ptr最大区别就在于前者可以多个指针共享一个对象或元素，而后者一块内存空间只能由唯一的一个指针持有。
使用堆内存新建对象均使用智能指针，就可以不用new&#47;delete</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/b3/7b/95adaf84.jpg" width="30px"><span>学习者</span> 👍（2） 💬（1）<div>打卡，感觉评论区也能学到很多，二刷的时候，要把评论区的内容好好整理一下。</div>2023-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/6c/43c82d43.jpg" width="30px"><span>不如不见</span> 👍（2） 💬（1）<div>罗老师，请教个问题。确实有时候在很长的链中很难发现shared_ptr的循环引用问题。那有没有什么好的办法（工具）知道自己发生了循环引用。或者一开始在设计的时候，从哪些方面可以考虑或者避免循环引用的问题。感谢。</div>2021-04-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJe0esddRVdG689MicU5zMibMtkyLpYkX4MtiamKP8eFf7KUoMlfU7ficrciakyVS06jHVdskYT67JKtdg/132" width="30px"><span>湖海散人</span> 👍（2） 💬（1）<div>老师，文中提到的右值，move，完美转发会有课程讲到吗</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/35/76/951b0daf.jpg" width="30px"><span>K. D.</span> 👍（2） 💬（1）<div>罗老师你好，有个问题请教一下：std::move是否也适用于shared_ptr，和=有区别吗？</div>2020-05-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIm5rlbJ4HdXLbxmflvW0FW4rTyLcDzHLGDJUJic9W3f1KibWY7mAj9dxUIEVlxDyjwRXEX54KXEn5g/132" width="30px"><span>sea520</span> 👍（2） 💬（2）<div>您好！为什么面试喜欢问cpp底层实现细节。比如说虚表实现，stl实现？有什么最大的价值？万一工作换新语言还要都弄的很清楚吗？那时间成本呢？</div>2020-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/7c/ef/013087c4.jpg" width="30px"><span>大白v5</span> 👍（1） 💬（1）<div>weak_ptr与shared_ptr配合着使用，用weak_ptr先确保shared_ptr是持有指针的，然后再放心使用</div>2022-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/b2/59/4ea0e511.jpg" width="30px"><span>e^(iα)=cosα+isinα⁵·⁰</span> 👍（1） 💬（1）<div>老师，您好，
如果指针是“独占”使用，就应该选择 unique_ptr；
“共享”使用，就应该选择 shared_ptr；
这里独占指的是在单一线程里使用，共享是指可能多个线程都会使用这个指针，是这个意思吗？
所以一个叫unique_pte，一个叫shared_ptr</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b3/17/9f6d67dc.jpg" width="30px"><span>超越杨超越</span> 👍（1） 💬（3）<div>请问老师，如果直接在栈上分配对象，跟unique ptr相比，我应该倾向于哪种呢</div>2021-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8b/19/a15d060d.jpg" width="30px"><span>silverhawk</span> 👍（1） 💬（1）<div>说实话，unique_ptr比起裸指针革命性进步，但是shared_ptr 有点over engineering ，感觉有些时候用起来会很坑。不知道你怎么看</div>2020-05-31</li><br/><li><img src="" width="30px"><span>java2c++</span> 👍（1） 💬（1）<div>老师文稿中的这段代码我改了下如果封装到一个函数里，可以被多线程并发调用吗？unique_ptr尽管有move可以进行转移，但是同一时刻ptr1是不是只允许转移到一个ptr2，而之前转移成功的后续逻辑还没有执行完


void methodtest（uniqptr_ptr ptr1）｛
auto ptr2 = std::move(ptr1);         &#47;&#47; 使用move()转移所有权
assert(!ptr1 &amp;&amp; ptr2);               &#47;&#47; ptr1变成了空指针

&#47;&#47;use ptr2 dosomething……
｝</div>2020-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/c2/b7/f7facaae.jpg" width="30px"><span>李锐</span> 👍（1） 💬（2）<div>罗老师，您好，我的工作场景中经常需要new一个数组来缓存从下位机采集到的数据，比如new [100]来缓存100帧图像数据，请问下，c++11中智能指针如何去管理new数组，谢谢</div>2020-05-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIicr82CnrdEjibibAvyeKRQHszSzIAqoCWxN0kqC442XcjEae6S9j6NDtKLpg4Da4CUQQeUFUicWqiaDw/132" width="30px"><span>有学识的兔子</span> 👍（1） 💬（1）<div>1. 我的理解是Unique pointer 是对象而不是指针，但重载了*和箭头，离开了对象的作用域就会被析构，所管理的资源在析构执行过程中被释放；那move操作是不是对对象进行拷贝了才得以传递？
shared_ptr 貌似也是对象，重点在于引用计数，对赋值拷贝计数+1，对于执行析构时计数-1，同时判断计数是否0，被管理的资源是否需要释放；
没明白为什么weak pointer能避免循环引用，是因为locker，避免错误计数？
</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/ce/fd45714f.jpg" width="30px"><span>bearlu</span> 👍（1） 💬（1）<div> shared_ptr 的销毁动作，这段说世界停止，是为什么停止，做了什么操作导致世界停止，智能指针不是线程安全？</div>2020-05-23</li><br/><li><img src="" width="30px"><span>Geek_6a1d96</span> 👍（0） 💬（2）<div>对于只能指针shared_ptr的释放其实还有一点需要注意的，对于复杂点的释放最好加入释放函数。如下：shared_ptr&lt;int&gt; tmp(new int(10),[](int* p){delete[] p;p＝nullptr;});这样能完全避免内存泄露。</div>2023-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/56/9d/4b2a7d29.jpg" width="30px"><span>ryanxw</span> 👍（0） 💬（1）<div>请教一下老师make_shared，make_unique这种工厂函数除了能防止操作空指针的失误，还有哪些方面要比手动构造好呢？能详细说一下吗</div>2022-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/7f/6b/83236a96.jpg" width="30px"><span>娃哈哈</span> 👍（0） 💬（1）<div>老师讲的很好，但是让我用，我还是用不出来，难受呀。。</div>2022-04-26</li><br/>
</ul>