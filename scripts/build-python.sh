#! /usr/bin/env sh

rm -rf build dist *.egg-info
rm -rf packaging/python/build packaging/python/dist packaging/python/*.egg-info
python -m build

mv -f build packaging/python/
mv -f dist packaging/python/
mv -f *.egg-info packaging/python/
