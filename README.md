# Alignment of French Crop Usage with TAXREF-LD

This project contains different experiments meant to align the [French Crop Usage](http://ontology.irstea.fr/pmwiki.php/Site/FrenchCropUsage) theaurus (FCU) with [TAXREF-LD](https://github.com/frmichel/taxref-ld/), the Linked Data representation of the french taxonomic registry, [TAXREF](https://inpn.mnhn.fr/programme/referentiel-taxonomique-taxref?lg=en).

One experiment favors alignments precision (fewer alignments with better precision), while the other favors recall (more alignments with potentially more false positives).

In both cases, 3 methods are run separately and intermediate results and then merged:
- Method 1: direct lowercase exact match of FCU crop names with TAXREF-LD vernacular names.
- Method 2: use the [GEVES](https://www.geves.fr/) catalog of seeds as an intermediary source
    - lowercase exact match of FCU crop names with GEVES seed names, and get the corresponding scientific names. Remark: GEVES registers lowercase scientific names with the authority but not the date, e.g.: *prunus armeniaca l.* instead of the proper full scientific name *Prunus armeniaca L., 1753*;
    - lowercase substring match of GEVES name with the full scientific name of TAXREF-LD.
- Method 3: use the [EPPO Global Database](https://gd.eppo.int/) as an intermediary source
    - use the EPPO API to match FCU crop names with EPPO codes, and get the corresponding full scientific names;
    - lowercase exact match of EPPO full scientific names with TAXREF-LD full scientific names.

The tables below give, for each experiment "precision" or "recall", the results of each method in terms of number of FCU crops aligned with TAXREF-LD taxa. Column "Intermediate source" means GEVES in method 2 and EPPO in method 3.

## Algorithm tuned for precision

Results: 651 alignments of 300 FCU concepts with 579 taxa

| Alignment method   | FCU concepts | Intermediate source | TAXREF-LD taxa | Taxonomic ranks |
| :-- |       :--:   |         :--: |           :--: | :--: |
| 1. FCU name `-exact string match->` TAXREF-LD vernacular name | 161 | | 369 | species, subspecies, varietas, forma, cultivar |
| 2. FCU name `-exact string match->` GEVES name `->` GEVES scientific name with authority `-substring match->` TAXREF-LD full scientific name | 64 | 57  | 57 | species, subspecies |
| 3. FCU name `-API match->` EPPO code `->` EPPO scientific name with authority/date `-exact string match->` TAXREF-LD full scientific name | 266 | 306 | 315 | species, subspecies, varietas, forma, cultivar |


## Algorithm tuned for recall

Results: 710 alignments of 337 FCU concepts with 609 taxa

| Alignment method   | FCU concepts | Intermediate source | TAXREF-LD taxa | Taxonomic ranks |
| :-- |       :--:   |         :--: |           :--: | :--: |
| 1. FCU name `-exact string match->` TAXREF-LD vernacular name | 174 | | 385 | species, subspecies, varietas, forma, cultivar |
| 2. FCU name `-exact string match->` GEVES name `->` GEVES scientific name with authority `-substring match->` TAXREF-LD full scientific name | 81 | 78  | 70 | species, subspecies |
| 3. FCU name `-API match->` EPPO code `->` EPPO scientific name with authority/date `-exact string match->` TAXREF-LD full scientific name | 300 | 326 | 336 | species, subspecies, varietas, forma, cultivar |


## License

Data files (csv, ttl, xlsx) are made available under the terms of the [Open Data Commons Attribution License v1.0](https://opendatacommons.org/licenses/by/1-0/) (ODC-By-1.0) license.

The code used to produce the data files, provided within Jupyter Notebooks, is licensed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).
