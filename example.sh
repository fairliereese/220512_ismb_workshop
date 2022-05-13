threads=64

pbmm2 align \
    --preset ISOSEQ \
    --sort \
    -j $threads \
    $HOME/refs/hg38.fa \
    h1_combined.fastq.gz \
    h1_combined.aligned.bam

samtools view \
    -L /pbi/dept/appslab/datasets/rv_ismb_2022/from_ana/encode_1_regions_hg38.bed \
    h1_combined.aligned.bam \
    >h1_combined_encode1.sam
samtools view \
    -L /pbi/dept/appslab/datasets/rv_ismb_2022/from_ana/encode_1_regions_extended_hg38.bed \
    h1_combined.aligned.bam \
    >h1_combined_encode1_extended.sam

cat h1_combined_encode1.sam | cut -d'	' -f1 | sort | uniq >h1_combined_encode1.zmws
cat h1_combined_encode1_extended.sam | cut -d'	' -f1 | sort | uniq >h1_combined_encode1_extended.zmws
