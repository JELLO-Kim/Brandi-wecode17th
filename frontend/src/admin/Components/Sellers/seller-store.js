import store from '@/store/index'
import AdminApiMixin from '@/admin/mixins/admin-api'
import Message from '@/admin/utils/message'
import mockup from '@/admin/mockup/sellerList.json'

export default {
  store: store,
  mixins: [AdminApiMixin],
  data () {
    return {
      list: [],
      page: 1,
      total: 0,
      pageLen: 10,
      loading: false,
      filter: {},
      detailData: {}
    }
  },
  created () {
    this.load()
  },
  computed: {
    maxPage () {
      return Math.ceil(this.total / this.pageLen)
    },
    constants () {
      return this.$store.state.const
    },
    // 셀러 리스트 / 수정
    listUrl () {
      return this.constants.apiDomain + '/master/management-seller'
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

      new Promise((resolve, reject) => {
        setTimeout(() => {
          this.$emit('test', { a: 1 })
          resolve(listMockup())
        }, 300)
      })
      // this.get(this.listUrl, {
      //   params: params
      // })
        .then((res) => {
          if (res.data) {
            res.data.seller_list.forEach((d) => {
              d.checked = false
            })
            const sellerList = res.data.seller_list
            const totalCount = res.data.total_count
            this.total = totalCount
            this.list = sellerList
          } else {
            Message.error('통신 실패')
          }
        }).catch((e) => {
          if (e.code === 'ECONNABORTED') {
            Message.error('요청 시간을 초과 하였습니다. 다시 시도해주시기 바랍니다.')
          } else {
            Message.errors('처리 중 오류 발생')
          }
        }).then((res) => {
          this.loading = false
        })
    },
    changeStatus (sellerId, button) {
      this.loading = true
      const params = {
        seller_id: sellerId,
        button: button
      }
      this.put(this.listUrl, params)
        .then((res) => {
          if (res.data && res.data.message === 'success') {
            Message.success('셀러 상태 변경 성공')
            this.load()
          } else {
            Message.success('통신 실패')
          }
        })
        .catch((e) => {
          if (e.code === 'ECONNABORTED') {
            Message.error({
              content: '요청 시간을 초과 하였습니다. 다시 시도해주시기 바랍니다.'
            })
          } else {
            Message.error({
              content: '처리 중 오류 발생'
            })
          }
        }).then((res) => {
          this.loading = false
        })
    },
    getDetail (sellerId) {
      this.loading = true
      this.get(this.listUrl + '/' + sellerId)
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
    putDetail (sellerId, sellerData) {
      this.loading = true
      this.put(this.listUrl + '/' + sellerId, sellerData)
        .then((res) => {
          if (res.data && res.data.message === 'success') {
            Message.success('셀러 수정 성공')
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

function listMockup () {
  return mockup
}
