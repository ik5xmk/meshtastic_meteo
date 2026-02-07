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

The mt_meteo_pws program has the same functionality as sending messages to the meshtastic network, but retrieves data from the Wunderground website. This can be useful if you're publishing data from your own weather station. The API key (from your account) and the weather station ID are required. You can specify by editing the code whether to manage the connection via serial or TCP, the meshtastic channel on which to send the data, and the name of the location where the pws is located. The script can be automated via cron (Linux) or scheduled tasks (Windows).<br>

![](https://github.com/ik5xmk/meshtastic_meteo/blob/main/output_lora_meshtastic_meteo_pws.jpg)<br>
<br>
![](https://github.com/ik5xmk/meshtastic_meteo/blob/main/output_lora_meshtastic_meteo_pws_dos.jpg)<br>

For more information:<br>
https://t.me/Reti_LoRaAPRS_Meshcom_Meshtastic<br>
https://www.wunderground.com/<br>
https://open-meteo.com/<br>
