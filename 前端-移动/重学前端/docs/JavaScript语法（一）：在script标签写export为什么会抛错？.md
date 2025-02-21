你好，我是winter，今天我们进入到语法部分的学习。在讲解具体的语法结构之前，这一堂课我首先要给你介绍一下JavaScript语法的一些基本规则。

## 脚本和模块

首先，JavaScript有两种源文件，一种叫做脚本，一种叫做模块。这个区分是在ES6引入了模块机制开始的，在ES5和之前的版本中，就只有一种源文件类型（就只有脚本）。

脚本是可以由浏览器或者node环境引入执行的，而模块只能由JavaScript代码用import引入执行。

从概念上，我们可以认为脚本具有主动性的JavaScript代码段，是控制宿主完成一定任务的代码；而模块是被动性的JavaScript代码段，是等待被调用的库。

我们对标准中的语法产生式做一些对比，不难发现，实际上模块和脚本之间的区别仅仅在于是否包含import 和 export。

脚本是一种兼容之前的版本的定义，在这个模式下，没有import就不需要处理加载“.js”文件问题。

现代浏览器可以支持用script标签引入模块或者脚本，如果要引入模块，必须给script标签添加type=“module”。如果引入脚本，则不需要type。

```HTML
<script type="module" src="xxxxx.js"></script>
```
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/9b/5d/629fa226.jpg" width="30px"><span>洛克不菲勒</span> 👍（19） 💬（2）<div>看了之后好像明白了，但是又好像什么都没学到，是否需要多看几遍？</div>2019-09-03</li><br/><li><img src="" width="30px"><span>xwchris</span> 👍（4） 💬（1）<div>console.log(foo);

if (true) {
      function foo() {}
}

