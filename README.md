# Minecraft translation tools

A small collection of python scripts I've made to make translation of minecraft lang files easier. Nothing too complex, just scripts that seemed useful to me.

---
## Empty fix
Fills empty entry for the translation key using it's name.

## Lang merger
Merges two lang json files into one by appending missing translation keys in the target file with ones in the source file.

## Lang statistic
Checks and prints statistic about translated files of specified language code (like en_us) in the dir. Also writes info into output file.

## Tips localise
A simple script for making multiple json files, containing text for the Tips minecraft mod, localisable by changing text to translation keys and generating a lang file (en_us.json). Change the BASENAME variable in the script to the whatever you need.

## Translation tool
Small cli program for editing minecraft lang files.
