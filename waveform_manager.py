import numpy as np
import os


class WaveformManager:
    """波形管理器类，整合波形生成、分析和可视化功能"""

    def __init__(self, config=None):
        """
        初始化波形管理器
        
        参数:
        config (dict): 配置参数字典
        """
        # 默认配置
        default_config = {
            "wave_widths": [0.6e-3, 1e-3, 2.5e-3, 5e-3, 10e-3, 20e-3],
            "time_delay": 1e-5,
            "t_max": 1.0,
            "n_samples": 100000,
            "results_dir": "waveform_results",
        }

        # 更新配置
        self.config = default_config
        if config:
            self.config.update(config)

        # 创建波形生成器
        from waveform_generator import WaveformGenerator
        self.generator = WaveformGenerator({
            "time_delay": self.config["time_delay"],
        })

        # 创建波形分析器
        from waveform_analyzer import WaveformAnalyzer
        self.analyzer = WaveformAnalyzer({
            "t_max": self.config["t_max"],
            "n_samples": self.config["n_samples"],
        })

        # 创建波形可视化器
        from waveform_visualizer import WaveformVisualizer
        self.visualizer = WaveformVisualizer({
            "results_dir": self.config["results_dir"],
        })

    def analyze_single_waveform(self, wave_func, width, name, save_data=True):
        """
        分析单个波形
        
        参数:
        wave_func (callable): 波形生成函数
        width (float): 波宽，单位秒
        name (str): 波形名称
        save_data (bool): 是否保存数据
        
        返回:
        dict: 分析结果
        """
        # 生成波形
        t_full = np.linspace(0, self.config["t_max"], self.config["n_samples"])
        wave = wave_func(t_full, width)
        
        # 分析波形
        spectrum = self.analyzer.compute_spectrum(wave)
        dominant_freq = self.analyzer.find_dominant_frequency(wave)
        bandwidth = self.analyzer.compute_bandwidth(wave)
        stats = self.analyzer.compute_statistics(wave)
        peaks = self.analyzer.find_multiple_peaks(wave)
        
        # 可视化
        t_display = np.linspace(0, width*3, 10000)
        wave_display = wave_func(t_display, width)
        
        # 保存结果
        result = {
            "name": name,
            "width": width,
            "dominant_freq": dominant_freq,
            "bandwidth": (*bandwidth, 0.5),  # 添加阈值信息
            "peaks": peaks,
            "stats": stats,
        }
        
        # 可视化波形和频谱
        self.visualizer.plot_waveform_and_spectrum(
            t_display, 
            wave_display, 
            self.analyzer.freq_positive, 
            spectrum[1:len(self.analyzer.freq_positive)+1],
            width,
            f"{name} (Width: {width*1e3:.1f}ms)",
            f"{name.replace(' ', '_')}_{width*1e3:.1f}ms_analysis.png",
            dominant_freq=dominant_freq[0]
        )
        
        # 生成报告
        self.visualizer.generate_report(
            result,
            f"{name.replace(' ', '_')}_{width*1e3:.1f}ms_report.txt"
        )
        
        # 保存数据
        if save_data:
            self.visualizer.export_waveform_data(
                t_display,
                wave_display,
                self.analyzer.freq_positive,
                spectrum[1:len(self.analyzer.freq_positive)+1],
                f"{name.replace(' ', '_')}_{width*1e3:.1f}ms"
            )
        
        return result

    def analyze_multiple_waveforms(self, wave_func, name):
        """
        分析多个波宽的波形
        
        参数:
        wave_func (callable): 波形生成函数
        name (str): 波形名称
        
        返回:
        list: 分析结果列表
        """
        results = []
        
        for width in self.config["wave_widths"]:
            result = self.analyze_single_waveform(wave_func, width, name)
            results.append(result)
        
        return results

    def compare_waveforms(self, wave_funcs, names, width):
        """
        比较不同波形
        
        参数:
        wave_funcs (list): 波形生成函数列表
        names (list): 波形名称列表
        width (float): 波宽，单位秒
        
        返回:
        dict: 比较结果
        """
        t_display = np.linspace(0, width*3, 10000)
        waves = []
        spectra = []
        results = []
        
        for wave_func, name in zip(wave_funcs, names):
            # 生成波形
            wave = wave_func(t_display, width)
            waves.append(wave)
            
            # 分析波形
            t_full = np.linspace(0, self.config["t_max"], self.config["n_samples"])
            wave_full = wave_func(t_full, width)
            spectrum = self.analyzer.compute_spectrum(wave_full)
            spectra.append(spectrum[1:len(self.analyzer.freq_positive)+1])
            
            # 收集结果
            result = self.analyze_single_waveform(wave_func, width, name, save_data=False)
            results.append(result)
        
        # 可视化波形比较
        self.visualizer.plot_multiple_waveforms(
            t_display, 
            waves, 
            [width] * len(wave_funcs), 
            names, 
            f"Waveform Comparison (Width: {width*1e3:.1f}ms)",
            f"waveform_comparison_{width*1e3:.1f}ms.png"
        )
        
        # 可视化频谱比较
        self.visualizer.plot_multiple_spectra(
            self.analyzer.freq_positive, 
            spectra, 
            names, 
            f"Spectrum Comparison (Width: {width*1e3:.1f}ms)",
            f"spectrum_comparison_{width*1e3:.1f}ms.png"
        )
        
        return {
            "width": width,
            "waveforms": names,
            "results": results
        }

    def run_comprehensive_analysis(self):
        """
        运行全面分析，分析所有内置波形
        """
        print("开始全面波形分析...")
        
        # 获取所有内置波形函数
        wave_funcs = [
            self.generator.half_sine_wave,
            self.generator.differential_pulse,
            self.generator.square_wave,
            self.generator.triangle_wave,
            self.generator.gaussian_pulse
        ]
        
        wave_names = [
            "Half-Sine Wave",
            "Differential Pulse",
            "Square Wave",
            "Triangle Wave",
            "Gaussian Pulse"
        ]
        
        # 如果安装了SimPEG，添加SimPEG波形
        if self.generator.has_simpeg:
            wave_funcs.extend([
                self.generator.simpeg_trapezoid,
                self.generator.simpeg_differential_pulse,
                self.generator.simpeg_step_off
            ])
            
            wave_names.extend([
                "SimPEG Trapezoid",
                "SimPEG Differential Pulse",
                "SimPEG Step-Off"
            ])
        
        # 分析每种波形的不同波宽
        for func, name in zip(wave_funcs, wave_names):
            print(f"分析 {name}...")
            self.analyze_multiple_waveforms(func, name)
        
        # 比较不同波形
        for width in [1e-3, 5e-3, 20e-3]:  # 选择几个典型波宽进行比较
            print(f"比较波宽为 {width*1e3:.1f}ms 的波形...")
            self.compare_waveforms(wave_funcs, wave_names, width)
        
        print(f"分析完成。结果保存在 {self.config['results_dir']} 目录中。")
