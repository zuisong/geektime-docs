你好，我是蒋宏伟。今天我们学习的重点是列表组件 RecyclerListView。

如果你熟悉 React Native ，那你可能会问了：“React Native 中的列表组件不是 FlatList 吗？”

没错。React Native 官方提供的列表组件确实是 FlatList，但是我推荐你优先使用开源社区提供的列表组件 RecyclerListView。因为，开源社区提供的 RecyclerListView 性能更好。

对于列表组件来说，我们最应该关心的就是性能。这里我给你分享下我的个人经历。2016~2018 年，我参与了一个用 React Native 搭建的信息流项目。信息流这种无限列表页是非常常见的业务场景，比如你使用的京东首页、抖音视频、微信朋友圈都属于信息流页面。你看完一页，还有下一页，看完下一页还有下下页，无穷无尽。这时就要用到我们马上要探讨的列表组件了，而且必须是高性能的列表组件，不能翻着翻着就卡起来了。

2016 年，没有 RecyclerListView，也没有 FlatList，我们用的是第一版的 ListView 组件。ListView 组件性能很差，没有内存回收机制，翻一页内存就涨一点，再翻一页内存又再涨一点。前 5 页滚动非常流畅，第 10 页开始就感觉到卡顿了，到 50 页的时候，基本就滑不动了。卡顿的原因就是无限列表太吃内存了。如果手机的可使用内存不够了，卡顿就会发生。这也是 React Native 刚出来时被吐槽得最多的地方。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/17/57/ac61fff9.jpg" width="30px"><span>卯熙</span> 👍（1） 💬（1）<div>老师， 按需渲染组件，数据还需要分页加载吗？是不是可以不用分页加载，一次性把数据请求回来，它会自动按需渲染。</div>2022-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/37/e5/92cf5c98.jpg" width="30px"><span>山文宋</span> 👍（1） 💬（1）<div>老师，有比较好的RN的书或者资料推荐吗？</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/12/aa2d5cb3.jpg" width="30px"><span>持续思考持续做的牛牛</span> 👍（0） 💬（1）<div>现在新架构里面分支，0.68，有相应的listview优化么？怎么看不到对应的scrollview os库？rrc_scrollview这个组件是还没有完成么？</div>2022-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/12/aa2d5cb3.jpg" width="30px"><span>持续思考持续做的牛牛</span> 👍（0） 💬（1）<div>对于item高度会变化的，能适配么？</div>2022-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（0） 💬（2）<div>作业 
1， https:&#47;&#47;github.com&#47;hdouhua&#47;hybrid-mobile-app&#47;tree&#47;main&#47;AwesomeProject&#47;src&#47;c08
2， 新手，工作中没有使用过，作业中有下面两个问题，请老师帮忙解答。
一，设置 loading 属性会引起 RecyclerListView 重新渲染
二，屏幕下方 “加载更多” 按钮，屏幕有一点抖动</div>2022-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/49/bd/ae37990b.jpg" width="30px"><span>geeklyc</span> 👍（0） 💬（1）<div>老师，有支持多列，瀑布流的不。RecyclerListView</div>2022-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ad/92/98a1fd3c.jpg" width="30px"><span>Geek_e4a05b</span> 👍（0） 💬（1）<div>RecyclerListView 在安卓底端机上暴力滑动底部有可能有闪动情况。RecyclerListView如果卡片高度不固定需要提前计算卡片高度，这个可能会牺牲展示时间。Flatlist可以通过指定windowSize来减少白屏出现，感觉性能比之前好很多了。</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/2e/53/734a3675.jpg" width="30px"><span>Luvian</span> 👍（2） 💬（0）<div>现在有一个新的flashList，原理和recycleList差不多，但是使用更简单</div>2023-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/f1/d785984a.jpg" width="30px"><span>Duke</span> 👍（0） 💬（1）<div>最后一个列表项可枚举是什么意思？</div>2022-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/29/cd/0e6994f8.jpg" width="30px"><span>IRONMAN</span> 👍（0） 💬（0）<div>你好，这个是我写的rowRenderer的函数:
 const _rowRenderer = (type,data)=&gt;{
        console.log(data,data.name)
        &#47;&#47;编写如何渲染数据
       return (
        &lt;View style={{height:100}}&gt;
             &lt;Text &gt;data&lt;&#47;Text&gt;
          
        &lt;&#47;View&gt;
       )
    }

