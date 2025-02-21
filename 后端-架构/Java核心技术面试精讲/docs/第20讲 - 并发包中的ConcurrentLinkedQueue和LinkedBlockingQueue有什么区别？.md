在上一讲中，我分析了Java并发包中的部分内容，今天我来介绍一下线程安全队列。Java标准库提供了非常多的线程安全队列，很容易混淆。

今天我要问你的问题是，并发包中的ConcurrentLinkedQueue和LinkedBlockingQueue有什么区别？

## 典型回答

有时候我们把并发包下面的所有容器都习惯叫作并发容器，但是严格来讲，类似ConcurrentLinkedQueue这种“Concurrent\*”容器，才是真正代表并发。

关于问题中它们的区别：

- Concurrent类型基于lock-free，在常见的多线程访问场景，一般可以提供较高吞吐量。
- 而LinkedBlockingQueue内部则是基于锁，并提供了BlockingQueue的等待性方法。

不知道你有没有注意到，java.util.concurrent包提供的容器（Queue、List、Set）、Map，从命名上可以大概区分为Concurrent\*、CopyOnWrite*和Blocking*等三类，同样是线程安全容器，可以简单认为：

- Concurrent类型没有类似CopyOnWrite之类容器相对较重的修改开销。
- 但是，凡事都是有代价的，Concurrent往往提供了较低的遍历一致性。你可以这样理解所谓的弱一致性，例如，当利用迭代器遍历时，如果容器发生修改，迭代器仍然可以继续进行遍历。
- 与弱一致性对应的，就是我介绍过的同步容器常见的行为“fail-fast”，也就是检测到容器在遍历过程中发生了修改，则抛出ConcurrentModificationException，不再继续遍历。
- 弱一致性的另外一个体现是，size等操作准确性是有限的，未必是100%准确。
- 与此同时，读取的性能具有一定的不确定性。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/58/5d/8de7f8dc.jpg" width="30px"><span>爱新觉罗老流氓</span> 👍（4） 💬（2）<div>杨老师，“与弱一致性对应的，就是我介绍过的同步容器常见的行为“fast-fail”，也就是检测到容器在遍历过程中发生了修改，则抛出 ConcurrentModificationException，不再继续遍历。” 
这一段落里，快速失败的英文在doc上是“fail-fast”，在ArrayList源码中文档可以搜到。
还有，同步容器不应该是“fail-safe”吗？</div>2018-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/92/99530cee.jpg" width="30px"><span>灰飞灰猪不会灰飞.烟灭</span> 👍（3） 💬（1）<div>老师 线程池中如果线程已经运行结束则删除该线程。如何判断线程已经运行结束了呢？源码中我看见按照线程的状态，我不清楚这些状态值哪来的。java代码有判断线程状态的方法吗？谢谢老师</div>2018-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4b/fc/a535ce4f.jpg" width="30px"><span>Invocker.C</span> 👍（2） 💬（2）<div>求老师解答一个困扰已久的问题，就是初始化arrayblockingqueue的时候，capacity的大小如何评估和设置？望解答</div>2018-06-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIyqjqjTlaiavQb1I7d5au4A3mojticTXgBEu6picAv3qS7f1jhdq4bSS8mJpic1zWNhxaQWNPfYkQF0w/132" width="30px"><span>杭州</span> 👍（0） 💬（1）<div>杨老师你好，遇到个问题，200个并发线程池阻塞读linkBlockingQueue队列，偶尔会出现阻塞时会线程cpu很好。jstack看了很多lock。会不会出现线程离开线程池，去干别的任务，干了一半又回到线程池中干活。两边出现死锁？</div>2018-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/95/96/0020bd67.jpg" width="30px"><span>夏洛克的救赎</span> 👍（0） 💬（1）<div>老师你好，问个题外问题，在jdk10源码  string类中，成员变量coder起到什么作用？如何理解？</div>2018-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/32/3f/fa4ac035.jpg" width="30px"><span>sunlight001</span> 👍（94） 💬（0）<div>这个看着很吃力啊，都没接触过😂</div>2018-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0f/fb/68196d4c.jpg" width="30px"><span>丘壑</span> 👍（49） 💬（7）<div>栈来实现blockqueue，个人感觉比较好的有
方案一：总共3个栈，其中2个写入栈（A、B），1个消费栈栈C（消费数据），但是有1个写入栈是空闲的栈（B），随时等待写入，当消费栈(C)中数据为空的时候，消费线程（await），触发数据转移，原写入栈(A)停止写入，，由空闲栈（B）接受写入的工作，原写入栈(A)中的数据转移到消费栈（C）中，转移完成后继续（sign）继续消费，2个写入栈，1个消费栈优点是：不会堵塞写入，但是消费会有暂停

