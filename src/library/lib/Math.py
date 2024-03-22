from typing import Union, List
from math import floor, sqrt, isnan


class Math:
    @staticmethod
    def floor(
        value: Union[int, float],
        unit: Union[int, float] = 1,
    ) -> Union[int, float]:
        return floor(value / unit) * unit

    @staticmethod
    def max(data: List[Union[int, float]]) -> Union[int, float, None]:
        return max(data) if data else None

    @staticmethod
    def min(data: List[Union[int, float]]) -> Union[int, float, None]:
        return min(data) if data else None

    @staticmethod
    def is_NaN(value: Union[int, float]) -> bool:
        return isnan(value)

    @staticmethod
    def ratio(a: Union[int, float], b: Union[int, float]) -> float:
        return (a / b) if b else float("NaN")

    @staticmethod
    def percentage(a: Union[int, float], b: Union[int, float]) -> float:
        return ((a / b) * 100) if b else float("NaN")

    @staticmethod
    def change_percentage(a: Union[int, float], b: Union[int, float]) -> float:
        return (((a - b) / b) * 100) if b else float("NaN")

    @staticmethod
    def average(data: List[Union[int, float]]) -> float:
        return (sum(data) / len(data)) if data else float("NaN")

    @classmethod
    def variance(cls, data: List[Union[int, float]]) -> float:
        average = cls.average(data)
        return (
            (sum((x - average) ** 2 for x in data) / len(data))
            if data
            else float("NaN")
        )

    @classmethod
    def standard_deviation(cls, data: List[Union[int, float]]) -> float:
        return sqrt(cls.variance(data)) if data else float("NaN")

    @staticmethod
    def sum(data: List[Union[int, float]]) -> Union[int, float]:
        return sum(data) if data else 0

    @staticmethod
    def range(data: List[Union[int, float]]) -> float:
        return (max(data) - min(data)) if data else float("NaN")
