# MASTER PROMPT - 印尼语培训游戏平台（企业版）

## ROLE

你是一名世界级软件架构师、产品经理、教育游戏设计师、全栈工程师。

你的任务是生成一个可直接运行的完整项目。

禁止生成Demo。

禁止生成示例代码。

禁止省略任何文件。

必须生成完整工程。

---

# PROJECT NAME

IWIP Indonesian Learning Game

---

# PROJECT TARGET

将《印尼语培训课程》制作成企业级WEB游戏学习平台，界面效果要像IPHONE一样的磨砂玻璃效果，所有文字必须能看清楚。

用于：

* 中国员工学习印尼语
* 考核印尼语水平
* KPI培训管理
* 生成能力分析报表
* 企业后台统一管理

最终效果：

Duolingo + Quizizz + 企业培训系统

---

# TECH STACK

Frontend

* Vue3
* Vite
* Pinia
* Axios
* Bootstrap5
* ECharts

Backend

* Flask
* SQLAlchemy
* JWT
* Redis
* Celery

Database

* MySQL 8

Deployment

* Docker
* Docker Compose
* Nginx

---

# PROJECT STRUCTURE

modules/

language_game/

backend/

frontend/

database/

docker/

reports/

scripts/

docs/

---

# LOGIN SYSTEM

员工必须输入工号登录

需要有用EXCEL导入员工工号，姓名，部门，登录密码的功能

登录接口：

POST /api/login

返回：

{
"id":"EMP0001",
"name":"张三",
"department":"后勤部"
}

---

# COURSE IMPORT ENGINE

读取教材：

indonesia_course.pdf

自动解析：

章节

单词

例句

对话

语法

自动写入数据库

表：

lessons

vocabulary

dialogues

grammar

sentences

---

# QUESTION GENERATOR

根据教材自动生成题库

总题量：

≥3000题

每课：

≥100题

---

# QUESTION TYPES

## Vocabulary Choice

选择正确中文

## Chinese To Indonesian

中文选择印尼语

## Indonesian To Chinese

印尼语选择中文

## Audio Question

TTS播放单词，增加选择男声和女声的功能，印尼语发音要标准

选择答案

## Picture Question

显示图片，图片必须正确

选择单词

## Fill Blank

补全句子

## Dialogue

对话补全

## Drag Match

拖拽匹配

## Boss Battle

20道随机题

80分通关，所有题目不论做对或做错都得有中文解释。

---

# GAME SYSTEM

XP系统

正确：

+10XP

连击：

Combo Bonus

---

# LEVEL SYSTEM

LV1

LV2

...

LV100

---

# BADGE SYSTEM

首次通关

连续学习7天

连续学习30天

词汇达人

办公达人

安全达人

翻译达人

---

# MAP SYSTEM

课程地图

Lesson 1

↓

Lesson 2

↓

Lesson 3

↓

...

↓

Lesson 21

必须解锁上一关

---

# SCENE MAP

生活场景

* 食堂
* 超市
* 宿舍
* 天气

办公场景

* 办公室
* 会议
* 请假

安全场景

* APD
* SOP
* 安全标识

医疗场景

* 医院
* 生病
* 药品

签证场景

* 休假
* 续签

---

# LEARNING RECORD

记录：

学习次数

学习时长

通过率

正确率

连续学习天数

错题数量

---

# WRONG QUESTION SYSTEM

自动记录：

question_id

wrong_count

last_wrong_time

support:

重新练习

专项练习

---

# RANKING SYSTEM

个人排行榜

部门排行榜

公司排行榜

实时刷新

---

# LANGUAGE LEVEL MODEL

A1

A2

B1

B2

C1

C2

自动计算

---

# REPORT ENGINE

生成：

## 学习趋势图

Line Chart

## 能力雷达图

Radar Chart

维度：

Vocabulary

Grammar

Dialogue

Safety

Work

## 部门平均成绩

Bar Chart

## 排行榜

Bar Chart

## 学习热力图

Heat Map

---

# ADMIN PANEL

管理员：

admin

功能：

员工管理

课程管理

题库管理

成绩管理

排行榜管理

勋章管理

导出Excel

导出PDF

---

# DATABASE TABLES

employees

departments

lessons

vocabulary

dialogues

grammar

questions

question_options

learning_records

wrong_questions

badges

employee_badges

rankings

language_reports

game_levels

game_rewards

system_logs

---

# API DOCUMENT

生成完整Swagger

包含：

Auth API

Course API

Question API

Game API

Ranking API

Report API

Admin API

---

# DOCKER

生成：

docker-compose.yml

services:

frontend

backend

mysql

redis

nginx

支持：

docker compose up -d

直接运行

---

# OUTPUT REQUIREMENT

必须输出：

1. 完整目录结构

2. 全部源码

3. SQL脚本

4. Docker配置

5. Swagger文档

6. Vue页面

7. Flask接口

8. 自动导题脚本

9. 自动出题脚本

10. 自动报表脚本

禁止输出伪代码。

禁止省略文件。
所有功能必须采用 Blueprint 模块化设计，可直接挂载到现有 Flask 项目，避免修改主程序，仅通过 app.register_blueprint(language_game_bp) 即可完成集成。这样后续维护和升级不会影响现有员工管理系统。
所有代码必须可运行。

最终生成完整企业级项目。
