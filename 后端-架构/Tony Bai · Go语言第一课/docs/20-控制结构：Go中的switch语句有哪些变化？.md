你好，我是Tony Bai。

经过前两节课的学习，我们已经掌握了控制结构中的分支结构以及循环结构。前面我们也提到过，在计算机世界中，再复杂的算法都可以通过顺序、分支和循环这三种基本的控制结构构造出来。所以，理论上讲，我们现在已经具备了实现任何算法的能力了。

不过理论归理论，我们还是要回到现实中来，继续学习Go语言中的控制结构，现在我们还差一种分支控制结构没讲。除了if语句之外，Go语言还提供了一种更适合多路分支执行的分支控制结构，也就是**switch语句**。

今天这一节课，我们就来系统学习一下switch语句。Go语言中的switch语句继承自它的先祖C语言，所以我们这一讲的重点是Go switch语句相较于C语言的switch，有哪些重要的改进与创新。

在讲解改进与创新之前，我们先来认识一下switch语句。

## 认识switch语句

我们先通过一个例子来直观地感受一下switch语句的优点。在一些执行分支较多的场景下，使用switch分支控制语句可以让代码更简洁，可读性更好。

比如下面例子中的readByExt函数会根据传入的文件扩展名输出不同的日志，它使用了if语句进行分支控制：

```plain
func readByExt(ext string) {
    if ext == "json" {
        println("read json file")
    } else if ext == "jpg" || ext == "jpeg" || ext == "png" || ext == "gif" {
        println("read image file")
    } else if ext == "txt" || ext == "md" {
        println("read text file")
    } else if ext == "yml" || ext == "yaml" {
        println("read yaml file")
    } else if ext == "ini" {
        println("read ini file")
    } else {
        println("unsupported file extension:", ext)
    }
}
```
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（41） 💬（1）<div>type switch里的

