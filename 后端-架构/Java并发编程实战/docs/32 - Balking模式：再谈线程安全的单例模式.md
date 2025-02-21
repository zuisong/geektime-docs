上一篇文章中，我们提到可以用“多线程版本的if”来理解Guarded Suspension模式，不同于单线程中的if，这个“多线程版本的if”是需要等待的，而且还很执着，必须要等到条件为真。但很显然这个世界，不是所有场景都需要这么执着，有时候我们还需要快速放弃。

需要快速放弃的一个最常见的例子是各种编辑器提供的自动保存功能。自动保存功能的实现逻辑一般都是隔一定时间自动执行存盘操作，存盘操作的前提是文件做过修改，如果文件没有执行过修改操作，就需要快速放弃存盘操作。下面的示例代码将自动保存功能代码化了，很显然AutoSaveEditor这个类不是线程安全的，因为对共享变量changed的读写没有使用同步，那如何保证AutoSaveEditor的线程安全性呢？

```
class AutoSaveEditor{
  //文件是否被修改过
  boolean changed=false;
  //定时任务线程池
  ScheduledExecutorService ses = 
    Executors.newSingleThreadScheduledExecutor();
  //定时执行自动保存
  void startAutoSave(){
    ses.scheduleWithFixedDelay(()->{
      autoSave();
    }, 5, 5, TimeUnit.SECONDS);  
  }
  //自动存盘操作
  void autoSave(){
    if (!changed) {
      return;
    }
    changed = false;
    //执行存盘操作
    //省略且实现
    this.execSave();
  }
  //编辑操作
  void edit(){
    //省略编辑逻辑
    ......
    changed = true;
  }
}
```

解决这个问题相信你一定手到擒来了：读写共享变量changed的方法autoSave()和edit()都加互斥锁就可以了。这样做虽然简单，但是性能很差，原因是锁的范围太大了。那我们可以将锁的范围缩小，只在读写共享变量changed的地方加锁，实现代码如下所示。

```
//自动存盘操作
void autoSave(){
  synchronized(this){
    if (!changed) {
      return;
    }
    changed = false;
  }
  //执行存盘操作
  //省略且实现
  this.execSave();
}
//编辑操作
void edit(){
  //省略编辑逻辑
  ......
  synchronized(this){
    changed = true;
  }
}  
```

如果你深入地分析一下这个示例程序，你会发现，示例中的共享变量是一个状态变量，业务逻辑依赖于这个状态变量的状态：当状态满足某个条件时，执行某个业务逻辑，其本质其实不过就是一个if而已，放到多线程场景里，就是一种“多线程版本的if”。这种“多线程版本的if”的应用场景还是很多的，所以也有人把它总结成了一种设计模式，叫做**Balking模式**。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKlwpFM3tkeG15YqyJTYWkfqkdmro9POq6SicYm57TaEFDOUZCXjoe0Z0Iz6UibGQqic3icJRsHdFzibtw/132" width="30px"><span>zero</span> 👍（58） 💬（3）<div>是有问题的，volatile关键字只能保证可见性，无法保证原子性和互斥性。所以calc方法有可能被重复执行。</div>2019-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/95/a3/744995c1.jpg" width="30px"><span>LeonHan</span> 👍（50） 💬（1）<div>思考题代码相当于：
if（intied == false） {  &#47;&#47; 1
     inited = true;          &#47;&#47;2
     count = calc()
}

可能有多条线程同时到1的位置，判断到inited为false，都进入2执行。
解决方案：
（1）加锁保护临界区
（2） AtomicBoolean.compareAndSet(false, true)
</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3b/ad/31193b83.jpg" width="30px"><span>孙志强</span> 👍（18） 💬（1）<div>inited变量需要使用CAS的方式进行赋值，赋值失败就return，保证只有一个线程可以修改inited变量。</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/11/ac/9cc5e692.jpg" width="30px"><span>Corner</span> 👍（17） 💬（4）<div>最好就不要单独使用volatile防止产生线程安全问题。因为变量的读写是两个操作，和我们的直觉不一样，很容易出问题。老师的那个volatile就没有问题吗？如果一个线程修改了路由表，此时定时器任务判断共享变量为true，在将其修改为false之前，此时另一个线程又修改了路由表，然后定时任务继续执行会将其修改为false，这就出现问题了。最后还是要在autoSave方法上做同步的。</div>2019-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/39/bd/74059999.jpg" width="30px"><span>岥羽</span> 👍（5） 💬（2）<div>老师，自动保存路由表用 Balking 模式的volatile方式实现中，为什么对共享变量 changed 和 rt 的写操作不存在原子性的要求？</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（5） 💬（1）<div>volative修饰的属性。我见过在方法中。用局部变量接收该属性值，方法后续的操作都基于该局部变量。这样是不是就不再有volative的特性了？性能虽然提高了，毕竟能走缓存和编译优化了。但是就像上例双重检查的场景。这么个操作就依旧会有空指针异常的可能。请问老师我理解对吗。</div>2019-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（5） 💬（1）<div>回答问题：
有问题，volatile不能保证原子性，题目要求只需计算一次Count，所以需要对共享变量inited加锁保护。

