import store from '@/store/index'
import _ from 'lodash'

export default {
  store: store,
  computed: {
    constants () {
      return this.$store.state.const
    }
  },
  methods: {
    isMaster () {
      return localStorage.getItem('user_type_id') === '3' || localStorage.getItem('user_type_id') === 3
    },
    isSeller () {
      return localStorage.getItem('user_type_id') === '2' || localStorage.getItem('user_type_id') === 2
    },
    difference (object, base) {
      function changes (object, base) {
        return _.transform(object, function (result, value, key) {
          if (!_.isEqual(value, base[key])) {
            result[key] = (_.isObject(value) && _.isObject(base[key])) ? changes(value, base[key]) : value
          }
        })
      }
      return changes(object, base)
    }
  }
}
