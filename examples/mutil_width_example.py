"""循环计算多个宽度的微分脉冲波形."""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec

from waveform_analyzer import WaveformAnalyzer
from waveform_generator import WaveformGenerator
from waveform_visualizer import WaveformVisualizer

# 导入必要的模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 创建结果目录
results_dir = "multi_width_analysis_results"
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# 初始化各个组件
generator = WaveformGenerator()
analyzer = WaveformAnalyzer({"t_max": 0.5, "n_samples": 50000})
visualizer = WaveformVisualizer({"results_dir": results_dir})

# 设置要分析的不同宽度值（单位：秒）
widths = [1e-3, 2e-3, 5e-3, 10e-3, 20e-3]  # 1ms到20ms的不同宽度

# 创建汇总比较图
fig = plt.figure(figsize=(15, 10))
gs = GridSpec(2, 2, figure=fig)

# 时域波形比较
ax1 = fig.add_subplot(gs[0, 0])
# 频谱比较
ax2 = fig.add_subplot(gs[0, 1])
# 主频与宽度关系
ax3 = fig.add_subplot(gs[1, 0])
# 带宽与宽度关系
ax4 = fig.add_subplot(gs[1, 1])

# 存储结果数据
dominant_freqs = []
bandwidths = []
peak_values = []

# 循环处理每个宽度
for width in widths:
    print(f"处理宽度为 {width*1e3:.1f}ms 的波形...")

    # 设置时间轴
    t_display = np.linspace(0, width * 4, 10000)  # 显示4倍波宽以便观察
    t_full = np.linspace(0, analyzer.config["t_max"], analyzer.config["n_samples"])

    # 生成微分脉冲波
    differential = generator.differential_pulse(t_display, width)
    differential_full = generator.differential_pulse(t_full, width)

    # 分析波形
    spectrum = analyzer.compute_spectrum(differential_full)
    dominant_freq = analyzer.find_dominant_frequency(differential_full)
    bandwidth = analyzer.compute_bandwidth(differential_full)
    stats = analyzer.compute_statistics(differential_full)
    peaks = analyzer.find_multiple_peaks(differential_full)

    # 存储结果
    dominant_freqs.append(dominant_freq[0])
    bandwidths.append(bandwidth[0])
    peak_values.append(np.max(np.abs(differential)))

    # 可视化单个波形和频谱
    visualizer.plot_waveform_and_spectrum(
        t_display,
        differential,
        analyzer.freq_positive,
        spectrum[1 : len(analyzer.freq_positive) + 1],
        width,
        f"Differential pulse (width: {width*1e3:.1f}ms)",
        f"differential_width_{width*1e3:.1f}ms.png",
        dominant_freq=dominant_freq[0],
    )

    # 导出数据
    visualizer.export_waveform_data(
        t_display,
        differential,
        analyzer.freq_positive,
        spectrum[1 : len(analyzer.freq_positive) + 1],
        f"differential_data_width_{width*1e3:.1f}ms",
    )

    # 生成报告
    wave_info = {
        "name": "Differential pulse",
        "width": width,
        "stats": stats,
        "dominant_freq": dominant_freq,
        "bandwidth": (*bandwidth, 0.8),
        "peaks": peaks,
    }

    visualizer.generate_report(
        wave_info, f"differential_report_width_{width*1e3:.1f}ms.txt"
    )

    # 添加到比较图
    # 归一化时域波形以便比较
    normalized_wave = differential / np.max(np.abs(differential))
    ax1.plot(t_display * 1000, normalized_wave, label=f"{width*1e3:.1f}ms")

    # 频谱比较（使用对数刻度以便观察）
    spec_to_plot = spectrum[1 : len(analyzer.freq_positive) + 1]
    spec_to_plot = spec_to_plot / np.max(spec_to_plot)  # 归一化频谱
    ax2.semilogy(analyzer.freq_positive, spec_to_plot, label=f"{width*1e3:.1f}ms")

# 绘制主频和带宽与宽度的关系
ax3.plot(np.array(widths) * 1000, dominant_freqs, "o-", linewidth=2)
ax3.set_xlabel("Wave width (ms)")
ax3.set_ylabel("Dominant frequency (Hz)")
ax3.set_title("Relationship between Dominant Frequency and Wave Width")
ax3.grid(True)

ax4.plot(np.array(widths) * 1000, bandwidths, "o-", linewidth=2)
ax4.set_xlabel("Wave width (ms)")
ax4.set_ylabel("Bandwidth (Hz)")
ax4.set_title("Relationship between Bandwidth and Wave Width")
ax4.grid(True)

# 设置比较图的标签
ax1.set_xlabel("Time (ms)")
ax1.set_ylabel("Normalized Amplitude")
ax1.set_title("Time Domain Comparison of Differential Pulses with Different Widths")
ax1.legend()
ax1.grid(True)

ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Normalized Amplitude (Log Scale)")
ax2.set_title(
    "Frequency Spectrum Comparison of Differential Pulses with Different Widths"
)
ax2.legend()
ax2.grid(True)

# 保存比较图
plt.tight_layout()
plt.savefig(os.path.join(results_dir, "width_comparison_summary.png"), dpi=300)

# 创建表格数据
table_data = {
    "宽度 (ms)": [w * 1000 for w in widths],
    "主频 (Hz)": dominant_freqs,
    "带宽 (Hz)": bandwidths,
    "峰值": peak_values,
}

# 导出表格数据到CSV
df = pd.DataFrame(table_data)
df.to_csv(os.path.join(results_dir, "width_comparison_data.csv"), index=False)

print(f"分析完成。所有结果保存在 {results_dir} 目录中。")
