#!/bin/sh

set -e

uvicorn app:app --host 0.0.0.0 --port 8002 --reload