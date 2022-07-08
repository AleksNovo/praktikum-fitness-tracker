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

        return(f'Тип тренировки: {self.training_type};'
               f' Длительность: {self.duration:.3f} ч.;'
               f' Дистанция: {self.distance:.3f} км;'
               f' Ср. скорость: {self.speed:.3f} км/ч;'
               f' Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

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

        return self.count_calor()

    def show_training_info(self) -> InfoMessage:
        """Преобразует объект класса Training в объект класса InfoMessage."""

        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""

    def count_calor(self):
        """Количество затраченных калорий"""

        cff_cal_1 = 18
        cff_cal_2 = 20
        return (cff_cal_1 * self.get_mean_speed()
                - cff_cal_2) * self.weight / self.M_IN_KM * self.duration * 60


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

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

    def count_calor(self) -> float:
        """Количество затраченных калорий"""

        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        return (coeff_calorie_1 * self.weight
                + (self.get_mean_speed()**2 // self.height) * coeff_calorie_2
                * self.weight) * self.duration * 60


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

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

    def count_calor(self) -> float:
        """Рассчет потраченных калорий"""

        coeff_cal_1 = 1.1
        coeff_cal_2 = 2
        return (self.get_mean_speed()
                + coeff_cal_1) * coeff_cal_2 * self.weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type == 'SWM':
        action, duration, weight, length_pool, count_pool = data
        return Swimming(action, duration, weight, length_pool, count_pool)
    if workout_type == 'RUN':
        action, duration, weight = data
        return Running(action, duration, weight)
    if workout_type == 'WLK':
        action, duration, weight, height = data
        return SportsWalking(action, duration, weight, height)


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
