import pandas as pd

ab_df = pd.read_csv('h1_talon_abundance_filtered.tsv', sep='\t')

df = pd.read_csv('metadata.tsv', sep='\t')
m = {'endodermal cell': 'h1_de', 'H1': 'h1'}
df['hr'] = df['Biosample term name'].map(m)
df['biorep'] = df.groupby('hr').cumcount()+1
df['hr'] = df.hr+'_'+df.biorep.astype(str)

keep_cols = ['annot_transcript_id']
dataset_cols = []
for ind, entry in df.iterrows():
    hr = entry.hr
    fname = entry['File accession']
    ab_df.rename({hr:fname},axis=1, inplace=True)
    keep_cols.append(fname)
    dataset_cols.append(fname)

# get TPM
ab_df = ab_df[keep_cols]
for d in dataset_cols:
    ab_df['sum'] = ab_df[d].sum(axis=0)
    ab_df[d] = (ab_df[d]*1000000)/ab_df['sum']

ab_df.drop('sum', axis=1, inplace=True)
ab_df.rename({'annot_transcript_id': 'ID'}, axis=1, inplace=True)
