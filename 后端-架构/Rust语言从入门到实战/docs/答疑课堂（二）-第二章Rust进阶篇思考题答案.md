你好，我是Mike。

这节课我们继续来看第二章的课后思考题答案。还是和之前一样，最好是自己学完做完思考题之后再来看答案，效果会更好。话不多说，我们直接开始吧！

## **进阶篇**

### [12｜智能指针：从所有权和引用看智能指针的用法](https://time.geekbang.org/column/article/725815?utm_campaign=geektime_search&utm_content=geektime_search&utm_medium=geektime_search&utm_source=geektime_search&utm_term=geektime_search)

#### 思考题

你试着打开示例中的这两句，看看报错信息，然后分析一下是为什么？

```plain
    // arced.play_mutref();  // 不能用
    // arced.play_own();     // 不能用
```

#### 答案

Arc本质上是个引用，所以不允许同时存在可变引用或者移动。play\_boxown() 和 play\_own() 只能同时打开一个，这两个方法调用都会消耗所有权，导致没法调用另外一个。

答案来自Taozi和Michael

### [13｜异步并发编程：为什么说异步并发编程是 Rust 的独立王国？](https://time.geekbang.org/column/article/725837?utm_campaign=geektime_search&utm_content=geektime_search&utm_medium=geektime_search&utm_source=geektime_search&utm_term=geektime_search)

#### 思考题

为什么我们要把 async Rust 叫做“独立王国”呢？

#### 答案

因此async Rust代码是在一个Runtime里面执行的，而std Rust的代码不需要这个额外的Runtime，因此说它是独立王国。

另一方面，在 Rust 中，异步编程是使用 async/await 语法，这种语法具有可传染性，与std Rust代码也可以明显区分开，因此它像一个独立王国。

### [14｜Tokio 编程（一）：如何编写一个网络命令行程序？](https://time.geekbang.org/column/article/726207?utm_campaign=geektime_search&utm_content=geektime_search&utm_medium=geektime_search&utm_source=geektime_search&utm_term=geektime_search)