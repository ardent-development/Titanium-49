# clean.sh: Removes build artifacts
# Run from within src to clean

rm -rfv CMakeFiles
rm -rfv generated
rm -rfv pico-sdk
rm -rfv pioasm
rm -rfv pioasm-install
rm -rfv cmake_*
rm -rfv CMakeCache.txt
rm -rfv Makefile
rm -rfv t49_*
rm -rfv pico_*