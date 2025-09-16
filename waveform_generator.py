import numpy as np
import importlib
import os


class WaveformGenerator:
    """波形生成器类，用于生成各种波形"""

    def __init__(self, config=None):
        """
        初始化波形生成器
        
        参数:
        config (dict): 配置参数字典，可包含以下键:
            - time_delay: 波形时间延迟
            - pulse_ratio: 脉冲宽度比例
        """
        # 默认配置
        default_config = {
            "time_delay": 1e-5,
            "pulse_ratio": 0.5,
        }

        # 更新配置
        self.config = default_config
        if config:
            self.config.update(config)

        # 检查是否安装了SimPEG
        self.has_simpeg = self._check_simpeg()

    def _check_simpeg(self):
        """检查是否安装了SimPEG"""
        try:
            import simpeg.electromagnetics.time_domain as tdem
            return True
        except ImportError:
            return False

    def half_sine_wave(self, t, width):
        """
        生成半正弦波
        
        参数:
        t (ndarray): 时间向量
        width (float): 波宽，单位秒
        
        返回:
        ndarray: 波形振幅
        """
        wave = np.zeros_like(t)
        mask = (0 <= t) & (t <= width)
        wave[mask] = np.sin(np.pi * t[mask] / width)
        return wave

    def differential_pulse(self, t, width):
        """
        生成差分脉冲波
        
        参数:
        t (ndarray): 时间向量
        width (float): 波宽，单位秒
        
        返回:
        ndarray: 波形振幅
        """
        wave = np.zeros_like(t)
        time_delay = self.config["time_delay"]
        pulse_time = width * self.config["pulse_ratio"]

        # 时间点定义
        t1 = 0
        t2 = t1 + time_delay
        t3 = t2 + pulse_time
        t4 = t3 + 2 * time_delay
        t5 = t4 + pulse_time
        t6 = t5 + time_delay

        # 使用向量化操作代替循环
        mask1 = (t1 <= t) & (t < t2)
        mask2 = (t2 <= t) & (t < t3)
        mask3 = (t3 <= t) & (t < t4)
        mask4 = (t4 <= t) & (t < t5)
        mask5 = (t5 <= t) & (t < t6)

        wave[mask1] = (t[mask1] - t1) / time_delay
        wave[mask2] = 1.0
        wave[mask3] = 1.0 - (t[mask3] - t3) / time_delay
        wave[mask4] = -1.0
        wave[mask5] = -1.0 * (t6 - t[mask5]) / time_delay

        return wave

    def square_wave(self, t, width):
        """
        生成方波
        
        参数:
        t (ndarray): 时间向量
        width (float): 波宽，单位秒
        
        返回:
        ndarray: 波形振幅
        """
        wave = np.zeros_like(t)
        mask = (0 <= t) & (t <= width)
        wave[mask] = 1
        return wave
        
    def triangle_wave(self, t, width):
        """
        生成三角波
        
        参数:
        t (ndarray): 时间向量
        width (float): 波宽，单位秒
        
        返回:
        ndarray: 波形振幅
        """
        wave = np.zeros_like(t)
        mask1 = (0 <= t) & (t <= width/2)
        mask2 = (width/2 < t) & (t <= width)
        
        wave[mask1] = 2 * t[mask1] / width
        wave[mask2] = 2 - 2 * t[mask2] / width
        
        return wave
        
    def gaussian_pulse(self, t, width):
        """
        生成高斯脉冲
        
        参数:
        t (ndarray): 时间向量
        width (float): 波宽，单位秒
        
        返回:
        ndarray: 波形振幅
        """
        # 高斯脉冲中心和标准差
        center = width / 2
        sigma = width / 6  # 使3sigma约等于半宽
        
        return np.exp(-((t - center) ** 2) / (2 * sigma ** 2))

    def simpeg_trapezoid(self, t, width):
        """
        生成SimPEG梯形波
        
        参数:
        t (ndarray): 时间向量
        width (float): 波宽，单位秒
        
        返回:
        ndarray: 波形振幅
        """
        if not self.has_simpeg:
            raise ImportError("SimPEG not installed. Please install it first.")
            
        import simpeg.electromagnetics.time_domain as tdem
        
        time_delay = self.config["time_delay"]
        ramp_on = np.array([0, time_delay])
        ramp_off = np.array([width - time_delay, width])
        
        waveform = tdem.sources.TrapezoidWaveform(ramp_on=ramp_on, ramp_off=ramp_off)
        
        return np.array([waveform.eval(time) for time in t])

    def simpeg_differential_pulse(self, t, width):
        """
        生成SimPEG差分脉冲
        
        参数:
        t (ndarray): 时间向量
        width (float): 波宽，单位秒
        
        返回:
        ndarray: 波形振幅
        """
        if not self.has_simpeg:
            raise ImportError("SimPEG not installed. Please install it first.")
            
        import simpeg.electromagnetics.time_domain as tdem
        
        time_delay = self.config["time_delay"]
        ramp_on = np.array([0, time_delay])
        ramp_off = np.array([width - time_delay, width])
        
        waveform = tdem.sources.DifferentialPulseWaveform(ramp_on=ramp_on, ramp_off=ramp_off)
        
        return np.array([waveform.eval(time) for time in t])

    def simpeg_step_off(self, t, width):
        """
        生成SimPEG阶跃波
        
        参数:
        t (ndarray): 时间向量
        width (float): 波宽，单位秒
        
        返回:
        ndarray: 波形振幅
        """
        if not self.has_simpeg:
            raise ImportError("SimPEG not installed. Please install it first.")
            
        import simpeg.electromagnetics.time_domain as tdem
        
        waveform = tdem.sources.StepOffWaveform(off_time=width)
        
        return np.array([waveform.eval(time) for time in t])
        
    def custom_waveform(self, t, width, func):
        """
        使用自定义函数生成波形
        
        参数:
        t (ndarray): 时间向量
        width (float): 波宽，单位秒
        func (callable): 自定义波形函数，接受参数(t, width)
        
        返回:
        ndarray: 波形振幅
        """
        return func(t, width)
