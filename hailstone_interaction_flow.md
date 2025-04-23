# Hailstone 项目交互流程说明

本文档使用 PlantUML 描述了 Hailstone 项目中几个核心的用户交互流程和系统内部的数据流向。

## 参与者说明

*   **User**: 最终用户，通过前端界面与系统交互。
*   **Frontend**: 用户界面层，可能是 Web 应用或移动应用，负责展示信息和接收用户输入。
*   **Hailstone API (Django)**: 后端核心服务，处理业务逻辑，与数据库和外部服务交互。
*   **Database (Postgres)**: 数据库，用于持久化存储用户信息、钱包数据、交易记录、活动状态等。
*   **Blockchain Node / External Services**: 区块链节点或其他第三方服务，用于查询链上实时数据（如余额、Nonce、Gas费）、广播交易、获取市场行情等。

## 核心交互场景

下面的 PlantUML 图展示了四个典型的交互场景：

1.  **查看钱包资产**: 用户请求查看其钱包内的代币及余额。系统需要从数据库获取用户钱包信息，并可能需要从区块链节点获取实时余额。
2.  **发送交易**: 用户发起一笔链上交易。系统需要先获取链上最新的 Nonce 和 Gas 费用，待用户签名后，将交易广播出去，并记录交易状态。
3.  **查看市场行情**: 用户请求查看加密货币的市场价格信息。系统可能从数据库缓存或外部行情服务获取数据。
4.  **参与空投活动**: 用户参与平台举办的空投活动，完成指定任务以获取积分或奖励。系统需要记录用户的参与状态和积分。

## PlantUML 时序图

```plantuml
@startuml Hailstone Interaction Flow

!theme plain
' 使用简洁主题

actor User
participant Frontend
participant "Hailstone API (Django)" as API
database "Database (Postgres)" as DB
participant "Blockchain Node / External Services" as Ext

title Hailstone 项目主要交互流程

== 场景1: 用户查看钱包资产 ==
note over User, Ext: 用户发起查看钱包资产请求
User -> Frontend: 请求查看钱包资产
Frontend -> API: GET /api/get_wallet_asset (或其他相关端点)
API -> DB: 查询用户钱包地址和代币列表
DB --> API: 返回钱包信息
API -> Ext: 查询各代币实时余额
Ext --> API: 返回余额信息
API --> Frontend: 返回整合后的资产数据
Frontend -> User: 显示钱包资产

== 场景2: 用户发送交易 ==
note over User, Ext: 用户进行链上交易操作
User -> Frontend: 输入交易信息 (To, Amount)
Frontend -> API: GET /api/get_nonce, /api/get_fee (获取交易前置信息)
API -> Ext: 查询 Nonce, Gas Price
Ext --> API: 返回 Nonce, Gas Price
API --> Frontend: 返回 Nonce, Gas Price
User -> Frontend: (在前端或钱包插件) 签名交易
Frontend -> API: POST /api/send_transaction (提交签名后交易)
API -> Ext: 广播交易
Ext --> API: 返回交易提交结果 (Tx Hash)
API -> DB: 存储交易记录 (Tx Hash, Status)
DB --> API: 确认存储
API --> Frontend: 返回交易已提交及 Tx Hash
Frontend -> User: 显示交易已发送

== 场景3: 用户查看市场行情 ==
note over User, Ext: 用户查询市场数据
User -> Frontend: 请求市场行情数据
Frontend -> API: GET /api/get_exchange_market (或 get_market_detail)
API -> Ext: (可能) 从外部服务获取行情数据
alt 从缓存获取
    API -> DB: 查询行情缓存数据
    DB --> API: 返回缓存数据
else 从外部服务获取
    Ext --> API: 返回实时行情数据
    API -> DB: (可能) 更新行情缓存
end
API --> Frontend: 返回市场行情数据
Frontend -> User: 显示市场行情

== 场景4: 用户参与空投活动 ==
note over User, Ext: 用户参与平台空投活动
User -> Frontend: 进入空投活动页面
Frontend -> API: GET /api/get_project_interactions (或 get_reward_info)
API -> DB: 查询活动详情及用户状态
DB --> API: 返回活动信息
API --> Frontend: 返回活动信息
Frontend -> User: 显示活动任务
User -> Frontend: 完成任务 (如提交邀请码)
Frontend -> API: POST /api/submit_invite_info (或其他交互端点)
API -> DB: 更新用户积分或活动状态
DB --> API: 确认更新
API --> Frontend: 返回操作结果
Frontend -> User: 显示任务完成状态或积分更新

@enduml
``` 