# meshtastic_meteo
Code to send weather messages to a specific meshtastic node or channel<br>
<br>
Written in Python, this code allows you to send weather messages (data retrieved from Open Meteo) to a LoRa board equipped with Meshtastic firmware. The board can be reached via serial/USB or network.<br>

You must have Python installed, and any libraries that can be installed via pip.<br>
Edit the code in the CONFIGURATION section, enter the communication port or network address:port. Then complete the code with the coordinates of the location you're interested in data from (you can choose any of these; see Open Meteo), and specify the meshtastic node (in the form !nnnnnnnn) to receive the information (or all of them), and the channel present in your board configuration.<br>

Nothing else is needed; run it by prefixing it with the python command.<br>

![](https://github.com/ik5xmk/meshtastic_meteo/blob/main/meshtastic_meteo.jpg)<br>
<br>
![](https://github.com/ik5xmk/meshtastic_meteo/blob/main/messaggio_ricevuto.jpg)<br>

For more information:<br>
https://www.loraitalia.it/<br>
https://meshtastic.org/<br>
https://open-meteo.com/<br>
