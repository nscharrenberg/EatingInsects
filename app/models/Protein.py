from django.db import models


class Protein(models.Model):
    # Input Fields
    yield_um = models.DecimalField(decimal_places=2, max_digits=12)
    yield_ml = models.DecimalField(decimal_places=2, max_digits=12)
    calculated_mw = models.DecimalField(decimal_places=2, max_digits=12)
    calculated_pi = models.DecimalField(decimal_places=2, max_digits=12)
    sequence_length = models.BigIntegerField()
    sequence_mass = models.BigIntegerField()
    gene_product_type = models.TextField()

    # Output Field
    solubility = models.DecimalField(decimal_places=2, max_digits=12, null=True)

    # Miscellaneous Fields
    gene_name = models.TextField(null=True)
    cell_location = models.TextField(null=True)
    amino_acid_sequence = models.TextField()
    organism = models.TextField(null=True)

    def __str__(self):
        if not self.gene_name:
            return self.amino_acid_sequence
        else:
            return self.gene_name






