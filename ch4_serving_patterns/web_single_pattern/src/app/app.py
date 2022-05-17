import os
from logging import getLogger

from fastapi import FastAPI
from src.app.routers import routers
from src.configurations import APIConfigurations