你好，我是大圣。

跟随我的脚步，通过对前面数讲内容的学习，相信你现在对Vue+Vuex+vue-router都已经比较熟悉了。在开启课程后续的复杂项目之前，学会如何调试项目也是我们必须要掌握的一个技能。

在项目开发中，我们会碰到各种各样的问题，有样式错误、有不符合预期的代码报错、有前后端联调失败等问题。也因此，一个能全盘帮我们监控项目的方方面面，甚至在监控时，能精确到源码每一行的运行状态的调试工具，就显得非常有必要了。

而Chrome的开发者工具Devtools，就是Vue的调试工具中最好的选择。由于Chrome也公开了Devtools开发的规范，因而各大框架比如Vue和React，都会在Chrome Devtools的基础之上，开发自己框架的调试插件，这样就可以更方便地调试框架内部的代码。Vue Devtools就是Vue官方开发的一个基于Chrome浏览器的插件，作为调试工具，它可以帮助我们更好地调试Vuejs代码。

这节课，我会先为你讲解如何借助Chrome和VS Code搭建高效的开发环境，然后再教你使用Vue 的官方调试插件 Vue Devtools 来进行项目调试工作。

## Chrome调试工具

首先，我们来了解一下Chrome的调试工具，也就是Chrome的开发者工具Chrome DevTools。在Chrome浏览器中，我们打开任意一个页面，点击鼠标右键，再点击审查元素（检查），或者直接点击F12就可以看到调试窗口了。
<div><strong>精选留言（26）</strong></div><ul>
<li><img src="" width="30px"><span>元宝</span> 👍（58） 💬（2）<div>Object.entries([...document.querySelectorAll(&quot;*&quot;)].map(n=&gt;n.tagName).reduce((pre, cur)=&gt;{
  pre[cur] = (pre[cur] || 0) + 1;
  return pre;
}, {})).sort((a, b)=&gt;b[1]-a[1]).slice(0, 3)</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c8/04/fed4c1ad.jpg" width="30px"><span>若川</span> 👍（42） 💬（5）<div>debugger 也是高级程序员必备的断点调试法，你一定要掌握。

很赞同大圣老师的这句话。我觉得是基本必备技能。但我发现真的有很多人不太会，甚至没调试过代码，没安装过vue-devtools。

其实vue官方文档有写怎么调试。《在 VS Code 中调试》https:&#47;&#47;cn.vuejs.org&#47;v2&#47;cookbook&#47;debugging-in-vscode.html

