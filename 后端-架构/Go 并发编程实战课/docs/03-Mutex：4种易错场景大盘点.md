你好，我是鸟窝。

上一讲，我带你一起领略了Mutex的架构演进之美，现在我们已经清楚Mutex的实现细节了。当前Mutex的实现貌似非常复杂，其实主要还是针对饥饿模式和公平性问题，做了一些额外处理。但是，我们在第一讲中已经体验过了，Mutex使用起来还是非常简单的，毕竟，它只有Lock和Unlock两个方法，使用起来还能复杂到哪里去？

正常使用Mutex时，确实是这样的，很简单，基本不会有什么错误，即使出现错误，也是在一些复杂的场景中，比如跨函数调用Mutex或者是在重构或者修补Bug时误操作。但是，我们使用Mutex时，确实会出现一些Bug，比如说忘记释放锁、重入锁、复制已使用了的Mutex等情况。那在这一讲中，我们就一起来看看使用Mutex常犯的几个错误，做到“Bug提前知，后面早防范”。

# 常见的4种错误场景

我总结了一下，使用Mutex常见的错误场景有4类，分别是Lock/Unlock不是成对出现、Copy已使用的Mutex、重入和死锁。下面我们一一来看。

## Lock/Unlock不是成对出现

Lock/Unlock没有成对出现，就意味着会出现死锁的情况，或者是因为Unlock一个未加锁的Mutex而导致panic。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/e1/4f/00476b4c.jpg" width="30px"><span>Remember九离</span> 👍（19） 💬（3）<div>第三课代码整理:https:&#47;&#47;github.com&#47;wuqinqiang&#47;Go_Concurrency&#47;tree&#47;main&#47;class_3</div>2020-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/56/6c/042a2e41.jpg" width="30px"><span>David</span> 👍（3） 💬（3）<div>个人理解：我觉得go里面的可重入锁，有点鸡肋，这也是go官方没有实现的原因吧。第一，如果我加了互斥锁，说明这临界区的资源都是某个groutine独享，那何必要在临界区里面再去请求锁呢，不是多此一举吗，第二，就拿递归来说，我们完全可以把加在递归函数里面的锁，提取到调用递归之前，这样就可以避免递归函数加锁的情况。这是我的个人理解。在redis里面有分布式锁，会出现一个持有锁的线程再次加锁的情况，但是呢，和这里的使用情况还是不一样，redis一般加锁，都会加个有效期(担心忘记释放锁，造成死锁)，这个有效期时间长度，不能太大于程序执行时间，这样如果锁来不及释放的时候可能会影响性能，所以一般有效期都和程序执行时间差不多。但是有时候，出现执行时间长超过了有效期的时候，需要续期，才有再次请求锁。以上是我个人理解，如果老师看到评论，可以点评一下我的思维是否有问题</div>2020-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/56/6c/042a2e41.jpg" width="30px"><span>David</span> 👍（2） 💬（4）<div>您好老师，在设计可重入锁的时候，在lock方法中，
	&#47;&#47; 延用mutex的加锁机制
	m.Mutex.Lock()
	atomic.StoreInt64(&amp;m.owner, gid)
这个地方有必要 使用atomic吗？
      

其次，如果有必要，为什么  m.recursion = 1  不用了呢
我个人认为，在锁里面，好像是没必要使用的吧</div>2021-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/80/de/c6191045.jpg" width="30px"><span>gitxuzan</span> 👍（2） 💬（3）<div>有个地方不明白， 为什么源码里面需要用atomic 原子操作和直接赋值有什么区别</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/59/d3/696b1702.jpg" width="30px"><span>校歌</span> 👍（1） 💬（1）<div>Tidb在用mutex的时候特意改成了defer 这种方式，https:&#47;&#47;github.com&#47;pingcap&#47;tidb&#47;pull&#47;19072，
不过找了个比较老的issue，https:&#47;&#47;github.com&#47;pingcap&#47;tidb&#47;pull&#47;5171 ，lock和unlock还是没有统一用defer的方式，这个以后可能成为隐患吧。</div>2021-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（1） 💬（2）<div>看了前三节，这门课写的太棒了。继续打卡。</div>2020-12-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PXT6vnzzI62YFMeecE5Jic5jzrO2vAFlZicAOic3sTpTNFvs3YeDcBV2FyBfhHiaKjibplY2vIfBzeFDCkQSRQyOM1eDAvrGtvVJgS5MbCZJeiap4/132" width="30px"><span>Geek_fa7924</span> 👍（0） 💬（1）<div>老师您好，看到第三节课了。这里我有个疑问，课程中遇到重入锁导致死锁的问，老师都是说提供一个不加锁的方法，这里我不太明白，不加锁的方法的含义？</div>2024-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/2e/ca/469f7266.jpg" width="30px"><span>菠萝吹雪—Code</span> 👍（0） 💬（1）<div>打卡

作业：

https:&#47;&#47;github.com&#47;pingcap&#47;tidb&#47;issues&#47;27725  
</div>2022-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/06/ed/5a167dda.jpg" width="30px"><span>niceshot</span> 👍（0） 💬（2）<div>func (m *TokenRecursiveMutex) Lock(token int64)  {
	if atomic.LoadInt64(&amp;m.token)==token{
		m.recursion++
		return
	}
	m.Mutex.Lock()
	atomic.StoreInt64(&amp;m.token,token)
	m.recursion = 1
}
这里如果调用者提供前后两次两个不同的token Mutex.Lock()不就调用两次了吗</div>2020-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/6e/76b4aa3d.jpg" width="30px"><span>橙子888</span> 👍（0） 💬（1）<div>更新地好快，上一讲的源码还没消化完，新的一讲又出了……</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ab/a9/590d6f02.jpg" width="30px"><span>Junes</span> 👍（64） 💬（0）<div>分享一个我觉得很有项目借鉴意义的PR吧：

