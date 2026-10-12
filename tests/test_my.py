import pytest
from conftest import load

# Завантажуємо модуль задачі 5
M = load(5)

# Напрямки для Набору 3 (відновлення бази)
DIR_RECOV = {
    "rpo_min": "min",
    "rto_min": "min",
    "cost": "min",
}

# Тестові дані на основі кейсу 3 (data/case_3_recovery.json)
RECOV_OPTIONS = {
    "Х: щодобова копія": {"rpo_min": 1440, "rto_min": 120, "cost": 15},
    "Ү: щогодинна копія": {"rpo_min": 60, "rto_min": 90, "cost": 30},
    "Z: потокова реплікація": {"rpo_min": 1, "rto_min": 10, "cost": 120},
}


@pytest.mark.parametrize("options, directions, expected_front", [
    # Випадок 1 (S3): Базові варіанти відновлення — усі три є Парето-оптимальними
    (
        RECOV_OPTIONS,
        DIR_RECOV,
        ["Х: щодобова копія", "Ү: щогодинна копія", "Z: потокова реплікація"],
    ),
    # Випадок 2 (S3): Варіант-переможець T домінує всі інші
    (
        {
            "Х: щодобова копія": {"rpo_min": 1440, "rto_min": 120, "cost": 15},
            "Ү: щогодинна копія": {"rpo_min": 60, "rto_min": 90, "cost": 30},
            "T: ідеальне відновлення": {"rpo_min": 0, "rto_min": 0, "cost": 0},
        },
        DIR_RECOV,
        ["T: ідеальне відновлення"],
    ),
    # Випадок 3 (S3): Рівні вектори (дублікати не домінують один одного)
    (
        {
            "Y1: копія вузол 1": {"rpo_min": 60, "rto_min": 90, "cost": 30},
            "Y2: копія вузол 2": {"rpo_min": 60, "rto_min": 90, "cost": 30},
        },
        DIR_RECOV,
        ["Y1: копія вузол 1", "Y2: копія вузол 2"],
    ),
])
def test_my_pareto_front_s3(options, directions, expected_front):
    assert M.pareto_front(options, directions) == expected_front


@pytest.mark.parametrize("options, directions, expected_explain", [
    # Випадок 4 (S3): Перевірка функції explain для набору відновлення
    (
        {
            "Ү: щогодинна копія": {"rpo_min": 60, "rto_min": 90, "cost": 30},
            "W: застаріла копія": {"rpo_min": 120, "rto_min": 90, "cost": 35},
        },
        DIR_RECOV,
        {"W: застаріла копія": ["Ү: щогодинна копія"]},
    ),
])
def test_my_explain_s3(options, directions, expected_explain):
    assert M.explain(options, directions) == expected_explain