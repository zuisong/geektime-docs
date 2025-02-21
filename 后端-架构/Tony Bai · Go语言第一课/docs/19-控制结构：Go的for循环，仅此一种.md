你好，我是Tony Bai。

上一节课，我们开始了对程序控制结构的学习，学习了分支结构中的if语句。上节课我们也说过，针对程序的分支结构，Go提供了if和switch-case两种语句形式。那你肯定在想，这节课肯定是要讲switch-case语句了吧！我不想按常规出牌，这一节课我们换换口味，挑战一下程序控制结构中最复杂的一款：循环结构。

为什么这么设置呢？因为我想让你能更早开始动手编写具有循环结构的Go代码。虽然switch-case分支结构也非常重要，但毕竟我们已经有了if分支语句的基础了，很多时候用if也可以替代switch-case，所以把它往后放放也没关系。

日常编码过程中，我们常常需要重复执行同一段代码，这时我们就需要循环结构来帮助我们控制程序的执行顺序。一个循环结构会执行循环体中的代码直到结尾，然后回到开头继续执行。 主流编程语言都提供了对循环结构的支持，绝大多数主流语言，包括C语言、C++、Java和Rust，甚至连动态语言Python还提供了不止一种的循环语句，但Go却只有一种，也就是for语句。

所以这节课，我们就来系统学习一下Go语言循环结构中的这一支独苗，for语句，聚焦于它的使用形式和常见坑点，让你能更快上手Go编码。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/59/21/d2efde18.jpg" width="30px"><span>布凡</span> 👍（43） 💬（1）<div>老师，最后问题三：遍历 map 中元素的随机性中举的例子没看懂：
1、示例1中，当 k=&quot;tony&quot;作为第一个迭代的元素时，我们将得到如下结果：包含了“tony”,是因为for循环中读取的是“tony”不允许被删除吗？
2、示例2中，是当m[&quot;lucky&quot;]=24 这个值被其它原map中的值覆盖，导致赋值不成功吗？
还请老师指教</div>2021-11-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/lfMbV8RibrhFxjILg4550cZiaay64mTh5Zibon64TiaicC8jDMEK7VaXOkllHSpS582Jl1SUHm6Jib2AticVlHibiaBvUOA/132" width="30px"><span>用0和1改变自己</span> 👍（40） 💬（4）<div>用数组指针替换数组
func main() {
	var a = [5]int{1, 2, 3, 4, 5}
	var r [5]int
	fmt.Println(&quot;original a =&quot;, a)

	for i, v := range &amp;a {  &#47;&#47;a 改为&amp;a
		if i == 0 {
			a[1] = 12
			a[2] = 13
		}
		r[i] = v
	}
	fmt.Println(&quot;after for range loop, r =&quot;, r)
	fmt.Println(&quot;after for range loop, a =&quot;, a)
}</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（17） 💬（5）<div>Tony Bai老师，你在评论中说：“如果luckey创建与第一个被遍历的元素之前了，那么后续就不会遍历它了。别忘了，key存储在哪里是根据hash值来定的”。

这个我还是似懂非懂，能举例说明一下么？ 非常感谢。</div>2021-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（8） 💬（3）<div>map 中的坑比想象的要多，使用的时候一定要细心。老师基本上把能遇到的坑都指出来了。惭愧的是 continue 和 break 的 label 从来没用过。</div>2021-11-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIfQFSpQJNKeqTicbpr3Rjo4VYdjE85QMWicMkoTCrGljg6GZcTjXFib1hSt8X9QuUfEuhMQCrdP15Aw/132" width="30px"><span>crabxyj</span> 👍（7） 💬（2）<div>问题三：java 中是不允许在遍历中修改当前集合的，和fastfail有关，直接会抛出异常，而go允许，但遍历结果不可控</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（4） 💬（4）<div>对于 map 遍历的那个例子，新增一个 map key  m[&quot;lucy&quot;] = 24 ， 这里的结果counter 不应该一直是 4吗？ 给 map 添加的元素为什么有的时候可以访问到 有的时候访问不到？</div>2021-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/22/5a/873ac981.jpg" width="30px"><span>酥宝话不多</span> 👍（3） 💬（1）<div>传数组地址，&amp;a</div>2021-11-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/pESfAX6YVRnVg3HpOX44bTa64bHTbhsnlHJqqDjicBeELxCs5rwwIXibFibd0fua3VyVExypnqnfgTSUp8WoYmc9g/132" width="30px"><span>白小白</span> 👍（2） 💬（1）<div>老师，请教一下：最后一个例子的结果出现的原因正是因为map 中元素的随机性，如何能保证只输出一种结果？</div>2022-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4b/d7/f46c6dfd.jpg" width="30px"><span>William Ning</span> 👍（2） 💬（2）<div>老师同学好，
关于评论列表中第一条 中的 第二个问题，就是map新元素的插入，位置是随机的，不定的，所以，可能插入到原来第一个元素的前面，也可能在后面，如果在前面，就被跳过了，便没有输出。
从个人代码执行，输出结果便可知，m[&quot;lucy&quot;] = 24 插入的位置，确实会出现在任意的位置，因为输出的位置，从0-3都有～

