class FilterAddress:
    @staticmethod
    def remove_duplicates(address_list):
        return [address[0] for address in set(list(address_list))]

    @staticmethod
    def sort_area_by_priority(address_list):
        try:
            area_fooiy_priority = {
                "서울": 0,
                "경기": 1,
                "인천": 2,
                "부산": 3,
                "대전": 4,
                "대구": 5,
                "울산": 6,
                "세종": 7,
                "광주": 8,
                "강원": 9,
                "충북": 0,
                "충남": 10,
                "경북": 11,
                "전북": 12,
                "경남": 13,
                "전남": 14,
                "제주": 15,
            }
            return sorted(address_list, key=lambda x: area_fooiy_priority[x])
        except:
            address_list
