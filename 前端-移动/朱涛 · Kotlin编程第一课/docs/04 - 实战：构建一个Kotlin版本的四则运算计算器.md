你好，我是朱涛。

前面几节课，我们学了不少Kotlin的语法，也算是对Kotlin有了一个基本认识。不过，单纯只认识Kotlin是远远不够的，我们还要**会用Kotlin**。当遇到一个具体问题的时候，我们得能用Kotlin来解决这个问题。换句话说，就是要实战。在实战的过程中，我们对Kotlin的理解也会进一步加深。

那么这节课，我们就把前面的知识点串联起来，一起做一个Kotlin版本的计算器。为了便于理解，我会以**循序渐进**的方式来编写这个计算器程序，由简单到复杂。你在这个由易到难的实操过程中，可以实际体会到Kotlin的代码实现思路以及编码方式的变化，进而也就能更好地掌握和运用前面所学的基础语法，以及与面向对象相关的知识点。

这个计算器程序大致会分为三个版本：

- 计算器1.0，实现两个整数的“加减乘除”，对输入数据有严格要求。
- 计算器2.0，对输入数据无严格要求，融入面向对象的编程思想。
- 计算器3.0，支持“大数的加法”，增加单元测试。

现在，我们就开始实战吧。

## 创建Kotlin工程

如果你之前没有使用过IntelliJ或Android Studio，你可能还不知道怎么创建一个工程。别担心，这个过程其实很简单，它分为以下几个步骤。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（32） 💬（5）<div>val left = exp.left
val operator = exp.operator
val right = exp.right

是不是可以写成

val (left, operator, right) = exp</div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/87/14e6475a.jpg" width="30px"><span>王玉朋</span> 👍（6） 💬（1）<div>老师，135+99的加法竖式动画图是用什么做的？</div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/e5/e1/a5064f88.jpg" width="30px"><span>Geek_Adr</span> 👍（3） 💬（1）<div>V3实战 加 算法 ！提高语言的手感？
坏学生偷懒 string.toBigInteger()
</div>2022-02-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epPU6RSBhdOdkTcLEtgWKuoXib2u34flmBicAwdXzEchibwEjmQsFiabyrNVajibdStw8UH3PuM4pfBIxg/132" width="30px"><span>JokerFake</span> 👍（3） 💬（1）<div>所以枚举那只能传ADD 不能传+ 这个bug是故意就给我们自己改的？</div>2022-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/bf/da/fede41ea.jpg" width="30px"><span>苍王</span> 👍（2） 💬（2）<div>private fun minusString(left: String, right: String): String {
        val result = StringBuilder()

        &#47;&#47;判断是否结果位负数
        val isMinus = (left.length &lt; right.length || left.length == right.length &amp;&amp; left[0] &lt; right[0])

        var leftIndex = left.length - 1
        var rightIndex = right.length - 1
        var _left = left
        var _right = right
        if (isMinus) {
            _left = right
            _right = left
            leftIndex = _left.length - 1
            rightIndex = _right.length - 1
        }

        var carry = 0
        while (leftIndex &gt;= 0 || rightIndex &gt;= 0) {
            val leftVal = if (leftIndex &gt;= 0) _left[leftIndex].digitToInt() else 0
            val rightVal = if (rightIndex &gt;= 0) _right[rightIndex].digitToInt() else 0
            var sum: Int
            if (leftVal - rightVal &lt; 0) {
                sum = leftVal - rightVal + 10 + carry
                carry = -1
            } else {
                sum = leftVal - rightVal + carry
                carry = 0
            }
            result.append(sum)
            leftIndex--
            rightIndex--

        }

        if (isMinus) {
            result.append(&quot;-&quot;)
        }

        return result.reverse().toString()
    }


 @Test
    fun testCalculateMinus1() {
        val calculatorV = CalculatorV3()

        val result = calculatorV.calculate(&quot;90-1&quot;)
        assertEquals(&quot;89&quot;, result)
    }

    @Test
    fun testCalculateMinus2() {
        val calculatorV = CalculatorV3()

        val result = calculatorV.calculate(&quot;1-9&quot;)
        assertEquals(&quot;-8&quot;, result)
    }

    @Test
    fun testCalculateMinus3() {
        val calculatorV = CalculatorV3()

        val result = calculatorV.calculate(&quot;233333333333333333333-1&quot;)
        assertEquals(&quot;233333333333333333332&quot;, result)
    }</div>2022-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/00/26/a80010f0.jpg" width="30px"><span>JL</span> 👍（2） 💬（1）<div>您好，想问一个关于单元测试的问题：
我在工作中assertEquals 和 assertThat().equals() 两种都遇到过 但是有人说 第二种更好一点。 想听听您的意见和建议。

