我们知道Tomcat和Jetty的核心功能是处理请求，并且请求的处理者不止一个，因此Tomcat和Jetty都实现了责任链模式，其中Tomcat是通过Pipeline-Valve来实现的，而Jetty是通过HandlerWrapper来实现的。HandlerWrapper中保存了下一个Handler的引用，将各Handler组成一个链表，像下面这样：

WebAppContext -&gt; SessionHandler -&gt; SecurityHandler -&gt; ServletHandler

这样链中的Handler从头到尾能被依次调用，除此之外，Jetty还实现了“回溯”的链式调用，那就是从头到尾依次链式调用Handler的**方法A**，完成后再回到头节点，再进行一次链式调用，只不过这一次调用另一个**方法B**。你可能会问，一次链式调用不就够了吗，为什么还要回过头再调一次呢？这是因为一次请求到达时，Jetty需要先调用各Handler的初始化方法，之后再调用各Handler的请求处理方法，并且初始化必须在请求处理之前完成。

而Jetty是通过ScopedHandler来做到这一点的，那ScopedHandler跟HandlerWrapper有什么关系呢？ScopedHandler是HandlerWrapper的子类，我们还是通过一张图来回顾一下各种Handler的继承关系：
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（9） 💬（1）<div>最后的问题，应该是这样的：

protected void doStart() throws Exception
{
    try{
        _outerScope=__outerScope.get();
        if (_outerScope==null){
           &#47;&#47;本次处理的第一个scope handler
           &#47;&#47;告知后续scope handler，_outerScope选我
            __outerScope.set(this);
        }
        super.doStart();
        _nextScope= getChildHandlerByClass(ScopedHandler.class);
    }
    finally
    {
        if (_outerScope==null){
           &#47;&#47;本次处理结束
           &#47;&#47;为了下次同一个线程处理是，
           &#47;&#47;还能正常的设置第一个scope handler
           &#47;&#47;必须把threadlocal变量设为null
            __outerScope.set(null);
        }
    }
}


此外，这一节里有一个non scoped handler X，一开始没太看懂调阅顺序。
后来发现是这样的：

public final void nextHandle(String target...)...
{
    if (_nextScope!=null &amp;&amp; _nextScope==_handler){
        &#47;&#47;上面条件可以保证下一个handler是scope handler
        _nextScope.doHandle(target,baseRequest,request, response);
    }
    else if (_handler!=null){
        &#47;&#47;non scpoe handler调用下一个handler的
        super.handle(target,baseRequest,request,response);
    }
}

感觉类成员的命名不太合适，
比如__outerScope和_outerScope
比如_handler其实一直指向的是下一个handler，是不是该为_nextHandler更好一些？
</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/40/3301e490.jpg" width="30px"><span>despacito</span> 👍（6） 💬（0）<div>ScopedHandler 会有不同的实现类，而__outerScope 是ScopedHandler里static的变量，如果不设置为null，那么不同的子类实例执行doStrat()方法的时候，会有问题</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b2/b3/798a4bb2.jpg" width="30px"><span>帽子丨影</span> 👍（5） 💬（1）<div>感觉jetty的源码写的好混乱，经常没有注释，一个类也通常扩展3&#47;4个接口功能，还各种循环嵌套。好难懂。。。</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/ec/779c1a78.jpg" width="30px"><span>往事随风，顺其自然</span> 👍（3） 💬（0）<div>可以重新处理下一次请求</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1e/3a/5b21c01c.jpg" width="30px"><span>nightmare</span> 👍（3） 💬（0）<div>每一次请求的请求链互不影响</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/85/a9/6d4d3ae8.jpg" width="30px"><span>绍棠</span> 👍（1） 💬（0）<div> threadlocal为什么在每次请求结束需要设置为null：为了下次请求复用。因为线程是用池化技术，下次请求优先共用线程，而不是新建线程</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f3/06/8da1bf0c.jpg" width="30px"><span>Fredo</span> 👍（0） 💬（0）<div>1. 防止影响下个请求数据
2. 用完即清理，防内存泄露</div>2024-02-06</li><br/>
</ul>