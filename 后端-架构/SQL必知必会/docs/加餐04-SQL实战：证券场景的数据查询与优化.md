你好，我是陈博士。今天我们来探讨一下客户持仓配置建议业务的SQL分析。

合理的资产配置，是确保客户投资组合既能满足其财务目标，又能有效管理风险的关键。通过深入的数据查询和分析，我们可以评估客户的当前资产状况、风险承受能力以及投资偏好，从而提供个性化的资产配置建议。

针对该场景，我整理了2张数据表以及对应的查询问题。针对这些查询问题，你可以了解到这些SQL该如何撰写。

## **数据表**

- 客户持仓表 customer\_positions

<!--THE END-->

![](https://static001.geekbang.org/resource/image/6c/8e/6c2c38a25ca4afbd6621579aaf82278e.jpg?wh=1792x1408)

- 产品配置表 product\_configuration

![](https://static001.geekbang.org/resource/image/e4/f5/e4a7269781ec0d2ee0d71420c06701f5.jpg?wh=1792x804)

## **问题设定**

我从客户资产分析、资产配置分析、风险等级分析、产品持仓排名等维度设置了一些常见的查询问题，一起来看一下。

### **1. 客户资产分析**

查询指定客户（customer\_id = ‘C00001’）在特定日期（2024-12-21）的各类资产（股票、基金、固收、结构性产品、现金）具体金额是多少？总资产是多少？

```plain
SELECT
    customer_id,
    customer_name,
    SUM(stock_amount) as total_stock,
    SUM(fund_amount) as total_fund,
    SUM(fixed_income_amount) as total_fixed_income,
    SUM(structured_amount) as total_structured,
    SUM(cash_amount) as total_cash,
    SUM(stock_amount + fund_amount + fixed_income_amount + structured_amount + cash_amount) as total_assets
FROM customer_positions FORCE INDEX (idx_customer_id)
WHERE customer_id = 'C00001'
AND position_date = '2024-12-21'
GROUP BY customer_id, customer_name;
 
// 说明： 使用 SUM() 聚合函数计算各类资产总金额，并通过 GROUP BY 按客户分组。FORCE INDEX 提示优化查询性能，确保快速定位指定客户和日期的数据。
```