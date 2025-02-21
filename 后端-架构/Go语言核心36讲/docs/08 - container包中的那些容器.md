我们在上次讨论了数组和切片，当我们提到数组的时候，往往会想起链表。那么Go语言的链表是什么样的呢？

Go语言的链表实现在标准库的`container/list`代码包中。这个代码包中有两个公开的程序实体——`List`和`Element`，List实现了一个双向链表（以下简称链表），而Element则代表了链表中元素的结构。

**那么，我今天的问题是：可以把自己生成的`Element`类型值传给链表吗？**

我们在这里用到了`List`的四种方法。

`MoveBefore`方法和`MoveAfter`方法，它们分别用于把给定的元素移动到另一个元素的前面和后面。

`MoveToFront`方法和`MoveToBack`方法，分别用于把给定的元素移动到链表的最前端和最后端。

在这些方法中，“给定的元素”都是`*Element`类型的，`*Element`类型是`Element`类型的指针类型，`*Element`的值就是元素的指针。

```
func (l *List) MoveBefore(e, mark *Element)
func (l *List) MoveAfter(e, mark *Element)

func (l *List) MoveToFront(e *Element)
func (l *List) MoveToBack(e *Element)
```

具体问题是，如果我们自己生成这样的值，然后把它作为“给定的元素”传给链表的方法，那么会发生什么？链表会接受它吗？

这里，给出一个**典型回答**：不会接受，这些方法将不会对链表做出任何改动。因为我们自己生成的`Element`值并不在链表中，所以也就谈不上“在链表中移动元素”。更何况链表不允许我们把自己生成的`Element`值插入其中。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/46/50/511205c3.jpg" width="30px"><span>louis</span> 👍（45） 💬（5）<div>郝老师，这里不太理解什么叫“自己生成的Element类型值”？把自己生成的Element类型值传给链表——这个能不能再通俗点描述？</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b7/b5/07fc5f58.jpg" width="30px"><span>fliter</span> 👍（10） 💬（2）<div>为什么不把list像slice，map一样作为一种不需要import其他包就能使用的数据类型？是因为使用场景较后两者比较少吗</div>2018-08-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKdiaUiaCYQe9tibemaNU5ya7RrU3MYcSGEIG7zF27u0ZDnZs5lYxPb7KPrAsj3bibM79QIOnPXAatfIw/132" width="30px"><span>Geek_a8be59</span> 👍（7） 💬（2）<div>您好 能否出一个list 链表生成的一个图解，现在我看源码用图去模拟生成 一直搞混掉，特别是在初始化的时候prev和next都指向自身的root 这个很迷糊
比如:
	c.PushBack(&quot;123&quot;)
	c.PushFront(&quot;456&quot;)
	c.PushFront(&quot;789&quot;)
根据个人图解应该是789-》456-》nil，为什么能遍历出来很不清楚。能否有一个从初始化到最后生成的样例看一下 万分感谢</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e9/71/40b04914.jpg" width="30px"><span>Zer0</span> 👍（6） 💬（1）<div>不能把自己生成的Element传给List主要是因为Element的list成员是不开放的，我们不能操作，而在List上操作Element的时候是会判断Element的list成员是否是自己。是这样吗？</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5f/09/80484e2e.jpg" width="30px"><span>李斌</span> 👍（5） 💬（3）<div>用 vscode 就蛮好的，我之前是八年 vim 党，写 golang 时硬生生地被掰成 vscode</div>2018-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/2a/68913d36.jpg" width="30px"><span>杨震</span> 👍（4） 💬（1）<div>以后再有课的话  希望老师多加点图   虽然费点事  但应该更多为学员着想吧。文字阐述一点也不直观。</div>2020-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9d/a4/5d2b5aed.jpg" width="30px"><span>雷朝建</span> 👍（3） 💬（1）<div>老师， 我看了一下list.go的源码，发现一个疑问是：延迟初始化的含义就是调用lazyInit，它的一个判断条件是：l.root.next==nil； 但是我们在使用list时候，不是先调用New函数吗？那么不应该会出现l.root.next为nil的情况的。
什么时候回出现l.root.next==nil, 从而导致源码中每次的PushFront等操作调用lazyInit呢？</div>2021-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/37/8775d714.jpg" width="30px"><span>jackstraw</span> 👍（3） 💬（1）<div>我尝试打印了 “var l = list.New()” 与 “var l list.List”两种方式的l类型，发现是不一样的，但是下面的操作却都是可以的
func main() {
    &#47;&#47;l := list.New()
    var l list.List
    e4 := l.PushBack(4)
    e1 := l.PushFront(1)
    l.InsertBefore(3, e4)
    l.InsertAfter(2, e1)
    &#47;&#47;travel(l)
    travel(&amp;l)
}</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3f/c9/1ccefb9a.jpg" width="30px"><span>Sky</span> 👍（2） 💬（1）<div>这一讲没有实例代码</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/1c/c0d14793.jpg" width="30px"><span>白有才</span> 👍（0） 💬（1）<div>这课程就像小说里的武功秘籍, 看了你不一定会练, 所以练成绝世武功的人就少之又少</div>2021-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（0） 💬（1）<div>这一课没有示例代码，确实不太习惯，去看了一下 list.go 的源码，才平复了一下心情。

