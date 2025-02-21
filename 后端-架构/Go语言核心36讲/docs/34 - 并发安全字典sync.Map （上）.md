在前面，我几乎已经把Go语言自带的同步工具全盘托出了。你是否已经听懂了会用了呢？

无论怎样，我都希望你能够多多练习、多多使用。它们和Go语言独有的并发编程方式并不冲突，相反，配合起来使用，绝对能达到“一加一大于二”的效果。

当然了，至于怎样配合就是一门学问了。我在前面已经讲了不少的方法和技巧，不过，更多的东西可能就需要你在实践中逐渐领悟和总结了。

* * *

我们今天再来讲一个并发安全的高级数据结构：`sync.Map`。众所周知，Go语言自带的字典类型`map`并不是并发安全的。

## 前导知识：并发安全字典诞生史

换句话说，在同一时间段内，让不同goroutine中的代码，对同一个字典进行读写操作是不安全的。字典值本身可能会因这些操作而产生混乱，相关的程序也可能会因此发生不可预知的问题。

在`sync.Map`出现之前，我们如果要实现并发安全的字典，就只能自行构建。不过，这其实也不是什么麻烦事，使用 `sync.Mutex`或`sync.RWMutex`，再加上原生的`map`就可以轻松地做到。

GitHub网站上已经有很多库提供了类似的数据结构。我在《Go并发编程实战》的第2版中也提供了一个比较完整的并发安全字典的实现。它的性能比同类的数据结构还要好一些，因为它在很大程度上有效地避免了对锁的依赖。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/2d/2c9177ca.jpg" width="30px"><span>给力</span> 👍（5） 💬（1）<div>并发安全的字典里少了两个方法，比如已经有多少key，我们有什么解决办法没，只能自己每次插入或者删除key记录元素个数变化吗？
</div>2020-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e8/55/63189817.jpg" width="30px"><span>MClink</span> 👍（2） 💬（1）<div>感觉并发编程和日常的业务CRUD还是有很多区别的，一般业务很多东西都用不上。</div>2022-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（2） 💬（1）<div>郝林老师，在 IntStrMap 的方法中这种 值点上 括号 string int。  key.(int) 、value.(string) 、a.(string) 代表的是将对应的数据转换为 string和 int 类型吧？ 我这样理解对吗？</div>2021-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/93/38/71615300.jpg" width="30px"><span>DayDayUp</span> 👍（1） 💬（1）<div>老师，看到有人用github.com&#47;orcaman&#47;concurrent-map，不知道二者有何区别呢？</div>2022-05-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（1）<div>能用原子操作就不要用锁，不过这很有局限性，毕竟原子只能对一些基本的数据类型提供支持。问题：
atomic.Value不是可以支持除了二进制和int类型以外的数据类型的原子操作吗，还是其仍有一定局限性，另外atomic.Value使用是否有禁忌或者需要注意的地方</div>2021-10-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（2）<div>我们都知道，使用锁就意味着要把一些并发的操作强制串行化。这往往会降低程序的性能，尤其是在计算机拥有多个 CPU 核心的情况下。问题：
1 一个程序的每个进程只能跑在一个cpu的核心上，对吗？
2 每个进程中的锁只会控制该进程内部的goroutine串行执行，应该是不能控制其他进程里的goroutine的吧，那这里多核CPU下使用互斥锁更加影响性能的意思是指什么</div>2021-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a7/b2/274a4192.jpg" width="30px"><span>漂泊的小飘</span> 👍（0） 💬（1）<div>什么字典的并发写会造成fatal error呢，简单的原理是什么？</div>2020-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/73/abb7bfe3.jpg" width="30px"><span>疯琴</span> 👍（0） 💬（1）<div>我觉得老师的示例代码要是对 sync.map 做一些可能引发冲突的并发操作就更好了。</div>2020-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（29） 💬（0）<div>打卡，后面的留言越来越少，看来有点难度了，加油啃下它！后面的兄弟</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/aa/21275b9d.jpg" width="30px"><span>闫飞</span> 👍（8） 💬（2）<div>我觉得这里的主要麻烦之一是golang不支持泛型编程这一重大的范式，用户不得不在上层代码里面做繁琐的检查。</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8c/e2/48f4e4fa.jpg" width="30px"><span>mkii</span> 👍（1） 💬（0）<div>这下可以把项目里丑陋的mutex+map去掉了👍👍👍</div>2021-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/0c/8d/90bee755.jpg" width="30px"><span>寄居与蟹</span> 👍（0） 💬（0）<div>打卡，冲</div>2022-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/91/17/89c3d249.jpg" width="30px"><span>下雨天</span> 👍（0） 💬（1）<div>我最近遇到一个问题，sync.Map之间赋值操作之后，会变成线程不安全的map（原始map），赋值之后可能会导致底的原始map操作出现读写，导致问题。</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/59/8bb1f879.jpg" width="30px"><span>涛声依旧</span> 👍（0） 💬（0）<div>这个章节我又学习一招</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4b/35/28fa7039.jpg" width="30px"><span>猫九</span> 👍（0） 💬（0）<div>打卡</div>2019-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/67/6e/d59a413f.jpg" width="30px"><span>羽仔</span> 👍（0） 💬（0）<div>Fine.</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0e/12/0398de50.jpg" width="30px"><span>么乞儿</span> 👍（0） 💬（0）<div>打卡!</div>2019-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/69/39d0a2b2.jpg" width="30px"><span>show</span> 👍（0） 💬（0）<div>打卡，读完了，还需要实践下</div>2019-03-15</li><br/>
</ul>