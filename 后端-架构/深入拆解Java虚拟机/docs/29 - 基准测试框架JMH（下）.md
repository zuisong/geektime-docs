今天我们来继续学习基准测试框架JMH。

## @Fork和@BenchmarkMode

在上一篇的末尾，我们已经运行过由JMH项目编译生成的jar包了。下面是它的输出结果：

```
$ java -jar target/benchmarks.jar
...
# JMH version: 1.21
# VM version: JDK 10.0.2, Java HotSpot(TM) 64-Bit Server VM, 10.0.2+13
# VM invoker: /Library/Java/JavaVirtualMachines/jdk-10.0.2.jdk/Contents/Home/bin/java
# VM options: <none>
# Warmup: 5 iterations, 10 s each
# Measurement: 5 iterations, 10 s each
# Timeout: 10 min per iteration
# Threads: 1 thread, will synchronize iterations
# Benchmark mode: Throughput, ops/time
# Benchmark: org.sample.MyBenchmark.testMethod

# Run progress: 0,00% complete, ETA 00:08:20
# Fork: 1 of 5
# Warmup Iteration   1: 1023500,647 ops/s
# Warmup Iteration   2: 1030767,909 ops/s
# Warmup Iteration   3: 1018212,559 ops/s
# Warmup Iteration   4: 1002045,519 ops/s
# Warmup Iteration   5: 1004210,056 ops/s
Iteration   1: 1010251,342 ops/s
Iteration   2: 1005717,344 ops/s
Iteration   3: 1004751,523 ops/s
Iteration   4: 1003034,640 ops/s
Iteration   5: 997003,830 ops/s

# Run progress: 20,00% complete, ETA 00:06:41
# Fork: 2 of 5
...

# Run progress: 80,00% complete, ETA 00:01:40
# Fork: 5 of 5
# Warmup Iteration   1: 988321,959 ops/s
# Warmup Iteration   2: 999486,531 ops/s
# Warmup Iteration   3: 1004856,886 ops/s
# Warmup Iteration   4: 1004810,860 ops/s
# Warmup Iteration   5: 1002332,077 ops/s
Iteration   1: 1011871,670 ops/s
Iteration   2: 1002653,844 ops/s
Iteration   3: 1003568,030 ops/s
Iteration   4: 1002724,752 ops/s
Iteration   5: 1001507,408 ops/s


Result "org.sample.MyBenchmark.testMethod":
  1004801,393 ±(99.9%) 4055,462 ops/s [Average]
  (min, avg, max) = (992193,459, 1004801,393, 1014504,226), stdev = 5413,926
  CI (99.9%): [1000745,931, 1008856,856] (assumes normal distribution)


# Run complete. Total time: 00:08:22

...

Benchmark                Mode  Cnt        Score      Error  Units
MyBenchmark.testMethod  thrpt   25  1004801,393 ± 4055,462  ops/s
```

在上面这段输出中，我们暂且忽略最开始的Warning以及打印出来的配置信息，直接看接下来貌似重复的五段输出。

```
# Run progress: 0,00% complete, ETA 00:08:20
# Fork: 1 of 5
# Warmup Iteration   1: 1023500,647 ops/s
# Warmup Iteration   2: 1030767,909 ops/s
# Warmup Iteration   3: 1018212,559 ops/s
# Warmup Iteration   4: 1002045,519 ops/s
# Warmup Iteration   5: 1004210,056 ops/s
Iteration   1: 1010251,342 ops/s
Iteration   2: 1005717,344 ops/s
Iteration   3: 1004751,523 ops/s
Iteration   4: 1003034,640 ops/s
Iteration   5: 997003,830 ops/s
```

你应该已经留意到`Fork: 1 of 5`的字样。这里指的是JMH会Fork出一个新的Java虚拟机，来运行性能基准测试。

之所以另外启动一个Java虚拟机进行性能基准测试，是为了获得一个相对干净的虚拟机环境。

在介绍反射的那篇文章中，我就已经演示过因为类型profile被污染，而导致无法内联的情况。使用新的虚拟机，将极大地降低被上述情况干扰的可能性，从而保证更加精确的性能数据。

在介绍虚方法内联的那篇文章中，我讲解过基于类层次分析的完全内联。新启动的Java虚拟机，其加载的与测试无关的抽象类子类或接口实现相对较少。因此，具体是否进行完全内联将交由开发人员来决定。

关于这种情况，JMH提供了一个性能测试案例\[1]。如果你感兴趣的话，可以下载下来自己跑一遍。

除了对即时编译器的影响之外，Fork出新的Java虚拟机还会提升性能数据的准确度。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/15/81/2c31cf79.jpg" width="30px"><span>永烁星光</span> 👍（2） 💬（0）<div>老师 @State注解 这个程序状态类 实在没有看懂，其用处在于什么？</div>2018-10-12</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLz3icr3mGs5ib8FbSPQZ2ic3ib90mHkd1btQrmGacZjJxfYXrerIdaTxglKyCicFzLcEAb6deC2cWjE5Q/132" width="30px"><span>the geek</span> 👍（0） 💬（0）<div>看网上其他文章，都是说@State注解是用来设置标注类的实例范围。性能测试类由JMH管理，和spring的@Scope注解相似。</div>2020-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（0） 💬（0）<div>动手做一遍，感受会更深些</div>2019-10-29</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/0CL2N0xC7M9sQ0fVGHXibkCK1EZibtjylLQ1NsiaPCN0fCeNkDuuibDZahC8iaeiafDnzXlicCW0xHxWHw2Ubz7ov9nJg/132" width="30px"><span>cras</span> 👍（0） 💬（1）<div>需要那些基础知识才听得懂老师的内容?</div>2019-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（0） 💬（0）<div>建议老师给一个更贴合生产环境的例子，比如用JMH测试SpringBoot RestController的性能，可能效果会更好一些？</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/10/dc/fc9efd01.jpg" width="30px"><span>HELSING</span> 👍（0） 💬（0）<div>郑老师，能不能介绍一下，为什么ZGC会快那么多啊</div>2018-09-26</li><br/>
</ul>