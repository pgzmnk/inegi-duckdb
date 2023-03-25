import sys

import duckdb
import geopandas as gpd
import pandas as pd
from shapely import wkt
from sqlalchemy import create_engine
from unidecode import unidecode

con = duckdb.connect()

def shapefile_to_parquet():
    """ Read shapefile, convert geometry column to string, write to parquet.
    """

    # Input arguments
    shapefile_path = sys.argv[1]
    output_path = sys.argv[2]

    # Process table, convert to `EPSG:4326 -- WGS84` which is the standard for Unfolded
    # Reference requirement: https://location.foursquare.com/studio/docs/data-formats#coordinate-reference-systems
    gdf = gpd.read_file(shapefile_path).to_crs(epsg=4326)

    # Clean up NOMGEO to strings safely encoded to ASCII
    if 'NOMGEO' in gdf.columns:
        gdf['NOMGEO'] = gdf.NOMGEO.apply(unidecode)

    # Geometry as string because Duckdb doesn't yet handle geometry type
    gdf['geometry_str'] = gdf.geometry.apply(lambda x: wkt.dumps(x))
    gdf.drop('geometry', inplace=True, axis=1)
    gdf.to_parquet(output_path, engine='auto', compression='snappy', index=None)
    # gdf.to_csv(output_path.replace('.parquet', '.csv'))

def str_to_geom():
    gdf['geometry'] = gdf.geometry_str.apply(wkt.loads)

def polyfill():
    import h3pandas
    gdf.h3.polyfill(8)


if __name__=="__main__":
    shapefile_to_parquet()