方案二：总共4个栈，其中2个写入栈（A、B），2个消费栈（C、D）,其中B为空闲的写入栈，D为空闲的消费栈，当消费栈（C）中的数据下降到一定的数量，则触发数据转移，这时候A栈停止写入，由B栈接受写入数据，然后将A栈中的数据转入空闲的消费栈D，当C中的数据消费完了后，则C栈转为空闲，D栈转为激活消费状态，当D栈中的数据消费到一定比例后，重复上面过程，该方案优点即不堵塞写入，也不会造成消费线程暂停


</div>2018-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/b4/33099f97.jpg" width="30px"><span>吕倩</span> 👍（20） 💬（2）<div>老师你好，在读ArrayBlockingQueue源码的时候，发现很多地方都有 final ReentrantLock lock = this.lock; 这样的语句，处于什么原因会将类变量复制一份到局部变量，然后再使用呢？</div>2018-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/9f/f8bc3520.jpg" width="30px"><span>Lighters</span> 👍（14） 💬（0）<div>希望能够增加一些具体的业务使用场景，否则只是单纯的分析，太抽象了
</div>2019-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0f/4f/c75c4889.jpg" width="30px"><span>石头狮子</span> 👍（13） 💬（0）<div>实现课后题过程中把握以下几个维度，
1，数据操作的锁粒度。
2，计数，遍历方式。
3，数据结构空，满时线程的等待方式，有锁或无锁方式。
4，使用离散还是连续的存储结构。</div>2018-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/03/a2/ceb37046.jpg" width="30px"><span>crazyone</span> 👍（8） 💬（0）<div>从上面这些角度，能够理解 ConcurrentLinkedDeque 和 LinkedBlockingQueue 的主要功能区别。  这段应该是 &quot;ConcurrentLinkedDeque 和 LinkedBlockingDeque 的主要功能区别&quot;</div>2018-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d2/c7/14d235bb.jpg" width="30px"><span>猕猴桃 盛哥</span> 👍（8） 💬（2）<div>{
    &quot;test&quot;:[
        [
            89,
            90,
            [
                [
                    1093,
                    709
                ],
                [
                    1056,
                    709
                ]
            ]
        ]
    ]
}

测试题：这个json用java对象怎么表示？</div>2018-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7a/ab/342ec0ca.jpg" width="30px"><span>无呢可称</span> 👍（4） 💬（3）<div>@Jerry银银。用两个栈可以实现fifo的队列

</div>2018-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0f/4f/c75c4889.jpg" width="30px"><span>石头狮子</span> 👍（4） 💬（0）<div>实现课后题过程中把握以下几个维度，
1，数据操作的锁粒度。
2，计数，遍历方式。
3，数据结构空，满时线程的等待方式，有锁或无锁方式。
4，使用离散还是连续的存储结构。</div>2018-06-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIlZ9AObDSXrfSEibY94uyQvMQ4tOvbb7iaQH9H7QQ6ibNaqFKUGq1TboaFpBSLuP0MCcSXvmqHNg0IA/132" width="30px"><span>Geek_8c5f9c</span> 👍（3） 💬（2）<div>fail-fast不是同步容器的行为， fail-safe才是。</div>2020-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/21/3f/409aa5d2.jpg" width="30px"><span>汉彬</span> 👍（3） 💬（0）<div>用栈实现BlockingQueue，我的理解是：栈是LIFO，BlockingQueue是FIFO，因此需要两个栈。take时先把栈A全部入栈到栈B，然后栈B出栈得到目标元素；put时把栈B全部入栈到栈A，然后栈A再入栈目标元素。相当于倒序一下。