List 实现了一个双向链表，Ring 实现一个循环链表。

对于思考题，container&#47;ring 包中的循环链表可能的适用场景可能有类似于滑动窗口协议的缓存实现，可以实现 FIFO 的队列；

container&#47;heap 没有用过，看了一下 heap.go 的源码，以及附带的 example_intheap_test.go 和 example_pq_test.go，感觉设计还是很巧妙的，可以用于堆排序和优先队列。</div>2021-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（1）<div>老师你好，go内置的数据结构是不是挺少的？</div>2020-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/73/abb7bfe3.jpg" width="30px"><span>疯琴</span> 👍（0） 💬（1）<div>请问老师，为什么切片扩容以后”旧的底层数组无法被回收“？是指扩容太频繁GC没来得及清理么？</div>2020-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0b/0f/8a524cab.jpg" width="30px"><span>漫步跑小鸡</span> 👍（0） 💬（1）<div>container&#47;list 的元素Element为啥还要设置自己所属的列表，这样设计解决的是什么问题？
&#47;&#47; The list to which this element belongs.
	list *List</div>2020-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/94/12/15558f28.jpg" width="30px"><span>Jason</span> 👍（0） 💬（1）<div>老师，读了list.go源码后有点理解您说的自定义的elem不被List接受的含义了，因为自定义的elem里的list成员为nil,在List的成员函数中和自身的指针不同。但是我还有两个疑问，希望老师能解答：
1）使用显示的elem构造，可以被list接受，是否和您说的自定义elem含义不同呢？
fmt.Println(&quot;***********custom pushback*************&quot;)
	em := list.Element{}
	li.PushBack(&amp;em)
	fmt.Println(li.Len())

2）如果elem不是list的元素，像Remove或moveToFront都是不影响源list,那开发者该如何知道成功还是失败呢？</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/84/5e/79568644.jpg" width="30px"><span>兔子高</span> 👍（0） 💬（2）<div>你好，有个问题想问一下，你在文中有说每次判断链表是否初始化很浪费性能，但是你后面又说每次判断链表的长度或者它是否为空，问题如下
1.如何判断是否初始化
2.判断初始化和判断为空的区别
3.判断链表长度和是否为空比判断是否初始化更节约性能是吗？性能大概会节约多少倍呢？
麻烦解答一下，谢谢</div>2018-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/99/44378317.jpg" width="30px"><span>李皮皮皮皮皮</span> 👍（124） 💬（3）<div>1.list可以作为queue和
stack的基础数据结构
2.ring可以用来保存固定数量的元素，例如保存最近100条日志，用户最近10次操作
3.heap可以用来排序。游戏编程中是一种高效的定时器实现方案</div>2018-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6b/23/73f18275.jpg" width="30px"><span>陌上人 .</span> 👍（113） 💬（10）<div>老师,之后的课可不可以多加一些图形解释,原理性的知识只用文字确实有些晦涩难懂</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（49） 💬（4）<div>关于 container包中的链表list 和环ring的知识总结
按我的思考
1. 为什么go语言会出现list这个包
    首先一个语言或者新技术的出现肯定是为了解决一些疑难杂症 在go语言中数组的特点非常鲜明 固定不可变 访问方便,但是如果不适合动态增长，所以出现了slice切片 切片是对数组的一层封装为了解决数组动态扩容问题， 但是实际上底层依赖的还是数组，但是问题来了 如果slice切片 在添加或者删除元素的时候如果没一个好的策略 扩容或者缩容过后旧的切片没有释放 则会造成内存泄漏 就是c语言的malloc 久而久之 内存越来越少 程序就会崩溃, 而List的出现就是为了解决动态扩容或者缩容的后遗症 因为依赖指针这个东西 所以删除和增加都非常方便
