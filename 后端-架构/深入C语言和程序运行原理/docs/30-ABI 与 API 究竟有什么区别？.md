你好，我是于航。

今天我们来聊另外一个老生常谈的话题：“ ABI 与 API 这两个概念究竟有什么区别？”

也许你之前也思考过这个问题。ABI 与 API 这两个英文缩写只差一个字符，因此它们对应的概念在很多线下讨论和博客文章中会被经常混用，甚至是乱用。当然，时不时地，这个问题也会成为人们在技术社交圈内的丰富谈资。这一讲，就以你熟悉的 C 语言体系为例，我们来一起看看 ABI 与 API 二者分别指代什么内容，有什么区别。

## **API**

API 的全称为“应用程序编程接口（Application Programming Interface）”。从它的名字我们就能看出来，这一类接口的侧重点在于“编程”。因此，通过遵循 API 规范，我们可以在相应的编程语言代码中使用这些接口，以操作计算机系统来完成某项特定任务。而对 C 语言来说，那些由 C 标准库提供的，被定义在不同头文件中的函数原型，便是一种 API 的具体表现形式。

### 重要特征

**API 具有的一个最重要特征，便是隐藏了其背后具体功能的内部实现细节，只公开对编码有意义的部分**（如接口名称、可接收参数的个数与类型等）。通过保持这部分特征的一致性，API 提供者与调用者便可在相对隔离的环境下被独立维护。在这种情况下，这部分相对统一和稳定的特征也可被单独抽离出来，成为相应的 API 规范。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="" width="30px"><span>Y</span> 👍（15） 💬（1）<div>API：规定了螺丝和螺丝母的规格
ABI：规定了制作螺丝的材料和制作细节
😂</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f6/80/85ec2c2a.jpg" width="30px"><span>连瑞龙</span> 👍（0） 💬（0）<div>原文中的汇编语言小伙伴们如果想实践，需要将 # 注释部分删掉或者改为 ; 注释。汇编不支持 # 注释。

; main.asm
extern sub
global _start
section .text
_start:
  and   rsp, 0xfffffffffffffff0
  sub   rsp, 1
  mov   esi, 2  ; the 1st param.
  mov   edi, 1  ; the 2nd param.
  call  sub
  mov   edi, eax
  mov   eax, 60
  syscall</div>2024-01-12</li><br/>
</ul>