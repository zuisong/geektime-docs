Semaphore，现在普遍翻译为“信号量”，以前也曾被翻译成“信号灯”，因为类似现实生活里的红绿灯，车辆能不能通行，要看是不是绿灯。同样，在编程世界里，线程能不能执行，也要看信号量是不是允许。

信号量是由大名鼎鼎的计算机科学家迪杰斯特拉（Dijkstra）于1965年提出，在这之后的15年，信号量一直都是并发编程领域的终结者，直到1980年管程被提出来，我们才有了第二选择。目前几乎所有支持并发编程的语言都支持信号量机制，所以学好信号量还是很有必要的。

下面我们首先介绍信号量模型，之后介绍如何使用信号量，最后我们再用信号量来实现一个限流器。

## 信号量模型

信号量模型还是很简单的，可以简单概括为：**一个计数器，一个等待队列，三个方法**。在信号量模型里，计数器和等待队列对外是透明的，所以只能通过信号量模型提供的三个方法来访问它们，这三个方法分别是：init()、down()和up()。你可以结合下图来形象化地理解。

![](https://static001.geekbang.org/resource/image/6d/5c/6dfeeb9180ff3e038478f2a7dccc9b5c.png?wh=1142%2A566)

信号量模型图

这三个方法详细的语义具体如下所示。

- init()：设置计数器的初始值。
- down()：计数器的值减1；如果此时计数器的值小于0，则当前线程将被阻塞，否则当前线程可以继续执行。
- up()：计数器的值加1；如果此时计数器的值小于或者等于0，则唤醒等待队列中的一个线程，并将其从等待队列中移除。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/50/da/ed4803cb.jpg" width="30px"><span>CCC</span> 👍（273） 💬（8）<div>我理解的和管程相比，信号量可以实现的独特功能就是同时允许多个线程进入临界区，但是信号量不能做的就是同时唤醒多个线程去争抢锁，只能唤醒一个阻塞中的线程，而且信号量模型是没有Condition的概念的，即阻塞线程被醒了直接就运行了而不会去检查此时临界条件是否已经不满足了，基于此考虑信号量模型才会设计出只能让一个线程被唤醒，否则就会出现因为缺少Condition检查而带来的线程安全问题。正因为缺失了Condition，所以用信号量来实现阻塞队列就很麻烦，因为要自己实现类似Condition的逻辑。</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/f7/3a493bec.jpg" width="30px"><span>老杨同志</span> 👍（171） 💬（7）<div>需要用线程安全的vector，因为信号量支持多个线程进入临界区，执行list的add和remove方法时可能是多线程并发执行</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/f9/1f0a9665.jpg" width="30px"><span>任大鹏</span> 👍（54） 💬（3）<div>有同学认为up()中的判断条件应该&gt;=0，我觉得有可能理解为生产者-消费者模式中的生产者了。可以这么想，&gt;0就意味着没有阻塞的线程了，所以只有&lt;=0的情况才需要唤醒一个等待的线程。其实down()和up()是成对出现的，并且是先调用down()获得锁，处理完成再调用up()释放锁，如果信号量初始值为1，应该是不会出现&gt;0的情况的，除非故意调先用up()，这也失去了信号量本身的意义了。不知道我理解的对不对。</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4b/e4/abb7bfe3.jpg" width="30px"><span>Alvan</span> 👍（30） 💬（5）<div>很多人对up()方法的计数器count&lt;=0不理解，可以看下这里：
1、反证法验证一下，假如一个线程先执行down()操作，那么此时count的值是0，接着这个线程执行up()操作，此时count的值是1，如果count应该是大于等于0，那么应该唤醒其他线程，可是此时并没有线程在睡眠呀，count的值不应该是大于等于0。
2、假如一个线程t1执行down()操作，此时count = 0，然后t1被中断，另外的线程t2执行down()操作，此时count=-1，t2阻塞睡眠，另外的线程t3执行down()操作，count=-2，t3也睡眠。count=-2 说明有两个线程在睡眠，接着t1执行up() 操作，此时count=-1，小于等于0，唤醒t2或者t3其中一个线程，假如计数器count是大于等于0才唤醒其他线程，这明显是不对的。</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4d/87/57236a2d.jpg" width="30px"><span>木卫六</span> 👍（21） 💬（4）<div>换ArrayList是不行的，临界区内可能存在多个线程来执行remove操作，出现不可预知的后果。

对于chaos同学说return之前释放的问题，我觉得可以这么理解：return的是执行后的结果，而不是“执行”。所以顺序应该是这样的：1acquire；2apply；3finally release；4return2的结果</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e7/56/c72997f3.jpg" width="30px"><span>缪文</span> 👍（16） 💬（1）<div>这个限流器实际上限的是并发量，也就是同时允许多少个请求通过，如果限制每秒请求数，不是这个实现的吧</div>2019-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/05/4c/558b0012.jpg" width="30px"><span>刘彦辉</span> 👍（10） 💬（3）<div>假如有3个线程，线程A、B、C，信号量计数器为1，线程A执行down的时候变为0，不阻塞；线程B执行down，变为-1，阻塞；线程C执行down变为-2，阻塞。当线程A执行完，调用up后，变为-1，此时唤醒一个线程，那么请问唤醒之后的操作呢？唤醒之后直接就执行了业务代码了？还是唤醒之后还需要去先执行down？按分析的话应该不能执行down了，如果执行down的话，计数器变为-2，还会阻塞，所以是不是这块儿的阻塞和唤醒也是用的wait和notify呢？唤醒之后，从阻塞的代码开始继续执行，这样就可以成功执行下去了。麻烦老师解答一下哈，谢谢。</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/ef/494f56c3.jpg" width="30px"><span>crazypokerk</span> 👍（9） 💬（4）<div>老师，那个计数器中得s.acquire()是需要捕获异常的。
static int count;
    static final Semaphore s = new Semaphore(1);

    static void addOne() throws InterruptedException {
        s.acquire();
        try {
            count += 1;
        }finally {
            s.release();
        }
    }</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fe/b5/df0f658f.jpg" width="30px"><span>ken</span> 👍（7） 💬（2）<div>
public class Food {

    public String name;

    private long warmTime;

    public Food(String name, long warmTime) {
        this.name = name;
        this.warmTime = warmTime;
    }

    public String getName() {
        return name;
    }

    public long getWarmTime() {
        return warmTime;
    }
}



public class MicrowaveOven {

    public String name;

    public MicrowaveOven(String name) {
        this.name = name;
    }

    public Food warm(Food food) {
        long second = food.getWarmTime() * 1000;
        try {
            Thread.sleep(second);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println(String.format(&quot;%s warm %s %d seconds food.&quot;, name,food.getName() ,food.getWarmTime()));
        return food;
    }

    public String getName() {
        return name;
    }
}
public class MicrowaveOvenPool {

    private List&lt;MicrowaveOven&gt; microwaveOvens;

    private Semaphore semaphore;

    public MicrowaveOvenPool(int size,@NotNull List&lt;MicrowaveOven&gt; microwaveOvens) {
        this.microwaveOvens = new Vector&lt;&gt;(microwaveOvens);
        this.semaphore = new Semaphore(size);
    }
    public Food exec(Function&lt;MicrowaveOven, Food&gt; func) {
        MicrowaveOven microwaveOven = null;
        try{
            semaphore.acquire();
            microwaveOven = microwaveOvens.remove(0);
            return func.apply(microwaveOven);
        }catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            microwaveOvens.add(microwaveOven);
            semaphore.release();
        }
        return null;
    }

}
</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/01/e7/091804b7.jpg" width="30px"><span>长眉_张永</span> 👍（6） 💬（2）<div>对于进入的多个线程资源之间，如果有公用的信息的话，是否还需要加锁操作呢？</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e5/a5/fae40ac3.jpg" width="30px"><span>倚梦流</span> 👍（5） 💬（5）<div>限流器，基于老师的代码，自己手动完善了一下。
package com.thread.demo;

import java.util.List;
import java.util.Vector;
import java.util.concurrent.Semaphore;
import java.util.function.Function;

public class ObjPool&lt;T,R&gt; {
    private List&lt;T&gt; pool;
    &#47;&#47;使用信号量实现限流器
    private final Semaphore semaphore;


    ObjPool(T[] tArray){
        pool=new Vector&lt;T&gt;(){};
        int size=tArray.length;
        for(int i=0;i&lt;size;i++){
            pool.add(tArray[i]);
        }
        semaphore=new Semaphore(size);
    }

    R exec(Function&lt;T,R&gt; func) throws InterruptedException {
        T t=null;
        semaphore.acquire();
        try{
            t=pool.remove(0);
            return func.apply(t);
        }finally {
            pool.add(t);
            semaphore.release();
        }
    }

    public static void main(String[] args){
        String[] messages=new String[10];
        for(int i=0;i&lt;10;i++){
            messages[i]=&quot;obj_&quot;+i;
        }
        ObjPool&lt;String,String&gt; pool=new ObjPool&lt;&gt;(messages );

        for(int i=0;i&lt;100;i++){
            Thread thread=new Thread(() -&gt;{
                try {
                    pool.exec(t -&gt; {
                        System.out.println(&quot;当前线程id:&quot;+Thread.currentThread().getId()+&quot;,当前获取到的对象：&quot;+t);
                        return  t;
                    });
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            });
            thread.start();
            try {
                thread.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

    }


}
</div>2019-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/61/94/713b38ef.jpg" width="30px"><span>小和尚笨南北</span> 👍（5） 💬（6）<div>semaphore底层通过AQS实现，AQS内部通过一个volatile变量间接实现同步。
根据happen-before原则的volatile规则和传递性规则。使用arraylist也不会发生线程安全问题。</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b2/c5/6ae0be56.jpg" width="30px"><span>木偶人King</span> 👍（4） 💬（1）<div>ObjPool(int size, T t){
    pool = new Vector&lt;T&gt;(){};
    for(int i=0; i&lt;size; i++){
      pool.add(t);
    }
    sem = new Semaphore(size);
  }
 &#47;&#47;--------------------------------

老师这里pool.add(t)  一直循环添加的是同一个引用对象。没太明白。 为什么不是添加不同的t </div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（3） 💬（2）<div>用初始化为1的Semaphore和管程来单单控制线程安全，哪个更有优势？为啥java不直接用信号量来实现互斥?</div>2019-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8a/f3/7c89d00e.jpg" width="30px"><span>Presley</span> 👍（3） 💬（1）<div>进入临界区的N个线程不安全。add&#47;remove都是不安全的。拿remove举例, ArrayList remove()源码：
public E remove(int index) {
        rangeCheck(index);

        modCount++;
       
        &#47;&#47; 假设连个线程 t1,t2都执行到这一步，t1 让出cpu,t2执行
        E oldValue = elementData(index);
        &#47;&#47; 到这步,t1继续执行，这时t1,t2拿到的oldValue是一样的，两个线程能拿到同一个对象，明显线程不安全啊

        int numMoved = size - index - 1;
        if (numMoved &gt; 0)
            System.arraycopy(elementData, index+1, elementData, index,
                             numMoved);
        elementData[--size] = null; &#47;&#47; clear to let GC do its work

        return oldValue;
    }
</div>2019-04-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/bvj76PmeUvW8kokyu91IZWuRATKmabibDWbzAj2TajeEic7WvKCJOLaOh6jibEmdQ36EO3sBUZ0HibAiapsrZo64U8w/132" width="30px"><span>梦倚栏杆</span> 👍（2） 💬（1）<div>如果一个线程一直在睡眠不被唤醒呢？这个线程会经过一定时间自己消亡吗？</div>2019-12-03</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqLcWH3mSPmhjrs1aGL4b3TqI7xDqWWibM4nYFrRlp0z7FNSWaJz0mqovrgIA7ibmrPt8zRScSfRaqQ/132" width="30px"><span>易儿易</span> 👍（2） 💬（1）<div>计数器值小于0，线程会阻塞并进入队列，如果计数器值大于初始值呢？我代码测试了一下，执行起来没有什么问题，但总觉得有些不太靠谱……请问老师：信号量的使用规范是不是得要求acquire()release()必须成对出现并保证release()顺利执行？否则独立的acquire()就能使计数器值大于初始值，可能会引入BUG（导致线程数多余池中限定的数量），不过这个也有好处，貌似也可以起到动态调整semaphore初始值的作用。老师我没有并发开发经验，只是根据专栏内有限内容思考，不知道我的想法对不对，有没有实际意义。请指教~</div>2019-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（1） 💬（2）<div>思考题：
Vector换成ArrayList会有线程安全问题，问题出现在pool.remove()和pool.add()方法调用时。</div>2020-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/66/bd/bd5d503e.jpg" width="30px"><span>杨鹏程baci</span> 👍（1） 💬（1）<div>老师，这一节感觉有些内容没有讲全，semaphore中线程的等待唤醒机制是不是还是用到了wait和siganal方法？</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/db/80/6b7629d7.jpg" width="30px"><span>roaming</span> 👍（1） 💬（1）<div>老师，LockSupport用的也是信号量模型，对吗？专栏里没有提到这个工具类，是不常用吗？</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（1） 💬（1）<div>我只想说，真的讲的很赞！

清明节后到现在一直在忙其他的，今天早上才补了一节，真的很赞！ 

谢谢老师解开了我一直以来的疑惑，谢谢您！</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/12/e1/6d0114fe.jpg" width="30px"><span>顾言</span> 👍（0） 💬（1）<div>Semaphore 多于多个临界区的互斥感觉没有管程那么方便，不知道老师有没有更好的思路？</div>2022-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b3/d8/c56e0f0b.jpg" width="30px"><span>宋柯仰</span> 👍（0） 💬（1）<div>老师，信号量初始值设置为1也不可以直接作为锁来使用的吧，它保证不了被保护资源的可见性吧？</div>2021-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/60/91/b17c007b.jpg" width="30px"><span>Eduardo Falaschi</span> 👍（0） 💬（1）<div>在调用一个第三方的支持并发量不大的系统时，需要限流</div>2020-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/34/47/6d212e42.jpg" width="30px"><span>Destiny</span> 👍（0） 💬（3）<div>老师好，有一个问题想问一下，如果部署服务的机器是集群，那么这个Semaphore的限流是不是就不能用了？</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ed/e6/75a32708.jpg" width="30px"><span>日拱一兵</span> 👍（0） 💬（1）<div>老师，信号量是允许多个线程进入临界区，如果临界区内有共享变量，那么这个变量也是要加锁的吧，比如 count 计数</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/56/c6/0b449bc6.jpg" width="30px"><span>斐波那契</span> 👍（0） 💬（1）<div>老师 我想问一下 在那个对象池例子中 是不是装入的对象是不可变的 不然在调用func的时候多线程可能会导致结果错误？</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d9/93/098e5ef5.jpg" width="30px"><span>海鸿</span> 👍（0） 💬（2）<div>Semaphore 可以允许多个线程访问一个临界区。像池资源那样，进入之后还是得控制资源的获取啊，不然还是会产生并发问题啊，不是吗？</div>2019-04-05</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqLcWH3mSPmhjrs1aGL4b3TqI7xDqWWibM4nYFrRlp0z7FNSWaJz0mqovrgIA7ibmrPt8zRScSfRaqQ/132" width="30px"><span>易儿易</span> 👍（0） 💬（1）<div>限流器，平时自己开发的时候，是不是简单使用阻塞队列就可以了呢？和信号量比起来有什么差别吗？</div>2019-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e0/24/4529f2a4.jpg" width="30px"><span>WP</span> 👍（0） 💬（1）<div>我好像知道原因了   finally里面的回收和计数器顺序调整下就对了   我错了~~</div>2019-04-04</li><br/>
</ul>