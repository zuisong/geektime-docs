你好，我是孔令飞。

上一讲，我介绍了公有云厂商普遍采用的SDK设计方式。其实，还有一些比较优秀的SDK设计方式，比如 Kubernetes的 [client-go](https://github.com/kubernetes/client-go) SDK设计方式。IAM项目参考client-go，也实现了client-go风格的SDK：[marmotedu-sdk-go](https://github.com/marmotedu/marmotedu-sdk-go)。

和 [33讲](https://time.geekbang.org/column/article/406389) 介绍的SDK设计方式相比，client-go风格的SDK具有以下优点：

- 大量使用了Go interface特性，将接口的定义和实现解耦，可以支持多种实现方式。
- 接口调用层级跟资源的层级相匹配，调用方式更加友好。
- 多版本共存。

所以，我更推荐你使用marmotedu-sdk-go。接下来，我们就来看下marmotedu-sdk-go是如何设计和实现的。

## marmotedu-sdk-go设计

和medu-sdk-go相比，marmotedu-sdk-go的设计和实现要复杂一些，但功能更强大，使用体验也更好。

这里，我们先来看一个使用SDK调用iam-authz-server `/v1/authz` 接口的示例，代码保存在 [marmotedu-sdk-go/examples/authz\_clientset/main.go](https://github.com/marmotedu/marmotedu-sdk-go/blob/v1.0.3/examples/authz_clientset/main.go)文件中：

```go
package main

import (
	"context"
	"flag"
	"fmt"
	"path/filepath"

	"github.com/ory/ladon"

	metav1 "github.com/marmotedu/component-base/pkg/meta/v1"
	"github.com/marmotedu/component-base/pkg/util/homedir"

	"github.com/marmotedu/marmotedu-sdk-go/marmotedu"
	"github.com/marmotedu/marmotedu-sdk-go/tools/clientcmd"
)

func main() {
	var iamconfig *string
	if home := homedir.HomeDir(); home != "" {
		iamconfig = flag.String(
			"iamconfig",
			filepath.Join(home, ".iam", "config"),
			"(optional) absolute path to the iamconfig file",
		)
	} else {
		iamconfig = flag.String("iamconfig", "", "absolute path to the iamconfig file")
	}
	flag.Parse()

	// use the current context in iamconfig
	config, err := clientcmd.BuildConfigFromFlags("", *iamconfig)
	if err != nil {
		panic(err.Error())
	}

	// create the clientset
	clientset, err := marmotedu.NewForConfig(config)
	if err != nil {
		panic(err.Error())
	}

	request := &ladon.Request{
		Resource: "resources:articles:ladon-introduction",
		Action:   "delete",
		Subject:  "users:peter",
		Context: ladon.Context{
			"remoteIP": "192.168.0.5",
		},
	}

	// Authorize the request
	fmt.Println("Authorize request...")
	ret, err := clientset.Iam().AuthzV1().Authz().Authorize(context.TODO(), request, metav1.AuthorizeOptions{})
	if err != nil {
		panic(err.Error())
	}

	fmt.Printf("Authorize response: %s.\n", ret.ToString())
}
```
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（2） 💬（1）<div>总结：
client-go 风格的SDK从项目、应用、服务 都有客户端，且上一层客户端封装了下层的客户端。
1. NewForConfig 操作，会将下层的客户端都创建出来。
2. clientset.Iam().AuthzV1() 就是指定客户端的过程。
3. 在要创建具体的资源时，客户端作为参数，动态创建一个资源的“客户端”。这是在服务客户端做的
4. 资源客户端拿到了“RESTClient”对象，开始操作资源。

在服务级别的接口，不但提供了 RESTClient() rest.Interface 来操作资源，也可以调用 AuthzGetter 封装的接口，更加友好。</div>2021-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ff/c6/3586506e.jpg" width="30px"><span>筱泉</span> 👍（0） 💬（1）<div>老师￼，这个example代码怎么跑起来
</div>2022-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/51/84/5b7d4d95.jpg" width="30px"><span>冷峰</span> 👍（0） 💬（1）<div>authz 默认使用的 jwt 认证， 这个例子中的认证方式使用的是 basic , 会导致认证失败</div>2021-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（7） 💬（0）<div>K8s client-go风格的sdk实现方式比公有云普遍采用的sdk更灵活，调用和扩展都更方便，还可以多版本共存。</div>2021-08-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKotsBr2icbYNYlRSlicGUD1H7lulSTQUAiclsEz9gnG5kCW9qeDwdYtlRMXic3V6sj9UrfKLPJnQojag/132" width="30px"><span>ppd0705</span> 👍（5） 💬（1）<div>这种分层设计好妙，可以按需创建某层客户端</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/83/17/df99b53d.jpg" width="30px"><span>随风而过</span> 👍（1） 💬（0）<div>K8s client-go风格确实比公有云的sdk风格有很多优势，目前项目基本都是采用公有云的方式，get到老师的点，学习了</div>2021-09-08</li><br/><li><img src="" width="30px"><span>Geek_12356a</span> 👍（0） 💬（0）<div>这个稍微有些复杂了，各种v1、v2，可维护性不好</div>2025-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（0） 💬（0）<div>请问下 http 客户端使用第三方库的好吗？比如 go-resty</div>2023-02-03</li><br/>
</ul>