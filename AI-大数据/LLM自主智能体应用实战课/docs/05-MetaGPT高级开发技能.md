你好，我是李锟

在上节课中第二版的24点游戏智能体实现中，我们分别调用 qwen2.5 和 qwen2.5-math 来实现随机发牌（DealCards）和检查表达式是否正确（CheckExpression）的任务。自己手写这些代码当然也不难，不过此类任务千变万化，针对每个新的任务都要重写一套代码，似乎不够 AI。难道我们做 AI 开发就是所谓的“我负责人工，你负责智能”？！

其实 MetaGPT 开发团队已经开发了一个通用的多功能组件，这两个任务都可以交给这个通用组件来完成，这个组件叫做 DataInterpreter（数据解释器）。

## DataInterpreter

什么是数据解释器呢？我们看一下[数据解释器的官方文档](https://docs.deepwisdom.ai/main/zh/guide/use_cases/agent/interpreter/intro.html)的描述：

> 数据解释器是一个通过编写代码来解决数据相关问题的智能体。它能理解用户需求，制定计划，编写执行代码，并在必要时使用工具。这些能力使它能够处理广泛的场景，请查看论文和下面的示例列表。

这段描述比较简略，不是很清晰，只能让人有一种不明觉厉的印象。不过这个不是大问题，MetaGPT 团队在项目中给出了很多使用 DataInterpreter 的例子，包括了以下这些：

- [数据可视化](https://docs.deepwisdom.ai/main/zh/guide/use_cases/agent/interpreter/data_visualization.html)
- [机器学习建模](https://docs.deepwisdom.ai/main/zh/guide/use_cases/agent/interpreter/machine_learning.html)
- [使用工具进行机器学习建模](https://docs.deepwisdom.ai/main/zh/guide/use_cases/agent/interpreter/machine_learning_with_tools.html)
- [图像背景移除](https://docs.deepwisdom.ai/main/zh/guide/use_cases/agent/interpreter/image_removebg.html)
- [解决数学问题](https://docs.deepwisdom.ai/main/zh/guide/use_cases/agent/interpreter/solve_mathematical_problems.html)
- [票据OCR](https://docs.deepwisdom.ai/main/zh/guide/use_cases/agent/interpreter/ocr_receipt.html)
- [工具使用：网页仿写](https://docs.deepwisdom.ai/main/zh/guide/use_cases/agent/interpreter/imitate_webpage.html)
- [工具使用：网页爬取](https://docs.deepwisdom.ai/main/zh/guide/use_cases/agent/interpreter/crawl_webpage.html)
- [工具使用：文转图](https://docs.deepwisdom.ai/main/zh/guide/use_cases/agent/interpreter/text2image.html)
- [工具使用：邮件总结与回复](https://docs.deepwisdom.ai/main/zh/guide/use_cases/agent/interpreter/email_summary.html)