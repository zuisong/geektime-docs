你好，我是李锟。

在前面课程中我们了解到，AutoGPT 的新版本 AutoGPT Platform 的体系架构比 MetaGPT 更为复杂，这也是我需要 4 节课的篇幅讲解 AutoGPT 的原因。在这节课中，我们以前面三课学习到的知识为基础，继续学习 AutoGPT Platform 的一些高级开发技能。

## Block 高级开发技术

在上节课中，我们仅仅使用最基础的 Block 开发技术，实现了 24 点游戏智能体应用中的几个自定义 Block。在所有 AutoGPT Platform 官方教程中，最为详尽的就是关于 Block 开发的教程：[Contributing to AutoGPT Agent Server: Creating and Testing Blocks](https://docs.agpt.co/platform/new_blocks)，这体现出 Block 在 AutoGPT Platform 中的核心地位。在这篇教程中，还有一些高级的 Block 开发技术，我有必要讲解一下。

这篇教程中说道：

> Block 是可重复使用的组件，它们可以连接起来，形成一个代表智能体行为的图。每个 Block 都有输入、输出和特定的功能。适当的测试对于确保 Block 正确一致地工作至关重要。

在上节课中我们已经在实战层面看到了，可以把多个 Block 组装成 Agent，然后还可以把多个 Agent 和 Block 组装成更复杂的 Agent。就像 MetaGPT 中的那种团队组织一样，Agent 系统可以被划分成很多层，形成一个类似公司或者军队的分层组织架构。