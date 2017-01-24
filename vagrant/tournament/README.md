Project: fullstack-nanodegree-vm
--------------------------------

Files:
------
     tournament.py - Contains code that implements tournament game 
                     functionality. 
     tournament.sql - Contains code to setup the database for tournament 
                     game.  
     tournament_test.py - Contains code to simulate/test the tournament 
                          game.

How to Run:
-----------
      Go to the folder fullstack-nanodegree-vm/vagrant/tournament then
      run the following in the command prompt in the vagrant machine.

        1. Database Setup
            i. psql
           ii. \i tournament.sql
          iii. \q

        2. Simulate the tournament game
          i. python tournament_test.py
