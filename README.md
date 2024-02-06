# Catalogue_Color_Sampler
Sample sources from the full catalogue according to AGN colors

The code takes the sources from the full catalogue according
to the color distribution of the AGN sample catalogue.

The catalogues should have the following columns (but this
can be easily modified):
'ID_Real'
'Redshift_Real'
'Stellar_Mass
'Flux_Real'
'Luminosity_Real'
'Alpha_Real'
'Color'


Two folders are required for the code to work:
1) Input : Folder contains the catalogues and the
           redshift bin edges (given in an example).
2) Output : Folder for the resulting sdample and the
            histograms used for a "sanity check".
