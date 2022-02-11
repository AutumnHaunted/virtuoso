How to run the program:
----------------------------
1. Install all of the fonts in the "fonts" directory.

2. Make sure your desired cards are in the "cards.ods" spreadsheet.

3. Run "ods-to-json.py". (This will require you to have Python installed, as well as the module "pyexcel_ods".)

4. Open the GIMP, and under "Edit/Preferences/Folders/Plug-ins", add the folder "gimp-virtuoso" to the list.

5. A "Virtuoso" option should now be added to the "File" tab. (You may need to restart the GIMP.)

6. You can generate a single card, a series of cards, a set of cards, or all cards.

7. In the field, '"Virtuoso" project directory', navigate to this folder. (For future reference, you may want to favorite this folder.)

8. Fill out the remaining fields as you desire, and then click "OK".

An observation: There may be an issue in which the GIMP does not dispose of data after it has been used. To avoid high memory usage, close the GIMP after generating a large series of cards.

--------------------

Also supplied is the script, "convert-a-deck.py". (This script has the same dependencies as "ods-to-json.py".) Running this script will allow you to convert decks made using the old run of Virtuoso cards into the new cards. Card information will also be added automatically. The script can be used on both individual JSON files as well as directories. (By default, Tabletop Simulator saves objects in "Documents/My Games/Tabletop Simulator/Saves/Saved Objects". A backup of the original files will also be saved.