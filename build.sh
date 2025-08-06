#!/bin/bash
rm -rf build/ dist/

pyinstaller --onefile --noconsole \
    --add-data "assets:assets" \
    --name "SpaceshipGame" \
    main.py

chmod +x dist/SpaceshipGame

echo -e "\n\033[1;32mSUCCESS!\033[0m Executable is in dist/"
echo "Run with: ./dist/SpaceshipGame"
