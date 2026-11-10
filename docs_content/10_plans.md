# Future plans

*A demonstration is only a beginning. This is where it goes next.*

The project as it stands is a working demonstration. This chapter sets out where it goes next.

## From simulation to a real electronic nose

At present the electronic nose is **simulated in code**. It shows how the whole pipeline fits together, but no physical sensor is involved.

The next major step is to build it with **real smelling devices**. The plan is to:

1. Connect a gas sensor, a good candidate being the **BME688**, which steps its heater through several temperatures so one chip gives several readings per cycle, to a small microcontroller such as an ESP32.
2. Record real smells in controlled conditions, in separate sessions on different days, with clean-air readings in between.
3. Replace the simulated readings with the real ones and retrain the same nose model.
4. Test it on a session the model has never seen, which is the honest measure of whether it works.
5. Publish the real results here, including the failures, and keep improving it.

Real sensors are noisier than the simulation, so the accuracy will start lower. Learning from that gap is the point of the exercise.

## A stronger smell model

The smell model is currently a random forest on chemical fingerprints. The research behind this project used a **graph neural network**, which learns directly from the atoms and bonds of a molecule. OpenPOM provides an open-source version that reported 0.89 ROC-AUC in its authors' tests. Moving to it is a planned upgrade.

## A harder, more honest test

- Hold out whole molecules and chemical families when testing, rather than splitting at random.
- Use larger, more realistic mixtures with many more molecules.
- Measure how repeatable the sensor readings are across sniffs and across days.

## New features

- Describe a smell in words and have the model suggest molecules that produce it.
- Compare readings from several sniffs of the same sample.
- Support more than two smell words in one query with clearer mixing.

These plans will be updated as the work progresses. The next chapter will hold the results of the real-device version once it exists.

> **The takeaway.** The goal is a real smelling device, tested honestly, with the results published here whether they are good or bad.
