你好，我是Tony Bai。

上一节课，我们学习了Go语言中最常用的两个复合类型：数组与切片。它们代表**一组连续存储的同构类型元素集合。**不同的是，数组的长度是确定的，而切片，我们可以理解为一种“动态数组”，它的长度在运行时是可变的。

这一节课，我们会继续前面的脉络，学习另外一种日常Go编码中比较常用的复合类型，这种类型可以让你将一个值（Value）唯一关联到一个特定的键（Key）上，可以用于实现特定键值的快速查找与更新，这个复合数据类型就是 **map**。很多中文Go编程语言类技术书籍都会将它翻译为映射、哈希表或字典，但在我的课程中，**为了保持原汁原味，我就直接使用它的英文名，map**。

map是我们继切片之后，学到的第二个由Go编译器与运行时联合实现的复合数据类型，它有着复杂的内部实现，但却提供了十分简单友好的开发者使用接口。这一节课，我将从map类型的定义，到它的使用，再到map内部实现机制，由浅到深地让你吃透map类型。

## 什么是map类型？

map是Go语言提供的一种抽象数据类型，它表示一组无序的键值对。在后面的讲解中，我们会直接使用key和value分别代表map的键和值。而且，map集合中每个key都是唯一的：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/lfMbV8RibrhFxjILg4550cZiaay64mTh5Zibon64TiaicC8jDMEK7VaXOkllHSpS582Jl1SUHm6Jib2AticVlHibiaBvUOA/132" width="30px"><span>用0和1改变自己</span> 👍（37） 💬（3）<div>可以用一个有序结构存储key,如slice,然后for这个slice,用key获取值。资料来源至：https:&#47;&#47;go.dev&#47;blog&#47;maps</div>2021-11-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLBFkSq1oiaEMRjtyyv4ZpCI0OuaSsqs04ODm0OkZF6QhsAh3SvqhxibS2n7PLAVZE3QRSn5Hic0DyXg/132" width="30px"><span>ddh</span> 👍（19） 💬（3）<div>请问一下老师， map 元素不能寻址， 是因为动态扩容， 那么切片不也有动态扩容吗。 为什么切片元素可以寻址呢？  难道切片动态扩容之后， 它的元素地址不会变吗</div>2022-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/c9/5d03981a.jpg" width="30px"><span>thomas</span> 👍（17） 💬（2）<div>go团队为什么要故意把map的遍历设置为随机？</div>2022-04-12</li><br/><li><img src="" width="30px"><span>Geek_244c46</span> 👍（13） 💬（2）<div>map的key和value的值，是否可以为null</div>2022-05-26</li><br/><li><img src="" width="30px"><span>flexiver</span> 👍（7） 💬（1）<div>老师，想请问一下，hmap这个结构中的extra字段， 在key和value都不是指针的情况下，会存储所有的overflow bucket的指针，里面有提到一个内联，这个内联是什么意思？以及为什么当key和value都不是指针的情况下，会将bucket中的overflow指针全部放到extra字段存储</div>2022-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/d7/5315f6ce.jpg" width="30px"><span>不负青春不负己🤘</span> 👍（6） 💬（1）<div>可以把key 赋值到变量，使用sort 排序，在遍历</div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（5） 💬（2）<div>老师我想问下这里：
“如果是因为 overflow bucket 过多导致的“扩容”，实际上运行时会新建一个和现有规模一样的 bucket 数组，然后在 assign 和 delete 时做排空和迁移。”
如果bucket规模不变的话，那所有key在hash之后还是分到原来的桶中，好像该overflow还是会overflow？主要是因为这里既没有通过真正增加桶的数量实现扩容，也没有通过更换hash函数改变key在桶中的分布，那么这个overflow的问题到底是怎么解决的呢？谢谢老师</div>2022-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/da/0a8bc27b.jpg" width="30px"><span>文经</span> 👍（4） 💬（1）<div>我看了《Go语言实践》，《Go专家编程》，《Go语言底层原理剖析》这几本书对map的描述，对比才发现白老师讲得最清晰，在封装和细节方面拿捏得最好，大大地赞👍 剩下不清楚的地方就只能自己看源码了。</div>2022-01-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLBFkSq1oiaEMRjtyyv4ZpCI0OuaSsqs04ODm0OkZF6QhsAh3SvqhxibS2n7PLAVZE3QRSn5Hic0DyXg/132" width="30px"><span>ddh</span> 👍（4） 💬（2）<div>把key存到有序切片中，用切片遍历</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/b1/f89a84d0.jpg" width="30px"><span>wu526</span> 👍（3） 💬（1）<div>老师，请问一下如果是因为overflow bucket过多导致的&quot;扩容&quot;, 是否可以理解为这个hash函数的算法不太合理，导致大部分的key都分配到了一个bucket中，是否可以通过修改hash算法来重新hash一遍呢？</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0c/46/dfe32cf4.jpg" width="30px"><span>多选参数</span> 👍（3） 💬（2）<div>突然想到之前碰到的一个问题，就是golang 结构体作为map的元素时，不能够直接赋值给结构体的某个字段。这个也有“Go 不允许获取 map 中 value 的地址”的原因在嘛？假如这样的话，那么为什么读结构体中的某个字段是可以的？</div>2021-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/26/bc/a73e4275.jpg" width="30px"><span>TonyGao</span> 👍（3） 💬（2）<div>func doIteration(m map[int]int) {
	mu.RLock()
	defer mu.RUnlock()

	keys := []int{}

	for k := range m {
		keys = append(keys, k)
	}

	sort.SliceStable(keys, func(x, y int) bool {
		return x &lt; y
	})

	for _, k := range keys {
		fmt.Printf(&quot;[%d, %d] &quot;, k, m[k])
	}

	fmt.Println()
}

