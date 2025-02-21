你好，我是黄佳。

上一课中，我们学习了如何基于Code Interpreter做自然语言驱动的数据分析。今天我们来看Assistant中的最后一个，也是超级强大的工具 —— File search（原名Retrieval，也就是文件检索，或者叫RAG）。通过File search，你的Assistant将获得从外部知识库中检索信息的能力，犹如装备了“千里眼”。

![图片](https://static001.geekbang.org/resource/image/1b/9a/1b283c5f403e41d68f80cf3e9cb5299a.png?wh=1130x937 "Playground 中 Assistant 的 File search 工具")

根据OpenAI的说法，目前新版本可以检索多至10000个文档，果真如此，则OpenAI Assistants实在是一个强大的智能助理。

## 什么是 File search（Retrieval）

File search或Retrieval就是“检索”，是赋予Assistant查阅外部知识的能力。外部知识可以是你的企业内部文档、产品说明书、客户反馈等各种非结构化数据。有了这些额外的知识补充，Assistant可以更好地理解用户需求，给出更加准确、个性化的回复。

“检索”的实现原理并不复杂。当你上传一份文档后，OpenAI会自动对文档分块、创建索引，并使用向量搜索从中检索与用户查询最相关的内容。这一切都在File search工具内部自动完成，作为开发者的你并不需要关心其中的细节（当然，在后面的课程中，我也会带着你手动实现具体RAG步骤）。现在，你只管把数据“喂”给File search工具就可以啦。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/97/7b9f4b52.jpg" width="30px"><span>Mr King</span> 👍（0） 💬（2）<div>具备感知输入、利用内部知识进行分析和推理、最终产生输出的能力</div>2024-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/97/7b9f4b52.jpg" width="30px"><span>Mr King</span> 👍（0） 💬（1）<div>国内的 质朴轻言 有这个能力么？</div>2024-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（0） 💬（3）<div>chatgpt刚出来那会看到铺天盖地炒作AI是下一代的搜索引擎时就觉得纳闷，没有时效性，胡言乱语，甚至参考资料都可以编造出来的玩意儿要怎么取代搜索引擎？有了rag以后感觉似乎有希望了，不过那么久了还没看到商业上成功的AI搜索引擎出现又是为什么？</div>2024-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ad/ec/406130f3.jpg" width="30px"><span>coderlee</span> 👍（0） 💬（0）<div>Q1:
1）常见问题、流程引导、律所介绍等
2）检索、归纳总结、建议、
3）历年案例、司法等
Q2:
1.反思（Reflection）
2.工具使用（Tool use）
3.规划（Planning）
4.多Agent协作（Multiagent collaboration）
都具备。理由：从代码执行的各个步骤以及输出结果来看，从1-4都可以看到影子。
Q3:
1.直接将非结构化数据存入知识库
2.借助自定义工具（例如，深度学习训练出来的模型对视音频进行分析后得出的结论）存入知识库
3.本地模型与大模型相结合
4.领域多模态大模型的微调训练</div>2024-11-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI8qibAw4lRCic1pbnA6yzQU3UqtQm3NqV1bUJ5EiaUnJ24V1yf4rtY7n2Wx7ZVvTemqq5a61ERWrrHA/132" width="30px"><span>Alex</span> 👍（0） 💬（0）<div>main方法中:
# 将新的Vector Store关联到Assistant 
assistant = update_assistant_vector_store(assistant.id, vector_store.id)
这里 assistant 会覆盖掉 assistant.id会为None (python 3.11  openai 1.25.0)</div>2024-06-16</li><br/>
</ul>