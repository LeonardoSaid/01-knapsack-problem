import itertools

class General:

    @staticmethod
    def kbits(n, k) -> list:
        result = []
        for bits in itertools.combinations(range(n), k):
            s = ['0'] * n
            for bit in bits:
                s[bit] = '1'
            result.append(''.join(s))
        return result

    @staticmethod
    def parse_item_list_data(item_list: list) -> tuple[list, list]:
        value_list = [item.value for item in item_list]
        weight_list = [item.weight for item in item_list]
        return (value_list, weight_list)

    @staticmethod
    def get_mask_list(n: int, distance: int, climb: bool = False) -> list:
        mask_list = []
        if climb:
            for i in range(1, distance + 1):
                mask_list += General.kbits(n, i)
        else:
            mask_list += General.kbits(n, distance)
        return mask_list