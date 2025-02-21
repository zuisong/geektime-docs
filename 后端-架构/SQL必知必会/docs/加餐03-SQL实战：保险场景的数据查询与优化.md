你好，我是陈博士，今天我们来探讨一下保险续保业务的数据分析与优化。

续保业务是保险公司持续稳定发展的重要组成部分。通过深入的数据查询和分析，我们可以评估客户的续保倾向，识别潜在的流失风险，并为后续的续保策略提供决策支持。

针对该场景，我整理了5张数据表以及对应的查询问题。针对这些查询问题，你可以了解到这些SQL该如何撰写。

## **数据表**

- 客户信息表 customers

<!--THE END-->

![](https://static001.geekbang.org/resource/image/cd/45/cd58929f9e0c9b1cfcd4ca0812c0d245.jpg?wh=1790x1064)

- 保险产品表 insurance\_products

<!--THE END-->

![](https://static001.geekbang.org/resource/image/a2/90/a2449943d03e3c430fbdcc275411a990.jpg?wh=1782x964)

- 保单表 policies

<!--THE END-->

![](https://static001.geekbang.org/resource/image/28/58/28eafe57eef59f8efa1334b018e25958.jpg?wh=1780x1184)

- 续保记录表 renewal\_records

<!--THE END-->

![](https://static001.geekbang.org/resource/image/9b/f6/9b4247e0e84abd1267ff5e85yy908cf6.jpg?wh=1774x960)

- 续保提醒记录表 renewal\_reminders

![](https://static001.geekbang.org/resource/image/74/e4/74f440af660a378e6f15ac1f716a05e4.jpg?wh=1784x964)

## **问题设定**

我从客户分析、产品分析、保单分析、续保分析、异常分析、提醒效果分析、交叉分析等维度设置了一些常见的查询问题。

### **1. 客户分析**

- 查询购买保单数量最多的前10名客户及其保单数量

```plain
SELECT
    c.customer_id,
    c.name,
    c.phone,
    COUNT(p.policy_id) as policy_count
FROM customers c
JOIN policies p ON c.customer_id = p.customer_id
GROUP BY c.customer_id, c.name, c.phone
ORDER BY policy_count DESC
LIMIT 10;
 
// 说明：这里使用JOIN连接客户和保单表，GROUP BY按客户分组并统计保单数量
```