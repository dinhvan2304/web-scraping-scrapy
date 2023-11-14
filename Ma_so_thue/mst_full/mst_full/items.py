from attr import field
from scrapy import Item, Field


class MstFullItem(Item):
    url             = Field()
    ten_cong_ty     = Field()
    ten_viet_tat    = Field()
    mst             = Field()
    dia_chi         = Field()
    dien_thoai      = Field()
    nghanh_nghe     = Field()
    ten_quoc_te     = Field()
    nguoi_dai_dien  = Field()
    ngay_hoat_dong  = Field()
    quan_ly_boi     = Field()
    loai_hinh_DN    = Field()
    tinh_trang      = Field()

    

