import pytest
from pytest import approx
from water_flow import (
    water_column_height, pressure_gain_from_water_height,
    pressure_loss_from_pipe, pressure_loss_from_fittings,
    reynolds_number, pressure_loss_from_pipe_reduction,
    kpa_to_psi
)

def test_water_column_height():
    assert approx(water_column_height(0, 0)) == 0
    assert approx(water_column_height(20, 0)) == 20
    assert approx(water_column_height(0, 10)) == 7.5
    assert approx(water_column_height(10, 10)) == 17.5
    assert approx(water_column_height(100, 50)) == 137.5

def test_pressure_gain_from_water_height():
    assert approx(pressure_gain_from_water_height(0)) == 0
    assert approx(pressure_gain_from_water_height(36.6), abs=0.01) == 358.27732
    assert approx(pressure_gain_from_water_height(10), abs=0.01) == 97.88998
    assert approx(pressure_gain_from_water_height(50), abs=0.01) == 489.44990
    assert approx(pressure_gain_from_water_height(100), abs=0.01) == 978.8998

def test_pressure_loss_from_pipe():
    assert approx(pressure_loss_from_pipe(0.048692, 100, 0.018, 1.65), abs=0.1) == -50.230829
    assert approx(pressure_loss_from_pipe(0.28687, 100, 0.013, 1.65), abs=0.1) == -6.157631
    assert approx(pressure_loss_from_pipe(0.28687, 200, 0.013, 1.65), abs=0.1) == -12.315262
    assert approx(pressure_loss_from_pipe(0.048692, 50, 0.018, 1.75), abs=0.1) == -28.25195
    assert approx(pressure_loss_from_pipe(0.28687, 50, 0.013, 1.75), abs=0.1) == -3.463314

def test_pressure_loss_from_fittings():
    assert approx(pressure_loss_from_fittings(1.65, 0)) == 0.0000
    assert approx(pressure_loss_from_fittings(1.65, 2), abs=0.001) == -0.1090
    assert approx(pressure_loss_from_fittings(1.75, 2), abs=0.001) == -0.1220
    assert approx(pressure_loss_from_fittings(1.75, 5), abs=0.001) == -0.3060
    assert approx(pressure_loss_from_fittings(1.65, 1), abs=0.001) == -0.0545

def test_reynolds_number():
    assert approx(reynolds_number(0.048692, 1.65), abs=1) == 80069.10
    assert approx(reynolds_number(0.048692, 1.75), abs=1) == 84922.10
    assert approx(reynolds_number(0.28687, 1.65), abs=1) == 471729.10
    assert approx(reynolds_number(0.28687, 1.75), abs=1) == 500318.10
    assert approx(reynolds_number(0.048692, 0.001), abs=1) == 48.625

def test_pressure_loss_from_pipe_reduction():
    assert approx(pressure_loss_from_pipe_reduction(0.28687, 0.001, 48.692, 0.048692), abs=0.01) == 0.0000
    assert approx(pressure_loss_from_pipe_reduction(0.28687, 1.65, 471729.10, 0.048692), abs=0.1) == -163.744
    assert approx(pressure_loss_from_pipe_reduction(0.28687, 1.75, 500318.10, 0.048692), abs=0.1) == -184.182
    assert approx(pressure_loss_from_pipe_reduction(0.1, 1, 100000, 0.05), abs=0.1) == -0.752
    assert approx(pressure_loss_from_pipe_reduction(0.2, 2, 200000, 0.1), abs=0.1) == -3.002

def test_kpa_to_psi():
    assert approx(kpa_to_psi(0)) == 0
    assert approx(kpa_to_psi(100), abs=0.01) == 14.5038
    assert approx(kpa_to_psi(158.7), abs=0.01) == 23.0197706
    assert approx(kpa_to_psi(50), abs=0.01) == 7.2519
    assert approx(kpa_to_psi(200), abs=0.01) == 29.0076

if __name__ == "__main__":
    pytest.main(["-v", "--tb=line", "-rN", __file__])
