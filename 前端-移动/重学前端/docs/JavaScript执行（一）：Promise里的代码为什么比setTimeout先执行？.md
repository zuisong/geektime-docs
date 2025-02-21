你好，我是winter。这一部分我们来讲一讲JavaScript的执行。

首先我们考虑一下，如果我们是浏览器或者Node的开发者，我们该如何使用JavaScript引擎。

当拿到一段JavaScript代码时，浏览器或者Node环境首先要做的就是；传递给JavaScript引擎，并且要求它去执行。

然而，执行JavaScript并非一锤子买卖，宿主环境当遇到一些事件时，会继续把一段代码传递给JavaScript引擎去执行，此外，我们可能还会提供API给JavaScript引擎，比如setTimeout这样的API，它会允许JavaScript在特定的时机执行。

所以，我们首先应该形成一个感性的认知：一个JavaScript引擎会常驻于内存中，它等待着我们（宿主）把JavaScript代码或者函数传递给它执行。

在ES3和更早的版本中，JavaScript本身还没有异步执行代码的能力，这也就意味着，宿主环境传递给JavaScript引擎一段代码，引擎就把代码直接顺次执行了，这个任务也就是宿主发起的任务。

但是，在ES5之后，JavaScript引入了Promise，这样，不需要浏览器的安排，JavaScript引擎本身也可以发起任务了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/04/b3/3f0b69f9.jpg" width="30px"><span>杨学茂</span> 👍（557） 💬（16）<div>function sleep(duration){
    return new Promise(function(resolve){
        setTimeout(resolve, duration);
    })
}
async function changeColor(duration,color){
    document.getElementById(&quot;traffic-light&quot;).style.background = color;
    await sleep(duration);

}
async function main(){
    while(true){
        await changeColor(3000,&quot;green&quot;);
        await changeColor(1000, &quot;yellow&quot;);
        await changeColor(2000, &quot;red&quot;);
    }
}
main()</div>2019-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/29/39/0aec7827.jpg" width="30px"><span>费马</span> 👍（35） 💬（5）<div>const lightEle = document.getElementById(&#39;traffic-light&#39;);
function changeTrafficLight(color, duration) {
  return new Promise(function(resolve, reject) {
    lightEle.style.background = color;
    setTimeout(resolve, duration);
  })
}

