"""Module containing models representing patients and their data.

The Model layer is responsible for the 'business logic' part of the software.

Patients' data is held in an inflammation table (2D array) where each row contains
inflammation data for a single patient taken over a number of days
and each column represents a single day across all patients.
"""

import numpy as np
from functools import reduce


def load_csv(filename):
    """Load a Numpy array from a CSV

    :param filename: Filename of CSV to load
    """
    return np.loadtxt(fname=filename, delimiter=',')


def daily_mean(data):
    """Calculate the daily mean of a 2D inflammation data array.

    :param data: A 2D data array with inflammation data (each row
    contains measurements for a single patient across all days).

    :returns: An array of mean values of measurements for each day.
    """
    return np.mean(data, axis=0)


def daily_max(data):
    """Calculate the daily max of a 2D inflammation data array.

    :param data: A 2D data array with inflammation data (each row
    contains measurements for a single patient across all days).
    :returns: An array of max values of measurements for each day.
    """
    return np.max(data, axis=0)


def daily_min(data):
    """Calculate the daily min of a 2D inflammation data array.

    :param data: A 2D data array with inflammation data (each row
    contains measurements for a single patient across all days).
    :returns: An array of min values of measurements for each day.
    """
    return np.min(data, axis=0)


def patient_normalise(data):
    """
    Normalise patient data from a 2D inflammation data array.

    Any NaN values are ignored, and normallised to 0.

    :param data: 2D array of inflammation data
    :type data: ndarray
    """
    if not isinstance(data, np.ndarray):
        raise TypeError('data input should be ndarray')
    if len(data.shape) != 2:
        raise ValueError('inflammation array should be 2-dimensional')
    if np.array(data < 0):
        raise ValueError('Inflammation values should not be negative')

    max_data = np.nanmax(data, axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        normalised = data / max_data[:, np.newaxis]
    normalised[np.isnan(normalised)] = 0
    return normalised


def daily_above_threshold(patient_num, data, threshold):
    """Count how many days a given patient's inflammation exceeds a given threshold.

    :param patient_num: The patient row number
    :param data: A 2D data array with inflammation data
    :param threshold: An inflammation threshold to check each daily value against
    :returns: An integer representing the number of days a patient's inflammation is over a given threshold
    """

    above_threshold = map(lambda x: x > threshold, data[patient_num])
    return reduce(lambda a, b: a + 1 if b else a, above_threshold, 0)



class Observation:
    def __init__(self, day, value):
        self.day = day
        self.value = value

    def __str__(self):
        return self.value


class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Patient(Person):
    """A patient in an inflammation study."""
    def __init__(self, name, observations=None):
        super().__init__(name)

        self.observations = []
        if observations is not None:
            self.observations = observations

    def add_observation(self, value, day=None):
        if day is None:
            try:
                day = self.observations[-1].day + 1

            except IndexError:
                day = 0

        new_observation = Observation(day, value)

        self.observations.append(new_observation)
        return new_observation

