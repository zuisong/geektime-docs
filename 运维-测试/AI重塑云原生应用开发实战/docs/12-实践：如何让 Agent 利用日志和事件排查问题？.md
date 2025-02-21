你好，我是邢云阳。

在上一节课我们是直接使用了 kubectl 作为工具，让 Agent 通过执行命令行的方式，帮我们解决运维问题。这种方法对于优秀的大模型来说，问题不大，因为它们已经熟练掌握了如何使用 kubectl ，以及如何根据 kubectl 的执行结果，分析问题。

但任何事物都有其两面性，这种方法虽然简单，但缺乏了一定的灵活性。比如，如果让 Agent 帮我们排查一个 pod 为什么起不来，Agent 可能会使用 kubectl get event 或者 kubectl describe pod xxx 来获取 pod 的事件。无论使用哪条命令，其中都会夹杂着一些无用信息，因为我们想要的只有 Type 是 Warning 的 Message。

这些无用信息一方面可能会影响大模型的理解，另一方面太多的信息会占用上下文窗口以及耗费更多的 token。因此本节课我们让 Agent 帮我们分析日志和事件的项目，与上一章一样，采用自己封装 API 的手法，从而达到工具返回的信息可筛选的目的。

## Cobra 前端

为了和上一节课的手法区分开，我们来添加一条名字叫 analyze 的命令。

```plain
cobra-cli add analyze
```

业务代码依然是在生成的 Run 方法中完成。

## 工具

### EventTool
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2d/e5/6b/17de4410.jpg" width="30px"><span>🤡</span> 👍（0） 💬（1）<div>如果工具不给力得不到final answer，可以设置一个循环的上限次数，比如说循环思考 10 次得不到结果，说明这个大模型可能解决不了这个问题，可以直接退出循环</div>2025-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/32/a8/d5bf5445.jpg" width="30px"><span>郑海成</span> 👍（0） 💬（0）<div>【少轮对话才能得到“Final Answer”】本质就是控制上下文长度，openai包里面好像没有相应参数，只能自己控制，通过 MessageStore 的长度控制上下文的长度，上下文长度达到一定就使用【Thought】作为【Final Answer】</div>2025-02-21</li><br/>
</ul>