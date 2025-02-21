你好，我是Mike。今天我们一起来学习Rust游戏编程技术。这节课我们会基于Bevy游戏框架来开发一个入门版的贪吃蛇游戏。

Rust生态内目前已经有不少很不错的游戏开发框架，而Bevy是其中最热门的那一个，目前（2023年12月）最新版本是 0.12，还处在积极开发的过程中。Bevy框架和Axum Web框架、Slint框架给人的感觉有点儿像，都很简单、优美、灵活。用Bevy框架写游戏非常惬意，已经有不少人在尝试使用Bevy开发自己的独立游戏，目前有三款（Molecoole、Tiny Glade、Roids）已经上架或即将上架 Steam。

用Bevy开发的游戏能够运行在Windows、macOS、Linux, Web浏览器等平台。

## Bevy框架

Bevy 框架是一个数据驱动的游戏开发框架（引擎），其核心是一个ECS。

### ECS

ECS是 Entity Component System 的缩写，意思是实体-组件-系统。它是一种编程范式，这种范式非常有趣，也非常有潜力，现在的主流游戏引擎都开始支持这种编程范式了。这种范式是与传统的OOP（面向对象编程）范式相对的，跟Rust的 trait 的设计理念有一些相似之处。

我们用一个例子来说明ECS是怎样对问题进行建模的。假如现在有这样一幅画面：一个下午，在温暖的家里面，爸爸D正在边吃甜点边看书，妈妈M在边吃甜点边玩手机，儿子S在和狗狗B玩。你想一想，这个场景如果用OOP方式，应该如何建模呢？而用ECS范式可以这样建立模型：
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1f/1b/be/525e05ae.jpg" width="30px"><span>NiceBlueChai</span> 👍（1） 💬（1）<div>还有个bug，向上走的过程中快速按左下（或者右下），蛇直接原地向相反方向走了</div>2024-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/36/33/3411df0d.jpg" width="30px"><span>seven9t</span> 👍（0） 💬（1）<div>补充了个最起码的长按加速功能，没找到timer的就地调频接口，只能另开了个timer做切换。各位有啥更好办法么。</div>2024-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/44/22/403a340a.jpg" width="30px"><span>unistart</span> 👍（0） 💬（2）<div>BUG: 食物可能在蛇身上产生
处理:  在生成食物的时候，判断一下随机生成的Position值是否和当前蛇的某一个部分位置是重合的，如果是就直接return，不生成食物。

&#47;&#47; 修改food_spawner
fn food_spawner(
    mut commands: Commands, 
    time: Res&lt;Time&gt;,
    mut timer: ResMut&lt;FoodSpawnTimer&gt;,
    segment_pos_set: Query&lt;&amp;Position, With&lt;SnakeSegment&gt;&gt;
)
{
    &#47;&#47; ...

    let rand_x: i32 = (random::&lt;f32&gt;() * ARENA_WIDTH as f32) as i32;
    let rand_y: i32 = (random::&lt;f32&gt;() * ARENA_HEIGHT as f32) as i32;
        
    for pos in segment_pos_set.iter() {
        if pos.x == rand_x &amp;&amp; pos.y == rand_y {
            return;
        }
    }

    &#47;&#47; ...
    .insert(Position {
        x: rand_x,
        y: rand_y,
    })
    &#47;&#47; ...
}

BUG: 食物有可能在已经产生过的地方产生
个人感觉这个不太算bug吧，分两种情况看，一种是食物A之前被吃过，又在相同的位置生成了新的食物，这个应该是没问题的；另一种就是食物A之前没有被吃过，同时新生成的食物B的位置和食物A重合，这样确实貌似有问题。
但是我不知道Bevy是如何处理的，按我的理解来说食物B应该会盖掉食物A，即某一位置只会有一个最新的食物实体。还是说bevy中出现这种情况，同一位置会有多个实体。如果是同一位置有多个实体的话，那么再Query一下已经生成的Food的Position，然后和新生成的食物坐标比较一下是否有出现的重合就行了吧。</div>2023-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a6/8c/344f03dd.jpg" width="30px"><span>大白菜🥬</span> 👍（0） 💬（1）<div>14步那里需要添加LastTailPosition资源， App需要添加 .insert_resource(LastTailPosition::default())</div>2023-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/5f/894761f8.jpg" width="30px"><span>十八哥</span> 👍（0） 💬（1）<div>当年用vb.net用了1千行实现的。思路是按钮数组，一个二维数组。</div>2023-12-26</li><br/>
</ul>