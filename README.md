# hot-seahorse








一个api 积分系统的售卖小程序
现在需要设计一下这个小程序的注册、登录页面
用户可以使用微信登录注册

​一、核心流程调整
​注册/登录

​仅微信授权登录：用户通过微信一键授权，获取OpenID和昵称/头像，自动创建账户。
​无任何绑定引导：登录后直接进入首页，不弹窗、不提示绑定手机/邮箱。
​绑定入口设计

​位置：仅在「个人中心」页面底部设置「绑定手机号」和「绑定邮箱」按钮。
绑定功能会暂时置灰

注册登录这块就这样了



​小程序底部导航菜单设计（推荐4个主入口）​
​一、导航标签与功能分配
markdown
1. ​**首页（图标：🏠）​**  
   - 核心入口：展示积分余额、快捷购买入口、API服务状态  
   - 禁止关闭或隐藏（始终保留）

2. ​**购买积分（图标：💰）​**  
   - 独立标签页，强化付费转化  
   - 包含套餐列表、支付记录、活动横幅（如首充优惠）

3. ​**API Key（图标：🔑）​**  
   - 管理所有API Key的专属页面  
   - 功能：生成/删除Key、查看调用统计、设置权限规则

4. ​**个人中心（图标：👤）​**  
   - 次级功能聚合入口：  
     - 账户信息（昵称/绑定状态）  
     - ​**积分消耗记录**​（隐藏较深路径）  
     - 系统设置（通知开关、关于我们）



首页
1. ​**顶部状态栏**  
   - 显示用户昵称（取自微信） + 当前积分余额（突出显示）  
   - 右侧「刷新」按钮（手动同步积分实时数据）  

2. ​**核心功能入口**​（卡片式布局，不超过3个）  
   - ​**购买积分**：按钮颜色高亮（如橙色），显示推荐档位（如「50元=600积分，最热销」）  
   - ​**API Key管理**：显示当前有效Key数量（如「2个Key使用中」）  
   - ​**文档中心**：快捷入口（文案：查看接口文档）  

3. ​**API服务状态**  
   - 公告栏样式，默认折叠，异常时展开红字提示（如「图片识别接口临时维护中」）  

4. ​**快速操作区**​（悬浮底栏，常驻显示）  
   - 「生成Key」 + 「购买积分」按钮（优先用户高频操作）




购买积分（图标：💰）页面
1. ​**当前账户状态栏（吸顶）​**  
   - 显示「可用积分：1,200」 +「有效期至：2024/12/31」  
   - 右侧「购买记录」文字链（跳转订单列表页）

2. ​**推荐套餐（黄金位置）​**  
   - 主推1-3个高性价比套餐（如「600积分=50元，节省20%」）  
   - 设计差异：  
     ✅ 放大卡片尺寸  
     ✅ 添加「热销」角标  
     ✅ 按钮文案为「立即充值」（强化行动暗示）
        - 交互规则：  
     - 点击套餐卡直接选中（无需二次确认）  
     - 当前选中套餐高亮蓝色边框

3. ​**全部套餐列表**  
   - 分档设计：  
     - 小档（10元档）：100积分  
     - 中档（50元档）：600积分（默认展开）  
     - 大额（300元档）：4000积分 + 赠200积分  
   - 交互规则：  
     - 点击套餐卡直接选中（无需二次确认）  
     - 当前选中套餐高亮蓝色边框


点击套餐后的支付流程设计
​一、流程步骤
​点击套餐 → ​进入订单确认页​（非直接弹出支付码）
​确认页信息展示 → ​用户主动点击支付 → ​调起微信支付弹窗
​二、详细交互说明
markdown
1. ​**订单确认页内容**  
   - 顶部显示：「确认订单」 + 关闭按钮  
   - 核心信息：  
     ✅ 套餐详情（50元=600积分）  
     ✅ 有效期提示（如「积分有效期至2025年1月1日」）  
     ✅ 支付方式选择（默认微信支付，不可更改）  
   - 法律声明：  
     「虚拟商品不支持退款，请确认套餐内容」  

2. ​**支付触发规则**  
   - 点击「立即支付」按钮 → 调用微信支付API  
   - 支付弹窗显示金额（50元） + 商品描述（「API积分充值」）  

3. ​**防误触机制**  
   - 点击套餐后，按钮保持禁用状态1秒（防止快速重复点击）  
   - 支付弹窗需用户主动点击「确认支付」才会调起


一、核心跳转路径
markdown
1. ​**支付成功** → ​**支付成功页**​（停留5秒，含自动跳转）  
2. ​**支付失败** → ​**失败提示页**​（手动操作）  
3. ​**支付中/未知状态** → ​**订单状态轮询页**
​二、详细页面设计
​1. 支付成功页
markdown
- ​**核心信息展示**：  
  ✅ 大号绿色对勾图标 + 「支付成功」标题  
  ✅ 充值金额（¥50）→ 获得积分（600积分）  
  ✅ 积分有效期提醒（「有效期至2025年1月1日」）  
  ✅ 按钮：  
    - 「查看积分余额」（跳转首页）  
    - 「生成API Key」（跳转Key管理页）  

