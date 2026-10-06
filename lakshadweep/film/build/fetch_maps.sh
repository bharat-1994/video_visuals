#!/bin/sh
# NASA GIBS imagery used by the film (public domain). Run from lakshadweep/film/
mkdir -p assets/maps && cd assets/maps
B="https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?SERVICE=WMS&REQUEST=GetMap&VERSION=1.1.1&STYLES=&FORMAT=image/jpeg&SRS=EPSG:4326"
H=HLS_S30_Nadir_BRDF_Adjusted_Reflectance
g() { curl -sS -m 180 -o "$1" "$B&LAYERS=$2${3:+&TIME=$3}&BBOX=$4&WIDTH=$5&HEIGHT=$6"; }
g world_bm.jpg BlueMarble_ShadedRelief_Bathymetry "" -180,-90,180,90 4096 2048
g trade_bm.jpg BlueMarble_ShadedRelief_Bathymetry "" 40,0,85,30 3200 2133
g bm_region.jpg BlueMarble_ShadedRelief_Bathymetry "" 60,0,90,28 2400 2240
g ridge_bathy.jpg BlueMarble_ShadedRelief_Bathymetry "" 66,4,78,16 2400 2400
g ridge_long.jpg BlueMarble_ShadedRelief_Bathymetry "" 64,-10,80,16 3000 4875
g mid_all_mo.jpg MODIS_Aqua_CorrectedReflectance_TrueColor 2023-03-10 70.5,7.5,75.5,12.5 4096 4096
g mid_north.jpg $H 2023-03-10 71.9,10.4,73.9,11.8 4096 2867
g mid_minicoy.jpg $H 2023-03-10 72.7,8.0,73.4,8.55 3200 2514
g mid_kalpeni.jpg $H 2023-03-10 73.3,9.8,74.0,10.35 3200 2514
g agatti_hls.jpg $H 2023-03-10 72.00,10.74,72.40,10.965 3200 1800
g kavaratti_hls.jpg $H 2023-03-10 72.45,10.46,72.85,10.685 3200 1800
g minicoy_hls.jpg $H 2023-03-10 72.85,8.17,73.25,8.395 3200 1800
g kalpeni_hls.jpg $H 2023-03-10 73.45,9.97,73.85,10.195 3200 1800
g bangaram_hls.jpg $H 2023-03-10 72.10,10.80,72.50,11.025 3200 1800
g kadmat_hls.jpg $H 2023-03-10 72.58,11.05,72.98,11.275 3200 1800
g ockhi_viirs3.jpg VIIRS_SNPP_CorrectedReflectance_TrueColor 2017-12-03 62,4,80,18 1800 1400
g ockhi_modis.jpg MODIS_Terra_CorrectedReflectance_TrueColor 2017-12-02 60,2,82,20 2200 1800
g hyd_night.jpg VIIRS_Black_Marble 2016-01-01 78.0,17.0,78.96,17.54 1920 1080
cd ../.. && python3 build/prep_maps.py && python3 build/match_layers.py
