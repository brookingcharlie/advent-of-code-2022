#!/bin/bash

docker run -v "$PWD/$1":/code -w /code 'python:3.11.1' sh -c 'python -B -m unittest test.Test'
