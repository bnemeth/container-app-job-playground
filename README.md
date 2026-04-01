## Unit teszt, és coverage:
```
uv run pytest --cov --cov-report=xml:coverage.xml
```
Ezt egyébként a beépített unit teszt is futtatja.

# Sonarqube
Tokent kell generálni a webes felületen.

Ezt a tokent tudod beállítani a github-ban secret environment változónak.

A [Sonarqube.io](https://sonarcloud.io/) -ba ki kell kapcsolni az automatic analysis method-ot.