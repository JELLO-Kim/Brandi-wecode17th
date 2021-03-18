import AdminApiMixin from '@/admin/mixins/admin-api'
import CommonMixin from '@/admin/mixins/common-mixin'
import errors from '@/admin/errors/errors'
import mockup from '@/admin/mockup/productList.json'
// import router from '@/router'
const ExpireTokenException = errors.ExpireTokenException
const TimeoutException = errors.TimeoutException

export default {
  mixins: [AdminApiMixin, CommonMixin],
  data () {
    return {
      list: [],
      page: 1,
      total: 0,
      pageLen: 10,
      loading: false,
      filter: {}
    }
  },
  props: {
    router: {
      default () {
        return null
      }
    }
  },
  created () {
    // this.load();
  },
  computed: {
    maxPage () {
      return Math.ceil(this.total / this.pageLen)
    },
    // 셀러 리스트 / 수정
    listUrl () {
      return this.constants.apiDomain + '/product/management'
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

      return new Promise((resolve, reject) => {
        // 아래는 테스트 코드
        // new Promise((_resolve, _reject)=>{
        //     setTimeout(()=>{
        //         // router.push('/')
        //         _reject(tokenExpireMockup())
        //     }, 300)
        // })
        new Promise((resolve, reject) => {
          setTimeout(() => {
            this.$emit('test', { a: 1 })
            resolve(listMockup())
          }, 300)
        })
        // 실제 연동은 아래
        // this.get(this.listUrl, {
        //     params: params
        // })
          .then((res) => {
            if (res.data && res.data.total_count !== undefined) {
              res.data.product_list.forEach((d) => {
                d.checked = false
              })
              const productList = res.data.product_list
              const totalCount = res.data.total_count
              this.total = totalCount
              this.list = productList
              resolve()
            } else {
              // eslint-disable-next-line prefer-promise-reject-errors
              reject('통신 실패')
            }
          }).catch((e) => {
            // TODO 타임아웃 처리를 공통으로 할 수 있을까?
            if (e.code === 'ECONNABORTED') {
              reject(new TimeoutException('요청 시간을 초과 하였습니다. 다시 시도해주시기 바랍니다.'))
            } else if (e.response && e.response.data.message === 'INVALID TOKEN') {
              reject(new ExpireTokenException('로그인이 만료 되었습니다. 다시 로그인 해주세요.'))
            } else {
              // eslint-disable-next-line prefer-promise-reject-errors
              reject('처리 중 오류 발생')
            }
          }).then((res) => {
            this.loading = false
          })
      })
    },
    getDetail () {

    },
    changePage (page) {
      this.page = page
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
