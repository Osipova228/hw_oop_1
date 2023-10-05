from dataclasses import dataclass
import json


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR = 60

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
        raise NotImplementedError('Невозможно обратиться напрямую.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return (((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed())
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    MSEC_IN_KMH: float = 0.278
    SM_IN_M: float = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.MSEC_IN_KMH) ** 2
                   / (self.height / self.SM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_WEIGHT_MULTIPLIER: int = 2
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    package = {'RUN': Running,
               'SWM': Swimming,
               'WLK': SportsWalking}
    if workout_type not in package:
        raise NotImplementedError('Ключ не найден в словаре.')
    return package[workout_type](*data)


try:
    with open('data.json', 'r') as json_file:
        loaded_data = json.load(json_file)
except FileNotFoundError:
    print("Файл 'data.json' не найден.")
except json.JSONDecodeError:
    print("Ошибка при чтении данных из файла 'data.json'."
          "Неверный формат JSON.")


# Создаем список объектов тренировки
training_data = [
    Running(1000, 30, 70),
    SportsWalking(8000, 60, 65, 175),
    Swimming(50, 45, 75, 25, 5)
]

# Преобразуем данные в формат JSON
json_data = []
for training in training_data:
    json_data.append({
        'type': training.__class__.__name__,
        'duration': training.duration,
        'distance': training.get_distance(),
        'mean_speed': training.get_mean_speed(),
        'calories': training.get_spent_calories()
    })

# Сохраняем данные в JSON-файл
with open('data.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

# Считываем данные из JSON-файла
try:
    with open('data.json', 'r') as json_file:
        loaded_data = json.load(json_file)
except FileNotFoundError:
    print("Файл 'data.json' не найден.")
except json.JSONDecodeError:
    print("Ошибка при чтении данных из файла 'data.json'."
          "Неверный формат JSON.")

# Добавляем новые данные в loaded_data
new_training = {
    'type': 'Running',
    'duration': 45,
    'distance': 10.5,
    'mean_speed': 7.0,
    'calories': 400
}

loaded_data.append(new_training)

# Записываем обновленные данные обратно в JSON-файл
with open('data.json', 'w') as json_file:
    json.dump(loaded_data, json_file, indent=4)
