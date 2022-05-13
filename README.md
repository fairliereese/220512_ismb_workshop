Got read names to analyze from Roger that are from ENCODE regions.

* [Query for ENCODE data](https://www.encodeproject.org/search/?searchTerm=lrgasp&type=Experiment&assay_title=long+read+RNA-seq&replicates.library.biosample.donor.organism.scientific_name=Homo+sapiens&biosample_ontology.term_name=H1&biosample_ontology.term_name=endodermal+cell&files.platform.term_name=Pacific+Biosciences+Sequel+II&replicates.library.nucleic_acid_term_name=polyadenylated+mRNA)
* [ENCODE cart](https://www.encodeproject.org/carts/2a400711-709e-4167-a65a-4d1da2e4a4fc/)
* [Subset bam files](https://drive.google.com/drive/folders/1wRoUicPTH3-h6SeuUI7t23aFQ7A2RcWI?usp=sharing)
Download ENCODE data
```bash
xargs -L 1 curl -O -J -L < files.txt
```

Rename files
```python
import os
import pandas as pd

df = pd.read_csv('metadata.tsv', sep='\t')
m = {'endodermal cell': 'h1_de', 'H1': 'h1'}
df['hr'] = df['Biosample term name'].map(m)
df['biorep'] = df.groupby('hr').cumcount()+1
df['hr'] = df.hr+'_'+df.biorep.astype(str)

for ind, entry in df.iterrows():
    old = entry['File accession']+'.bam'
    # old = entry.hr
    new = entry.hr+'.bam'
    os.rename(old, new)
```

Cat all the zmw ids together
```bash
f=read_names.txt
echo "" >  $f
for zmw in *zmws
do
  cat $zmw >> $f
done
```

Subset based on the reads that we're using
```bash
for bam in *bam
do
  new_bam=${bam%.bam}_subset.bam
  samtools view -h -N $f $bam > $new_bam
done
```
