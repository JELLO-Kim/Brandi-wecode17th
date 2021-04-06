<template>
  <div>
    <a-descriptions bordered size="small" class="seller-from" label-width="20%">
      <a-descriptions-item :span="3">
        <template slot="label">
          셀러 프로필 <span class="required">*</span>
        </template>
        <image-upload v-model="dataStore.detailData.profile" />
      </a-descriptions-item>
      <a-descriptions-item label="셀러 상태" :span="3">
        {{ dataStore.detailData.sellerStatus }}
        <!-- {{ getSellerStatusName(dataStore.detailData.seller_status_id) }} -->
      </a-descriptions-item>
      <a-descriptions-item label="셀러 속성" :span="3" v-if="isMaster()">
        <a-radio-group v-model="dataStore.detailData.sellerCategoryId">
          <a-radio v-for="item in constants.sellerSections" :value="item.value" :key="item.value">{{ item.label }}</a-radio>
        </a-radio-group>
      </a-descriptions-item>
      <a-descriptions-item label="셀러 한글명" :span="3">
        <a-input placeholder="셀러 한글명" class="normal-size" v-model="dataStore.detailData.brandKorean" />
      </a-descriptions-item>
      <a-descriptions-item label="셀러 영문명" :span="3">
        <a-input placeholder="셀러 영문명" class="normal-size" v-model="dataStore.detailData.brandEnglish" />
      </a-descriptions-item>
    </a-descriptions>
  </div>
</template>

<script>
import CommonMixin from '@/admin/mixins/common-mixin'
import ImageUpload from '@/admin/Components/Common/image-upload'
export default {
  mixins: [CommonMixin],
  components: {
    ImageUpload
  },
  props: {
    dataStore: {
      default () {
        return {}
      }
    }
  },
  data () {
    return {
      filter: {
        seller_property_id: 1,
        brand_name_english: '',
        brand_name_korean: ''
      }
    }
  },
  computed: {
    constants () {
      return this.$store.state.const
    }
  },
  methods: {
    setFormData (value) {

    },
    getFromData () {
      return JSON.stringify(JSON.parse(this.filter))
    },
    validate () {
      return true
    },
    getSellerStatusName (statusId) {
      const statusItem = this.constants.sellerStatus.filter((d) => { return d.value === statusId })
      if (statusItem.length > 0) return statusItem[0].label
      return ''
    }

  }
}
</script>

<style type="scss" scoped>
.normal-size {
  width: 200px;
}
.required {
  color: red
}
</style>
