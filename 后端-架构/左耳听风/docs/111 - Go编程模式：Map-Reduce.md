你好，我是陈皓，网名左耳朵耗子。

这节课，我们来学习一下函数式编程中非常重要的Map、Reduce、Filter这三种操作。这三种操作可以让我们轻松灵活地进行一些数据处理，毕竟，我们的程序大多数情况下都在倒腾数据。尤其是对于一些需要统计的业务场景来说，Map、Reduce、Filter是非常通用的玩法。

话不多说，我们先来看几个例子。

## 基本示例

### Map示例

在下面的程序代码中，我写了两个Map函数，这两个函数需要两个参数：

- 一个是字符串数组 `[]` `string`，说明需要处理的数据是一个字符串；
- 另一个是一个函数func(s string) string 或 func(s string) int。

```
func MapStrToStr(arr []string, fn func(s string) string) []string {
    var newArray = []string{}
    for _, it := range arr {
        newArray = append(newArray, fn(it))
    }
    return newArray
}

func MapStrToInt(arr []string, fn func(s string) int) []int {
    var newArray = []int{}
    for _, it := range arr {
        newArray = append(newArray, fn(it))
    }
    return newArray
}
```

整个Map函数的运行逻辑都很相似，函数体都是在遍历第一个参数的数组，然后，调用第二个参数的函数，把它的值组合成另一个数组返回。

因此，我们就可以这样使用这两个函数：

```
var list = []string{"Hao", "Chen", "MegaEase"}

x := MapStrToStr(list, func(s string) string {
    return strings.ToUpper(s)
})
fmt.Printf("%v\n", x)
//["HAO", "CHEN", "MEGAEASE"]

y := MapStrToInt(list, func(s string) int {
    return len(s)
})
fmt.Printf("%v\n", y)
//[3, 4, 8]
```

可以看到，我们给第一个 `MapStrToStr()` 传了功能为“转大写”的函数，于是出来的数组就成了全大写的，给`MapStrToInt()` 传的是计算长度，所以出来的数组是每个字符串的长度。

我们再来看一下Reduce和Filter的函数是什么样的。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJcwXucibksEYWRmibTZj9pb3d5ibfVQHFS9shvJmgMgtN3BM3r9qiaL5YTZSFdLvPZiaEHfBia4dFODVqw/132" width="30px"><span>北国骑士</span> 👍（11） 💬（1）<div>所以我觉得用go写业务逻辑真的是件很sb的事情</div>2021-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（2） 💬（1）<div>就是因为go最初不支持泛型，所以每个go框架都要搞一堆的代码生成器来生成重复代码，恶心的不要不要的</div>2022-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c1/57/27de274f.jpg" width="30px"><span>萧</span> 👍（1） 💬（0）<div>通俗易懂</div>2021-02-18</li><br/><li><img src="" width="30px"><span>Refrain</span> 👍（0） 💬（1）<div>verifyFuncSignature(fn, elemType, nil) 为什么要传一个空值呢？

outType := types[len(types)-1] 这个地方outType必然是空值
</div>2021-02-05</li><br/>
</ul>