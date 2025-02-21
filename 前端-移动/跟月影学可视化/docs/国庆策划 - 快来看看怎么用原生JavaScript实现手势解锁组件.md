你好，我是月影。前几天，我给你出了一道实操题，不知道你完成得怎么样啦？

今天，我就给你一个[参考版本](https://github.com/akira-cn/handlock)。当然，并不是说这一版就最好，而是说，借助这一版的实现，我们就能知道当遇到这样比较复杂的 UI 需求时，我们应该怎样思考和实现。

![](https://static001.geekbang.org/resource/image/b1/b2/b1a40490690d3c0418842d86fc81b2b2.jpeg?wh=1920%2A1080)

首先，组件设计一般来说包括7个步骤，分别是理解需求、技术选型、结构（UI）设计、数据和API设计、流程设计、兼容性和细节优化，以及工具和工程化。

当然了，并不是每个组件设计的时候都需要进行这些过程，但一个项目总会在其中一些过程里遇到问题需要解决。所以，下面我们来做一个简单的分析。

## 理解需求

上节课的题目本身只是说设计一个常见的手势密码的 UI 交互，那我们就可以通过选择验证密码和设置密码来切换两种状态，每种状态有自己的流程。

如果你就照着需求把整个组件的状态切换和流程封装起来，或者只是提供了一定的 UI 样式配置能力的话，还远远不够。实际上这个组件如果要给用户使用，我们需要将过程节点开放出来。也就是说，**需要由使用者决定设置密码的过程里执行什么操作、验证密码的过程和密码验证成功后执行什么操作**，这些是组件开发者无法代替使用者来决定的。

```
var password = '11121323';


var locker = new HandLock.Locker({
  container: document.querySelector('#handlock'),
  check: {
    checked: function(res){
      if(res.err){
        console.error(res.err); //密码错误或长度太短
        [执行操作...]
      }else{
        console.log(`正确，密码是：${res.records}`);
        [执行操作...]
      }
    },
  },
  update:{
    beforeRepeat: function(res){
      if(res.err){
        console.error(res.err); //密码长度太短
        [执行操作...]
      }else{
        console.log(`密码初次输入完成，等待重复输入`);
        [执行操作...]
      }
    },
    afterRepeat: function(res){
      if(res.err){
        console.error(res.err); //密码长度太短或者两次密码输入不一致
        [执行操作...]
      }else{
        console.log(`密码更新完成，新密码是：${res.records}`);
        [执行操作...]
      }
    },
  }
});


locker.check(password)
```

## 技术选型

这个问题的 UI 展现的核心是九宫格和选中的小圆点，从技术上来讲，我们有三种可选方案： DOM/Canvas/SVG，三者都是可以实现主体 UI 的。那我们该怎么选择呢？
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/34/99/a62a125d.jpg" width="30px"><span>安东</span> 👍（2） 💬（0）<div>老师真的厉害 我怎么就没想到这样写。 我写的还是太粗糙了</div>2020-10-21</li><br/>
</ul>