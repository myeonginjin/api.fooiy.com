from django.db.models import F, Case, When
from django.db.models.functions import Abs

##### Shop 오브젝트에서만 사용 가능 #####
# 개인 푸이티아이 점수와 매장 푸이티아이 점수 비교 쿼리
def personalize_fooiyti(account):
    try:
        account_fooiyti = str(account.fooiyti).lower()
        account_e = int(getattr(account, f"fooiyti_e_percentage", 0))
        account_i = int(getattr(account, f"fooiyti_i_percentage", 0))
        account_s = int(getattr(account, f"fooiyti_s_percentage", 0))
        account_n = int(getattr(account, f"fooiyti_n_percentage", 0))
        account_t = int(getattr(account, f"fooiyti_t_percentage", 0))
        account_f = int(getattr(account, f"fooiyti_f_percentage", 0))
        account_a = int(getattr(account, f"fooiyti_a_percentage", 0))
        account_c = int(getattr(account, f"fooiyti_c_percentage", 0))
        fooiyti = account_fooiyti + "_score"
        fooiyti_ei = Case(
            When(
                shopfooiyti__e_percentage__gte=F("shopfooiyti__i_percentage"),
                then=Abs(account_e - F("shopfooiyti__e_percentage")) / 4,
            ),
            default=Abs(account_i - F("shopfooiyti__i_percentage")) / 4,
        )
        fooiyti_sn = Case(
            When(
                shopfooiyti__s_percentage__gte=F("shopfooiyti__n_percentage"),
                then=Abs(account_s - F("shopfooiyti__s_percentage")) / 4,
            ),
            default=Abs(account_n - F("shopfooiyti__n_percentage")) / 4,
        )
        fooiyti_tf = Case(
            When(
                shopfooiyti__t_percentage__gte=F("shopfooiyti__f_percentage"),
                then=Abs(account_t - F("shopfooiyti__t_percentage")) / 4,
            ),
            default=Abs(account_f - F("shopfooiyti__f_percentage")) / 4,
        )
        fooiyti_ac = Case(
            When(
                shopfooiyti__a_percentage__gte=F("shopfooiyti__c_percentage"),
                then=Abs(account_a - F("shopfooiyti__a_percentage")) / 4,
            ),
            default=Abs(account_c - F("shopfooiyti__c_percentage")) / 4,
        )
        personalize_fooiyti = Case(
            When(
                shopfooiyti__feed_count__gte=3,
                then=100 - fooiyti_ei - fooiyti_sn - fooiyti_tf - fooiyti_ac,
            ),
            default=F(f"shopscore__{fooiyti}"),
        )
        return personalize_fooiyti
    except:
        return F("shopscore__score")
