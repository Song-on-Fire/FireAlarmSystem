# Prototype Set Up

## Fire Alarm App Set Up

The Fire Alarm App is a Progressive Web Application for users to easily interface with their Smart Fire Alarm. To set up the Fire Alarm App: 
- Clone prototype branch of FireAlarmApp at https://github.com/Fire-Alarm-App/FireAlarmApp
- Download dependencies from `package.json` with `bun install`
- Run `bun index.ts` to start the PWA on `http://127.0.0.1:3000/`
- Open `http://127.0.0.1:3000/` in a browser

## Fire Alarm System Set Up

Ensure all dependencies are installed, then in the `src` folder, run `python3 Server.py`

If you have a Smart Fire Alarm running, a push notification should appear on the system running the PWA. 

## If you do NOT have a Smart Fire Alarm

You may simulate one using the deprecated `FireAlarm.py` in the `src`. Open another terminal process and run `python3 FireAlarm.py` **after** running the `Server.py` process. 

Again, you should expect a push notification to appear on the system running the PWA. 