但是在模拟显示的时候却报错：
  LayoutException: RecyclerListView needs to have a bounded size. Currently height or, width is 0.Consider adding style={{flex:1}} or, fixed dimensions

     我明明已经明确了每一个列表项的height，为什么还会报错？但是一旦我重新刷新之后，报错就消失了，但是控制台中并没有打印我在rowRenderer函数中中指定的信息，所以为什么rowRenderer函数没有被调用？
</div>2022-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/29/cd/0e6994f8.jpg" width="30px"><span>IRONMAN</span> 👍（0） 💬（0）<div>老师我用函数组件重新写了一下你的demo，为什么RecycleListView中的内容根本不显示，页面一篇空白。
function  Scroll (props){
    const {width} = useContext(devInfoContext)
    &#47;&#47; const {data} =  props
    const data = [1,2,3]

    const [_dataProvider] = useState(new DataProvider((r1,r2)=&gt;{
        return r1 !== r2
    }))

    &#47;&#47;因为容器内的数据是一直在变化的，所以需要容器内部的数据保存到state中，进入让其会更新界面
    const [dataProvider] = useState(_dataProvider.cloneWithRows(data))


    const [_layoutProvider] = useState(new LayoutProvider(index=&gt;{
        if (index % 3 === 0) {
            return ViewTypes.FULL;
          } else if (index % 20 === 0) {
            return ViewTypes.HALF_LEFT;
          } else {
            return ViewTypes.HALF_RIGHT;
          }
    },(type,dim)=&gt;{
        switch (type) {
            case ViewTypes.HALF_LEFT:
              dim.width = width &#47; 2 - 0.0001;
              dim.height = 160;
              break;
            case ViewTypes.HALF_RIGHT:
              dim.width = width &#47; 2;
              dim.height = 160;
              break;
            case ViewTypes.FULL:
              dim.width = width;
              dim.height = 140;
              break;
            default:
              dim.width = 0;
              dim.height = 0;
          }
    }))
&#47;&#47; console.log(dataProvider)
    const _rowRenderer = (type,data)=&gt;{
        console.log(data,data.name)
        &#47;&#47;编写如何渲染数据
       return (
        &lt;View style={{height:10}}&gt;
           { [1,2,3].map(()=&gt;{
               return  &lt;Text key={String(new Date().getUTCMilliseconds())}&gt;data&lt;&#47;Text&gt;
            })}
        &lt;&#47;View&gt;
       )
    }

    return (
        &lt;RecyclerListView
            renderAheadOffset={100}
            layoutProvider={_layoutProvider}
            dataProvider={dataProvider}
            rowRenderer={_rowRenderer}
            style={{flex:1}}
        
        &#47;&gt;
    )

}</div>2022-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/29/28/b6b73f57.jpg" width="30px"><span>大龙龙龙</span> 👍（0） 💬（0）<div>老师， 问一下 之前的章节都是 funcation实现组件， 到这里 我看到demo里的recyclerlistview 为什么使用类来实现组件了呢？</div>2022-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/c1/93031a2a.jpg" width="30px"><span>Aaaaaaaaaaayou</span> 👍（0） 💬（2）<div>一般业务中列表数据都是分页请求的，按照文中的说法“已经渲染好的组件滚动是跟js没关系的”，那这种场景是不是用scrollview就好了？</div>2022-06-08</li><br/>
</ul>