@echo off
rem call miniconda.bat to activate base python env
set PYTHONPATH=%CD%
echo "PYTHONPATH = %PYTHONPATH%"
echo "running python %*"
python %*

