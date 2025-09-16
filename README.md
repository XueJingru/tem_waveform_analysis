# TEM Waveform Analysis

用于瞬变电磁波形生成、分析和可视化的 Python 工具包。

## 功能特点

- 波形生成：创建各种类型的瞬变电磁波形
- 波形分析：计算频谱、主频、带宽和统计数据
- 可视化工具：绘制波形和频谱图表
- SimPEG 集成：与 SimPEG 库集成进行电磁模拟

## 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/tem_waveform_analysis.git
cd tem_waveform_analysis

# 安装依赖
pip install -r requirements.txt
```

## 快速开始

### 基本波形分析

```python
from waveform_generator import WaveformGenerator
from waveform_analyzer import WaveformAnalyzer
from waveform_visualizer import WaveformVisualizer

# 初始化组件
generator = WaveformGenerator()
analyzer = WaveformAnalyzer({"t_max": 0.5, "n_samples": 50000})
visualizer = WaveformVisualizer({"results_dir": "results"})

# 生成和分析波形
# ...详细代码见 examples/basic_example.py
```

### 自定义波形

请参考 `examples/custom_waveform.py` 了解如何创建和分析自定义波形。

### SimPEG 集成

请参考 `examples/simpeg_example.py` 了解如何将此工具包与 SimPEG 库集成。

## 项目结构

```
tem_waveform_analysis/
├── examples/                  # 示例脚本
│   ├── basic_example.py       # 基本用法示例
│   ├── custom_waveform.py     # 自定义波形示例
│   └── simpeg_example.py      # SimPEG 集成示例
├── tests/                     # 单元测试
│   ├── test_analyzer.py
│   ├── test_generator.py
│   └── test_visualizer.py
├── waveform_analyzer.py       # 波形分析模块
├── waveform_generator.py      # 波形生成模块
├── waveform_manager.py        # 波形管理模块
├── waveform_visualizer.py     # 可视化模块
└── main.py                    # 主程序入口
```

## 运行测试

```bash
pytest tests/
```

## 许可证

[MIT](LICENSE)

## 贡献指南

1. Fork 该仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开一个 Pull Request
