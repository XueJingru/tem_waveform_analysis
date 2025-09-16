"""自定义波形示例."""

import os
import sys

import numpy as np

from waveform_analyzer import WaveformAnalyzer
from waveform_generator import WaveformGenerator
from waveform_visualizer import WaveformVisualizer

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 创建结果目录
results_dir = "custom_waveform_results"
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# 初始化各个组件
generator = WaveformGenerator()
analyzer = WaveformAnalyzer({"t_max": 0.5, "n_samples": 50000})
visualizer = WaveformVisualizer({"results_dir": results_dir})


# 定义自定义波形函数
def sawtooth_wave(t, width):
    """锯齿波."""
    wave = np.zeros_like(t)
    mask = (0 <= t) & (t <= width)
    wave[mask] = t[mask] / width
    return wave


def chirp_wave(t, width):
    """啁啾信号."""
    wave = np.zeros_like(t)
    mask = (0 <= t) & (t <= width)
    f0 = 10  # 起始频率
    f1 = 1000  # 结束频率
    wave[mask] = np.sin(
        2 * np.pi * (f0 * t[mask] + (f1 - f0) * t[mask] ** 2 / (2 * width))
    )
    return wave


# 设置波形参数
width = 5e-3  # 5ms
t_display = np.linspace(0, width * 3, 10000)  # 显示3倍波宽
t_full = np.linspace(
    0, analyzer.config["t_max"], analyzer.config["n_samples"]
)  # 用于频谱分析的完整时间序列

# 生成自定义波形
sawtooth = sawtooth_wave(t_display, width)
sawtooth_full = sawtooth_wave(t_full, width)

chirp = chirp_wave(t_display, width)
chirp_full = chirp_wave(t_full, width)

# 使用generator的custom_waveform方法
custom_sawtooth = generator.custom_waveform(t_display, width, sawtooth_wave)
custom_chirp = generator.custom_waveform(t_display, width, chirp_wave)

# 分析波形
sawtooth_spectrum = analyzer.compute_spectrum(sawtooth_full)
chirp_spectrum = analyzer.compute_spectrum(chirp_full)

# 可视化波形和频谱
visualizer.plot_waveform_and_spectrum(
    t_display,
    sawtooth,
    analyzer.freq_positive,
    sawtooth_spectrum[1 : len(analyzer.freq_positive) + 1],
    width,
    f"Sawtooth Wave (Width: {width*1e3:.1f}ms)",
    "sawtooth_analysis.png",
)

visualizer.plot_waveform_and_spectrum(
    t_display,
    chirp,
    analyzer.freq_positive,
    chirp_spectrum[1 : len(analyzer.freq_positive) + 1],
    width,
    f"Chirp Wave (Width: {width*1e3:.1f}ms)",
    "chirp_analysis.png",
)

# 比较不同波形
visualizer.plot_multiple_waveforms(
    t_display,
    [sawtooth, chirp],
    [width, width],
    ["Sawtooth Wave", "Chirp Wave"],
    f"Custom Waveform Comparison (Width: {width*1e3:.1f}ms)",
    "custom_waveform_comparison.png",
)

visualizer.plot_multiple_spectra(
    analyzer.freq_positive,
    [
        sawtooth_spectrum[1 : len(analyzer.freq_positive) + 1],
        chirp_spectrum[1 : len(analyzer.freq_positive) + 1],
    ],
    ["Sawtooth Wave", "Chirp Wave"],
    f"Custom Spectrum Comparison (Width: {width*1e3:.1f}ms)",
    "custom_spectrum_comparison.png",
)

print(f"分析完成。结果保存在 {results_dir} 目录中。")
