你好，我是winter。

今天我们进入浏览器API的学习, 这一节课，我们来学习一下DOM API。

DOM API是最早被设计出来的一批API，也是用途最广的API，所以早年的技术社区，常常用DOM来泛指浏览器中所有的API。不过今天这里我们要介绍的DOM，指的就是狭义的文档对象模型。

## DOM API介绍

首先我们先来讲一讲什么叫做文档对象模型。

顾名思义，文档对象模型是用来描述文档，这里的文档，是特指HTML文档（也用于XML文档，但是本课不讨论XML）。同时它又是一个“对象模型”，这意味着它使用的是对象这样的概念来描述HTML文档。

说起HTML文档，这是大家最熟悉的东西了，我们都知道，HTML文档是一个由标签嵌套而成的树形结构，因此，DOM也是使用树形的对象模型来描述一个HTML文档。

DOM API大致会包含4个部分。

- 节点：DOM树形结构中的节点相关API。
- 事件：触发和监听事件相关API。
- Range：操作文字范围相关API。
- 遍历：遍历DOM需要的API。

事件相关API和事件模型，我们会用单独的课程讲解，所以我们本篇文章重点会为你介绍节点和遍历相关API。

DOM API 数量很多，我希望给你提供一个理解DOM API设计的思路，避免单靠机械的方式去死记硬背。
<div><strong>精选留言（25）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLIOSzr2bibaFfoI1RjYyHDoebCZI7KnhTkOnYChQRKVVkmNHTL4chd7BKTGppArERd8x02aZGwDpQ/132" width="30px"><span>kgdmhny</span> 👍（0） 💬（2）<div>老师,请问一下,&quot;对 DOM 而言，Attribute 和 Property 是完全不同的含义，只有特性场景下，两者才会互相关联（这里在后面我会详细讲解，今天的文章里我就不展开了）&quot;后面有讲解这块吗？</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/d9/3014889f.jpg" width="30px"><span>周序猿</span> 👍（41） 💬（1）<div>&#47;&#47; 深度优先
function deepLogTagNames(parentNode){
  console.log(parentNode.tagName)
  const childNodes = parentNode.childNodes
  &#47;&#47; 过滤没有 tagName 的节点，遍历输出
  Array.prototype.filter.call(childNodes, item=&gt;item.tagName)
  .forEach(itemNode=&gt;{
    deepLogTagNames(itemNode)
  })
}
deepLogTagNames(document.body)

&#47;&#47; 广度优先
function breadLogTagNames(root){
  const queue = [root]
  while(queue.length) {
    const currentNode = queue.shift()
    const {childNodes, tagName} = currentNode
    tagName &amp;&amp; console.log(currentNode.tagName)
    &#47;&#47; 过滤没有 tagName 的节点
    Array.prototype.filter.call(childNodes, item=&gt;item.tagName)
    .forEach(itemNode=&gt;{
      queue.push(itemNode)
    }) 
  }
}
breadLogTagNames(document.body)</div>2019-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（14） 💬（2）<div>第一段代码中的 DocumentFragment 应该改为 DocumentType...

&#47;**
 * @param {Element} el
 * @param {(Element) =&gt; void} action
function walk (el, action) {
  if (el) {
    action(el)
    walk(el.firstElementChild, action)
    walk(el.nextElementSibling, action)
  }
}

walk(document.documentElement, el =&gt; console.log(el.nodeName))

&#47;&#47; 如果想要去重...
const set = new Set()
walk(document.documentElement, el =&gt; {
  set.add(el.nodeName)
})
for (let n of set)
  console.log(n)
