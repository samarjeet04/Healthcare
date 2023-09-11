#HEALTHCARE




   def get_label_mapping_dict(self, element_types, inverse=False):

        if inverse == True:

            mapping_dict = {"0": "O"}

            for el_type in sorted(element_types):

                mapping_dict.update({str(max([int(i) for i in mapping_dict.keys()])+1): f'B-{el_type}',

                                    str(max([int(i) for i in mapping_dict.keys()])+2): f'I-{el_type}'})

        else:

            mapping_dict = {"O": 0}

            for el_type in sorted(element_types):

                mapping_dict.update({f'B-{el_type}': max(mapping_dict.values())+1,

                                    f'I-{el_type}': max(mapping_dict.values())+2})



        return mapping_dict
