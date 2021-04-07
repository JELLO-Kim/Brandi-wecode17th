import AdminApiMixin from '@/admin/mixins/admin-api'
import CommonMixin from '@/admin/mixins/common-mixin'
import errors from '@/admin/errors/errors'
import mockup from '@/admin/mockup/productList.json'
import Message from '@/admin/utils/message'
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
      isNew: true, // 신규 등록 여부
      filter: {},
      colors: [],
      sizes: [],
      productCategory: [],
      backupDetailData: {},
      detailData: {
        productThumbnailImages: ['', '', '', '', ''],
        firstCategoryId: null, // 1차 카테고리
        productCategoryId: null, // 2차 카테고리
        seller_property_id: 1,
        isSelling: 0, // 판먀여부
        isDisplay: 0, // 진열 여부
        productName: '', // 상품명
        brand_name_korean: '',
        gosiType: 1,
        productDetailImage: '', // 상품 상세 정보
        price: 0, // 판매가
        minimum: 1, // 최소 수량
        maximum: 20, // 최대 수량
        discountRate: 0, // 할인율
        discountPrice: 0, // 할인가
        discountStart: '', // 할인시작일
        discountEnd: '', // 할인종료일
        productOptions: [] // 옵션 상품
      }
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
    // 셀러 리스트 / 수정
    listUrl () {
      return this.prefixUrl + '/product/management'
    },
    // 셀러 리스트 / 수정
    getUrl () {
      return this.prefixUrl + '/product/management'
    },
    // 셀러 리스트 / 수정
    postUrl () {
      return this.prefixUrl + '/product/management/init'
    },
    // 셀러 리스트 / 수정
    putUrl () {
      return this.prefixUrl + '/product/management'
    },
    // 셀러 리스트 / 수정
    metaUrl () {
      return this.prefixUrl + '/product/management/init'
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
    getDetail (productId) {
      this.get(this.getUrl + '/' + productId)
        .then(res => {
          this.backupDetailData = JSON.parse(JSON.stringify(res.data.result))
          const response = JSON.parse(JSON.stringify(res.data.result))
          response.productThumbnailImages = []
          for (let i = 0; i < 5; i++) {
            if (response.productThumbnails[i] && response.productThumbnails[i].imageUrl) {
              response.productThumbnailImages[i] = response.productThumbnails[i].imageUrl
            } else {
              response.productThumbnailImages[i] = ''
            }
          }
          this.detailData = response
        })
    },
    putProduct (productId) {
      const payload = JSON.parse(JSON.stringify(this.detailData))
      payload.productThumbnailImages = payload.productThumbnailImages.filter(d => d).splice(0, 5)
      // deleteProductThumbnails 삭제 (기존에 있고, 현재 없는거)
      payload.deleteProductThumbnails = this.detailData.productThumbnails.filter(d => {
        // console.log(d.imageUrl, payload.productThumbnailImages, payload.productThumbnailImages.includes(d.imageUrl))
        if (!payload.productThumbnailImages.includes(d.imageUrl)) return true
        return false
      }).map(d => d.productThumbnailId)
      // productThumbnailImages 신규 등록
      payload.productThumbnailImages = payload.productThumbnailImages.filter(d => {
        // console.log(this.detailData.productThumbnails, d, this.detailData.productThumbnails.includes(d))
        const findList = this.detailData.productThumbnails.find(dd => dd.imageUrl === d)
        if (!findList) return true
        return false
      })
      // console.log(payload)
      this.patch(this.putUrl + '/' + productId, payload)
        .then(res => {
          Message.success('상품 수정 성공')
        })
    },
    getMeta () {
      this.get(this.metaUrl)
        .then(res => {
          this.productCategory = res.data.result.product_categories
          this.colors = res.data.result.product_colors
          this.sizes = res.data.result.product_sizes
        })
    },
    addProduct () {
      const payload = JSON.parse(JSON.stringify(this.detailData))
      payload.productThumbnailImages = payload.productThumbnailImages.filter(d => d)
      this.post(this.postUrl, payload)
        .then(response => {
          if (response.data.result.accessToken) {
            localStorage.setItem('access_token', response.data.result.accessToken)
            localStorage.setItem('user_type_id', response.data.result.userTypeId)
          }
        })
        .then(() => {
          Message.success('상품이 등록되었습니다.', () => {
          })
        })
        .catch(err => {
          if (err.response) {
            console.log(err.response)
            console.log(err.response.message)
          }
          Message.error('상품 등록에 실패하였습니다.')
        })
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
