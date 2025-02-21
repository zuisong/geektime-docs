今天我们来聊聊性能基准测试（benchmarking）。

大家或许都看到过一些不严谨的性能测试，以及基于这些测试结果得出的令人匪夷所思的结论。

```
static int foo() {
  int i = 0;
  while (i < 1_000_000_000) {
    i++;
  }
  return i;
}
```

举个例子，上面这段代码中的`foo`方法，将进行10^9次加法操作及跳转操作。

不少开发人员，包括我在介绍反射调用那一篇中所做的性能测试，都使用了下面这段代码的测量方式，即通过`System.nanoTime`或者`System.currentTimeMillis`来测量每若干个操作（如连续调用1000次`foo`方法）所花费的时间。

```
public class LoopPerformanceTest {
  static int foo() { ... }

  public static void main(String[] args) {
    // warmup
    for (int i = 0; i < 20_000; i++) {
      foo();
    }
    // measurement
    long current = System.nanoTime();
    for (int i = 1; i <= 10_000; i++) {
      foo();
      if (i % 1000 == 0) {
        long temp = System.nanoTime();
        System.out.println(temp - current);
        current = System.nanoTime();
      }
    }
  }
}
```

这种测量方式实际上过于理性化，忽略了Java虚拟机、操作系统，乃至硬件系统所带来的影响。

## 性能测试的坑

关于Java虚拟机所带来的影响，我们在前面的篇章中已经介绍过不少，如Java虚拟机堆空间的自适配，即时编译等。

在上面这段代码中，真正进行测试的代码（即`// measurement`后的代码）由于循环次数不多，属于冷循环，没有能触发OSR编译。

也就是说，我们会在`main`方法中解释执行，然后调用`foo`方法即时编译生成的机器码中。这种混杂了解释执行以及即时编译生成代码的测量方式，其得到的数据含义不明。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/49/06/b90049f4.jpg" width="30px"><span>shitao</span> 👍（19） 💬（0）<div>这篇还没留言啊，总结下自己的一点jmh测试经验吧，希望老师指导。
1. 最好在专门的机器上做测试而不是自己的pc
2. 依赖的外部资源如redis，db等，测试过程中最好是独占的
3. 测试时间不宜过短，我一般10min以上吧</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（2） 💬（1）<div>老师，什么叫冷循环呀？
既然有冷循环，是不是还有什么所谓的热循环？</div>2020-03-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKumMwlVcElxg28b0QZibiaDNxN35BDUvSiaMedz6QqVFC6S0Yp4d5FUicKUV4whGK0lov7fiaicJJnhhRQ/132" width="30px"><span>史海洋</span> 👍（0） 💬（0）<div>       &lt;dependency&gt;
            &lt;groupId&gt;javax.annotation&lt;&#47;groupId&gt;
            &lt;artifactId&gt;javax.annotation-api&lt;&#47;artifactId&gt;
            &lt;version&gt;1.3.2&lt;&#47;version&gt;
        &lt;&#47;dependency&gt;</div>2021-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（0） 💬（0）<div>感觉基准测试好麻烦，能否有更加简洁的方式呢？比较真实项目中，依赖还是比较强的</div>2021-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f9/fc/f01e160f.jpg" width="30px"><span>akka</span> 👍（0） 💬（0）<div>自己测试时的一点不同点:
java版本:java version &quot;11.0.3&quot; 2019-04-16 LTS;
需提供额外jar包:javax.annotation.javax.annotation-api,否则提示文件缺失;
原@Benchmark包中未提供，自动生成以@GenerateMicroBenchmark替代;
mvn package会生成两个jar:microbenchmarks.jar&#47;test-1.21.jar</div>2019-05-27</li><br/>
</ul>