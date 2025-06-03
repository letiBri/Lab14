from dataclasses import dataclass

from model.order import Order


@dataclass
class Arco:
    ordine1: int
    ordine2: int
    peso: int