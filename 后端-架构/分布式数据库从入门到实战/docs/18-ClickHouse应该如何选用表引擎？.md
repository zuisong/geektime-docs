你好，我是彭旭。

我们在上节课讲ClickHouse的极致性能的时候，提到了ClickHouse支持灵活多样的表引擎，而每个表引擎都有自己的适用场景。

表引擎决定了数据表最终数据存储的模式，能够支撑的数据量大小，数据读写的方式等等。如果选择了不恰当的表引擎，可能会导致数据的存储结构不合理，影响数据的读写效率，甚至限制系统对大规模数据的支持能力。

这一讲，我们就来认识一下ClickHouse最强大的MergeTree表引擎系列。

## MergeTree

MergeTree以及其家族（MergeTree）的其他引擎系列是ClickHouse中使用最多，最强大的引擎。

先来看一个使用MergeTree引擎创建CDP用户表的示例。

```shell
CREATE TABLE cdp_user (
    unique_user_id UInt64 COMMENT '用户全局唯一ID，ONE-ID',
    name String COMMENT '用户姓名',
    nickname String COMMENT '用户昵称',
    gender Int8 COMMENT '性别：1-男；2-女；3-未知',
    birthday String COMMENT '用户生日：yyyyMMdd',
    user_level Int8 COMMENT '用户等级：1-5',
    register_date DateTime64 COMMENT '注册日期',
    last_login_time DateTime64 COMMENT '最后一次登录时间'
) ENGINE = MergeTree()
PARTITION BY register_date
PRIMARY KEY unique_user_id
ORDER BY unique_user_id;
```