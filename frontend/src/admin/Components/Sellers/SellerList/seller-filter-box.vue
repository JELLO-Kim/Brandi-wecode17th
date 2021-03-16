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
        <a-col :span="2" class="filter-label">셀러한글명</a-col>
        <a-col :span="7"><a-input-search placeholder="검색어를 입력해주세요." v-model="filter.brand_name_korean"/></a-col>
        <a-col :span="8">
          <a-input-group compact>
            <a-select v-model="filter.keywordType">
              <a-select-option value="">Select... &nbsp;&nbsp;&nbsp;</a-select-option>
              <a-select-option v-for="item in items" :key="item.value" :value="item.value">{{ item.label }}</a-select-option>
            </a-select>
            <a-input-search placeholder="검색어를 입력해주세요." v-model="filter.keywordValue" style="width: 70%"/>
          </a-input-group>
        </a-col>
      </a-row>
      <a-row :gutter="8" class="filter-row">
        <a-col :span="2" class="filter-label">셀러속성</a-col>
        <a-col :span="22">
          <multi-select-buttons :multiple-select="false" :items="constants.sellerSections" v-model="filter.property_id"/>
        </a-col>
      </a-row>
      <a-row :gutter="8" class="filter-row">
        <a-col :span="2" class="filter-label">셀러상태</a-col>
        <a-col :span="22">
          <multi-select-buttons :multiple-select="false" :items="constants.sellerStatus" v-model="filter.status_id"/>
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

export default {
  name: 'seller-filter-box',
  components: { MultiSelectButtons },
  data () {
    /*
      number  : 번호(id)
      account  : 계정
      brand_name_korean  :  브랜드한글명
      brand_name_english  :  브랜드영어명
      manager_name  :  담당자이름
      manager_number  :  담당자번호
      manager_email   :   담당자이메일
      status_id   :  입점상태id (입점, 휴점, …)
      property_id  :  셀러속성id  ( 로드샵, 마켓 …)
      start_date  :  시작일자
      end_date   :   마지막일자
       */
    return {
      filter: {
        property_id: [],
        status_id: [],
        brand_name_korean: '',
        keywordType: '',
        keywordValue: '',
        rangeDate: null
      },
      items: [
        { label: '셀러번호', value: 'number' },
        { label: '셀러아이디', value: 'account' },
        { label: '셀러영문명', value: 'brand_name_english' },
        { label: '담당자이름', value: 'brand_name_korean' },
        { label: '담당자연락처', value: 'phone_number' },
        { label: '담당자이메일', value: 'email' }
      ]
    }
  },
  computed: {
    constants () {
      return this.$store.state.const
    }
  },
  created () {
    // 리셋 기능을 위해 clone 데이터 생성
    this.backupFilter = JSON.parse(JSON.stringify(this.filter))
  },
  mounted () {
  },
  methods: {
    search () {
      const filter = this.getFilter()
      this.$emit('search', filter)
    },
    changeDatePicker (v) {
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
      if (filter.status_id.length > 0) {
        filter.status_id = filter.status_id[0]
      }
      if (filter.property_id.length > 0) {
        filter.property_id = filter.property_id[0]
      }
      delete filter.keywordType
      delete filter.keywordValue
      delete filter.rangeDate
      return filter
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
