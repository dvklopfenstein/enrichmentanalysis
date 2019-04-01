"""Read IDs and associations from files."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein, H Tang. All rights reserved."
__author__ = "various"

import os
import sys
import numpy as np
import collections as cx


# https://docs.scipy.org/doc/numpy/user/basics.io.genfromtxt.html

def read_notfound(fin_txt, prt=sys.stdout):
    """Read Reactome Pathway Analysis file containing IDs that are not found."""
    rows = _read_genfromtxt(fin_txt, 'not found', str, prt)[1:]
    if len(rows) != 0:
        if isinstance(next(iter(rows)), np.ndarray):
            def _get_val(val):
                """Return ID as an int or a string."""
                return int(val) if val.isdigit() else val
            return [_get_val(v[0]) for v in rows]
        else:
            return [int(v) if v.isdigit() else v for v in rows]
    return []

def read_mapping(fin_csv, prt=sys.stdout):
    """Read Reactome Pathway Analysis file containing study IDs that are mapped."""
    rows = _read_genfromtxt(fin_csv, 'mapped   ', str, prt)
    if len(rows.shape) == 2:
        ntobj = cx.namedtuple('nt', [r.replace(' identifier', '') for r in rows[0]])
        # print('MMMMMMMMMMMMMMMM', ntobj._fields, rows[1])
        nts = [ntobj._make([int(v) if v.isdigit() else v for v in r]) for r in rows[1:]]
        # print(nts)
        return {nt.Submitted:nt for nt in nts}
    return {}

def _read_genfromtxt(fin_csv, desc, dtype, prt=sys.stdout):
    """Read Reactome Pathway Analysis file containing study IDs that are mapped."""
    if os.path.exists(fin_csv):
        ids = np.genfromtxt(fin_csv, dtype=dtype, delimiter=',', comments=None)
        if prt:
            prt.write('{N:4} IDs {DESC} WROTE: {CSV}\n'.format(
                N=len(ids), DESC=desc, CSV=fin_csv))
        return ids
    prt.write('   - IDs {DESC}    NO: {CSV}\n'.format(DESC=desc, CSV=fin_csv))
    return np.empty([0])

def read_ids(file_txt, sep=None):
    """Read study or population IDs. Return set of IDs."""
    if file_txt is None or not os.path.exists(file_txt):
        return {}
    ids = set()
    study_name = None
    with open(file_txt) as ifstrm:
        for line in ifstrm:
            if line[0] != '#' and line[:9] != 'Not found':
                lst = line.split(sep)
                if lst:
                    ids.add(lst[0])
            elif study_name is not None and line[0] == '#':
                study_name = line[1:].strip()
    ids = set(int(v) if v.isdigit() else v for v in ids)
    ret = {'ids':ids}
    msg = '  {N:6,} IDs READ: {FILE}'.format(N=len(ids), FILE=file_txt)
    if study_name is not None:
        ret['name'] = study_name
        msg += 'NAME({NAME})'.format(NAME=study_name)
    print(msg)
    return ret

def read_associations(assoc_fn):
    """
    Reads a gene id go term association file. The format of the file
    is as follows:

    AAR1	GO:0005575;GO:0003674;GO:0006970;GO:0006970;GO:0040029
    AAR2	GO:0005575;GO:0003674;GO:0040029;GO:0009845
    ACD5	GO:0005575;GO:0003674;GO:0008219
    ACL1	GO:0005575;GO:0003674;GO:0009965;GO:0010073
    ACL2	GO:0005575;GO:0003674;GO:0009826
    ACL3	GO:0005575;GO:0003674;GO:0009826;GO:0009965

    Also, the following format is accepted (gene ids are repeated):

    AAR1	GO:0005575
    AAR1    GO:0003674
    AAR1    GO:0006970
    AAR2	GO:0005575
    AAR2    GO:0003674
    AAR2    GO:0040029

    :param assoc_fn: file name of the association
    :return: dictionary having keys: gene id, values set of GO terms
    """
    assoc = cx.defaultdict(set)
    with open(assoc_fn) as ifstrm:
        for row in ifstrm:
            atoms = row.split()
            num_atoms = len(atoms)
            if num_atoms == 2:
                gene_id, go_terms = atoms
            elif num_atoms > 2 and row.count('\t') == 1:
                gene_id, go_terms = row.split("\t")
            else:
                continue
            gos = set(go_terms.split(";"))
            assoc[gene_id] |= gos
        print('  {N:6,} POPULATION IDs READ: {FILE}'.format(
            N=len(assoc), FILE=assoc_fn))
    return {p:es for p, es in assoc.items()}

def prepend(file_prefix, fout):
    """Prepend user-requested text to a filename."""
    if file_prefix is None:
        return fout
    fdir, fname = os.path.split(fout)
    return os.path.join(fdir, '{PRE}{FILE}'.format(PRE=file_prefix, FILE=fname))

def clean_args(args):
    """Clean keys: remove '-', '--', '<', '>'."""
    kws = {}
    for key, val in args.items():
        if key[0] == '-':
            key = key[1:]
        if key[0] == '-':
            key = key[1:]
        if key[0] == '<':
            key = key[1:]
        if key[-1] == '>':
            key = key[:-1]
        if val is not None:
            kws[key] = val
    return {k:v for k, v in kws.items() if v}

def get_fout_pdf(args):
    """Get the name of the pdf file where results are written."""
    if 'pdfname' in args:
        return args['pdfname']
    if 'pdf' in args and args['pdf']:
        return '{BASE}.pdf'.format(BASE=os.path.splitext(args['csv'])[0])
    raise RuntimeError('PDF FILENAME NOT SPECFIED')

def get_kws_analyse(args):
    """Get keyword args used when running a pathway analysis."""
    kws = {}
    if 'interactors' in args and args['interactors']:
        kws['interactors'] = True
    if 'excludeDisease' in args and args['excludeDisease']:
        kws['includeDisease'] = False
    return kws


# Copyright (C) 2018-2019, DV Klopfenstein, H Tang. All rights reserved.