2. 延迟初始化机制
   延迟初始化机制 主要是为了解决像数组这种 声明的时候就分配了内存空间的问题，有的时候我们只需要声明，但还不需要使用它，这个时候没有必要分配内存空间，再如文中提到的 在同一时刻声明大量的内存空间的话 那么cpu的使用和内存空间的使用将会激增
   所以我们需要延迟初始化机制(设计模式中的单例模式也提到了延迟初始化问题,避免声明出来没人使用的尴尬局面)
3. list关于延迟初始化机制的一些处理
   延迟初始化机制的缺点就在于在使用的时候需要判断是否已经初始化了,如果使用比较频繁的话，就会造成大量的计算浪费(cpu浪费)
   所以list当中关于延迟初始化机制的处理方案如下
   3.1 在插入新元素时 需要检查是否已经初始化好了
   3.2 在移动 或者将已有元素再修改位置插入时 需要判断元素身上的链表是否和要操作的链表的指针相同 如果不相同说明元素不存在该链表中 如果相同则说明这个链表肯定已经初始化好了
4. ring包和list包的区别
    首先从源码来看
   type Ring struct {
       next, prev *Ring
       Value
   }

  type Element struct {
       next, prev *Element
       list *List &#47;&#47;它所属的链表的指针
       Value interface{} 
  }

   type List struct {
       root element
       len int
   }
   从源码的定义分析得出 ring 的元素就是ring结构体(只代表了一个元素)  而list的元素 是list+element(代表了一个链表)
  list在创建的时候不需要指定元素也没有必要,因为它会不停的增长 而ring的创建需要指定元素个数 且不再增长
  并且list的还存在一个没有实际意义的根元素  该根元素还可以用来连接首位两端 使其成为一个循环链表
关于文中 两个结论的思考
结论1 go语言中切片实现了数组的延迟初始化机制
       我的思考是 因为切片延迟初始化了， 所以他的底层数组在切片声明时也没有被初始化出来
结论2 ring 使用len方法是o(n) 而list使用len方法是o(1)
       还没看讲解我就去翻看了源码(我比较喜欢的一句话是源码之下无秘密),从上面两个结构体的声明和list的insert方法可以看出 因为list的根元素这个根元素也代表了链表(突然想明白ring和list的第二点区别) 在这个根元素上存放了一个len数据表示链表的长度 insert时这个长度会执行+1,所以执行len方法时只需要取出这个长度即可从而达到了o(1)的时间复杂度 而ring结构体中却不存在这样的len所以需要遍历完整个环,所以时间复杂度为o(n)
