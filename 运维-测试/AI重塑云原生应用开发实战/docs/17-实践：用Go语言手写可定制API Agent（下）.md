你好，我是邢云阳。

上节课，我们搞定了 OpenAPI 的配置、解析以及 ReAct 模板的填充，相当于初始化的工作都已经完成了。那今天这节课，我们就来完成剩余的部分。

## Output\_parser

如何与 Agent 进行多轮对话，在之前的课程中，我们曾反复练习过，相信你已经比较熟悉了。在每一轮对话结束时，Agent 都会按照 ReAct 模板规定的格式给出回答。本章节的 ReAct 模板，是采用的 Dify 的模板，其使用的是 JSON 模式。 输出格式如下：

````plain
Action:
```
$JSON_BLOB
```
````

也就是说，JSON 输出会被夹在三个反引号（\`\`\`）代码块之间。而根据 Agent 是选择工具还是得到了 Final Answer，上述格式会产生两种输出。

如果是选择工具，就会输出以下示例中的格式：

````plain
Action:
```
{
  "action": "search_nearby_pois",
  "action_input": {
    "keywords": "游泳馆",
    "location": "117.120308,36.656973"
  }
}
```
````

即 action\_input 对应的值也是一个 JSON。如果是得到了 Final Answer，则是如下格式：