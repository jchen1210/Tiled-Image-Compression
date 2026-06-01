from dataclasses import dataclass

@dataclass
class OptimizationSettings:
    '''
    Hyperparameters for the CVXPY model
    '''
    def __init__(self, edge_penalty_weight: float, size_bonus_weight: float):
        self.edge_penalty_weight = edge_penalty_weight
        self.size_bonus_weight = size_bonus_weight

@dataclass
class ImageSettings:
    '''
    Settings for the image tiling
    '''
    def __init__(self, num_rows: int, num_cols: int, block_size: int):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.block_size = block_size