async function trafficScheduler() {
  await changeTrafficLight(&#39;green&#39;, 3000);
  await changeTrafficLight(&#39;yellow&#39;, 1000);
  await changeTrafficLight(&#39;red&#39;, 2000);
  trafficScheduler();
}

trafficScheduler();</div>2019-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cb/82/d01f40b4.jpg" width="30px"><span>deiphi</span> 👍（33） 💬（8）<div>&#47;&#47; 比较原始的写法
function color () { 
	console.log(&#39;green&#39;);
	
	setTimeout(() =&gt; {
			console.log(&#39;yellow&#39;);
			
			setTimeout(() =&gt; {
				console.log(&#39;red&#39;);
				
				setTimeout(color, 2000);
			}, 1000)
	}, 3000);
}
color();</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/4a/13/42e02b09.jpg" width="30px"><span>许吉中</span> 👍（13） 💬（2）<div>async&#47;await函数属于宏观还是微观？</div>2019-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0e/04/d710d928.jpg" width="30px"><span>奥斯特洛夫斯基</span> 👍（12） 💬（1）<div>同步的代码和setTimeout都是宏任务？</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6f/60/edbb8b8a.jpg" width="30px"><span>小孔</span> 👍（8） 💬（2）<div>1. async&#47;await ，遇到await时就会退出执行，我想问下，退出之后是处于等待await执行完再开始之后吗？
2. 如果promise中产生setTimeout函数，那么在这里的setTimeout是处于微观任务对吗？因为这是js引擎直接发起的？
</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/d9/3014889f.jpg" width="30px"><span>周序猿</span> 👍（4） 💬（1）<div>&#47;&#47; 另类的写法
 var lightDiv = document.getElementById(&#39;light&#39;)
    function wait(seconds){
      return new Promise((resolve)=&gt;{
        setTimeout(resolve,seconds)
      })
    }

    function light(color, waitTime){
      this.color = color
      this.waitTime = waitTime
    }
    light.prototype.run = function(){
      lightDiv.style.backgroundColor = this.color
      return wait(this.waitTime).then(()=&gt;{
        return this.nextLight.run()
      })
    }

    let redLight = new light(&#39;red&#39;,2000)
    let yellowLight = new light(&#39;yellow&#39;,1000)
    let greenLight = new light(&#39;green&#39;,3000)

    redLight.nextLight = greenLight
    yellowLight.nextLight = redLight
    greenLight.nextLight = yellowLight

    redLight.run()</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/de/3e/2e87843c.jpg" width="30px"><span>不曾潇洒</span> 👍（4） 💬（2）<div>老师你好，看了这篇文章后受益匪浅，有个小问题:
在Promise段的最后一个例子中，最后一句代码:
sleep(5000).then(()=&gt;{console.log(&#39;c&#39;)})，
这里面的打印c是属于第一个宏任务还是属于setTime产生的第二个宏任务呢?</div>2019-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（4） 💬（6）<div>async function controlLoop () {
  await changeColor(&#39;green&#39;, 3000)
  await changeColor(&#39;yellow&#39;, 1000)
  await changeColor(&#39;red&#39;, 2000)
  await controlLoop()
}

async function changeColor (color, time) {
  console.log(color + &#39; begin&#39;)
  return new Promise((resolve) =&gt; {
    setTimeout(() =&gt; {
      console.log(color + &#39; end&#39;)
      resolve()
    }, time)
  })
}

controlLoop()</div>2019-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9c/e2/368f6734.jpg" width="30px"><span>🇨🇳🇨🇳🇨🇳</span> 👍（3） 💬（2）<div>async&#47;awiat 只是generator&#47;iterator的语法糖而已</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d1/81/89ba9d81.jpg" width="30px"><span>大力</span> 👍（3） 💬（1）<div>用了async, await后貌似宏观与微观任务分得没那么清晰了。</div>2019-06-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJEPMj69Hy9qq8SuEsiccKKaJQt20vvjl9Z9DMJxNmvrq6X3LrDMONTT6Jkg70kEVg13Lkdc6eMWlA/132" width="30px"><span>Geek_e21f0d</span> 👍（3） 💬（1）<div>let lightStates = [{
        color: &#39;green&#39;,
        duration: 3000
    },
    {
        color: &#39;yellow&#39;,
        duration: 1000
    },
    {
        color: &#39;red&#39;,
        duration: 2000
    }];
    let setLightColorAndVisibleDuration = function(color, duration) {
        &#47;&#47;set light color
        return new Promise((resolve) =&gt; {
            setTimeout(() =&gt; {
                resolve();
            }, duration);
        });
    }
    let startShowLight = async function() {
        let index = 0;
        while(index &lt;= lightStates.length - 1) {
            let nextState = lightStates[index];
            await setLightColorAndVisibleDuration(nextState.color, nextState.duration);
            index++;
        }
        
    };
    startShowLight();</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0a/de/8c4810b0.jpg" width="30px"><span>NeverEver</span> 👍（3） 💬（1）<div>我想到的方法是用Recursion。写一个函数setColor，需要一个参数color，函数里首先把div的backgroundColor设置color，然后用setTimeout来设置下一个颜色，根据传入的color相应更改时间和颜色即可</div>2019-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/bf/bb/c0e9847e.jpg" width="30px"><span>Geek_55d7cf</span> 👍（2） 💬（1）<div>除了setTimeout还有哪些宏观任务呢？
</div>2019-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（2） 💬（1）<div>略简陋...
&#47;&#47; sleep,green,red,yellow already defined
async function main () {
  while (true) {
    green()
    await sleep(3)
    yellow ()
    await sleep (1)
    red()
    await sleep(2)
  }
}
main()</div>2019-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/26/4b/d1fc46d6.jpg" width="30px"><span>奋逗的码农哥</span> 👍（0） 💬（1）<div>&#47;&#47; 实现一个红绿灯，把一个圆形 div 按照绿色3 秒，黄色 1 秒，红色 2 秒循环改变背景色
&#47;&#47; 初始化创建元素
var div = document.createElement(&quot;div&quot;)
div.className = &#39;light&#39;
div.innerText=&#39;&#39;
div.style.backgroundColor = &#39;&#39;
div.align = &#39;center&#39;
div.style.fontSize = &#39;30px&#39;
div.style.lineHeight = &#39;100px&#39;
div.style.color = &#39;#fff&#39;
div.style.height = 100
div.style.width = 100
div.style.borderRadius = &#39;50px&#39;
document.body.appendChild(div)

var sleep = function (duration) {
    return new Promise(function(resolve, reject) {
        setTimeout(resolve,duration);
    })
}

&#47;&#47; 绿灯
var green = function () {
  document.querySelector(&#39;.light&#39;).style.backgroundColor = &#39;green&#39;
  sleep(3000).then(()=&gt; { yellow() });
}

&#47;&#47; 黄灯
var yellow = function () {
  document.querySelector(&#39;.light&#39;).style.backgroundColor = &#39;yellow&#39;
  sleep(1000).then(()=&gt; { red() });
}

&#47;&#47; 红灯
var red = function () {
  document.querySelector(&#39;.light&#39;).style.backgroundColor = &#39;red&#39;
  sleep(2000).then(()=&gt; { green() });
}

var init = function() {
  &#47;&#47; 绿灯启动
  green()
}

&#47;&#47; 执行
init()</div>2019-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/28/d6f49ec2.jpg" width="30px"><span>MarlboroKay</span> 👍（0） 💬（1）<div>function main(duration,color){
			return new Promise(function(resolve,reject){
				setTimeout(resolve,duration)
			});
		}
		function changeColor(color){
			var lamp = document.getElementById(&#39;#lapm&#39;);
			lapm.style.backgroundColor = color;
		}

		async function change(){
			await main(3000).then(()=&gt;changeColor(&#39;yellow&#39;));
			await main(1000).then(()=&gt;changeColor(&#39;red&#39;));
			await main(2000).then(()=&gt;changeColor(&#39;green&#39;));
			return change();
		}
		change();
PS:执行耗时1秒的Promis 代码段第5行：应该是 r1.then(...)</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c1/cc/6b6bbd41.jpg" width="30px"><span>周小成</span> 👍（0） 💬（1）<div>讲的很通俗易懂，认识更清晰了。执行耗时1秒的Promise那里的代码有些小问题哦，r.then应该改成r1.then</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/42/e7/e5afadf7.jpg" width="30px"><span>风吹一个大耳东</span> 👍（0） 💬（1）<div>function light(time, color) {
	return new Promise(function(resolve,reject) {
		setTimeout(()=&gt; {
			resolve();
			console.log(color)
		}, time)
    })
}

async function run() {
	await light(3000, &#39;green&#39;)
	await light(1000, &#39;red&#39;)
	await light(2000, &#39;yellow&#39;)
}

run()</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/18/3f/93e02812.jpg" width="30px"><span>xlm</span> 👍（0） 💬（1）<div>async&#47;await的实现原理是Generator +Promise的语法糖😳 ？</div>2019-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/4a/de82f373.jpg" width="30px"><span>AICC</span> 👍（0） 💬（1）<div>function sleep(duration) {
  return new Promise(function(resolve, reject) {
      setTimeout(resolve,duration);
  })
}
async function foo(duration,name){
  console.log(name)
  await sleep(duration)
}
async function foo2(){
  await foo(3000,&quot;绿&quot;);
  await foo(1000,&quot;黄&quot;);
  await foo(2000,&quot;红&quot;);
}

while(true) {
  foo2()
}</div>2019-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2e/64/10182523.jpg" width="30px"><span>whatever</span> 👍（192） 💬（12）<div>https:&#47;&#47;jakearchibald.com&#47;2015&#47;tasks-microtasks-queues-and-schedules&#47;
为了更深入的理解宏任务和微任务，读了这篇。感觉文中说的微任务总是先于宏任务会让人产生误解，更准确的说法应该是微任务总会在下一个宏任务之前执行，在本身所属的宏任务结束后立即执行。</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/80/c3/82923c17.jpg" width="30px"><span>马克豚</span> 👍（65） 💬（1）<div>宏任务和微任务的执行顺序其实很好理解。首先一个js脚本本身对于浏览器而言就是一个宏任务，也是第一个宏任务，而处于其中的代码可能有3种：非异步代码、产生微任务的异步代码（promise等）、产生宏任务的异步代码(settimeout、setinterval等)。
我们知道宏任务处于一个队列中，应当先执行完一个宏任务才会执行下一个宏任务，所以在js脚本中，会先执行非异步代码，再执行微任务代码，最后执行宏任务代码。这时候我们进行到了下一个宏任务中，又按照这个顺序执行。
微任务总是先于宏任务这个说法不准确，应该是处于同一级的情况下才能这么说。实际上微任务永远是宏任务的一部分，它处于一个大的宏任务内。


</div>2020-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/be/e2/57d62270.jpg" width="30px"><span>奇奇</span> 👍（26） 💬（2）<div>怎么区分是宿主环境还是js引擎发起的任务呢</div>2019-02-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/s0bx4WXQNkAJ3c3map0g6dlt3sKDgTtN7Ria96YoufjQcVVI8Shv5CN1jnK1ZTImNnlPcibRqvyiaUuhpIvV1TpnQ/132" width="30px"><span>wingsico</span> 👍（17） 💬（3）<div>这一节主要讲了一下JS的执行栈，从宿主环境到JS引擎，分为宏任务和微任务。但实际上并没有阐述的十分清楚，只是根据一些比较浅显的现象来说明了一下这些任务的执行机制。

对于为什么采用事件循环，以及多种宏任务队列以及浏览器渲染，IO，网络请求等均无涉及。

实际上事件循环依赖于宿主，是宿主需要事件循环来协调js中多种事件源进行交互。而事件循环并不是js本身具有的能力。

对于浏览器中的多种的宏任务队列，可分为页面渲染、用户交互、网络请求、History API以及计时器等，不同种类的宏任务队列之间的优先级不同，也跟实际执行的时机有关，不同时机得到的结果也会不同。

而浏览器中的事件循环与Node中的事件循环也有区别（原因上面说了），Node中没有DOM，没有页面渲染，但多了文件读取等。在Node11之前，Node中一次事件循环可以执行完所有宏任务后再进入下一次事件循环。在Node中，各种不同的宏任务之间也有优先级，并且是固定的，但跟执行的时机也有关系。所以我们也经常看到重复执行一段代码会得到不同的结果。但具体的一个运作机制我目前仍然没有搞清楚，翻看了很多资料也没有对这部分有着详细的阐述。

</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/8b/7e/f78e86a8.jpg" width="30px"><span>顾盼神飞👻</span> 👍（16） 💬（5）<div>js 版本 最高赞同学够标准 来个 css 版本 哈哈
&lt;div class=&quot;toggle-color&quot;&gt;&lt;&#47;div&gt;
.toggle-color {
			width: 100px;
			height: 100px;
			animation: toggle_color linear 6s infinite
		}

		@keyframes toggle_color {

			0%,
			50% {
				background: green
			}

			51%,
			67% {
				background: yellow
			}

			68%,
			100% {
				background: red
			}
		}</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8e/7f/4ff4472f.jpg" width="30px"><span>CaveShao</span> 👍（6） 💬（0）<div>   function func(color, duration) {
        return new Promise(function(resolve, reject) {
            light.style.backgroundColor = color;
            setTimeout(function() {
                it.next();
            }, duration)
        })
    }

    function* main() {
        while (1) {
            yield func(&#39;red&#39;,2000);
            yield func(&#39;yellow&#39;,1000);
            yield func(&#39;green&#39;,3000);
        }
    }

    var it = main();
    it.next();</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/f7/abb7bfe3.jpg" width="30px"><span>帅气小熊猫</span> 👍（6） 💬（3）<div>怎么确定这个微任务属于一个宏任务呢，js主线程跑下来，遇到setTImeout会放到异步队列宏任务中，那下面的遇到的promise怎么判断出它是属于这个宏任务呢？是不是只有这个宏任务没有从异步队列中取出，中间所碰到的所有微任务都属于这个宏任务？</div>2019-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/49/e4/fb47bfcd.jpg" width="30px"><span>dellyoung</span> 👍（4） 💬（0）<div>15行代码最简实现：
const changeNowColor = (time) =&gt; {
    setTimeout(() =&gt; {
        switch (document.getElementById(&#39;root&#39;).style.background) {
            case &#39;green&#39;:
                document.getElementById(&#39;root&#39;).style.background = &#39;yellow&#39;;
                return changeNowColor(1000);
            case &#39;yellow&#39;:
                document.getElementById(&#39;root&#39;).style.background = &#39;red&#39;;
                return changeNowColor(2000);
            case &#39;red&#39;:
                document.getElementById(&#39;root&#39;).style.background = &#39;green&#39;;
                return changeNowColor(3000);
        }
    }, time);
};
changeNowColor(3000);</div>2019-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dc/0b/0baff83d.jpg" width="30px"><span>拒绝第十七次🤤</span> 👍（3） 💬（1）<div>    let sleep = (color,deep)=&gt;{
      return new Promise(reslove=&gt;{
        setTimeout(()=&gt;reslove(color) ,deep)
      })
    }
    async function  changColor (color){
      await sleep (&#39;green&#39;,3000),
      await sleep (&#39;yellow&#39;,1000)
      await sleep (&#39;red&#39;,2000)
    }
    changColor();</div>2019-04-10</li><br/>
</ul>