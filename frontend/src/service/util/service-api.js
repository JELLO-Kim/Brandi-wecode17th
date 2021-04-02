import axios from 'axios'
import store from '@/store/index'
// import getToken from '@/store/modules/serviceStore'

export default {
  store: store,
  computed: {
    constants () {
      return this.$store.state.const
    }
  },
  methods: {
    get (url, config) {
      config = this.cloneAndAuthHeader(config)
      return axios.get(url, config)
    },
    post (url, data, config) {
      config = this.cloneAndAuthHeader(config)
      return axios.post(url, data, config)
    },
    delete (url, config) {
      config = this.cloneAndAuthHeader(config)
      return axios.delete(url, config)
    },
    cloneAndAuthHeader (config) {
      if (config === undefined) {
        config = {}
      } else {
        config = JSON.parse(JSON.stringify(config))
      }

      if (config.headers === undefined) {
        config.headers = {}
      }
      config.headers.authorization = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo5Nn0.Pr0585D-dkyqc-bjQIHtQZAJlalJsv59QPeLoCYMWkw'
      config.timeout = 10000
      return config
    }
  }
}
