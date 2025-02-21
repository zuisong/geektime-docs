你好，我是孔令飞。

今天我们更新一期特别放送作为加餐。在 [特别放送 | Go Modules依赖包管理全讲](https://time.geekbang.org/column/article/416397)中，我介绍了Go Modules的知识，里面内容比较多，你可能还不知道具体怎么使用Go Modules来为你的项目管理Go依赖包。

这一讲，我就通过一个具体的案例，带你一步步学习Go Modules的常见用法以及操作方法，具体包含以下内容：

1. 准备一个演示项目。
2. 配置Go Modules。
3. 初始化Go包为Go模块。
4. Go包依赖管理。

## 准备一个演示项目

为了演示Go Modules的用法，我们首先需要一个Demo项目。假设我们有一个hello的项目，里面有两个文件，分别是hello.go和hello\_test.go，所在目录为`/home/lk/workspace/golang/src/github.com/marmotedu/gopractise-demo/modules/hello`。

hello.go文件内容为：

```go
package hello

func Hello() string {
	return "Hello, world."
}
```

hello\_test.go文件内容为：

```go
package hello

import "testing"

func TestHello(t *testing.T) {
	want := "Hello, world."
	if got := Hello(); got != want {
		t.Errorf("Hello() = %q, want %q", got, want)
	}
}
```
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/25/06/13/e4f9f79b.jpg" width="30px"><span>你赖东东不错嘛</span> 👍（5） 💬（1）<div>1. 项目根目录下，执行go get -d -u .&#47;...
2. 在外网环境把package下载到vendor目录下，在无网环境用go vendor构建应用。</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/45/be/a4182df4.jpg" width="30px"><span>2035去台湾</span> 👍（1） 💬（1）<div>客户练习2目前我们使用了nexus代理</div>2021-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（2）<div>go test 没有自动下载依赖，是需要配置什么吗？</div>2022-04-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ge7uhlEVxicQT73YuomDPrVKI8UmhqxKWrhtO5GMNlFjrHWfd3HAjgaSribR4Pzorw8yalYGYqJI4VPvUyPzicSKg/132" width="30px"><span>陈东</span> 👍（0） 💬（1）<div>go构建约束问题，Build constraints exclude all Go files in ？
尝试以下办法解决不了
1、searcheverything 搜索后删除所有包,
$GOPATH目录下，把对应的包删除，重新go get,还是不行.
2、go get -u -v github.com&#47;karalabe&#47;xgo
3、Right click -&gt; Mark folder as not excluded.
4、引用包报错，重启电脑，查看goproxy配置，还不行重装goland
怎么解决，寻求老师帮助，谢谢。</div>2021-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/b0/d3/200e82ff.jpg" width="30px"><span>功夫熊猫</span> 👍（0） 💬（1）<div>有没有办法就是直接导入本地包。而不是设置代理</div>2021-11-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJkOj8VUxLjDKp6jRWJrABnnsg7U1sMSkM8FO6ULPwrqNpicZvTQ7kwctmu38iaJYHybXrmbusd8trg/132" width="30px"><span>yss</span> 👍（0） 💬（2）<div>2. 我们内网机是与外网物理隔离的机器，使用 vendor在内网机构建是我们的解决方案。</div>2021-10-28</li><br/>
</ul>