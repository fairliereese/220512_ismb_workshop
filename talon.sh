# symlink all bams to current directory
ln -s ../data/PacBio/03_alignments/*bam .

# create samples file
touch samples.txt
printf "" > samples.txt
for f in *bam
do
  b=`basename $f .bam`
  printf "${b}\n" >> samples.txt
done

# ref=~/mortazavi_lab/ref/hg38/hg38.fa
ref=../data/reference/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta
while read s
do
    echo $s
    sam=${s}.bam
    talon_label_reads \
        --f $sam \
        --g $ref \
        --t 1 \
        --ar 20  \
        --deleteTmp  \
        --o $s
done < samples.txt

annot=../data/reference/gencode.v40.annotation.encode_pilot_regions.gtf
talon_initialize_database \
  --f $annot \
  --g hg38 \
  --a gencode_v40 \
  --l 0 \
  --idprefix ENCODEH \
  --5p 500 \
  --3p 300 \
  --o h1

cfg=talon_config.csv
touch ${cfg}
printf "" > ${cfg}
while read s
do
  sam=${s}_labeled.sam
  printf "${s},${s},SequelII,${sam}\n">>${cfg}
done < samples.txt

talon \
  --f ${cfg} \
  --db h1.db \
  --build hg38 \
  --t 8 \
  --o h1

db=h1.db
talon_filter_transcripts \
    --db $db \
    -a gencode_v40 \
    --maxFracA=0.5 \
    --minCount=5 \
    --minDatasets=2 \
    --o h1_pass_list.csv

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
