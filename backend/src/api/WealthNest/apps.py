from django.apps import AppConfig
import csv
import os
from django.conf import settings

class WealthNestConfig(AppConfig):
    name = 'WealthNest'

    data = []
