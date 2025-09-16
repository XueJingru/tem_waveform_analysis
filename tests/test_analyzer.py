"""
测试波形分析器
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest

import numpy as np

from waveform_analyzer import WaveformAnalyzer
from waveform_generator import WaveformGenerator


class TestWaveformAnalyzer(unittest.TestCase):
    """测试波形分析器类"""

    def setUp(self):
        """测试前准备"""
        self.generator = WaveformGenerator()
        self.analyzer = WaveformAnalyzer()
        self.width = 0.01  # 10ms

    def test_compute_spectrum(self):
        """测试频谱计算"""
        # 生成正弦波
        t = np.linspace(0, 1, 10000)
        freq = 100  # 100Hz
        wave = np.sin(2 * np.pi * freq * t)

        # 计算频谱
        spectrum = self.analyzer.compute_spectrum(wave, normalize=False)

        # 找到频谱中的峰值
        peak_idx = np.argmax(spectrum[1:]) + 1
        peak_freq = self.analyzer.freq[peak_idx]

        # 检查峰值频率是否接近预期
        self.assertAlmostEqual(peak_freq, freq, delta=1.0)

    def test_find_dominant_frequency(self):
        """测试主频查找"""
        # 生成正弦波
        t = np.linspace(0, 1, 10000)
        freq = 100  # 100Hz
        wave = np.sin(2 * np.pi * freq * t)

        # 查找主频
        dominant_freq, _ = self.analyzer.find_dominant_frequency(wave)

        # 检查主频是否接近预期
        self.assertAlmostEqual(dominant_freq, freq, delta=1.0)

    def test_compute_bandwidth(self):
        """测试带宽计算"""
        # 生成半正弦波
        wave = self.generator.half_sine_wave(self.analyzer.t, self.width)

        # 计算带宽
        low_freq, high_freq, bandwidth = self.analyzer.compute_bandwidth(wave)

        # 检查带宽是否大于0
        self.assertGreater(bandwidth, 0)
        self.assertLess(low_freq, high_freq)

    def test_compute_energy(self):
        """测试能量计算"""
        # 生成方波
        wave = self.generator.square_wave(self.analyzer.t, self.width)

        # 计算能量
        energy = self.analyzer.compute_energy(wave)

        # 检查能量是否大于0
        self.assertGreater(energy, 0)

    def test_compute_statistics(self):
        """测试统计特性计算"""
        # 生成三角波
        wave = self.generator.triangle_wave(self.analyzer.t, self.width)

        # 计算统计特性
        stats = self.analyzer.compute_statistics(wave)

        # 检查统计特性
        self.assertIn("mean", stats)
        self.assertIn("std", stats)
        self.assertIn("min", stats)
        self.assertIn("max", stats)
        self.assertIn("peak_to_peak", stats)
        self.assertIn("rms", stats)
        self.assertIn("energy", stats)

        # 检查最大值和最小值
        self.assertAlmostEqual(stats["max"], 1.0, delta=1e-4)
        self.assertGreaterEqual(stats["min"], 0.0)
        self.assertAlmostEqual(stats["peak_to_peak"], 1.0, delta=1e-4)


if __name__ == "__main__":
    unittest.main()
