currentdir=$(pwd)
if [[ $PYTHONPATH != *"$currentdir"* ]]; then
  export PYTHONPATH=$currentdir:$PYTHONPATH
fi
if [[ $PYTHONPATH != *"$currentdir/Submodules"* ]]; then
  export PYTHONPATH=$currentdir/Submodules:$PYTHONPATH
fi
echo $PYTHONPATH

result=$(pgrep python3)
echo $result
if [ -z "$result" ]; then
	echo "Running Server"
	python3 bbb_test_runner/TestRunnerManager.py > /dev/null &
else
	echo "Server is Already Running"
fi
exit
