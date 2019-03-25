"""Read IDs and associations from files."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein, H Tang. All rights reserved."
__author__ = "various"

import os
import collections as cx


def read_ids(file_txt):
    """Read study or population IDs. Return set of IDs."""
    ids = set()
    study_name = None
    if not os.path.exists(file_txt):
        return ids
    with open(file_txt) as ifstrm:
        for line in ifstrm:
            if line[0] != '#':
                lst = line.split()
                if lst:
                    ids.add(lst[0])
            elif study_name is not None:
                study_name = line[1:].strip()
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


# Copyright (C) 2018-2019, DV Klopfenstein, H Tang. All rights reserved.