func doWrite(m map[int]int) {
	mu.Lock()
	defer mu.Unlock()

	for k, v := range m {
		m[k] = v + 1
	}
}

==&gt; 对并发示例代码的稳定排序输出 (原例1000次输出太多，输出前10个作为说明)：
[1, 11] [2, 12] [3, 13] 
[1, 12] [2, 13] [3, 14] 
[1, 13] [2, 14] [3, 15] 
[1, 14] [2, 15] [3, 16] 
[1, 15] [2, 16] [3, 17] 
[1, 16] [2, 17] [3, 18] 
[1, 17] [2, 18] [3, 19] 
[1, 18] [2, 19] [3, 20] 
[1, 19] [2, 20] [3, 21] 
[1, 20] [2, 21] [3, 22] 
。。。</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6e/6f/44da923f.jpg" width="30px"><span>邹志鹏.Joey ⁷⁷⁷</span> 👍（2） 💬（1）<div>既切片之后, 应该是 &quot;继切片之后&quot;?</div>2023-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/97/1f/2a68c980.jpg" width="30px"><span>不说话装糕手</span> 👍（2） 💬（1）<div>关于老师并发读写map的示例，做了如下修改
	&#47;&#47;go func() {
	&#47;&#47;	for i := 0; i &lt; 1000; i++ {
	&#47;&#47;		doIteration(m)
	&#47;&#47;	}
	&#47;&#47;}()

	go func() {
		for i := 0; i &lt; 10000; i++ {
			doWrite(m)
		}
	}()

	time.Sleep(5 * time.Second)
	fmt.Println(m)
	
output:
map[1:10011 2:10012 3:10013]
进程 已完成，退出代码为 0

我本地是1.16版本，看起来是可以并发写的？</div>2022-10-20</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/wgMMrp1hvSB3E30KqZvMsj3KQdAI3T1uQM77LT7hZ65nVSjPGRg3AbUOyiahnssA6AIT5PAkyHFmlTBzUH9gdyQ/132" width="30px"><span>pythonbug</span> 👍（2） 💬（1）<div>func sortMap(m map[string]int) {
	&#47;&#47; 存key
	var s []string
	for k, _ := range m {
		s = append(s, k)
	}

	&#47;&#47; 对s进行排序
	sort.Strings(s)

	&#47;&#47; 遍历输出
	for _, v := range s {
		fmt.Println(v, m[v])
	}
}</div>2022-10-09</li><br/><li><img src="" width="30px"><span>Geek_d86547</span> 👍（2） 💬（1）<div>老师 map遍历的随机性可以再详细说明一些嘛？</div>2022-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/8c/60/58b6c39e.jpg" width="30px"><span>zzy</span> 👍（2） 💬（1）<div>想问下golang为何不像java那样，在底层使用红黑树，性能应该是更好的</div>2022-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/2e/ca/469f7266.jpg" width="30px"><span>菠萝吹雪—Code</span> 👍（2） 💬（1）<div>彩！只要key是有序的并且访问顺序是固定的，value也就可以确定顺序了，通过切片、数组可以实现</div>2022-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9d/cd/c21a01dd.jpg" width="30px"><span>W-T</span> 👍（2） 💬（1）<div>老师，自定义数据类型能否支持for range语句，支持的话需要实现什么接口</div>2022-06-22</li><br/><li><img src="" width="30px"><span>大帅哥</span> 👍（2） 💬（1）<div>想问一下，当map扩容后，有新的数据插入是，如果此时数据还没有迁移到新的bucket中，那么runtime是怎么知道这个可以是在olderbuckets和buckets的具体位置的，是不是计算规则不一样，但是这个规则具体是怎么样的？</div>2022-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/12/f0c145d4.jpg" width="30px"><span>Rayjun</span> 👍（2） 💬（1）<div> 老师，问一下关于 bucket 的问题，既然 bucket 是数组，如果 key 和 value 的类型不一样，要怎么存储呢？而且下面还需要存储 overflow bucket 的指针</div>2022-03-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/QPLkhJ3CoNt0j4ccGovE8tp7ma097vMrKbEq3jefQZNxI6psShxXxqMWTtI4T7oV0Jqq2KnWREnsJwkkZwnJ8Q/132" width="30px"><span>Geek_f654de</span> 👍（2） 💬（1）<div>思考题：
1.把map的key拿出来，放到切片里
2.对切片进行排序
3.取出切片中元素对应的value</div>2022-02-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep7c7UKsjRiclaAqD9vMHSUXayzrvRhvic3Lm6ibX82L3DibJnCCtDmB3OfxbuVjetpT6Qa8IuwqZCWlw/132" width="30px"><span>Geek_2337af</span> 👍（2） 💬（1）<div>go是否支持利用自定义的哈希函数创建map呢</div>2022-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/43/23/d98fb8f7.jpg" width="30px"><span>Niverkk</span> 👍（2） 💬（1）<div>老师好，有几个问题请教下
问题1：
1.v := m[&quot;key&quot;] → v := runtime.mapaccess1(maptype, m, &quot;key&quot;)
2.v, ok := m[&quot;key&quot;] → v, ok := runtime.mapaccess2(maptype, m, &quot;key&quot;)
其实这两种写法调用的底层方法是不一样的，2他会返回两个值，v是对应的value， ok代表key是否存在于map中？