但是关于上面的回答中的“，别忘了，key存储在哪里是根据hash值来定的”  如果是这样，m[&quot;lucy&quot;] = 24，lucy应该是一个确定的值，不论经过次重复的hash，hash值应该都是一样的，也就是说，插入的位置，应该都是确定的，那么输出结果应该只有上面结果的中的一种可能，我的理解出了什么偏差吗？
谢谢老师，同学～

下面是输出结果，供参考
➜  golearning go run .
tony 21
tom 22
jim 23
lucy 24
counter is  4
➜  golearning go run .
tony 21
tom 22
jim 23
counter is  3
➜  golearning go run .
tony 21
tom 22
jim 23
lucy 24
counter is  4
➜  golearning go run .
tony 21
tom 22
jim 23
lucy 24
counter is  4
➜  golearning go run .
tony 21
tom 22
jim 23
lucy 24
counter is  4
➜  golearning go run .
tony 21
tom 22
jim 23
lucy 24
counter is  4
➜  golearning go run .
tony 21
tom 22
jim 23
lucy 24
counter is  4
➜  golearning go run .
tom 22
jim 23
lucy 24
tony 21
counter is  4
➜  golearning go run .
tony 21
tom 22
jim 23
lucy 24
counter is  4
➜  golearning go run .
tom 22
jim 23
lucy 24
tony 21
counter is  4
➜  golearning go run .
tony 21
tom 22
jim 23
lucy 24
counter is  4
➜  golearning go run .
tony 21
tom 22
jim 23
lucy 24
counter is  4
➜  golearning go run .
tony 21
tom 22
jim 23
lucy 24
counter is  4
➜  golearning go run .
tony 21
tom 22
jim 23
lucy 24
counter is  4
➜  golearning go run .
tony 21
tom 22
jim 23
lucy 24
counter is  4
➜  golearning go run .
tom 22
jim 23
lucy 24
tony 21
counter is  4
➜  golearning go run .
jim 23
lucy 24
tony 21
tom 22
counter is  4
➜  golearning go run .
tom 22
jim 23
lucy 24
tony 21
counter is  4
➜  golearning go run .
jim 23
lucy 24
tony 21
tom 22
counter is  4
</div>2022-03-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（2） 💬（1）<div>关于思考题，除了换成切片或者指针外，我们可以将 for range 替换为传统的 for ;; 循环就可以解决问题。

这里有一个衍生的问题，还烦请老师解答，如果说 for range 会对遍历的结构产生副本，那么我们用 for range 去遍历大型的数组的话是不是会有性能或者资源浪费等问题？所以说在平时，我们还是尽量用传统的三段式 for 循环而不是 for range？这样即使是不太了解 go 的人来看代码也不会有困惑</div>2022-03-10</li><br/><li><img src="" width="30px"><span>0mfg</span> 👍（2） 💬（2）<div>白老师，您好
请问课程中提到的“我们可以为闭包函数增加参数，并且在创建 Goroutine 时将参数与 i、v 的当时值进行绑定”，这个绑定具体如何理解，或者是怎么实现的呢？希望老师百忙中可以抽空解答，谢谢</div>2021-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/00/7a/791d0f5e.jpg" width="30px"><span>大年糕</span> 👍（1） 💬（1）<div>请问老师 下面的代码我这么理解对不对?
func main() {
	var a = [5]int{1, 2, 3, 4, 5}
	var r [5]int
	fmt.Println(&quot;original a =&quot;, a)

	for i, v := range &amp;a {  &#47;&#47;a 改为&amp;a
		if i == 0 {
			a[i] = 12
		
		}
		r[i] = v
	}
	fmt.Println(&quot;after for range loop, r =&quot;, r)
	fmt.Println(&quot;after for range loop, a =&quot;, a)
}

