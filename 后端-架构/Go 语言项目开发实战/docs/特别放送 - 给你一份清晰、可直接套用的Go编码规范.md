你好，我是孔令飞。

我们在上一讲学习了“写出优雅Go项目的方法论”，那一讲内容很丰富，是我多年Go项目开发的经验沉淀，需要你多花一些时间好好消化吸收。吃完大餐之后，咱们今天来一期特别放送，就是上一讲我提到过的编码规范。这一讲里，为了帮你节省时间和精力，我会给你一份清晰、可直接套用的 Go 编码规范，帮助你编写一个高质量的 Go 应用。

这份规范，是我参考了Go官方提供的编码规范，以及Go社区沉淀的一些比较合理的规范之后，加入自己的理解总结出的，它比很多公司内部的规范更全面，你掌握了，以后在面试大厂的时候，或者在大厂里写代码的时候，都会让人高看你一眼，觉得你code很专业。

这份编码规范中包含代码风格、命名规范、注释规范、类型、控制结构、函数、GOPATH 设置规范、依赖管理和最佳实践九类规范。如果你觉得这些规范内容太多了，看完一遍也记不住，这完全没关系。你可以多看几遍，也可以在用到时把它翻出来，在实际应用中掌握。这篇特别放送的内容，更多是作为写代码时候的一个参考手册。

## 1. 代码风格

### 1.1 代码格式

- 代码都必须用 `gofmt` 进行格式化。
- 运算符和操作数之间要留空格。
- 建议一行代码不超过120个字符，超过部分，请采用合适的换行方式换行。但也有些例外场景，例如import行、工具自动生成的代码、带tag的struct字段。
- 文件长度不能超过800行。
- 函数长度不能超过80行。
- import规范
  
  - 代码都必须用 goimports进行格式化（建议将代码Go代码编辑器设置为：保存时运行 goimports）。  
    \- 不要使用相对路径引入包，例如 import …/util/net 。  
    \- 包名称与导入路径的最后一个目录名不匹配时，或者多个相同包名冲突时，则必须使用导入别名。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/2e/7e/ebc28e10.jpg" width="30px"><span>NULL</span> 👍（11） 💬（2）<div>不认同的地方:
4.1字符串, 空字符串的判断
两种方式都可以
详见: https:&#47;&#47;stackoverflow.com&#47;questions&#47;18594330&#47;what-is-the-best-way-to-test-for-an-empty-string-in-go

4.2切片, 空 slice 判断
应该是&quot;如果你需要测试一个slice是否是空的，使用len(s) == 0来判断，而不应该用s == nil来判断&quot;
详见Go语言圣经: https:&#47;&#47;books.studygolang.com&#47;gopl-zh&#47;ch4&#47;ch4-02.html

描述不够准确定地方:
4.2切片, 声明 slice
描述不够准确
详见: https:&#47;&#47;github.com&#47;golang&#47;go&#47;wiki&#47;CodeReviewComments#declaring-empty-slices
补充: 可以根据需要指定cap, 减少内存分配次数, 降低gc压力, 如 make([]int, 0, 100)

6.函数, 尽量采用值传递，而非指针传递。
描述不够准确
详见: https:&#47;&#47;github.com&#47;golang&#47;go&#47;wiki&#47;CodeReviewComments#pass-values

6.1 函数参数, 尽量用值传递，非指针传递。
描述不够准确
详见: https:&#47;&#47;github.com&#47;golang&#47;go&#47;wiki&#47;CodeReviewComments#pass-values

6.函数, 传入参数是 map、slice、chan、interface ，不要传递指针。
描述不够准确, 如果是slice, 并且有append操作, 并且期望改变可以影响原函数, 应当传递指针
这与slice的底层结构有关, 两个value, 一个 pointer
这在&quot;9.2 注意事项&quot;第一条也有说明
详见: https:&#47;&#47;github.com&#47;golang&#47;go&#47;blob&#47;master&#47;src&#47;runtime&#47;slice.go#L22

