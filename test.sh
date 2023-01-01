#!/bin/bash

docker run -v "$PWD/$1":/code -w /code 'python:3.11.1' sh -c 'python -u -B -m unittest test.Test'
