import csv
import numpy as np
import pandas as pd
from scipy import sparse, io
from quanter import ACGT_list


class Data:

    def __init__(self, matrix_file, groups_file=None):
        f = open(matrix_file, 'r')
        reader = csv.reader(f)

        data = []
        for i, row in enumerate(reader):
            if i == 0:
                pass
            else:
                data.append(row)
        data = np.array(data)

        self.gene_name = data[:, 0]
        self.matrix = np.array(data[:, 1:], dtype=np.int32)
        self.shape = self.matrix.shape
        self.matrix = sparse.csc_matrix(self.matrix)
        self.barcodes = pd.DataFrame(ACGT_list(self.shape[1]))
        self.gene_id = self.__get_id(self.gene_name)
        self.feature_type = np.tile('Gene Expression', self.shape[0])
        self.gene = np.vstack((self.gene_name, self.feature_type))
        self.gene = np.vstack((self.gene_id, self.gene))
        self.gene = pd.DataFrame(self.gene.T)

    def __get_id(self, genes):
        gene_id = []
        for i in range(len(genes)):
            gene_id.append('NA%i' % i)

        gene_id = np.array(gene_id)
        return gene_id

    def save(self, path='data'):
        io.mmwrite(path + '/matrix.mtx', self.matrix)
        self.barcodes.to_csv(path + '/barcodes.tsv.gz', sep='\t', header=False, index=False)
        self.gene.to_csv(path + '/features.tsv.gz', sep='\t', header=False, index=False)


if __name__ == '__main__':
    data = Data('../data.csv')
    data.save()
    pass
