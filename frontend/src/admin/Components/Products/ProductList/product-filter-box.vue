<template>
  <div>
    <a-input-group>
      <a-row :gutter="8" class="filter-row">
        <a-col :span="2" class="filter-label">조회기간</a-col>
        <a-col :span="7">
          <a-range-picker @change="changeDatePicker" :placeholder="['시작일', '종료일']" v-model="filter.rangeDate" />
        </a-col>
      </a-row>
      <a-row :gutter="8" class="filter-row">
        <a-col :span="2" class="filter-label">셀러명</a-col>
        <a-col :span="7"><a-input-search placeholder="검색어를 입력해주세요." v-model="filter.brand_name_korean"/></a-col>
        <a-col :span="7">
          <a-input-group compact>
            <a-select v-model="filter.keywordType">
              <a-select-option value="">Select...</a-select-option>
              <a-select-option v-for="item in items" :key="item.value" :value="item.value">{{ item.label }}</a-select-option>
            </a-select>
            <a-input-search placeholder="검색어를 입력해주세요." v-model="filter.keywordValue" style="width: 70%"/>
          </a-input-group>
        </a-col>
      </a-row>
      <a-row :gutter="8" class="filter-row">
        <a-col :span="2" class="filter-label">셀러속성</a-col>
        <a-col :span="22">
          <multi-select-buttons :multiple-select="true" :items="constants.sellerSections" v-model="filter.seller_property_id"/>
        </a-col>
      </a-row>
      <a-row :gutter="8" class="filter-row">
        <a-col :span="2" class="filter-label">판매여부</a-col>
        <a-col :span="7">
          <multi-select-buttons :multiple-select="false" :items="constants.saleTypes" v-model="filter.is_sell"/>
        </a-col>
        <a-col :span="2" class="filter-label">진열여부</a-col>
        <a-col :span="7">
          <multi-select-buttons :multiple-select="false" :items="constants.exhibitTypes" v-model="filter.is_display"/>
        </a-col>
      </a-row>
      <a-row :gutter="8" class="filter-row">
        <a-col :span="2" class="filter-label">할인여부</a-col>
        <a-col :span="7">
          <multi-select-buttons :multiple-select="false" :items="constants.discountTypes" v-model="filter.is_discount"/>
        </a-col>
      </a-row>
    </a-input-group>
    <div class="search-buttons">
      <a-button type="primary" size="large" @click="search">검색</a-button>
      <a-button type="normal" size="large" @click="resetFilter">초기화</a-button>
    </div>
  </div>
</template>

<script>
import MultiSelectButtons from '@/admin/Components/Common/multi-select-buttons'
import CommonMixin from '@/admin/mixins/common-mixin'

export default {
  name: 'product-filter-box',
  mixins: [CommonMixin],
  components: { MultiSelectButtons },
  data () {
    return {
      filter: {
        seller_property_id: [],
        is_sell: [],
        is_display: [],
        is_discount: [],
        brand_name_korean: '',
        keywordType: '',
        keywordValue: '',
        rangeDate: null
      },
      items: [
        { label: '상품명', value: 'name' },
        { label: '상품코드', value: 'code_number' },
        { label: '상품번호', value: 'product_id' }
      ]
    }
  },
  computed: {
  },
  created () {
    // 리셋 기능을 위해 clone 데이터 생성
    this.backupFilter = JSON.parse(JSON.stringify(this.filter))
  },
  mounted () {
    this.search()
  },
  methods: {
    search () {
      const filter = this.getFilter()
      this.$emit('search', filter)
    },
    getFilter () {
      const filter = JSON.parse(JSON.stringify(this.filter))
      if (filter.keywordType && filter.keywordValue) {
        filter[filter.keywordType] = filter.keywordValue
      }
      if (this.filter.rangeDate && this.filter.rangeDate.length === 2) {
        filter.start_date = this.filter.rangeDate[0].format('YYYY-MM-DD')
        filter.end_date = this.filter.rangeDate[1].format('YYYY-MM-DD')
      }
      if (filter.is_discount.length > 0) {
        filter.is_discount = filter.is_discount[0]
      }
      if (filter.is_sell.length > 0) {
        filter.is_sell = filter.is_sell[0]
      }
      if (filter.is_display.length > 0) {
        filter.is_display = filter.is_display[0]
      }
      if (filter.seller_property_id.length > 0) {
        filter.seller_property_id = filter.seller_property_id[0]
      }
      if (!filter.brand_name_korean) { delete filter.brand_name_korean }
      delete filter.keywordType
      delete filter.keywordValue
      delete filter.rangeDate
      return filter
    },
    changeDatePicker (v) {
    },
    resetFilter () {
      this.filter = JSON.parse(JSON.stringify(this.backupFilter))
      this.search()
    }
  }
}
</script>

<style scoped>
.search-buttons {
  text-align: center;
  margin: 10px 0;
}
.filter-row {
  height: 32px;
  margin: 5px 0;
}
.filter-label {
  font-weight: bold;
  text-indent: 5px;
}
</style>
