import csv
import numpy as np
import h5py
from quanter import ACGT_list
from scipy import sparse


class Matrix:

    def __init__(self, filename: str):
        f = open(filename, 'r')
        reader = csv.reader(f)

        data = []
        for i, row in enumerate(reader):
            if i == 0:
                # barcodes = row[:-1]
                # for j, barcode in enumerate(barcodes):
                #     barcodes[j] = str(barcode)+'AAAA-1'
                #
                # barcodes = [bytes(x, encoding="utf8") for x in barcodes]
                # self.barcodes = barcodes
                pass
            else:
                data.append(row)
        data = np.array(data)
        gene_name = data[:, 0]
        self.gene_id = self.__get_id(gene_name)

        gene_name = [bytes(x, encoding="utf8") for x in gene_name]

        self.matrix = np.array(data[:, 1:], dtype=np.int32)
        self.gene_name = np.array(gene_name)
        self.shape = np.array(self.matrix.shape)

        barcodes = ACGT_list(self.shape[1])
        barcodes = [bytes(x, encoding="utf8") for x in barcodes]

        self.barcodes = barcodes[:self.shape[1]]

        self.matrix = sparse.csc_matrix(self.matrix)
        self.data = self.matrix.data
        self.indices = self.matrix.indices
        self.indptr = self.matrix.indptr

        # under features
        self._all_tag_keys = np.array([b'genome', b'read', b'pattern', b'sequence'])
        self.feature_type = np.tile([b'Gene Expression'], self.shape[0])
        self.genome = np.tile([b'GRCh38'], self.shape[0])
        self.pattern = np.tile([b''], self.shape[0])
        self.read = np.tile([b''], self.shape[0])
        self.sequence = np.tile([b''], self.shape[0])
        self.id = self.gene_id
        self.name = self.gene_name

    def __get_id(self, genes):
        gene_id = []
        for i in range(len(genes)):
            gene_id.append('NA%i' % i)

        gene_id = np.array([bytes(x, encoding="utf8") for x in gene_id])
        return gene_id

    def save(self, filename: str):
        f = h5py.File(filename, 'w')

        f.attrs['chemistry_description'] = b"Single Cell 3' v3"
        f.attrs['filetype'] = 'matrix'
        f.attrs['library_ids'] = np.array([b'5k_pbmc_protein_v3'])
        f.attrs['original_gem_groups'] = np.array([1], dtype=np.int64)
        f.attrs['version'] = 2

        group = f.create_group('matrix')
        group.create_dataset(name='barcodes', data=self.barcodes)
        group.create_dataset(name='data', data=self.data, chunks=(80000,), compression='gzip', compression_opts=4,
                             shuffle=True)
        group.create_dataset(name='indices', data=np.array(self.indices, np.int64), chunks=(80000,), compression='gzip',
                             compression_opts=4, shuffle=True)
        group.create_dataset(name='indptr', data=np.array(self.indptr, np.int64), chunks=True, compression='gzip',
                             compression_opts=4, shuffle=True)
        group.create_dataset(name='shape', data=self.shape, chunks=True, compression='gzip', compression_opts=4,
                             shuffle=True)

        feature = group.create_group('features')
        feature.create_dataset(name='_all_tag_keys', data=self._all_tag_keys)
        feature.create_dataset(name='feature_type', data=self.feature_type)
        feature.create_dataset(name='genome', data=self.genome)
        feature.create_dataset(name='id', data=self.id)
        feature.create_dataset(name='name', data=self.name)
        feature.create_dataset(name='pattern', data=self.pattern)
        feature.create_dataset(name='read', data=self.read)
        feature.create_dataset(name='sequence', data=self.sequence)

        # f['/matrix/barcodes'] = self.barcodes
        # f['/matrix/data'] = self.data
        # f['/matrix/indices'] = np.array(self.indices, np.int64)
        # f['/matrix/indptr'] = np.array(self.indptr, np.int64)
        # f['/matrix/shape'] = self.shape
        #
        # f['/matrix/features/_all_tag_keys'] = self._all_tag_keys
        # f['/matrix/features/feature_type'] = self.feature_type
        # f['/matrix/features/genome'] = self.genome
        # f['/matrix/features/id'] = self.id
        # f['/matrix/features/name'] = self.name
        # f['/matrix/features/pattern'] = self.pattern
        # f['/matrix/features/read'] = self.read
        # f['/matrix/features/sequence'] = self.sequence

        f.close()


if __name__ == '__main__':
    matrix = Matrix('../data.csv')
    matrix.save('../filtered_feature_bc_matrix.h5')