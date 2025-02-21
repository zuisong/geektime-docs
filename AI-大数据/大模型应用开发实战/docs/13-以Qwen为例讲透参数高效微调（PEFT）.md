你好，我是黄佳。从今天起，我们将正式进入大模型微调实战。

大模型的微调，是一个对大模型的原理和实践经验要求都非常高的领域。初学者想把微调技术掌握清晰，在我看来，至少面临三个很大的障碍。

1. 优秀资料的匮乏，因为有成功微调大模型经验的人往往都是好的研究者和企业中的骨干，这些人很少有时间和精力制作完善的文档，把具体的微调细节讲清楚。
2. 对大模型整体知识体系的学习要求高，懂微调，又懂如何微调是最有效的，需要你对整个大模型技术栈有一个宏观且深入的认知。
3. 微调技术不仅内容多，而且进化得很快。微调这个技术栈的名词众多，包括全量微调（Full Fine-tuning）、指令微调（Instruction Tuning）、基于人类反馈的强化学习（RLHF）、参数高效微调（PEFT，Parameter-Efficient Fine-Tuning）等等。而参数高效微调中，又包括基于提示的微调方法（如Prompt Tuning / Prefix Tuning / P-Tuning）以及基于低秩分解的微调方法（LoRA / LoHA / LoKr）等。

这么多的新名词，加上这么复杂的技术栈，让人眼花缭乱，不知道从何下手，当然也给了初学者很大的震撼。不过，万丈高楼平地起，我们可以从简单开始学起。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ad/ec/406130f3.jpg" width="30px"><span>coderlee</span> 👍（0） 💬（0）<div>这节课，比较尴尬，window运行，一直提示
Traceback (most recent call last):
  File &quot;D:\Workspace\AI\pwerfull_llm\13_FinetuneQwenPEFT\02_finetune_qwen_1b_lora_ok.py&quot;, line 123, in &lt;module&gt;
    trainer.train()
  File &quot;D:\ProgramData\anaconda3\envs\langchain-test-v2\Lib\site-packages\transformers\trainer.py&quot;, line 1539, in train
    return inner_training_loop(
           ^^^^^^^^^^^^^^^^^^^^
  File &quot;D:\ProgramData\anaconda3\envs\langchain-test-v2\Lib\site-packages\transformers\trainer.py&quot;, line 1944, in _inner_training_loop
    self._maybe_log_save_evaluate(tr_loss, model, trial, epoch, ignore_keys_for_eval)
  File &quot;D:\ProgramData\anaconda3\envs\langchain-test-v2\Lib\site-packages\transformers\trainer.py&quot;, line 2300, in _maybe_log_save_evaluate
    self._save_checkpoint(model, trial, metrics=metrics)
  File &quot;D:\ProgramData\anaconda3\envs\langchain-test-v2\Lib\site-packages\transformers\trainer.py&quot;, line 2418, in _save_checkpoint
    fd = os.open(output_dir, os.O_RDONLY)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [Errno 13] Permission denied: &#39;D:\\Workspace\\AI\\pwerfull_llm\\13_FinetuneQwenPEFT\\results\\checkpoint-1&#39;
 10%|█         | 1&#47;10 [00:17&lt;02:39, 17.71s&#47;it]
所以，我打算等后续找个linux环境，再实际操作下。</div>2024-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（0） 💬（0）<div>佳哥好，什么时候应该使用微调，什么时候应该用RAG或sql agent啊？</div>2024-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cc/25/8c6eab2c.jpg" width="30px"><span>ArtistLu</span> 👍（0） 💬（0）<div>老师，我用 Qwen2-0.5B 训练出来的效果不行。结果如下：
---------------------------------------------------------
Input: 肛门疼痛，痔疮，肛裂。
Output: Instruction: 使用中医知识正确回答适合这个病例的中成药。
Input: 肛门疼痛，痔疮，肛裂。
Answer: 、、。、黄、，、制、片、品、状、剂、性、炒、；、醋、.、）。品。
----------------------------------------------------------
能帮忙解答几个问题吗？
1.出现这种情况是不是预训练模型太小导致？
2.训练的结果文件总大小只有十几M，为啥训练后这么小勒？
3.如果只需要大模型回答很小领域问题，选择预训练模型大小有啥优劣？（比如我只想用大模型给 k8s 节点打分，用于调度）🙏</div>2024-06-25</li><br/>
</ul>