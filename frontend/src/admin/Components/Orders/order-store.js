import AdminApiMixin from '@/admin/mixins/admin-api'
import store from '@/store/index'
import Message from '@/admin/utils/message'

export default {
  store: store,
  mixins: [AdminApiMixin],
  data () {
    return {
      list: [],
      page: 1,
      total: 0,
      pageLen: 50,
      loading: false,
      filter: {},
      detailData: {}
    }
  },
  created () {
    // this.load();
  },
  computed: {
    maxPage () {
      return Math.ceil(this.total / this.pageLen)
    },
    constants () {
      return this.$store.state.const
    },
    // 주문 리스트
    listUrl () {
      return this.constants.apiDomain + '/order/status'
    },
    // 주문 상세 / 수정
    detailUrl () {
      return this.constants.apiDomain + '/order'
    },
    offset () {
      return (this.page - 1) * this.pageLen
    }
  },
  methods: {
    load () {
      this.loading = true
      const params = JSON.parse(JSON.stringify(this.filter))
      params.limit = this.pageLen
      params.offset = this.offset
      this.get(this.listUrl + '/' + this.filter.status_id, {
        params: params
      })
        .then((res) => {
          if (res.data && res.data.total_count !== undefined) {
            res.data.order_list.forEach((d) => {
              d.checked = false
            })
            this.total = res.data.total_count
            this.list = res.data.order_list
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
    getDetail (orderNo) {
      this.loading = true
      this.get(this.detailUrl + '/' + orderNo)
        .then((res) => {
          if (res.data) {
            this.detailData = res.data
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
    }
  },
  watch: {
    pageLen (v) {
      this.changePage(1)
    }
  }
}
