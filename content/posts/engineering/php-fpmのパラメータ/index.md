---
date: 2022-07-06
title: php-fpmのパラメータ設定
---

[PHP-FPM Process Caluculator - Chris Moore](https://spot13.com/pmcalculator/) を用いて計算するのが良い。
vCPU: 1, Memory: 1GBだと以下で設定している：
```
pm=static
pm.max_children=3
pm.max_requests=100
```
