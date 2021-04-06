import AdminApiMixin from '@/admin/mixins/admin-api'
import CommonMixin from '@/admin/mixins/common-mixin'
import store from '@/store/index'
import Message from '@/admin/utils/message'
// import mockup from '@/admin/mockup/orderList.json'

export default {
  store: store,
  mixins: [AdminApiMixin, CommonMixin],
  data () {
    return {
      list: [],
      page: 1,
      total: 0,
      pageLen: 50,
      loading: false,
      filter: {},
      detailData: {},
      sellerAttribute: []
    }
  },
  created () {
    this.getMeta()
  },
  computed: {
    prefixUrl () {
      if (this.isMaster()) {
        return this.constants.apiDomain + '/master'
      } else {
        return this.constants.apiDomain + '/seller'
      }
    },
    maxPage () {
      return Math.ceil(this.total / this.pageLen)
    },
    constants () {
      return this.$store.state.const
    },
    // 주문 리스트
    listUrl () {
      return this.prefixUrl + '/order/ready'
    },
    // 주문 상세 / 수정
    detailUrl () {
      return this.prefixUrl + '/order'
    },
    // 셀러 리스트 / 수정
    metaUrl () {
      return this.prefixUrl + '/order/ready/init'
    },
    // 배송처리
    deliveryUrl () {
      return this.prefixUrl + '/order/ready/'
    },
    offset () {
      return (this.page - 1) * this.pageLen
    },
    checkedList () {
      const newList = []
      this.list.forEach(d => { if (d.checked) newList.push(d) })
      return newList
    }
  },
  methods: {
    load () {
      this.loading = true
      const params = JSON.parse(JSON.stringify(this.filter))
      params.limit = this.pageLen
      params.offset = this.offset

      // new Promise((resolve, reject) => {
      //   setTimeout(() => {
      //     this.$emit('test', { a: 1 })
      //     resolve(listMockup())
      //   }, 300)
      // })
      this.get(this.listUrl, {
        params: params
      })
        .then((res) => {
          const orderList = res.data.result.data
          orderList.forEach((d) => {
            d.checked = false
          })
          this.total = res.data.result.totalCount
          this.list = orderList
        }).catch((e) => {
          if (e.code === 'ECONNABORTED') {
            Message.error('요청 시간을 초과 하였습니다. 다시 시도해주시기 바랍니다.')
          } else {
            console.log(e)
            Message.error('처리 중 오류 발생')
          }
        }).then((res) => {
          this.loading = false
        })
    },
    getDetail (orderNo) {
      this.loading = true
      this.get(this.detailUrl + '/' + orderNo)
        .then((res) => {
          if (res.data) {
            this.detailData = res.data.result.data.orderDetails
          } else {
            Message.error('통신 실패')
          }
        }).catch((e) => {
          if (e.code === 'ECONNABORTED') {
            Message.error('요청 시간을 초과 하였습니다. 다시 시도해주시기 바랍니다.')
          } else {
            Message.error('처리 중 오류 발생')
          }
        }).then((res) => {
          this.loading = false
        })
    },
    changePage (page) {
      this.page = page
      this.load()
    },
    setFilter (filter) {
      this.filter = filter
    },
    getMeta () {
      this.get(this.metaUrl)
        .then((res) => {
          if (res.data) {
            this.sellerAttribute = res.data.result.data.sellerAttribute
          } else {
            Message.error('통신 실패')
          }
        }).catch((e) => {
          if (e.code === 'ECONNABORTED') {
            Message.error('요청 시간을 초과 하였습니다. 다시 시도해주시기 바랍니다.')
          } else {
            Message.error('처리 중 오류 발생')
          }
        }).then((res) => {
          // this.loading = false
        })
    },
    async setDelivery (list) {
      if (list.length > 0) {
        try {
          for (let i = 0, len = list.length; i < len; i++) {
            await this.patch(this.deliveryUrl + list[i].orderDetailNumber)
          }
          Message.success('배송처리가 완료되었습니다.')
          this.load()
        } catch (e) {
          Message.error(e.response.data.message)
        }
      }
      // 배송처리
      // /master/order/ready/<order_id>
      // {
      //    "message": "updated",
      //    "result": "PATCH"
      // }
    }
  },
  watch: {
    pageLen (v) {
      this.changePage(1)
    }
  }
}
