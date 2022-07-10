from inspect import signature


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Выводит информационное сообщение о тренировке."""

        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    CF_MIN: int = 60

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
        """Получить количество затраченных калорий."""

        pass

    def show_training_info(self) -> InfoMessage:
        """Преобразует объект класса Training в объект класса InfoMessage."""

        training_type = type(self).__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""

    CF_CAL_RUN_F: int = 18
    CF_CAL_RUN_S: int = 20

    def get_spent_calories(self):
        """Количество затраченных калорий"""

        return (self.CF_CAL_RUN_F * self.get_mean_speed()
                - self.CF_CAL_RUN_S) * (self.weight
                                        / self.M_IN_KM) * (self.duration
                                                           * self.CF_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CF_CAL_SW_F: int = 0.035
    CF_CAL_SW_S: int = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий"""

        return (self.CF_CAL_SW_F * self.weight
                + (self.get_mean_speed()**2 // self.height) * self.CF_CAL_SW_S
                * self.weight) * self.duration * self.CF_MIN


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CF_CAL_SWM_F: int = 1.1
    CF_CAL_SWM_S: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Рассчет средней скорости"""

        return (self.length_pool
                * self.count_pool) / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Рассчет потраченных калорий"""

        return (self.get_mean_speed()
                + self.CF_CAL_SWM_F) * self.CF_CAL_SWM_S * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    dict_workout_type = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in dict_workout_type.keys():
        raise KeyError(f'Ошибка: тип тренировки "{workout_type}" не обнаружен')
    if len(data) != (len(signature(dict_workout_type[workout_type])
                     .parameters)):
        raise ValueError(f'Ошибка: несоответствие кол-ва параметров '
                         f'тренировки "{workout_type}"')
    return dict_workout_type[workout_type](*data)


def main(training: Training) -> None:
    """Создать объект класса InfoMessage и вызвает информационное сообщение."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
