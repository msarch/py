This repository contains the (optimized) code from [this](http://stackoverflow.com/questions/14885349/how-to-implement-a-particle-engine/14892607#14892607) StackOverflow answer.

It uses `numpy`, `itertools` and `pygame.surfarray` and eschews the `random` module for massive speed improvement.

![in-game screenshot](https://bitbucket.org/BigYellowCactus/particlegame/downloads/img.jpg)

(Here's an example using three emitters to create smoke, rain, and wind)