疑问：
public class RouterTable 类中AutoSave方法同一时刻只有一个线程调用，而Remove和Add方法也是要求使用方单线程访问吗？在实际开发中一般采用什么方式达成这种约定呢？</div>2019-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/16/fb/c8a52099.jpg" width="30px"><span>热台</span> 👍（3） 💬（1）<div>回答问题
1，cal（）可能被执行多次
2.  也可能cal（）执行结束前，count就被使用

解决方法
inited 赋值和cal（）执行放在一个同步块中，并增加双重check</div>2019-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/a5/71358d7b.jpg" width="30px"><span>J.M.Liu</span> 👍（3） 💬（1）<div>有问题，存在竞态条件</div>2019-05-11</li><br/><li><img src="" width="30px"><span>geoxs</span> 👍（0） 💬（1）<div>我有个问题，如果需求不要求只执行一次呢，比如计算很简单，耗费资源不大，多计算几次是可以接受的，可不可以这样写，有没有并发问题呢，甚至我把volitale关键字去掉可不可以呢？</div>2020-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ff/0a/12faa44e.jpg" width="30px"><span>晓杰</span> 👍（0） 💬（2）<div>在微服务的场景下，synchornize应该不适用了吧</div>2019-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5f/73/bb3dc468.jpg" width="30px"><span>拒绝</span> 👍（0） 💬（1）<div>老师，volatile只能保证变量的可见性，在多线程下，发生线程切换会都读取到变量为false，则计算count方法被调用多次，对吗？</div>2019-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/37/8e/cf0b4575.jpg" width="30px"><span>郑晨Cc</span> 👍（10） 💬（1）<div>第8行 inited = true；改成cas操作
失败直接return。成功继续执行cal方法</div>2019-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/33/9f/8dbd9558.jpg" width="30px"><span>逆流的鱼</span> 👍（5） 💬（0）<div>这两个模式怎么这么违和，突兀，虎头虎脑的</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/5e/81/82709d6e.jpg" width="30px"><span>码小呆</span> 👍（0） 💬（0）<div>感觉需要加锁,无法保证原子性</div>2022-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f3/de/c6509355.jpg" width="30px"><span>花蛋壳</span> 👍（0） 💬（1）<div>把代码 inited = true; 放在 init方法第一行执行可不可行？</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/f2/26/a8ac6b42.jpg" width="30px"><span>听风有信</span> 👍（0） 💬（0）<div>AutoSaveEditor是不是也可以用volatile保证可见性就行了？</div>2021-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/b6/46a5bbf3.jpg" width="30px"><span>俺能学个啥</span> 👍（0） 💬（0）<div>多个线程同时执行完if判断后进入到inited=true赋值操作，这一步无法确认单个线程通过，可以对if判断部分加锁</div>2021-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/f4/e277325d.jpg" width="30px"><span>bin.chen</span> 👍（0） 💬（0）<div>1.计算count值会造成执行多次
解决方案1:不使用volatile 直接使用锁解决
解决方案2:设置inited=true的地方使用CAS类解决多次重复操作执行计算的问题</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/dc/e2/a3abd320.jpg" width="30px"><span>Just</span> 👍（0） 💬（0）<div>1）并发情况下，calc会被执行多次
2）count的值有可能不正确</div>2020-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/5c/86606d9c.jpg" width="30px"><span>湮汐</span> 👍（0） 💬（1）<div>用一个全局变量，去控制业务代码的流程。但是要注意这个业务代码的流程会不会存在“并发”，如果不存在并发，可以只用volatile；如果存在，那么必须要用管程控制原子性！</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/82/3d/356fc3d6.jpg" width="30px"><span>忆水寒</span> 👍（0） 💬（0）<div>肯定有问题的，最简单的可以加个synchronize解决。就像上面InitTest类初始化一次一样解决。</div>2020-04-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI2vn8hyjICTCletGs0omz28lhriaZKX2XX9icYzAEon2IEoRnlXqyOia2bEPP0j7T6xexTnr77JJic8w/132" width="30px"><span>Geek_c22199</span> 👍（0） 💬（0）<div>路由表的例子中不加锁的话就不能保证change=true会写入成功，写入不成功就可能会丢失一部分改变的路由表</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/74/21/6c64afa9.jpg" width="30px"><span>奔跑的猪</span> 👍（0） 💬（0）<div>volatile关键字只能保证可见性，无法保证互斥性，所以思考题中volatile变量的正确使用姿势如下：
public class Test {

