import random

import numpy as np
import pandas as pd
import torch
import torchvision.transforms.v2 as T
from torch.utils.data import DataLoader, Dataset

IMG = 224
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]
NOMES = {0: 'meningioma', 1: 'glioma', 2: 'pituitary'}

# Augmentation leve, apenas no treino (aplicada antes da normalização).
train_aug = T.Compose([
    T.RandomHorizontalFlip(0.5),
    T.RandomRotation(10, interpolation=T.InterpolationMode.BILINEAR),
    T.ColorJitter(brightness=0.1, contrast=0.1),
])
norm = T.Normalize(MEAN, STD)


def load_cache(path):
    """Carrega o .npz do cache e devolve um dict com X, M, Y, IDS e row_of."""
    z = np.load(path)
    cache = {k: z[k] for k in ('X', 'M', 'Y', 'IDS')}
    cache['row_of'] = {int(i): k for k, i in enumerate(cache['IDS'])}
    return cache


class MRIDataset(Dataset):
    """Lê as linhas do CSV de divisão e busca as imagens no cache.

    augment=True aplica a augmentation do treino; return_mask=True também
    devolve a máscara do tumor (usada no teste e na análise de XAI).
    """

    def __init__(self, cache, csv_path, augment=False, return_mask=False):
        self.cache = cache
        self.ids = pd.read_csv(csv_path)['id'].astype(int).tolist()
        self.augment, self.return_mask = augment, return_mask

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, i):
        k = self.cache['row_of'][self.ids[i]]
        x = torch.from_numpy(self.cache['X'][k].astype(np.float32))
        x = x.unsqueeze(0).repeat(3, 1, 1)   # 1 canal -> 3 canais
        if self.augment:
            x = train_aug(x)
        x = norm(x)
        y = int(self.cache['Y'][k])
        if self.return_mask:
            return x, y, torch.from_numpy(self.cache['M'][k]), self.ids[i]
        return x, y, self.ids[i]


def seed_worker(worker_id):
    s = torch.initial_seed() % 2**32
    np.random.seed(s)
    random.seed(s)


def make_loaders(cache, splits_dir, batch=32, workers=2, seed=42):
    """Cria datasets e DataLoaders de treino, validação e teste."""
    g = torch.Generator()
    g.manual_seed(seed)
    train_ds = MRIDataset(cache, f'{splits_dir}/train.csv', augment=True)
    val_ds = MRIDataset(cache, f'{splits_dir}/val.csv')
    test_ds = MRIDataset(cache, f'{splits_dir}/test.csv', return_mask=True)
    train_dl = DataLoader(train_ds, batch, shuffle=True, num_workers=workers,
                          worker_init_fn=seed_worker, generator=g, pin_memory=True)
    val_dl = DataLoader(val_ds, batch, shuffle=False, num_workers=workers,
                        pin_memory=True)
    test_dl = DataLoader(test_ds, batch, shuffle=False, num_workers=workers,
                         pin_memory=True)
    return train_ds, val_ds, test_ds, train_dl, val_dl, test_dl