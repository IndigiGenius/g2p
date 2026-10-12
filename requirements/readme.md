All requirements for normal use are in `requirements.txt`.

The web stack behind the g2p studio and its API is in `requirements.studio.txt`, installed by the `studio` extra (`pip install g2p[studio]`). The library and the rest of the CLI don't need it.

We use a specific version of gunicorn to run the g2p studio in production, and don't want to introduce git as a dependency, so we separate these requirements here into `requirements.prod.txt`.

Requirements recommended for use during development but not needed for running g2p are separated into `requirements.dev.txt`.
