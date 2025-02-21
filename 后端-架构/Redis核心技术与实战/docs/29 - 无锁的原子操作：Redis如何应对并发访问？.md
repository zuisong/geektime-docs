你好，我是蒋德钧。

我们在使用Redis时，不可避免地会遇到并发访问的问题，比如说如果多个用户同时下单，就会对缓存在Redis中的商品库存并发更新。一旦有了并发写操作，数据就会被修改，如果我们没有对并发写请求做好控制，就可能导致数据被改错，影响到业务的正常使用（例如库存数据错误，导致下单异常）。

为了保证并发访问的正确性，Redis提供了两种方法，分别是加锁和原子操作。

加锁是一种常用的方法，在读取数据前，客户端需要先获得锁，否则就无法进行操作。当一个客户端获得锁后，就会一直持有这把锁，直到客户端完成数据更新，才释放这把锁。

看上去好像是一种很好的方案，但是，其实这里会有两个问题：一个是，如果加锁操作多，会降低系统的并发访问性能；第二个是，Redis客户端要加锁时，需要用到分布式锁，而分布式锁实现复杂，需要用额外的存储系统来提供加解锁操作，我会在下节课向你介绍。

**原子操作是另一种提供并发访问控制的方法**。原子操作是指执行过程保持原子性的操作，而且原子操作执行时并不需要再加锁，实现了无锁操作。这样一来，既能保证并发控制，还能减少对系统并发性能的影响。

这节课，我就来和你聊聊Redis中的原子操作。原子操作的目标是实现并发访问控制，那么当有并发访问请求时，我们具体需要控制什么呢？接下来，我就先向你介绍下并发控制的内容。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_fb6ea6</span> 👍（30） 💬（8）<div>Redis不是单线程吗？怎么还会有并发读写的问题呢</div>2020-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（337） 💬（36）<div>是否需要把读取客户端 ip 的访问次数 GET(ip)，以及判断访问次数是否超过 20 的判断逻辑，也加到 Lua 脚本中？

我觉得不需要，理由主要有2个。

1、这2个逻辑都是读操作，不会对资源临界区产生修改，所以不需要做并发控制。

2、减少 lua 脚本中的命令，可以降低Redis执行脚本的时间，避免阻塞 Redis。

另外使用lua脚本时，还有一些注意点：

1、lua 脚本尽量只编写通用的逻辑代码，避免直接写死变量。变量通过外部调用方传递进来，这样 lua 脚本的可复用度更高。

2、建议先使用SCRIPT LOAD命令把 lua 脚本加载到 Redis 中，然后得到一个脚本唯一摘要值，再通过EVALSHA命令 + 脚本摘要值来执行脚本，这样可以避免每次发送脚本内容到 Redis，减少网络开销。</div>2020-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ff/51/9d5cfadd.jpg" width="30px"><span>好运来</span> 👍（20） 💬（7）<div>“对于这些操作，我们同样需要保证它们的原子性。否则，如果客户端使用多线程访问，访问次数初始值为 0，第一个线程执行了 INCR(ip) 操作后，第二个线程紧接着也执行了 INCR(ip)，此时，ip 对应的访问次数就被增加到了 2，我们就无法再对这个 ip 设置过期时间了。这样就会导致，这个 ip 对应的客户端访问次数达到 20 次之后，就无法再进行访问了。即使过了 60s，也不能再继续访问，显然不符合业务要求。&quot;

对于这段话我有疑惑，假如有两个线程A和线程B，初始ip计数是0，线程A和线程B并发执行，不管线程A和线程B谁先执行到 value = INCR(ip) ，获取到的value值总会有一个是1，而value作为线程的局部变量，也是可以继续执行下去，那不就是能够执行到 IF value == 1 THEN        EXPIRE(ip,60)    END 这个判断逻辑了吗，不明白为什么说不能设置先到的ip过期时间60s了?



</div>2020-11-01</li><br/><li><img src="" width="30px"><span>dfuru</span> 👍（19） 💬（3）<div>获取访问次数和判断访问是否大于20，
若放到lua脚本中，获取到的访问次数是准确的最新值，进行判断更准确；
当放到lua脚本外，并发访问时某线程获取到的访问次数可能旧(偏小)，当获取到访问次数为19时(实际可能已经达到20了)，该线程仍然会对访问次数执行+1，所以应该放到lua中。</div>2020-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/f9/75d08ccf.jpg" width="30px"><span>Mr.蜜</span> 👍（9） 💬（1）<div>是否需要把读取客户端 ip 的访问次数 GET(ip)，以及判断访问次数是否超过 20 的判断逻辑，也加到 Lua 脚本中？

