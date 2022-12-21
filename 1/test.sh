#!/bin/bash

docker run -v "$PWD":/code -w /code 'python:3.11.1' python -m unittest main.Test
