from enum import Enum


class Indicator:
    class Average(Enum):
        SIMPLE = "Simple"
        EXPONENTIAL = "Exponential"
        SMOOTHED = "Smoothed"