为什么这段代码 我在chrome73中执行得到的是ƒ foo() {}</div>2019-04-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIic4jon8dBkYh5qbKnpeB0YsFjHsicrr0d9DKmuaZX6rcQ2QtH9VqJPGOnURNlaKfT6eRZThXQjPVA/132" width="30px"><span>Geek_7e2326</span> 👍（2） 💬（3）<div>闭包那边解释的不对吧，闭包应该可以看做一个函数，可以让外部访问函数内部的变量，而不会污染全局。
你说的是访问外部的变量。</div>2019-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0d/52/6c39f46e.jpg" width="30px"><span>Richard</span> 👍（175） 💬（0）<div>当你认为你已经掌握了JS，JS会反手给你一巴掌。</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/11/5c/9f6827cc.jpg" width="30px"><span>以勒</span> 👍（122） 💬（0）<div>前面学的宏观任务和微观人物 还记得的同学举个手，点个赞</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/16/4d1e5cc1.jpg" width="30px"><span>mgxian</span> 👍（33） 💬（7）<div>作为一个非前段程序员 看了老师的专栏发现 js 坑真多 各种奇怪的语法和表现 感觉像语言的 bug 一样</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/16/cf/bfde35d6.jpg" width="30px"><span>alue</span> 👍（10） 💬（3）<div>这个教程我总感觉支零破碎的，像盲人摸象一样。可能是我的问题吧</div>2020-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2c/88/2a7fe1a9.jpg" width="30px"><span>让时间说真话</span> 👍（9） 💬（0）<div>首先讲了脚本和模块，而这次老师讲的模块补缺我近段时间用模块时的一些疑问，Js的预处理语法让我更加理解了以前经常用到的作用域。感谢winter！！！</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（7） 💬（1）<div>https:&#47;&#47;github.com&#47;aimergenge&#47;get-exported-names-via-babel</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/29/39/0aec7827.jpg" width="30px"><span>费马</span> 👍（6） 💬（2）<div>能否讲讲为什么导出的无论是基本类型还是引用类型，都会和原模块的变量有绑定关系？</div>2019-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（6） 💬（0）<div>通过@babel&#47;parser解析模块文件，然后通过遍历ExportNamedDeclaration，找出所有export的变量，
spec参考：https:&#47;&#47;github.com&#47;babel&#47;babel&#47;blob&#47;master&#47;packages&#47;babel-parser&#47;ast&#47;spec.md#exports</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1e/c2/edf5dfcb.jpg" width="30px"><span>南墙的树</span> 👍（4） 💬（1）<div>with 作用域那里不太明白，大神能否解答一下？</div>2019-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（4） 💬（2）<div>* 预处理机制让我对 js 中的声明有了更全面的认识，很多文章中提到的一个词是“提升”，与这里提到的预处理机制不无关联。
* 关于声明这块儿，这篇文章讲得也有点意思，不知道winter老师怎么看：
https:&#47;&#47;zhuanlan.zhihu.com&#47;p&#47;28140450
* 在我看来，if中的function声明在预处理阶段的”赋值“行为好像被if形成的块级作用域”拦截“了，导致这个赋值行为推迟到if语句块执行开始之前。（这里只是一种隐喻，并不准确）。
* let,const,class这些在js中的”后来者“由于没有历史包袱，行为大多更加正常（符合直觉，及早抛错）。这让我想到了一篇文章中介绍的temporal dead zone机制：http:&#47;&#47;es6.ruanyifeng.com&#47;#docs&#47;let#%E6%9A%82%E6%97%B6%E6%80%A7%E6%AD%BB%E5%8C%BA</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/da/68/688318f3.jpg" width="30px"><span>∝卓然</span> 👍（2） 💬（0）<div>希望可以在有样例代码后面添加执行结果，让读者更明白，手机端用户没法运行代码，代码水平层次不齐，很难保证作者和读者会保持同一语境。</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fc/80/21d67b9b.jpg" width="30px"><span>二狗</span> 👍（2） 💬（0）<div>作为一个非前端程序员，日常工作觉得简单的js都会写，复杂的js都能看懂  现在已经一脸问号？？？</div>2019-09-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（2） 💬（0）<div>看了老师的文章，越来越理解为啥TS出现的地方越来越多了</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（2） 💬（0）<div>想问一个问题：import 进来的引用为什么可以获取到最新的值，是类似于 getter 的机制吗？</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/d7/a9/f341b89c.jpg" width="30px"><span>azurepwq</span> 👍（1） 💬（0）<div>读了老师的文章，像是读过了，又像是什么都没读。但每篇文章之后都可以罗列一大堆问题，每个问题都可以定义一个主题，每个主题可以写一篇博客，未来几个月不怕没灵感写东西了，这种感觉不要太酸爽。谢谢winter老师。</div>2020-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a2/3d/c6b68ce8.jpg" width="30px"><span>学聪</span> 👍（1） 💬（1）<div>export a from &quot;a.js&quot;
这语法没问题吗？是不是得改成
export {a} from &quot;a.js&quot;
</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/26/4b/d1fc46d6.jpg" width="30px"><span>奋逗的码农哥</span> 👍（1） 💬（0）<div>看完老师的文章，再看看大家的留言评论，能够体会到交流学习的乐趣。:-)</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e9/c1/bd86aaba.jpg" width="30px"><span>马儿</span> 👍（1） 💬（0）<div>真不亏为大神！长见识了</div>2019-04-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLz44WGtTHNfCE3L2fZvvhSPx7CwLJtLyTRhYAQ568h81kMic3xJLZ63OPVPpnqgCByG74fXSKNib5g/132" width="30px"><span>Geek_430795</span> 👍（0） 💬（0）<div>module.exports = function(){
    return {
        visitor:{
            ExportNamedDeclaration(path){
                const {specifiers} = path.node
                specifiers.forEach(item=&gt;{
                    console.log(item.exported.name)
                })
            }
        }
    }
}</div>2023-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/9b/6716b613.jpg" width="30px"><span>杨腊梅</span> 👍（0） 💬（0）<div>测试点评</div>2023-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/ab/fd201314.jpg" width="30px"><span>小耿</span> 👍（0） 💬（0）<div>
console.log(foo);
function foo(){

}
这段代码在 edge 浏览器中执行打印 undefined.</div>2023-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/da/3e/e0d073ca.jpg" width="30px"><span>「前端天地」公众号</span> 👍（0） 💬（0）<div>{
 function foo() {}
 foo = 1;
 foo = 2;
 function foo() {}
 foo = 10;
}
console.log(foo);
winter老师，这个怎么解释呢</div>2021-09-21</li><br/><li><img src="" width="30px"><span>fms</span> 👍（0） 💬（0）<div>一定是特别的缘分才让我入了js的坑，一定是_(:i」∠)_</div>2021-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/03/b8/bf7c310e.jpg" width="30px"><span>dingww</span> 👍（0） 💬（1）<div>export a from &quot;a.js&quot; 什么场景会用到呢？</div>2020-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/22/dd505e6d.jpg" width="30px"><span>Yully</span> 👍（0） 💬（0）<div>通过老师的问题又对babel有了进一步的了解。神奇的JavaScript To JavaScript</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2a/a5/625c0a2e.jpg" width="30px"><span>hhhh</span> 👍（0） 💬（0）<div>js感觉是自己给自己挖坑完了还不填</div>2020-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/6d/a9/4f461d80.jpg" width="30px"><span>固执的鱼wu</span> 👍（0） 💬（2）<div>for(var i = 0; i &lt; 20; i ++) {    void function(i){        var div = document.createElement(&quot;div&quot;);        div.innerHTML = i;        div.onclick = function(){            console.log(i);        }        document.body.appendChild(div);    }(i);}此处的function之前为何要加void，求解答</div>2020-01-08</li><br/>
</ul>