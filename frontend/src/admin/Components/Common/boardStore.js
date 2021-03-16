export default {
  data () {
    return {
      list: [],
      page: 1,
      total: 50 + Math.floor(Math.random() * 1000),
      pageLen: 10,
      loading: false,
      loadUri: 'http:/aaaa.com/notice/list'
    }
  },
  created () {
    this.load()
  },
  computed: {
    maxPage () {
      return Math.ceil(this.total / this.pageLen)
    }
  },
  methods: {
    load () {
      this.loading = true
      setTimeout(() => {
        const newList = []
        for (let i = 0; i < this.pageLen; i++) {
          const price = Math.floor(1500 * Math.random()) * 100
          const isDiscount = Math.random() < 0.2
          const discountRate = isDiscount ? Math.floor(30 * Math.random()) : 0
          newList.push({
            no: i + 1,
            checked: false,
            type: '등록상태',
            registDate: '2020-10-31 01:12:22',
            imgUrl: 'https://image.brandi.me/cproduct/2020/10/22/17893030_1603361920_image1_S.jpg',
            productName: '데니즈 세일러 카라 홈웨어 파자마 잠옷세트',
            productCode: 'SB000000000009044804',
            productNo: '17893030',
            sellerType: '쇼핑몰',
            sellerName: '울트라패션',
            salePrice: price,
            discountPrice: price - Math.floor(price * discountRate / 100),
            discountRate: discountRate,
            saleYn: '판매여부',
            exhibitYn: '진열여부',
            discountYn: isDiscount ? '할인' : '할인안함'
          })
        }
        this.loading = false
        this.list = newList
        // this.total = 550;
      }, 1000)
      // this.getPHP('/api/notice', {page:this.page}).
      //     then((res)=>{
      //         this.loading = false;
      //         this.list = res.data.list;
      //         this.total = res.data.total;
      // })
    },
    changePage (page) {
      console.log(page)
      this.page = page
      this.load()
    }
  },
  watch: {
    pageLen (v) {
      this.changePage(1)
    }
  }
}
