Java对象，特别是一个比较大、比较复杂的Java对象，它们的创建、初始化和GC都需要耗费CPU和内存资源，为了减少这些开销，Tomcat和Jetty都使用了对象池技术。所谓的对象池技术，就是说一个Java对象用完之后把它保存起来，之后再拿出来重复使用，省去了对象创建、初始化和GC的过程。对象池技术是典型的以**空间换时间**的思路。

由于维护对象池本身也需要资源的开销，不是所有场景都适合用对象池。如果你的Java对象数量很多并且存在的时间比较短，对象本身又比较大比较复杂，对象初始化的成本比较高，这样的场景就适合用对象池技术。比如Tomcat和Jetty处理HTTP请求的场景就符合这个特征，请求的数量很多，为了处理单个请求需要创建不少的复杂对象（比如Tomcat连接器中SocketWrapper和SocketProcessor），而且一般来说请求处理的时间比较短，一旦请求处理完毕，这些对象就需要被销毁，因此这个场景适合对象池技术。

## Tomcat的SynchronizedStack

Tomcat用SynchronizedStack类来实现对象池，下面我贴出它的关键代码来帮助你理解。

```
public class SynchronizedStack<T> {

    //内部维护一个对象数组,用数组实现栈的功能
    private Object[] stack;

    //这个方法用来归还对象，用synchronized进行线程同步
    public synchronized boolean push(T obj) {
        index++;
        if (index == size) {
            if (limit == -1 || size < limit) {
                expand();//对象不够用了，扩展对象数组
            } else {
                index--;
                return false;
            }
        }
        stack[index] = obj;
        return true;
    }
    
    //这个方法用来获取对象
    public synchronized T pop() {
        if (index == -1) {
            return null;
        }
        T result = (T) stack[index];
        stack[index--] = null;
        return result;
    }
    
    //扩展对象数组长度，以2倍大小扩展
    private void expand() {
      int newSize = size * 2;
      if (limit != -1 && newSize > limit) {
          newSize = limit;
      }
      //扩展策略是创建一个数组长度为原来两倍的新数组
      Object[] newStack = new Object[newSize];
      //将老数组对象引用复制到新数组
      System.arraycopy(stack, 0, newStack, 0, size);
      //将stack指向新数组，老数组可以被GC掉了
      stack = newStack;
      size = newSize;
   }
}
```
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/6d/8f/81e282e2.jpg" width="30px"><span>802.11</span> 👍（15） 💬（2）<div>工厂模式和池化思想有什么区别呢</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（5） 💬（1）<div>同步栈有看到，但是不知道它是做池化用的 😂😂😂

