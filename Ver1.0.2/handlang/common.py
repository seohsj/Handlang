class SignLanguage:

    #알파벳 모델 라벨 리스트
    _alphabet_label_list=["A", "B", "C", "D", "E", "F", "G",
             "H", "I", "K", "L", "M", "N", "O", "P", "Q",
            "R", "S", "T", "U", "V", "W", "X", "Y",
            "del", "nothing", "space"]
    #실제 사이트에서 사용할 지문자 리스트
    __alphabet_letter_list=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o',
                      'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y']
    

    #숫자 모델 라벨 리스트
    _number_label_list=["0","1","2","3","4","5","6","7","8","9","del", "nothing", "space"]

    #실제 사이트에서 사용할 지문자 리스트
    __number_letter_list=['0','1','2','3','4','5','6','7','8','9']
    
    
    @classmethod
    def get_label(cls, group ,idx):
        try:
            if group=="alphabet":
                 ret=cls._alphabet_label_list[idx]
            elif group=="number":
                ret=cls._number_label_list[idx]
            else:
                raise Exception('잘못된 group 입니다.')
        except IndexError as e:
            print(e)
        return ret

    @classmethod
    def get_letter_list(cls, group):
        if group=="alphabet":
            return cls.__alphabet_letter_list
        elif group=="number":
            return cls.__number_letter_list
        else:
            raise Exception('잘못된 group 입니다.')

            
    




