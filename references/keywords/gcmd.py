#!/usr/bin/env python3
from pandas import read_csv
smode = "/Users/jmcnelis/Projects/podaac-git.jpl.nasa.gov/data-publication-docs/smode-data-pub"

sk = read_csv(f"{smode}/gcmd/csv/sciencekeywords.csv", header=1)
skes = sk[sk.Category=='EARTH SCIENCE']
for Topic in [
    'ATMOSPHERE',
    'CLIMATE INDICATORS',
    'OCEANS',
    'PALEOCLIMATE',
    'SOLID EARTH',
    'SPECTRAL/ENGINEERING',
    'TERRESTRIAL HYDROSPHERE',
]:
    skes[skes.Topic==Topic].to_csv(f"{smode}/references/keywords/gcmd.sciencekeywords.earth_science.{Topic.lower().replace(' ', '_').replace('/', '_')}.csv")


instr = read_csv(f"{smode}/gcmd/csv/instruments.csv", header=1)
instrcat = instr[instr.Category.isin(['Earth Remote Sensing Instruments', 'In Situ/Laboratory Instruments'])]
for Class in [
    'Active Remote Sensing',
    'Passive Remote Sensing',
    'Chemical Meters/Analyzers',
    'Conductivity Sensors',
    #'Corers',
    'Current/Wind Meters',
    'Data Analysis',
    'Electrical Meters',
    'Gauges',
    'Magnetic/Motion Sensors',
    'Photon/Optical Detectors',
    'Pressure/Height Meters',
    #'Probes',
    'Profilers/Sounders',
    'Radiation Sensors',
    'Recorders/Loggers',
    'Samplers',
    'Spectrometers/Radiometers',
    'Temperature/Humidity Sensors',
]:
    instrcat[instrcat.Class==Class].to_csv(f"{smode}/references/keywords/gcmd.instruments.{Class.lower().replace(' ', '_').replace('/', '_')}.csv")
