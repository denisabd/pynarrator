```python
import os
from pynarrator import narrate_descriptive, read_data, gpt_get_completions, enhance_narrative, translate_narrative, summarize_narrative
```

```python
df = read_data()
df.head()
```

```python
narrative = narrate_descriptive(df, measure = 'Sales', dimensions = ['Region', 'Product'], return_data = False, coverage = 0.5)
print(narrative)
```

    {'Total Sales': 'Total Sales across all Regions is 38790478.42.', 'Region by Sales': 'Outlying Region by Sales is NA (18079736.4, 47.0%).', 'Product by Sales': 'Outlying Product by Sales is Food & Beverage (15543469.7, 40.0%).'}



```python
narrate_descriptive(df, measure = 'Sales', dimensions = ['Region', 'Product'], return_data = False, coverage = 0.5)
```
    {'Total Sales': 'Total Sales across all Regions is 38790478.42.',
     'Region by Sales': 'Outlying Region by Sales is NA (18079736.4, 47.0%).',
     'Product by Sales': 'Outlying Product by Sales is Food & Beverage (15543469.7, 40.0%).'}


```python
narrate_descriptive(df, measure = 'Sales', dimensions = ['Region', 'Product'], simplify=True, coverage = 0.5)
```
    ['Total Sales across all Regions is 38790478.42.',
     'Outlying Region by Sales is NA (18079736.4, 47.0%).',
     'Outlying Product by Sales is Food & Beverage (15543469.7, 40.0%).']

```python
n = str(narrative)
f'{narrative}'
```

    "{'Total Sales': 'Total Sales across all Regions is 38790478.42.', 'Region by Sales': 'Outlying Region by Sales is NA (18079736.4, 47.0%).', 'Product by Sales': 'Outlying Product by Sales is Food & Beverage (15543469.7, 40.0%).'}"


```python
enhance_narrative(narrative)
```

    "As a knowledgeable business assistant, I would like to present key business insights for your consideration. The Total Sales figure, which represents the aggregate revenue generated across all operational Regions, stands at a noteworthy 38,790,478.42. \n\nFurther, an analysis of sales performance by distinct Regions reveals that the Outlying Region has generated top sales, accounting for 47.0% of the revenue, totaling an impressive 18,079,736.4. \n\nIn addition, a product-centric analysis has also been conducted, which underscores the significant contribution of the Food & Beverage segment towards the company's overall sales figures. This product category has emerged as the Outlying Product by Sales, generating a revenue of 15,543,469.7, which accounts for 40.0% of the total sales. \n\nI hope that this information helps you in making informed business decisions. Please do not hesitate to reach out in case of any further queries."


```python
prompt = "Improve the narrative by adding better business language for 'By Region Sales across all Regions is 2.3 M. Outlying Regions by Sales: West (725,457.9, 31.6 %), East (678,781.2, 29.5 %) West by Segment. In West, Sales across all Segment is equal to 725,457.9. In West, significant Segment by Sales: Consumer (362,880.8, 50.0 %) East by Segment. In East, Sales across all Segment is equal to 678,781.2. In East, significant Segment by Sales: Consumer (350,908.2, 51.7 %). By Segment. Sales across all Segment is 2.3 M. Outlying Segment by Sales: Consumer (1.2 M, 50.6 %)'"

output = gpt_get_completions(prompt)
print(output)
```

    The latest sales figures reveal that the company generated a revenue of 2.3 million through its operations across all regions. Sales across different regions were as follows: West generated the highest revenue of 725,457.9 (31.6%), while in the East, sales worth 678,781.2 (29.5%) were recorded. In the West region, the Consumer segment proved to be the most significant contributor, generating 50.0% of total sales, with revenue amounting to 362,880.8. Similarly, in the East, the Consumer segment dominated, contributing 51.7% of the total sales value of 350,908.2. 
    
    Breaking down the figures by segment, the consumer segment proved to be the most successful for the company, contributing 1.2 million (50.6%) of the total sales. This highlights the importance of investing resources and efforts towards consumer-centric products and services, as they seem to be the primary drivers of revenue growth for the company.


```python
translate_narrative(output, language="Russian")
```

    'Последние данные по продажам показывают, что компания заработала доход в размере 2,3 миллиона через свои операции во всех регионах. Продажи в различных регионах были следующими: Запад сгенерировал наибольший доход в размере 725 457,9 (31,6%), в то время как на Востоке были зафиксированы продажи на сумму 678 781,2 (29,5%). В регионе Запада Сегмент потребителей оказался наиболее значимым вкладчиком, генерируя 50,0% от общих продаж, с общим доходом в размере 362 880,8. Аналогично, на востоке Сегмент потребителей доминировал, внося 51,7% от общей стоимости продажи в размере 350 908,2.\nРазбивая цифры по сегментам, Сегмент потребителей оказался наиболее успешным для компании, внесшим 1,2 миллиона (50,6%) от общей выручки. Это подчеркивает важность вложения ресурсов и усилий в потребительские продукты и услуги, так как они, кажется, являются основными движущими силами роста доходов для компании.'

```python
summarize_narrative(output)
```

    'The company generated 2.3 million in revenue across regions. Consumer sales in the West and East regions were dominant, contributing 50% and 51.7% respectively. The consumer segment drove 50.6% of total sales, showing the importance of investing in consumer-centric products and services.'


