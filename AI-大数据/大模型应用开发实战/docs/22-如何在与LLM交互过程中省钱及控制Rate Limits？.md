你好，我是黄佳。

OpenAI提供了强大的自然语言处理API，但在将原型转移到生产环境时，管理与运行应用程序相关的成本是一个重要的挑战，尤其是当我们调用OpenAI家族中比较贵的模型的时候，这一讲我们来看看这方面的内容。

OpenAI采用按使用量付费的定价模式，费用以Token为单位计算。Token的价格因所使用的模型而异。为了估算成本，需要预测Token的使用量，考虑诸如流量水平、用户与应用程序交互的频率以及要处理的数据量等因素。

## 对话过程中的 Token

众所周知，语言模型以称为Token的块来读写文本。一个Token可以是一个字符、一个单词，甚至在某些语言中可以比一个字符更短或比一个单词更长。例如，“ChatGPT is great!” 这个句子被编码为六个Token：\[“Chat”, “G”, “PT”, “is”, “great”, “!”]。

API调用中的Token总数会影响API调用的成本，也会影响API调用的时间。同时，总Token数必须低于模型所能容纳的最大限制。

![图片](https://static001.geekbang.org/resource/image/42/06/425930cfb42aa7bdbbaa174d4c395e06.png?wh=933x188)

图中这个Context Window，指的是输入输出能够容纳的Token总和。在OpenAI的API中，并没有对所能输出的Token进行限制，也就是说max\_tokens是一个可选项。