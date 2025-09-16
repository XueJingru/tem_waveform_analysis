import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class WaveformVisualizer:
    """波形可视化器类，用于可视化和保存波形分析结果"""

    def __init__(self, config=None):
        """
        初始化波形可视化器

        参数:
        config (dict): 配置参数字典，可包含以下键:
            - colors: 绘图颜色列表
            - results_dir: 结果保存目录
            - dpi: 图像DPI
            - figsize_time: 时域图尺寸
            - figsize_freq: 频域图尺寸
            - figsize_compare: 比较图尺寸
        """
        # 默认配置
        default_config = {
            "colors": [
                "#FF6666",
                "#FF9966",
                "#FFCC66",
                "#99CCFF",
                "#3399FF",
                "#666699",
            ],
            "results_dir": "waveform_results",
            "dpi": 300,
            "figsize_time": (10, 6),
            "figsize_freq": (10, 6),
            "figsize_compare": (12, 10),
        }

        # 更新配置
        self.config = default_config
        if config:
            self.config.update(config)

        # 创建结果保存目录
        if not os.path.exists(self.config["results_dir"]):
            os.makedirs(self.config["results_dir"])
        self.results_dir = self.config["results_dir"]

        # 设置绘图样式
        plt.rcParams["font.family"] = "Times New Roman"
        plt.rcParams["mathtext.fontset"] = "stix"
        plt.rcParams["axes.unicode_minus"] = True

    def plot_waveform(self, t, wave, width, title, filename, xlim=None, ylim=None):
        """
        绘制单个波形

        参数:
        t (ndarray): 时间向量
        wave (ndarray): 波形振幅
        width (float): 波宽，单位秒
        title (str): 图表标题
        filename (str): 保存文件名
        xlim (tuple): x轴范围
        ylim (tuple): y轴范围
        """
        plt.figure(figsize=self.config["figsize_time"])
        plt.plot(t * 1e3, wave, "r-", linewidth=2)
        plt.axhline(y=0, color="k", linestyle="-", linewidth=0.8)

        if xlim is None:
            plt.xlim([0, width * 3 * 1e3])  # 默认显示3倍波宽
        else:
            plt.xlim(xlim)

        if ylim is not None:
            plt.ylim(ylim)

        plt.xlabel("Time (ms)")
        plt.ylabel("Amplitude")
        plt.title(title)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        save_path = os.path.join(self.config["results_dir"], filename)
        plt.savefig(save_path, dpi=self.config["dpi"])
        plt.close()

        return save_path

    def plot_spectrum(
        self, freq, spectrum, title="Frequency Spectrum", filename="spectrum.png"
    ):
        """
        绘制频谱图

        Args:
            freq: 频率数组
            spectrum: 频谱数组
            title: 图表标题
            filename: 保存的文件名

        Returns:
            str: 保存的文件路径
        """
        plt.figure(figsize=(10, 6))

        # 确保频率和频谱数组长度一致
        min_len = min(len(freq), len(spectrum))
        freq = freq[:min_len]
        spectrum = spectrum[:min_len]

        plt.semilogx(freq, spectrum, "b-", linewidth=2)
        plt.grid(True, which="both", ls="--", alpha=0.7)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")
        plt.title(title)

        # 设置x轴的范围和刻度
        if len(freq) > 0:
            plt.xlim(freq[1], freq[-1])  # 从第二个点开始，避免log(0)

        save_path = os.path.join(self.results_dir, filename)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.close()

        return save_path

    def plot_waveform_and_spectrum(
        self,
        t,
        wave,
        freq,
        spectrum,
        width=None,
        title="Waveform and Spectrum",
        filename="waveform_and_spectrum.png",
        dominant_freq=None,  # 新增参数
    ):
        """
        在一张图中绘制波形和频谱

        Args:
            t: 时间数组
            wave: 波形数组
            freq: 频率数组
            spectrum: 频谱数组
            width: 波形宽度
            title: 图表标题
            filename: 保存的文件名
            dominant_freq: 主频，如果提供则在频谱图中标出

        Returns:
            str: 保存的文件路径
        """
        fig, axes = plt.subplots(2, 1, figsize=(10, 10))

        # 绘制波形
        axes[0].plot(t, wave, "r-", linewidth=2)
        axes[0].grid(True, ls="--", alpha=0.7)
        axes[0].set_xlabel("Time (s)")
        axes[0].set_ylabel("Amplitude")
        axes[0].set_title("Waveform")

        if width is not None:
            axes[0].axvline(
                x=width, color="g", linestyle="--", label=f"Width = {width:.3f}s"
            )
            axes[0].legend()

        # 确保频率和频谱数组长度一致
        min_len = min(len(freq), len(spectrum))
        freq_plot = freq[:min_len]
        spectrum_plot = spectrum[:min_len]

        # 绘制频谱
        axes[1].semilogx(freq_plot, spectrum_plot, "b-", linewidth=2)
        axes[1].grid(True, which="both", ls="--", alpha=0.7)
        axes[1].set_xlabel("Frequency (Hz)")
        axes[1].set_ylabel("Amplitude")
        axes[1].set_title("Frequency Spectrum")

        # 如果提供了主频，在频谱图中标出
        if dominant_freq is not None:
            # 找到主频对应的幅值
            # 找到最接近主频的频率点索引
            if len(freq_plot) > 0:
                idx = np.abs(freq_plot - dominant_freq).argmin()
                dom_freq_amp = spectrum_plot[idx]
                
                # 在频谱图中标出主频位置
                axes[1].axvline(
                    x=dominant_freq, 
                    color="r", 
                    linestyle="--", 
                    label=f"Dominant Freq = {dominant_freq:.1f} Hz"
                )
                axes[1].plot(dominant_freq, dom_freq_amp, 'ro', markersize=6)
                axes[1].legend()

        # 设置x轴的范围和刻度
        if len(freq_plot) > 0:
            axes[1].set_xlim(freq_plot[1], freq_plot[-1])  # 从第二个点开始，避免log(0)

        plt.suptitle(title, fontsize=16)
        plt.tight_layout()

        save_path = os.path.join(self.results_dir, filename)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.close()

        return save_path


    def export_waveform_data(
        self, t, wave, freq, spectrum, filename_base="waveform_data"
    ):
        """
        导出波形和频谱数据到CSV文件

        Args:
            t: 时间数组
            wave: 波形数组
            freq: 频率数组
            spectrum: 频谱数组
            filename_base: 文件名基础

        Returns:
            tuple: (时域文件路径, 频域文件路径)
        """
        import pandas as pd

        # 导出时域数据
        time_data = pd.DataFrame({"Time (s)": t, "Amplitude": wave})

        time_file = os.path.join(self.results_dir, f"{filename_base}_time.csv")
        time_data.to_csv(time_file, index=False)

        # 确保频率和频谱数组长度一致
        min_len = min(len(freq), len(spectrum))
        freq_export = freq[:min_len]
        spectrum_export = spectrum[:min_len]

        # 导出频域数据
        freq_data = pd.DataFrame(
            {"Frequency (Hz)": freq_export, "Amplitude": spectrum_export}
        )

        freq_file = os.path.join(self.results_dir, f"{filename_base}_freq.csv")
        freq_data.to_csv(freq_file, index=False)

        return time_file, freq_file

    def plot_multiple_waveforms(
        self, t, waves, widths, labels, title, filename, xlim=None, ylim=None
    ):
        """
        绘制多个波形对比

        参数:
        t (ndarray): 时间向量
        waves (list): 波形振幅列表
        widths (list): 波宽列表，单位秒
        labels (list): 波形标签列表
        title (str): 图表标题
        filename (str): 保存文件名
        xlim (tuple): x轴范围
        ylim (tuple): y轴范围
        """
        plt.figure(figsize=self.config["figsize_compare"])

        for i, (wave, width, label) in enumerate(zip(waves, widths, labels)):
            color_idx = i % len(self.config["colors"])
            plt.plot(
                t * 1e3,
                wave,
                color=self.config["colors"][color_idx],
                label=label,
                linewidth=2,
            )

        plt.axhline(y=0, color="k", linestyle="-", linewidth=0.8)

        if xlim is None:
            plt.xlim([0, max(widths) * 3 * 1e3])  # 默认显示3倍最大波宽
        else:
            plt.xlim(xlim)

        if ylim is not None:
            plt.ylim(ylim)
        else:
            plt.ylim([-1.1, 1.1])

        plt.xlabel("Time (ms)")
        plt.ylabel("Amplitude")
        plt.title(title)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        save_path = os.path.join(self.config["results_dir"], filename)
        plt.savefig(save_path, dpi=self.config["dpi"])
        plt.close()

        return save_path

    def plot_multiple_spectra(
        self, freq, spectra, labels, title, filename, xlim=None, ylim=None
    ):
        """
        绘制多个频谱对比

        参数:
        freq (ndarray): 频率向量
        spectra (list): 频谱幅值列表
        labels (list): 频谱标签列表
        title (str): 图表标题
        filename (str): 保存文件名
        xlim (tuple): x轴范围
        ylim (tuple): y轴范围
        """
        plt.figure(figsize=self.config["figsize_compare"])

        for i, (spectrum, label) in enumerate(zip(spectra, labels)):
            color_idx = i % len(self.config["colors"])
            plt.semilogx(
                freq,
                spectrum,
                color=self.config["colors"][color_idx],
                label=label,
                linewidth=2,
            )

        if xlim is None:
            plt.xlim([1, 1e5])  # 默认频率范围
        else:
            plt.xlim(xlim)

        if ylim is not None:
            plt.ylim(ylim)
        else:
            plt.ylim([0, 1.05])

        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Normalized Amplitude")
        plt.title(title)
        plt.legend()
        plt.grid(True, which="both", linestyle="--", alpha=0.3)
        plt.tight_layout()

        save_path = os.path.join(self.config["results_dir"], filename)
        plt.savefig(save_path, dpi=self.config["dpi"])
        plt.close()

        return save_path

    def generate_report(self, wave_info, filename="waveform_report.txt"):
        """
        生成波形分析报告

        参数:
        wave_info (dict): 波形信息字典，包含以下键:
            - name: 波形名称
            - width: 波宽
            - stats: 统计信息
            - dominant_freq: 主频
            - bandwidth: 带宽信息
        filename (str): 报告文件名

        返回:
        str: 报告文件路径
        """
        report_path = os.path.join(self.config["results_dir"], filename)

        with open(report_path, "w") as f:
            f.write(f"波形分析报告\n")
            f.write(f"{'='*50}\n\n")

            f.write(f"波形名称: {wave_info['name']}\n")
            f.write(f"波宽: {wave_info['width']*1e3:.2f} ms\n\n")

            f.write(f"时域统计:\n")
            f.write(f"  平均值: {wave_info['stats']['mean']:.6f}\n")
            f.write(f"  标准差: {wave_info['stats']['std']:.6f}\n")
            f.write(f"  最小值: {wave_info['stats']['min']:.6f}\n")
            f.write(f"  最大值: {wave_info['stats']['max']:.6f}\n")
            f.write(f"  峰峰值: {wave_info['stats']['peak_to_peak']:.6f}\n")
            f.write(f"  有效值: {wave_info['stats']['rms']:.6f}\n")
            f.write(f"  能量: {wave_info['stats']['energy']:.6f}\n\n")

            f.write(f"频域分析:\n")
            f.write(f"  主频: {wave_info['dominant_freq'][0]:.2f} Hz\n")
            f.write(f"  主频幅值: {wave_info['dominant_freq'][1]:.6f}\n")

            if "bandwidth" in wave_info:
                f.write(f"  带宽分析 (阈值: {wave_info['bandwidth'][3]:.2f}):\n")
                f.write(f"    低频: {wave_info['bandwidth'][0]:.2f} Hz\n")
                f.write(f"    高频: {wave_info['bandwidth'][1]:.2f} Hz\n")
                f.write(f"    带宽: {wave_info['bandwidth'][2]:.2f} Hz\n\n")

            if "peaks" in wave_info:
                f.write(f"多峰分析:\n")
                for i, (freq, val) in enumerate(
                    zip(wave_info["peaks"][0], wave_info["peaks"][1])
                ):
                    f.write(f"  峰值 {i+1}: {freq:.2f} Hz (幅值: {val:.6f})\n")

            f.write(f"\n生成时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        return report_path
