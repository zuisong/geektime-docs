你好，我是石川。

在上一讲中，我们初步介绍了并发和并行的概念，对比了不同语言对多线程开发的支持。我们也通过postMessage，学习了用信息传递的方式在主线程和Worker线程间实现交互。但是，我们也发现了JavaScript对比其它语言，在多线程方面还有不足，似乎信息传递本身不能让数据在不同的线程中真正做到共享，而**只是互传拷贝的信息**。

所以今天，我们再来看看如何能在信息互传的基础上，让数据真正地在多线程间共享和修改。不过更重要的是，这种修改是不是真的有必要呢。

## SAB+Atomics模式

前面，我们说过对象的数据结构在线程间是不能共享的。如果通过postMessage来做信息传递的话，需要数据先被深拷贝。那有没有什么办法能让不同的线程同时访问一个数据源呢？答案是有，要做到数据的共享，也就是内存共享，我们就需要用到 **SAB（SharedArrayBuffer）**和 **Atomics**。下面，我们先从SAB开始了解。

### **共享的ArrayBuffer**

SAB是一个共享的ArrayBuffer内存块。在说到SAB前，我们先看看ArrayBuffer是什么，这还要从内存说起。我们可以把内存想象成一个储藏室中的货架，为了找到存放的物品，有从1-9这样的地址。而里面存储的物品是用字节表示的，字节通常是内存中最小的值单元，里面可以有不同数量的比特（bit)，比如一个字节（byte）里可以有8、32或64比特。我们可以看到 bit 和 byte 它俩的英文写法和读音有些相似，所以这里要注意**不要把字节和比特混淆**。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1c/f4/73/8079d3fd.jpg" width="30px"><span>郭慧娟</span> 👍（1） 💬（1）<div>waitAsync 和 热路径 这里不太了解，有没有什么资料可以推荐一下</div>2022-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f4/73/8079d3fd.jpg" width="30px"><span>郭慧娟</span> 👍（1） 💬（1）<div>https:&#47;&#47;static001.geekbang.org&#47;resource&#47;image&#47;f8&#47;6c&#47;f81f3b9e0d9347ffc9d1a23e0758ae6c.jpeg?wh=1920x1080  这个图片感觉表意不太明白

参考链接 
https:&#47;&#47;juejin.cn&#47;post&#47;7016962394479919118
https:&#47;&#47;github.com&#47;mdn&#47;dom-examples&#47;tree&#47;main&#47;web-workers&#47;simple-web-worker
https:&#47;&#47;developer.chrome.com&#47;blog&#47;enabling-shared-array-buffer&#47;</div>2022-12-04</li><br/>
</ul>