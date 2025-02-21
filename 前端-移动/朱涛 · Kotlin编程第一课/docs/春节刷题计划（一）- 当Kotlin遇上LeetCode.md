你好，我是朱涛。

时光飞逝，不知不觉间，我们就已经完成了基础篇的学习，并且也已经完成了三个实战项目，但这终归是不够过瘾的。想要完全掌握Kotlin的基础语法，我们还需要更多的练习。我相信，你现在的心情就像是一个手握屠龙刀的勇士，热切希望找一些对手来验证自己的学习成果。

其实，我自己在学习一门新的编程语言的时候，有一个高效的方法，也分享给你。这里我以Kotlin为例，假设我现在是一个新手，想快速掌握Kotlin的话，我会这样做：

- 第一步，我会**去Google搜索一些语言特性对比的文章**。比如，我熟悉Java，想学Kotlin，我就会去搜“from Java to Kotlin”，然后去看一些Java、Kotlin语法对比的文章。这时候，我大脑里就会建立起Java与Kotlin的语法联系。
- 第二步，我会打开[Kotlin官方文档](https://kotlinlang.org/docs/basic-syntax.html)，花几个小时的时间粗略看一遍，对Kotlin的语法有个大致印象。
- 最后一步，我会**打开LeetCode之类的网站**，开始用Kotlin刷题。在刷题的过程中，我也会先从模拟类的题目开始，之后再到数组、链表、Map、二叉树之类的数据结构。整个过程由易到难，刚开始的时候，我会选择“简单题”，等熟练以后，再选择“中等题”，心情好的时候，我偶尔会做个“困难题”挑战一下。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/c5/95b97dfa.jpg" width="30px"><span>郑峰</span> 👍（5） 💬（1）<div>```Kotlin
fun compareVersion(version1: String, version2: String): Int {
  val v1 = version1.split(&quot;.&quot;).map { it.toInt() }
  val v2 = version2.split(&quot;.&quot;).map { it.toInt() }

  for (i in 0 until maxOf(v1.size, v2.size)) {
    val diff = (v1.getOrElse(i) { 0 } - v2.getOrElse(i) { 0 })
    if (diff != 0) return if (diff &gt; 0) 1 else -1
  }
  return 0;
}

```</div>2022-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（2） 💬（2）<div>我知道为啥找不到 maxBy 了，估计是因为这个方法在 1.6 版本中隐藏了

@DeprecatedSinceKotlin(warningSince = &quot;1.4&quot;, errorSince = &quot;1.5&quot;, hiddenSince = &quot;1.6&quot;)
public inline fun &lt;T, R : Comparable&lt;R&gt;&gt; Sequence&lt;T&gt;.maxBy(selector: (T) -&gt; R): T? {
    return maxByOrNull(selector)
}</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/e5/e1/a5064f88.jpg" width="30px"><span>Geek_Adr</span> 👍（2） 💬（1）<div>&#47;&#47; 我能找到的最大程度的函数式
    fun compareVersion(version1: String, version2: String): Int {
        return (version1.split(&quot;.&quot;).map { it.toInt() }
                to version2.split(&quot;.&quot;).map { it.toInt() })
            .run {
                (0 until maxOf(first.size, second.size))
                    .fold(0) { acc, i -&gt;
                        if (acc != 0) acc
                        else first.getOrElse(i) { 0 }.compareTo(second.getOrElse(i) { 0 })
                    }
            }
    }
</div>2022-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/c5/1231d633.jpg" width="30px"><span>梁中华</span> 👍（1） 💬（1）<div>
fun mostCommonWord1(paragraph: String, banned: Array&lt;String&gt;) =
            paragraph.toLowerCase()
                .replace(&quot;[^a-zA-Z ]&quot;.toRegex(), &quot; &quot;)
                .split(&quot;\\s+&quot;.toRegex())
                .filter { it !in banned.toSet() }
                .groupBy { it }
                .mapValues { it.value.size }
               &#47;&#47; .maxBy { it.value }  &#47;&#47;这里编译不过，我改了下
               &#47;&#47; ?.key?:throw IllegalArgumentException()
             .toList()   &#47;&#47;先转成List才能用MaxBy
            .maxByOrNull { it.second }</div>2022-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/07/6d/4c1909be.jpg" width="30px"><span>PoPlus</span> 👍（1） 💬（1）<div>涛哥，校招生还推荐用 kotlin 来写算法吗，感觉有些简化的太过了 😅</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/e5/e1/a5064f88.jpg" width="30px"><span>Geek_Adr</span> 👍（1） 💬（1）<div>&#47;&#47; 函数式 176ms 击败19%
    fun compareVersion(version1: String, version2: String): Int {
        return (version1.split(&quot;.&quot;).map { it.toInt() }
                to version2.split(&quot;.&quot;).map { it.toInt() })
            .run {
                (0 until max(first.size, second.size))
                    .fold(0) { acc, i -&gt;
                        if (acc != 0) acc 
                        else first.getOrElse(i) { 0 } - second.getOrElse(i) { 0 }
                    }
            }.let {
                when {
                    it &gt; 0 -&gt; 1
                    it &lt; 0 -&gt; -1
                    else -&gt; 0
                }
            }
    }

&#47;&#47; java  156ms 击败70%
    fun compareVersion(version1: String, version2: String): Int {
        val v1 = version1.split(&quot;.&quot;).map { it.toInt() }
        val v2 = version2.split(&quot;.&quot;).map { it.toInt() }
        var idx = 0
        while (idx &lt; v1.size &amp;&amp; idx &lt; v2.size) {
            if (v1[idx] &gt; v2[idx]) {
                return 1
            } else if (v1[idx] &lt; v2[idx]) {
                return -1
            }
            idx++
        }
        while (idx &lt; v1.size) {
            if (v1[idx++] &gt; 0) {
                return 1
            }
        }
        while (idx &lt; v2.size) {
            if (v2[idx++] &gt; 0) {
                return -1
            }
        }
        return 0
    }

</div>2022-02-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Urc67zDC8R6dh9U1ZFTF36icXewM1seehvOUYUs4hyWSsFzS5WQc2RcrE1Mzs8qtgib5SM5wFrVh22QcQd0JUUBw/132" width="30px"><span>jim</span> 👍（1） 💬（1）<div>春节还更新吗？</div>2022-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/01/50/c1556a25.jpg" width="30px"><span>爱学习的小羊</span> 👍（0） 💬（1）<div>我这个算是半java半kotlin编程了吧
fun compareVersion(version1: String, version2: String): Int {
        val nums1 = version1.split(&quot;.&quot;)
        val nums2 = version2.split(&quot;.&quot;)
        for (i in 0..maxOf(nums1.size,nums2.size)){
            var a = 0
            var b = 0
            if (i &lt; nums1.size) a = nums1[i].toInt()
            if (i&lt;nums2.size) b = nums2[i].toInt()
            val data = a - b
            when {
                data &gt; 0 -&gt; return 1
                data &lt; 0 -&gt; return -1
            }

        }
        return 0
    }</div>2022-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/f0/20/54253ab7.jpg" width="30px"><span>浅色的风</span> 👍（0） 💬（1）<div>是不是java思维
fun compareVersion(version1: String, version2: String): Int {
        val listV1 = version1.split(&quot;.&quot;).toList()
        val listV2 = version2.split(&quot;.&quot;).toList()

        val result = if (listV1.size &gt; listV2.size) 1 else -1

        val maxList = if (listV1.size &gt; listV2.size) listV1 else listV2
        val minList = if (listV1.size &lt;= listV2.size) listV1 else listV2

        for(i in 0..minList.size - 1){
            if(listV1[i].toInt() &gt; listV2[i].toInt()){
                return 1
            }else if(listV1[i].toInt() &lt; listV2[i].toInt()){
                return -1
            }
        }

        for(j in minList.size..maxList.size - 1){
            if(maxList[j].toInt() &gt; 0){
                return result
            }
        }

        return 0

    }</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/c7/5c/94cb3a1a.jpg" width="30px"><span>$Kotlin</span> 👍（0） 💬（1）<div>    fun compareVersion(version1: String, version2: String): Int {
        val versionList1 = version1.split(&quot;.&quot;).toMutableList()
        val versionList2 = version2.split(&quot;.&quot;).toMutableList()
        if (versionList1.size &gt; versionList2.size) {
            repeat(versionList1.size - versionList2.size) {
                versionList2.add(&quot;0&quot;)
            }
        } else {
            repeat(versionList2.size - versionList1.size) {
                versionList1.add(&quot;0&quot;)
            }
        }
        for (index in 0..versionList1.size-1) {
            val v1Int = versionList1[index].toInt()
            val v2Int = versionList2[index].toInt()
            if (v1Int &gt; v2Int) {
                return 1
            } else if (v1Int &lt; v2Int) {
                return -1
            }
        }
        return 0
    }</div>2022-01-28</li><br/>
</ul>