https:&#47;&#47;github.com&#47;pingcap&#47;tidb&#47;pull&#47;20381&#47;files 

这个问题是在当前的函数中Lock，然后在调用的函数中Unlock。这种方式会导致，如果运行子函数时panic了，而外部又有recover机制不希望程序崩溃，就触发不到Unlock，引起死锁。

PR中加了个recover处理，并且判断recover有error才Unlock，这是一种处理方法。

理想的设计，是将子函数的Unlock挪到与Lock平级的代码，或者不进行recover处理，Let it panic后修复问题。但大型项目项目经常会因为逻辑错综复杂或者各种历史原因，不好改动吧，这种处理方式虽然不好看，但能解决问题，有时候也挺无奈的~</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/1f/b1d458a9.jpg" width="30px"><span>iamjohnnyzhuang</span> 👍（16） 💬（4）<div>买这个课程本来没报多大希望，没想到看看几节下来太赞了，不仅说到了一些技术的实现细节，同时给出的让我们业务开发避免的经验、排查方法也十分有借鉴价值</div>2020-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5e/d3/e4d2ae68.jpg" width="30px"><span>buckwheat</span> 👍（8） 💬（3）<div>看了一眼tidb关于mutex的issue，发现大部问题都出现在Unlock的时机上面，尤其是涉及到多个锁的时候，把Lock和Unlock放到两个方法里面就非常容易出现这种情况。tidb出现data race的issue要比dead lock的要多的多。老师，业务复杂时，在涉及到链式加锁时有没有什么好的办法避免死锁呢？</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/96/5a/846a09f7.jpg" width="30px"><span>pony</span> 👍（5） 💬（1）<div>老师讲解的很仔细，对mutex使用错误场景都列举了
补充点：Go语言核心36讲的解锁一个未加锁的mutex 导致的panic，无法被recover()捕获</div>2020-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2e/f4/1e4d6941.jpg" width="30px"><span>打奥特曼的小怪兽</span> 👍（5） 💬（0）<div>这个课程看起来很有意思</div>2020-10-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/vRoYUplibtKY2YFg7icP8A7SBSicAuhxz2mxgY6kibzaKRO8c1PXpNskGJB2Z3WfFoRaX5nh8oztib0NOr5qNdibCyaw/132" width="30px"><span>消逝文字</span> 👍（4） 💬（0）<div>真是想不到，知名的开源项目里面居然也会有一些我们编码时常犯的低级错误</div>2020-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/6e/76b4aa3d.jpg" width="30px"><span>橙子888</span> 👍（4） 💬（1）<div>在 TiDB Pull requests 已经 closed 的搜索 deadlock 关键字发现好多，例如 https:&#47;&#47;github.com&#47;pingcap&#47;tidb&#47;pull&#47;500，问题的原因在于释放的位置有问题。</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（3） 💬（0）<div>简单易懂 列举知名开源项目漏洞来对应自己的总结 太棒了👏</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/31/9d/daad92d2.jpg" width="30px"><span>Stony.修行僧</span> 👍（3） 💬（0）<div>活捉一只大佬，写的真好，感觉编程语言里面锁技术是精髓之一</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/54/b3eb605b.jpg" width="30px"><span>阿牛</span> 👍（2） 💬（0）<div>Mutex常见四种错误场景
1、Lock&#47;Unlock不是成对出现
2、Copy已使用的Mutex
3、重入
4、死锁</div>2021-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/04/f3/a3ff8a58.jpg" width="30px"><span>roseduan</span> 👍（2） 💬（0）<div>将 Unlock 误写成了 Lock，哈哈哈，原来这些大佬也会犯低级错误</div>2020-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（0）<div>能把并发的课程讲得这么深入浅出，老师的功底可见一斑~</div>2022-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/22/c8/f2892022.jpg" width="30px"><span>科科</span> 👍（1） 💬（0）<div>大佬也有写错的时候，不能说完全避免问题，但一定要学习如何解决问题</div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b6/5b/4486e4f9.jpg" width="30px"><span>虫子樱桃</span> 👍（1） 💬（0）<div>跟这个很类似 https:&#47;&#47;medium.com&#47;@bytecraze.com&#47;recursive-locking-in-go-9c1c2a106a38</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/a5/a5/ad715d22.jpg" width="30px"><span>echo</span> 👍（0） 💬（0）<div>同志们 我又来了</div>2022-07-17</li><br/><li><img src="" width="30px"><span>taro</span> 👍（0） 💬（0）<div>对owner&#47;token的操作为什么要用原子操作呢？多个goroutine读取或者写入owner&#47;token的值会影响可重入锁的运行效果吗？</div>2022-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/a5/a5/ad715d22.jpg" width="30px"><span>echo</span> 👍（0） 💬（0）<div>打开</div>2022-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/bb/e0/c7cd5170.jpg" width="30px"><span>Bynow</span> 👍（0） 💬（0）<div>go vet 为什么无法检查 goroutine 里的锁问题？</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7e/75/3e6bdc4c.jpg" width="30px"><span>李金狗</span> 👍（0） 💬（0）<div>写了一个库 https:&#47;&#47;github.com&#47;longlihale&#47;goid 获取 goid 的欢迎大家使用～ </div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/89/71/03a99e56.jpg" width="30px"><span>、荒唐_戏_</span> 👍（0） 💬（0）<div>docker 第二个锁问题，遇到相同的，当时排查了一天多。搞到凌晨一点，没搞定，第二天中午十一点发现依赖的同事开发的库有这个问题， 发现原因的时候想死的心都有了</div>2021-07-17</li><br/>
</ul>