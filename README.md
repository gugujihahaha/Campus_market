<!--
────────────────────────────────────────────────────────────
  校园二手交易平台 · Campus Market
  Django 5.2 + Tailwind CSS · 2026
────────────────────────────────────────────────────────────
-->

<h1 align="center">
  🎓 校园二手交易平台 <br>
  <sub><code>Campus Market</code></sub>
</h1>

<p align="center">
  <i>让闲置流动起来 —— 安全、便捷的校园 C2C 交易空间</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white&style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white&style=for-the-badge" alt="Django">
  <img src="https://img.shields.io/badge/Tailwind_CSS-v3-06B6D4?logo=tailwindcss&logoColor=white&style=for-the-badge" alt="Tailwind CSS">
  <img src="https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white&style=for-the-badge" alt="SQLite">
  <img src="https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white&style=for-the-badge" alt="HTML5">
</p>

---

## 📖 项目简介

校园二手交易平台是一个专为高校学生打造的 **C2C 闲置物品交易系统**。学生可以在平台上：

- 📸 **发布商品** — 上传照片、填写描述，一键上架闲置
- 🔍 **浏览 / 搜索** — 逛遍全校好物，按分类、关键词精准筛选
- 💬 **留言互动** — 在商品下留言，与卖家沟通细节
- 👤 **个人主页** — 管理自己的商品、查看交易历史

项目采用 **Django MTV 架构** + **Tailwind CSS** 构建，注重代码健壮性（权限校验、异常处理）与 UI 审美（毛玻璃卡片、微交互动画），设计风格参考闲鱼 App 网页版。

---

## 🧰 核心技术栈

| 层级 | 技术 | 说明 |
|:---|:---|:---|
| 🔙 后端框架 | **Django 5.2** | ORM、模板引擎、表单验证、用户认证 |
| 🎨 前端样式 | **Tailwind CSS (CDN)** | 原子化 CSS，拒绝手写样式表 |
| 🗄️ 数据库 | **SQLite** | 轻量、零配置；后期可平滑迁移至 MySQL / PostgreSQL |
| 📝 模板 | **Django Template Language** | 配合 Tailwind 实现组件化页面 |
| 🧩 图标 | **Emoji + Heroicons** | 轻量图标方案，无需额外字体库 |

---

## ✨ 功能清单 / Features

### 🔐 用户系统
- [x] 注册（用户名 + 密码，注册即自动登录）
- [x] 登录 / 注销
- [x] 注册时自动创建 UserProfile（头像、联系方式、宿舍区）
- [ ] 个人中心（头像上传、资料修改）
- [ ] 修改密码

### 📦 商品模块
- [x] 商品发布（标题、价格、描述、图片、分类）
- [x] 商品列表页（公开浏览）
- [x] 商品详情页
- [x] 我的商品管理（仅本人可见，支持下架/重新上架/删除 + 统计面板）
- [x] 商品状态机：在售 ⇄ 交易中 ⇄ 已售出 / 已下架（支持下架/重新上架操作）
- [x] 浏览量统计
- [x] 精美瀑布流首页（毛玻璃导航 + Hero 渐变横幅 + 响应式卡片网格 + 悬浮动画）
- [x] 鉴权页面美化（Indigo/Emerald 品牌色 + 全屏渐变背景 + 毛玻璃卡片 + 错误提示优化）
- [x] 用户主页重构（个人信息卡片 + 统计面板 + 商品管理操作区 + 下架/上架/删除）
- [ ] 多图上传（每个商品 N 张图）
- [x] 分类筛选（胶囊按钮横向滚动，支持按分类过滤）
- [x] 关键词搜索（标题/描述模糊匹配，搜索框 + 分类联动保留）
- [ ] 商品编辑

### 💬 留言互动
- [x] Comment 数据模型（用户 ↔ 商品 多对一）
- [ ] 商品详情页留言区
- [ ] 留言删除（本人 / 商品主）

### 🛠️ Django Admin 后台
- [x] @admin.register 装饰器注册全部模型
- [x] 彩色状态圆角标签（在售=绿、交易中=黄、已售出=灰、已下架=红）
- [x] 价格红色 ¥ 格式化、头像圆形预览
- [x] list_filter / search_fields / date_hierarchy 完整配置
- [ ] 导出 CSV
- [ ] 数据看板（Dashboard 概览）

### 🧱 数据模型
- [x] `Category` — 商品分类（图标 + 名称）
- [x] `Goods` — 商品（标题、价格、描述、图片、状态、浏览量、分类 FK；`increment_view()` 防竞态）
- [x] `UserProfile` — 用户资料（头像、联系方式、宿舍区；User ↔ UserProfile 信号自动创建）
- [x] `Comment` — 商品留言

---

## 🚀 快速开始

### 环境要求

- Python 3.12+
- Git（可选）

### 本地运行

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd Campus_market

# 2. 创建虚拟环境（推荐）
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. 安装依赖
pip install django

# 4. 数据库迁移
python manage.py makemigrations goods
python manage.py migrate

