    #map new fields to fields in NHGIS csv
    new={
        "total_vacant"  :"MTEE001"
        ,"for_rent"     :"MTEE002" 
        ,"for_sale"     :"MTEE004"    
        ,"other_vacant" :"MTEE008" 
        ,"total_own"    :"MU6E001" 
        ,"total_rent"   :"MUTE001" 
        }
#map new fields to fields in NHGIS csv
new={
     "mdeianincome"    :"HF6001"      
 }

# raw csv
raw="/Users/slow/workspace/choropleth-maps/data/raw/nhgis/ca_blockgroups/misc.csv"

new={
     "total"    :"JNRE001"      
    ,"householdswchildren" :"JNRE002" 
 }

# raw csv
raw="/Users/slow/workspace/choropleth-maps/data/raw/nhgis/ca_blockgroups/age.csv"


convert(new,raw)
