"""基本用法示例."""

import os
import sys

import numpy as np

from waveform_analyzer import WaveformAnalyzer
from waveform_generator import WaveformGenerator
from waveform_visualizer import WaveformVisualizer

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 创建结果目录
results_dir = "basic_example_results"
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# 初始化各个组件
generator = WaveformGenerator()
analyzer = WaveformAnalyzer({"t_max": 0.5, "n_samples": 50000})
visualizer = WaveformVisualizer({"results_dir": results_dir})

# 设置波形参数
width = 5e-3  # 5ms
t_display = np.linspace(0, width * 3, 10000)  # 显示3倍波宽
t_full = np.linspace(
    0, analyzer.config["t_max"], analyzer.config["n_samples"]
)  # 用于频谱分析的完整时间序列

# 生成微分脉冲波
differential = generator.differential_pulse(t_display, width)
differential_full = generator.differential_pulse(t_full, width)

# 分析波形
spectrum = analyzer.compute_spectrum(differential_full)
dominant_freq = analyzer.find_dominant_frequency(differential_full)
bandwidth = analyzer.compute_bandwidth(differential_full)
stats = analyzer.compute_statistics(differential_full)

# 可视化波形和频谱
visualizer.plot_waveform_and_spectrum(
    t_display,
    differential,
    analyzer.freq_positive,
    spectrum[1 : len(analyzer.freq_positive) + 1],
    width,
    f"Half-Sine Wave (Width: {width*1e3:.1f}ms)",
    "differential_analysis.png",
    dominant_freq=dominant_freq[0],
)

# 导出数据
visualizer.export_waveform_data(
    t_display,
    differential,
    analyzer.freq_positive,
    spectrum[1 : len(analyzer.freq_positive) + 1],
    "differential_data",
)

# 生成报告
wave_info = {
    "name": "Half-Sine Wave",
    "width": width,
    "stats": stats,
    "dominant_freq": dominant_freq,
    "bandwidth": (*bandwidth, 0.5),
    "peaks": analyzer.find_multiple_peaks(differential_full),
}

visualizer.generate_report(wave_info, "differential_report.txt")

print(f"分析完成。结果保存在 {results_dir} 目录中。")
