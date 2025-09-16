"""
测试波形生成器
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest

import numpy as np

from waveform_generator import WaveformGenerator


class TestWaveformGenerator(unittest.TestCase):
    """测试波形生成器类"""

    def setUp(self):
        """测试前准备"""
        self.generator = WaveformGenerator()
        self.t = np.linspace(0, 0.1, 1000)
        self.width = 0.01  # 10ms

    def test_half_sine_wave(self):
        """测试半正弦波"""
        wave = self.generator.half_sine_wave(self.t, self.width)

        # 检查波形长度
        self.assertEqual(len(wave), len(self.t))

        # 检查波形最大值
        self.assertAlmostEqual(np.max(wave), 1.0, delta=1e-2)

        # 检查波形在指定宽度之外为0
        self.assertEqual(np.sum(wave[self.t > self.width]), 0)

    def test_differential_pulse(self):
        """测试差分脉冲"""
        wave = self.generator.differential_pulse(self.t, self.width)

        # 检查波形长度
        self.assertEqual(len(wave), len(self.t))

        # 检查波形最大值和最小值
        self.assertAlmostEqual(np.max(wave), 1.0)
        self.assertAlmostEqual(np.min(wave), -1.0)

    def test_square_wave(self):
        """测试方波"""
        wave = self.generator.square_wave(self.t, self.width)

        # 检查波形长度
        self.assertEqual(len(wave), len(self.t))

        # 检查波形最大值
        self.assertAlmostEqual(np.max(wave), 1.0)

        # 检查波形在指定宽度之外为0
        self.assertEqual(np.sum(wave[self.t > self.width]), 0)

    def test_triangle_wave(self):
        """测试三角波"""
        wave = self.generator.triangle_wave(self.t, self.width)

        # 检查波形长度
        self.assertEqual(len(wave), len(self.t))

        # 检查波形最大值
        self.assertAlmostEqual(np.max(wave), 1.0, delta=1e-2)

        # 检查波形在指定宽度之外为0
        self.assertEqual(np.sum(wave[self.t > self.width]), 0)

    def test_gaussian_pulse(self):
        """测试高斯脉冲"""
        wave = self.generator.gaussian_pulse(self.t, self.width)

        # 检查波形长度
        self.assertEqual(len(wave), len(self.t))

        # 检查波形最大值
        self.assertAlmostEqual(np.max(wave), 1.0, delta=1e-2)

    def test_custom_waveform(self):
        """测试自定义波形"""

        def custom_func(t, width):
            return np.exp(-t / width) * np.sin(2 * np.pi * t / width)

        wave = self.generator.custom_waveform(self.t, self.width, custom_func)

        # 检查波形长度
        self.assertEqual(len(wave), len(self.t))

        # 检查是否与直接调用函数结果一致
        expected = custom_func(self.t, self.width)
        np.testing.assert_array_almost_equal(wave, expected)


if __name__ == "__main__":
    unittest.main()
