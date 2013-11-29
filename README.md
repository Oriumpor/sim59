sim59
=====

Meridian59 1v1 Simulator


This project aims to  simulate a stand up battle between two Meridian59 players.  

Dependencies: 
http://matplotlib.org/

* Player A always swings first (to reflect the typical combat style of getting jumped)
* The Offense (tohit) calculation isn't implemented you have to enter it manually in the config file per run.
* Player B has a unique parameter (piSimulatorRange.)  This is used to determine the hitpoint range to test against during simulation.  Player B's statistics are fixed, but the hitpoints iterate up to the range maximum plus the starting hitpoints.