输出结果:
original a = [1 2 3 4 5]
after for range loop, r = [1 2 3 4 5]
after for range loop, a = [12 2 3 4 5]

我的理解,当i等于0时,虽然if语句中把a[0]修改为了12, 但是v值并不是指针类型,还是当前获取的值1, 所以后面的代码r[i] = v 还是原来数组中a[0]的值.</div>2023-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/91/d0/35bc62b1.jpg" width="30px"><span>无咎</span> 👍（1） 💬（1）<div>其实说明range使用的是副本，直接代码打印地址即可。
```
package main

import &quot;fmt&quot;

func main() {
	var a = [5]int{1, 2, 3, 4, 5} &#47;&#47; [5]int{1,2,3,4,5}
	var r [5]int

	fmt.Println(&quot;original a =&quot;, a)
	for i := 0; i &lt; len(a); i++ {
		fmt.Println(&amp;a[i], &quot;: &quot;, a[i])
	}

	for i, v := range a {
		fmt.Println(&amp;a[i], &quot;: &quot;, a[i])
		if i == 0 {
			a[1] = 12
			a[2] = 13
		}
		r[i] = v
	}

	fmt.Println(&quot;after for range loop, r = &quot;, r)
	fmt.Println(&quot;after for range loop, a = &quot;, a)
}
```
original a = [1 2 3 4 5]
0xc000100000 :  1
0xc000100008 :  2
0xc000100010 :  3
0xc000100018 :  4
0xc000100020 :  5
0xc000100000 :  1
0xc000100008 :  12
0xc000100010 :  13
0xc000100018 :  4
0xc000100020 :  5
after for range loop, r =  [1 2 3 4 5]
after for range loop, a =  [1 12 13 4 5]

Program exited.</div>2023-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/43/1aa8708a.jpg" width="30px"><span>子杨</span> 👍（1） 💬（1）<div>终于阳康，新年第一天，学习起来。祝老师新年快乐，2023 心想事成。

思考题：给 a 加上一个地址符即可 &amp;。</div>2023-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f5/5a/c7635ba6.jpg" width="30px"><span>ReviveKwan</span> 👍（1） 💬（1）<div>func main() {

    var a = [5]int{1, 2, 3, 4, 5}
    var r [5]int

    fmt.Println(&quot;origin a =&quot;, a)

    for i, _ := range a {
        if i == 0 {
            a[1] = 12
            a[2] = 13
        }
        r[i] = a[i]
    }
    fmt.Println(&quot;循环之后 r是这样的 r =&quot;, r)
    fmt.Println(&quot;循环之后 a是这样的 a =&quot;, a)

}

老师，剑走偏锋，没用引用，但是也能达到效果😂😂😂，我知道好像不太正规</div>2022-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/2e/ca/469f7266.jpg" width="30px"><span>菠萝吹雪—Code</span> 👍（1） 💬（1）<div>package main

import &quot;fmt&quot;

func main() {

	var sl = [6]int{1, 2, 3, 4, 5, 6}
	var a [6]int

	fmt.Println(&quot;sl = &quot;, sl)
	for i, v := range &amp;sl {
		if i == 0 {
			sl[1] = 12
			sl[2] = 13
		}
		a[i] = v
	}
	
	fmt.Println(&quot;a = &quot;, a)
	fmt.Println(&quot;sl = &quot;, sl)
}
sl =  [1 2 3 4 5 6]
a =  [1 12 13 4 5 6] 
sl =  [1 12 13 4 5 6]
</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/57/41/886a9d74.jpg" width="30px"><span>ming</span> 👍（1） 💬（2）<div>老师，我理解range的复制和函数入参的复制不一样吧？如下：func没有改变arr的len，但range改变了arr的len
func appendArr(arr []int) {
	arr = append(arr, 1)
}