9. 最佳实践, 在编译时验证接口的符合性，例如：
描述不够准确
详见: https:&#47;&#47;github.com&#47;xxjwxc&#47;uber_go_guide_cn#toc8</div>2022-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/a9/66/2df6b3fe.jpg" width="30px"><span>滴滴答答</span> 👍（11） 💬（2）<div>为什么函数参数尽量不用指针传递？如果是一个比较大的结构体，传指针不是更好吗？</div>2021-06-17</li><br/><li><img src="" width="30px"><span>苳冬</span> 👍（3） 💬（1）<div>驼峰命名 APIClient、UserID，如果遇到API+ID就是APIID这样连续两个全大写可读性很低啊</div>2021-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/63/84/f45c4af9.jpg" width="30px"><span>Vackine</span> 👍（3） 💬（1）<div>在1.2初始化结构体引用时，给的案例里面bad 和good的sval的方式是一模一样的啊？还有在切片初始化时不都建议提前制定容量，然后后面为什么在声明slice是时候，又不建议make的方式而用var 的方式？</div>2021-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/1d/69/c21d2644.jpg" width="30px"><span>josephzxy</span> 👍（2） 💬（4）<div>想问1.2节里为什么“对于未导出的顶层常量和变量，使用 _ 作为前缀。”，有什么作用吗？首字母小写不是已经表明是未导出(unexported)了吗？谢谢！</div>2021-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/11/d7e08b5b.jpg" width="30px"><span>dll</span> 👍（2） 💬（1）<div>注释写中文才能说清楚的情况，该怎么规范注释呢</div>2021-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4b/24/8c9eaf7f.jpg" width="30px"><span>Seven</span> 👍（2） 💬（1）<div>为方便团队都使用这份规范，需要写到开发文档里。请问这篇规范可以给个GitHub链接吗？这样方便更多人用，当然注明来自本课程也可以让更多人慕名学习。</div>2021-06-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/5GQZCecntmOibVjWkMWVnibqXEZhAYnFiaRkgfAUGdrQBWzfXjqsYteLee6afDEjvBLBVa5uvtWYTTicwO2jKia0zOw/132" width="30px"><span>Geek_a4cca6</span> 👍（2） 💬（2）<div>老师，请问有学习班的群吗？</div>2021-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/37/1e/9b6554b6.jpg" width="30px"><span>Q</span> 👍（2） 💬（4）<div>空slice那里为啥要 先判断slice != nil 再判断 len(slice) &gt; 0 呢？不判断不可以吗？</div>2021-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/28/68/774b1619.jpg" width="30px"><span>Fan</span> 👍（1） 💬（1）<div>请问go web 的项目结构目录有标准吗？ 查资料查到一个社区标准（https:&#47;&#47;github.com&#47;golang-standards&#47;project-layout），但是褒贬不一。所以想问问您那的结构目录是怎么标准化的？</div>2021-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/56/115c6433.jpg" width="30px"><span>jssfy</span> 👍（1） 💬（1）<div>不要使用相对路径引入包，例如 import ..&#47;util&#47;net 。
请问这里是不是指不要用.或者..这种符号？引用内部子目录下的其他package应该还是允许的吧？</div>2021-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1d/c0/978fc470.jpg" width="30px"><span>dch666</span> 👍（1） 💬（4）<div>判断空字符串用 len(s) == 0 比 s == &quot;&quot; 好在哪呢</div>2021-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/2c/013afd74.jpg" width="30px"><span>夏夜星语</span> 👍（1） 💬（2）<div>请问我们现在的iam 项目代码已经完全写完了嘛，以后就都是这种理论课嘛？</div>2021-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e2/c7/3e1d396e.jpg" width="30px"><span>oneWalker</span> 👍（0） 💬（1）<div>这个规范可以给一份word版本的吗？或者推荐一下来源，我好做成flashcard培养编码规范习惯。</div>2022-05-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIW5xLKMIwlibBXdP5sGVqhXAGuLYk7XFBrhzkFytlKicjNpSHIKXQclDUlSbD9s2HDuOiaBXslCqVbg/132" width="30px"><span>Geek_f23c82</span> 👍（0） 💬（1）<div>1.2和6.5的第一条似乎是冲突的</div>2022-04-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIW5xLKMIwlibBXdP5sGVqhXAGuLYk7XFBrhzkFytlKicjNpSHIKXQclDUlSbD9s2HDuOiaBXslCqVbg/132" width="30px"><span>Geek_f23c82</span> 👍（0） 💬（1）<div>麻烦问下为什么在判断字符串是否相等时，bytes.Compare比bytes.Equal好？</div>2022-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/e9/29dfa621.jpg" width="30px"><span>小灰</span> 👍（0） 💬（1）<div>不太明白，为什么 &quot;pi&quot; 示例那里的变量名是 Price,不是 &quot;PI&quot; 这个变量名更好理解吗？</div>2022-01-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（1）<div>如果要直接修改 map 的 value 值，则 value 只能是指针，否则要覆盖原来的值。
传入时会复制的map的副本，类型为指针的value被修改，原map对应的value也被修改，如果这个value不是指针类型，修改后不是也会覆盖掉原来map的value吗</div>2021-12-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（2）<div>在编译时验证接口的符合性，例如：
type LogHandler struct {
  h   http.Handler
  log *zap.Logger
}
var _ http.Handler = LogHandler{}
这里说的接口是指什么，没有太理解，能否给一个更具体的例子
</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/89/11/4300024e.jpg" width="30px"><span>不平凡的路</span> 👍（0） 💬（1）<div>在初始化结构引用时，请使用 &amp;T{}代替 new(T)，以使其与结构体初始化一致。  为什么使用&amp;T 而不是new 
</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1d/53/224591fb.jpg" width="30px"><span>Archer</span> 👍（0） 💬（1）<div>包名以及包所在的目录名，不要使用复数，例如，是net&#47;utl，而不是net&#47;urls 这里写错成utl了</div>2021-11-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLJ86tichGXtZMLLhicb8V0wJE92xdpQmVW1u06ZkT7BkvxyZMfWcVluyUdMrz0cBIkuX9MhXm2PZOQ/132" width="30px"><span>Geek_a15aca</span> 👍（0） 💬（1）<div>老师，之前课程中规范提到切片判空始终用len就好了，因为nil切片是一个有效的len为0的切片。所以判断是否为nil是bad的做法，为什么这里需要先判断nil呢？</div>2021-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6d/ef/08132ab2.jpg" width="30px"><span>万里</span> 👍（0） 💬（1）<div>老师好，判断空字符串用 len(s) == 0 比 s == &quot;&quot; 好在哪呢</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ed/0a/18201290.jpg" width="30px"><span>Juniper</span> 👍（0） 💬（1）<div>字符串去除前后子串的bad示例，strings.TrimPrefix(s1,s2)函数实现：
func TrimPrefix(s, prefix string) string {
	if HasPrefix(s, prefix) {
		return s[len(prefix):]
	}
	return s
}
可以看到，其实也是调用HasPrefix，然后做字符串切割操作，跟good示例的核心逻辑是一样的。但是当s2不是s1的子串时，bad示例s3就是s1的值，good示例s3是空字符串。我个人反而觉得bad示例更合理点，请老师解答下</div>2021-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/14/b488f241.jpg" width="30px"><span>o9</span> 👍（0） 💬（2）<div>大佬您好 【字符串是否包含子串或字符】 和 【去除前后子串】 
我使用 1.16.6 版本 benchmark 了一下 性能几乎没有差别啊</div>2021-09-28</li><br/><li><img src="" width="30px"><span>action</span> 👍（0） 💬（1）<div>建议一行代码不超过 120 行？？</div>2021-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（3） 💬（0）<div>终极规范：当遇到规范问题不知道如何处理时，立马查看文档！</div>2021-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/9a/52/93416b65.jpg" width="30px"><span>不明真相的群众</span> 👍（2） 💬（0）<div>作为一个新手，只能在实际应用的时候 再看翻看这章节</div>2021-06-17</li><br/><li><img src="" width="30px"><span>Geek_b797c1</span> 👍（2） 💬（0）<div>催更：更新太慢了</div>2021-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/9a/52/93416b65.jpg" width="30px"><span>不明真相的群众</span> 👍（1） 💬（0）<div>日常催更</div>2021-06-18</li><br/>
</ul>