# 5. 创建超级管理员（用于访问 Admin 后台）
python manage.py createsuperuser

# 6. 启动开发服务器
python manage.py runserver
```

### 访问地址

| 地址 | 说明 |
|:---|:---|
| http://localhost:8000/goods/ | 商品列表（首页） |
| http://localhost:8000/goods/register/ | 用户注册 |
| http://localhost:8000/goods/login/ | 用户登录 |
| http://localhost:8000/goods/add/ | 发布商品 |
| http://localhost:8000/goods/my/ | 我的商品 |
| http://localhost:8000/admin/ | Django 管理后台 |

---

## 📁 目录结构

```
Campus_market/
├── campus_market/              # Django 项目配置
│   ├── settings.py             # 全局配置（DEBUG、数据库、静态文件等）
│   ├── urls.py                 # 根路由
│   └── wsgi.py                 # WSGI 入口
│
├── goods/                      # 商品应用（核心业务）
│   ├── models.py               # 数据模型：Category, Goods, UserProfile, Comment
│   ├── admin.py                # 管理后台注册与美化
│   ├── urls.py                 # 应用路由
│   ├── apps.py                 # 应用配置
│   ├── views/                  # 视图层（按模块拆分）
│   │   ├── goods_views.py      #   商品 CRUD 视图
│   │   └── user_views.py       #   登录 / 注册视图
│   ├── services/               # 业务逻辑层
│   │   └── goods_service.py    #   商品删除等服务
│   ├── forms/                  # 表单层
│   │   └── goods_form.py       #   商品表单
│   └── templates/              # 模板层
│       ├── base.html           #   基础布局（Tailwind CDN 引入）
│       ├── goods_list.html     #   商品列表页
│       ├── goods_detail.html   #   商品详情页
│       ├── add_goods.html      #   发布商品页
│       ├── my_goods.html       #   我的商品页
│       ├── login.html          #   登录页
│       └── register.html       #   注册页
│
├── media/                      # 用户上传文件
│   ├── goods/                  #   商品图片
│   └── avatars/                #   用户头像
│
├── db.sqlite3                  # SQLite 数据库（开发）
├── manage.py                   # Django 命令行入口
├── .gitignore
└── README.md
```

---

## 📅 更新日志 / Changelog

### 🗓️ 2026-05-31 — 业务闭环：鉴权页面美化、搜索过滤 & 个人主页重构

> **Tag:** `v0.4.0-dashboard`

**鉴权页面 UI 现代化（login.html / register.html）：**
- ✅ 登录页采用 Indigo 品牌色系，全屏渐变背景 + 4 个装饰性模糊几何图形
- ✅ 注册页采用 Emerald 品牌色系，同款渐变背景布局
- ✅ 表单卡片：毛玻璃效果（`backdrop-blur-2xl`）+ `shadow-2xl` + 白色半透明环
- ✅ 输入框：`focus:ring-2` 品牌色聚焦效果 + 左侧图标
- ✅ 按钮：渐变色（Indigo/Emerald）+ `active:scale-[0.98]` 按压反馈
- ✅ 错误提示：红色 Alert 框包含图标 + 标题 + 消息，结构清晰
- ✅ 底部互跳链接保持品牌色一致

**个人主页重构（my_goods.html）：**
- ✅ 个人信息卡片：渐变色装饰条 + 头像/昵称/宿舍区/联系方式
- ✅ 四格统计面板：全部 / 在售 / 交易中 / 已售出，彩色背景区分
- ✅ 发布新商品按钮使用 Indigo→Purple 渐变色
- ✅ 商品卡片网格：响应式 `grid-cols-2` ~ `xl:grid-cols-5`
- ✅ 每张卡片：图片 + 状态角标 + 价格 + 浏览量 + 操作按钮组（查看/下架/删除）
- ✅ 已下架商品显示绿色「重新上架」按钮替代下架
- ✅ 空状态友好引导文案

**搜索 & 分类过滤激活：**
- ✅ 首页新增搜索输入框（搜索图标 + 清除按钮 + 搜索按钮）
- ✅ `goods_list` 视图 `?q=` 参数对标题/描述进行 `__icontains` 模糊匹配
- ✅ `?category=` 分类筛选与搜索关键词双向联动（切换分类保留搜索词，反之亦然）
- ✅ 标题行动态显示当前搜索/筛选上下文
- ✅ 分类胶囊按钮横向滚动 + 选中态黑白高亮

**后端新增：**
- ✅ `off_shelf_goods` 视图 — 下架商品（仅本人，状态改为已下架）
- ✅ `relist_goods` 视图 — 重新上架（仅本人，已下架→在售）
- ✅ `my_goods` 视图增加统计上下文（on_sale_count / sold_count / in_trade_count / off_shelf_count）
- ✅ URL 路由注册 off_shelf 和 relist 端点

### 🗓️ 2026-05-31 — 商品详情页 & 发布表单 UI 重构

> **Tag:** `v0.3.0-details`

**商品详情页（goods_detail.html）全面重写：**
- ✅ 左右分栏布局（`grid md:grid-cols-2 gap-8`），左侧大图 + 右侧信息
- ✅ 图片区：`rounded-3xl` + `shadow-lg` + `aspect-square object-cover`，无图时渐变占位符
- ✅ 价格：超大号玫瑰红（`text-4xl lg:text-5xl font-extrabold text-rose-600`）
- ✅ 状态标签带脉冲动画（在售绿点）、浏览量 / 发布时间
- ✅ 卖家信息卡片：渐变头像、用户名、宿舍区（地图图标）、联系方式
- ✅ 渐变色「联系卖家」按钮 → 毛玻璃弹窗展示联系方式
- ✅ 未登录引导登录；本人商品显示「这是你的商品」
- ✅ 面包屑导航（首页 > 分类 > 商品名）

**发布表单（add_goods.html）完全重写：**
- ✅ 居中白色圆角卡片布局（`rounded-3xl shadow-sm`）
- ✅ 所有输入框 Tailwind 定制：灰色底 + 聚焦 `ring-2 ring-emerald-400`
- ✅ 图片上传区：虚线边框拖拽视觉（`border-dashed` + 上传图标）
- ✅ 分类下拉选择器（自定义箭头图标）
- ✅ 红色错误提示文本（图标 + 消息，逐字段显示）
- ✅ 渐变色提交按钮「确认发布商品」

**后端增强：**
- ✅ `goods_detail` 视图：访问时自动 `increment_view()`（F 表达式防竞态）
- ✅ `add_goods` 视图：传入 `categories` 供表单下拉使用
- ✅ `GoodsForm`：新增 `category` 字段、`clean_title`（≥2 字符）、`clean_price`（范围校验）
- ✅ `get_object_or_404` 替代 `.get()` 避免 500

### 🗓️ 2026-05-31 — 全局 UI 重塑 & 交互升级

> **Tag:** `v0.2.0-ui`

**首页与导航全面升级：**
- ✅ 导航栏改为吸顶毛玻璃效果（`backdrop-blur-xl` + `backdrop-saturate-150`）
- ✅ 已登录用户头像下拉菜单（Alpine.js 交互）：我的商品、发布商品、退出登录
- ✅ 未登录用户精美登录/注册按钮组
- ✅ Hero Section 渐变色横幅（emerald → teal → cyan），标语「让闲置物品在校园里重新发光」
- ✅ 横向滚动分类胶囊筛选按钮，选中态黑白高亮
- ✅ 商品卡片响应式网格 `grid-cols-2` ~ `xl:grid-cols-5`
- ✅ 卡片悬浮上移 + 阴影加深动画（`hover:-translate-y-1.5 hover:shadow-xl`）
- ✅ 图片悬浮放大（`hover:scale-110`）、状态角标（在售=绿、交易中=黄、已售出=灰）
- ✅ 空状态友好引导（引导发布第一条商品）
- ✅ 新增退出登录功能 + URL 命名路由

**后端更新：**
- ✅ `goods_list` 视图支持 `?category=` 参数筛选
- ✅ 首页仅显示在售/交易中商品，已售出/已下架不公开

### 🗓️ 2026-05-31 — 项目初始化 & 数据模型重构

> **Tag:** `v0.1.0-init`

**数据库模型全面升级：**
- ✅ 新增 `Category` 模型 — 商品分类（名称 + 图标），支持 `goods_count` 统计
- ✅ 扩展 `Goods` 模型 — 增加 `status` 状态字段（0 在售 / 1 交易中 / 2 已售出 / 3 已下架）
- ✅ 增加 `view_count` 浏览量字段，`increment_view()` 使用 `F()` 表达式防止竞态条件
- ✅ 增加 `category` 外键关联
- ✅ 新增 `UserProfile` 模型 — User 一对一扩展（头像、联系方式、宿舍区）
- ✅ 新增 `Comment` 模型 — 商品留言（用户 ↔ 商品）

**信号机制：**
- ✅ 使用 `@receiver(post_save, sender=User)` 实现注册时自动创建 UserProfile

**Django Admin 后台美化：**
- ✅ `@admin.register` 装饰器注册全部模型
- ✅ 彩色状态圆角标签（Tailwind 风格配色）
- ✅ 价格红色 ¥ 格式化、头像圆形预览
- ✅ `list_filter` / `search_fields` / `date_hierarchy` 完整配置

**已有功能（来自基础框架）：**
- ✅ 用户注册 / 登录
- ✅ 商品发布（含图片上传）
- ✅ 商品列表页
- ✅ 商品详情页
- ✅ 我的商品管理（含删除）

**已完成的后续迭代：**
- ✅ 首页 UI 重塑（毛玻璃导航 + Hero 横幅 + 分类筛选 + 卡片动画） → 见 v0.2.0-ui
- ✅ 商品详情页 & 发布表单重构（联系卖家弹窗、虚线拖拽上传） → 见 v0.3.0-details

---

<p align="center">
  <sub>Built with ❤️ using Django & Tailwind CSS · Campus Market © 2026</sub>
</p>
