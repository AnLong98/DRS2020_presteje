# Introduction

Multiplayer turn-based snake game implementation in python PyQT5. Up to 4 players can run and play a game against each other on LAN network. Players can move their snakes with arrow keys, switch between snakes with tab key and eat food represented with blue and orange squares. Orange food will extend players snake by one part and add points, blue food will either give player a new adittional snake or punish him by imobllising his snake for a turn.

Game fully utilises computer hardware and network resources by separating tasks into different threads such as network receiving and network outgoing thread. Collision detection is separated into independent tasks performed by separate CPU cores running process instances from process pool.

Full documentation in Serbian available in Dokumentacija.pdf

## Technologies

- Python
- PyQT5

## How to run this?
 
 - Turn on your internet
 - Run server.py
 - Write down host and port for server and pass it to your firends
 - Run client.py on your local network computers and specify server host and port to which they should connect
 - Play

## Authors
Predrag Glavas, Stefan Besovic, Stefan Djurovic, Jelena Beader

## License
[MIT](https://choosealicense.com/licenses/mit/)
