import numpy as np

def calculate_abrams_features(water_kg: float, cement_kg: float, fly_ash_kg: float = 0.0, slag_kg: float = 0.0):
    """
    Computes physical materials informatics features:
    - Water-to-Binder ratio (w/b) according to Abrams and Lyse laws.
    - SCM (Supplementary Cementitious Materials) substitution ratios.
    """
    total_binder = cement_kg + fly_ash_kg + slag_kg
    if total_binder <= 0:
        raise ValueError("Total binder mass must be greater than zero.")
    
    wb_ratio = water_kg / total_binder
    scm_ratio = (fly_ash_kg + slag_kg) / total_binder
    
    # Abrams theoretical compressive strength index (fc = A / B^(w/c))
    abrams_index = 100.0 / (2.5 ** (wb_ratio * 4.0))
    
    return {
        'wb_ratio': round(wb_ratio, 4),
        'scm_ratio': round(scm_ratio, 4),
        'abrams_index': round(abrams_index, 2)
    }