我觉得需要分3步来优化：
1.在执行lua之前，get(ip)，进行判断，如果大于20，就直接报错了，这样也就减少了执行lua的开销；
2.在执行lua时，判断incr（ip）的返回值，这个值是加一之后的值，直接判断这个值是否大于20，返回错误。
3.如果并发量特别大的时候，可以在incr前再判断一次get（ip），减少incr的开销。</div>2020-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/83/4b/0e96fcae.jpg" width="30px"><span>sky</span> 👍（8） 💬（6）<div>对于这些操作，我们同样需要保证它们的原子性。否则，如果客户端使用多线程访问，访问次数初始值为 0，第一个线程执行了 INCR(ip) 操作后，第二个线程紧接着也执行了 INCR(ip)，此时，ip 对应的访问次数就被增加到了 2，我们就无法再对这个 ip 设置过期时间了。这样就会导致，这个 ip 对应的客户端访问次数达到 20 次之后，就无法再进行访问了。即使过了 60s，也不能再继续访问，显然不符合业务要求。


不太明白为何过了 60 秒，也不能继续访问呢</div>2020-10-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIY8df9yV6vQjOMxv5xym070hFT2GWYELpqBhxSicQoq5IqBx6teS1xJaomkOBeuzv4vkXRJfibqcMw/132" width="30px"><span>永不止步</span> 👍（7） 💬（1）<div>除了技术之外，我觉得那段代码的判断逻辑应该属于业务范畴，最好不要放lua中，因为业务是经常变化的，lua脚本最好与具体业务无关</div>2021-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/e2/2dcab30d.jpg" width="30px"><span>郑印</span> 👍（6） 💬（3）<div>感觉 “Redis 在执行 Lua 脚本时，是可以保证原子性的”  这句话有误导，当lua脚本中间有命令执行出错时，以执行的命令还是生效了的，这样不能完全称之为原子性。redis只是通过lua脚本让一组命令想一个命令一样执行在加上单线程的特性避免了并发产生的问题，而不能称之为原子性。</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fc/0a/0c4b9170.jpg" width="30px"><span>泠小墨</span> 👍（4） 💬（4）<div>关于最后的问题，我觉得可以不判断访问次数，前提稍微修改下lua脚本，将current的值返回给客户端，这样客户端可以根据返回值进行处理；
local current 
current = redis.call(&#39;incr&#39;,KEYS[1]) 
if tonumber(current)==1 then redis.call(&#39;expire&#39;,KEYS[1],60) 
end  
return current</div>2020-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/f6/76/f7666f76.jpg" width="30px"><span>huiye</span> 👍（3） 💬（2）<div>除了把多个操作在 Redis 中实现成一个操作，和使用lua脚本，使用redis的事务，把多个命令放入队列里一起执行，是不是也能保证原子性呢</div>2021-02-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ZGbq9QcsysWhYJvIXaZ0S9llXDVicF0Tvm2ibgGehHCPYWxHzZ2Z34SVOyIOKkH44qPFCANBbib2iawqrWU7azD3og/132" width="30px"><span>Geek_750e24</span> 👍（3） 💬（1）<div>  value = INCR(ip)    &#47;&#47;如果是第一次访问，将键值对的过期时间设置为60s后  
  IF value == 1 
  THEN       
  EXPIRE(ip,60)    
END
执行 INCR命令返回value不是原子操作么？就算两个线程执行了INCR，第一个线程返回的不是1么？</div>2020-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（3） 💬（0）<div>思考题
思考题：是否需要把读取客户端 ip 的访问次数，也就是 GET(ip)，以及判断访问次数是否超过 20 的判断逻辑，也加到 Lua 脚本中吗？
我觉得不需要将其添加到 Lua 脚本中，理由如下：
1.获取客户端 ip 的访问次数和判断访问次数是否超过 20 并没有进行 R-M-W 操作即这个代码没有操作临界区代码，所以不会有并发问题
2.因为如果把更多操作加到 Lua 脚本中，会导致 Redis 执行 Lua 脚本的时间增加，会降低 Redis 的并发性能，建议就是在编写 Lua 脚本中，要避免添加不需要做并发控制的代码

补充
上面的 Lua 脚本中有一个是判断次数是否为 1，按道理这个操作也是读操作，没有操作临界区的代码，为何要把它加到 Lua 脚本中呢？
这个是因为客户端 ip 的访问次数 +1 和 判断是否等于 1 ，和后面的设置过期时间，是一个最小的逻辑单元，这个判断会影响到后面过期时间的设，所以这个读操作要加入到 Lua 脚本中</div>2020-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/44/d8/1a1761f9.jpg" width="30px"><span>James_Shangguan</span> 👍（2） 💬（1）<div>不需要加到Lua脚本里面。并发编程思想里面，降低锁的粒度，提高并发的性能。</div>2021-11-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJRFRX8kNzNet7FibNvtavbVpAwK09AhIhrib9k762qWtH6mre8ickP7hM5mgZC4ytr8NnmIfmAhxMSQ/132" width="30px"><span>老大不小</span> 👍（2） 💬（0）<div>之前文章里不是有讲另外一种方式——MULTI和EXEC吗？这种是不是可以实现lua脚本一样的功能？</div>2021-04-27</li><br/><li><img src="" width="30px"><span>Geek_89e362</span> 👍（2） 💬（1）<div>我感觉需要，比如当前 count 为19 ，但是并发上来三个请求，调用get获取的都是19，小于20，那么访问的次数可能就会超过20了。</div>2021-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6c/b5/32374f93.jpg" width="30px"><span>可怜大灰狼</span> 👍（2） 💬（0）<div>我觉得get(ip)可以不需要，因为incr已经可以返回当前访问次数，current值大于20的时候，直接返回客户端加锁失败。但是判断是否超过20次逻辑，应该要加到lua脚本中，不然没法保证对控制次数的原子性</div>2020-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/bb/8b2ba45d.jpg" width="30px"><span>冯传博</span> 👍（2） 💬（3）<div>对于这些操作，我们同样需要保证它们的原子性。否则，如果客户端使用多线程访问，访问次数初始值为 0，第一个线程执行了 INCR(ip) 操作后，第二个线程紧接着也执行了 INCR(ip)，此时，ip 对应的访问次数就被增加到了 2，我们就无法再对这个 ip 设置过期时间了。这样就会导致，这个 ip 对应的客户端访问次数达到 20 次之后，就无法再进行访问了。即使过了 60s，也不能再继续访问，显然不符合业务要求。


如果第一个线程正常执行，是能够给ip设置过期时间的，也就能够满足业务。出现没有设置过期时间的情景，是线程一在设置过期时间之前退出了。

这段代码还有个问题是，在高并发的时候20次的访问限制可能会被击穿，也就是访问次数能够超过20次。

不知理解是否争取，请老师指教</div>2020-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/a2/7c/be30e54c.jpg" width="30px"><span>不动</span> 👍（1） 💬（0）<div>&quot;第一个线程执行了 INCR(ip) 操作后，第二个线程紧接着也执行了 INCR(ip)，此时，ip 对应的访问次数就被增加到了 2，我们就无法再对这个 ip 设置过期时间了&quot;
老师, 你这里说的貌似有误吧。两个线程同时执行incr，总有一个先后，先的那个的返回值肯定是1，后的那个是2，所以先的那个必然会设置好过期时间。所以这里不需要使用lua脚本</div>2024-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（1） 💬（0）<div>Redis 同样会遇到并发访问问题，为了保证并发访问，Redis 提供了加锁和原子操作两种方式。

其实原子操作听上去比较高端，但实际上就是让多个操作变成一步，和事务有点像。加一减一这种比较简单的，Redis 自身就提供了 INCR&#47;DECR 的命令；对于复杂多步骤的，可以编写 Lua 脚本，而 Redis 把 Lua 脚本当做“一条”命令来处理。

当然，如果 Lua 脚本内的操作过于复杂，耗时过长，Redis 的性能也会受到影响。

我觉的 Redis 从一出生，就是当做缓存来设计的，最好只做简单的读写操作（要是用作只读缓存就更合适了）。

对于课后题，读取客户端 ip 的访问次数，不需要添加到 Lua 脚本里面。假设有多个并发访问，获取到了当前的 ip 访问次数，假设不超过 20 且不为 NULL 值，那么每次（并发）访问，都给访问次数加一，这个没有问题。如果 value == 1，那么就设置过期时间，如果哪一个并发访问到了，都可以执行。

唯一可能有问题的地方，就是有超过 20 个并发同时访问到了 GET(ip)，并且得到的值小于 20，然后都执行了加一操作，那么就会超过 20 的访问次数限制。</div>2021-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/41/5b/23baaded.jpg" width="30px"><span>猫猫虫</span> 👍（1） 💬（0）<div>无论是使用lua脚本还是业务加锁，本质上都是保证读并修改的原子性，读并修改未执行完成前都会阻塞其他请求，那为什么更推荐lua脚本呢，redis在执行过程中是如何实现读写锁的功能，并保证比业务加锁效率更高呢</div>2021-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/a6/188817b6.jpg" width="30px"><span>郭嵩阳</span> 👍（1） 💬（0）<div>想问下老师,你们在开发项目中是否，经常使用lua脚本.或者是否建议经常去使用lua脚本,个人觉得lua脚本维护不是很方便，相听一下老师的意见</div>2020-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/78/52/116508b8.jpg" width="30px"><span>字节情怀</span> 👍（0） 💬（0）<div>想问下老师，redis对同一个key 的INCR操作如果并发太高是不是会有问题？会变成类似热点key问题吗？比如要一秒限流10W的请求，相当于1秒有10W的请求操作同一个redis key</div>2024-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/21/77949293.jpg" width="30px"><span>Paualf</span> 👍（0） 💬（0）<div>GET(ip) 不需要放到里面，因为每个并发访问是一样的，判断访问次数是否超过20的判断逻辑，也不需要放到lua脚本里面，都是读取操作，不涉及到并发操作，可以放到外面</div>2023-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/ab/fd201314.jpg" width="30px"><span>小耿</span> 👍（0） 💬（0）<div>请问老师，加锁和使用 lua 脚本有什么区别吗？我理解加锁和 lua 脚本都是串行执行临界区代码片段，在性能上会有不同吗？</div>2023-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/ab/fd201314.jpg" width="30px"><span>小耿</span> 👍（0） 💬（0）<div>需要，如果不控制并发，多个客户端同时获取到初始值 A = 20，其中一个客户端将 A 加 1，此时 A` = 21 的值大于 20，按照业务要求，后续其它客户端的操作应该失败。但实际上，此时其它客户端拿到的 A 仍然是 20，所以会继续执行加1等业务逻辑，不符合业务要求。</div>2023-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b8/41/d33a7f53.jpg" width="30px"><span>Dai Yan</span> 👍（0） 💬（0）<div>感觉每个客户的点赞次数都是独立的，所以不同客户端的点击次数不会互相干扰，在某一个客户的session里，读是否放入lua，效果是一样的。因为incr只会针对自己的点击次数加一，别人不会来改变这个值。如果不是这个场景，多个客户端共享一个后台数据，那get（IP）就要放到lua里面，因为，可能不同的客户端incr会改变次数，这个跟当时读取的时候，已经不一样了，可能是+2或+3，那这样可能点击不到20次，就要停止了。但这个也不可能，因为点击次数是分到每个客户的。这个是我的疑问。</div>2023-01-27</li><br/><li><img src="" width="30px"><span>beifengzhishen001</span> 👍（0） 💬（0）<div>multi&#47;exec执行的组合语句，假设所有语句都没有发生错误，算不算原子操作呢？考虑到redis执行客户端请求都是并行操作，看到第31节的内容后，回过头来看本节有了这个疑问。</div>2022-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/6c/bc/f751786b.jpg" width="30px"><span>Ming</span> 👍（0） 💬（0）<div>为什么不在一个lua脚本内可以做到如下几点：
1. 判断改ip是否第一次访问，是的话设置过期时间60秒，同时该ip访问次数+1;
2. 如果不是第一次，且访问次数小于20，那么则在当前次数上+1；
3.如果当前次数大于等于20直接返回错误，不进行后续逻辑；
这样所有操作都通过lua脚本实现原子性，更能保证准确及并发性；为什么文章中没有这种方式</div>2022-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/6c/bc/f751786b.jpg" width="30px"><span>Ming</span> 👍（0） 💬（0）<div>这种读取方式和塞入方式在高并发的情况下一定会超过20，因为读取和增加值这两个动作不是一个完整的原子性操作；那么必定会产生两个线程都读取次数为19，然后两个线程都加1超过20次的情况；</div>2022-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/46/a0/aa6d4ecd.jpg" width="30px"><span>张潇赟</span> 👍（0） 💬（0）<div>老师说的场景是限流，所以我理解如果多几次访问应该是问题不大的。所以可以将get 和比较放在lua脚本外执行。这样尽可能的降低lua脚本的成本</div>2022-03-29</li><br/>
</ul>