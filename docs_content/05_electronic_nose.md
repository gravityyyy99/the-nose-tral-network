# The electronic nose

*A real electronic nose is hardware. Ours is a carefully built imitation, designed so that the things that go wrong with real sensors go wrong here too.*

This chapter explains the simulated sensor array in `sensor.py`.

## What it is pretending to be

A real electronic nose has several gas sensors. Each is a small device whose electrical resistance changes when certain gases touch it. Different sensors react to different kinds of chemicals, so together they give a pattern.

In this project there are **8 virtual sensors**. They are computed, not physical.

## The 8 sensors

| # | Sensor | What it reacts to |
|---|---|---|
| 1 | Small and light | small, very volatile molecules |
| 2 | Large and heavy | big, slower-evaporating molecules |
| 3 | Oily / fatty | oil-loving molecules such as terpenes |
| 4 | Water-loving | polar molecules such as acids and alcohols |
| 5 | Oxygen-rich | aldehydes, ketones and esters |
| 6 | Sulfur | sulfur compounds (coffee, onion, garlic) |
| 7 | Aromatic rings | ring compounds such as phenols and vanillin |
| 8 | General gases | a broad response to almost anything |

## How a sniff is simulated

For each molecule, the program measures five simple properties with RDKit: molecular weight (size), how oil-loving it is (a number called logP), the number of oxygen atoms, the number of sulfur atoms, and how aromatic it is.

Each sensor has a weight for each property. For example, "Sulfur" cares mostly about sulfur atoms. A small random amount of cross-sensitivity is added, because real sensors are never perfectly selective. The sensor's response is then squashed into a range of roughly -1 to +1 with a `tanh` curve (real sensors also saturate).

## Making it realistic: noise and mess

Perfect readings would make the problem too easy, so every sniff includes:

- **Random concentrations**: each molecule is present in a different amount every time.
- **Humidity**: a random humidity level nudges some sensors, as it does on real gas sensors.
- **Sensor drift**: a small random gain change on all sensors.
- **Electrical noise**: random jitter on each reading.

This is why pressing Sniff twice gives slightly different bars.

## The numbers you see

The app shows each reading as a "reaction strength" from 0 to 100, which is just the raw reading rescaled for readability.

## Why this matters

The sensors never tell the nose model which molecules are present. They only give 8 numbers. Everything the nose model knows, it must work out from those 8 numbers alone. This is the same situation a real sensor puts you in.

## Why simulate first?

Real gas sensors take time to set up, drift as they age, and need carefully prepared samples. Building the whole pipeline on a simulation first meant the models, the app and the testing could all be built and checked before any hardware arrives. When the real device is ready, only the source of the eight numbers changes. Everything downstream stays the same.

> **The takeaway.** The simulation is deliberately messy, with noise, humidity and drift, so that whatever the nose model learns has to survive real-world mess.
