#!/bin/bash

docker run -i -v "$PWD":/code -w /code 'python:3.11.1' python main.py < input.txt
