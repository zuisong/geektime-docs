你好，我是朱涛。今天我们来分析Channel的源码。

Kotlin的Channel是一个非常重要的组件，在它出现之前，协程之间很难进行通信，有了它以后，协程之间的通信就轻而易举了。在[第22讲](https://time.geekbang.org/column/article/493069)当中，我们甚至还借助Channel实现的Actor做到了并发安全。

那么总的来说，Channel是热的，同时它还是一个**线程安全的数据管道**。而由于Channel具有线程安全的特性，因此，它最常见的用法，就是建立CSP通信模型（Communicating Sequential Processes）。

不过你可能会觉得，CSP太抽象了不好理解，但其实，这个通信模型我们在第22讲里就接触过了。当时我们虽然是通过Actor来实现的，但却是把它当作CSP在用，它们两者的差异其实很小。

关于[CSP的理论](https://en.wikipedia.org/wiki/Communicating_sequential_processes)，它的精确定义其实比较复杂，不过它的核心理念用一句话就可以概括：**不要共享内存来通信；而是要用通信来共享内存**（Don’t communicate by sharing memory; share memory by communicating）。

可是，我们为什么可以通过Channel实现CSP通信模型呢？这背后的技术细节，则需要我们通过源码来发掘了。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="" width="30px"><span>Paul Shan</span> 👍（9） 💬（1）<div>思考题：LinkedListChannel.offerInternal调用AbstractSendChannel.offerInternal 失败的时候，会把发送的内容持续放到队列中，这样即使接受方没准备好或者不存在，发送方也不会等待，而持续进入可以接收数据并发送的状态。LinkedListChannel.offerSelectInternal调用AbstractSendChannel.offerSelectInternal失败的时候，还是会继续尝试调用这个方法，因为LinkedListChannel只要内存允许，会时刻处于接受数据的状态。
</div>2022-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/fa/9e/306a5ce7.jpg" width="30px"><span>EdisonLi</span> 👍（5） 💬（1）<div>要是能开辟一篇实际工作业务场景的使用就更好了。</div>2022-05-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqQVYE1EfqibdyNsnjFibHW4jee0Q3qMMeRhqqVQUn5Ix9fFl3Zfzf0xpdrGypxHUmBCyiczfyEaPoWA/132" width="30px"><span>ACE_Killer09</span> 👍（2） 💬（1）<div>java 阻塞队列 的感觉</div>2022-04-18</li><br/>
</ul>