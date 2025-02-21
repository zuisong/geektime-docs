你好，我是徐昊，今天我们来继续学习AI时代的软件工程。

在上一节课，我们介绍了如何使用业务模型通过模型展开的方式，帮助我们理解业务。我们也谈到了，在使用模型展开的时候，我们处在庞杂的认知模式下。因此，提效的关键在于构造思维链，让LLM帮助我们更好地应用不可言说知识。

那么今天，我们就围绕之前的例子，看看如何通过LLM辅助我们理解不同的业务场景。

## 通过半结构化自然语言表示模型

当我们想让大语言模型（Large Language Model，LLM）帮助我们通过模型解释业务知识时，首先就会碰到一个问题，如何将我们的模型表达为大语言模型能够理解的形式。

其实这比想象中要容易得多，因为LLM不仅仅懂得自然语言，它还懂得各种编程语言或结构化描述语言。我们可以使用 **Mermaid** 描述我们的领域模型：

```plain
classDiagram
  Department "1" -- "*" Program 
  Department "1" -- "*" Offer 
  Offer  "1" -- "1" Program
  Program "1" -- "1" Curriculum 
  Curriculum "1" -- "*" Course 
  Student "1" -- "1" ProgramEnrollment
  ProgramEnrollment "1" -- "*" CourseEnrollment
  Student "1" -- "1" Offer
  ProgramEnrollment "1" -- "1" Program
  CourseEnrollment "1" -- "1" Course 
  
  class Department {
  }
  class Program {
  }
  class Curriculum {
  }
  class Course {
  }
  class Student {
  }
  class Offer {
  }
  class ProgramEnrollment {
  }
  class CourseEnrollment {
  }
```
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/4a/e1/2a498473.jpg" width="30px"><span>李威</span> 👍（2） 💬（1）<div>请教老师：对于一个复杂的软件系统有大量的领域模型，所有的领域模型及其他们之间的关系我都用mermaid格式编写好，并添加相应的注释，但是最终生成的文本超过了LLM可接受最大字数限制，我譔怎么办呢？

当然我可以根据限界上下文或者功能模块将领域模型进行拆分，每次只为LLM提供部分领域模型的半结构化自然语言描述文本，这样可以让LLM针对部分业务需求为我提供相关的辅助。

还有一种办法是每次为LLM提供部分领域模型的半结构化自然语言描述文本，然后让其先总结一把，之后再输入另一部分的领域模型，继续让其总结以压缩文本内容。但是我试了一下发现，针对这种领域模型的半结构化自然语言的描述文本，LLM一总结就把重要的领域概念直接给总结没了，下次直接使用LLM总结后的文本重新发起一轮新的聊天对话，他就完全不知道自己在说什么了。

所以，请教老师，如何突破LLM对字数的限制，将大量的领域知识一把喂给LLM？</div>2024-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/6e/efb76357.jpg" width="30px"><span>一只豆</span> 👍（1） 💬（2）<div>有个很模糊的直觉性感触：这两讲中的业务模型好像是比较 E-R 样子的，好像偏重于显性知识的核心脉络全写出来。看了编辑推荐的 《创造知识的企业》后，特别是SECI 模型，我在想 未来的模型是不是 不一定停留在显性知识范畴，而是从人类直接提取不可言说知识后形成的模型。所以我的问题是：我的推论是否合理？哪里偏差了？如果存在这种新模型，LLM 如何辅助我们展开，并增强业务理解？</div>2024-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f6/27/c27599ae.jpg" width="30px"><span>术子米德</span> 👍（0） 💬（4）<div>08 | 使用LLM辅助业务理解
🤔☕️🤔☕️🤔
【R】Mermaid（🧜🏻‍♀️），用它来描述业务模型，能绘制成示意图，人瞄一眼就懂，LLM也能读懂，这样就双赢。
半结构化自然语言（即：写注释），一方面，作为自然语言的结构化补充，另一方面，作为结构化语言的自然补充，这样就双边补充、双边互通。
【.I.】之前，我敲代码，敲的时候，我Clear，跑一下发现不对，那就转到调试，调的时候，我到处打断点，待程序跑到那里，我停下来看看，我大概率是Complex、小概率是Chaotic。无论怎样，我总能一点点来，喝点水、走走路、熬个夜、睡一觉、问一问，总能搞定。
【Q】如今，自然语言的描述、加上半结构化的注释、再加上增强半结构化的Mermaid，输出的内容有个三长两短，除了一遍又一遍尝试，我咋个“逐行调试”法？
—  by 术子米德@2024年3月25日</div>2024-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（0） 💬（4）<div>神操作！

问个细微的问题，请教一下老师和各位同学的经验：

对于比较庞大的领域模型，画图的方式和顺序有什么经验嘛？比如，应该采用以下哪种方式呢？

1、先用draw.io等类似工具画图，再让gpt生成 mermaid.  (可能gpt看不懂？）

2、一开始就用mermaid来画图（可能有些没法用mermaid表达？或者不太灵活？）

3、迭代交织使用1和2。

4、还有更好的方式？</div>2024-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（2） 💬（0）<div>第二次学习，把示例中变量 {user_story}、{ac} 从 07 课中补充完整后询问 AI 获得了正常的答案
第一次学习时，直接粘贴了模板，AI 和我都懵了</div>2024-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（1） 💬（0）<div>趁还没讲到测试驱动AI开发，我盲猜一下：生成 yaml 数据后，就可以用于编写 TDD的测试了，有了测试，“功能良好”的软件 就不是啥问题了。不过仅靠这些yaml，应该还没法保证“架构良好”？架构良好得靠CoT？ 那CoT从哪来呢？直接复制粘贴架构的描述？（比如六边形架构的描述？）</div>2024-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9c/f6/eca921d9.jpg" width="30px"><span>赫伯伯</span> 👍（0） 💬（4）<div>所以，模型展开的用途是什么？？？</div>2024-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（0） 💬（0）<div>和 chatGPT 的聊天：https:&#47;&#47;chat.openai.com&#47;share&#47;587f2e0f-53be-4fa0-8458-7f5658b30714</div>2024-04-04</li><br/>
</ul>