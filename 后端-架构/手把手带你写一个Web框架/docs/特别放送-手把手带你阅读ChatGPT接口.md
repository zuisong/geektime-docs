你好，我是轩脉刃。

好久不见，经过四、五月份GPT的信息轰炸，想必有些同学已经尝试调用过ChatGPT的接口了，今天我们也来聊聊这个话题。

我们大多数人使用ChatGPT，一般是直接使用网页版本的GPT对话框。但是实际上，OpenAI提供了ChatGPT开放平台的调用方式，这个方式，反而是我们目前碰到的各种应用中最常用的方式。

我们可以使用HTTP API的方式来调用ChatGPT。这节课我们就来详细解析一下，如何通过API来调用OpenAI的开放平台，并且通过理解API来解构下目前最火的AutoGPT的实现原理。

## 接口地址

首先我们明确下范围，OpenAI提供了非常多的模型，不同模型在开放平台可能有不同的调用方式，而OpenAI目前最流行的模型就是ChatGPT，专注于聊天对话的大模型。我们这里研究的接口，就是 **ChatGPT 提供的开放平台的接口**。

ChatGPT的接口是一个标准的HTTP请求，请求的URL为：`POST https://api.openai.com/v1/chat/completions`

官方的接口文档地址为：[https://platform.openai.com/docs/api-reference/chat/create](https://platform.openai.com/docs/api-reference/chat/create)
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="" width="30px"><span>wanghaijie</span> 👍（0） 💬（0）<div>jianfeng 666</div>2023-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/8c/f9/e1dab0ca.jpg" width="30px"><span>怎么睡才能做这种梦</span> 👍（0） 💬（0）<div>干货满满哇</div>2023-07-09</li><br/>
</ul>