- ​**自动跳转规则**：  
  倒计时5秒后自动返回首页，显示「即将返回首页（3...2...1）」  

- ​**法律声明**：  
  底部小字：「积分为虚拟商品，不支持提现或退款」
https://via.placeholder.com/300x500/EEE/AAA?text=Payment+Success+Page

​2. 支付失败页
markdown
- ​**核心信息展示**：  
  ✅ 红色感叹号图标 + 「支付失败」标题  
  ✅ 失败原因（如「余额不足」「网络超时」）  
  ✅ 按钮：  
    - 「重新支付」（返回订单确认页）  
    - 「联系客服」（跳转在线客服）  

- ​**设计原则**：  
  避免自动跳转，让用户主动选择下一步




点击api key
1. ​**API Key列表（核心区域）​**  
   - 展示所有已生成的Key（默认按最近使用排序）  
   - 单条Key卡片显示信息：  
     ✅ Key名称（可编辑，默认「我的第一个Key」）  
     ✅ 状态标签（活跃/已禁用/积分耗尽）  
     ✅ 剩余积分 + 今日调用次数  
     ✅ 最近调用时间（如「5分钟前」或「从未使用」）  

2. ​**操作入口（顶部功能区）​**  
   - 「生成新Key」按钮（高亮显示，触发生成弹窗）  
   - 筛选器（按状态/名称搜索）  
   - 批量操作（选择多个Key后显示「批量禁用」「批量删除」）


​生成新Key流程

markdown
1. 点击「生成新Key」→ 弹窗填写信息：  
   - Key名称（必填，20字符内）  
   - 权限范围（默认「全部接口」，可改为指定接口）  
   - IP白名单（选填，支持CIDR格式）  
2. 点击确认 → 显示蒙层加载动画 → 生成成功页  
3. 成功页内容：  
   - 新Key明文显示（仅此一次可见）  
   - 「复制Key」按钮 + 「我已保存」确认勾选  
   - 警告提示：「Key一旦关闭将无法再次查看」



【个人中心】页详细设计
​一、核心模块布局
markdown
1. ​**账户信息头图**  
   - 微信头像 + 昵称（居中显示）  
   - 绑定状态提示（如「已绑定手机」「未绑定邮箱」）  
   - 「编辑资料」按钮（仅支持修改昵称，微信头像需重新授权）  

2. ​**功能入口列表（卡片式）​**  
   - ​**积分消耗记录**：显示最近3条扣费记录（时间+接口+消耗量）  
   - ​**API调用日志**：最近一次调用状态（成功/失败）+ 时间  
   - ​**发票管理**：入口按钮（显示待开票数量，如「2张待申请」）  

3. ​**系统设置区**  
   - 通知开关（默认开启支付成功提醒）  
   - 「关于我们」 + 「用户协议」链接  
   - 退出登录按钮（底部固定，红色文字警示）  

4. ​**扩展入口（折叠区）​**  
   - 「联系客服」 + 「常见问题」  
   - 「开发者合作」 + 「API服务状态」  





【个人中心】页详细设计
​一、核心模块布局
markdown
1. ​**账户信息头图**  
   - 微信头像 + 昵称（居中显示）  
   - 绑定状态提示（如「已绑定手机」「未绑定邮箱」）  暂时不可用只展示 未绑定就可以

2. ​**系统设置区**  
   - 「关于我们」 + 「用户协议」链接  
   - 退出登录按钮（底部固定，红色文字警示）  


   开发期间可以先使用mock接口实现



商品表
活动表
商品活动包
订单表
用户购买记录表




