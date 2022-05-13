Got read names to analyze from Roger that are from ENCODE regions.

* [Query for ENCODE data](https://www.encodeproject.org/search/?searchTerm=lrgasp&type=Experiment&assay_title=long+read+RNA-seq&replicates.library.biosample.donor.organism.scientific_name=Homo+sapiens&biosample_ontology.term_name=H1&biosample_ontology.term_name=endodermal+cell&files.platform.term_name=Pacific+Biosciences+Sequel+II&replicates.library.nucleic_acid_term_name=polyadenylated+mRNA)
* [ENCODE cart]()
Download ENCODE data
```bash
xargs -L 1 curl -O -J -L < files.txt
```