之前网上搜了一下 也没有看到过说哪个好哪个坏</div>2022-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/7b/db/7cfa21ad.jpg" width="30px"><span>droidYu</span> 👍（1） 💬（2）<div>老师，V1版本的代码输入 3 + 4 会报错：No enum constant Operation.+；需要输入3 ADD 4才能正常运行，是您标的①处的代码的问题Operation.valueOf()方法抛错，为什么要故意写错，是有什么设计要讲解吗？</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/01/50/c1556a25.jpg" width="30px"><span>爱学习的小羊</span> 👍（1） 💬（1）<div>private fun minus(left: String, right: String): String {

        var maxNumber = String()
        var mainNumber = String()
        var resultMean = String()
        val data = left.length - right.length
        if (data &gt; 0){
            maxNumber = left
            mainNumber = right
            resultMean = &quot;&quot;
        }else if (data &lt; 0){
            maxNumber = right
            mainNumber = left
            resultMean = &quot;-&quot;
        }else{
            var position = 0
            while (left.get(position).digitToInt() == right.get(position).digitToInt()){
                position++
            }
            if (left.get(position).digitToInt() - right.get(position).digitToInt() &gt; 0){
                maxNumber = left
                mainNumber = right
                resultMean = &quot;&quot;
            }else{
                maxNumber = right
                mainNumber = left
                resultMean = &quot;-&quot;
            }
        }
        val result = StringBuilder()
        var maxIndex = maxNumber.length - 1
        var mainIndex = mainNumber.length - 1
        var carry = 0
        while (maxIndex &gt;= 0 || mainIndex &gt;= 0) {
            var leftVal = if (maxIndex &gt;= 0) maxNumber.get(maxIndex).digitToInt() else 0
            var rightVal = if (mainIndex &gt;= 0) mainNumber.get(mainIndex).digitToInt() else 0
            leftVal -= carry
            while (leftVal + carry * 10 &lt; rightVal) {
                carry++
            }
            val sum = leftVal + carry * 10 - rightVal
            if (sum in 1..9) {
                result.append(sum)
            }
            maxIndex--
            mainIndex--
        }
        return result.append(resultMean).reverse().toString()
    }
大佬这样写可吗</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/8b/94/09dca97d.jpg" width="30px"><span>故事与酒</span> 👍（0） 💬（1）<div>大数加和乘

