import store from '@/store/index'

export default {
  store: store,
  computed: {
    constants () {
      return this.$store.state.const
    }
  },
  methods: {

  }
}
