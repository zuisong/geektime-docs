你好，我是郭屹。今天我们继续手写MiniTomcat。

学完前几节课的内容之后，现在我们已经做到接口满足Servlet规范，而且功能模块拆分成了Connector和Processor两部分，它们各司其职，一个负责网络连接，一个负责Servlet调用处理。

但现在这个Server的运行模式是，一个Connector服务于一个Processor，而且每次创建Processor的时候都是重新实例化一个新的对象，Processor还不支持多线程处理，所以我们在HttpServer性能方面还有提升的空间。

这节课，我们计划引入池的概念，增强Processor的复用性，同时将Processor异步化，支持一个Connector服务于多个Processor。

![](https://static001.geekbang.org/resource/image/15/c6/1534805c6edf2fb2c2493d34792bbac6.png?wh=2212x944)

## 项目结构

这节课，我们只针对原有的HttpConnector和HttpProcessor类进行改造，所以项目结构和maven引入依赖保持不变，还是延续下面的结构和配置。

```plain
MiniTomcat
├─ src
│  ├─ main
│  │  ├─ java
│  │  │  ├─ server
│  │  │  │  ├─ HttpConnector.java
│  │  │  │  ├─ HttpProcessor.java
│  │  │  │  ├─ HttpServer.java
│  │  │  │  ├─ Request.java
│  │  │  │  ├─ Response.java
│  │  │  │  ├─ ServletProcessor.java
│  │  │  │  ├─ StatisResourceProcessor.java
│  │  ├─ resources
│  ├─ test
│  │  ├─ java
│  │  │  ├─ test
│  │  │  │  ├─ HelloServlet.java
│  │  ├─ resources
├─ webroot
│  ├─ test
│  │  ├─ HelloServlet.class
│  ├─ hello.txt
├─ pom.xml
```
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/83/af/1cb42cd3.jpg" width="30px"><span>马以</span> 👍（5） 💬（4）<div>思考题：tomcat的线程池模型和JDK自带线程池模型在核心线程池用完后的实现方式上是不同的；JDK的线程池在达到核心线程池数量后，后续的请求会进入到等待队列（微观上看属于阻塞），因为tomcat作为servlet服务请求，本质上只能并发处理有限个（核心线程数）的并发数，这显然是不合理的；所以tomcat的线程池模型是达到核心线程池后会继续启动新线程处理请求，直到达到最大线程数；</div>2024-01-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/kgFgg4b6yribq8tSqAht0383fzoGSG9COPiaicLMzbdouGBrtJehiboqnJbbAiaNEtib1wYM9wAlAvCTZFUfYQDaElBA/132" width="30px"><span>Geek_ac5e30</span> 👍（4） 💬（3）<div>这里 available 变量是否使用 volatile 修饰会好一些呢？这里涉及到两个线程之间的可见性问题</div>2024-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1e/cf/97cd8be1.jpg" width="30px"><span>so long</span> 👍（2） 💬（1）<div>jdk线程池，在并发数超过核心线程数后，会先将请求任务添加到队列中，而不是创建新的线程处理请求任务，所以会存在一定的延迟</div>2023-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/03/99/d7737b19.jpg" width="30px"><span>像少年样飞驰</span> 👍（1） 💬（1）<div>这里面线程同步机制需要这样写么？ 直接参考线程池的设计，用一个阻塞队列是不是就可以了？ 本质上还是一个生产和消费的模型吧</div>2023-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（4）<div>请教老师几个问题：
Q1：用notifyAll唤醒所有线程，不对吧。
假如有5个线程，connector同时启动这5个线程，5个线程处于wait状态。假设此时来了一个连接请求，由其中的一个线程A处理，那么，connector应该只唤醒这线程A吧。用notifyall会唤醒全部5个线程，难道5个线程处理同一个请求吗？

Q2：recycle方法有多线程问题吗？
假设有5个线程在处理5个请求，这5个线程都会调用recycle方法，此时会存在并发问题吗？
Q3：线程池的大小一般为多大？
有经验公式吗？</div>2023-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/73/f7/d7581b65.jpg" width="30px"><span>无心</span> 👍（0） 💬（2）<div>avaliable的 ture 和 false 语意是不是反了</div>2024-03-09</li><br/><li><img src="" width="30px"><span>Geek_b7bd01</span> 👍（0） 💬（2）<div>为什么connector调用processor.assign()方法，这样不会导致connector线程进行等待吗？为何不直接将任务丢给processor。</div>2024-01-31</li><br/><li><img src="" width="30px"><span>Geek_b7bd01</span> 👍（0） 💬（1）<div>这样connector不是必须得等待processor执行完成之后才能继续往下走吗，不影响效率吗？</div>2024-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/31/05/9028e9ac.jpg" width="30px"><span>ctt</span> 👍（0） 💬（1）<div> HttpProcessor initprocessor = new HttpProcessor();       
 processors.push(initprocessor);        
curProcessors++;        
return ((HttpProcessor) processors.pop());    请问这段代码为什么push完就立即pop了呢</div>2023-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0b/5a/453ad411.jpg" width="30px"><span>C.</span> 👍（0） 💬（2）<div>Tomcat 为什么用一个简单的 queue 来实现多线程而不是用 JDK 自带的线程池？
1.自定义可以更好地控制，还有后期的优化
2.历史原因，可能当时内置线程池功能没那么完善
现在，应该也支持使用JDK自带的线程池

交个作业：https:&#47;&#47;github.com&#47;caozhenyuan&#47;mini-tomcat</div>2023-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/6e/5435e214.jpg" width="30px"><span>HH🐷🐠</span> 👍（0） 💬（1）<div>🌝🌝自带JDK线程池初始化指定线程数， 共用这些线程， 可能这次在A线程执行， 下次在B线程执行，上下文切来切去造成性能不必要的开销，在网络中这点开销算是很大了。 只能想到这个点，不知道是否正确</div>2023-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/bd/01/9c6482df.jpg" width="30px"><span>小树</span> 👍（1） 💬（1）<div>想请教一下老师，实际上是不是不会有 “如果available标志为 true，Connetor 线程就继续死等”这个情况呢。
因为每个processor线程的available初始是false的，等connector接收了新连接、assign了socket、更新了available变量以后，processor才能执行；processor执行完了以后这个processor也就被回收了，又进入了新一轮的上述过程。
所以我觉得，好像永远是各个processor等待connector来执行assign，而connector实际并没有机会进入到assign里的wait()的部分？</div>2024-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/2a/0e/4e187484.jpg" width="30px"><span>夙夜SEngineer</span> 👍（0） 💬（0）<div>发现个不太合理的地方，newProcessor方法正确逻辑应该如下才对：

private HttpProcessor newProcessor() {
        HttpProcessor initprocessor = new HttpProcessor(this);
        initprocessor.start();
        processors.push(initprocessor);
        curProcessors++;
&#47;&#47;        return ((HttpProcessor) processors.pop());
        return (HttpProcessor) initprocessor;
    }</div>2025-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/2a/0e/4e187484.jpg" width="30px"><span>夙夜SEngineer</span> 👍（0） 💬（0）<div>虽然Connctor和Proccessor是两个线程了，但本质还是同步模型，感觉性能没有提升。不知道我哪里理解的不对，请指教</div>2025-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/d7/9d/73390cc0.jpg" width="30px"><span>wild wings.Luv</span> 👍（0） 💬（0）<div>老师您好，看了您的文章收获满满。其中关于并发处理请求的架构我有一些问题。由于connector和processor是一对多的关系，所以每个processor要单独维护自己的信号，connector在分配socket时，调用processor的同步块assign。但是这个同步这里的代码我好像不是很理解。connector和processor之间实际上没有”同步的生产消费关系“：首先，createProcessor处有空余的processor时才会分配给connector，所以connector并不需要等待某个processor消费完了再给他socket，当没有空余的processor时直接放弃处理（这里也是我觉得设计的不足之处）。其次，processor中的同步块也并不是等待processor处理完请求释放socket之后，才把状态设置为false，而是拿到socket之后就马上更改状态。这样做的目的我不是很清楚，也就是这样的同步机制，我没有理解到它的用处。</div>2024-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3c/5d/21/afbecbd3.jpg" width="30px"><span>符方继</span> 👍（0） 💬（0）<div>@Override public void run() { 
while (true) { 
                &#47;&#47; 等待分配下一个 
               socket Socket socket = await(); 
               if (socket == null) continue; 
               &#47;&#47; 处理来自这个socket的请求 process(socket);
              &#47;&#47; 完成此请求 connector.recycle(this); 
} 
}
在高并发的情况下，是否要对socket的outputStream互斥？如果一个socket发送多个请求，每个线程都返回数据是否会出现粘包、数据错误等问题？
</div>2024-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/0e/dd/4d468ad7.jpg" width="30px"><span>__Alucard</span> 👍（0） 💬（0）<div>1.JDK线程池使用的阻塞队列BlockingQueue是单向队列，不支持双端操作，而Tomcat使用了Deque作为双端队列来优先使用旧的线程，平衡线程间的工作负载。
2.JDK线程池的工作队列机制不适合作为WebServer容器来处理IO请求。
3.事实上到这一节已经出现了经典的通信模型的设计： 单线程(多协程，IO操作上下文开销小)处理IO操作，多线程处理后续的业务逻辑，Netty也参考了这种设计。</div>2024-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ae/90/83e0d28d.jpg" width="30px"><span>chang</span> 👍（0） 💬（0）<div>void recycle(HttpProcessor processor) {
        processors.push(processor);
    }
这里应该加下synchronized，可能多个线程处理完同时归还</div>2024-06-23</li><br/>
</ul>