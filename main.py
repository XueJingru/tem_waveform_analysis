"""
波形分析项目主程序
"""

from waveform_manager import WaveformManager
import argparse


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='波形分析工具')
    
    parser.add_argument('--mode', type=str, default='comprehensive',
                        choices=['comprehensive', 'single', 'compare'],
                        help='分析模式: comprehensive(全面分析), single(单一波形), compare(比较波形)')
    
    parser.add_argument('--wave_type', type=str, default='half_sine',
                        choices=['half_sine', 'differential', 'square', 'triangle', 
                                'gaussian', 'trapezoid', 'simpeg_diff', 'step_off'],
                        help='波形类型')
    
    parser.add_argument('--width', type=float, default=5e-3,
                        help='波宽，单位秒')
    
    parser.add_argument('--results_dir', type=str, default='waveform_results',
                        help='结果保存目录')
    
    return parser.parse_args()


def get_wave_func(manager, wave_type):
    """获取波形函数"""
    wave_funcs = {
        'half_sine': manager.generator.half_sine_wave,
        'differential': manager.generator.differential_pulse,
        'square': manager.generator.square_wave,
        'triangle': manager.generator.triangle_wave,
        'gaussian': manager.generator.gaussian_pulse,
    }
    
    if manager.generator.has_simpeg:
        wave_funcs.update({
            'trapezoid': manager.generator.simpeg_trapezoid,
            'simpeg_diff': manager.generator.simpeg_differential_pulse,
            'step_off': manager.generator.simpeg_step_off,
        })
    
    return wave_funcs.get(wave_type)


def get_wave_name(wave_type):
    """获取波形名称"""
    wave_names = {
        'half_sine': 'Half-Sine Wave',
        'differential': 'Differential Pulse',
        'square': 'Square Wave',
        'triangle': 'Triangle Wave',
        'gaussian': 'Gaussian Pulse',
        'trapezoid': 'SimPEG Trapezoid',
        'simpeg_diff': 'SimPEG Differential Pulse',
        'step_off': 'SimPEG Step-Off',
    }
    
    return wave_names.get(wave_type)


def main():
    """主函数"""
    args = parse_args()
    
    # 初始化波形管理器
    manager = WaveformManager({
        "results_dir": args.results_dir,
    })
    
    if args.mode == 'comprehensive':
        # 运行全面分析
        manager.run_comprehensive_analysis()
    
    elif args.mode == 'single':
        # 分析单一波形
        wave_func = get_wave_func(manager, args.wave_type)
        wave_name = get_wave_name(args.wave_type)
        
        if wave_func is None:
            print(f"未知波形类型: {args.wave_type}")
            return
        
        print(f"分析 {wave_name} (Width: {args.width*1e3:.1f}ms)...")
        manager.analyze_single_waveform(wave_func, args.width, wave_name)
        print(f"分析完成。结果保存在 {args.results_dir} 目录中。")
    
    elif args.mode == 'compare':
        # 比较所有波形
        wave_funcs = []
        wave_names = []
        
        # 添加内置波形
        wave_types = ['half_sine', 'differential', 'square', 'triangle', 'gaussian']
        if manager.generator.has_simpeg:
            wave_types.extend(['trapezoid', 'simpeg_diff', 'step_off'])
        
        for wave_type in wave_types:
            wave_func = get_wave_func(manager, wave_type)
            wave_name = get_wave_name(wave_type)
            
            if wave_func is not None:
                wave_funcs.append(wave_func)
                wave_names.append(wave_name)
        
        print(f"比较波宽为 {args.width*1e3:.1f}ms 的波形...")
        manager.compare_waveforms(wave_funcs, wave_names, args.width)
        print(f"比较完成。结果保存在 {args.results_dir} 目录中。")


if __name__ == "__main__":
    main()
