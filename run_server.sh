currentdir=$(pwd)
if [[ $PYTHONPATH != *"$currentdir"* ]]; then
  export PYTHONPATH=$currentdir:$PYTHONPATH
fi
if [[ $PYTHONPATH != *"$currentdir/Submodules"* ]]; then
  export PYTHONPATH=$currentdir/Submodules:$PYTHONPATH
fi
echo $PYTHONPATH
python bbb_test_runner/TestRunnerManager.py
