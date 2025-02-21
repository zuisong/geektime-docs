你好，我是邢云阳。

在前面的几节课中，我从 Wasm 的理论和实践两个角度，为你介绍了 Wasm。核心知识点实际上就是两块，一是 Wasm 的原理，二就是如何用 Wasm Go SDK 编写 Wasm程序。对于原理，感兴趣的话你可以详细了解一下，而对于如何写 Wasm 程序，参考上节课的例子学会套路即可，后面用到哪个工具函数可以随时查文档。

在上节课的例子中，我们用到过 AI Proxy 这个插件，主要是为了能以网关 URL + OpenAI 协议的方式请求大模型。因为我们知道现在市面上无论是商业模型还是开源模型，基本大多都会遵循 OpenAI 标准，但每家厂商的 Base\_Url 不一样，因此如果能有一个插件帮我们做好适配，让我们无论使用什么模型时，都可以以标准 OpenAI 格式请求，就会很方便。

因此本节课，我就用最近比较火的 DeepSeek 模型为例，带你写一下 AI Proxy 程序。

## 总体架构

我们先来了解一下 AI Proxy 的总体架构原理。

![图片](https://static001.geekbang.org/resource/image/a4/25/a478e4ayyfe80a38e30f8ef64018c225.jpg?wh=1920x960)

从前面的课程中，我们已经了解到，Wasm 插件是如何在一次完整的 HTTP 请求中起作用的。简单来说，它主要在四个阶段介入：RequestHeader、RequestBody、ResponseHeader 和 ResponseBody。