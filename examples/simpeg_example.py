"""SimPEG波形示例."""

import os
import sys

import numpy as np

from waveform_analyzer import WaveformAnalyzer
from waveform_generator import WaveformGenerator
from waveform_visualizer import WaveformVisualizer

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 创建结果目录
results_dir = "simpeg_example_results"
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# 初始化各个组件
generator = WaveformGenerator()
analyzer = WaveformAnalyzer({"t_max": 0.5, "n_samples": 50000})
visualizer = WaveformVisualizer({"results_dir": results_dir})

# 检查是否安装了SimPEG
if not generator.has_simpeg:
    print("SimPEG未安装，请先安装SimPEG库。")
    exit()

# 设置波形参数
width = 5e-3  # 5ms
t_display = np.linspace(0, width * 3, 10000)  # 显示3倍波宽
t_full = np.linspace(
    0, analyzer.config["t_max"], analyzer.config["n_samples"]
)  # 用于频谱分析的完整时间序列

# 生成SimPEG波形
trapezoid = generator.simpeg_trapezoid(t_display, width)
trapezoid_full = generator.simpeg_trapezoid(t_full, width)

diff_pulse = generator.simpeg_differential_pulse(t_display, width)
diff_pulse_full = generator.simpeg_differential_pulse(t_full, width)

step_off = generator.simpeg_step_off(t_display, width)
step_off_full = generator.simpeg_step_off(t_full, width)

# 分析波形
trapezoid_spectrum = analyzer.compute_spectrum(trapezoid_full)
diff_pulse_spectrum = analyzer.compute_spectrum(diff_pulse_full)
step_off_spectrum = analyzer.compute_spectrum(step_off_full)

# 可视化波形和频谱
visualizer.plot_waveform_and_spectrum(
    t_display,
    trapezoid,
    analyzer.freq_positive,
    trapezoid_spectrum[1 : len(analyzer.freq_positive) + 1],
    width,
    f"SimPEG Trapezoid Wave (Width: {width*1e3:.1f}ms)",
    "simpeg_trapezoid_analysis.png",
)

visualizer.plot_waveform_and_spectrum(
    t_display,
    diff_pulse,
    analyzer.freq_positive,
    diff_pulse_spectrum[1 : len(analyzer.freq_positive) + 1],
    width,
    f"SimPEG Differential Pulse (Width: {width*1e3:.1f}ms)",
    "simpeg_diff_pulse_analysis.png",
)

visualizer.plot_waveform_and_spectrum(
    t_display,
    step_off,
    analyzer.freq_positive,
    step_off_spectrum[1 : len(analyzer.freq_positive) + 1],
    width,
    f"SimPEG Step-Off Wave (Width: {width*1e3:.1f}ms)",
    "simpeg_step_off_analysis.png",
)

# 比较不同波形
visualizer.plot_multiple_waveforms(
    t_display,
    [trapezoid, diff_pulse, step_off],
    [width, width, width],
    ["Trapezoid Wave", "Differential Pulse", "Step-Off Wave"],
    f"SimPEG Waveform Comparison (Width: {width*1e3:.1f}ms)",
    "simpeg_waveform_comparison.png",
)

visualizer.plot_multiple_spectra(
    analyzer.freq_positive,
    [
        trapezoid_spectrum[1 : len(analyzer.freq_positive) + 1],
        diff_pulse_spectrum[1 : len(analyzer.freq_positive) + 1],
        step_off_spectrum[1 : len(analyzer.freq_positive) + 1],
    ],
    ["Trapezoid Wave", "Differential Pulse", "Step-Off Wave"],
    f"SimPEG Spectrum Comparison (Width: {width*1e3:.1f}ms)",
    "simpeg_spectrum_comparison.png",
)

print(f"分析完成。结果保存在 {results_dir} 目录中。")
