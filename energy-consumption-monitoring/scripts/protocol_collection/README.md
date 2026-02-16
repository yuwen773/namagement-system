# 阶段 1.5：工业协议采集环境准备（Modbus/BACnet）

本目录提供阶段 `1.5` 的可执行验收脚手架，覆盖：

- 采集网关方案与点位映射（`仪表ID -> 设备ID -> 房间`）
- Modbus/BACnet 协议模拟器（无实物设备可验收）
- 采集频率、超时重试、断线重连策略
- 采集字段与 `em_energy_data` 目标字段对齐校验

## 文件说明

- `collection_config.example.json`：采集策略与点位映射配置模板。
- `config.py`：配置解析与校验。
- `simulators.py`：Modbus/BACnet 模拟器服务。
- `adapters.py`：采集适配器（含超时、重试、重连）。
- `collector.py`：统一采集器，输出 JSONL。
- `validate_phase_1_5.py`：一键执行阶段 1.5 验收检查。

## 快速开始

在仓库根目录运行：

```bash
python -m scripts.protocol_collection.validate_phase_1_5
```

预期输出包含 5 个 `PASS`：

1. Modbus 模拟设备可读取且值稳定
2. BACnet 模拟设备可读取且值稳定
3. 断网后可自动重连并恢复采集
4. 采集字段与 `em_energy_data` 对齐
5. 无实物设备场景可完成验收

## 分步调试

1) 启动模拟器：

```bash
python -m scripts.protocol_collection.simulators
```

2) 另一个终端运行采集器：

```bash
python -m scripts.protocol_collection.collector --iterations 3
```

输出文件：

- `scripts/protocol_collection/output/collected_energy_data.jsonl`

## 字段对齐规则（em_energy_data）

采集输出严格使用以下字段顺序：

```text
device, energy_type, timestamp, value, voltage, current, power, flow_rate
```

说明：

- `device`：设备标识（映射自 `仪表ID -> 设备ID`）
- `energy_type`：能源类型（如 `ELECTRICITY`/`WATER`）
- `timestamp`：采集时间（UTC ISO8601）
- `value`：累计读数（必填）
- `voltage/current/power/flow_rate`：按设备类型填充，不适用时为 `null`

