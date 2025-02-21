你好，我是郑晔！

通过上一讲的介绍，我们已经知道了，OpenAI API 已经成为了 LLM 编程的事实标准，作为开发者，我们需要对它有一个基本的了解，并且选择了聊天补全这个最核心的 API 作为学习的切入点。

不过，我们上一讲只讲聊天补全的请求部分，让你对怎样对 LLM 提问有了基本了解。在实际工作中，我们还有更重要的部分要去处理，这就是大模型的回答。这一讲，我们就书接上文，看看 LLM 怎样回答我们的问题。

## 聊天应答

在正常情况下，聊天补全的应答内容本身是比较简单的，就是一个标准的 HTTP 的应答。之所以我们还要把它单独拿出来说一下，主要是它还有一种流式应答的模式。

我们先来看正常的 HTTP 应答，也就是一个请求过去，大模型直接回复一个完整的应答。下面是一个应答的例子：

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-4o-mini",
  "system_fingerprint": "fp_44709d6fcb",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "\n\nHello there, how may I assist you today?",
    },
    "logprobs": null,
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}
```
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/64/bd/cbcdc4a6.jpg" width="30px"><span>rOMEo罗密欧</span> 👍（5） 💬（2）<div>请问一下有可以实战的环境或者平台吗</div>2024-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（5） 💬（1）<div>每个技术都有自己的适用场景：SSE（Server-Sent Event）自己可能都没想到，有一天我竟然会从无人问津，到火爆 AI 开发。</div>2024-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c3/e0/3db22579.jpg" width="30px"><span>技术骨干</span> 👍（3） 💬（1）<div>无意带火 了一项技术SSE</div>2024-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（3） 💬（1）<div>第6讲打卡~
Stream 流式响应，特别是在 AI 聊天应用中，可以大幅提升用户体验。</div>2024-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/78/3e/f60ea472.jpg" width="30px"><span>grok</span> 👍（3） 💬（2）<div>纯小白；有几个问题：
1. 这个SSE 技术，是在ChatGPT界面聊天的底层机制？还是我用python调用OpenAI API时的底层机制？估计两个都是？
2. 如果OpenAI采用WebSocket (&quot;服务端需要维护连接&quot;), 用户的使用体验和现在有什么不一样？更慢？更不稳定？还是用户的体验完全一样？
3. 同理claude&#47;gemini&#47;etc.全是SSE？</div>2024-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/c9/98/0bd2c3f9.jpg" width="30px"><span>腿毛茸茸</span> 👍（0） 💬（1）<div>看到同事儿子背诵小学课文的视频，典型的“流式响应”，转几次眼珠吐几个词或半句话，偶尔还卡顿几秒中。</div>2025-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/45/c8/1ccbb110.jpg" width="30px"><span>淡漠尘花划忧伤</span> 👍（0） 💬（0）<div>速记：聊天补全接口的应答消息，其中，最核心的信息是消息内容。当然，根据请求内容的不同，应答可能还会包含很多其它信息，比如工具调用、生成 token 的概率信息等。
应答的模式有两种，一种是常规的 HTTP 同步应答，另一种是流式应答。流式应答主要是用在聊天的场景，用于提高响应速度。</div>2025-02-09</li><br/>
</ul>