func main() {
	arr := make([]int, 1, 2)
	arr[0] = 0

	appendArr(arr)
	fmt.Println(len(arr), cap(arr), arr) &#47;&#47; 1 2 [0]

	for range arr {
		arr = append(arr, 1)
		break
	}
	fmt.Println(len(arr), cap(arr), arr) &#47;&#47; 2 2 [0 1]
}</div>2022-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/12/a8/8aaf13e0.jpg" width="30px"><span>mikewoo</span> 👍（1） 💬（1）<div>这一节课的内容非常细致，受益匪浅。思考题中是不是可以传数组换成传数组指针来解决问题。</div>2022-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/23/5c74e9b7.jpg" width="30px"><span>$侯</span> 👍（1） 💬（1）<div>老师你好，请问下那怎么在for range中对map插入数据才是安全的呢</div>2021-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/61/58/7b078879.jpg" width="30px"><span>Julien</span> 👍（1） 💬（1）<div>最后那个例子，delete(m, &quot;tony&quot;)不总是删除map中key等于tony的键值对吗？为什么和顺序有关系呢？求指教，谢谢。</div>2021-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/6b/17/0c73f775.jpg" width="30px"><span>武好累</span> 👍（1） 💬（1）<div>可以直接取原数组下标值
func main() {
	var a = [5]int{1, 2, 3, 4, 5}
	var r [5]int

	fmt.Println(&quot;original a =&quot;, a)

	for i, _ := range a[:] {
		if i == 0 {
			a[1] = 12
			a[2] = 13
		}
		r[i] = a[i]
	}

	fmt.Println(&quot;after for range loop, r =&quot;, r)
	fmt.Println(&quot;after for range loop, a =&quot;, a)
}
</div>2021-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/20/124ae6d4.jpg" width="30px"><span>若水清菡</span> 👍（1） 💬（1）<div>这节课真长哈~~~，感觉学了复合数据类型，诸如数组 &#47; 切片、map 这些，还是有点蒙，感觉没有联系起来，也没有在这些上面给出更多的示例
</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（1） 💬（5）<div>老师，常见“坑”点中的问题二：

for i, v := range a&#39; { &#47;&#47; a&#39; 是 a 的一个值拷贝
    if i == 0 {
        a[1] = 12
        a[2] = 13
    }
    r[i] = v
}

其中说到，a&#39; 是 a 的一个值拷贝，但是我看循环体中 if 语句中的是 a 而不是 a&#39;，也就是说里面的还是原数组变量 a，不是切片 a&#39; 吗？它不是在 for 循环体范围内，难道不应该是使用 a&#39; 吗？有点疑惑！</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/15/c9/6ae2903f.jpg" width="30px"><span>Jim</span> 👍（1） 💬（1）<div>&#47;&#47;课后题:数组a遍历时前面加个&amp;
func main() {
	var a = [5]int{1, 2, 3, 4, 5}
	var r [5]int

	fmt.Println(&quot;original a =&quot;, a)

	for i, v := range &amp;a {
		if i == 0 {
			a[1] = 12
			a[2] = 13
		}
		r[i] = v
	}

	fmt.Println(&quot;after for range loop, r =&quot;, r)
	fmt.Println(&quot;after for range loop, a =&quot;, a)
}</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/d0/3f/08316343.jpg" width="30px"><span>小豆子</span> 👍（1） 💬（1）<div>func main() {
    var a = [5]int{1, 2, 3, 4, 5}
    var r [5]int

    fmt.Println(&quot;original a =&quot;, a)

    p := &amp;a
    for i, v := range p {
        if i == 0 {
            p[1] = 12
            p[2] = 13
        }
        r[i] = v
    }

    fmt.Println(&quot;after for range loop, r =&quot;, r)
    fmt.Println(&quot;after for range loop, a =&quot;, a)
}

