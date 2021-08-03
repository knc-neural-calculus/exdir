import sys


def test_import():
	# TODO: actually integrate this test with everything
	sys.path.append('..')
	import exdir.utils.serialize as serialize
	print(serialize.AVAILIBLE_MODES)
	print(serialize.MODE)
	# assert serialize.MODE == "yaml"

	import serializer_mode
	print(serialize.AVAILIBLE_MODES)
	print(serialize.MODE)
	# assert serialize.MODE == "yaml"

if __name__ == '__main__':
	test_import()