关于思考题
1. ring包从实现来分析得出 适合用来执行长度固定的循环事件
2. heap包 则适合用来做堆排序 求第k大 第k小等问题 还有就是前面某些同学提到的优先调度问题
关于优先调度问题我觉得思路大概如下
首先维护一个堆 然后针对每个要调度的事件 分配一个优先级 然后从下到上执行堆化过程 让优先级(最低或者最高的放到堆的顶部) 当处理完成之后 再把堆尾部的事件放到堆顶部 然后执行从上往下进行堆化维护好堆的顺序 再执行逻辑</div>2020-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/77/a4/e57f2014.jpg" width="30px"><span>Err</span> 👍（39） 💬（0）<div>我觉得写一个实际的例子能帮助更好理解</div>2018-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9f/1d/ec173090.jpg" width="30px"><span>melon</span> 👍（22） 💬（1）<div>list的一个典型应用场景是构造FIFO队列；ring的一个典型应用场景是构造定长环回队列，比如网页上的轮播；heap的一个典型应用场景是构造优先级队列。</div>2018-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/a1/43d83698.jpg" width="30px"><span>云学</span> 👍（10） 💬（0）<div>在内存上，和ring的区别是list多了一个特殊表头节点，充当哨兵</div>2018-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/39/04/a8817ecf.jpg" width="30px"><span>会网络的老鼠</span> 👍（8） 💬（2）<div>现在大家写golang程序，一般用什么IDE？</div>2018-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2d/18/918eaecf.jpg" width="30px"><span>后端进阶</span> 👍（7） 💬（2）<div>前面的网友，goland了解一下，超赞的ide</div>2018-09-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLDpvdcQA8KSxEh9NRlyWZJR8icuefKbSpapgIDuKVYdEgeT9X0NC5VsOaQBPvIOLRbWC15qp6eGmQ/132" width="30px"><span>为中华之崛起而卷</span> 👍（1） 💬（0）<div>数据结构的使用，我觉得是实际开发过程中最重要，最高频的部分，感觉这边有些过于简单了不是吗，没有代码示例，纯靠文字描述，你可以认为是写给有go语言开发经验的人看的，但是真的有go语言开发经验的从你这一节也没啥太大的收获吧。</div>2024-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（0）<div>对于这一讲的内容，确实要用IDE（例如Goland）打开源码文件一边阅读一边对着课中的文字，一边推敲、实验。

几个源码文件都是一两百来行，读起来不吃力。（前提是已经有了Go的基础）</div>2021-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/37/3f/a9127a73.jpg" width="30px"><span>KK</span> 👍（1） 💬（0）<div>关于list的结构，画个图会更加直观</div>2020-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/a8/98507423.jpg" width="30px"><span>lixiaofeng</span> 👍（1） 💬（0）<div>func flist(){
    link := list.New()
    for i:=1; i&lt; 11; i++  {
        link.PushBack(i)
    }
    for p:= link.Front(); p!=link.Back(); p=p.Next(){
        fmt.Println(&quot;Number&quot;, p.Value)
    }
}
#链表的常用方法
func (e *Element) Next() *Element
func (e *Element) Prev() *Element
func (l *List) Init() *List
 New() *List { return new(List).Init() }
 func (l *List) Len() int { return l.len }
 func (l *List) Front() *Element
 func (l *List) Back() *Element
 func (l *List) Remove(e *Element) interface{}
 func (l *List) PushFront(v interface{}) *Element
 func (l *List) PushBack(v interface{}) *Element
 func (l *List) InsertBefore(v interface{}, mark *Element) *Element 
 func (l *List) InsertAfter(v interface{}, mark *Element) *Element
 func (l *List) MoveToFront(e *Element)
 func (l *List) MoveToBack(e *Element) 
 func (l *List) MoveBefore(e, mark *Element)
 func (l *List) MoveAfter(e, mark *Element)
 func (l *List) PushBackList(other *List)
 func (l *List) PushFrontList(other *List)</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/46/3573d1d0.jpg" width="30px"><span>缘木求鱼</span> 👍（1） 💬（0）<div>又比如，在用于删除元素、移动元素，以及一些用于插入元素的方法中，只要判断一下传入的元素中指向所属链表的指针，是否与当前链表的指针相等就可以了。   这里传入的元素的所属链表指针是如何赋值的</div>2018-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/91/15/3657d6ee.jpg" width="30px"><span>citi 城</span> 👍（0） 💬（0）<div>container包含list、ring、heap三个子包，分别是链表、循环链表、堆。
是golang sdk原生支持的3个容器类。
list开箱即用，通过lazyinit在操作链表时进行初始化的动作。</div>2023-12-17</li><br/>
</ul>