    private volatile boolean inited = false;

    @Getter
    private int count = 0;

    public void init() {
        if (inited) {
            return;
        }

        &#47;&#47; 写volatile变量前先执行一段空循环，增加读到inited为false的并发几率
        IntStream.range(0, Integer.MAX_VALUE).forEach(i -&gt; { });
        &#47;&#47; 正确用法1：写volatile变量前先通过CAS判断是否可以写成功
        if (!new AtomicBoolean(inited).compareAndSet(false, true)) {
            return;
        }
        inited = true;
        &#47;&#47; 正确用法2：写volatile变量时加锁，并在写之前做双重Check
&#47;&#47;        synchronized (this) {
&#47;&#47;            if (inited) {
&#47;&#47;                return;
&#47;&#47;            }
&#47;&#47;            inited = true;
&#47;&#47;        }
        try {
            calc();
        } catch (Exception e) {
            inited = false;
            e.printStackTrace();
        }
    }

    private void calc() {
        count = count + 1;
    }

    public static void main(String[] args) throws InterruptedException {
        Test test = new Test();
        int taskTotal = 10000;
        CountDownLatch counter = new CountDownLatch(taskTotal);
        ExecutorService exec = Executors.newFixedThreadPool(5);
        for (int i = 0; i &lt; taskTotal; i++) {
            exec.submit(() -&gt; {
                test.init();
                counter.countDown();
            });
        }
        counter.await();
        System.out.println(&quot;count = &quot; + test.getCount());
        exec.shutdown();
    }
}</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b0/65/90387745.jpg" width="30px"><span>Mr.wang</span> 👍（0） 💬（0）<div>Balking模式需要保持互斥性，这里没有保证互斥，只是有使用voliate关键字，没法保证原子性和一致性。</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/19/0a3fe8c1.jpg" width="30px"><span>Evan</span> 👍（0） 💬（0）<div>从表面上看，这段代码的性能还可以了，但从安全性方面考虑多线程会出现Data Race，也就没有办法原子性。 而volatiled只解决了可见性问题</div>2020-03-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoViaN0hP07cXOl7vOIvHPu7DZ3wxHBz4iaLVEqG1TFfiagm1wUaiczbCyicwib7oDWw0vD4cXg9eZ0Okqg/132" width="30px"><span>韭菜河子</span> 👍（0） 💬（0）<div>Volatile只能保证可见性，无法保证互斥性</div>2019-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d1/29/1b1234ed.jpg" width="30px"><span>DFighting</span> 👍（0） 💬（0）<div>volatile没办法保证操作的原子性，也就是在第一个线程执行inited=true时可能会发生时间片的切换，导致下一个线程在判断是否初始化的时候继续执行calc()操作，也就是说没办法保证calc()的唯一性，对比老师给的代码，应该为整个方法加上synchronized以达到只计算一次calc()的目的</div>2019-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/06/73/4d6b1f09.jpg" width="30px"><span>熊熊周周</span> 👍（0） 💬（1）<div>inited = true;
除非代码所工作的操作系统平台环境或者java官方指定这个操作是原子性操作，线程安全的。我们不应该把它当做原子性的操作，线程安全性的操作。
解决了原始数据类型赋值是否是原子性操作的疑问</div>2019-06-21</li><br/><li><img src="" width="30px"><span>奇奇</span> 👍（0） 💬（0）<div>课后思考题应该是!inited 代码是错的</div>2019-06-05</li><br/>
</ul>