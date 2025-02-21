你好，我是孔令飞。

[上一讲](https://time.geekbang.org/column/article/408529)，我介绍了Go中的两类测试：单元测试和性能测试。在Go中，还有一些其他的测试类型和测试方法，值得我们去了解和掌握。此外，IAM项目也编写了大量测试用例，这些测试用例使用了不同的编写方法，你可以通过学习IAM的测试用例来验证你学到的测试知识。

今天，我就来介绍下Go 语言中的其他测试类型：示例测试、TestMain函数、Mock测试、Fake测试等，并且介绍下IAM项目是如何编写和运行测试用例的。

## 示例测试

示例测试以`Example`开头，没有输入和返回参数，通常保存在`example_test.go`文件中。示例测试可能包含以`Output:`或者`Unordered output:`开头的注释，这些注释放在函数的结尾部分。`Unordered output:`开头的注释会忽略输出行的顺序。

执行`go test`命令时，会执行这些示例测试，并且go test会将示例测试输出到标准输出的内容，跟注释作对比（比较时将忽略行前后的空格）。如果相等，则示例测试通过测试；如果不相等，则示例测试不通过测试。下面是一个示例测试（位于example\_test.go文件中）：

```go
func ExampleMax() {
    fmt.Println(Max(1, 2))
    // Output:
    // 2
}
```
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/2e/7e/ebc28e10.jpg" width="30px"><span>NULL</span> 👍（2） 💬（1）<div>go1.18又新增了一种fuzzing测试
https:&#47;&#47;go.dev&#47;doc&#47;fuzz&#47;</div>2022-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/47/bd/3c88b41b.jpg" width="30px"><span>Geek_zwip3b</span> 👍（1） 💬（1）<div>静态检查吧，不是竞态检查</div>2022-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/d4/1b/82a32d66.jpg" width="30px"><span>是在下输了</span> 👍（0） 💬（1）<div>在目录下执行go test -coverprofile=coverage.out 没有生成 coverage.out 文件</div>2022-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/26/34/891dd45b.jpg" width="30px"><span>宙斯</span> 👍（0） 💬（1）<div>fake测试和mock测试有什么区别吗？感觉是一样的东西，没看出侧重点</div>2022-06-29</li><br/><li><img src="" width="30px"><span>~\(≧▽≦)/~</span> 👍（0） 💬（1）<div>老师，调用第三方rest api接口需要用到mock进行测试吗</div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（0） 💬（2）<div>老师，请教一下，一般对 rest api 的测试 应该怎么做比较好，
我们现在是 按照写单元测试的方式， 测试函数内 调用http请求，判断response。
不知道有没有更好的方式。</div>2021-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/de/97/cda3f551.jpg" width="30px"><span>倪昊</span> 👍（0） 💬（1）<div>老师请问单元测试一般对哪几部分代码做呢？控制层，service层，仓库层都要做吗？</div>2021-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fc/55/e03bb6db.jpg" width="30px"><span>i-neojos</span> 👍（4） 💬（0）<div>这篇文章实用性特别强，对测试平台很有参考意义</div>2022-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2e/7e/ebc28e10.jpg" width="30px"><span>NULL</span> 👍（1） 💬（0）<div>bouk&#47;monkey许可证好像有问题

也可以看看这个 https:&#47;&#47;github.com&#47;agiledragon&#47;gomonkey

agiledragon&#47;gomonkey被bouk&#47;monkey的作者推荐过, 见https:&#47;&#47;esoteric.codes&#47;blog&#47;bouk-monkey-satirical-code-used-by-people-who-dont-get-the-joke</div>2022-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/68/d4/c9b5d3f9.jpg" width="30px"><span>💎A</span> 👍（0） 💬（0）<div>越到后面人越少</div>2022-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b2/91/714c0f07.jpg" width="30px"><span>zero</span> 👍（0） 💬（0）<div>收获满满</div>2021-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（0） 💬（0）<div>总结：
1. 介绍了Example、Mock、Fake 测试规范，以及常见的框架。
2. 重点介绍了 gomock package 的使用方法。包括运行 mockgen 的两种方式：source mode &amp; reflect mode；如何对输入和输出参数的约束。
3. 对于复杂的 interface，你也可以采用自己实现fake测试。
4. iam 提供了 make test 和 make cover 两个命令。</div>2021-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/60/4f/db0e62b3.jpg" width="30px"><span>Daiver</span> 👍（0） 💬（0）<div>其实可以把自动生成mock和 test 放makefile中管理</div>2021-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/83/17/df99b53d.jpg" width="30px"><span>随风而过</span> 👍（0） 💬（0）<div>一般开发中就做了单元测试和mock测试。而且还都是手写，CV复制，没想到还有大量工具来自动生成，包括很多测试框架，gei到了</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（0） 💬（1）<div>介绍了示例测试、TestMain 测试、Mock 测试、Fake 测试，加上上一讲中的单元测试和性能测试，共6种测试类型。
文中提供了每种测试的示例，可以作为测试方法大全，供后续需要的时候查看。</div>2021-08-19</li><br/>
</ul>