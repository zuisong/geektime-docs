你好，我是孔令飞。今天我们更新一期特别放送作为加餐。

在Go项目开发中，依赖包管理是一个非常重要的内容，依赖包处理不好，就会导致编译失败。而且Go的依赖包管理有一定的复杂度，所以，我们有必要系统学习下Go的依赖包管理工具。

这一讲，我会首先介绍下Go依赖包管理工具的历史，并详细介绍下目前官方推荐的依赖包管理方案Go Modules。Go Modules主要包括了 `go mod` 命令行工具、模块下载机制，以及两个核心文件go.mod和go.sum。另外，Go Modules也提供了一些环境变量，用来控制Go Modules的行为。这一讲，我会分别介绍下这些内容。

在正式开始讲解这些内容之前，我们先来对Go Modules有个基本的了解。

## Go Modules简介

Go Modules是Go官方推出的一个Go包管理方案，基于vgo演进而来，具有下面这几个特性：

- 可以使包的管理更加简单。
- 支持版本管理。
- 允许同一个模块多个版本共存。
- 可以校验依赖包的哈希值，确保包的一致性，增加安全性。
- 内置在几乎所有的go命令中，包括`go get`、`go build`、`go install`、`go run`、`go test`、`go list`等命令。
- 具有Global Caching特性，不同项目的相同模块版本，只会在服务器上缓存一份。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/1d/69/c21d2644.jpg" width="30px"><span>josephzxy</span> 👍（11） 💬（3）<div>“思考下，如果不提交 go.sum，会有什么风险？”
如果go get时，GOSUMDB=off，就没有办法校验下载的包是否被篡改。

推荐两篇博文可做辅助阅读
https:&#47;&#47;zaracooper.github.io&#47;blog&#47;posts&#47;go-module-tidbits&#47;
https:&#47;&#47;insujang.github.io&#47;2020-04-04&#47;go-modules&#47;</div>2021-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ed/0a/18201290.jpg" width="30px"><span>Juniper</span> 👍（3） 💬（1）<div>问下老师，go get和go mod download的场景有什么不一样吗，不太明天go mod download这个命令的场景
</div>2021-09-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLDUJyeq54fiaXAgF62tNeocO3lHsKT4mygEcNoZLnibg6ONKicMgCgUHSfgW8hrMUXlwpNSzR8MHZwg/132" width="30px"><span>types</span> 👍（2） 💬（1）<div>go get如何拉取指定分支的指定commit id</div>2021-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>最后一个流程图中， GOSUMDB=off 的时候，还会和 go.sum 文件中的 hash 做对比吗？</div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>开启 go module 的环境变量 GO1111MODULE 为什么中间有 3个1？</div>2022-04-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ge7uhlEVxicQT73YuomDPrVKI8UmhqxKWrhtO5GMNlFjrHWfd3HAjgaSribR4Pzorw8yalYGYqJI4VPvUyPzicSKg/132" width="30px"><span>陈东</span> 👍（0） 💬（1）<div>goland构建module并引用方包logrus，能go run代码，但是logrus.Println 中的（Println ）一直显示红色报错，尝试很多办法，解决
go构建约束问题，错误提示是Build constraints exclude all Go files in c：代码目录文件夹？
尝试以下办法解决不了
1、searcheverything 搜索后删除所有包,
$GOPATH目录下，把对应的包删除，重新go get,还是不行.
2、go get -u -v github.com&#47;karalabe&#47;xgo
3、Right click -&gt; Mark folder as not excluded.
4、引用包报错，重启电脑，查看goproxy配置，重装goland等等都解决不了。
怎么解决，希望得到老师帮助，谢谢。</div>2021-12-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJkOj8VUxLjDKp6jRWJrABnnsg7U1sMSkM8FO6ULPwrqNpicZvTQ7kwctmu38iaJYHybXrmbusd8trg/132" width="30px"><span>yss</span> 👍（0） 💬（1）<div>如果不提交 go.sum，会有什么风险？

当别人使用项目并下载依赖时，无法验证他们使用的依赖和你开发时的依赖是否一致，存在下载到被篡改代码的风险</div>2021-10-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLDUJyeq54fiaXAgF62tNeocO3lHsKT4mygEcNoZLnibg6ONKicMgCgUHSfgW8hrMUXlwpNSzR8MHZwg/132" width="30px"><span>types</span> 👍（0） 💬（1）<div>go build或者go run的时候，如果依赖包都已经下载到 pkg&#47;mod下了，还会进行校验吗？？
自己测试了下已经是不会校验的</div>2021-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（0） 💬（4）<div>“如果不指定版本号，Go Modules 会根据自定义的规则，选择最小版本来下载。”，这里说的最小版本指的是latest版本吗</div>2021-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/0b/73628618.jpg" width="30px"><span>兔嘟嘟</span> 👍（4） 💬（0）<div>解惑了，整个中文互联网上都没这样好好讲go module的，至少我没找到。导致我一开始搞项目的时候，在某个地方纠结了好久</div>2021-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（2） 💬（0）<div>分析的真细致，厉害👍</div>2021-09-10</li><br/><li><img src="" width="30px"><span>biby</span> 👍（0） 💬（0）<div>之前看了许多篇go module的文章，都是很碎片的知识，学习完也没有完整认知，导致用的时候都是模模糊糊。这篇讲的完整细致，能系统的学习，开发使用的时候清晰很多。</div>2023-04-04</li><br/>
</ul>