---------------- 元数据表：商品表 -----------------
CREATE TABLE meta_product (
    id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    product_type SMALLINT NOT NULL CHECK (product_type IN (1,2)), -- 1-积分 2-套餐
    point_amount INT NOT NULL,
    original_price NUMERIC(10,2) NOT NULL,
    sale_price NUMERIC(10,2) NOT NULL,
    currency VARCHAR(3) NOT NULL CHECK (currency IN ('CNY','USD')),
    expire_time TIMESTAMPTZ NOT NULL DEFAULT '2099-12-31 23:59:59+08',
    status SMALLINT NOT NULL DEFAULT 1, -- 0-下架 1-上架
    sort SMALLINT,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE meta_product IS '商品基础信息表';
COMMENT ON COLUMN meta_product.product_type IS '商品类型：1-积分 2-套餐';

---------------- 元数据表：营销活动表 -----------------
CREATE TABLE meta_promotion (
    id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    promo_type SMALLINT NOT NULL CHECK (promo_type IN (1,2)), -- 1-折扣 2-满减
    discount_rate NUMERIC(5,2),
    min_amount NUMERIC(10,2),
    bonus_points INT,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    applicable_products JSONB,
    status SMALLINT NOT NULL, -- 0-未激活 1-进行中 2-已结束
    memo TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

---------------- 关系表：商品活动包 -----------------
CREATE TABLE rel_product_package (
    id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    product_id UUID NOT NULL REFERENCES meta_product(id),
    promotion_id UUID REFERENCES meta_promotion(id),
    package_price NUMERIC(10,2) NOT NULL CHECK (package_price > 0),
    total_points INT NOT NULL CHECK (total_points > 0),
    is_hot BOOLEAN NOT NULL DEFAULT false,
    sort SMALLINT NOT NULL DEFAULT 0,
    expire_time TIMESTAMPTZ NOT NULL DEFAULT '2099-12-31 23:59:59+08',
    status SMALLINT NOT NULL, -- 0-下架 1-上架
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_package_hot ON rel_product_package(is_hot, status);

---------------- 元数据表：订单表 -----------------
CREATE TABLE meta_order (
    id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    order_no VARCHAR(32) NOT NULL UNIQUE,
    -- 用户信息
    user_id UUID NOT NULL REFERENCES meta_user(id),
    user_name VARCHAR(100), -- 冗余用户名
    -- 商品信息
    product_id UUID NOT NULL REFERENCES meta_product(id),
    package_id UUID REFERENCES rel_product_package(id),
    promotion_id UUID REFERENCES meta_promotion(id),
    -- 支付信息
    total_amount NUMERIC(10,2) NOT NULL CHECK (total_amount >= 0),
    payment_status SMALLINT NOT NULL DEFAULT 0, -- 0-待支付 1-已支付 2-已关闭 3-已退款
    wx_appid VARCHAR(32),
    wx_mchid VARCHAR(32),
    wx_transaction_id VARCHAR(64),
    wx_payer_openid VARCHAR(128),
    -- 时间信息
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    paid_at TIMESTAMPTZ
);

COMMENT ON TABLE meta_order IS '订单主表';
COMMENT ON COLUMN meta_order.payment_status IS '支付状态：0-待支付 1-已支付 2-已关闭 3-已退款';

---------------- 购买记录表 -----------------
CREATE TABLE purchase_record (
    id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES meta_user(id),
    order_id UUID NOT NULL REFERENCES meta_order(id),
    -- API调用追踪
    api_key_id UUID NOT NULL REFERENCES meta_auth_key(id),
    api_name VARCHAR(100),
    api_path VARCHAR(255),
    -- 积分明细
        {"column_name": "points_change", "data_type": "integer", "is_nullable": "NO", "desc": "积分变动值"},
    {"column_name": "remaining_points", "data_type": "integer", "is_nullable": "NO", "desc": "剩余积分"},
    {"column_name": "operation_type", "data_type": "smallint", "is_nullable": "NO", "desc": "操作类型(1-购买 2-消费 )"},
    {"column_name": "memo", "data_type": "text", "is_nullable": "YES"},

    expire_time TIMESTAMPTZ NOT NULL DEFAULT '2099-12-31 23:59:59+08',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE meta_user 
ADD COLUMN total_points INT NOT NULL DEFAULT 0,







API Key 接口功能描述文档
1. 获取 API Key 列表 
接口职责

查询并返回当前用户所有的 API Key
提供每个 API Key 的详细信息和当前状态
帮助用户管理和追踪其 API Key

具体实现

如果是微信请求
还需要根据用户 token 识别当前用户
查询数据库中该用户的所有 API Key
组装 API Key 列表，包括：

唯一标识符
名称
状态（激活/禁用）
创建时间
过期时间
最后使用时间



2. 创建 API Key 
接口职责

为用户生成新的 API Key
提供 API Key 管理和访问能力
支持用户根据需求设置 API Key 的有效期

具体实现

如果是微信用户请求，则需要验证用户身份
生成唯一的 API Key
记录 API Key 相关信息：

随机生成安全的 API Key
设置过期时间（1/3/6/12个月）
初始状态为激活
关联当前用户


将 API Key 信息存储到数据库
仅在创建时返回完整的 API Key

记录日志，便于追踪和安全审计


3. 删除 API Key /api/v1/api-keys/delete
接口职责

允许用户删除不再需要的 API Key
及时清理无用的访问凭证
保护系统安全性

具体实现

如果是微信用户，则需要验证微信用户身份和权限
验证用户身份和权限
检查要删除的 API Key 是否属于当前用户
执行删除操作：

从数据库中移除 API Key 记录
使相关的访问凭证失效


记录删除日志，便于追踪和安全审计

4. 更新 API Key 状态
接口职责

提供临时启用/禁用 API Key 的能力
增强 API Key 管理的灵活性
支持安全控制

具体实现

如果是微信用户，则需要验证微信用户身份和权限

验证用户身份和权限
检查要更新状态的 API Key 是否属于当前用户
执行状态更新：

将 API Key 状态切换为激活或禁用
立即生效，影响 API 访问权限


记录状态变更日志

安全考虑

所有操作如果是微信的用户，基于用户 token 鉴权
API Key 生成使用安全的随机算法
仅在创建时展示完整 API Key
支持灵活的 API Key 生命周期管理
提供状态控制机制，防止未授权访问






用户关注公众号，微信调用api 发来请求，
   服务端判断当前用户在 meta_user表 是否存在，
      存在则更新用户信息，返回用户信息给微信端。
   不存在则创建用户，返回用户信息给微信端。
