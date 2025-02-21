你好，我是鸟窝。

Go是一个自动垃圾回收的编程语言，采用[三色并发标记算法](https://go.dev/blog/ismmkeynote)标记对象并回收。和其它没有自动垃圾回收的编程语言不同，使用Go语言创建对象的时候，我们没有回收/释放的心理负担，想用就用，想创建就创建。

但是，**如果你想使用Go开发一个高性能的应用程序的话，就必须考虑垃圾回收给性能带来的影响**，毕竟，Go的自动垃圾回收机制还是有一个STW（stop-the-world，程序暂停）的时间，而且，大量地创建在堆上的对象，也会影响垃圾回收标记的时间。

所以，一般我们做性能优化的时候，会采用对象池的方式，把不用的对象回收起来，避免被垃圾回收掉，这样使用的时候就不必在堆上重新创建了。

不止如此，像数据库连接、TCP的长连接，这些连接在创建的时候是一个非常耗时的操作。如果每次都创建一个新的连接对象，耗时较长，很可能整个业务的大部分耗时都花在了创建连接上。

所以，如果我们能把这些连接保存下来，避免每次使用的时候都重新创建，不仅可以大大减少业务的耗时，还能提高应用程序的整体性能。

Go标准库中提供了一个通用的Pool数据结构，也就是sync.Pool，我们使用它可以创建池化的对象。这节课我会详细给你介绍一下sync.Pool的使用方法、实现原理以及常见的坑，帮助你全方位地掌握标准库的Pool。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/22/58/a2/24612c85.jpg" width="30px"><span>末班车</span> 👍（28） 💬（3）<div>之前用到去看过，好像是通过一个链表的形式，把request存起来，最新的在链表的头，最旧的在链表的尾部，可是不懂的是，为什么每次取出了req，还要重新赋零值呢，这和我每次new一个有什么区别么？求大佬指点。</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（4） 💬（7）<div>请问老师, sync.Pool会有内存泄漏，怎么理解因为 Pool 回收的机制，这些大的 Buffer 可能不被回收？</div>2020-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>老师的文章讲解的非常细致。 请问一下：

1. 三色并发标记算法 这个 链接地址 Not found 了。
2. 举例大的buffer 不被回收的 第一个 源码 函数：putEncodeState ，我没找到。请问一下在哪个文件里面呀。
</div>2021-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/50/a9/3f8c7418.jpg" width="30px"><span>冰糕不冰</span> 👍（0） 💬（1）<div>讲的太好了！ 真的是开启了新世界的大门。 感谢大佬</div>2022-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/0f/f6/609ded9f.jpg" width="30px"><span>tingting</span> 👍（0） 💬（1）<div>请问老师，RPC request 池化的实现为什么不用sync.Map，而是选择使用链表实现呢？</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/37/92/961ba560.jpg" width="30px"><span>授人以🐟，不如授人以渔</span> 👍（0） 💬（1）<div>「因为 Pool 回收的机制，这些大的 Buffer 可能不被回收」是什么原因？</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ab/a9/590d6f02.jpg" width="30px"><span>Junes</span> 👍（13） 💬（1）<div>分享一下我的理解，主要分为回收和获取两个函数：

func (server *Server) freeRequest(req *Request) {
	server.reqLock.Lock()
	&#47;&#47; 将req放在freeReq的头部，指向原先的链表头
	&#47;&#47; 至于为什么放在头部、而不是尾部，我觉得是放在尾部需要遍历完这个链表(增加时间复杂度)、或者要额外维护一个尾部Request的指针(增加空间复杂度)，权衡下放在头部更方便
	req.next = server.freeReq
	server.freeReq = req
	server.reqLock.Unlock()
}

func (server *Server) getRequest() *Request {
	server.reqLock.Lock()
	&#47;&#47; freeReq是一个链表，保存空闲的Request
	req := server.freeReq
	if req == nil {
		&#47;&#47; 初始状态：freeReq为空时，在heap上重新分配一个对象
		req = new(Request)
	} else {
		server.freeReq = req.next
		&#47;&#47; 复用的关键在这里，这里并不是新建一个对象 new(Request)
		&#47;&#47; 这里的思想类似于Reset，将原先有数据的Request设置为空
		*req = Request{}
	}
	server.reqLock.Unlock()
	return req
}</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/24/df/645f8087.jpg" width="30px"><span>Yayu</span> 👍（8） 💬（0）<div>谢谢老师，喜欢老师这篇文章中通过外链的方式列出一些老师常用的三方库，很有用！</div>2020-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/34/b0/8d14a2a1.jpg" width="30px"><span>大布丁</span> 👍（1） 💬（0）<div>一文解决之前组长问我的一个问题：除了使用更多的goroutine来干更多的活之外，还有什么设计与优化的思想？当时没往线程池跟sync.Pool去思考，现在感触很深了！身为年轻人，代码功底不足的情况，我还是喜欢阅读源码后，动手实现里面的几个方法，以便于自己能够更深刻的去理解第三方库！</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b6/5b/4486e4f9.jpg" width="30px"><span>虫子樱桃</span> 👍（1） 💬（2）<div>思考题的奥秘感觉在这两个函数 
```
&#47;&#47; ServeRequest is like ServeCodec but synchronously serves a single request.
&#47;&#47; It does not close the codec upon completion.
func (server *Server) ServeRequest(codec ServerCodec) error {
	sending := new(sync.Mutex)
	service, mtype, req, argv, replyv, keepReading, err := server.readRequest(codec)
	if err != nil {
		if !keepReading {
			return err
		}
		&#47;&#47; send a response if we actually managed to read a header.
		if req != nil {
			server.sendResponse(sending, req, invalidRequest, codec, err.Error())
			server.freeRequest(req)
		}
		return err
	}
	service.call(server, sending, nil, mtype, req, argv, replyv, codec)
	return nil
} 

func (server *Server) freeRequest(req *Request) {
	server.reqLock.Lock()
	req.next = server.freeReq
	server.freeReq = req
	server.reqLock.Unlock()
}
```
</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/8c/f9/e1dab0ca.jpg" width="30px"><span>怎么睡才能做这种梦</span> 👍（0） 💬（0）<div>请问老师, sync.Pool会有内存泄漏，怎么理解因为 Pool 回收的机制，这些大的 Buffer 可能不被回收？</div>2023-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/bf/88/e6d9ec41.jpg" width="30px"><span>Geek_b8670e</span> 👍（0） 💬（0）<div>数据库连接池上有没有必要再做多路复用？</div>2021-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b8/3c/1a294619.jpg" width="30px"><span>Panda</span> 👍（0） 💬（0）<div>减少跟 OS 的 IO 次数  用池化手段来优化系统 </div>2021-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（0） 💬（0）<div>可以用池化技术做任务队列么?尤其是worker pool这几个库</div>2020-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（0） 💬（1）<div>那像websocke这种长连接，每个ws用一个goroutine来维护，是不是就没必要用池化技术了。</div>2020-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/6e/76b4aa3d.jpg" width="30px"><span>橙子888</span> 👍（0） 💬（0）<div>打卡。</div>2020-11-02</li><br/>
</ul>