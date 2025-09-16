"""Waveform Analyzer module for TEM waveform analysis.

This module provides functionality for waveform analyzer.
"""

import numpy as np
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks


class WaveformAnalyzer:
    """波形分析器类，用于分析波形特性."""

    def __init__(self, config=None):
        """
        初始化波形分析器.

        参数:
        config (dict): 配置参数字典，可包含以下键:
            - t_max: 最大时间
            - n_samples: 采样点数
        """
        # 默认配置
        default_config = {
            "t_max": 1.0,
            "n_samples": 100000,
        }

        # 更新配置
        self.config = default_config
        if config:
            self.config.update(config)

        # 初始化时间和频率参数
        self._init_time_freq_params()

    def _init_time_freq_params(self):
        """初始化时间和频率参数."""
        self.t = np.linspace(0, self.config["t_max"], self.config["n_samples"])
        self.dt = self.t[1] - self.t[0]
        self.n_freq = self.config["n_samples"] // 2
        self.freq = fftfreq(self.config["n_samples"], self.dt)[: self.n_freq]
        self.freq_positive = self.freq[self.freq > 0]

    def compute_spectrum(self, wave, normalize=True):
        """
        计算波形的频谱.

        参数:
        wave (ndarray): 波形振幅
        normalize (bool): 是否归一化频谱

        返回:
        ndarray: 频谱幅值
        """
        spectrum = fft(wave)
        magnitude = np.abs(spectrum[: self.n_freq]) / self.config["n_samples"]

        if normalize and np.max(magnitude) > 0:
            magnitude = magnitude / np.max(magnitude)

        return magnitude

    def find_dominant_frequency(self, wave, min_freq=1, max_freq=None):
        """
        查找波形的主频.

        参数:
        wave (ndarray): 波形振幅
        min_freq (float): 最小频率限制，单位Hz
        max_freq (float): 最大频率限制，单位Hz

        返回:
        tuple: (主频, 幅值)
        """
        spectrum = self.compute_spectrum(wave, normalize=False)

        # 确定频率范围
        min_idx = max(1, np.searchsorted(self.freq_positive, min_freq))
        if max_freq is None:
            max_idx = len(self.freq_positive)
        else:
            max_idx = np.searchsorted(self.freq_positive, max_freq)

        # 在指定范围内查找峰值
        freq_range = self.freq_positive[min_idx:max_idx]
        spectrum_range = spectrum[min_idx : min_idx + len(freq_range)]

        if len(freq_range) == 0:
            return (0, 0)

        # 找到最大值
        peak_idx = np.argmax(spectrum_range)
        dominant_freq = freq_range[peak_idx]
        peak_value = spectrum_range[peak_idx]

        return (dominant_freq, peak_value)

    def find_multiple_peaks(
        self, wave, n_peaks=3, min_freq=1, max_freq=None, height=0.1
    ):
        """
        查找波形的多个频率峰值.

        参数:
        wave (ndarray): 波形振幅
        n_peaks (int): 要查找的峰值数量
        min_freq (float): 最小频率限制，单位Hz
        max_freq (float): 最大频率限制，单位Hz
        height (float): 峰值最小高度（相对于最大值）

        返回:
        tuple: (峰值频率数组, 对应幅值数组)
        """
        spectrum = self.compute_spectrum(wave, normalize=True)

        # 确定频率范围
        min_idx = max(1, np.searchsorted(self.freq_positive, min_freq))
        if max_freq is None:
            max_idx = len(self.freq_positive)
        else:
            max_idx = np.searchsorted(self.freq_positive, max_freq)

        # 在指定范围内查找峰值
        freq_range = self.freq_positive[min_idx:max_idx]
        spectrum_range = spectrum[min_idx : min_idx + len(freq_range)]

        if len(freq_range) == 0:
            return ([], [])

        # 找到多个峰值
        peaks, _ = find_peaks(spectrum_range, height=height)

        # 按幅值排序
        sorted_indices = np.argsort(spectrum_range[peaks])[::-1][:n_peaks]
        peak_freqs = freq_range[peaks[sorted_indices]]
        peak_values = spectrum_range[peaks[sorted_indices]]

        return (peak_freqs, peak_values)

    def compute_bandwidth(self, wave, threshold=0.8):
        """
        计算波形的带宽（频谱幅值超过阈值的频率范围）.

        参数:
        wave (ndarray): 波形振幅
        threshold (float): 阈值，相对于最大幅值

        返回:
        tuple: (最低频率, 最高频率, 带宽)
        """
        spectrum = self.compute_spectrum(wave, normalize=True)

        # 找到超过阈值的频率点
        mask = spectrum[1 : len(self.freq_positive) + 1] >= threshold

        if not np.any(mask):
            return (0, 0, 0)

        indices = np.where(mask)[0]
        low_freq = self.freq_positive[indices[0]]
        high_freq = self.freq_positive[indices[-1]]
        bandwidth = high_freq - low_freq

        return (low_freq, high_freq, bandwidth)

    def compute_energy(self, wave):
        """
        计算波形的能量.

        参数:
        wave (ndarray): 波形振幅

        返回:
        float: 波形能量
        """
        return np.sum(wave**2) * self.dt

    def compute_statistics(self, wave):
        """
        计算波形的统计特性.

        参数:
        wave (ndarray): 波形振幅

        返回:
        dict: 包含统计特性的字典
        """
        stats = {
            "mean": np.mean(wave),
            "std": np.std(wave),
            "min": np.min(wave),
            "max": np.max(wave),
            "peak_to_peak": np.max(wave) - np.min(wave),
            "rms": np.sqrt(np.mean(wave**2)),
            "energy": self.compute_energy(wave),
        }

        return stats
