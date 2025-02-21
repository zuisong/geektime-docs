你好，我是Tony Bai。今天我想和你分享一个Go纯计算逻辑调优的故事。

在[开篇词](https://time.geekbang.org/column/article/426265)中我提到过，**Go语言是生产力与性能的最佳结合**。Go语言提供了足够快的运行效率，可以满足大多数场景下的性能需求，但这并不意味着Go的执行性能已经到了“天花板”。近期国外开发者Ben Dicken做了一个[语言性能测试](https://benjdd.com/languages/)，对比了十多种主流语言执行10亿次循环（一个双层循环：1万 * 10 万）的纯计算逻辑速度。下面是这项测试的结果示意图：

![图片](https://static001.geekbang.org/resource/image/f0/d9/f094536718550301b0719c1faeb30dd9.png?wh=1500x1486%2210%E4%BA%BF%E5%BE%AA%E7%8E%AF%E6%B5%8B%E8%AF%95%E7%BB%93%E6%9E%9C%EF%BC%8C%E6%9D%A5%E6%BA%90%E4%BA%8E%E7%BD%91%E7%BB%9C%22)

我们看到，在这项测试中，Go的表现不仅远不及NonGC的C/Rust，甚至还落后于同为GC语言的Java。这一结果可能让许多Go开发者感到意外，Go通常被认为是轻量级的高性能语言，然而**实际的测试结果却揭示了其在纯计算逻辑运行速率上仍有优化空间**。

那在这项测试中，为什么Go的表现不及预期？我们又该如何进一步优化？这篇加餐，我们就来探讨一下可能的原因和具体的优化方案，希望能为你提供更多的思考。

为了更直观地呈现整个过程，我们先要在自己的环境重现该性能问题。

## 重现性能问题

下面是此项测试的原作者给出的Go测试程序：

```plain
// why-go-sucks/billion-loops/go/code.go 


package main


import (
    "fmt"
    "math/rand"
    "os"
    "strconv"
)


func main() {
    input, e := strconv.Atoi(os.Args[1]) // Get an input number from the command line
    if e != nil {
        panic(e)
    }
    u := int32(input)
    r := int32(rand.Intn(10000))        // Get a random number 0 <= r < 10k
    var a [10000]int32                  // Array of 10k elements initialized to 0
    for i := int32(0); i < 10000; i++ { // 10k outer loop iterations
        for j := int32(0); j < 100000; j++ { // 100k inner loop iterations, per outer loop iteration
            a[i] = a[i] + j%u // Simple sum
        }
        a[i] += r // Add a random value to each element in array
    }
    fmt.Println(a[r]) // Print out a single element from the array
}
```
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1a/06/84/3c66309c.jpg" width="30px"><span>沿见</span> 👍（0） 💬（1）<div>之前在公众号上看到了这篇，结果老师竟然作为迭代放到了这门课上，课程常看常新，手动点赞。感觉现在很少有人像在嵌入式平台上开发一样死抠这些小的运行效率问题了，但是整个调优过程确实让人受益匪浅</div>2025-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（0） 💬（1）<div>太厉害了👍</div>2025-01-03</li><br/>
</ul>