更是少数人知道 vue-devtools 可以直接打开页面对应的组件源文件，不需要问同事，定位半天。
我之前也写过文章分析这个功能原理。《据说 99% 的人不知道 vue-devtools 还能直接打开对应组件文件？本文原理揭秘》https:&#47;&#47;juejin.cn&#47;post&#47;6959348263547830280</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/a1/0e/108d6fb7.jpg" width="30px"><span>Kobe的篮球</span> 👍（12） 💬（1）<div>vue3项目通过vite打包后，如何支持dev-tools啊</div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/64/aa/623076a3.jpg" width="30px"><span>Beauty~fish🐬</span> 👍（1） 💬（1）<div>贺老面试题。。。还有其他的题吗，在哪里可以学习呢</div>2021-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8d/ff/986ffb41.jpg" width="30px"><span>轻飘飘过</span> 👍（1） 💬（1）<div>看大家的写法都挺优秀的，大圣老师说的不用sort 和并列打印数据的问题，个人思考用桶排序求解🤔，代码如下，互相学习。
function main() {
  let tags = Array.from(document.querySelectorAll(&#39;*&#39;));
  let tMap = {}, max = min = 1;
  tags.forEach(tag =&gt; {
    let v = tag.tagName;
    if (!tMap[v]) tMap[v] = 0;
    tMap[v]++;
    max = Math.max(tMap[v], max);
    min = Math.min(tMap[v], min);
  });

  let bucket = new Array(max - min + 1);
  Object.keys(tMap).forEach(v =&gt; {
    if (!bucket[tMap[v] - min]) bucket[tMap[v] - min] = [];
    bucket[tMap[v] - min].push(v);
  });

  let res = [], count = 3, i = bucket.length - 1;
  while (count &gt; 0 &amp;&amp; i &gt;= 0) {
    if (bucket[i]) {
      count--;
      res.push(bucket[i]);
    }
    i--;
  }
  return res;
};</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/0a/80/b916faf5.jpg" width="30px"><span>飞翔国度</span> 👍（1） 💬（2）<div>发现公司的vue项目都屏蔽了vuetools...在生产上开着是不是有点不安全？</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/27/d6/c318bd20.jpg" width="30px"><span>乐叶</span> 👍（0） 💬（1）<div>let tag = [...document.querySelectorAll(&#39;*&#39;)].map(node =&gt; node.nodeName)
let many3 = {}
for (let i=0;i&lt;tag.length;i++) {
  if (!many3[tag[i]]) {
    many3[tag[i]] = 0
  }
  many3[tag[i]]++
}
return Object.keys(many3).map(itemKey =&gt; ({label: itemKey, value: many3[itemKey]})).sort((item1, item2) =&gt; item2.value-item1.value)</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f5/7a/7351b235.jpg" width="30px"><span>ch3cknull</span> 👍（15） 💬（0）<div>vue-devtools有两个，其中一个是不支持vue3的

下面是Google应用商店的扩展的链接，这个链接指向的插件是支持vue3的

http:&#47;&#47;chrome.google.com&#47;webstore&#47;detail&#47;ljjemllljcmogpfapbkkighbhhppjdbg</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/50/c3/0aa50246.jpg" width="30px"><span>花果山大圣</span> 👍（11） 💬（0）<div>参考答案之一， 其实这一题还可以扩展很多，比如不让你用sort，比如如果三四五名词的次数一样，怎么把这些并列的也打出来等等
let ret = Object.entries([...document.querySelectorAll(&#39;*&#39;)].map(node =&gt; node.nodeName).reduce((ret,n)=&gt;{
    ret[n] = ret[n]?ret[n]+1:1
    return ret 
},{})).sort((a,b)=&gt;b[1]-a[1]).slice(0,3)
console.table(ret)
</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c8/4a/3a322856.jpg" width="30px"><span>ll</span> 👍（5） 💬（0）<div>devTool 是很牛的“谁用谁知道”，通过这节，如果没用过的小伙伴赶紧尝试下；
这节课后有如下感想：
1. 调试是工程的重要一环。
2. 想要提高调试环节的效率，要有好的方法，更要有趁手的工具
3. 在 web 开发领域，不夸张的说，最优秀和专业的非 Chrome devtoool 莫属。
4. 针对特定框架，更更专业的工具是各个“框架公司”基于 devtool 开发的“专属”测试工具。 
5. 掌握方法论，并且熟练使用工具；是提高开发效率的明智选择。
6. 如果对 devtool 这么“神奇”抱有好奇，想知道这个是怎么实现的，其实结合思考题，就
   能略知一二，其实原理是相通的
</div>2021-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0e/d9/e61ce097.jpg" width="30px"><span>郭纯</span> 👍（1） 💬（0）<div>Object.entries(Array.from(document.querySelectorAll(&#39;*&#39;)).reduce((res, { tagName }) =&gt; ((tagName in res) ? (res[tagName] ++ ) : (res[tagName] = 1), res), {})).sort(([tagNameA, countA],[tagNameB, countB]) =&gt; countB - countA).map( ([tagName] ) =&gt; tagName ).slice(0,3)</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/a8/8da58e53.jpg" width="30px"><span>海阔天空</span> 👍（1） 💬（0）<div>长知识了，以前调试动画的时候，都是慢慢调的。原来动画还可以这样调。Vue Devtools没有过，可以试一下</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6c/d4/85ef1463.jpg" width="30px"><span>路漫漫</span> 👍（1） 💬（0）<div>先学为敬</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/7f/e4/d5a3c0e6.jpg" width="30px"><span>树</span> 👍（0） 💬（0）<div>安装了好几次vue devtools，其中有一次在极客时间网站是亮着的，vue3项目是灰的；其他安装的插件都是灰的。这个东西真的能用吗，怎么就是搞不定这个插件呢</div>2024-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/7f/e4/d5a3c0e6.jpg" width="30px"><span>树</span> 👍（0） 💬（0）<div>安装了vue devtools后，在控制台没有显示vue面板怎么办呢。网上找了很多方法，怀疑vue devtools真的有人用过吗</div>2024-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d3/9d/01bdd3b0.jpg" width="30px"><span>Skelanimals</span> 👍（0） 💬（0）<div>Object.entries(Array.from([...$$(&#39;*&#39;)])
      .reduce((total, node) =&gt; {
        if(!total[node.nodeName])
          total[node.nodeName] = 0
  
        total[node.nodeName] += 1
  
        return total
}, {}))
      .sort((a, b) =&gt; b[1] - a[1])
      .slice(0, 3)</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（0） 💬（2）<div>国内下载chrome插件有点困难 他们就不能搞个国内的下载链接么</div>2022-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9e/3c/0e2a08b1.jpg" width="30px"><span>杨闯</span> 👍（0） 💬（0）<div>刚才的问题解决了，不用求助了，谢谢了</div>2022-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9e/3c/0e2a08b1.jpg" width="30px"><span>杨闯</span> 👍（0） 💬（0）<div>试了好多办法都没有解决Vue.js is detected on this page，求助</div>2022-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e1/be/37db382a.jpg" width="30px"><span>大鸟</span> 👍（0） 💬（0）<div>老师你好，我用的是webstorm开发的，我使用devtools在编辑器中打开对应的组件的时候总是在命令行中打开了文件内容而不是标签页。这种情况搜了很久都没搜到解决方法。</div>2022-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/42/1de79e71.jpg" width="30px"><span>南山</span> 👍（0） 💬（0）<div>大开眼界</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/6a/04/351815e7.jpg" width="30px"><span>名扬呀</span> 👍（0） 💬（0）<div>[...document.querySelectorAll(&#39;*&#39;)].reduce((result, item) =&gt; {
  if(result.findIndex(itm =&gt; itm.type === item.nodeName) &lt; 0) {
    result.push({
      type: item.nodeName,
      num: document.querySelectorAll(item.nodeName.toLowerCase()).length
    })
  }
  return result
}, []).sort((a, b) =&gt; {
  return b.num - a.num
}).map(item  =&gt; {
  return item.type.toLowerCase()
}).slice(0, 3)
获取都有标签，每种标签计数，由大到小排序，取前三个。</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/58/40/c318a0dd.jpg" width="30px"><span>li_shenghong</span> 👍（0） 💬（0）<div>可不可以结合大一些项目，给一个比较完整的调试例子。</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/23/a6/88858c72.jpg" width="30px"><span>mixiuu</span> 👍（0） 💬（2）<div>大圣老师，我这边启动课程上的demo项目，不会出现vue-devtools，手动开启dev-tools提示，vue.js is not detected，但是打开极客官网会有devtools，是因为我之前装的版本只支持vue2不支持vue3嘛。</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/4a/75/51435f4b.jpg" width="30px"><span>@</span> 👍（0） 💬（0）<div>工欲善其事必先利其器</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/9a/17/1695d3a2.jpg" width="30px"><span>肉球</span> 👍（0） 💬（0）<div>打卡</div>2021-11-12</li><br/>
</ul>