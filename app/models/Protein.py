from django.db import models
import pandas as pd


class Protein(models.Model):
    # Input Fields
    yield_um = models.DecimalField(decimal_places=2, max_digits=12)
    yield_ml = models.DecimalField(decimal_places=2, max_digits=12)
    calculated_mw = models.DecimalField(decimal_places=2, max_digits=12)
    calculated_pi = models.DecimalField(decimal_places=2, max_digits=12)
    sequence_length = models.BigIntegerField()
    sequence_mass = models.BigIntegerField()
    gene_product_type = models.TextField(null=True)

    # Output Field
    solubility = models.DecimalField(decimal_places=2, max_digits=12, null=True)

    # Miscellaneous Fields
    gene_name = models.TextField()
    cell_location = models.TextField(null=True)
    amino_acid_sequence = models.TextField()
    organism = models.TextField(null=True)

    # AAPHY7
    steric_parameter = models.DecimalField(decimal_places=6, max_digits=12)
    polarizability = models.DecimalField(decimal_places=6, max_digits=12)
    volume = models.DecimalField(decimal_places=6, max_digits=12)
    hydrophobicity = models.DecimalField(decimal_places=6, max_digits=12)
    helix_probability = models.DecimalField(decimal_places=6, max_digits=12)
    sheet_probability = models.DecimalField(decimal_places=6, max_digits=12)

    def to_dict(self):
        return {
            'yield(uM)': float(self.yield_um),
            'Yield(ug/ml)': float(self.yield_ml),
            'Calculated MW(kDa)': float(self.calculated_mw),
            'Calculated pI': float(self.calculated_pi),
            'Sequence length': float(self.sequence_length),
            'Sequence mass': float(self.sequence_mass)
        }

    def to_dataFrame(self):
        df = pd.DataFrame(data=[
            [float(self.yield_um), float(self.yield_ml), float(self.calculated_mw), float(self.calculated_pi),
             float(self.sequence_length),
             float(self.sequence_mass)]], columns=['Yield(uM)', 'Yield(ug/ml)', 'Calculated MW(kDa)', 'Calculated pI',
                                                   'Sequence length', 'Sequence mass'])

        return df

    def __str__(self):
        if not self.gene_name:
            return self.amino_acid_sequence
        else:
            return self.gene_name
