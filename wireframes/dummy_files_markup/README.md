# NOTES.md

## Notes

* All markups prefixed with underscores `_` are still being revised -- i.e. they are in a preliminary state.
* The name of the file is an option for `source` global attribute. I think I remember you said you wanna drop that attribute entirely across all datasets. That's cool, too.
* `coverage_content_type` reference: https://wiki.esipfed.org/ISO_19115-3_Codelists#MD_CoverageContentTypeCode
  * generally, all variables currently labeled with `coordinate` for `coverage_content_type` standard attribute should be changed to `referenceInformation` *if they do not explicitly, completely label a dimension.*
* Here's a reference to the corresponding NCEI template for each product, where applicable (https://www.nodc.noaa.gov/data/formats/netcdf/v2.0/):
  * [S-MODE_PFC_surfacedrifter_##.nc.cdl](wireframes/dummy_files_markup/S-MODE_PFC_surfacedrifter_##.nc.cdl): *trajectory*
  * [S-MODE_PFC_slocumglider_##.nc.cdl](wireframes/dummy_files_markup/S-MODE_PFC_slocumglider_##.nc.cdl): *trajectoryProfile* (pretty confident, this is currently `trajectory`)
  * [#](#): ...
* CF Standard Name description for `sea_water_practical_salinity`: 
  
  ```
  "Practical Salinity, S_P, is a determination of the salinity of sea water, based on its electrical conductance. The measured conductance, corrected for temperature and pressure, is compared to the conductance of a standard potassium chloride solution, producing a value on the Practical Salinity Scale of 1978 (PSS-78). This name should not be used to describe salinity observations made before 1978, or ones not based on conductance measurements. Conversion of Practical Salinity to other precisely defined salinity measures should use the appropriate formulas specified by TEOS-10. Other standard names for precisely defined salinity quantities are sea_water_absolute_salinity (S_A); sea_water_preformed_salinity (S_*), sea_water_reference_salinity (S_R); sea_water_cox_salinity (S_C), used for salinity observations between 1967 and 1977; and sea_water_knudsen_salinity (S_K), used for salinity observations between 1901 and 1966. Salinity quantities that do not match any of the precise definitions should be given the more general standard name of sea_water_salinity. Reference: www.teos-10.org; Lewis, 1980 doi:10.1109/JOE.1980.1145448."
  ```

## Broadly applicable guidance/comments

* Include the auxiliary coordinate variables and optionally coordinate variables in the list. The order itself does not matter. Also, note that whenever any auxiliary coordinate variable contains a missing value, all other coordinate, auxiliary coordinate and data values corresponding to that element should also contain missing values. (`coverage_content_type = "relatedInformation" ;`)
* No need to use `scale_factor` of 1.0 and `add_offset` of 0.0. May even lead to unnecessary computation. **Use these if you are packing the data.**

## Questions/Comments

### lagrangian float

* Float depth is measured at the top and bottom of the float by two CTDs for every point along the time dimension. What are the appropriate metadata (standard names, attributes) to describe this observation/context?
  * `depth_bnds`? But that implies coordinate bounds, whereas `depth` is a coordinate describing vertical position along the time dimension.
  * I don't think that's accurate use. But there may not be a specification for this.

### surface drifter

* Recommend adding another dimension `trajectory` to support native netCDF aggregation with other trajectories from other files.
  * *if it's not inconvenient to the data needs/requirements for S-MODE science*
* In this case, `latitude` and `longitude` are NOT coordinates in the strict netCDF4 software sense, so they can have `_FillValue`s if there's true potential for missing values in the data.
  * If you assign `valid_min` and `valid_max`, also assign a `_FillValue` (double verify).
* Could optionally stack the temperature variables using another indexing dim (length 2); maybe requires a transpose.

### ctd

* Consider labeling the `temperature` and `temperature2` like `temperature_uctd` or **putting the measurements from the two types of CTD in separate groups.**

### lagrangianfloat

What's different between these two? Where do `depth` data come from?

```python
	double ctd_depth(ctd, time) ;
		ctd_depth:instrument = "2 Sea-Bird Scientific SBE 41 CTD units at top and bottom of float" ;
		ctd_depth:long_name = "Depth at the two CTD units" ;
		ctd_depth:valid_max = 200., 200. ;
		ctd_depth:valid_min = 0., 0. ;
		ctd_depth:axis = "Z" ;
		ctd_depth:positive = "down" ;
		ctd_depth:standard_name = "depth" ;
		ctd_depth:units = "m" ;
		ctd_depth:coverage_content_type = "referenceInformation" ;
	double depth(time) ;
		float_depth:instrument = "2 Sea-Bird Scientific SBE 41 CTD units at top and bottom of float" ;
		float_depth:long_name = "Depth at the float center" ;
		float_depth:valid_max = 200. ;
		float_depth:valid_min = 0. ;
		float_depth:axis = "Z" ;
		float_depth:positive = "down" ;
		float_depth:standard_name = "depth" ;
		float_depth:units = "m" ;
		float_depth:coverage_content_type = "referenceInformation" ;
```

## notes

Asorted notes about platforms/instruments from discussions with Fred and Susannah:

* lagrangian float
  * somewhat like an ARGO float, doesn't go nearly as deep
  * drifting wherever the current take it
  * CTD on top and bottom, moving vertically while the sampling takes place
* adcp
  * mounted on the bottom of the ship, putting out a ping of sound that measures the profiles of velocity every few minutes
  * velocity measured in regularly spaced bins
* drifter data from SPURS
  * drifter_id variable
  * each measurement was associated with a prticular drifter_id
  * https://podaac-opendap.jpl.nasa.gov/opendap/allData/insitu/L2/spurs2/drifter/SPURS2_SVP_Drifter.nc.html
* seaglider
  * moves xyz; x, y and z are recorded for each time interval
  * depth is reference information
  * latitude, longitude, depth bounds (dive)
  * data variables (time)
  * dive coordinate variable (time)
  * dives approximately ~1000m
* slocumglider
  * doesn't dive as deep as the seaglider
  * dives approximately ~100-200m
  * (follow seaglider)
* waveglider
  * two CTD streams
    * CTD mounted at the surface underneath the "sailboard"
    * CTD mounted about 6 meters below the sailboard
