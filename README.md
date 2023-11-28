# Fire Alarm System

## Test Fire Alarm Push Notificaiton

- Set Up PWA
  - Clone prototype branch of FireAlarmApp at https://github.com/Fire-Alarm-App/FireAlarmApp
  - Download dependencies
    - Install `bun-js` to your system
    - Use `bun` command to install all packages in `package.json`
  - Run `bun index.ts` to start the PWA on `http://127.0.0.1:3000/`
  - Open `http://127.0.0.1:3000/` in a browser
  - Open Web Dev Tools in browser
  - Click subscribe button on HTML page
  - Copy subscription information (`endpoint`, `keys` only) from browser console
- Set Up `Server.py`
  - Paste subscription inforamtion into the `sub` field in the `data` variable under `on_message()`
- Run `Server.py` first, then `FireAlarm.py` in two separate terminals

**Expected Behavior**

`FireAlarm.py` sends an MQTT Message to `Server.py` over the topic

`Server.py` uses the `on_message()` callback to send a POST request to `/notify` on the FireAlarmApp running in your browser (`http://127.0.0.1:3000/notify`)

A Push Notification sent to browser and raw JSON is printed to console that is running FireAlarmApp. 



