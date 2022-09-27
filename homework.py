from dataclasses import dataclass
from typing import ClassVar, Dict, List, Type


@dataclass(frozen=True)
class InfoMessage:
    """Информационное сообщение о тренировке. """
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:0.3f} ч.; '
                f'Дистанция: {self.distance:0.3f} км; '
                f'Ср. скорость: {self.speed:0.3f} км/ч; '
                f'Потрачено ккал: {self.calories:0.3f}.'
                )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    MINUTES_IN_HOUR: ClassVar[int] = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:

        raise NotImplementedError('Определите ф-ю в наследнике')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    KCAL_RUN_1: ClassVar[int] = 18
    KCAL_RUN_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.KCAL_RUN_1 * self.get_mean_speed()
                - self.KCAL_RUN_2) * self.weight / self.M_IN_KM
                * (self.duration * self.MINUTES_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    KCAL_SPWALK_1: ClassVar[float] = 0.035
    MEAN_SPEED_POW: ClassVar[int] = 2
    KCAL_SPWALK_3: ClassVar[float] = 0.029

    def __init__(self, action: int, duration: float, weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (self.KCAL_SPWALK_1 * self.weight
                + (self.get_mean_speed() ** self.MEAN_SPEED_POW // self.height)
                * self.KCAL_SPWALK_3
                * self.weight) * self.duration * self.MINUTES_IN_HOUR


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    KCAL_SWIMM_1: ClassVar[float] = 1.1
    KCAL_SWIMM_2: ClassVar[int] = 2

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed()
                + self.KCAL_SWIMM_1) * self.KCAL_SWIMM_2 * self.weight


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    kind_of_sport: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in kind_of_sport:
        raise KeyError(f'{workout_type} does not supported.'
                       f'Try{kind_of_sport.keys()}')
    return kind_of_sport[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('DIVE', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