original a = [1 2 3 4 5]
after for range loop, r = [1 12 13 4 5]
after for range loop, a = [1 12 13 4 5]</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/05/93/3c3f2a6d.jpg" width="30px"><span>安石</span> 👍（0） 💬（1）<div>实现类似于切片的效果，就是模拟切片咯，使用指针</div>2024-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/cc/70/64045bc0.jpg" width="30px"><span>人言有力</span> 👍（0） 💬（1）<div>本节讲解了go循环for语句语法。
1、仅有这一种循环结构 for preStam;condition;postStam {body}，除了循环体其他都是可选
2、支持continue和break，以及带label的循环跳转，解决循环嵌套场景的问题
3、for range语法糖支持数组、切片、map、channel等迭代器，更方便
4、注意for range本质是拷贝一个副本，所以遇到数组小心值传递问题；map小心无序问题；以及循环变量重用的问题</div>2024-05-14</li><br/><li><img src="" width="30px"><span>Geek_73c432</span> 👍（0） 💬（2）<div>关于参与循环的是 range 表达式的副本那里，有些同学对 range 后面的 a 和循环体里面的 a 是不是同一个有疑问。其实例子的输出已经说明了，如果是同一个的话，r 的值理应和 a 的值一样。

其实在汇编代码中看得更加清楚：
        MOVQ    $0, main.a+80(SP)
        MOVQ    $1, main.a+88(SP)
        MOVQ    $2, main.a+96(SP)
        MOVQ    $3, main.a+104(SP)
        MOVQ    $4, main.a+112(SP)
        MOVUPS  X15, main.r+40(SP)
        MOVUPS  X15, main.r+48(SP)
        MOVUPS  X15, main.r+64(SP)
        MOVQ    main.a+80(SP), CX
        MOVQ    CX, main..autotmp_14+120(SP)
        MOVUPS  main.a+88(SP), X0
        MOVUPS  X0, main..autotmp_14+128(SP)
        MOVUPS  main.a+104(SP), X0
        MOVUPS  X0, main..autotmp_14+144(SP)
        XORL    AX, AX
        NOP
        JMP     main_main_pc138
main_main_pc130:
        MOVQ    CX, main.r+40(SP)(AX*8)
        INCQ    AX
main_main_pc138:
        CMPQ    AX, $5
        JGE     main_main_pc174
        MOVQ    main..autotmp_14+120(SP)(AX*8), CX
        TESTQ   AX, AX
        JNE     main_main_pc130
        MOVQ    $11, main.a+88(SP)
        MOVQ    $12, main.a+96(SP)
        JMP     main_main_pc130

首先初始化了 a 和 r 两个数组，然后把 a 的值都拷贝到 main..autotmp_14+120(SP) 到main..autotmp_14+144(SP) 中，这个就是 a 的副本。然后跳转到 pc138 这个 label 处执行，然后跳转到 pc130 处执行，可以看到这两条指令：

MOVQ    main..autotmp_14+120(SP)(AX*8), CX
MOVQ    CX, main.r+40(SP)(AX*8)

每次都是从副本把值放到 CX 寄存器（应该吧）中，然后从 CX 中读出来放入 数组 r 中，不会从数组 a 中取

MOVQ    $11, main.a+88(SP)
MOVQ    $12, main.a+96(SP)
这两条指令是对应源码 a[1] = 11, a[2] = 12，操作的就是原来的数组 a

以上内容都是我从 GPT 现学的，如果有说的不正确的地方，还请大家指正</div>2024-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/54/dc/b4fa71cf.jpg" width="30px"><span>小凡</span> 👍（0） 💬（1）<div>for range sl { &#47;&#47; ... }
老师，这种写法同时省略了key和value，有什么意义吗。</div>2023-11-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ8ic8eLTo5rnqIMJicUfpkVBrOUJAW4fANicKIbHdC54O9SOdwSoeK6o8icibaUbh7ZUXAkGF9zwHqo0Q/132" width="30px"><span>ivhong</span> 👍（0） 💬（1）<div>func main() {
	var a = []int{1, 2, 3, 4, 5}
	var r [5]int

	fmt.Println(&quot;original a =&quot;, a)

	for i, v := range a {
		if i == 0 {
			a[1] = 12
			a[2] = 13
		}
		r[i] = v
	}

	fmt.Println(&quot;after for range loop, r =&quot;, r)
	fmt.Println(&quot;after for range loop, a =&quot;, a)
}</div>2022-03-15</li><br/>
</ul>