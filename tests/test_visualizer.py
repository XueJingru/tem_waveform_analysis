"""
测试波形可视化器
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import shutil
import unittest

import numpy as np

from waveform_analyzer import WaveformAnalyzer
from waveform_generator import WaveformGenerator
from waveform_visualizer import WaveformVisualizer


class TestWaveformVisualizer(unittest.TestCase):
    """测试波形可视化器类"""

    def setUp(self):
        """测试前准备"""
        self.test_dir = "test_visualizer_results"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

        self.generator = WaveformGenerator()
        self.analyzer = WaveformAnalyzer()
        self.visualizer = WaveformVisualizer({"results_dir": self.test_dir})

        self.width = 0.01  # 10ms
        self.t = np.linspace(0, self.width * 3, 1000)
        self.wave = self.generator.half_sine_wave(self.t, self.width)

        # 计算频谱
        t_full = np.linspace(0, 1, 10000)
        wave_full = self.generator.half_sine_wave(t_full, self.width)
        self.spectrum = self.analyzer.compute_spectrum(wave_full)
        self.freq = self.analyzer.freq_positive

        # 确保使用相同长度的频率和频谱数据
        self.freq = self.analyzer.freq_positive
        self.spectrum_positive = self.spectrum[
            : len(self.freq)
        ]  # 截取与freq长度相同的部分

    def tearDown(self):
        """测试后清理"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_plot_waveform(self):
        """测试波形绘制"""
        filename = "test_waveform.png"
        save_path = self.visualizer.plot_waveform(
            self.t, self.wave, self.width, "Test Waveform", filename
        )

        # 检查文件是否存在
        self.assertTrue(os.path.exists(save_path))

    def test_plot_spectrum(self):
        """测试频谱绘制"""
        filename = "test_spectrum.png"
        save_path = self.visualizer.plot_spectrum(
            self.freq, self.spectrum_positive, "Test Spectrum", filename
        )

        # 检查文件是否存在
        self.assertTrue(os.path.exists(save_path))

    def test_plot_waveform_and_spectrum(self):
        """测试波形和频谱绘制"""
        filename = "test_waveform_and_spectrum.png"
        save_path = self.visualizer.plot_waveform_and_spectrum(
            self.t,
            self.wave,
            self.freq,
            self.spectrum_positive,
            self.width,
            "Test Combined",
            filename,
        )

        # 检查文件是否存在
        self.assertTrue(os.path.exists(save_path))

    def test_export_waveform_data(self):
        """测试数据导出"""
        filename_base = "test_export"
        time_file, freq_file = self.visualizer.export_waveform_data(
            self.t,
            self.wave,
            self.freq,
            self.spectrum_positive,
            filename_base,
        )

        # 检查文件是否存在
        self.assertTrue(os.path.exists(time_file))
        self.assertTrue(os.path.exists(freq_file))

    def test_generate_report(self):
        """测试报告生成"""
        filename = "test_report.txt"

        wave_info = {
            "name": "Test Wave",
            "width": self.width,
            "stats": {
                "mean": 0.1,
                "std": 0.2,
                "min": -0.5,
                "max": 1.0,
                "peak_to_peak": 1.5,
                "rms": 0.3,
                "energy": 0.4,
            },
            "dominant_freq": (100, 0.8),
            "bandwidth": (50, 200, 150, 0.5),
            "peaks": ([100, 200, 300], [0.8, 0.6, 0.4]),
        }

        report_path = self.visualizer.generate_report(wave_info, filename)

        # 检查文件是否存在
        self.assertTrue(os.path.exists(report_path))


if __name__ == "__main__":
    unittest.main()