</div>2019-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/67/9cb713ec.jpg" width="30px"><span>天亮了</span> 👍（11） 💬（3）<div>这样可以把tagName全打印出来...
document.getElementsByTagName(&#39;*&#39;);
</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/45/3cb5cdc6.jpg" width="30px"><span>拾迹</span> 👍（3） 💬（0）<div>document.querySelectorAll(&#39;*&#39;)，这样有点过分了</div>2019-06-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIEOWhj2oCFJeErulEW3QKiamVkTf3o0HZ5gUgl6Gq6d9UmJWDMselGrgnDvd3kVbKqaXw72C05JfQ/132" width="30px"><span>kino</span> 👍（3） 💬（1）<div>insertBefore(newNode,null)和appendChild的区别是啥</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f8/ff/ae800f6b.jpg" width="30px"><span>我叫张小咩²⁰¹⁹</span> 👍（3） 💬（0）<div>var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT, null, false)
var node
while(node = walker.nextNode())
    console.log(node.tagName)
---------- or recursive ------------

const result = []
function getAllTagName(parent) {
	const childs = Array.from(parent.children)
	result.push(...childs.map(el =&gt; el.tagName))
	for (var i = 0; i &lt; childs.length; i++) {
		if (childs[i].children.length) getAllTagName(childs[i])
	}

	if (i == 0) return
}
getAllTagName(document)

console.log(result)


</div>2019-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6b/c9/f90dd3c3.jpg" width="30px"><span>小二子大人</span> 👍（1） 💬（0）<div>const root = document.getElementsByTagName(&#39;html&#39;)[0];
    &#47;&#47; 深度优先遍历
    function deepLogTagName(root) {
        console.log(root.tagName);
        if (root.childNodes.length &gt; 0) {
            for (let i = 0; i &lt; root.childNodes.length; i++) {
                if (root.childNodes[i].nodeType === 1) {
                    deepLogTagName(root.childNodes[i]);
                }
            }
        }
    }
    deepLogTagName(root);
    console.log(&quot;111111111111111111111&quot;)

    &#47;&#47; 广度优先遍历
    console.log(root.tagName);
    function breadLogTagName(root) {
        if (root.childNodes.length &gt; 0) {
            for (let i = 0; i &lt; root.childNodes.length; i++) {
                if (root.childNodes[i].nodeType === 1) {
                    console.log(root.childNodes[i].tagName);
                }
            }
            for (let i = 0; i &lt; root.childNodes.length; i++) {
                if (root.childNodes[i].nodeType === 1) {
                    breadLogTagName(root.childNodes[i]);
                }
            }
        }
    }
    breadLogTagName(root)</div>2019-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6d/38/c951cb2e.jpg" width="30px"><span>笨鸟</span> 👍（1） 💬（0）<div>function loop(node){
	if(!node){
		return
	}
	if(node.nodeType === document.ELEMENT_NODE)
	console.log(node.nodeName);
	if(node.childNodes){
		node.childNodes.forEach(child =&gt; {
			loop(child)
		})
	}
}
loop(document)</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/5d/9afdf648.jpg" width="30px"><span>Link</span> 👍（1） 💬（0）<div>第一段代码中的 DocumentFragment 应该改为 DocumentType</div>2019-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/da/3e/e0d073ca.jpg" width="30px"><span>「前端天地」公众号</span> 👍（0） 💬（0）<div>document好像没有createDocumentType方法</div>2021-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c5/dd/5a482cab.jpg" width="30px"><span>杜森垚</span> 👍（0） 💬（0）<div>document.body.attributes.class = &quot;a&quot; 少了.value 应该为 document.body.attributes.class.value = &quot;a&quot;</div>2020-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/89/15/381ce65f.jpg" width="30px"><span>不曾相识</span> 👍（0） 💬（0）<div>
    &lt;main&gt;
        &lt;!-- &lt;header&gt;
            &lt;h1&gt;遍历所有dom打印tagName&lt;&#47;h1&gt;
            &lt;nav&gt;
                &lt;ul&gt;
                    &lt;li&gt;遍历&lt;&#47;li&gt;
                    &lt;li&gt;递归&lt;&#47;li&gt;
                    &lt;li&gt;深度&lt;&#47;li&gt;
                    &lt;li&gt;广度&lt;&#47;li&gt;
                &lt;&#47;ul&gt;
            &lt;&#47;nav&gt;
        &lt;&#47;header&gt; 第一次的dom已经验证完成 --&gt;
        &lt;header&gt;
            &lt;!-- 加入更多的子元素p验证 --&gt;
            &lt;h1&gt;遍历所有dom打印tagName&lt;&#47;h1&gt;
            &lt;nav&gt;
                &lt;ul&gt;
                    &lt;li&gt;
                        &lt;p&gt;遍历&lt;&#47;p&gt;
                    &lt;&#47;li&gt;
                    &lt;li&gt;
                        &lt;p&gt;
                            递归
                        &lt;&#47;p&gt;
                    &lt;&#47;li&gt;
                    &lt;li&gt;
                        &lt;p&gt;深度&lt;&#47;p&gt;
                    &lt;&#47;li&gt;
                    &lt;li&gt;
                        &lt;p&gt;广度&lt;&#47;p&gt;
                    &lt;&#47;li&gt;
                &lt;&#47;ul&gt;
            &lt;&#47;nav&gt;
        &lt;&#47;header&gt;
    &lt;&#47;main&gt;
    &lt;footer&gt;
        &lt;b&gt;以上都是测试结果，研究中&lt;&#47;b&gt;
    &lt;&#47;footer&gt;
    &lt;script&gt;
        &#47;&#47; 获取根元素 html  开始逐渐有限使用tagName选择器 动态的。
        var html = document.getElementsByTagName(&#39;html&#39;)[0];

        &#47;&#47; 2、 暂时不要把功能柔和在一起，分解最小的功能 比如，查看单个节点的，打印tagName并返回一个包含其子节点集合
        function getChildrenNodes(node) {
            console.log(node.tagName);
            if (node.children.length) {
                var children = node.children;
                &#47;&#47; let flag = false;
                let childrenList = []; &#47;&#47;子节点的后代 
                for (let child of children) {
                    getChildrenNodes(child)
                    childrenList.push(child)
                }

                return childrenList;
            } else {
                return false; &#47;&#47;当前节点没有子元素
            }
        }
        &#47;&#47; 3、 很好第三步直接就，查看递归资料，找思路， 0-0

        &#47;&#47; 停止递归的条件是，所有子节点都没有子节点

        &#47;&#47; 验证 肯定会失败。贝贝
        &#47;&#47; console.log(getChildrenNodes(html));
        &#47;&#47; FIXME 我擦竟然成功了。。。只不过所有的元素都打印了2次

        &#47;&#47; 现在在li当中加入p元素，看结果有没有加入打印  看了，大佬们的答案随便填入的p，我也不懂啥事广度优先，深度优先
        console.log(getChildrenNodes(html));
    &lt;&#47;script&gt;
</div>2020-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bc/e8/43109d54.jpg" width="30px"><span>Peter</span> 👍（0） 💬（0）<div>var allTags = {};
[].forEach.call(document.body.getElementsByTagName(&#39;*&#39;), (e) =&gt; { 
  allTags[e.tagName] = (allTags[e.tagName] || 0) + 1 
})
console.log(allTags)</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/2f/10cbed82.jpg" width="30px"><span>pcxpccccx_</span> 👍（0） 💬（0）<div>讲的真好很全面</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/06/1a/a8a9094d.jpg" width="30px"><span>学海无涯莫非</span> 👍（0） 💬（1）<div>引用：如果你追求极致的性能，还可以把 Attribute 当作节点：getAttributeNode，setAttributeNode。
</div>2019-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d1/81/89ba9d81.jpg" width="30px"><span>大力</span> 👍（0） 💬（0）<div>let set = new Set();
Array.from(document.getElementsByTagName(&#39;*&#39;)).map(node =&gt; set.add(node.tagName.toLowerCase()));
let list = Array.from(set).sort();
console.log(list);</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/af/9a/23603936.jpg" width="30px"><span>胡琦</span> 👍（0） 💬（0）<div>膜拜前排各位大佬，学习了！</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b6/a9/bdf6f6cd.jpg" width="30px"><span>Sticker</span> 👍（0） 💬（0）<div>void function loop(parent){
    const children = parent.childNodes;
    children.forEach(item =&gt; {
        if(item.nodeType === 1){
            console.log(item.nodeName)
            if(item.childNodes.length &gt; 0){
                loop(item)
            }
        }
    })
}(document);</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1b/05/95fe1773.jpg" width="30px"><span>Ramda</span> 👍（0） 💬（0）<div>        const $body = document.body
    
        function deep (parentNode) {
            const children = parentNode.childNodes
            children.forEach(item =&gt; {
                if(item.nodeType === 1 ) {
                    console.log(item.nodeName)
                    if (item.childNodes.length &gt; 0) {
                        deep(item)
                    }
                }
            })
        }           
        deep($body)</div>2019-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6a/72/36c82f74.jpg" width="30px"><span>踏凌霄</span> 👍（0） 💬（0）<div>void function queryAndPrintSon(params) {
      var child = params.children
      for (let index = 0; index &lt; child.length; index++) {
        const element = child[index];
        console.log(element.tagName)
        queryAndPrintSon(element)
      }
    }(document.getRootNode())</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/de/5c67895a.jpg" width="30px"><span>周飞</span> 👍（0） 💬（0）<div> let tagNameArr = [];
    function travaldom(root){       
      if(root.tagName &amp;&amp; root.tagName !==&#39;text&#39;) tagNameArr.push(root.tagName)
       root.childNodes.forEach(node=&gt;{
          travaldom(node);
       });
    }
    travaldom(document);
    console.log(tagNameArr)</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/24/8d76ec60.jpg" width="30px"><span>逐梦无惧</span> 👍（0） 💬（0）<div>老师请问这些html的结构化内容有在哪本书进行介绍吗</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/f5/3a36af36.jpg" width="30px"><span>瓶盖</span> 👍（0） 💬（0）<div>&lt;!DOCTYPE html&gt;
&lt;html lang=&quot;en&quot;&gt;
&lt;head&gt;
  &lt;meta charset=&quot;UTF-8&quot;&gt;
  &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width, initial-scale=1.0&quot;&gt;
  &lt;meta http-equiv=&quot;X-UA-Compatible&quot; content=&quot;ie=edge&quot;&gt;
  &lt;title&gt;遍历输出tagName&lt;&#47;title&gt;
&lt;&#47;head&gt;
&lt;body&gt;
  &lt;section&gt;
    &lt;header&gt;This is a header&lt;&#47;header&gt;
    &lt;div&gt;
      &lt;h4&gt;This is a content title&lt;&#47;h4&gt;
      &lt;p&gt;This is the &lt;em&gt;first&lt;&#47;em&gt; paragraph.&lt;&#47;p&gt;
      &lt;p&gt;This is the &lt;strong&gt;second&lt;&#47;strong&gt; paragraph.&lt;&#47;p&gt;
    &lt;&#47;div&gt;
    &lt;footer&gt;This is a footer of this page.&lt;&#47;footer&gt;
  &lt;&#47;section&gt;
  &lt;script&gt;
    const secElement = document.getElementById(&#39;sec&#39;);
    function getChildTagNames() {
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT, null, false)
      let node;
      while(node = walker.nextNode()) {
        if(node.tagName)
        console.log(node.tagName);
      }
    }
    getChildTagNames(secElement);
  &lt;&#47;script&gt;
&lt;&#47;body&gt;
&lt;&#47;html&gt;</div>2019-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e5/aa/57926594.jpg" width="30px"><span>Ppei</span> 👍（0） 💬（0）<div>老师：
比如 document.body.attribute.class = “a” 等效于 document.setAttribute(“class”, “a”)。
应该是 document.body.attributes吧？
疑惑：
var divDom = document.createElement(&#39;div&#39;)
divDom.attributes.id = &#39;app&#39;
divDom.setAttribute(&#39;class&#39;, &#39;app&#39;)
为什么在divDom上看不到id属性？append到页面中后，同样用getElementById也选择不到这个DOM，用class就可以。</div>2019-03-11</li><br/>
</ul>