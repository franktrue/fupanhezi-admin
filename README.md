# 复盘盒子 fupanhezi
> 特别说明：股市有风险投资需谨慎，本项目只能用于Python代码学习，股票分析，投资失败亏钱不负责，不算BUG。
## 项目简介
大A 【超短】复盘大数据工具，龙虎榜跟踪，连板梯队查看，个人操作记录，今日同车讨论等功能。

项目地址：[https://github.com/franktrue/fupanhezi](https://github.com/franktrue/fupanhezi "复盘盒子")

fupanhezi基于django-vue-admin的pandas，akshare，pywencai，等框架开发的短线复盘股票系统，仅作数据可视化展示及对比，不提供策略建议等。

目前支持以下功能：
* 行情采集
* 涨停（含炸板）数据采集
* 龙虎榜数据
* 板块维护（概念+行业），含指数日K数据，可自定义板块

## 部署
框架参考：[https://django-vue-admin.com](https://django-vue-admin.com)

目前服务器使用手动部署
部署目录：/mnt/data/wwwroot/fupanhezi/admin/

部署命令
```
cd /mnt/data/wwwroot/fupanhezi/admin/
# 使用对应分支
git pull origin main

# 执行自动部署脚本(会根据docker-compose.yml部署在docker容器上)
./script.sh
```


## 项目展示
以下内容仅为客户端展示，不在本源码范围内

![](/doc/images/题材轮动.jpg)
![](/doc/images/题材轮动-侧边.jpg)
![](/doc/images/连板梯队.jpg)
![](/doc/images/连板梯队-侧边.jpg)
![](/doc/images/热门题材.jpg)
![](/doc/images/分时对比.jpg)

![](/doc/images/复盘梯队.png)

### 体验
微信扫码即可体验
![](/doc/images/qrcode2.png)


