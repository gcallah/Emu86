export user_type="test"
export test_dir="tests"
export ignores="(utils|selenium_tests)"

if [ -z "$1" ]; then
	export capture=""
else
	export capture="--nocapture"
fi

nosetests --ignore-files=$ignores --exe --verbose --with-coverage --cover-package=assembler $capture
# nosetests --ignore-files=$ignores --exe --collect-only --verbose --with-coverage $capture