switch v := x.(type) {

看上去像是一个初始化语句，但其实是一个type guard，所以后面没有分号。如果有初始化语句的话就是这样的：

switch a:= f(); v := x.(type) {

另外type switch里是不能fallthrough的</div>2021-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/6d/3e570bb8.jpg" width="30px"><span>一打七</span> 👍（17） 💬（2）<div>文中说x.(type)这种表达式形式是 switch 语句专有的，但是类型断言也可以这么写，所以不应该是专有的吧？</div>2022-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/58/45/9ba77dc3.jpg" width="30px"><span>lyy</span> 👍（9） 💬（5）<div>个人感觉fallthrough，执行完 case1 后，继续case2里面的代码，而不用判断case2的条件是否成立，这一点设计的并不好，估计很多人会理解为继续判断case2条件</div>2022-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/da/0a8bc27b.jpg" width="30px"><span>文经</span> 👍（3） 💬（1）<div>白老师，我这样理解对不对：
x.(type) 如果没有 := 符号的话，这个表达式是获取x的具体类型
v := x.(type), 这个则是把x从具体的接口类型中获取它实际类型的值。
x.(SomeType)， 则是判段x是否遵守SomeType接口，并转化为具体类型的值。
所有的这些行为都是编译器把它转化为相应的代码。</div>2021-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（3） 💬（3）<div>Tony Bai 老师的文章讲解的非常细致，鼓掌。

想问一下老师，文中的内容基本都能理解，但是过一段时间就遗忘比较多了，尤其是后面的内容涉及到前面的知识时。希望老师在这门课中搞个小型的实战项目，能把前面的知识串在一起就好了。

这样，不会觉得纸上得来终觉浅......</div>2021-11-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIV9NK3Mx29N2t9upmnZHN63hOgE6GV6LvaEDD2tkCASSKSVHictXZOucrpZJ0vPll4pF2XNVCKw1Q/132" width="30px"><span>十年一劫</span> 👍（2） 💬（1）<div>老师，现在go支持泛型了，type switch语句中传入的类型可以用泛型么</div>2023-11-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erEHTaQDkWqEYib9iabib8rACYpSFBHTPFmgicUKaib79MB6VIxNwiajHUS8kYFEKCGOjpibf0dibhIjqhfzg/132" width="30px"><span>plh</span> 👍（1） 💬（1）<div> switch 太灵活,即使有经验的go开发者也容易犯错. 看过好几篇文章,这个地方是讲的最全面,最清晰的. </div>2023-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0a/da/dcf8f2b1.jpg" width="30px"><span>qiutian</span> 👍（1） 💬（2）<div>哪来的case2呢</div>2022-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/70/6d/11ea66f0.jpg" width="30px"><span>peison</span> 👍（1） 💬（1）<div>我想请教一下，文中type switch中的  v:=x.(type)后面，为什么switch中的case分支，不是和x.(type)的返回值v做比较？那实际上case分支是和什么值做比较</div>2022-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/cc/70/64045bc0.jpg" width="30px"><span>人言有力</span> 👍（0） 💬（1）<div>本节讲述了switch语句的使用
1. switch是一个选择语句，对于多分支场景比if更加直观
2.go的switch相比c语言，改进了break机制，默认break，除非fallthrough
3.创新了一个type switch，可以用switch x.(type) 的方式，限定x需要是接口类型；并且如果x指定了类型，那么case语句需要是该接口类型的实现。
4. 思考题：if和switch其实if还是更常用，case用在分支特别多的场景多一些</div>2024-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/05/e4/3e676c4d.jpg" width="30px"><span>ps Sensking</span> 👍（0） 💬（1）<div>我们要注意的是只有接口类型变量才能使用 type switch，并且所有 case 语句中的类型必须实现 switch 关键字后面变量的接口类型。 
您好这个例子用interface 里面只要实现一个 int  或者 string 就可以正常启动吗？ 如果是type 自定义的类型 T 就需要制定一个int 或者 string吗？</div>2022-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/da/0a8bc27b.jpg" width="30px"><span>文经</span> 👍（0） 💬（1）<div>白老师，switch v := x.(type)，有点不太好理解。
这个语句编译器是不是转化为类型这样的代码：
v := x.(type)
switch x.(type)

我直观上会理解成：
v := x.(type)
switch v

这算不算编译器提供的一种语法糖？</div>2021-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（15） 💬（6）<div>今天《极客时间》两个专栏同时更新，主题都是 switch

- 《深入剖析 Java 新特性》06 | Switch表达式：怎么简化多情景操作？
- 《Tony Bai · Go 语言第一课》20｜控制结构：Go中的switch语句有哪些变化？

对比结果

- Java17 居然可以比 Go 简洁！
- 但然综合能力 Go 的更灵活


Java17 switch

```java
String checkWorkday(int day) {
	return switch (day) {
		case 1, 2, 3, 4, 5 -&gt; &quot;it is a work day&quot;;
		case 6, 7 -&gt; &quot;it is a weekend day&quot;;
		default -&gt; &quot;are you live on earth&quot;;
	};
}
```

Go switch

```go
func checkWorkday(day int) string {
	switch day {
	case 1, 2, 3, 4, 5:
		return &quot;it is a work day&quot;
	case 6, 7:
		return &quot;it is a weekend day&quot;
	default:
		return &quot;are you live on earth&quot;
	}
}
```</div>2021-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7b/bd/ccb37425.jpg" width="30px"><span>进化菌</span> 👍（5） 💬（0）<div>所以，switch 不需要 break 是出于大多数情况 switch 只需要走一条分支的缘故吗？</div>2021-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/44/b5/7eba5a0e.jpg" width="30px"><span>木木</span> 👍（1） 💬（1）<div>C语言的switch是为了模拟跳转表，所以如果目的是根据值执行一小段的话，需要每个条件的执行语句最后都加break，go的switch已经不再是为了模拟跳转表了，就是按着人们常用的方法设计的，所以不用加break，但是break的作用依旧留着</div>2021-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（1） 💬（0）<div>讲的非常详细，值得好好学习</div>2021-11-26</li><br/>
</ul>