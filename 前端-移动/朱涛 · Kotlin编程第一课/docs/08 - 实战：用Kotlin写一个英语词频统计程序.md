你好，我是朱涛。

前面几节课，我们学了一些Kotlin独有的特性，包括扩展、高阶函数等等。虽然我在前面的几节课当中都分别介绍了这些特性的实际应用场景，但那终归不够过瘾。因此，这节课我们来尝试将这些知识点串联起来，一起来写一个“单词词频统计程序”。

英语单词的频率统计，有很多实际应用场景，比如高考、研究生考试、雅思考试，都有对应的“高频词清单”，考生优先突破这些高频词，可以大大提升备考效率。那么这个高频词是如何统计出来的呢？当然是通过计算机统计出来的。只是，我们的操作系统并没有提供这样的程序，想要用这样的功能，我们必须自己动手写。

而这节课，我将带你用Kotlin写一个单词频率统计程序。为了让你更容易理解，我们的程序同样会分为三个版本。

- **1.0 版本**：实现频率统计基本功能，使用“命令式风格”的代码。
- **2.0 版本**：利用扩展函数、高阶函数来优化代码，实现“函数式风格”的代码。
- **3.0 版本**：使用inline进一步提升软件的性能，并分析高阶函数的实现原理，以及inline到底能带来多大的性能提升。

在正式开始学习之前，我也建议你去clone我GitHub上面的TextProcessor工程：[https://github.com/chaxiu/TextProcessor.git](https://github.com/chaxiu/TextProcessor.git)，然后用IntelliJ打开，并切换到 **start** 分支跟着课程一步步敲代码。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1a/ca/50c1fd43.jpg" width="30px"><span>colin</span> 👍（16） 💬（1）<div>String.clean() 使用顶层扩展好像不太合适，顶层扩展只适用于通用的逻辑，否则不清楚的人看着 idea 提示的扩展函数也一脸懵逼。</div>2022-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/06/e5/51ef9735.jpg" width="30px"><span>A Lonely Cat</span> 👍（8） 💬（1）<div>
fun main() {
    val word = &quot;Kotlin is my favorite language. I love Kotlin!&quot;
    val wordFrequencyList = word.clean()
        .participle()
        .countWordFrequency()
        .toList()
        .sortedByDescending { it.second }
    wordFrequencyList.forEach {
        println(&quot;word is ${it.first}, frequency is ${it.second}&quot;)
    }
}

&#47;**
 * 文本清洗
 *&#47;
private fun String.clean() =
    replace(&quot;[^A-Za-z]&quot;.toRegex(), &quot; &quot;)
        .trim()

&#47;**
 * 分词
 *&#47;
private fun String.participle() = split(&quot; &quot;).toList()

&#47;**
 * 计算词频
 *&#47;
private fun List&lt;String&gt;.countWordFrequency(): Map&lt;String, Int&gt; {
    val map = mutableMapOf&lt;String, Int&gt;()
    forEach {
        if (it.isNotBlank()) {
            val count = map.getOrDefault(it, 0)
            map[it] = count.plus(1)
        }
    }
    return map.toMap()
}
</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9d/12/af03109d.jpg" width="30px"><span>奥特之光</span> 👍（2） 💬（5）<div>fun foo(block: () -&gt; Unit) { 
   block()
}
从开始讲函数到这节课看完，我还没有发现有讲过-&gt;是什么意思，这里() -&gt; Unit这让人很懵，然后下面这个block()和参数的block又是啥关系？</div>2022-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/92/3e/82ab7967.jpg" width="30px"><span>_</span> 👍（0） 💬（1）<div>没用过JMH，查了一下Score的含义，默认情况下是Throughput模式，Score代表单位时间内执行的操作次数，所以testInlined要比testNoninlined快10倍。
https:&#47;&#47;stackoverflow.com&#47;questions&#47;24928922&#47;jmh-what-does-the-score-value-mean</div>2022-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/2a/57/6629c858.jpg" width="30px"><span>阿康</span> 👍（0） 💬（1）<div>在正式开始学习之前，我也建议你去 clone 我 GitHub 上面的 TextProcessor 工程：https:&#47;&#47;github.com&#47;chaxiu&#47;Calculator.git，然后用 IntelliJ 打开，并切换到 start 分支跟着课程一步步敲代码。
源码连接错了</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/c5/95b97dfa.jpg" width="30px"><span>郑峰</span> 👍（2） 💬（0）<div>One liner

fun processText(text: String) = text.replace(&quot;[^A-Za-z]&quot;.toRegex(), &quot; &quot;).trim()
    .split(&quot; &quot;).filter(String::isNotBlank)
    .groupingBy { it }.eachCount()
    .map { WordFreq(it.key, it.value) }
    .sortedByDescending { it.freq }
</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/84/ae/2c2a2fd3.jpg" width="30px"><span>ElleSky</span> 👍（1） 💬（0）<div>如果方法变得足够大，过度使用 inline 可能会妨碍或停止 Hotspot 优化（例如方法内联）。默认情况下， Hotspot 不会内联大于35个字节的方法。内联高阶函数也得根据实际情况吧？</div>2023-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/84/ae/2c2a2fd3.jpg" width="30px"><span>ElleSky</span> 👍（0） 💬（0）<div>hi，你好呀，请问你这gif图是用的什么软件生成的呢？</div>2023-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/5a/72/7e7385da.jpg" width="30px"><span>晓春</span> 👍（0） 💬（0）<div>Kotlin 最新 sortedByDescending 返回的是 List，
sortByDescending 返回的是 Unit</div>2023-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/74/e9/b74ea2b2.jpg" width="30px"><span>熊妈饭团</span> 👍（0） 💬（0）<div>为什么 inline mapToList 是private的method，当被拷贝到public area 执行时却不会报错呢？</div>2022-11-01</li><br/>
</ul>