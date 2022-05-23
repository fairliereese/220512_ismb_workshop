import swan_vis as swan

annot = 'gencode.v40.annotation.encode_pilot_regions.gtf'
gtf = 'h1_talon.gtf'
ab = 'h1_talon_abundance.tsv'

sg = swan.SwanGraph()
sg.add_annotation(annot)
sg.add_transcriptome(gtf)
sg.add_abundance(ab)

sg.save_graph('swan')

# add metadata
sg.adata.obs.head()
meta = sg.adata.obs.copy(deep=True)
meta['cell_type'] = meta.dataset.str.rsplit('_', n=1, expand=True)[0]

meta = meta[['dataset', 'cell_type']]
meta.to_csv('swan_metadata.tsv', sep='\t', index=False)
meta = 'swan_metadata.tsv'
sg.add_metadata(meta)

# add colors for h1 and h1_de
c_dict = {'h1': 'darkorchid', 'h1_de': 'darkgoldenrod'}
sg.set_metadata_colors('cell_type', c_dict)

sg.save_graph('swan')

# intron retention and exon skipping
es_df = sg.find_es_genes(verbose=False)
ir_df = sg.find_ir_genes(verbose=False)

ir_df.head()

# inspect a gene with IR and ES
sg.plot_graph('ENSG00000203879.12', indicate_novel=True)

# inspect a gene with IR and ES
sg.plot_graph('ENSG00000203879.12', indicate_novel=True)

sg.plot_transcript_path('ENCODEHT000013762', indicate_novel=True)

es_df.head()

sg.plot_graph('ENSG00000143398.20', indicate_novel=True)

sg.plot_transcript_path('ENCODEHT000005453', indicate_novel=True)

sg.plot_transcript_path('ENCODEHT000005453', indicate_novel=True)

sg.plot_transcript_path('ENCODEHT000005453', browser=True)

# differential expression tests
sg = swan.read('swan.p')

obs_col = 'cell_type'
degs = sg.de_gene_test(obs_col)

dets = sg.de_transcript_test(obs_col)

die, results = sg.die_gene_test(obs_col=obs_col, verbose=True)

die_df = sg.get_die_genes(obs_col=obs_col,
                          obs_conditions=['h1', 'h1_de'],
                          p=0.05, dpi=10)

def make_reports(gname):
  sg.gen_report(gname,
                'figures/'+gname,
                metadata_cols=['cell_type'],
                cmap='viridis',
                transcript_col='tname',
                novelty=True,
                indicate_novel=True,
                layer='tpm')

  sg.gen_report(gname,
                'figures/'+gname,
                metadata_cols=['cell_type'],
                cmap='magma',
                transcript_col='tname',
                novelty=True,
                layer='pi',
                browser=True)

make_reports('DES')
make_reports('POGZ')
make_reports('PI4KB')

sg.plot_transcript_path('ENCODEHT000006801', indicate_novel=True)

sg = swan.read('swan.p')

sg.t_df.loc[sg.t_df.tid == 'ENCODEHT000006801']

sg.plot_each_transcript_in_gene('PI4KB', 'figures/pi4kb', indicate_novel=True)