不知道理解对不对，请老师指出。</div>2018-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（2） 💬（1）<div>真好</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6e/8e/5d309a85.jpg" width="30px"><span>拯救地球好累</span> 👍（2） 💬（0）<div>从几个问题来学习新的框架或工具：
1.用来解决什么问题？常见的应用场景有哪些？
2.jdk内部或第三方框架在什么场景中如何运用？
3.有哪几种类似的实现或工具？它们之间有何区别？在结构层次上有何联系？
4.从源码上看关键代码有哪几个地方？</div>2019-05-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIyqjqjTlaiavQb1I7d5au4A3mojticTXgBEu6picAv3qS7f1jhdq4bSS8mJpic1zWNhxaQWNPfYkQF0w/132" width="30px"><span>杭州</span> 👍（2） 💬（0）<div>杨老师你好，我碰到个问题： 200个线程池 阻塞读take（）linkblockingqueue队列，偶尔会发现线程池中的阻塞线程cpu突高。jstack看了有很多的lock。怀疑是池程离开线程池去干别的活，干了一半又回到线程池中，出现死锁表现cpu高。不知道是什么这个原因，不知道怎么解决？</div>2018-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2b/2b/bebf6eed.jpg" width="30px"><span>酱了个油</span> 👍（2） 💬（0）<div>队列的一个问题是不能持久化、不能做到分布式，有时候考虑到系统可靠性，使用的机会不多。杨老师可以给一些使用队列的例子吗？</div>2018-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/38/f1/7f65979c.jpg" width="30px"><span>Gen幸福旅程iuS</span> 👍（1） 💬（0）<div>public class I20StackToBQ {

    static final Stack&lt;Object&gt; inStack = new Stack&lt;&gt;();

    static final Stack&lt;Object&gt; outStack = new Stack&lt;&gt;();

    static Object popElement() {
        if (!outStack.empty()) {
            return outStack.pop();
        }
        do {
            outStack.push(inStack.pop());
        } while (!inStack.empty());

        return outStack.pop();
    }

    static void popAllElement() {
        do {
            System.out.println(&quot;all&quot; + &quot;-&quot; + outStack.pop());
        } while (!outStack.empty());
        do {
            outStack.push(inStack.pop());
        } while (!inStack.empty());
        do {
            System.out.println(&quot;all&quot; + &quot;-&quot; + outStack.pop());
        } while (!outStack.empty());
    }

    static void putElement(Object element) {
        inStack.push(element);
    }


    public static void main(String[] args) {
        I20StackToBQ.putElement(&quot;one&quot;);
        I20StackToBQ.putElement(&quot;two&quot;);
        I20StackToBQ.putElement(&quot;three&quot;);
        System.out.println(I20StackToBQ.popElement());
        I20StackToBQ.putElement(&quot;four&quot;);
        I20StackToBQ.popAllElement();
    }
}
</div>2023-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9e/df/ac5c60b5.jpg" width="30px"><span>jiahua</span> 👍（1） 💬（0）<div>两个栈A和B, 一直向A中写，从B中读，B中没有时，把当前A中的放到B中</div>2020-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/29/629d9bb0.jpg" width="30px"><span>天王</span> 👍（1） 💬（0）<div>20 ConcurrentLinkedQueue和LinkedBlockingQueue有什么区别 1 Java.util.concurrent包下面的所有容器都叫并发容器，concurrent开头的叫并发容器，concurrent基于lock-free模式，在多线程场景，能提供较大的吞吐量 ，LinkedBlocking是基于锁，提供了BlockingQueue的等待方法 2 线程安全容器大概可以分为concurrent*，CopyOnWrite和Blocking等三类，CopyOnWrite需要拷贝一份数据，在拷贝数据上修改，开销比较大，常见的容器，有比较强的一致性，如果遍历过程发生修改，会抛出ConcurrentModificationException，而Concurrent*容器可以继续遍历。3 Blocking同步容器，需要等待，以代码为例 用BlockingQueue去实现生产者消费者，不用自己手工去实现轮询，条件判断等逻辑。</div>2020-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/4e/b81969fa.jpg" width="30px"><span>南北少卿</span> 👍（1） 💬（1）<div>杨老师,你好,最近我debug过ConcurrentLinkedQueue的源码,第一次添加元素的时候,为什么head指向添加的元素,而tail指向自己,始终搞不明白,经过p.casNext(null, newNode)操作之后,这中间的变化到底是怎么回事?您能解答下吗?望指点.我的微信号:LEE794112629</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（1） 💬（1）<div>用栈来实现BlockingQueue，换句话是说，用先进后出的数据结构来实现先进先出的数据结构，怎么感觉听起来不那么对劲呢？请指点</div>2018-06-22</li><br/><li><img src="" width="30px"><span>Geek_6ce7fa</span> 👍（0） 💬（1）<div>PriorityBlockingQueue是有界队列吧</div>2021-06-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJAnje12Sebss1BwgLF48Wk57zaMtMSWdStbC6R7l0ssCev0ddLPYd2QqGXBmpfNL89NtahYKVkVg/132" width="30px"><span>Geek_154f14</span> 👍（0） 💬（0）<div>一般情况下用linked确实好点，他有俩把锁，粒度细效率更高
</div>2020-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/36/47/8e80082c.jpg" width="30px"><span>大成尊者</span> 👍（0） 💬（1）<div>指定某种结构，比如栈，用它实现一个 BlockingQueue，实现思路是怎样的呢？
答：不能实现。因为栈遵循的是先进后出，你上面说的不管是ArrayBlockingQueue还是LinkedBlockingQueue，都是支持先进先出的，栈这个数据结构就不支持先进先出。</div>2020-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/5c/a3d42cdb.jpg" width="30px"><span>ilovealt</span> 👍（0） 💬（1）<div>这个有点吃力，不懂的很多，看来我我还是一个菜鸟啊。</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/61/c2/1da88a93.jpg" width="30px"><span>今天</span> 👍（0） 💬（0）<div>并发都有消耗，就是看如何更适合的降低</div>2020-03-22</li><br/>
</ul>