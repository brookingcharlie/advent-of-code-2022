#!/bin/bash

docker run -i -v "$PWD/$1":/code -w /code 'python:3.11.1' sh -c 'python main.py < input.txt'
