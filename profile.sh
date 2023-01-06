#!/bin/bash

docker run -i -v "$PWD/$1":/code -w /code 'python:3.11.1' sh -c 'python -u -m cProfile main.py < input.txt'
