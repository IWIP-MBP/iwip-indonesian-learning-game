# IWIP 印尼语学习游戏化平台 (IWIP Indonesian Learning Game)

这是一个专为企业员工设计的印尼语学习与考核游戏化平台。平台融合了 **Duolingo 式趣味通关学习地图**、**Quizizz 式多样化题型** 以及 **企业级 KPI 培训考核分析报表**。界面采用极具质感的 **iOS 磨砂玻璃 (Glassmorphism) 暗黑美学风格**。

---

## � 学习介绍

本平台通过游戏化的方式帮助员工快速掌握印尼语，适用于以下学习场景：

- **🎯 发音基础**：学习印尼语字母、发音规则和基础词汇
- **💬 日常对话**：掌握日常交流、问候、购物、餐饮等实用对话
- **🏢 办公场景**：学习商务会议、邮件沟通、工作汇报等职场用语
- **🛡️ 安全环保**：了解安全生产、环境保护相关的专业术语和规范

通过 21 个精心设计的课程节点，员工可以循序渐进地提升印尼语能力，从零基础到能够进行基本的工作交流。

---

##  核心特性

- **🎮 游戏化通关地图**：21 个课程节点（包含发音基础、日常对话、办公和安全环保场景），支持解锁通关、XP 积分、等级与连击加成。
- **📝 多样化智能题型**：包含词汇选择、中印互译、填空、连线、对话拼图、语音朗读等 8 种游戏题型，内置印尼语标准 TTS 发音朗读及详细中文解析。
- **📚 常用词汇专项学习**：包含 49 个由浅入深排序的词汇专题。针对企业特定场景新增：**宿管管理**、**食堂管理**、**车辆管理**、**物资管理**、**办公室管理**等专项词汇。支持**“对照学习（音形义复习）”**与**“听、读、写三维测试”**双重学习流。
- **📊 学习数据分析 (ECharts)**：多维度能力雷达图（词汇、语法、对话、安全、办公）、活跃度日历热力图、学习趋势曲线以及部门横向对比。
- **🏆 实时竞争排行榜**：包含公司总榜、部门分榜以及个人进度排行榜，激发学习动力。
- **⚙️ 企业级管理后台**：
  - 员工数据的增删改查及 Excel 批量注册导入。
  - 一键导出全体参训员工的 KPI 考核统计报表 (CSV)。
  - **系统端口自定义配置**：支持在后台 UI 界面一键保存并自动生成 Docker 容器映射端口重载指令，适配单域名多系统分时复用。

---

## 🛠️ 项目技术栈

- **前端**：Vue 3 + Vite + Pinia + Bootstrap 5 + ECharts + SheetJS (XLSX)
- **后端**：Flask + SQLAlchemy + JWT 认证
- **异步任务**：Celery + Redis
- **数据库**：MySQL 8.0 / SQLite (支持本地无缝切换)
- **容器化**：Docker & Docker Compose

---

## ⏱️ 快速启动

平台完全容器化，您只需一行命令即可在本地搭建并运行整套系统。

### 前提条件
- 本地已安装 [Docker](https://www.docker.com/) 和 [Docker Compose](https://docs.docker.com/compose/)。

### 启动服务
在项目根目录下执行：
```bash
docker compose -f modules/language_game/docker/docker-compose.yml up --build -d
```

启动完成后，各服务的访问地址如下：
- **Web 前端**：`http://localhost:8080` (可在配置中修改映射端口)
- **后端 API 服务**：`http://localhost:5000`
- **MySQL 数据库**：`localhost:3306`

### 关闭服务
```bash
docker compose -f modules/language_game/docker/docker-compose.yml down
```

---

## 🔑 账户登录说明

打开 `http://localhost:8080` 进入系统登录页：

1. **系统管理员登录**：
   - **工号 (Employee ID)**: `admin`
   - **密码 (Password)**: `123456`
   - 登录后，顶部导航栏会显示 **管理后台** 和 **专项学习** 选项。

2. **参训员工登录**：
   - 使用管理员在后台手动添加或通过 Excel 批量导入的 `工号` 和 `密码` 即可登录。

---

## 📥 批量导入员工数据 (Excel)

管理员登录进入管理后台后，可通过上传 Excel 文件快速导入参训员工：

1. 点击管理后台中的 **"点击选择 Excel 文件进行导入"** 虚线按钮。
2. 上传的 Excel 电子表格中应当包含以下列名表头（大小写/中文均可）：
   - `工号` (或 `id`)
   - `姓名` (或 `name`)
   - `部门` (或 `department`，可选)
   - `密码` (或 `password`，可选，留空则默认密码为 `123456`)
3. 系统将通过前端 SheetJS 自动解析并上传，导入成功后列表将实时刷新。

---

## 📚 常用词汇专项学习指南

专项学习专为碎片化记忆和核心场景词汇突破设计：
1. **章节由浅入深**：按字母、数字等基础专题开始，延伸至日常起居，最后深入到企业宿管、食堂、车辆、物资、办公室等专业行政管理场景。
2. **“学考闭环”流**：
   - **对照学习**：先展示完整的词汇中印对照列表，配有发音喇叭，供学员进行点击收听和对照记忆。
   - **测试挑战**：点击“我已学完，开始挑战”后，可选择 **听力专项测试（听）**、**认读联想测试（读）** 或 **词汇拼写测试（写）**，每组包含 10 道随机测验题。
3. **数据库重新播种 (Seed)**：
   若需重置或在 Docker 容器中重新导入最新生成的 49 专题词汇及 3137 道题库：
   ```bash
   docker compose -f modules/language_game/docker/docker-compose.yml exec backend flask seed-db --force
   ```

---

## ⚙️ 单域名系统分时复用 / 自定义端口配置

如果您在同一台服务器上只有一个域名，但想运行两个系统进行分时段切换复用，可以通过以下方式快速自定义前端的外网映射端口：

### 方法一：在管理后台界面直接配置（推荐）
1. 使用管理员账号登录，并进入右上角的 **“管理后台”**。
2. 在左下角的 **“系统端口配置 (Docker)”** 卡片中，修改“外网访问端口”为你需要的值。
3. 点击 **“保存并重启服务”**。
4. 系统会将新端口写入 `.env` 文件。并在页面中提示需要运行的重启指令，你只需复制并在终端执行即可：
   ```bash
   cd modules/language_game/docker
   docker compose down && docker compose up -d
   ```

### 方法二：直接编辑配置文件
1. 打开项目中的 [modules/language_game/docker/.env](file:///d:/STUDY/modules/language_game/docker/.env) 文件。
2. 修改 `FRONTEND_PORT` 变量（例如 `FRONTEND_PORT=9090`）。
3. 保存后，在 `modules/language_game/docker` 目录下运行容器重新加载命令：
   ```bash
   docker compose down && docker compose up -d
   ```

---

## 📂 项目结构

```text
├── modules/
│   └── language_game/
│       ├── backend/             # Flask 后端服务
│       │   ├── blueprints/      # Auth、Course、Game、Ranking、Report、Admin、SpecialStudy 蓝图
│       │   ├── models.py        # 数据库 ORM 模型
│       │   └── app.py           # 数据库播种与服务初始化
│       ├── database/            # MySQL 数据库初始化 SQL 及 49章节词汇 JSON
│       ├── docker/              # Dockerfile、docker-compose、Nginx 及环境配置文件 .env
│       ├── frontend/            # Vue 3 前端系统
│       │   └── src/             # 组件、视图、路由、Pinia Store
│       └── scripts/             # PDF 自动解析、3100+ 道题库自动生成脚本
```
