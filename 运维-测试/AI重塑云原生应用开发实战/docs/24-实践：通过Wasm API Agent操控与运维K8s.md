你好，我是邢云阳。

上一节课，我们留了一个小尾巴，也就是在 Agent 插件中，如何实现 JSON Mode 输出呢？本节课，我们先来解决掉这个小尾巴。

## JSON Mode

在[第 21 讲](https://time.geekbang.org/column/article/842102)中，我带你开发JSON Mode小插件时，详细讲解了JSON Mode的工作原理。其核心是通过prompt指示大模型按照指定的JSON Schema格式化输出结果。由于本插件的JSON Schema支持自定义，因此我对之前的JSON Mode prompt进行了调整，修改后的形式如下：

```go
Given the Json Schema: %s, please help me convert the following content to a pure json: %s
Do not respond other content except the pure json!!!!
```

- 第一个%s用于填充用户自定义的JSON Schema内容；
- 第二个%s用于填充需要格式化的原始数据。

在完成核心逻辑后，代码的实现就变得顺理成章了。具体流程如下：

1. 在获取到“Final Answer”时，首先判断是否开启了JSON输出设置。
2. 如果开启了JSON格式化功能，就先将结果按照指定的JSON Schema进行格式化；
3. 如果未开启，就直接返回结果，继续后续的Body替换操作。