线程池 里面维护了线程数组和任务队列
连接池 
jvm的常量池 ？</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（5） 💬（4）<div>老师好学到了。通过threadlocal来减少锁竞争上下文切换的开销。
可是我看见好多帖子说threadlocal容易内存泄露啥的肯比较多需要慎用。五年码龄从没用过😂。
请教一个问题threadLocal中的对象如果用完不清。下次别的请求Tomcat线程池中拿到同个线程，能取到之前请求存入的数据么?</div>2019-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/87/be/7466bf26.jpg" width="30px"><span>清风</span> 👍（4） 💬（3）<div>也看了些书上的讲解，看完后还是没有像老师这样能总结出一个清晰的逻辑结构，这样的情况需要怎么办呢</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/c5/7fc124e2.jpg" width="30px"><span>Liam</span> 👍（4） 💬（1）<div>tomcat和jetty的对象池没有空闲超时&#47;超量回收的机制吗？</div>2019-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/65/10/a543759a.jpg" width="30px"><span>kyon</span> 👍（3） 💬（1）<div>您好，请问 ArrayByteBufferPool 中，direct 和 indirect 都是 new 出来的，区别是什么？另外在 new ByteBufferPool.Bucket(this,size,_maxQueue) 中，参数 _maxQueue 的作用是什么？</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（2） 💬（3）<div>请问老师Tomcat为什么用栈做对象池，那要去栈底的对象不是很麻烦很不灵活吗？为啥不用map的方式呢？</div>2019-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/a6/6e/0ffa1ff6.jpg" width="30px"><span>XxxxxxxMr</span> 👍（0） 💬（1）<div>老师 我有一个疑问  池化。对象池 、线程池 、数据库连接池等等 他们都是如出一辙吗？还是大同小异</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/47/d1/15f1a8ce.jpg" width="30px"><span>TJ</span> 👍（0） 💬（1）<div>为什么tomcat不使用java本身的stack class? 它也是基于数组的。自己再加一个同步就可以了</div>2019-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fc/b5/ac717737.jpg" width="30px"><span>肖臧</span> 👍（6） 💬（0）<div>Java的Integer类的IntegerCache就是利用了池化技术，还有String.intern()也算池化技术</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cf/14/384258ba.jpg" width="30px"><span>Wiggle Wiggle</span> 👍（4） 💬（0）<div>“并且它本身只支持扩容不支持缩容，也就是说数组对象在使用过程中不会被重新赋值，也就不会被 GC”。这句话是不是写错了？我觉得是不是想说【数组元素】在使用过程中不会被重新赋值？因为扩容的话，创建了新的数组；缩容的话反而不用创建新的数组</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（1） 💬（0）<div>老师对象池可以认为是享元模式吗?对象结构和一些重复参数是元</div>2021-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/5d/d4/e5ea1c25.jpg" width="30px"><span>sun留白</span> 👍（1） 💬（2）<div>理解tomcat的数组是每个位置的对象set好后，不会被替换掉，当需要新的不存在的额对象时，再建立。那么，数组长度如何控制呢？达到长度限制时，长时间未用的对象被新的对象替换掉吗？请问老师，我这样理解对吗？</div>2020-01-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（0） 💬（0）<div>Spring的单例池也算一种对象池吧？</div>2022-09-09</li><br/><li><img src="" width="30px"><span>Geek_00271d</span> 👍（0） 💬（0）<div>在工作中会用到okhttpclient，看了里面源码，里面用到了连接池</div>2022-01-19</li><br/><li><img src="" width="30px"><span>Geek_383ffd</span> 👍（0） 💬（1）<div>如果你的内存足够大，可以考虑用线程本地（ThreadLocal）对象池，这样每个线程都有自己的对象池，线程之间互不干扰。
老师您好，不太理解这里为什么每个线程都弄对象池</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/c8/5ce842f6.jpg" width="30px"><span>maybe</span> 👍（0） 💬（0）<div>当需要频繁创建和销毁对象且对象的创建比较麻烦和消耗资源的时候，可以使用池化技术通过空间换取时间的策略。池化技术重用对象，减少对象创建和销毁的开销，也可以用于限制资源的创建，比如数据库连接。不过需要注意内存泄漏、对象及时重置防止脏读的问题</div>2020-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fc/b5/ac717737.jpg" width="30px"><span>肖臧</span> 👍（0） 💬（0）<div>SynchronizedStack的全局变量index应该会初始化成-1吧，要不然stack数组的第一个位置就浪费了，而且代码里有一些index = -1的逻辑判断。</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/5d/d4/e5ea1c25.jpg" width="30px"><span>sun留白</span> 👍（0） 💬（0）<div>Bucket[i]中的是size相同的Buffer队列。Bucket的内部用一个 ConcurrentLinkedDeque 来放置 ByteBuffer 对象的引用。这么理解对吗？老师。</div>2020-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/78/0f/f4e012a1.jpg" width="30px"><span>掐你小77</span> 👍（0） 💬（0）<div>老师，你说的：“对象一旦归还给对象池，使用者就不能对它做任何操作了”，是一种默认的编码规范么？一种口头约束：即使用者不应该再持有这个对象引用对对象做一些操作，避免造成一些线程安全问题。可以这样理解么？</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/7f/a7df049a.jpg" width="30px"><span>Standly</span> 👍（0） 💬（0）<div>赞，如果能有jetty和netty对象池实现的对比就更好了</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（0） 💬（0）<div>我之前听人说事务里面的数据库链接就是通过threadLocal来共享的(事务结束后会从threadlocal删除当前链接么?)。那这个数据库的连接如果和Tomcat的线程数一对一绑定上能提高效率么?</div>2019-06-25</li><br/>
</ul>