<template>
  <div>
    <a-descriptions bordered size="small" class="seller-from" label-width="20%">
      <a-descriptions-item label="옵션정보" :span="3">

        <table class="bordered">
          <thead>
          <tr>
            <th>옵션항목</th>
            <th>상품옵션명</th>
            <th>옵션값 추가/삭제</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(item, index) in data.colors" :key="item.value">
            <td :rowspan="data.colors.length" v-if="index == 0">색상</td>
            <td>
              <a-select show-search :data-source="colors" :filter-option="filterOption" v-model="item.colorId" style="width: 100%">
                <a-select-option :value="item.value" v-for="item in colors" :key="item.value">{{item.text}}</a-select-option>
              </a-select>
            </td>
            <td>
              <a-button type="normal" @click="addColor(index)" v-show="data.colors.length < 3">+</a-button>
              <a-button type="normal" @click="popColor(index)" v-show="data.colors.length > 1">-</a-button>
            </td>
          </tr>
          <tr v-for="(item, index) in data.sizes" :key="item.value">
            <td :rowspan="data.sizes.length" v-if="index == 0">사이즈</td>
            <td>
              <a-select show-search :data-source="sizes" :filter-option="filterOption" v-model="item.sizeId" style="width: 100%">
                <a-select-option :value="item.value" v-for="item in sizes" :key="item.value">{{item.text}}</a-select-option>
              </a-select>
            </td>
            <td>
              <a-button type="normal" @click="addSize(index)" v-show="data.sizes.length < 3">+</a-button>
              <a-button type="normal" @click="popSize(index)" v-show="data.sizes.length > 1">-</a-button>
            </td>
          </tr>
          </tbody>
          <tfoot>
          <tr>
            <th>재고관리여부</th>
            <th colspan="2">
              <a-radio-group>
                <a-radio>재고 수량 관리 안함</a-radio>
                <a-radio>재고 수량 관리</a-radio>
              </a-radio-group>
            </th>
          </tr>
          </tfoot>
        </table>

        <div class="apply-buttons">
          <a-button type="info" @click="applyOptions">적용</a-button>
        </div>

        <table class="bordered">
          <thead>
          <tr>
            <th colspan="2" width="300">상품옵션정보</th>
            <th rowspan="2">일반재고</th>
            <th rowspan="2" width="70"></th>
          </tr>
          <tr>
            <th>색상</th>
            <th>사이즈</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(item, index) in dataStore.detailData.productOptions" :key="item.value">
            <td>
              <a-select show-search :data-source="colors" :filter-option="filterOption" v-model="item.colorId" style="width: 100%">
                <a-select-option :value="item.value" v-for="item in colors" :key="item.value">{{item.text}}</a-select-option>
              </a-select>
            </td>
            <td>
              <a-select show-search :data-source="sizes" :filter-option="filterOption" v-model="item.sizeId" style="width: 100%">
                <a-select-option :value="item.value" v-for="item in sizes" :key="item.value">{{item.text}}</a-select-option>
              </a-select>
            </td>
            <td>
              <a-radio-group v-model="item.inventoryYn">
                <a-radio :value="1">재고관리 안함</a-radio>
                <a-radio :value="2"><a-input style="width: 150px" suffix="개" v-model="item.stock" :disabled="item.inventoryYn == 1" /></a-radio>
              </a-radio-group>
            </td>
            <td><a-button type="danger" @click="popOption(index)">-</a-button></td>
          </tr>
          </tbody>
        </table>

      </a-descriptions-item>

    </a-descriptions>
  </div>
</template>

<script>
// import VueSelect from 'vue-select'
import 'vue-select/dist/vue-select.css'

export default {
  components: {
    // VueSelect
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
      colorList: [],
      sizeList: [],
      options: [],
      data: {
        // 샘플 데이터
        productOptions: [
          {
            colorId: 6,
            sizeId: 3,
            stock: 100
          }
        ],
        colors: [{
          colorId: ''
        }],
        sizes: [{
          sizeId: ''
        }]
      }
    }
  },
  created () {
  },
  computed: {
    colors () {
      return this.dataStore.colors.map(d => { return { text: d.name, value: d.id } })
    },
    sizes () {
      return this.dataStore.sizes.map(d => { return { text: d.name, value: d.id } })
    }
  },
  methods: {
    addColor (index) {
      this.data.colors.splice(index + 1, 0, { colorId: '' })
    },
    popColor (index) {
      this.data.colors.splice(index, 1)
    },
    addSize (index) {
      this.data.sizes.splice(index + 1, 0, { sizeId: '' })
    },
    popSize (index) {
      this.data.sizes.splice(index, 1)
    },
    filterOption (input, option) {
      return (
        option.componentOptions.children[0].text.toUpperCase().indexOf(input.toUpperCase()) >= 0
      )
    },
    applyOptions () {
      const optionList = []
      // 컬러 > 사이즈 순으로 곱하기 하기
      for (let i = 0, len = this.data.colors.length; i < len; i++) {
        for (let z = 0, len2 = this.data.sizes.length; z < len2; z++) {
          optionList.push({
            colorId: this.data.colors[i].colorId,
            sizeId: this.data.sizes[z].sizeId,
            stock: 1,
            inventoryYn: 1
          })
        }
      }
      this.dataStore.detailData.productOptions = optionList
    },
    popOption (index) {
      this.options.splice(index, 1)
    },
    getData () {
      return JSON.parse(JSON.stringify(this.data))
    }
  }
}
</script>

<style type="scss" scoped>
.normal-size {
  width: 200px;
}
table.bordered th {
  background: #fafafa;
}
table.bordered th, table.bordered td{
  border: 1px solid #e8e8e8;
  padding: 10px 15px;
  font-size: 13px;
}
.apply-buttons {
  margin: 5px 5px;
}
</style>
