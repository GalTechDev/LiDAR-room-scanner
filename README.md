# LiDAR room scanner
 Projer pour scanner une piece avec un capteur LiDAR

## Représentation de l'espace avec des relevées d'angles horisontales, vertical et la distance
### Formules :
Soit `h` l'angle horisontal en radian, `v` l'angle vertical en radian, `d` la distance entre le capteur de position `(0,0,0)` et un object.

Un point `P` de coordonés `(x, y, z)` avec :
- x = d.cos(h)
- y = d.sin(h)
- z = d.sin(v)