问题2：
value存储区域kv格式为什么需要对齐？

问题3：
如果是因为当前数据数量超出 LoadFactor 指定水位而进行的扩容，那么运行时会建立一个两倍于现有规模的 bucket 数组，但真正的排空和迁移工作也是在 assign 和 delete 时逐步进行的。

对于这段话，逐步迁移是什么意思？assign代表增加吗？删除跟扩容有关系吗，删除应该是影响缩容吧？</div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2c/68/c299bc71.jpg" width="30px"><span>天敌</span> 👍（2） 💬（1）<div>老师, tophash区域存的是指针吗？当两个key的hashcode完全一样又是如何处理的？</div>2022-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/da/0a8bc27b.jpg" width="30px"><span>文经</span> 👍（2） 💬（1）<div>v, ok := m[&quot;key1&quot;]
v := m[&quot;key1&quot;]
白老师，这两种方式都可以，请问comma，OK， 这种方式是函数实现的吗？如果是函数的话，怎么一个函数可以同时返回一个值，或者两个值？ channel也有类似的用法，不太理解。
</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/da/0a8bc27b.jpg" width="30px"><span>文经</span> 👍（2） 💬（1）<div>&quot;但 map 类型，因为它内部实现的复杂性，无法“零值可用”。所以，如果我们对处于零值状态的 map 变量直接进行操作，就会导致运行时异常（panic），从而导致程序进程异常退出。&quot;

白老师，我理解零值可用，既可以把变量当做nil来使用，又可以当做一个初始化好的对象来使用。这样对吗？有两个进一步的疑问
1. slice 的零值初始化是怎么实现的，编译器和运行时分别扮演了什么角色。
2. map的零值初始化难在哪里，按照我的理解，只要在编译的时候判断是否为nil，运行的时候发现它是nil，给它分配一个对象就可以了。肯定是我遗漏了哪些重要的信息，请白老师解惑。</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4b/ea/a9e7bc50.jpg" width="30px"><span>℡人见人爱浩然君゜</span> 👍（1） 💬（1）<div>package main

import (
	&quot;fmt&quot;
	&quot;sort&quot;
)

func main(){
	m := map[string]int{ &#47;&#47;初始化一个map类型的变量m
		&quot;apple&quot;:1,
		&quot;banana&quot;:2,
		&quot;cherry&quot;:3,
	}
	keySlice := make([]string,0,len(m)) &#47;&#47;创建一个切片，长度是m的长度
	&#47;&#47;遍历m获取map类型的key并存到keySlice中
        for k := range m {
		keySlice = append(keySlice, k)
	}
	&#47;&#47; 对mySlice排序
	sort.Strings(keySlice)
        &#47;&#47;通过遍历有序key的方式获取map的值
	for _,v := range keySlice{
		fmt.Println(v,m[v])
	}
}</div>2023-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/45/b2/24dee83c.jpg" width="30px"><span>Ppppppp</span> 👍（1） 💬（1）<div>syncmap适合的场景好像不是很多。

The Map type is specialized. Most code should use a plain Go map instead, with separate locking or coordination, for better type safety and to make it easier to maintain other invariants along with the map content.

The Map type is optimized for two common use cases: (1) when the entry for a given key is only ever written once but read many times, as in caches that only grow, or (2) when multiple goroutines read, write, and overwrite entries for disjoint sets of keys. In these two cases, use of a Map may significantly reduce lock contention compared to a Go map paired with a separate Mutex or RWMutex.</div>2023-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/4d/7ba09ff0.jpg" width="30px"><span>郑童文</span> 👍（1） 💬（1）<div>请问有了tophash区域为什么还需要key区域呢？tophash就是用来决定key存储的位置的啊</div>2022-11-09</li><br/>
</ul>