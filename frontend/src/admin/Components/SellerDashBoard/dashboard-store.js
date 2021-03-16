import store from '@/store/index'
// import axios from 'axios'
import AdminApiMixin from '@/admin/mixins/admin-api'
import { Modal } from 'ant-design-vue'

export default {
  store: store,
  mixins: [AdminApiMixin],
  data () {
    return {
      dashboardData: {},
      loading: false
    }
  },
  created () {
    this.load()
  },
  computed: {
    constants () {
      return this.$store.state.const
    },
    // 셀러 대시보드 경로
    dashBoardUrl () {
      return this.constants.apiDomain + '/home'
    }
  },
  methods: {
    load () {
      this.loading = true
      const params = {}
      this.get(this.dashBoardUrl, {
        params: params
      })
        .then((res) => {
          if (res.data) {
            this.dashboardData = res.data
          } else {
            Modal.error({
              content: '통신 실패'
            })
          }
        }).catch((e) => {
          if (e.code === 'ECONNABORTED') {
            Modal.error({
              content: '요청 시간을 초과 하였습니다. 다시 시도해주시기 바랍니다.'
            })
          } else {
            Modal.error({
              content: '처리 중 오류 발생'
            })
          }
        }).then((res) => {
          this.loading = false
        })
    }
  }
}
