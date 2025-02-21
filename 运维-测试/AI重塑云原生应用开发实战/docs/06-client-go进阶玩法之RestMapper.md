你好，我是邢云阳。

在上一节课中，我们探讨了通过自然语言操控 Kubernetes 的基本原理，并分析了为了提升系统的可用性和安全性所需考虑的一些关键设计点，例如如何有效地使用 client-go。针对用户可能对任意 Kubernetes 资源进行操作的需求，我们引入了通用化的处理方案 RestMapper。同时，为了缓解查询操作对 apiserver 的访问压力，我们还提出了 Informer 方法。

在本节课中，我将重点介绍 RestMapper 的概念与应用。

为了照顾到对 client-go 不是太熟悉的同学，我们先从基础入手，讲解一下 client-go 四种客户端的使用手法以及 GVR、GVK 等概念。

## 四种客户端

在 client-go 中，有四种可以与 Kubernetes 资源进行交互的客户端，分别是 ClientSet、DynamicClient、DiscoveryClient 以及 RestClient，它们各自适用于不同的场景。下面结合代码来体会一下。

### ClientSet

ClientSet 是最常用的客户端，用于与 Kubernetes 核心资源（如 Pod、Service、Deployment 等）进行交互。它封装了对各类资源的操作，提供了类型安全的接口。我们用一个列出 default 命名空间下的 pod 列表的例子，看一下代码如何实现。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/53/b1/3d6075cc.jpg" width="30px"><span>王建</span> 👍（0） 💬（0）<div>您好，思考题我测试了一下，mappingFor 不管传入的是 resource（比如：pods) 还是 kind（比如 Pod），都是能正确返回 RESTMapping 的，所以是代码不用改？

测试代码如下：
package main

import (
	&quot;context&quot;
	&quot;fmt&quot;
	&quot;k8s.io&#47;apimachinery&#47;pkg&#47;api&#47;meta&quot;
	metav1 &quot;k8s.io&#47;apimachinery&#47;pkg&#47;apis&#47;meta&#47;v1&quot;
	&quot;k8s.io&#47;apimachinery&#47;pkg&#47;runtime&#47;schema&quot;
	&quot;k8s.io&#47;client-go&#47;dynamic&quot;
	&quot;k8s.io&#47;client-go&#47;kubernetes&quot;
	&quot;k8s.io&#47;client-go&#47;restmapper&quot;
	&quot;k8s.io&#47;client-go&#47;tools&#47;clientcmd&quot;
)

func InitRestMapper(clientSet *kubernetes.Clientset) meta.RESTMapper {
	gr, err := restmapper.GetAPIGroupResources(clientSet.Discovery())
	if err != nil {
		panic(err)
	}

	mapper := restmapper.NewDiscoveryRESTMapper(gr)

	return mapper
}

func mappingFor(resourceOrKindArg string, restMapper *meta.RESTMapper) (*meta.RESTMapping, error) {
	fullySpecifiedGVR, groupResource := schema.ParseResourceArg(resourceOrKindArg)
	gvk := schema.GroupVersionKind{}

	if fullySpecifiedGVR != nil {
		gvk, _ = (*restMapper).KindFor(*fullySpecifiedGVR)
	}
	if gvk.Empty() {
		gvk, _ = (*restMapper).KindFor(groupResource.WithVersion(&quot;&quot;))
	}
	if !gvk.Empty() {
		return (*restMapper).RESTMapping(gvk.GroupKind(), gvk.Version)
	}
	return nil, nil
}

func main() {

	config, err := clientcmd.BuildConfigFromFlags(&quot;&quot;, &quot;&#47;path&#47;to&#47;kubeconfig&quot;)
	if err != nil {
		panic(err)
	}

	clientSet, err := kubernetes.NewForConfig(config)
	if err != nil {
		panic(err)
	}

	mapper := InitRestMapper(clientSet)
	restMapping, _ := mappingFor(&quot;pod&quot;, &amp;mapper)

	dynamicClient, err := dynamic.NewForConfig(config)
	if err != nil {
		panic(err)
	}

	var ri dynamic.ResourceInterface

	if restMapping.Scope.Name() == &quot;namespace&quot; {
		ri = dynamicClient.Resource(restMapping.Resource).Namespace(&quot;default&quot;)
	} else {
		ri = dynamicClient.Resource(restMapping.Resource)
	}

	resource, err := ri.List(context.TODO(), metav1.ListOptions{})
	if err != nil {
		panic(err)
	}
	for _, item := range resource.Items {
		fmt.Printf(&quot;Resource Name: %s\n&quot;, item.GetName())
	}
}
</div>2025-02-20</li><br/>
</ul>