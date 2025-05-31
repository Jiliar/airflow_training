CREATE OR REPLACE VIEW `airflow-training-461420.marketing.ads_insights` AS
SELECT  
  i.date, i.campaign, 'Instagram_ADS' AS platform,
  SUM(i.clicks) AS clicks, SUM(i.views) AS views, SUM(i.sales) AS sales,
  SUM(i.costs) AS costs
FROM `airflow-training-461420.marketing.instagram` i
GROUP BY 1, 2

UNION ALL

SELECT  
  i.date, i.campaign, 'Facebook_ADS' AS platform,
  SUM(i.clicks) AS clicks, SUM(i.views) AS views, SUM(i.sales) AS sales,
  SUM(i.costs) AS costs
FROM `airflow-training-461420.marketing.facebook` i
GROUP BY 1, 2

UNION ALL

SELECT  
  i.date, i.campaign, 'TikTok_ADS' AS platform,
  SUM(i.clicks) AS clicks, SUM(i.views) AS views, SUM(i.sales) AS sales,
  SUM(i.costs) AS costs
FROM `airflow-training-461420.marketing.tiktok` i
GROUP BY 1, 2

UNION ALL

SELECT  
  i.date, i.campaign, 'Youtube_ADS' AS platform,
  SUM(i.clicks) AS clicks, SUM(i.views) AS views, SUM(i.sales) AS sales,
  SUM(i.costs) AS costs
FROM `airflow-training-461420.marketing.youtube` i
GROUP BY 1, 2;