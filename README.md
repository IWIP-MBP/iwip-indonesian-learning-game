# IWIP 印尼语学习游戏化平台 (IWIP Indonesian Learning Game)

这是一个专为企业员工设计的印尼语学习与考核游戏化平台。平台融合了 **Duolingo 式趣味通关学习地图**、**Quizizz 式多样化题型** 以及 **企业级 KPI 培训考核分析报表**。界面采用极具质感的 **iOS 磨砂玻璃 (Glassmorphism) 暗黑美学风格**。

---

## 🚀 核心特性

- **🎮 游戏化通关地图**：21 个课程节点（包含发音基础、日常对话、办公和安全环保场景），支持解锁通关、XP 积分、等级与连击加成。
- **📝 多样化智能题型**：包含词汇选择、中印互译、填空、连线、对话拼图、语音朗读等 8 种游戏题型，内置印尼语标准 TTS 发音朗读及详细中文解析。
- **📊 学习数据分析 (ECharts)**：多维度能力雷达图（词汇、语法、对话、安全、办公）、活跃度日历热力图、学习趋势曲线以及部门横向对比。
- **🏆 实时竞争排行榜**：包含公司总榜、部门分榜以及个人进度排行榜，激发学习动力。
- **⚙️ 企业级管理后台**：
  - 员工数据的增删改查。
  - **支持导入 Excel 表格 (`.xlsx`, `.xls`) 批量注册用户**。
  - 一键导出全体参训员工的 KPI 考核统计报表 (CSV)。

---

## 🛠️ 项目技术栈

- **前端**：Vue 3 + Vite + Pinia + Bootstrap 5 + ECharts + SheetJS (XLSX)
- **后端**：Flask + SQLAlchemy + JWT 认证
- **异步任务**：Celery + Redis
- **数据库**：MySQL 8.0
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
- **Web 前端**：`http://localhost:8080` (原 80 端口已被修改，防止与其他本地项目冲突)
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
   - **密码 (Password)**: `admin123`
   - 登录后，顶部导航栏会显示 **管理后台** 选项，点击可进行员工管理和数据导入。

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

## 📂 项目结构

```text
├── modules/
│   └── language_game/
│       ├── backend/             # Flask 后端服务
│       │   ├── blueprints/      # Auth、Course、Game、Ranking、Report、Admin 蓝图
│       │   ├── models.py        # 数据库 ORM 模型
│       │   └── app.py           # 数据库播种与服务初始化
│       ├── database/            # MySQL 数据库初始化 SQL 脚本
│       ├── docker/              # Dockerfile、docker-compose 及 Nginx 配置
│       ├── frontend/            # Vue 3 前端系统
│       │   └── src/             # 组件、视图、路由、Pinia Store
│       └── scripts/             # PDF 自动解析与 3000+ 题库自动生成脚本
```
