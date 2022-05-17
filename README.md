Got read names to analyze from Roger that are from ENCODE regions

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

samples = []
for ind, entry in df.iterrows():
    old = entry['File accession']+'.bam'
    # old = entry.hr
    samples.append(new)
    new = entry.hr+'.bam'
    os.rename(old, new)

with open('samples.txt', 'w') as ofile:
  for s in samples:
    ofile.write(s+'\n')
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

#Running TALON

## TALON label reads
```bash
ref=~/mortazavi_lab/ref/hg38/hg38.fa
while read s
do
    echo $s
    sam=${s}_subset.bam
    /usr/bin/time -l talon_label_reads \
        --f $sam \
        --g $ref \
        --t 1\
        --ar 20  \
        --deleteTmp  \
        --o $s
done < samples.txt 2> talon_label_reads.out
```

## TALON db initialization
```bash
annot=gencode.v40.annotation.encode_pilot_regions.gtf
/usr/bin/time -l talon_initialize_database \
  --f $annot \
  --g hg38 \
  --a gencode_v40 \
  --l 0 \
  --idprefix ENCODEH \
  --5p 500 \
  --3p 300 \
  --o h1 2> talon_init.out
```

## Create a TALON config file
```bash
cfg=talon_config.csv
touch ${cfg}
print "" > ${cfg}
while read s
do
  sam=${s}_labeled.sam
  printf "${s},${s},SequelII,${sam}\n">>${cfg}
done < samples.txt
```

## Run TALON
```bash
/usr/bin/time -l talon \
  --f ${cfg} \
  --db h1.db \
  --build hg38 \
  --t 8 \
  --o h1 2> talon.out
```

## Filter novel transcripts
```bash
db=h1.db
talon_filter_transcripts \
    --db $db \
    -a gencode_v40 \
    --maxFracA=0.5 \
    --minCount=5 \
    --minDatasets=2 \
    --o h1_pass_list.csv
```

## Create an unfiltered abundance, filtered abundance file, and gtf file
```bash
db=h1.db
talon_abundance \
    --db $db \
    -a gencode_v40 \
    -b hg38 \
    --o h1

talon_create_GTF \
  --db $db \
  -b hg38 \
  -a gencode_v40 \
  --whitelist h1_pass_list.csv \
  --o h1

talon_abundance \
  --db $db \
  -a gencode_v40 \
  -b hg38 \
  --o h1
```
