import board
import analogio
import adafruit_thermistor
import audiobusio

import array
import time
import math

light = analogio.AnalogIn(board.LIGHT)
thermistor = adafruit_thermistor.Thermistor(
    board.TEMPERATURE, 10000, 10000, 25, 3950)


def mean(values):
    return sum(values) / len(values)


def normalized_rms(values):
    minbuf = int(mean(values))
    sum_of_samples = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )

    return math.sqrt(sum_of_samples / len(values))


mic = audiobusio.PDMIn(
    board.MICROPHONE_CLOCK,
    board.MICROPHONE_DATA,
    sample_rate=16000,
    bit_depth=16
)
samples = array.array('H', [0] * 160)
mic.record(samples, len(samples))


while True:
    print("L:", light.value)
    print("T:", thermistor.temperature)

    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    print("S:", magnitude)

    time.sleep(5)
