你好，我是郭屹。

上一节课我们一起学习了如何使用ChatGPT来辅助我们编程，通过问答它给出了我们想要的答案。这个过程实际上还是以手工的方式来对话，不过好在OpenAI还提供一些API供程序调用。现在微软的搜索引擎Bing和Quora网站推出的Poe都使用了它。所以今天我们一起看看这些API。

## API入门

OpenAI给开发者提供API来访问它的模型，帮助开发者解决语言处理类任务。

它提供多种基础功能，包括：

- 内容生成Content generation
- 摘要Summarization
- 分类及语义分析Classification, categorization, and sentiment analysis
- 翻译Translation
- …

最主要的API访问入口是 [Completions](https://platform.openai.com/docs/api-reference/completions)。开发者输入一些文本，API会根据你在文本中的意图返回另一段文本。你可以以HTTP Request的方式与API进行交互，然后通过API key进行身份认证。

格式如下：

```plain
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
     "model": "gpt-3.5-turbo",
     "messages": [{"role": "user", "content": "Say this is a test!"}],
     "temperature": 0.7
   }'
```
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/36/bf/0d/d6ac34bd.jpg" width="30px"><span>AVENTADOR</span> 👍（0） 💬（1）<div>首先很感谢老师细心的教学。我想询问老师接下来有什么开课计划呢</div>2023-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>感谢老师的加餐！
Q1:spring我知道用于网站后端开发，除此之外，是否还有其他用途？
Q2：能否加两餐讲一下spring中的设计模式？
Q3：能否加两餐讲几个spring的典型面试题？</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/4d/d2/86dec58a.jpg" width="30px"><span>资深嵌入式点灯工程师</span> 👍（0） 💬（0）<div>完结撒花！之前学习 Spring 源码时，看了一个小册，内容丰富也十分注重细节。但是自己对于 Spring 的整体框架没有一个清晰的认知，后面学习花了很大力气梳理的差不多，通过这次学习对于 Spring 整体框架有了更加清晰地认知。十分感谢老师！
其次，随着 GPT 的出现，极大的降低了了解知识的门槛和搜索问题的难度，也可以十分有效地解决编程中遇到的问题， GPT 确实是非常重要的工具。</div>2023-10-02</li><br/>
</ul>