fun minusString(left:String,right:String):String{
    val result = StringBuilder()
    var _left = left
    var _right = right
    var borrowNum = 0 &#47;&#47;是否向前借位
    var leftIndex = left.length -1
    var rightIndex = right.length - 1


    &#47;&#47;判断是否是小-大
    val isRightBig = left.length&lt;right.length || left.length == right.length &amp;&amp; left[0] &lt; right[0]
    if (isRightBig){
         _left = right
         _right = left
        leftIndex = _left.length - 1
        rightIndex = _right.length - 1
    }


    while(leftIndex &gt;=0 || rightIndex &gt;= 0){
        val leftVal = if (leftIndex &gt;= 0) _left.get(leftIndex).digitToInt() else 0
        val rightVal = if (rightIndex &gt;= 0) _right.get(rightIndex).digitToInt() else 0

        val digitResult = leftVal - rightVal - borrow</div>2022-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/e6/7c/51a02e43.jpg" width="30px"><span>剑来</span> 👍（0） 💬（1）<div>讲一个不是很关键的东西，通过你这个方式拉取代码后，一般刚下来本地是没有start分支的，需要通过origin&#47;start这个远程分支去checkout。</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/f0/20/54253ab7.jpg" width="30px"><span>浅色的风</span> 👍（0） 💬（1）<div> fun minusString(leftNum: String, rightNum: String): String {
        val result = StringBuilder()
        var leftIndex = leftNum.length - 1
        var rightIndex = rightNum.length - 1

        var borrow = 0

        while(leftIndex &gt;= 0 || rightIndex &gt;= 0){
            var leftVal = if(leftIndex &gt;= 0 ) leftNum.get(leftIndex).digitToInt() else 0
            val rightVal = if(rightIndex &gt;= 0 ) rightNum.get(rightIndex).digitToInt() else 0

            leftVal -= borrow;

            if(leftVal &gt;= rightVal ) borrow = 0 else borrow = 1

            val minu = borrow*10 + leftVal - rightVal

            result.append(minu)

            leftIndex--
            rightIndex--
        }

        if (result.get(result.lastIndex).digitToInt() == 0) {
            result.deleteAt(result.lastIndex)
        }
        return result.reverse().toString()
    }</div>2022-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/c5/95b97dfa.jpg" width="30px"><span>郑峰</span> 👍（0） 💬（1）<div>  private fun addString(left: String, right: String) = left.toBigDecimal().add(right.toBigDecimal()).toString()
  private fun minusString(left: String, right: String) = left.toBigDecimal().subtract(right.toBigDecimal()).toString()
  private fun multiString(left: String, right: String) = left.toBigDecimal().multiply(right.toBigDecimal()).toString()
  private fun divString(left: String, right: String) = left.toBigDecimal().divideToIntegralValue(right.toBigDecimal()).toString()
</div>2022-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/01/50/c1556a25.jpg" width="30px"><span>爱学习的小羊</span> 👍（0） 💬（2）<div>大佬以后出书的话  可以送我一本吗</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ee/94/5f3460cd.jpg" width="30px"><span>Marten</span> 👍（0） 💬（3）<div>大数的减法
fun minusString(left: String, right: String): String {
        val result = StringBuilder()
        var leftIndex = left.length - 1
        var rightIndex = right.length - 1

        var carry = 0

        while (leftIndex &gt;= 0 || rightIndex &gt;= 0) {
            var leftVal = if (leftIndex &gt;= 0) left.get(leftIndex).digitToInt() else 0
            var rightVal = if (rightIndex &gt;= 0) right.get(rightIndex).digitToInt() else 0
            leftVal -= carry
            while (leftVal + carry * 10 &lt; rightVal) {
                carry++
            }
            val sum = leftVal + carry * 10 - rightVal
            if (sum &lt;10) {
                result.append(sum)
            }
            leftIndex--
            rightIndex--

        }

        return result.reverse().toString().toInt().toString()
    }</div>2022-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ee/94/5f3460cd.jpg" width="30px"><span>Marten</span> 👍（0） 💬（2）<div> fun minusString(left: String, right: String): String {
        val result = StringBuilder()
        var leftIndex = left.length - 1
        var rightIndex = right.length - 1

        var carry = 0

        while (leftIndex &gt;= 0 || rightIndex &gt;= 0) {
            var leftVal = if (leftIndex &gt;= 0) left.get(leftIndex).digitToInt() else 0
            var rightVal = if (rightIndex &gt;= 0) right.get(rightIndex).digitToInt() else 0
            leftVal -= carry
            if (leftVal &lt; rightVal) {
                carry = 1
            }
            val sum = leftVal + carry * 10 - rightVal

            result.append(sum)
            leftIndex--
            rightIndex--

        }
        return result.reverse().toString()
    }</div>2022-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/25/67/6496b6ac.jpg" width="30px"><span>吴超</span> 👍（0） 💬（1）<div>rightNum.get(rightIndex).digitToInt()    digitToInt()  为啥找不到呢？</div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/a6/679b3c6b.jpg" width="30px"><span>Renext</span> 👍（0） 💬（1）<div>good</div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a6/f0/50d0931d.jpg" width="30px"><span>木易杨</span> 👍（0） 💬（1）<div>No enum constant com.kymjs.project4.unit6.Operation.+    我的怎么会报这个错了？</div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/3f/30/41c34dbb.jpg" width="30px"><span>会飞的小猪</span> 👍（0） 💬（6）<div>作者你好，在第一个案例Operation.valueOf(inputList[1])访问枚举类的时候咋会报非法数据异常嘞？直接传入“+”会报非法异常，传入“ADD”才正常，这是为什么？valueOf正常来说应该是匹配枚举类构造参数的吧</div>2022-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/31/1c/436bb722.jpg" width="30px"><span>野火</span> 👍（0） 💬（0）<div>val operation = Operation.valueOf(inputList[1])  这个明明就跑不通
java.lang.IllegalArgumentException: No enum constant com.example.kotlinexamples.Operation.+</div>2024-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/34/eb/df/9f24a4bf.jpg" width="30px"><span>wresource</span> 👍（0） 💬（0）<div>val operation = Operation2.valueOf(inputList[1])
与
val operation = inputList[1]
原来是老师故意写错的，难怪语法一直报错，说这个类型不兼容</div>2023-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/7a/30/23fc4089.jpg" width="30px"><span>24隋心所欲</span> 👍（0） 💬（0）<div>“Kotlin 统一了数组和集合的元素访问操作”

大小：使用 Java 中集合的 size；访问：使用 Java 中数组的 []

这里不是很统一啊，都用集合或者都用数组，岂不是更符合“统一”？</div>2022-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/ff/2f/eb03fccc.jpg" width="30px"><span>maitian</span> 👍（0） 💬（0）<div>老师 计算器1.0版本 我报了这个错，很奇怪
Exception in thread &quot;main&quot; java.lang.IllegalArgumentException: No enum constant com.derry.mandy.Operation1.+
	at java.lang.Enum.valueOf(Enum.java:238)
	at com.derry.mandy.Operation1.valueOf(Cacu_Laoshi.kt)
	at com.derry.mandy.Cacu_LaoshiKt.calculate(Cacu_Laoshi.kt:39)
	at com.derry.mandy.Cacu_LaoshiKt.main(Cacu_Laoshi.kt:22)
	at com.derry.mandy.Cacu_LaoshiKt.main(Cacu_Laoshi.kt)
</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/cb/9d/6b93b659.jpg" width="30px"><span>静水流深</span> 👍（0） 💬（1）<div>第一个Demo的第34行 
    val operation = Operation.valueOf(inputList[1])
报错 
Exception in thread &quot;main&quot; java.lang.IllegalArgumentException: No enum constant com.boycoder.Operation.+
</div>2022-07-14</li><br/>
</ul>