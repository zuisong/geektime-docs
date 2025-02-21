你好，我是朱晔。今天，我来和你说说恼人的时间错乱问题。

在Java 8之前，我们处理日期时间需求时，使用Date、Calender和SimpleDateFormat，来声明时间戳、使用日历处理日期和格式化解析日期时间。但是，这些类的API的缺点比较明显，比如可读性差、易用性差、使用起来冗余繁琐，还有线程安全问题。

因此，Java 8推出了新的日期时间类。每一个类功能明确清晰、类之间协作简单、API定义清晰不踩坑，API功能强大无需借助外部工具类即可完成操作，并且线程安全。

但是，Java 8刚推出的时候，诸如序列化、数据访问等类库都还不支持Java 8的日期时间类型，需要在新老类中来回转换。比如，在业务逻辑层使用LocalDateTime，存入数据库或者返回前端的时候还要切换回Date。因此，很多同学还是选择使用老的日期时间类。

现在几年时间过去了，几乎所有的类库都支持了新日期时间类型，使用起来也不会有来回切换等问题了。但，很多代码中因为还是用的遗留的日期时间类，因此出现了很多时间错乱的错误实践。比如，试图通过随意修改时区，使读取到的数据匹配当前时钟；再比如，试图直接对读取到的数据做加、减几个小时的操作，来“修正数据”。
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（55） 💬（3）<div>试着回到下问题：
第一个：
Date的toString()方法处理的，同String中有BaseCalendar.Date date = normalize();
而normalize中进行这样处理cdate = (BaseCalendar.Date) cal.getCalendarDate(fastTime,TimeZone.getDefaultRef()；
因此其实是获取当前的默认时区的。
第二个：
从下面几个维度进行区分：
占用空间：datetime：8字节。timestamp 4字节
表示范围：datetime	&#39;1000-01-01 00:00:00.000000&#39; to &#39;9999-12-31 23:59:59.999999&#39;
		timestamp	&#39;1970-01-01 00:00:01.000000&#39; to &#39;2038-01-19 03:14:07.999999&#39;
时区：timestamp 只占 4 个字节，而且是以utc的格式储存， 它会自动检索当前时区并进行转换。
	datetime以 8 个字节储存，不会进行时区的检索.
	也就是说，对于timestamp来说，如果储存时的时区和检索时的时区不一样，那么拿出来的数据也不一样。对于datetime来说，存什么拿到的就是什么。
更新：timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP；
	这个特性是自动初始化和自动更新（Automatic Initialization and Updating）。
	自动更新指的是如果修改了其它字段，则该字段的值将自动更新为当前系统时间。
	它与“explicit_defaults_for_timestamp”参数有关。

	By default, the first TIMESTAMP column has both DEFAULT CURRENT_TIMESTAMP and ON UPDATE CURRENT_TIMESTAMP if neither is specified explicitly。
	很多时候，这并不是我们想要的，如何禁用呢？
		1. 将“explicit_defaults_for_timestamp”的值设置为ON。
		2. “explicit_defaults_for_timestamp”的值依旧是OFF，也有两种方法可以禁用
     		1&gt; 用DEFAULT子句该该列指定一个默认值
     		2&gt; 为该列指定NULL属性。


    在MySQL 5.6.5版本之前，Automatic Initialization and Updating只适用于TIMESTAMP，而且一张表中，最多允许一个TIMESTAMP字段采用该特性。从MySQL 5.6.5开始，Automatic Initialization and Updating同时适用于TIMESTAMP和DATETIME，且不限制数量。</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（20） 💬（3）<div>对于时间，我个人的理解和目前的使用经验是——能用时间戳就用时间戳。
时间戳有几个优势：
1，便于比较和排序，无论数据库还是后台业务中都是如此。
2，也比较便于计算，虽然文中提到了Long的问题，但是，我认为L的问题的根本在于Long类型的理解，不是时间戳这个业务的问题。对Long的基础比较好了之后，也就足以应对计算中的问题了。
3，多端统一，现在提供给前端的很多服务都采用直接转换好年月日的字符串了，但是有时候，前端需要对时间进行比较的时候还是需要额外转化，会很麻烦。而且不利于格式化。时间戳的话就避免了这个问题，自己进行计算，自己格式化。前端自己随便玩。
</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（15） 💬（1）<div>第一个问题，虽然 Date 本质是一个时间戳没有时区的概念，但是在 toString 的时候为了可读性会推测当前时区，如果得不到就会使用 GMT。</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f5/43/b882ab43.jpg" width="30px"><span>俊柱</span> 👍（5） 💬（1）<div>老师，映射表的bean，若数据库字段为 Timestamp，那 java 的字段应该设为 ZonedDateTime 最为合理吗？ 因为我看网上很多人都是用 LocalDateTime 进行映射</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/21/bb289d5e.jpg" width="30px"><span>lee</span> 👍（4） 💬（1）<div>老师好，上海时区和纽约时区下，格式化同一个时间串得到的当前时差有时候是12小时，有时候是13小时呢，把stringDate改成2020-05-02 22:00:00得到的相差12小时
String stringDate = &quot;2020-05-02 22:00:00&quot;;
SimpleDateFormat inputFormat = new SimpleDateFormat(&quot;yyyy-MM-dd HH:mm:ss&quot;);
&#47;&#47;同一Date
Date date = inputFormat.parse(stringDate);
&#47;&#47;默认时区格式化输出：
System.out.println(new SimpleDateFormat(&quot;[yyyy-MM-dd HH:mm:ss Z]&quot;).format(date));
&#47;&#47;纽约时区格式化输出
TimeZone.setDefault(TimeZone.getTimeZone(&quot;America&#47;New_York&quot;));
System.out.println(new SimpleDateFormat(&quot;[yyyy-MM-dd HH:mm:ss Z]&quot;).format(date));</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（3） 💬（1）<div>今天踩坑private static simpledateformat，高并发下出现numberformatexception错误。单笔数据重放没有问题。初看到这个异常一脸懵，完全联系不到是simpledateformat的坑。
后面突然想起老师这篇文章。。。完全是坑二的重现。因为是jdk6所以选择了去掉static解决，每次都会新建一个对象</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cb/18/4877c08b.jpg" width="30px"><span>eazonshaw</span> 👍（3） 💬（1）<div>问题二：
首先，为了让docker容器的时间格式和宿主机一致，可以在environment中添加TZ: Asia&#47;Shanghai。
实验发现，切换mysql的TIME_ZONE到“america&#47;new_york”后，发现datetime格式字段不发生变化，而timestamp格式会换算成纽约时区时间，所以timestamp格式的日期保存了时区信息，而datetime没有。
感觉在业务场景中，有可能出现服务器或容器系统时间并未设置时区，导致保存的数据并不是我们想要的。因此，是不是更推荐使用timestamp格式来保存日期，避免这种情况发生呢？</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（3） 💬（1）<div>思考题2:
说实话，数据库相关知识是我的弱项。
查了一下，大概是TIMESTAMP包含了时区信息，而DATETIME不包含。另外有一个是，我印象中5.7之后的mysql版本，最多只能有一个TIMESTAMP的字段。这也算是个区别吧。</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f5/43/b882ab43.jpg" width="30px"><span>俊柱</span> 👍（2） 💬（1）<div>老师，我有一个问题困扰已久，希望能够解答一下，目前我们对外输出的 API ，时间都是时间戳的形式， 内部系统的交互，时间也是时间戳的形式。 那我用 Instant 去映射数据库的 Timestamp&#47;DateTime 字段，会不会更好？ 否则的话，需要在多处都要注意 LocalDateTime 和 时间戳的相互转换 （比如 redis 的序列化反序列化，json 的序列化、反序列化）</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/62/d5/1f5c5ab6.jpg" width="30px"><span>大大大熊myeh</span> 👍（2） 💬（1）<div>我虽然现在用的是jdk1.8，但对于日期的操作一般还是习惯于用Date或long，以后可以尝试用LocalDateTime等类。

思考题1
Date#toString方法中，会将当前时间转化为BaseCalendar.Date类，这个类有一个Zone属性，在toString的时候会被追加到字符串中（默认是GMT）

思考题2
datetime占用8字节，不受时区影响，表示范围&#39;1000-01-01 00:00:00&#39; to &#39;9999-12-31 23:59:59&#39;
timestamp占用4字节，受时区影响，表示范围&#39;1970-01-01 00:00:01&#39; to &#39;2038-01-19 03:14:07&#39;，若插入null会自动转化为当前时间</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（2） 💬（1）<div>第二个问题，timestamp 会把传入的时间转化为 UTC 即时间戳进行存储，而 datetime 也直接将传入的时间存储。</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ff/d0/402be1e9.jpg" width="30px"><span>VIC</span> 👍（1） 💬（1）<div>threadlocal simpledateformat，有完整例子吗</div>2020-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/73/a3/2b077607.jpg" width="30px"><span>Michael</span> 👍（1） 💬（3）<div>private static final DateTimeFormatter df = DateTimeFormatter.ofPattern(&quot;yyyy-MM-dd HH:mm:ss&quot;);

**
     * 获取本周一开始时间
     * @return
     *&#47;
    public static String getFirstTimeByWeek() {
        LocalDateTime currentTime = LocalDateTime.now();
        LocalDateTime weekStartTime = currentTime.with(TemporalAdjusters.previous(DayOfWeek.SUNDAY)).plusDays(1).truncatedTo(ChronoUnit.DAYS);
        &#47;&#47;求出这个日期所在周的星期一
        return weekStartTime.format(df);
    }


    &#47;**
     * 获取本周一截止时间
     * @return
     *&#47;
    public static String getLastTimeByWeek() {
        LocalDateTime currentTime = LocalDateTime.now();
        LocalDateTime weekEndTime = currentTime.with(TemporalAdjusters.next(DayOfWeek.MONDAY)).minusDays(1);
        &#47;&#47;求出这个日期所在周的星期一
        return weekEndTime.format(df);
    }


    &#47;**
     * 获取当月第一天其实时间
     * @return
     *&#47;
    public static String getFirstTimeByMonth() {
        LocalDateTime currentTime = LocalDateTime.now();
        LocalDateTime monthStartDate = currentTime.withDayOfMonth(1).truncatedTo(ChronoUnit.DAYS);
        return monthStartDate.format(df);
    }

    &#47;**
     * 获取当月最后一天截止时间
     * @return
     *&#47;
    public static String getLastTimeByMonth() {
        LocalDateTime currentTime = LocalDateTime.now();
        LocalDateTime monthEndDate = currentTime.plusMonths(1L).withDayOfMonth(1).truncatedTo(ChronoUnit.DAYS).plus(-1L, ChronoUnit.MILLIS);
        return monthEndDate.format(df);
    }

获取本周日截止时间的时候总是获取不到时分秒的那部分:23:59:59</div>2020-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cf/14/384258ba.jpg" width="30px"><span>Wiggle Wiggle</span> 👍（1） 💬（1）<div>我在外企，公司大部分数据用的洛杉矶时间（带了夏令时），处理数据的时候要面对各种不带时区的string或datetime，无比酸爽</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/65/f444ea39.jpg" width="30px"><span>grandcool</span> 👍（0） 💬（1）<div>老师，为啥“不同的本地时间可能对应同一个 UTC”啊？</div>2020-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b7/f0/a570f68a.jpg" width="30px"><span>wang</span> 👍（0） 💬（1）<div>感觉LocalDateTime像是存了当前时区的zoneddatetime？</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/49/0b9ffc8e.jpg" width="30px"><span>刘大明</span> 👍（0） 💬（1）<div>思考题1.是toString 方法里面if (zi != null) {
            sb.append(zi.getDisplayName(date.isDaylightTime(), TimeZone.SHORT, Locale.US)); &#47;&#47; zzz
        } else {
            sb.append(&quot;GMT&quot;);
        }
加了这个输出结果

</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5d/6f/42494dcf.jpg" width="30px"><span>Jerry Wu</span> 👍（0） 💬（1）<div>在日期上，我没踩过坑。

首先，我做的都是国内项目，不会出现时区的问题；
其次，对时间的应用真不多，就是时间的保存、格式化、比较；

看来我还是太狭隘了，最近三节课说到的坑都没见过。周末得多跑几遍老师的代码，加深感受才行。</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（13） 💬（0）<div>思考题1:
根本原因在于toString的源代码：
sb.append(zi.getDisplayName(date.isDaylightTime(), TimeZone.SHORT, Locale.US)); &#47;&#47; zzz 这一行。
Date的toString实际上，是新建一个StringBuilder，然后根据Date对象里的年月日周，将其格式化。
格式化过程中，似乎会获取系统默认的时区，如果取不到系统默认时区，就使用GMT。
为了测试我的猜想，我尝试更改本机时区，结果输出：
Wed Apr 15 21:40:10 EDT 2020
相比较正常自动时区
Thu Apr 16 09:41:31 CST 2020
基本与我的猜测一致。



</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/bb/947c329a.jpg" width="30px"><span>程序员小跃</span> 👍（1） 💬（0）<div>学习这个专栏的前几篇的时候，就发现需要有很强的Java 8功底，作为一名Javaer，我买了本《Java 实战》来更好的学习Java 8的新特性，也能跟上课程的节奏。</div>2020-07-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erTlRJ6skf7iawAeqNfIT1PPgjD7swUdRIRkX1iczjj97GNrxnsnn3QuOhkVbCLgFYAm7sMZficNTSbA/132" width="30px"><span>senekis</span> 👍（1） 💬（0）<div>1. 时区问题的原因

Date和Instant都可以根据时间戳来创建，其中并不包含时区信息，因此并不会出现所谓的时间错误。
因此在保存数据时，都可以通过Long型来保存时间戳信息。
当需要实现日期格式化时，通过将时间戳转换为对应的时区的时间进行显示。


2. 测试Demo

public class DateTest {

    @Test
    public void timeStampTest() {

        Date date = new Date();
        Instant instant = date.toInstant();
        assertEquals(date.getTime(), instant.toEpochMilli());

        ZoneId shZoneId = ZoneId.of(&quot;Asia&#47;Shanghai&quot;);
        ZoneId cgZoneId = ZoneId.of(&quot;America&#47;Chicago&quot;);
        LocalDateTime shLocalDateTime =  LocalDateTime.ofInstant(instant, shZoneId);
        LocalDateTime cgLocalDateTime = LocalDateTime.ofInstant(instant, cgZoneId);
        assertEquals(shLocalDateTime.getSecond(), cgLocalDateTime.getSecond());
        assertEquals(Math.abs(shLocalDateTime.getHour() - cgLocalDateTime.getHour()), 13);

        ZonedDateTime shZonedDateTime = ZonedDateTime.of(shLocalDateTime, shZoneId);
        ZonedDateTime cgZonedDateTime = ZonedDateTime.of(cgLocalDateTime, cgZoneId);
        assertEquals(shLocalDateTime.getSecond(), cgZonedDateTime.getSecond());

        DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern(&quot;yyyy-MM-dd HH:mm:ss&quot;);
        String shDateTimeStr = dateTimeFormatter.format(shZonedDateTime);
        String cgDateTimeStr = dateTimeFormatter.format(cgZonedDateTime);
        assertFalse(shDateTimeStr.equals(cgDateTimeStr));

    }

}</div>2020-06-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/BDqfaEhaYiaRLj92HaU4P8fNciaXaCia9VnSEpIy5SqzlgvrxpNJ0e8FPGYqMg1PrCuXCbaJxyoJwukns7LdPCIHg/132" width="30px"><span>Geek_0b535f</span> 👍（0） 💬（0）<div>请教一下，原子钟校准会不会导致两个时间戳对应一个时间</div>2022-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c6/94/48ca3281.jpg" width="30px"><span>奔跑</span> 👍（0） 💬（0）<div>映射数据库时，Date用什么替换呢，LocalDateTime还是Instant？
JDK8的LocalDate和joda.time的LocalDate哪个更适合用在项目里？</div>2022-10-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJBru6Qa44qibaOnbEQprP1SOhBq0YWHCsjBAvNKmSu7DxKNSmtbiaZ1nQGf56m2gMDicsjiasnzI5VAw/132" width="30px"><span>车鸿韡</span> 👍（0） 💬（0）<div>MySQL时间戳有范围限制，那么date时间戳有范围限制吗？</div>2022-01-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ersGSic8ib7OguJv6CJiaXY0s4n9C7Z51sWxTTljklFpq3ZAIWXoFTPV5oLo0GMTkqW5sYJRRnibNqOJQ/132" width="30px"><span>walle斌</span> 👍（0） 💬（0）<div>我选择用joda-time 的 DateTime 而且绝大部分新老项目都是这个。。连贯性很好。。中间计算绝对时间也是方便的很。。 </div>2021-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2e/8c/b261e15a.jpg" width="30px"><span>张滔</span> 👍（0） 💬（0）<div>老师，java里面有接受字符串参数，然后返回日期对象的API吗？类似于java.util.Date里面的构造函数public Date(String s) ，但这个构造函数是Deprecated。</div>2021-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（0） 💬（0）<div>我用springboot2.2.x在POJO中分别使用LocalDateTime, Instant, ZonedDateTime中插入字段到mongodb中，其中ZonedDateTime不能直接插入，需要额外增加Convert进行转换。针对国际业务，用Instant可能会更方便些，然后使用带ZoneId的DateTimeFormatter进行格式化。如果只是国内业务，我觉得使用LocalDateTime就够用了。请老师及小伙伴们指正。</div>2020-11-25</li><br/><li><img src="" width="30px"><span>李松</span> 👍（0） 💬（0）<div>我开发中一般使用优秀的开源工具包，Apache commons  , joda</div>2020-06-17</li><br/>
</ul>